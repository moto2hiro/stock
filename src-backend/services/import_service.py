from datetime import datetime
from typing import List, Any, Dict
from alpaca_trade_api.entity import BarSet, Bars
from app_consts import AppConsts
from app_utils.log_utils import LogUtils
from app_utils.number_utils import NumberUtils
from app_utils.string_utils import StringUtils
from clients.alpaca_client import AlpacaClient
from clients.iex_cloud_client import IexCloudClient
from clients.email_client import EmailClient
from exceptions.not_found_exception import NotFoundException
from models.db.symbol_master import SymbolMaster
from models.db.stock_price_daily import StockPriceDaily
from models.db.etf_price_daily import EtfPriceDaily
from services.base_service import BaseService
from services.stock_service import StockService


class ImportService(BaseService):

  def __init__(self) -> None:
    super().__init__()
    self.__alpaca_client: AlpacaClient = AlpacaClient()
    self.__iex_cloud_client: IexCloudClient = IexCloudClient()
    self.__email_client: EmailClient = EmailClient()
    self.__stock_service: StockService = StockService()

  def import_prices(self, limit: int = 100) -> int:
    results: Dict = {
        'stock_prices': [],
        'etf_prices': [],
        'missing_symbols': [],
        'errors': []
    }
    try:
      symbol_masters: List[SymbolMaster] = self.__stock_service.get_symbols(instrument='', exclude_status=[AppConsts.SYMBOL_STATUS_ARCHIVED])
      symbols: List[str] = [s.symbol for s in symbol_masters]
      price_set: BarSet = self.__alpaca_client.get_prices(symbols, limit)

      if not price_set:
        raise NotFoundException('BarSet', 'symbols', '')

      for symbol in symbol_masters:
        LogUtils.debug('start {0}'.format(symbol.symbol))

        prices: Bars = price_set[symbol.symbol]
        if not prices:
          LogUtils.warning('{0} price not found.'.format(symbol))
          results['missing_symbols'].append(symbol.symbol)
          continue

        for price in prices:
          price_date: datetime = price.t.to_pydatetime()
          data: tuple = (
              symbol.id,
              price_date,
              NumberUtils.to_float(price.o),
              NumberUtils.to_float(price.h),
              NumberUtils.to_float(price.l),
              NumberUtils.to_float(price.c),
              NumberUtils.to_int(price.v),
          )
          if symbol.instrument == AppConsts.INSTRUMENT_STOCK:
            org: StockPriceDaily = self.__stock_service.get_single_stock_price_daily(symbol.id, price_date)
            if not org:
              results['stock_prices'].append(data)
          else:
            org: EtfPriceDaily = self.__stock_service.get_single_etf_price_daily(symbol.id, price_date)
            if not org:
              results['etf_prices'].append(data)
      if results['stock_prices']:
        BaseService._insert_bulk(StockPriceDaily, results['stock_prices'])
      if results['etf_prices']:
        BaseService._insert_bulk(EtfPriceDaily, results['etf_prices'])
    except NotFoundException as ex:
      results['errors'].append(ex)
    except Exception as ex:
      results['errors'].append(ex)
    finally:
      self.__email_client.send_html(
          subject=AppConsts.EMAIL_SUBJECT_IMPORT_PRICES,
          template_path=AppConsts.TEMPLATE_PATH_IMPORT_PRICES,
          model=results)
      if results['errors']:
        for error in results['errors']:
          LogUtils.error('Import Price Error', error)
      return 1

  def import_company_profiles(self) -> int:
    symbol_masters: List[SymbolMaster] = self.__stock_service.get_symbols(instrument='', exclude_status=[AppConsts.SYMBOL_STATUS_ARCHIVED])
    symbols: List[str] = [s.symbol for s in symbol_masters]
    company_profiles: List[Dict] = self.__iex_cloud_client.get_company_profiles(symbols)

    for profile in company_profiles:
      symbol: str = profile.get('symbol')
      name: str = profile.get('companyName')
      sector: str = profile.get('sector')
      industry: str = profile.get('industry')
      org: SymbolMaster = self.__stock_service.get_symbol(symbol, AppConsts.INSTRUMENT_STOCK)
      if not org:
        LogUtils.warning('{0} not found.'.format(symbol))
      else:
        LogUtils.debug('Updating {0}'.format(symbol))
        org.name = name if name != '' else org.name
        org.sector = sector if sector != '' else org.sector
        org.industry = industry if industry != '' else org.industry
        BaseService._update()

  def import_symbols(self) -> int:
    new_symbols: List[SymbolMaster] = self.__stock_service.get_sp500_mismatches(True)
    for new_symbol in new_symbols:
      org: SymbolMaster = self.__stock_service.get_symbol(new_symbol.symbol, AppConsts.INSTRUMENT_STOCK)
      if not org:
        new_symbol.status = AppConsts.SYMBOL_STATUS_INIT
        new_symbol.instrument = AppConsts.INSTRUMENT_STOCK
        BaseService._insert(new_symbol)
    self.import_company_profiles()
    return 1

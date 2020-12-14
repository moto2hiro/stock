from datetime import date, datetime, timedelta
from random import randint, shuffle
from typing import List, Any

import numpy as np
import pandas as pd
from numpy import ndarray
from pandas._libs.tslibs.timestamps import Timestamp
from pandas.core.frame import DataFrame
from pandas.core.series import Series

from app_consts import AppConsts
from app_db import db
from app_utils.date_utils import DateUtils
from app_utils.log_utils import LogUtils
from app_utils.number_utils import NumberUtils
from app_utils.string_utils import StringUtils
from clients.crawl_client import CrawlClient
from clients.email_client import EmailClient
from exceptions.bad_request_exception import BadRequestException
from exceptions.not_found_exception import NotFoundException
from models.db.etf_price_daily import EtfPriceDaily as EPD
from models.db.financial import Financial as FN
from models.db.stock_price_daily import StockPriceDaily as SPD
from models.db.symbol_master import SymbolMaster as SM
from models.db.vw_symbol_stock_price_daily import VwSymbolStockPriceDaily as VSPD
from models.db.vw_symbol_etf_price_daily import VwSymbolEtfPriceDaily as VEPD
from models.request_models.chart_request import ChartRequest as CR
from models.stock_price_custom import StockPriceCustom as SPC
from services.base_service import BaseService
from services.calc_service import CalcService
from services.strategies.base_strategy_service import BaseStrategyService
from services.strategies.demo_strategy_service import DemoStrategyService
from services.strategies.abz_strategy_service import AbzStrategyService
from services.strategies.double_bollinger_bands_strategy_service import DoubleBollingerBandsStrategyService
from services.strategies.double_bottoms_strategy_service import DoubleBottomsStrategyService
from services.strategies.double_tops_strategy_service import DoubleTopsStrategyService
from services.strategies.inverted_head_and_shoulders_strategy_service import InvertedHeadAndShouldersStrategyService
from services.strategies.sma_crossover_strategy_service import SmaCrossoverStrategyService
from services.strategies.turnaround_tuesday_strategy_service import TurnaroundTuesdayStrategyService
from services.strategies.tema_and_vwma_strategy_service import TEMAandVWMAStrategyService
pd.options.mode.chained_assignment = None


class StockService(BaseService):
  def __init__(self) -> None:
    super().__init__()
    self.__calc_service = CalcService()
    self.__crawl_client: CrawlClient = CrawlClient()
    self.__email_client: EmailClient = EmailClient()

  def get_symbol(self, symbol: str, instrument: str) -> SM:
    if StringUtils.isNullOrWhitespace(symbol):
      return None
    symbol = symbol.strip().upper()
    return BaseService._get_first(SM, [
        SM.symbol == symbol,
        SM.instrument == instrument
    ])

  def get_symbols(self, instrument: str = '', exclude_status: List[int] = []) -> List[SM]:
    query = db.session.query(SM)
    if instrument != '':
      query = query.filter(SM.instrument == instrument)
    for status in exclude_status:
      query = query.filter(SM.status.op('|')(status) != SM.status)
    query = query.order_by(SM.symbol)
    return query.all()

  def update_symbol(self, model: SM) -> int:
    if not model:
      raise BadRequestException()
    org_symbol: SM = self.get_symbol(model.symbol, model.instrument)
    if not org_symbol:
      raise NotFoundException(model.__class__.__name__, 'symbol', model.symbol)
    org_symbol.name = model.name
    org_symbol.status = model.status
    BaseService._update()
    return 1

  def delete_old_prices(self) -> int:
    error: Exception = None
    try:
      thirty_years_ago: datetime = datetime.now() - timedelta(days=365*30)
      LogUtils.debug('Deleting stock price older than {0}'.format(thirty_years_ago))
      db.session.query(SPD).filter(SPD.price_date <= thirty_years_ago).delete()
      db.session.commit()
    except Exception as ex:
      error = ex
    finally:
      self.__email_client.send_html(
          subject=AppConsts.EMAIL_SUBJECT_DELETE_PRICES,
          template_path=AppConsts.TEMPLATE_PATH_DELETE_PRICES,
          model={'errors': [error] if error else []})
      if error:
        LogUtils.error('Delete Price Error', error)
    return 1

  def get_single_stock_price_daily(self, symbol_id: int, price_date: date) -> SPD:
    return BaseService._get_first(SPD, [
        SPD.symbol_id == symbol_id,
        SPD.price_date == price_date
    ])

  def get_last_single_stock_price_daily(self, symbol_id: int) -> SPD:
    return db.session.query(SPD).filter(SPD.symbol_id == symbol_id).order_by(SPD.price_date.desc()).first()

  def get_single_etf_price_daily(self, symbol_id: int, price_date: date) -> SPD:
    return BaseService._get_first(EPD, [
        EPD.symbol_id == symbol_id,
        EPD.price_date == price_date
    ])

  def get_vw_symbol_spd_as_df(
          self,
          symbol_id: int = None,
          symbol_ids: List = None,
          date_from: date = None,
          date_to: date = None) -> DataFrame:
    query = db.session.query(VSPD)
    if symbol_id and symbol_id > 0:
      query = query.filter(VSPD.symbol_id == symbol_id)
    if symbol_ids and len(symbol_ids) > 0:
      query = query.filter(VSPD.symbol_id.in_(symbol_ids))
    if date_from:
      query = query.filter(VSPD.price_date >= date_from)
    if date_to:
      query = query.filter(VSPD.price_date <= date_to)
    return pd.read_sql(
        sql=query.statement,
        con=db.session.bind,
        index_col=[AppConsts.PRICE_COL_SYMBOL_ID, AppConsts.PRICE_COL_DATE])

  def get_vw_symbol_epd_as_df(
          self,
          symbol_id: int = None,
          symbol_ids: List = None,
          date_from: date = None,
          date_to: date = None) -> DataFrame:
    query = db.session.query(VEPD)
    if symbol_id and symbol_id > 0:
      query = query.filter(VEPD.symbol_id == symbol_id)
    if symbol_ids and len(symbol_ids) > 0:
      query = query.filter(VEPD.symbol_id.in_(symbol_ids))
    if date_from:
      query = query.filter(VEPD.price_date >= date_from)
    if date_to:
      query = query.filter(VEPD.price_date <= date_to)
    return pd.read_sql(
        sql=query.statement,
        con=db.session.bind,
        index_col=[AppConsts.PRICE_COL_SYMBOL_ID, AppConsts.PRICE_COL_DATE])

  def get_stock_prices_daily(
          self,
          symbol_id: int,
          date_from: date = None,
          date_to: date = None) -> List[SPD]:
    query = db.session.query(SPD)
    if symbol_id > 0:
      query = query.filter(SPD.symbol_id == symbol_id)
    if date_from:
      query = query.filter(SPD.price_date >= date_from)
    if date_to:
      query = query.filter(SPD.price_date <= date_to)
    return query.order_by(SPD.price_date).all()

  def get_etf_prices_daily(
          self,
          symbol_id: int,
          date_from: date = None,
          date_to: date = None) -> List[EPD]:
    query = db.session.query(EPD)
    if symbol_id > 0:
      query = query.filter(EPD.symbol_id == symbol_id)
    if date_from:
      query = query.filter(EPD.price_date >= date_from)
    if date_to:
      query = query.filter(EPD.price_date <= date_to)
    return query.order_by(EPD.price_date).all()

  def get_financial(self, symbol_id: int, year: int, quarter: int) -> FN:
    return BaseService._get_first(FN, [
        FN.symbol_id == symbol_id,
        FN.year == year,
        FN.quarter == quarter])

  def get_price_dataframe(self, prices: List[Any]) -> DataFrame:
    if not prices \
            or not isinstance(prices, List) \
            or not isinstance(prices[0], (SPD, EPD)):
      return None
    df: DataFrame = pd.DataFrame(data=[
        [
            p.id,
            p.symbol_id,  # idx = 0, 0
            p.price_date,  # idx = 0, 1
            NumberUtils.to_float(p.open_price),
            NumberUtils.to_float(p.high_price),
            NumberUtils.to_float(p.low_price),
            NumberUtils.to_float(p.close_price),
            p.volume
        ] for p in prices], columns=AppConsts.PRICE_COLS)
    df = df.set_index([AppConsts.PRICE_COL_SYMBOL_ID, AppConsts.PRICE_COL_DATE])
    return df

  def get_strategy_service(self, strategy_type: str, strategy_request: Any, symbols: List[SM], prices: DataFrame) -> BaseStrategyService:
    if strategy_type == AppConsts.STRATEGY_DEMO:
      return DemoStrategyService(strategy_request, symbols, prices)
    if strategy_type == AppConsts.STRATEGY_ABZ:
      return AbzStrategyService(strategy_request, symbols, prices)
    if strategy_type == AppConsts.STRATEGY_DBB:
      return DoubleBollingerBandsStrategyService(strategy_request, symbols, prices)
    if strategy_type == AppConsts.STRATEGY_DOUBLE_BOTTOMS:
      return DoubleBottomsStrategyService(strategy_request, symbols, prices)
    if strategy_type == AppConsts.STRATEGY_DOUBLE_TOPS:
      return DoubleTopsStrategyService(strategy_request, symbols, prices)
    if strategy_type == AppConsts.STRATEGY_INVERTED_HEAD_AND_SHOULDERS:
      return InvertedHeadAndShouldersStrategyService(strategy_request, symbols, prices)
    if strategy_type == AppConsts.STRATEGY_SMA_CROSSOVER:
      return SmaCrossoverStrategyService(strategy_request, symbols, prices)
    if strategy_type == AppConsts.STRATEGY_TURNAROUND_TUESDAY:
      return TurnaroundTuesdayStrategyService(strategy_request, symbols, prices)
    if strategy_type == AppConsts.STRATEGY_TEMA_AND_VWMA:
      return TEMAandVWMAStrategyService(strategy_request, symbols, prices)
    return None

  def get_dates(self, prices: DataFrame, start_date: date, end_date: date) -> DataFrame:
    if prices.empty \
            or not start_date \
            or not end_date \
            or start_date > end_date \
            or not AppConsts.PRICE_COL_DATE in prices.index.names:
      return None
    dates: DataFrame = pd.DataFrame(prices.index.get_level_values(AppConsts.PRICE_COL_DATE).unique())
    dates = dates.loc[(dates[AppConsts.PRICE_COL_DATE] >= start_date) & (dates[AppConsts.PRICE_COL_DATE] <= end_date)]
    dates[AppConsts.CUSTOM_COL_PREV_DATE] = dates[AppConsts.PRICE_COL_DATE].shift(1)
    dates[AppConsts.CUSTOM_COL_NEXT_DATE] = dates[AppConsts.PRICE_COL_DATE].shift(-1)
    dates[AppConsts.CUSTOM_COL_NEXT_NEXT_DATE] = dates[AppConsts.PRICE_COL_DATE].shift(-2)
    return dates

  def get_no_of_shares(
          self,
          capital: float,
          pct_risk_per_trade: float,
          volume_limit: float,
          price: Series,
          slippage: int = None,
          is_slip_up: bool = True) -> int:
    if not AppConsts.PRICE_COL_OPEN in price.index \
            or not AppConsts.CUSTOM_COL_ADV in price.index:
      return 0
    open_price: float = price.loc[AppConsts.PRICE_COL_OPEN]
    if slippage:
      if is_slip_up:
        open_price = NumberUtils.round(open_price + (open_price * AppConsts.BASIS_POINT * slippage))
      else:
        open_price = NumberUtils.round(open_price - (open_price * AppConsts.BASIS_POINT * slippage))

    no_of_shares: int = NumberUtils.to_floor(capital * pct_risk_per_trade / 100 / open_price)
    adv: float = price.loc[AppConsts.CUSTOM_COL_ADV] if price.loc[AppConsts.CUSTOM_COL_ADV] > 0 else price.loc[AppConsts.PRICE_COL_VOLUME]
    max_volume: float = NumberUtils.to_int(adv * volume_limit / 100)
    if no_of_shares > max_volume:
      LogUtils.warning('Capping max_volume adv={0}, no_of_shares={1}, max_volume={2}'.format(adv, no_of_shares, max_volume))
      no_of_shares = max_volume
    return no_of_shares

  def get_sample_prices_for_charts(self, req: CR) -> List[List[SPC]]:
    LogUtils.debug('START')
    ret: List[List[SPC]] = []
    if not req or not req.is_valid_model():
      raise BadRequestException()

    # region Init Symbols
    symbols: List[SymbolMaster] = self.get_symbols(AppConsts.INSTRUMENT_STOCK)
    if req.is_random_symbols:
      shuffle(symbols)
      symbols = symbols[:req.no_of_charts * 5]
    else:
      symbols = [s for s in symbols if s.symbol == req.symbol.upper()]
    if not symbols:
      return ret
    symbol_ids: List[int] = [symbol.id for symbol in symbols]
    # endregion

    LogUtils.debug('Symbols count={0}'.format(len(symbol_ids)))

    # region Init Prices
    prices = self.get_vw_symbol_spd_as_df(
        symbol_ids=symbol_ids,
        date_from=(req.date_from_obj - timedelta(days=300)),  # for sma (will filter later)
        date_to=req.date_to_obj)
    # endregion

    LogUtils.debug('Prices Init Shape={0}'.format(prices.shape))

    prices[AppConsts.CUSTOM_COL_PV] = prices[AppConsts.PRICE_COL_CLOSE] * prices[AppConsts.PRICE_COL_VOLUME]
    prices[AppConsts.CUSTOM_COL_ADPV] = 0

    for symbol in symbols:
      symbol_prices: DataFrame = prices.loc[[symbol.id]]
      if symbol_prices.empty:
        continue

      # region ADPV (50)
      adpvs: Series = symbol_prices[AppConsts.CUSTOM_COL_PV].rolling(window=50).mean()
      prices[AppConsts.CUSTOM_COL_ADPV].update(adpvs)
      adpv: float = adpvs.tail(1)[0]
      if adpv < AppConsts.ADPV_MIN_DFLT:
        continue
      symbol_prices = prices.loc[[symbol.id]]
      # endregion

      LogUtils.debug('START-Symbol={0},ADPV={1}'.format(symbol.symbol, adpv))

      # SMA
      prices = self.__calc_service.append_sma(
          prices=prices,
          index=[symbol.id],
          sma_period=req.sma_period_1,
          sma_column_name=AppConsts.CUSTOM_COL_SMA_PERIOD_1)
      prices = self.__calc_service.append_sma(
          prices=prices,
          index=[symbol.id],
          sma_period=req.sma_period_2,
          sma_column_name=AppConsts.CUSTOM_COL_SMA_PERIOD_2)

      # Exponential Price Smoothing
      prices = self.__calc_service.append_exponential_smoothing_price(
          prices=prices,
          index=[symbol.id],
          alpha=req.exponential_smoothing_alpha)

      # Exponential Price Smoothing Max/Min
      prices = self.__calc_service.append_exponential_smoothing_max_min(
          prices=prices,
          index=[symbol.id],
          exponential_smoothing_max_min_diff=req.exponential_smoothing_max_min_diff)

      # Double Bottom
      prices = self.__calc_service.append_double_bottoms(
          prices=prices,
          index=[symbol.id],
          price_column=AppConsts.PRICE_COL_CLOSE,
          smooth_price_column=AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE,
          max_column=AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_MAX,
          min_column=AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_MIN,
          double_bottoms_diff=5)

      # ABZ
      prices = self.__calc_service.append_abz(
          prices=prices,
          index=[symbol.id],
          abz_er_period=req.abz_er_period,
          abz_std_distance=req.abz_std_distance,
          abz_constant_k=req.abz_constant_k)

      symbol_prices = prices.loc[[symbol.id]]
      ret.append([SPC(i, row) for i, row in symbol_prices[symbol_prices.index.get_level_values(AppConsts.PRICE_COL_DATE) >= req.date_from_obj].iterrows()])
      if len(ret) == req.no_of_charts:
        return ret

    LogUtils.debug('END')
    return ret

  def get_sp500_mismatches(self, is_missing: bool) -> None:
    ret: List[SM] = []
    db_symbol_masters: List[SM] = self.get_symbols(AppConsts.INSTRUMENT_STOCK, [AppConsts.SYMBOL_STATUS_ARCHIVED])
    if not db_symbol_masters:
      return ret
    sp500_df: DataFrame = self.__crawl_client.get_html_table(AppConsts.WIKI_SP500_URL, AppConsts.WIKI_SP500_ELEMENT_ID, [AppConsts.WIKI_SP500_COL_SYMBOL])
    db_symbols: List[str] = [s.symbol for s in db_symbol_masters]

    if is_missing:
      # Get SP500 symbols not in db
      for idx, row in sp500_df.iterrows():
        if idx and not idx.strip().upper() in db_symbols:
          tmp: SM = SM()
          tmp.symbol = idx.strip().upper()
          tmp.name = row.loc[AppConsts.WIKI_SP500_COL_SYMBOL_NAME]
          ret.append(tmp)
    else:
      # Get symbols in db that is not SP500
      for symbol in db_symbol_masters:
        if not symbol.symbol in sp500_df.index:
          ret.append(symbol)
    return ret

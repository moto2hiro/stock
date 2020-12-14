from typing import List, Dict, Any
from datetime import date
from app_db import db
from app_consts import AppConsts
from app_utils.log_utils import LogUtils
from app_utils.csv_utils import CsvUtils
from app_utils.file_utils import FileUtils
from app_utils.date_utils import DateUtils
from app_utils.string_utils import StringUtils
from app_utils.number_utils import NumberUtils
from services.base_service import BaseService
from services.stock_service import StockService
from models.db.symbol_master import SymbolMaster as SM
from models.db.financial import Financial as FN
from models.db.stock_price_daily import StockPriceDaily as SPD
from models.db.etf_price_daily import EtfPriceDaily as EPD


class ImportCsvService(BaseService):

  def __init__(self) -> None:
    super().__init__()
    self.__stock_service = StockService()

# region KIBOT

  def import_from_csv_symbols(self) -> str:
    files: List[str] = FileUtils.get_files(AppConsts.STOCK_PRICE_FOLDER)
    for file in files:
      symbol: str = FileUtils.get_wo_ext(file)
      org_symbol: SM = self.__stock_service.get_symbol(symbol, AppConsts.INSTRUMENT_STOCK)
      if org_symbol:
        continue
      LogUtils.debug('Inserting {0}.'.format(symbol))
      BaseService._insert(SM(
          symbol=symbol,
          name='',
          status=AppConsts.SYMBOL_STATUS_INIT,
          instrument=AppConsts.INSTRUMENT_STOCK))
    return "1"

  def import_from_csv_prices(self) -> str:
    BaseService._truncate(SPD)

    files: List[str] = FileUtils.get_files(AppConsts.STOCK_PRICE_FOLDER, is_full=True)
    for file in files:
      symbol: str = FileUtils.get_wo_ext(FileUtils.get_base_name(file))
      org_symbol: SM = self.__stock_service.get_symbol(symbol, AppConsts.INSTRUMENT_STOCK)
      if not org_symbol:
        continue
      records: List[List[str]] = CsvUtils.parse_as_list(file)
      if not records:
        continue
      for record in records:
        record[AppConsts.KIBOT_IDX_DATE] = DateUtils.get_date(record[AppConsts.KIBOT_IDX_DATE],
                                                              AppConsts.KIBOT_DATE_FORMAT)
        record.insert(0, org_symbol.id)
      BaseService._insert_bulk(SPD, records)
    return "1"

# endregion

# region INTRINIO

  def import_from_csv_companynames(self) -> str:
    file: str = FileUtils.get_file(AppConsts.INCOME_STMT_FILE)
    records: List[Dict] = CsvUtils.parse_as_dict(file)
    curr_symbol: str = ''
    for record in records:
      symbol: str = record.get(AppConsts.INTRINIO_KEY_INC_STMT_TICKER)
      company_name: str = record.get(AppConsts.INTRINIO_KEY_INC_STMT_NAME)
      if symbol == curr_symbol or StringUtils.isNullOrWhitespace(company_name):
        continue
      curr_symbol = symbol
      org_symbol: SM = self.__stock_service.get_symbol(curr_symbol, AppConsts.INSTRUMENT_STOCK)
      if not org_symbol:
        continue
      LogUtils.debug('Updating {0}.'.format(company_name))
      org_symbol.name = company_name
      BaseService._update()
    return "1"

  def import_from_csv_incomestatements(self) -> str:
    BaseService._truncate(FN)

    file: str = FileUtils.get_file(AppConsts.INCOME_STMT_FILE)
    records: List[Dict] = CsvUtils.parse_as_dict(file)
    models: List[Any] = []
    for record in records:
      if not self.__is_valid_intrinio_record(record):
        continue
      symbol: str = record.get(AppConsts.INTRINIO_KEY_INC_STMT_TICKER)
      fiscal_period: str = record.get(AppConsts.INTRINIO_KEY_INC_STMT_FISC_PD)
      org_symbol: SM = self.__stock_service.get_symbol(symbol, AppConsts.INSTRUMENT_STOCK)
      if not org_symbol:
        continue
      quarter_end_dte: date = DateUtils.get_date(
          record.get(AppConsts.INTRINIO_KEY_INC_STMT_END_DTE),
          AppConsts.INTRINIO_END_DTE_FMT)
      file_date: date = DateUtils.get_date(
          record.get(AppConsts.INTRINIO_KEY_INC_STMT_FILE_DTE),
          AppConsts.INTRINIO_FILE_DTE_FMT)
      models.append((
          org_symbol.id,
          record.get(AppConsts.INTRINIO_KEY_INC_STMT_FISC_YR),
          self.__get_quarter(fiscal_period),
          quarter_end_dte,
          file_date,
          None,
          NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_INC_STMT_TTLREV)),
          NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_INC_STMT_TTLPROF)),
          NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_INC_STMT_TTLOPINC)),
          NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_INC_STMT_NETINC)),
          None, None, None, None, None, None, None, None, None, None,
          None, None, None, None, None, None, None, None, None
      ))
    BaseService._insert_bulk(FN, models)
    return "1"

  def import_from_csv_balancesheets(self) -> str:
    file: str = FileUtils.get_file(AppConsts.BALANCE_SHEET_FILE)
    records: List[Dict] = CsvUtils.parse_as_dict(file)
    for record in records:
      if not self.__is_valid_intrinio_record(record):
        continue
      symbol: str = record.get(AppConsts.INTRINIO_KEY_BLNC_SHEET_TICKER)
      fiscal_period: str = record.get(AppConsts.INTRINIO_KEY_BLNC_SHEET_FISC_PD)
      year: int = NumberUtils.to_int(record.get(AppConsts.INTRINIO_KEY_BLNC_SHEET_FISC_YR))
      quarter: int = self.__get_quarter(fiscal_period)
      org_symbol: SM = self.__stock_service.get_symbol(symbol, AppConsts.INSTRUMENT_STOCK)
      if not org_symbol:
        continue
      org_fn: FN = self.__stock_service.get_financial(org_symbol.id, year, quarter)
      if not org_fn:
        continue
      org_fn.current_assets = NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_BLNC_SHEET_CURR_ASSETS))
      org_fn.ttl_assets = NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_BLNC_SHEET_ASSETS))
      org_fn.current_liabilities = NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_BLNC_SHEET_CURR_LIABS))
      org_fn.ttl_liabilities = NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_BLNC_SHEET_LIABS))
      org_fn.ttl_equity = NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_BLNC_SHEET_EQUITY))
      BaseService._update()
    return "1"

  def import_from_csv_calculations(self) -> str:
    file: str = FileUtils.get_file(AppConsts.FINANCIAL_CALCS_FILE)
    records: List[Dict] = CsvUtils.parse_as_dict(file)
    for record in records:
      if not self.__is_valid_intrinio_record(record):
        continue
      symbol: str = record.get(AppConsts.INTRINIO_KEY_CALCS_TICKER)
      fiscal_period: str = record.get(AppConsts.INTRINIO_KEY_CALCS_FISC_PD)
      year: int = NumberUtils.to_int(record.get(AppConsts.INTRINIO_KEY_CALCS_FISC_YR))
      quarter: int = self.__get_quarter(fiscal_period)
      org_symbol: SM = self.__stock_service.get_symbol(symbol, AppConsts.INSTRUMENT_STOCK)
      if not org_symbol:
        continue
      org_fn: FN = self.__stock_service.get_financial(org_symbol.id, year, quarter)
      if not org_fn:
        continue
      org_fn.market_cap = NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_CALCS_MARK_CAP))
      org_fn.revenue_growth = NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_CALCS_REV_GRTH))
      org_fn.revenue_qq_growth = NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_CALCS_REV_QQ_GRTH))
      org_fn.nopat_growth = NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_CALCS_NOPAT_GRTH))
      org_fn.nopat_qq_growth = NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_CALCS_NOTPAT_QQ_GRTH))
      org_fn.net_income_growth = NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_CALCS_INCM_GRTH))
      org_fn.net_income_qq_growth = NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_CALCS_INCM_QQ_GRTH))
      org_fn.free_cash_flow = NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_CALCS_CSH_FLOW))
      org_fn.current_ratio = NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_CALCS_CURR_RATIO))
      org_fn.debt_to_equity_ratio = NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_CALCS_DE_RATIO))
      org_fn.pe_ratio = NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_CALCS_PE_RATIO))
      org_fn.pb_ratio = NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_CALCS_PB_RATIO))
      org_fn.div_payout_ratio = NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_CALCS_DIV_PAYOUT_RATIO))
      org_fn.roe = NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_CALCS_ROE))
      org_fn.roa = NumberUtils.to_float(record.get(AppConsts.INTRINIO_KEY_CALCS_ROA))
      BaseService._update()
    return "1"

  def import_from_csv_filedates(self) -> str:
    file: str = FileUtils.get_file(AppConsts.INCOME_STMT_FILE)
    records: List[Dict] = CsvUtils.parse_as_dict(file)
    for record in records:
      if not self.__is_valid_intrinio_record_for_filedates(record):
        continue
      symbol: str = record.get(AppConsts.INTRINIO_KEY_INC_STMT_TICKER)
      fiscal_period: str = record.get(AppConsts.INTRINIO_KEY_INC_STMT_FISC_PD)
      year: int = NumberUtils.to_int(record.get(AppConsts.INTRINIO_KEY_INC_STMT_FISC_YR))
      quarter: int = self.__get_quarter(fiscal_period)
      file_date: date = DateUtils.get_date(
          record.get(AppConsts.INTRINIO_KEY_INC_STMT_FILE_DTE),
          AppConsts.INTRINIO_FILE_DTE_FMT)
      if not file_date or quarter == 4:
        continue
      org_symbol: SM = self.__stock_service.get_symbol(symbol, AppConsts.INSTRUMENT_STOCK)
      if not org_symbol:
        continue
      org_fn: FN = self.__stock_service.get_financial(org_symbol.id, year, quarter)
      if not org_fn:
        continue
      org_fn.file_date = file_date
      BaseService._update()
    return "1"

  def __get_quarter(self, fiscal_period: str) -> int:
    if StringUtils.isNullOrWhitespace(fiscal_period):
      return None
    if fiscal_period.endswith(AppConsts.INTRINIO_PERIOD_SUFFIX_FY):
      return 4
    return NumberUtils.to_int(fiscal_period
                              .replace(AppConsts.INTRINIO_PERIOD_PREFIX, '')
                              .replace(AppConsts.INTRINIO_PERIOD_SUFFIX_TTM, ''))

  def __is_valid_intrinio_record(self, record: Dict) -> bool:
    fiscal_period: str = record.get(AppConsts.INTRINIO_KEY_INC_STMT_FISC_PD)
    return record \
        and not StringUtils.isNullOrWhitespace(record.get(AppConsts.INTRINIO_KEY_INC_STMT_TICKER)) \
        and not StringUtils.isNullOrWhitespace(record.get(AppConsts.INTRINIO_KEY_INC_STMT_NAME)) \
        and not StringUtils.isNullOrWhitespace(fiscal_period) \
        and (fiscal_period.endswith(AppConsts.INTRINIO_PERIOD_SUFFIX_TTM) or fiscal_period.endswith(AppConsts.INTRINIO_PERIOD_SUFFIX_FY))

  def __is_valid_intrinio_record_for_filedates(self, record: Dict) -> bool:
    fiscal_period: str = record.get(AppConsts.INTRINIO_KEY_INC_STMT_FISC_PD)
    return record \
        and not StringUtils.isNullOrWhitespace(record.get(AppConsts.INTRINIO_KEY_INC_STMT_TICKER)) \
        and not StringUtils.isNullOrWhitespace(record.get(AppConsts.INTRINIO_KEY_INC_STMT_NAME)) \
        and not StringUtils.isNullOrWhitespace(fiscal_period) \
        and not fiscal_period.endswith(AppConsts.INTRINIO_PERIOD_SUFFIX_TTM) \
        and not fiscal_period.endswith(AppConsts.INTRINIO_PERIOD_SUFFIX_FY) \
        and not fiscal_period.endswith(AppConsts.INTRINIO_PERIOD_SUFFIX_YTD)

# endregion

# region YAHOO

  def import_from_csv_yahoo(self) -> str:
    BaseService._truncate(EPD)

    files: List[str] = FileUtils.get_files(AppConsts.ETF_PRICE_FOLDER, is_full=True)
    for file in files:
      symbol: str = FileUtils.get_wo_ext(FileUtils.get_base_name(file))
      org_symbol: SM = self.__stock_service.get_symbol(symbol, AppConsts.INSTRUMENT_ETF)
      if not org_symbol:
        continue
      records: List[Dict] = CsvUtils.parse_as_dict(file)
      models: List[Any] = []
      for record in records:
        models.append((
            org_symbol.id,
            DateUtils.get_date(record.get(AppConsts.YAHOO_KEY_DATE), AppConsts.YAHOO_DATE_FORMAT),
            NumberUtils.to_float(record.get(AppConsts.YAHOO_KEY_OPEN)),
            NumberUtils.to_float(record.get(AppConsts.YAHOO_KEY_HIGH)),
            NumberUtils.to_float(record.get(AppConsts.YAHOO_KEY_LOW)),
            NumberUtils.to_float(record.get(AppConsts.YAHOO_KEY_CLOSE)),
            NumberUtils.to_int(record.get(AppConsts.YAHOO_KEY_VOLUME)),
        ))
      BaseService._insert_bulk(EPD, models)
    return "1"

# endregion

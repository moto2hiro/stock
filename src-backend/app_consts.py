from typing import List
from datetime import datetime


class AppConsts:

  FLASK_ENV_STG: str = 'stg'
  FLASK_ENV_PROD: str = 'prod'

  ROUTE_BASE: str = '/api'
  ROUTE_BACK_TEST: str = '{0}/back_test'.format(ROUTE_BASE)
  ROUTE_STOCK: str = '{0}/stock'.format(ROUTE_BASE)
  ROUTE_IMPORT: str = '{0}/import'.format(ROUTE_BASE)
  ROUTE_TRADE: str = '{0}/trade'.format(ROUTE_BASE)

  STATIC_FOLDER: str = 'static'
  STOCK_PRICE_FOLDER: str = '{0}/stock_price_daily'.format(STATIC_FOLDER)
  STOCK_FINANCIAL_FOLDER: str = '{0}/stock_financial'.format(STATIC_FOLDER)
  ETF_PRICE_FOLDER: str = '{0}/etf_price_daily'.format(STATIC_FOLDER)
  INCOME_STMT_FILE: str = '{0}/US_INDU_INCOME_STATEMENT.csv'.format(STOCK_FINANCIAL_FOLDER)
  BALANCE_SHEET_FILE: str = '{0}/US_INDU_BALANCE_SHEET_STATEMENT.csv'.format(STOCK_FINANCIAL_FOLDER)
  FINANCIAL_CALCS_FILE: str = '{0}/US_INDU_CALCULATIONS.csv'.format(STOCK_FINANCIAL_FOLDER)

  COL_ID: str = 'id'
  PRICE_COL_SYMBOL_ID: str = 'symbol_id'
  PRICE_COL_DATE: str = 'price_date'
  PRICE_COL_OPEN: str = 'open_price'
  PRICE_COL_HIGH: str = 'high_price'
  PRICE_COL_LOW: str = 'low_price'
  PRICE_COL_CLOSE: str = 'close_price'
  PRICE_COL_VOLUME: str = 'volume'
  PRICE_COLS: List[str] = [
      COL_ID,
      PRICE_COL_SYMBOL_ID,
      PRICE_COL_DATE,
      PRICE_COL_OPEN,
      PRICE_COL_HIGH,
      PRICE_COL_LOW,
      PRICE_COL_CLOSE,
      PRICE_COL_VOLUME]
  CUSTOM_COL_PREV_DATE: str = 'prev_date'
  CUSTOM_COL_NEXT_DATE: str = 'next_date'
  CUSTOM_COL_NEXT_NEXT_DATE: str = 'next_next_date'
  CUSTOM_COL_ADV: str = 'adv'
  CUSTOM_COL_PV: str = 'pv'
  CUSTOM_COL_ADPV: str = 'adpv'
  CUSTOM_COL_SMA: str = 'sma'
  CUSTOM_COL_SMA_TREND: str = 'sma_trend'
  CUSTOM_COL_SMA_FAST: str = 'sma_fast'
  CUSTOM_COL_SMA_SLOW: str = 'sma_slow'
  CUSTOM_COL_SMA_PERIOD_1: str = 'sma_period_1'
  CUSTOM_COL_SMA_PERIOD_2: str = 'sma_period_2'
  CUSTOM_COL_STD: str = 'std'
  CUSTOM_COL_RSI: str = 'rsi'
  CUSTOM_COL_RS: str = 'rs'
  CUSTOM_COL_DIFF: str = 'diff'
  CUSTOM_COL_POSITIVE_GAIN: str = 'positive_gain'
  CUSTOM_COL_NEGATIVE_GAIN: str = 'negative_gain'
  CUSTOM_COL_EMA_POSITIVE_GAIN: str = 'ema_positive_gain'
  CUSTOM_COL_EMA_NEGATIVE_GAIN: str = 'ema_negative_gain'
  CUSTOM_COL_TARGET_PRICE: str = 'target_price'
  CUSTOM_COL_STOP_LOSS: str = 'stop_loss'
  CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE: str = 'exponential_smoothing_price'
  CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE_PREV: str = 'exponential_smoothing_price_prev'
  CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE_NEXT: str = 'exponential_smoothing_price_next'
  CUSTOM_COL_EXPONENTIAL_SMOOTHING_MAX: str = 'is_exponential_smoothing_max'
  CUSTOM_COL_EXPONENTIAL_SMOOTHING_MIN: str = 'is_exponential_smoothing_min'
  CUSTOM_COL_DOUBLE_BOLLINGER_BANDS: str = 'has_double_bollinger_bands'
  CUSTOM_COL_UPPER_INNER_BOLLINGER_BAND: str = 'upper_inner_bollinger_band'
  CUSTOM_COL_IS_PRICE_ABOVE_UPPER_INNER_BOLLINGER_BAND: str = 'is_price_above_upper_inner_bollinger_band'
  CUSTOM_COL_IS_PRICE_ABOVE_UPPER_INNER_BOLLINGER_BAND_PREV: str = 'is_price_above_upper_inner_bollinger_band_prev'
  CUSTOM_COL_IS_PRICE_ABOVE_UPPER_INNER_BOLLINGER_BAND_PREV_PREV: str = 'is_price_above_upper_inner_bollinger_band_prev_prev'
  CUSTOM_COL_DOUBLE_BOTTOMS: str = 'has_double_bottoms'
  CUSTOM_COL_DOUBLE_BOTTOMS_TARGET_PRICE: str = 'double_bottoms_target_price'
  CUSTOM_COL_DOUBLE_BOTTOMS_STOP_LOSS: str = 'double_bottoms_stop_loss'
  CUSTOM_COL_DOUBLE_TOPS: str = 'has_double_tops'
  CUSTOM_COL_DOUBLE_TOPS_TARGET_PRICE: str = 'double_tops_target_price'
  CUSTOM_COL_DOUBLE_TOPS_STOP_LOSS: str = 'double_tops_stop_loss'
  CUSTOM_COL_INVERTED_HEAD_AND_SHOULDERS: str = 'has_inverted_head_and_shoulders'
  CUSTOM_COL_INVERTED_HEAD_AND_SHOULDERS_TARGET_PRICE: str = 'inverted_head_and_shoulders_target_price'
  CUSTOM_COL_INVERTED_HEAD_AND_SHOULDERS_STOP_LOSS: str = 'inverted_head_and_shoulders_stop_loss'
  CUSTOM_COL_ABZ_PERIOD: str = 'abz_period'
  CUSTOM_COL_ABZ_MIDDLE: str = 'abz_middle'
  CUSTOM_COL_ABZ_STD: str = 'abz_std'
  CUSTOM_COL_ABZ_UPPER: str = 'abz_upper'
  CUSTOM_COL_ABZ_LOWER: str = 'abz_lower'

  ORDER_STATUS_INIT: int = 0
  ORDER_STATUS_SUBMITTED_ENTRY: int = 1
  ORDER_STATUS_CANCELLED_ENTRY: int = 2
  ORDER_STATUS_IN_POSITION: int = 4
  ORDER_STATUS_SUBMITTED_EXIT: int = 8
  ORDER_STATUS_CANCELLED_EXIT: int = 16
  ORDER_STATUS_COMPLETED: int = 32

  ALPACA_ORDER_STATUS_FILLED: str = 'filled'
  ALPACA_ORDER_STATUS_CANCELLED: str = 'canceled'

  SYMBOL_STATUS_INIT: int = 0
  SYMBOL_STATUS_ARCHIVED: int = 1
  SYMBOL_STATUS_EXCLUDE_TRADE: int = 2

  INSTRUMENT_STOCK: str = 'stock'
  INSTRUMENT_ETF: str = 'etf'
  ACTION_BUY: str = 'buy'
  ACTION_SELL: str = 'sell'

  ORDER_TYPE_MARKET: str = 'market'
  ORDER_TYPE_LIMIT: str = 'limit'
  ORDER_TYPE_STOP: str = 'stop'
  ORDER_TYPE_STOP_LIMIT: str = 'stop_limit'
  ORDER_TYPES: List[str] = [
      ORDER_TYPE_MARKET,
      ORDER_TYPE_LIMIT,
      ORDER_TYPE_STOP,
      ORDER_TYPE_STOP_LIMIT
  ]

  # https://alpaca.markets/docs/trading-on-alpaca/orders/#time-in-force
  TIME_IN_FORCE_DAY: str = 'day'  # auto cancel order after day
  TIME_IN_FORCE_GTC: str = 'gtc'  # order good until cancelled
  TIME_IN_FORCE_OPG: str = 'opg'  # executes on market open (orders need to be submitted before open or after close)
  TIME_IN_FORCE_CLS: str = 'cls'  # executes on market close (orders need to be submitted before close or after close)
  TIME_IN_FORCE_IOC: str = 'ioc'  # immediate or cancel
  TIME_IN_FORCE_FOK: str = 'fok'  # fill or kill
  TIME_IN_FORCES: List[str] = [
      TIME_IN_FORCE_DAY,
      TIME_IN_FORCE_GTC,
      TIME_IN_FORCE_OPG,
      TIME_IN_FORCE_CLS,
      TIME_IN_FORCE_IOC,
      TIME_IN_FORCE_FOK]

  BASIS_POINT: float = 0.0001
  ADV_PERIOD_DFLT: int = 50
  ADPV_PERIOD_DFLT: int = 50
  ADV_MIN_DFLT: int = 1000000
  ADPV_MIN_DFLT: int = 20000000
  CURRENT_RATIO_MIN_DFLT: float = 1
  PE_RATIO_IDEAL_DFLT: float = 30
  PE_RATIO_MAX_DFLT: float = 50

  MIN_DATE: datetime = datetime(1995, 1, 1)
  BENCHMARK_ETF_SPY: str = 'SPY'
  BENCHMARK_ETF_DIA: str = 'DIA'

  # region Strategies
  STRATEGY_DEMO: str = 'demo'
  STRATEGY_ABZ: str = 'abz'
  STRATEGY_DBB: str = 'double_bollinger_bands'
  STRATEGY_DOUBLE_BOTTOMS: str = 'double_bottoms'
  STRATEGY_DOUBLE_TOPS: str = 'double_tops'
  STRATEGY_INVERTED_HEAD_AND_SHOULDERS: str = 'inverted_head_and_shoulders'
  STRATEGY_SMA_CROSSOVER: str = 'sma_crossover'
  STRATEGY_TURNAROUND_TUESDAY: str = 'turnaround_tuesday'
  STRATEGY_TEMA_AND_VWMA: str = 'tema_and_vwma'
  # endregion

  # region Email Templates
  TEMPLATE_PATH_EMAIL: str = 'email'
  TEMPLATE_PATH_DELETE_PRICES: str = '{0}/{1}'.format(TEMPLATE_PATH_EMAIL, 'delete_prices.html')
  TEMPLATE_PATH_IMPORT_PRICES: str = '{0}/{1}'.format(TEMPLATE_PATH_EMAIL, 'import_prices.html')
  TEMPLATE_PATH_GET_SUGGESTIONS: str = '{0}/{1}'.format(TEMPLATE_PATH_EMAIL, 'get_suggestions.html')
  TEMPLATE_PATH_QUEUE_POSITIONS: str = '{0}/{1}'.format(TEMPLATE_PATH_EMAIL, 'queue_positions.html')
  TEMPLATE_PATH_SYNC_ORDERS: str = '{0}/{1}'.format(TEMPLATE_PATH_EMAIL, 'sync_orders.html')
  TEMPLATE_PATH_CLOSE_POSITIONS: str = '{0}/{1}'.format(TEMPLATE_PATH_EMAIL, 'close_positions.html')

  EMAIL_SUBJECT_DELETE_PRICES: str = '[JOB COMPLETE - DELETE PRICES]'
  EMAIL_SUBJECT_IMPORT_PRICES: str = '[JOB COMPLETE - IMPORT PRICES]'
  EMAIL_SUBJECT_GET_SUGGESTIONS: str = '[JOB COMPLETE - GET SUGGESTIONS]'
  EMAIL_SUBJECT_QUEUE_POSITIONS: str = '[JOB COMPLETE - QUEUE POSITIONS]'
  EMAIL_SUBJECT_SYNC_ORDERS: str = '[JOB COMPLETE - SYNC ORDERS]'
  EMAIL_SUBJECT_CLOSE_POSITIONS: str = '[JOB COMPLETE - CLOSE POSITIONS]'
  # endregion

  TZ_NY: str = 'America/New_York'
  WEEKDAY_IDX_MON: int = 0
  WEEKDAY_IDX_TUES: int = 1
  WEEKDAY_IDX_WED: int = 2
  WEEKDAY_IDX_THURS: int = 3
  WEEKDAY_IDX_FRI: int = 4
  WEEKDAY_IDX_SAT: int = 5
  WEEKDAY_IDX_SUN: int = 6

  SPECIAL_NON_TRADING_DAYS: List[str] = [
      '2007-01-02T00:00:00'  # 38th President passed away.
  ]

  # region IEX CLOUD
  IEX_CLOUD_API_KEY: str = 'pk_5cfba93bd3db44ae916c73cdf9405c11'
  IEX_CLOUD_API_SECRET: str = 'sk_e460419fc9874bdcb9bbb0dd8b34ca19'
  IEX_CLOUD_API_BASE_URL: str = 'https://cloud.iexapis.com/v1'
  # endregion

  # region TD AMERITRADE
  TD_AMERITRADE_API_KEY: str = 'QLKKOSWCWHMNWUWAOL9Z1D1MIIXYGSLF'
  TD_AMERITRADE_API_BASE_URL: str = 'https://api.tdameritrade.com/v1'
  # endregion

  # region KIBOT
  KIBOT_IDX_DATE: int = 0
  KIBOT_IDX_OPEN: int = 1
  KIBOT_IDX_HIGH: int = 2
  KIBOT_IDX_LOW: int = 3
  KIBOT_IDX_CLOSE: int = 4
  KIBOT_IDX_VOLUME: int = 5
  KIBOT_DATE_FORMAT: str = '%m/%d/%Y'
  # endregion

  # region INTRINIO
  INTRINIO_KEY_INC_STMT_TICKER: str = 'ticker'
  INTRINIO_KEY_INC_STMT_NAME: str = 'name'
  INTRINIO_KEY_INC_STMT_FISC_YR: str = 'fiscal_year'
  INTRINIO_KEY_INC_STMT_FISC_PD: str = 'fiscal_period'
  INTRINIO_KEY_INC_STMT_END_DTE: str = 'end_date'
  INTRINIO_KEY_INC_STMT_FILE_DTE: str = 'filing_date'
  INTRINIO_KEY_INC_STMT_TTLREV: str = 'totalrevenue'
  INTRINIO_KEY_INC_STMT_TTLPROF: str = 'totalgrossprofit'
  INTRINIO_KEY_INC_STMT_TTLOPINC: str = 'totaloperatingincome'
  INTRINIO_KEY_INC_STMT_NETINC: str = 'netincome'
  INTRINIO_KEY_BLNC_SHEET_TICKER: str = 'ticker'
  INTRINIO_KEY_BLNC_SHEET_NAME: str = 'name'
  INTRINIO_KEY_BLNC_SHEET_FISC_YR: str = 'fiscal_year'
  INTRINIO_KEY_BLNC_SHEET_FISC_PD: str = 'fiscal_period'
  INTRINIO_KEY_BLNC_SHEET_END_DTE: str = 'end_date'
  INTRINIO_KEY_BLNC_SHEET_FILE_DTE: str = 'filing_date'
  INTRINIO_KEY_BLNC_SHEET_CURR_ASSETS: str = 'totalcurrentassets'
  INTRINIO_KEY_BLNC_SHEET_ASSETS: str = 'totalassets'
  INTRINIO_KEY_BLNC_SHEET_CURR_LIABS: str = 'totalcurrentliabilities'
  INTRINIO_KEY_BLNC_SHEET_LIABS: str = 'totalliabilities'
  INTRINIO_KEY_BLNC_SHEET_EQUITY: str = 'totalequity'
  INTRINIO_KEY_CALCS_TICKER: str = 'ticker'
  INTRINIO_KEY_CALCS_NAME: str = 'name'
  INTRINIO_KEY_CALCS_FISC_YR: str = 'fiscal_year'
  INTRINIO_KEY_CALCS_FISC_PD: str = 'fiscal_period'
  INTRINIO_KEY_CALCS_MARK_CAP: str = 'marketcap'
  INTRINIO_KEY_CALCS_REV_GRTH: str = 'revenuegrowth'
  INTRINIO_KEY_CALCS_REV_QQ_GRTH: str = 'revenueqoqgrowth'
  INTRINIO_KEY_CALCS_NOPAT_GRTH: str = 'nopatgrowth'
  INTRINIO_KEY_CALCS_NOTPAT_QQ_GRTH: str = 'nopatqoqgrowth'
  INTRINIO_KEY_CALCS_INCM_GRTH: str = 'netincomegrowth'
  INTRINIO_KEY_CALCS_INCM_QQ_GRTH: str = 'netincomeqoqgrowth'
  INTRINIO_KEY_CALCS_CSH_FLOW: str = 'freecashflow'
  INTRINIO_KEY_CALCS_CURR_RATIO: str = 'currentratio'
  INTRINIO_KEY_CALCS_DE_RATIO: str = 'debttoequity'
  INTRINIO_KEY_CALCS_PE_RATIO: str = 'pricetoearnings'
  INTRINIO_KEY_CALCS_PB_RATIO: str = 'pricetobook'
  INTRINIO_KEY_CALCS_DIV_PAYOUT_RATIO: str = 'divpayoutratio'
  INTRINIO_KEY_CALCS_ROE: str = 'roe'
  INTRINIO_KEY_CALCS_ROA: str = 'roa'
  INTRINIO_END_DTE_FMT = '%Y-%m-%d'
  INTRINIO_FILE_DTE_FMT = '%Y-%m-%d %H:%M:%S %z'
  INTRINIO_PERIOD_SUFFIX_YTD: str = "YTD"
  INTRINIO_PERIOD_SUFFIX_TTM: str = "TTM"
  INTRINIO_PERIOD_SUFFIX_FY: str = "FY"
  INTRINIO_PERIOD_PREFIX: str = "Q"
  # endregion

  # region YAHOO
  YAHOO_KEY_DATE: str = 'Date'
  YAHOO_KEY_OPEN: str = 'Open'
  YAHOO_KEY_HIGH: str = 'High'
  YAHOO_KEY_LOW: str = 'Low'
  YAHOO_KEY_CLOSE: str = 'Close'
  YAHOO_KEY_VOLUME: str = 'Volume'
  YAHOO_DATE_FORMAT: str = '%Y-%m-%d'
  # endregion

  # region Wikipedia
  WIKI_SP500_URL: str = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
  WIKI_SP500_ELEMENT_ID: str = 'constituents'
  WIKI_SP500_COL_SYMBOL: str = 'Symbol'
  WIKI_SP500_COL_SYMBOL_NAME: str = 'Security'
  # endregion

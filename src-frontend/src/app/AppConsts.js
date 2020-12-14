// #region Frontend Consts

export const HTTP_STATUS_CODE_OK = 200;

// #region Colors
export const COLOR_BLACK = '#000000';
export const COLOR_RED = '#ff0000';
export const COLOR_GREEN = '#00ff00';
export const COLOR_YELLOW = '#ffff00';
export const COLOR_ORANGE = '#ffa500';
export const COLOR_PURPLE = '#6a0dad';
export const COLOR_BROWN = '#964b00';
export const COLOR_TURQUOISE = '#40e0d0';
// #endregion

// #region Google Chart
export const GOOGLE_CHART_TYPE_COMBO = 'ComboChart';
export const GOOGLE_CHART_TYPE_LINE = 'LineChart';
export const GOOGLE_CHART_SERIES_CANDLE = 'candlesticks';
export const GOOGLE_CHART_SERIES_LINE = 'line';
export const GOOGLE_CHART_SERIES_SCATTER = 'scatter';
// #endregion

export const STRATEGY_CONFIG = {
  demo: {
    label: 'Demo',
    description: 'Explanation of demo strategy',
    fields: [
      {
        name: 'param_1',
        label: 'Param 1',
        type: 'number',
        step: 0.01,
        default: 1,
        description: 'Explanation of param_1',
        validation: {
          required: true,
          min: 0.01,
          max: 100,
        },
      },
      {
        name: 'param_2',
        label: 'Param 2',
        type: 'text',
        default: 'foo',
        description: 'Explanation of param_2',
        validation: {
          required: true,
        },
      },
    ],
  },
  abz: {
    label: 'Adaptive Bands Z Test-Statistics',
    description: "Bollinger Bands that adapt using Kaufman's Efficiency Ratio.",
    fields: [
      {
        name: 'abz_er_period',
        label: 'Efficiency Ratio Period',
        type: 'number',
        step: 1,
        default: 10,
        description: '',
        validation: {
          required: true,
          min: 1,
          max: 100,
        },
      },
      {
        name: 'abz_std_distance',
        label: 'Standard Deviation Distance',
        type: 'number',
        step: 0.01,
        default: 0.8,
        description: 'Upper/Lower Distance away from the middle band measured in standard deviations.',
        validation: {
          required: true,
          min: 0.01,
          max: 5,
        },
      },
      {
        name: 'abz_constant_k',
        label: 'Constant K',
        type: 'number',
        step: 0.01,
        default: 60,
        description: 'Some contant K.',
        validation: {
          required: true,
          min: 0.01,
          max: 200,
        },
      },
    ],
  },
  double_bollinger_bands: {
    label: 'Double Bollinger Bands',
    description: '',
    fields: [
      {
        name: 'sma_period',
        label: 'SMA Period',
        type: 'number',
        step: 1,
        default: 13,
        description: 'Period used to calculate the SMA',
        validation: {
          required: true,
          min: 1,
          max: 50,
        },
      },
      {
        name: 'std_distance',
        label: 'Standard Deviations',
        type: 'number',
        step: 0.01,
        default: 1,
        description: 'Standard deviation used to calculate the value for the upper inner band',
        validation: {
          required: true,
          min: 0.01,
          max: 5,
        },
      },
    ],
  },
  double_bottoms: {
    label: 'Double Bottoms',
    description: 'Chart pattern where there are two local mins.',
    fields: [
      {
        name: 'exponential_smoothing_alpha',
        label: 'Exponential Smoothing Alpha',
        type: 'number',
        step: 0.01,
        default: 0.8,
        description: 'A value between 0 and 1 to control smoothing. 0 with the least noise and vice versa.',
        validation: {
          required: true,
          min: 0.01,
          max: 1,
        },
      },
      {
        name: 'exponential_smoothing_max_min_diff',
        label: 'Exponential Smoothing Max/Min Diff Threshold',
        type: 'number',
        step: 0.01,
        default: 0.7,
        description: 'Threshold to control number of local max/mins.',
        validation: {
          required: true,
          min: 0.01,
          max: 5,
        },
      },
      {
        name: 'double_bottoms_diff',
        label: 'Double Bottoms Diff Threshold',
        type: 'number',
        step: 0.01,
        default: 1,
        description: 'Threshold to control max diff between the two local mins.',
        validation: {
          required: true,
          min: 0.01,
          max: 5,
        },
      },
    ],
  },
  double_tops: {
    label: 'Double Tops',
    description: 'Chart pattern where there are two local maxes.',
    fields: [
      {
        name: 'exponential_smoothing_alpha',
        label: 'Exponential Smoothing Alpha',
        type: 'number',
        step: 0.01,
        default: 0.8,
        description: 'A value between 0 and 1 to control smoothing. 0 with the least noise and vice versa.',
        validation: {
          required: true,
          min: 0.01,
          max: 1,
        },
      },
      {
        name: 'exponential_smoothing_max_min_diff',
        label: 'Exponential Smoothing Max/Min Diff Threshold',
        type: 'number',
        step: 0.01,
        default: 0.7,
        description: 'Threshold to control number of local max/mins.',
        validation: {
          required: true,
          min: 0.01,
          max: 5,
        },
      },
      {
        name: 'double_tops_diff',
        label: 'Double Tops Diff Threshold',
        type: 'number',
        step: 0.01,
        default: 1,
        description: 'Threshold to control max diff between the two local maxes.',
        validation: {
          required: true,
          min: 0.01,
          max: 5,
        },
      },
    ],
  },
  inverted_head_and_shoulders: {
    label: 'Inverted Head and Shoulders',
    description: 'Chart pattern where there are three local mins shaped like an inverted head and shoulders.',
    fields: [
      {
        name: 'exponential_smoothing_alpha',
        label: 'Exponential Smoothing Alpha',
        type: 'number',
        step: 0.01,
        default: 0.8,
        description: 'A value between 0 and 1 to control smoothing. 0 with the least noise and vice versa.',
        validation: {
          required: true,
          min: 0.01,
          max: 1,
        },
      },
      {
        name: 'exponential_smoothing_max_min_diff',
        label: 'Exponential Smoothing Max/Min Diff Threshold',
        type: 'number',
        step: 0.01,
        default: 0.7,
        description: 'Threshold to control number of local max/mins.',
        validation: {
          required: true,
          min: 0.01,
          max: 5,
        },
      },
      {
        name: 'shoulder_diff',
        label: 'Shoulder Diff Threshold',
        type: 'number',
        step: 0.01,
        default: 1,
        description: 'Threshold to control max diff between the two shoulders.',
        validation: {
          required: true,
          min: 0.01,
          max: 5,
        },
      },
      {
        name: 'neck_diff',
        label: 'Neck Diff Threshold',
        type: 'number',
        step: 0.01,
        default: 1,
        description: 'Threshold to control max diff between the left side and right side of the neck.',
        validation: {
          required: true,
          min: 0.01,
          max: 5,
        },
      },
    ],
  },
  sma_crossover: {
    label: 'SMA Crossover',
    description: 'Trade when the fast SMA crosses above the slow SMA.',
    fields: [
      {
        name: 'sma_period_fast',
        label: 'SMA Period Fast',
        type: 'number',
        step: 1,
        default: 20,
        description: '',
        validation: {
          required: true,
          min: 1,
          max: 200,
          lessThan: 'sma_period_slow',
        },
      },
      {
        name: 'sma_period_slow',
        label: 'SMA Period Slow',
        type: 'number',
        step: 1,
        default: 100,
        description: '',
        validation: {
          required: true,
          min: 1,
          max: 200,
          greaterThan: 'sma_period_fast',
        },
      },
    ],
  },
  turnaround_tuesday: {
    label: 'Turnaround Tuesday',
    description: 'Market goes up on Tuesday if Monday was down.',
    fields: [],
  },
  tema_and_vwma: {
    label: 'TEMA and VWMA',
    description: '',
    fields: [
      {
        name: 'tema_period',
        label: 'TEMA Period',
        type: 'number',
        default: 50,
        description: 'Period to calculate the TEMA',
      },
      {
        name: 'vwma_period',
        label: 'VWMA Period',
        type: 'number',
        default: 25,
        description: 'Period to calculate the TEMA',
      },
    ],
  },
};

// #endregion

// #region Backend Consts

// #region API Routes
export const ROUTE_BASE = 'http://127.0.0.1:5000/api';
export const ROUTE_BACK_TEST = `${ROUTE_BASE}/back_test`;
export const ROUTE_STOCK = `${ROUTE_BASE}/stock`;
export const ROUTE_IMPORT = `${ROUTE_BASE}/import`;
export const ROUTE_TRADE = `${ROUTE_BASE}/trade`;
// #endregion

export const PRICE_COL_SYMBOL_ID = 'symbol_id';
export const PRICE_COL_DATE = 'price_date';
export const PRICE_COL_OPEN = 'open_price';
export const PRICE_COL_HIGH = 'high_price';
export const PRICE_COL_LOW = 'low_price';
export const PRICE_COL_CLOSE = 'close_price';
export const PRICE_COL_VOLUME = 'volume';
export const PRICE_COLS = [
  PRICE_COL_SYMBOL_ID,
  PRICE_COL_DATE,
  PRICE_COL_OPEN,
  PRICE_COL_HIGH,
  PRICE_COL_LOW,
  PRICE_COL_CLOSE,
  PRICE_COL_VOLUME,
];
export const CUSTOM_COL_SMA = 'sma';
export const CUSTOM_COL_SMA_PERIOD_1 = 'sma_period_1';
export const CUSTOM_COL_SMA_PERIOD_2 = 'sma_period_2';
export const CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE = 'exponential_smoothing_price';
export const CUSTOM_COL_EXPONENTIAL_SMOOTHING_MAX = 'is_exponential_smoothing_max';
export const CUSTOM_COL_EXPONENTIAL_SMOOTHING_MIN = 'is_exponential_smoothing_min';
export const CUSTOM_COL_ABZ_PERIOD = 'abz_period';
export const CUSTOM_COL_ABZ_MIDDLE = 'abz_middle';
export const CUSTOM_COL_ABZ_STD = 'abz_std';
export const CUSTOM_COL_ABZ_UPPER = 'abz_upper';
export const CUSTOM_COL_ABZ_LOWER = 'abz_lower';

export const ORDER_STATUS_INIT = 0;
export const ORDER_STATUS_SUBMITTED_ENTRY = 1;
export const ORDER_STATUS_CANCELLED_ENTRY = 2;
export const ORDER_STATUS_IN_POSITION = 4;
export const ORDER_STATUS_SUBMITTED_EXIT = 8;
export const ORDER_STATUS_CANCELLED_EXIT = 16;
export const ORDER_STATUS_COMPLETED = 32;

export const SYMBOL_STATUS_INIT = 0;
export const SYMBOL_STATUS_ARCHIVED = 1;
export const SYMBOL_STATUS_EXCLUDE_TRADE = 2;

export const INSTRUMENT_STOCK = 'stock';
export const INSTRUMENT_ETF = 'etf';
export const ACTION_BUY = 'buy';
export const ACTION_SELL = 'sell';

export const ORDER_TYPE_MARKET = 'market';
export const ORDER_TYPE_LIMIT = 'limit';
export const ORDER_TYPE_STOP = 'stop';
export const ORDER_TYPE_STOP_LIMIT = 'stop_limit';
export const ORDER_TYPES = [ORDER_TYPE_MARKET, ORDER_TYPE_LIMIT, ORDER_TYPE_STOP, ORDER_TYPE_STOP_LIMIT];

// https://alpaca.markets/docs/trading-on-alpaca/orders/#time-in-force
export const TIME_IN_FORCE_DAY = 'day'; // auto cancel order after day
export const TIME_IN_FORCE_GTC = 'gtc'; // order good until cancelled
export const TIME_IN_FORCE_OPG = 'opg'; // executes on market open (orders need to be submitted before open or after close)
export const TIME_IN_FORCE_CLS = 'cls'; // executes on market close (orders need to be submitted before close or after close)
export const TIME_IN_FORCE_IOC = 'ioc'; // immediate or cancel
export const TIME_IN_FORCE_FOK = 'fok'; // fill or kill
export const TIME_IN_FORCES = [
  TIME_IN_FORCE_DAY,
  TIME_IN_FORCE_GTC,
  TIME_IN_FORCE_OPG,
  TIME_IN_FORCE_CLS,
  TIME_IN_FORCE_IOC,
  TIME_IN_FORCE_FOK,
];

export const BASIS_POINT = 0.0001;
export const MARKET_CAP_MIN_DFLT = 300000000;
export const ADV_PERIOD_DFLT = 50;
export const ADPV_PERIOD_DFLT = 50;
export const ADV_MIN_DFLT = 1000000;
export const ADPV_MIN_DFLT = 20000000;
export const CURRENT_RATIO_MIN_DFLT = 1;
export const PE_RATIO_IDEAL_DFLT = 30;
export const PE_RATIO_MAX_DFLT = 50;

export const MIN_DATE = '1995-01-01';
export const BENCHMARK_ETF_SPY = 'SPY';
export const BENCHMARK_ETF_DIA = 'DIA';

// #region Strategies
export const STRATEGY_DEMO = 'demo';
export const STRATEGY_ABZ = 'abz';
export const STRATEGY_DBB = 'double_bollinger_bands';
export const STRATEGY_DOUBLE_BOTTOMS = 'double_bottoms';
export const STRATEGY_DOUBLE_TOPS = 'double_tops';
export const STRATEGY_INVERTED_HEAD_AND_SHOULDERS = 'inverted_head_and_shoulders';
export const STRATEGY_TURNAROUND_TUESDAY = 'turnaround_tuesday';
// #endregion

// #endregion

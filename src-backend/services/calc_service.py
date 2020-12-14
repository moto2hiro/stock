import numpy as np
import pandas as pd
from typing import Any
from pandas.core.frame import DataFrame
from app_consts import AppConsts
from app_utils.log_utils import LogUtils
from app_utils.number_utils import NumberUtils
from services.base_service import BaseService


class CalcService(BaseService):
  def __init__(self) -> None:
    super().__init__()

  def append_sma(
          self,
          prices: DataFrame,
          index: Any,
          sma_period: int,
          sma_column_name: str,
          target_column: str = AppConsts.PRICE_COL_CLOSE) -> DataFrame:
    if not isinstance(prices, DataFrame) \
            or sma_period < 1 \
            or not target_column in prices.columns:
      return None
    if not sma_column_name in prices.columns:
      prices[sma_column_name] = 0
    sma: Series = prices.loc[index][target_column].rolling(sma_period).mean()
    prices[sma_column_name].update(sma)
    return prices

  def append_std(
          self,
          prices: DataFrame,
          index: Any,
          std_period: int,
          std_column_name: str,
          target_column: str = AppConsts.PRICE_COL_CLOSE) -> DataFrame:
    if not isinstance(prices, DataFrame) \
            or std_period < 1 \
            or not target_column in prices.columns:
      return None
    if not std_column_name in prices.columns:
      prices[std_column_name] = 0
    std: Series = prices.loc[index][target_column].rolling(std_period).std()
    prices[std_column_name].update(std)
    return prices

  def append_rsi(
          self,
          prices: DataFrame,
          index: Any,
          rsi_period: int = 14,
          target_column: str = AppConsts.PRICE_COL_CLOSE,
          adjust: bool = True) -> DataFrame:
    if not isinstance(prices, DataFrame) \
            or rsi_period < 1 \
            or not target_column in prices.columns:
      return None
    if not AppConsts.CUSTOM_COL_DIFF in prices.columns:
      prices[AppConsts.CUSTOM_COL_DIFF] = 0
    if not AppConsts.CUSTOM_COL_POSITIVE_GAIN in prices.columns:
      prices[AppConsts.CUSTOM_COL_POSITIVE_GAIN] = 0
    if not AppConsts.CUSTOM_COL_NEGATIVE_GAIN in prices.columns:
      prices[AppConsts.CUSTOM_COL_NEGATIVE_GAIN] = 0
    if not AppConsts.CUSTOM_COL_EMA_POSITIVE_GAIN in prices.columns:
      prices[AppConsts.CUSTOM_COL_EMA_POSITIVE_GAIN] = 0
    if not AppConsts.CUSTOM_COL_EMA_NEGATIVE_GAIN in prices.columns:
      prices[AppConsts.CUSTOM_COL_EMA_NEGATIVE_GAIN] = 0
    if not AppConsts.CUSTOM_COL_RS in prices.columns:
      prices[AppConsts.CUSTOM_COL_RS] = 0
    if not AppConsts.CUSTOM_COL_RSI in prices.columns:
      prices[AppConsts.CUSTOM_COL_RSI] = 0

    diff: Series = prices.loc[index][target_column].diff()
    prices[AppConsts.CUSTOM_COL_DIFF].update(diff)

    prices[AppConsts.CUSTOM_COL_POSITIVE_GAIN] = np.where((prices[AppConsts.CUSTOM_COL_DIFF] < 0), 1, 0)
    prices[AppConsts.CUSTOM_COL_NEGATIVE_GAIN] = np.where((prices[AppConsts.CUSTOM_COL_DIFF] > 0), 1, 0)

    ema_gains: Series = prices.loc[index][AppConsts.CUSTOM_COL_POSITIVE_GAIN].ewm(alpha=1.0 / rsi_period, adjust=adjust).mean()
    prices[AppConsts.CUSTOM_COL_EMA_POSITIVE_GAIN].update(ema_gains)

    ema_losses: Series = prices.loc[index][AppConsts.CUSTOM_COL_NEGATIVE_GAIN].abs().ewm(alpha=1.0 / rsi_period, adjust=adjust).mean()
    prices[AppConsts.CUSTOM_COL_EMA_NEGATIVE_GAIN].update(ema_losses)

    rs: Series = prices.loc[index][AppConsts.CUSTOM_COL_EMA_POSITIVE_GAIN] / prices.loc[index][AppConsts.CUSTOM_COL_EMA_NEGATIVE_GAIN]
    prices[AppConsts.CUSTOM_COL_RS].update(rs)

    rsi: Series = 100 - (100 / (1 + prices.loc[index][AppConsts.CUSTOM_COL_RS]))
    prices[AppConsts.CUSTOM_COL_RSI].update(rsi)

    return prices

  def append_exponential_smoothing_price(
          self,
          prices: DataFrame,
          index: Any,
          alpha: float,
          price_column: str = AppConsts.PRICE_COL_CLOSE) -> DataFrame:

    # https://en.wikipedia.org/wiki/Exponential_smoothing
    if not isinstance(prices, DataFrame) \
            or alpha < 0 \
            or alpha > 1 \
            or not price_column in prices.columns:
      return None
    if not AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE in prices.columns:
      prices[AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE] = 0
    if not AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE_PREV in prices.columns:
      prices[AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE_PREV] = 0
    if not AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE_NEXT in prices.columns:
      prices[AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE_NEXT] = 0

    exponential_smoothing_prices: Series = prices.loc[index][price_column].ewm(alpha=alpha).mean()
    prices[AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE].update(exponential_smoothing_prices)
    prices[AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE_PREV].update(exponential_smoothing_prices.shift(1))
    prices[AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE_NEXT].update(exponential_smoothing_prices.shift(-1))
    return prices

  def append_exponential_smoothing_max_min(
          self,
          prices: DataFrame,
          index: Any,
          exponential_smoothing_max_min_diff: float) -> DataFrame:

    if not (isinstance(prices, DataFrame)
            and AppConsts.PRICE_COL_SYMBOL_ID in prices.index.names
            and AppConsts.PRICE_COL_DATE in prices.index.names
            and AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE in prices.columns
            and AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE_PREV in prices.columns
            and AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE_NEXT in prices.columns):
      return None
    if not AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_MAX in prices.columns:
      prices[AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_MAX] = 0
    if not AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_MIN in prices.columns:
      prices[AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_MIN] = 0

    curr_exp_smoothed_maxmin: float = 0.1
    for i, row in prices.loc[index].iterrows():
      symbol_id: int = i[0]
      curr_date: date = i[1]
      curr_exp_smoothed_p: float = row[AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE]
      prev_exp_smoothed_p: float = row[AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE_PREV]
      next_exp_smoothed_p: float = row[AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE_NEXT]
      maxmin_diff: float = NumberUtils.get_change(
          curr_exp_smoothed_p,
          curr_exp_smoothed_maxmin)
      is_max: bool = (not np.isnan(prev_exp_smoothed_p)
                      and not prev_exp_smoothed_p == 0
                      and not np.isnan(next_exp_smoothed_p)
                      and not next_exp_smoothed_p == 0
                      and maxmin_diff is not None
                      and curr_exp_smoothed_p > prev_exp_smoothed_p
                      and curr_exp_smoothed_p >= next_exp_smoothed_p
                      and abs(maxmin_diff) > exponential_smoothing_max_min_diff)
      is_min: bool = (not np.isnan(prev_exp_smoothed_p)
                      and not prev_exp_smoothed_p == 0
                      and not np.isnan(next_exp_smoothed_p)
                      and not next_exp_smoothed_p == 0
                      and maxmin_diff is not None
                      and curr_exp_smoothed_p < prev_exp_smoothed_p
                      and curr_exp_smoothed_p <= next_exp_smoothed_p
                      and abs(maxmin_diff) > exponential_smoothing_max_min_diff)
      prices[AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_MAX].loc[symbol_id, curr_date] = 1 if is_max else 0
      prices[AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_MIN].loc[symbol_id, curr_date] = 1 if is_min else 0
      if is_max or is_min:
        curr_exp_smoothed_maxmin = curr_exp_smoothed_p
    return prices

  def append_double_bollinger_bands(
          self,
          prices: DataFrame,
          index: Any,
          std_distance: float,
          target_column: str = AppConsts.PRICE_COL_CLOSE) -> DataFrame:
    if not (isinstance(prices, DataFrame)
            and AppConsts.PRICE_COL_SYMBOL_ID in prices.index.names
            and AppConsts.PRICE_COL_DATE in prices.index.names
            and AppConsts.CUSTOM_COL_SMA in prices.columns
            and AppConsts.CUSTOM_COL_STD in prices.columns
            and target_column in prices.columns):
      return None
    if not AppConsts.CUSTOM_COL_DOUBLE_BOLLINGER_BANDS in prices.columns:
      prices[AppConsts.CUSTOM_COL_DOUBLE_BOLLINGER_BANDS] = 0
    if not AppConsts.CUSTOM_COL_UPPER_INNER_BOLLINGER_BAND in prices.columns:
      prices[AppConsts.CUSTOM_COL_UPPER_INNER_BOLLINGER_BAND] = 0
    if not AppConsts.CUSTOM_COL_IS_PRICE_ABOVE_UPPER_INNER_BOLLINGER_BAND in prices.columns:
      prices[AppConsts.CUSTOM_COL_IS_PRICE_ABOVE_UPPER_INNER_BOLLINGER_BAND] = 0
    if not AppConsts.CUSTOM_COL_IS_PRICE_ABOVE_UPPER_INNER_BOLLINGER_BAND_PREV in prices.columns:
      prices[AppConsts.CUSTOM_COL_IS_PRICE_ABOVE_UPPER_INNER_BOLLINGER_BAND_PREV] = 0
    if not AppConsts.CUSTOM_COL_IS_PRICE_ABOVE_UPPER_INNER_BOLLINGER_BAND_PREV_PREV in prices.columns:
      prices[AppConsts.CUSTOM_COL_IS_PRICE_ABOVE_UPPER_INNER_BOLLINGER_BAND_PREV_PREV] = 0

    upper_inner: Series = prices.loc[index][AppConsts.CUSTOM_COL_SMA] + prices.loc[index][AppConsts.CUSTOM_COL_STD] * std_distance
    prices[AppConsts.CUSTOM_COL_UPPER_INNER_BOLLINGER_BAND].update(upper_inner)

    prices[AppConsts.CUSTOM_COL_IS_PRICE_ABOVE_UPPER_INNER_BOLLINGER_BAND] = np.where(
        (prices[target_column] > prices[AppConsts.CUSTOM_COL_UPPER_INNER_BOLLINGER_BAND]),
        1,
        0)

    prev: Series = prices.loc[index][AppConsts.CUSTOM_COL_IS_PRICE_ABOVE_UPPER_INNER_BOLLINGER_BAND].shift(1)
    prices[AppConsts.CUSTOM_COL_IS_PRICE_ABOVE_UPPER_INNER_BOLLINGER_BAND_PREV].update(prev)

    prev_prev: Series = prices.loc[index][AppConsts.CUSTOM_COL_IS_PRICE_ABOVE_UPPER_INNER_BOLLINGER_BAND_PREV].shift(1)
    prices[AppConsts.CUSTOM_COL_IS_PRICE_ABOVE_UPPER_INNER_BOLLINGER_BAND_PREV_PREV].update(prev_prev)

    prices[AppConsts.CUSTOM_COL_DOUBLE_BOLLINGER_BANDS] = np.where(
        (prices[AppConsts.CUSTOM_COL_IS_PRICE_ABOVE_UPPER_INNER_BOLLINGER_BAND] == 1)
        & (prices[AppConsts.CUSTOM_COL_IS_PRICE_ABOVE_UPPER_INNER_BOLLINGER_BAND_PREV] == 0)
        & (prices[AppConsts.CUSTOM_COL_IS_PRICE_ABOVE_UPPER_INNER_BOLLINGER_BAND_PREV_PREV] == 0),
        1,
        0)

    return prices

  def append_double_bottoms(
          self,
          prices: DataFrame,
          index: Any,
          price_column: str,
          smooth_price_column: str,
          max_column: str,
          min_column: str,
          double_bottoms_diff: float) -> DataFrame:

    if not (isinstance(prices, DataFrame)
            and AppConsts.PRICE_COL_SYMBOL_ID in prices.index.names
            and AppConsts.PRICE_COL_DATE in prices.index.names
            and price_column in prices.columns
            and smooth_price_column in prices.columns
            and max_column in prices.columns
            and min_column in prices.columns):
      return None
    if not AppConsts.CUSTOM_COL_DOUBLE_BOTTOMS in prices.columns:
      prices[AppConsts.CUSTOM_COL_DOUBLE_BOTTOMS] = 0
    if not AppConsts.CUSTOM_COL_DOUBLE_BOTTOMS_TARGET_PRICE in prices.columns:
      prices[AppConsts.CUSTOM_COL_DOUBLE_BOTTOMS_TARGET_PRICE] = 0
    if not AppConsts.CUSTOM_COL_DOUBLE_BOTTOMS_STOP_LOSS in prices.columns:
      prices[AppConsts.CUSTOM_COL_DOUBLE_BOTTOMS_STOP_LOSS] = 0

    last_four_maxmins: List[float] = []
    for i, row in prices.loc[index].iterrows():
      symbol_id: int = i[0]
      curr_date: date = i[1]
      is_max: bool = row[max_column] == 1
      is_min: bool = row[min_column] == 1
      if is_max or is_min:
        if len(last_four_maxmins) >= 4:
          last_four_maxmins.pop(0)
        last_four_maxmins.append(row[smooth_price_column])

      if len(last_four_maxmins) < 4:
        continue
      (point_a, point_b, point_c, point_d) = last_four_maxmins
      point_b_d_diff: float = NumberUtils.get_change(point_b, point_d)
      target_price: float = point_c + (point_c - point_d)
      has_double_bottoms: bool = (point_a > point_b
                                  and point_a > point_c
                                  and point_a > point_d
                                  and point_b < point_c
                                  and point_c > point_b
                                  and point_c > point_d
                                  and abs(point_b_d_diff) < double_bottoms_diff
                                  and row[price_column] > point_c)
      # and row[price_column] < target_price) # Actual Double Bottoms condition, but get better results without it.
      if has_double_bottoms:
        prices[AppConsts.CUSTOM_COL_DOUBLE_BOTTOMS].loc[symbol_id, curr_date] = 1
        prices[AppConsts.CUSTOM_COL_DOUBLE_BOTTOMS_TARGET_PRICE].loc[symbol_id, curr_date] = target_price
        prices[AppConsts.CUSTOM_COL_DOUBLE_BOTTOMS_STOP_LOSS].loc[symbol_id, curr_date] = point_d

    return prices

  def append_double_tops(
          self,
          prices: DataFrame,
          index: Any,
          price_column: str,
          smooth_price_column: str,
          max_column: str,
          min_column: str,
          double_tops_diff: float) -> DataFrame:

    if not (isinstance(prices, DataFrame)
            and AppConsts.PRICE_COL_SYMBOL_ID in prices.index.names
            and AppConsts.PRICE_COL_DATE in prices.index.names
            and price_column in prices.columns
            and smooth_price_column in prices.columns
            and max_column in prices.columns
            and min_column in prices.columns):
      return None
    if not AppConsts.CUSTOM_COL_DOUBLE_TOPS in prices.columns:
      prices[AppConsts.CUSTOM_COL_DOUBLE_TOPS] = 0
    if not AppConsts.CUSTOM_COL_DOUBLE_TOPS_TARGET_PRICE in prices.columns:
      prices[AppConsts.CUSTOM_COL_DOUBLE_TOPS_TARGET_PRICE] = 0
    if not AppConsts.CUSTOM_COL_DOUBLE_TOPS_STOP_LOSS in prices.columns:
      prices[AppConsts.CUSTOM_COL_DOUBLE_TOPS_STOP_LOSS] = 0

    last_four_maxmins: List[float] = []
    for i, row in prices.loc[index].iterrows():
      symbol_id: int = i[0]
      curr_date: date = i[1]
      is_max: bool = row[max_column] == 1
      is_min: bool = row[min_column] == 1
      if is_max or is_min:
        if len(last_four_maxmins) >= 4:
          last_four_maxmins.pop(0)
        last_four_maxmins.append(row[smooth_price_column])

      if len(last_four_maxmins) < 4:
        continue
      (point_a, point_b, point_c, point_d) = last_four_maxmins
      point_b_d_diff: float = NumberUtils.get_change(point_b, point_d)
      target_price: float = point_c - (point_d - point_c)
      has_double_tops: bool = (point_a < point_b
                               and point_a < point_c
                               and point_a < point_d
                               and point_b > point_c
                               and point_c < point_d
                               and abs(point_b_d_diff) < double_tops_diff
                               and row[price_column] < point_c)

      # and row[price_column] > target_price) # Actual Double Tops condition, but get better results without it.
      if has_double_tops:
        prices[AppConsts.CUSTOM_COL_DOUBLE_TOPS].loc[symbol_id, curr_date] = 1
        prices[AppConsts.CUSTOM_COL_DOUBLE_TOPS_TARGET_PRICE].loc[symbol_id, curr_date] = target_price
        prices[AppConsts.CUSTOM_COL_DOUBLE_TOPS_STOP_LOSS].loc[symbol_id, curr_date] = point_d

    return prices

  def append_inverted_head_and_shoulders(
          self,
          prices: DataFrame,
          index: Any,
          price_column: str,
          smooth_price_column: str,
          max_column: str,
          min_column: str,
          shoulder_diff: float,
          neck_diff: float) -> DataFrame:

    if not (isinstance(prices, DataFrame)
            and AppConsts.PRICE_COL_SYMBOL_ID in prices.index.names
            and AppConsts.PRICE_COL_DATE in prices.index.names
            and price_column in prices.columns
            and smooth_price_column in prices.columns
            and max_column in prices.columns
            and min_column in prices.columns):
      return None
    if not AppConsts.CUSTOM_COL_INVERTED_HEAD_AND_SHOULDERS in prices.columns:
      prices[AppConsts.CUSTOM_COL_INVERTED_HEAD_AND_SHOULDERS] = 0
    if not AppConsts.CUSTOM_COL_INVERTED_HEAD_AND_SHOULDERS_TARGET_PRICE in prices.columns:
      prices[AppConsts.CUSTOM_COL_INVERTED_HEAD_AND_SHOULDERS_TARGET_PRICE] = 0
    if not AppConsts.CUSTOM_COL_INVERTED_HEAD_AND_SHOULDERS_STOP_LOSS in prices.columns:
      prices[AppConsts.CUSTOM_COL_INVERTED_HEAD_AND_SHOULDERS_STOP_LOSS] = 0

    last_six_maxmins: List[float] = []
    for i, row in prices.loc[index].iterrows():
      symbol_id: int = i[0]
      curr_date: date = i[1]
      is_max: bool = row[max_column] == 1
      is_min: bool = row[min_column] == 1
      if is_max or is_min:
        if len(last_six_maxmins) >= 6:
          last_six_maxmins.pop(0)
        last_six_maxmins.append(row[smooth_price_column])

      if len(last_six_maxmins) < 6:
        continue
      (point_a, point_b, point_c, point_d, point_e, point_f) = last_six_maxmins
      point_b_f_diff: float = NumberUtils.get_change(point_b, point_f)
      point_c_e_diff: float = NumberUtils.get_change(point_c, point_e)
      neck_point: float = point_c if point_c > point_e else point_e
      target_price: float = neck_point + (neck_point - point_d)
      has_inverted_head_and_shoulders: bool = (point_a > point_b
                                               and point_a > point_c
                                               and point_a > point_d
                                               and point_a > point_e
                                               and point_a > point_f
                                               and point_b < point_c
                                               and point_b > point_d
                                               and point_b < point_e
                                               and point_c > point_d
                                               and point_c > point_f
                                               and point_d < point_e
                                               and point_d < point_f
                                               and abs(point_b_f_diff) < shoulder_diff
                                               and abs(point_c_e_diff) < neck_point
                                               and row[price_column] > neck_point
                                               and row[price_column] < target_price)
      if has_inverted_head_and_shoulders:
        prices[AppConsts.CUSTOM_COL_INVERTED_HEAD_AND_SHOULDERS].loc[symbol_id, curr_date] = 1
        prices[AppConsts.CUSTOM_COL_INVERTED_HEAD_AND_SHOULDERS_TARGET_PRICE].loc[symbol_id, curr_date] = target_price
        prices[AppConsts.CUSTOM_COL_INVERTED_HEAD_AND_SHOULDERS_STOP_LOSS].loc[symbol_id, curr_date] = point_f
    return prices

  def append_abz(
          self,
          prices: DataFrame,
          index: Any,
          abz_er_period: int,
          abz_std_distance: float,
          abz_constant_k: float,
          target_column: str = AppConsts.PRICE_COL_CLOSE) -> DataFrame:
    if not isinstance(prices, DataFrame) \
            or not target_column in prices.columns:
      return None
    if not AppConsts.CUSTOM_COL_ABZ_PERIOD in prices.columns:
      prices[AppConsts.CUSTOM_COL_ABZ_PERIOD] = 0
    if not AppConsts.CUSTOM_COL_ABZ_MIDDLE in prices.columns:
      prices[AppConsts.CUSTOM_COL_ABZ_MIDDLE] = 0
    if not AppConsts.CUSTOM_COL_ABZ_STD in prices.columns:
      prices[AppConsts.CUSTOM_COL_ABZ_STD] = 0
    if not AppConsts.CUSTOM_COL_ABZ_UPPER in prices.columns:
      prices[AppConsts.CUSTOM_COL_ABZ_UPPER] = 0
    if not AppConsts.CUSTOM_COL_ABZ_LOWER in prices.columns:
      prices[AppConsts.CUSTOM_COL_ABZ_LOWER] = 0

    direction: Series = prices.loc[index][target_column].diff(abz_er_period).abs()
    volatility: Series = prices.loc[index][target_column].diff().abs().rolling(abz_er_period).sum()
    er: Series = direction / volatility
    periods: Series = er * abz_constant_k
    prices[AppConsts.CUSTOM_COL_ABZ_PERIOD].update(periods)

    cursor: int = 0
    for i, row in prices.loc[index].iterrows():
      symbol_id: int = i[0]
      curr_date: date = i[1]
      period: int = NumberUtils.to_int(row[AppConsts.CUSTOM_COL_ABZ_PERIOD])
      period = period if period > 2 else 2
      sma_series: Series = prices.loc[index][target_column].rolling(period).mean()
      std_series: Series = prices.loc[index][target_column].rolling(period).std()
      sma: float = sma_series[symbol_id, curr_date]
      std: float = std_series[symbol_id, curr_date]
      upper: float = sma + (std * abz_std_distance)
      lower: float = sma - (std * abz_std_distance)
      prices[AppConsts.CUSTOM_COL_ABZ_MIDDLE].loc[symbol_id, curr_date] = sma
      prices[AppConsts.CUSTOM_COL_ABZ_UPPER].loc[symbol_id, curr_date] = upper
      prices[AppConsts.CUSTOM_COL_ABZ_LOWER].loc[symbol_id, curr_date] = lower
      cursor += 1

    return prices

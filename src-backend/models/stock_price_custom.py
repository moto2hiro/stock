from typing import Tuple
from datetime import date
from pandas.core.series import Series
from app_consts import AppConsts
from app_utils.number_utils import NumberUtils
from models.response_models.base_response import BaseResponse


class StockPriceCustom(BaseResponse):

  def __init__(self, i: Tuple, row: Series):
    super().__init__()
    self._symbol_id = i[0]
    self._price_date = i[1]
    self._open_price = row[AppConsts.PRICE_COL_OPEN]
    self._high_price = row[AppConsts.PRICE_COL_HIGH]
    self._low_price = row[AppConsts.PRICE_COL_LOW]
    self._close_price = row[AppConsts.PRICE_COL_CLOSE]
    self._volume = row[AppConsts.PRICE_COL_VOLUME]
    self._sma_period_1 = row[AppConsts.CUSTOM_COL_SMA_PERIOD_1]
    self._sma_period_2 = row[AppConsts.CUSTOM_COL_SMA_PERIOD_2]
    self._exponential_smoothing_price = row[AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE]
    self._is_exponential_smoothing_max = (row[AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_MAX] == 1)
    self._is_exponential_smoothing_min = (row[AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_MIN] == 1)
    self._abz_middle = row[AppConsts.CUSTOM_COL_ABZ_MIDDLE]
    self._abz_upper = row[AppConsts.CUSTOM_COL_ABZ_UPPER]
    self._abz_lower = row[AppConsts.CUSTOM_COL_ABZ_LOWER]

  @property
  def id(self) -> int: return self._id

  @id.setter
  def id(self, val: int) -> None: self._id = val

  @property
  def symbol_id(self) -> int: return self._symbol_id

  @symbol_id.setter
  def symbol_id(self, val: int) -> None: self._symbol_id = val

  @property
  def price_date(self) -> date: return self._price_date

  @price_date.setter
  def price_date(self, val: date) -> None: self._price_date = val

  @property
  def open_price(self) -> float: return self._open_price

  @open_price.setter
  def open_price(self, val: float) -> None: self._open_price = val

  @property
  def high_price(self) -> float: return self._high_price

  @high_price.setter
  def high_price(self, val: float) -> None: self._high_price = val

  @property
  def low_price(self) -> float: return self._low_price

  @low_price.setter
  def low_price(self, val: float) -> None: self._low_price = val

  @property
  def close_price(self) -> float: return self._close_price

  @close_price.setter
  def close_price(self, val: float) -> None: self._close_price = val

  @property
  def volume(self) -> int: return self._volume

  @volume.setter
  def volume(self, val: int) -> None: self._volume = val

  @property
  def sma_period_1(self) -> float: return self._sma_period_1

  @sma_period_1.setter
  def sma_period_1(self, val: float) -> None: self._sma_period_1 = val

  @property
  def sma_period_2(self) -> float: return self._sma_period_2

  @sma_period_2.setter
  def sma_period_2(self, val: float) -> None: self._sma_period_2 = val

  @property
  def exponential_smoothing_price(self) -> float: return self._exponential_smoothing_price

  @exponential_smoothing_price.setter
  def exponential_smoothing_price(self, val: float) -> None: self._exponential_smoothing_price = val

  @property
  def is_exponential_smoothing_max(self) -> bool: return self._is_exponential_smoothing_max

  @is_exponential_smoothing_max.setter
  def is_exponential_smoothing_max(self, val: bool) -> None: self._is_exponential_smoothing_max = val

  @property
  def is_exponential_smoothing_min(self) -> bool: return self._is_exponential_smoothing_min

  @is_exponential_smoothing_min.setter
  def is_exponential_smoothing_min(self, val: bool) -> None: self._is_exponential_smoothing_min = val

  @property
  def abz_middle(self) -> float: return self._abz_middle

  @abz_middle.setter
  def abz_middle(self, val: float) -> None: self._abz_middle = val

  @property
  def abz_upper(self) -> float: return self._abz_upper

  @abz_upper.setter
  def abz_upper(self, val: float) -> None: self._abz_upper = val

  @property
  def abz_lower(self) -> float: return self._abz_lower

  @abz_lower.setter
  def abz_lower(self, val: float) -> None: self._abz_lower = val

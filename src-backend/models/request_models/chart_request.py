from datetime import date
from app_consts import AppConsts
from app_utils.date_utils import DateUtils


class ChartRequest:

  @property
  def is_random_symbols(self) -> bool: return self._is_random_symbols

  @is_random_symbols.setter
  def is_random_symbols(self, val: bool) -> None: self._is_random_symbols = val

  @property
  def no_of_charts(self) -> int: return self._no_of_charts

  @no_of_charts.setter
  def no_of_charts(self, val: int) -> None: self._no_of_charts = val

  @property
  def symbol(self) -> str: return self._symbol

  @symbol.setter
  def symbol(self, val: str) -> None: self._symbol = val

  @property
  def date_from(self) -> str: return self._date_from

  @date_from.setter
  def date_from(self, val: str) -> None: self._date_from = val

  @property
  def date_from_obj(self) -> date: return DateUtils.get_date(self._date_from, '%Y-%m-%d')

  @property
  def date_to(self) -> str: return self._date_to

  @date_to.setter
  def date_to(self, val: str) -> None: self._date_to = val

  @property
  def date_to_obj(self) -> date: return DateUtils.get_date(self._date_to, '%Y-%m-%d')

  @property
  def is_exclude_sma(self) -> bool: return self._is_exclude_sma

  @is_exclude_sma.setter
  def is_exclude_sma(self, val: bool) -> None: self._is_exclude_sma = val

  @property
  def sma_period_1(self) -> int: return self._sma_period_1

  @sma_period_1.setter
  def sma_period_1(self, val: int) -> None: self._sma_period_1 = val

  @property
  def sma_period_2(self) -> int: return self._sma_period_2

  @sma_period_2.setter
  def sma_period_2(self, val: int) -> None: self._sma_period_2 = val

  @property
  def is_exclude_exponential_smoothing_prices(self) -> bool: return self._is_exclude_exponential_smoothing_prices

  @is_exclude_exponential_smoothing_prices.setter
  def is_exclude_exponential_smoothing_prices(self, val: bool) -> None: self._is_exclude_exponential_smoothing_prices = val

  @property
  def exponential_smoothing_prices_color(self) -> str: return self._exponential_smoothing_prices_color

  @exponential_smoothing_prices_color.setter
  def exponential_smoothing_prices_color(self, val: str) -> None: self._exponential_smoothing_prices_color = val

  @property
  def exponential_smoothing_prices_shift(self) -> float: return self._exponential_smoothing_prices_shift

  @exponential_smoothing_prices_shift.setter
  def exponential_smoothing_prices_shift(self, val: float) -> None: self._exponential_smoothing_prices_shift = val

  @property
  def exponential_smoothing_alpha(self) -> float: return self._exponential_smoothing_alpha

  @exponential_smoothing_alpha.setter
  def exponential_smoothing_alpha(self, val: float) -> None: self._exponential_smoothing_alpha = val

  @property
  def is_exclude_exponential_smoothing_max_min(self) -> bool: return self._is_exclude_exponential_smoothing_max_min

  @is_exclude_exponential_smoothing_max_min.setter
  def is_exclude_exponential_smoothing_max_min(self, val: bool) -> None: self._is_exclude_exponential_smoothing_max_min = val

  @property
  def exponential_smoothing_max_min_color(self) -> str: return self._exponential_smoothing_max_min_color

  @exponential_smoothing_max_min_color.setter
  def exponential_smoothing_max_min_color(self, val: str) -> None: self._exponential_smoothing_max_min_color = val

  @property
  def exponential_smoothing_max_min_diff(self) -> float: return self._exponential_smoothing_max_min_diff

  @exponential_smoothing_max_min_diff.setter
  def exponential_smoothing_max_min_diff(self, val: float) -> None: self._exponential_smoothing_max_min_diff = val

  @property
  def is_exclude_abz(self) -> bool: return self._is_exclude_abz

  @is_exclude_abz.setter
  def is_exclude_abz(self, val: bool) -> None: self._is_exclude_abz = val

  @property
  def abz_er_period(self) -> int: return self._abz_er_period

  @abz_er_period.setter
  def abz_er_period(self, val: int) -> None: self._abz_er_period = val

  @property
  def abz_std_distance(self) -> float: return self._abz_std_distance

  @abz_std_distance.setter
  def abz_std_distance(self, val: float) -> None: self._abz_std_distance = val

  @property
  def abz_constant_k(self) -> float: return self._abz_constant_k

  @abz_constant_k.setter
  def abz_constant_k(self, val: float) -> None: self._abz_constant_k = val

  def is_valid_model(self) -> bool:
    is_valid = True
    if self.is_random_symbols:
      is_valid = is_valid and self.no_of_charts
      is_valid = is_valid and self.no_of_charts >= 1
      is_valid = is_valid and self.no_of_charts <= 10
    else:
      is_valid = is_valid and self.symbol
    return is_valid \
        and self.date_from_obj \
        and self.date_from_obj >= AppConsts.MIN_DATE \
        and self.date_to_obj \
        and self.date_to_obj >= AppConsts.MIN_DATE \
        and self.date_from_obj < self.date_to_obj \
        and self.sma_period_1 >= 1 \
        and self.sma_period_1 <= 200 \
        and self.sma_period_2 >= 1 \
        and self.sma_period_2 <= 200 \
        and self.sma_period_1 != self.sma_period_2 \
        and self.exponential_smoothing_alpha >= 0.01 \
        and self.exponential_smoothing_alpha <= 1 \
        and self.exponential_smoothing_max_min_diff >= 0.01 \
        and self.exponential_smoothing_max_min_diff <= 5 \
        and self.abz_er_period >= 1 \
        and self.abz_er_period <= 100 \
        and self.abz_std_distance >= 0.01 \
        and self.abz_std_distance <= 5 \
        and self.abz_constant_k >= 0.01 \
        and self.abz_constant_k <= 200

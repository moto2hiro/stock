from typing import Any
from app_consts import AppConsts
from app_utils.date_utils import DateUtils
from app_utils.number_utils import NumberUtils
from models.db.symbol_master import SymbolMaster
from datetime import date, timedelta


class Transaction:

  @property
  def symbol_master(self) -> SymbolMaster: return self._symbol_master

  @symbol_master.setter
  def symbol_master(self, val: SymbolMaster) -> None: self._symbol_master = val

  @property
  def action(self) -> str: return self._action

  @action.setter
  def action(self, val: str) -> None: self._action = val

  @property
  def no_of_shares(self) -> int: return self._no_of_shares

  @no_of_shares.setter
  def no_of_shares(self, val: int) -> None: self._no_of_shares = val

  @property
  def start_price(self) -> float: return self._start_price

  @start_price.setter
  def start_price(self, val: Any) -> None: self._start_price = NumberUtils.to_float(val)

  @property
  def end_price(self) -> float: return self._end_price

  @end_price.setter
  def end_price(self, val: Any) -> None: self._end_price = NumberUtils.to_float(val)

  @property
  def start_date(self) -> date: return self._start_date

  @start_date.setter
  def start_date(self, val: date) -> None: self._start_date = val

  @property
  def end_date(self) -> date: return self._end_date

  @end_date.setter
  def end_date(self, val: date) -> None: self._end_date = val

  # region [Readonly Props]
  def set_readonly_props(self) -> None:
    if not hasattr(self, 'start_date') \
            or not hasattr(self, 'end_date') \
            or not hasattr(self, 'start_price') \
            or not hasattr(self, 'end_price') \
            or not hasattr(self, 'no_of_shares') \
            or not hasattr(self, 'action'):
      return
    delta: timedelta = DateUtils.get_diff(self._end_date, self._start_date)
    if self._action == AppConsts.ACTION_BUY:
      self._net_change_in_price = NumberUtils.round(self._end_price - self._start_price)
    elif self._action == AppConsts.ACTION_SELL:
      self._net_change_in_price = NumberUtils.round(self._start_price - self._end_price)
    self._year = self._end_date.year
    self._quarter = DateUtils.get_quarter(self._end_date.month)
    self._month = self._end_date.month
    self._hold_length_days = delta.days if delta else 0
    self._change_in_capital = NumberUtils.round(self._net_change_in_price * self._no_of_shares)
    self._has_profit = (self._change_in_capital > 0)

  @property
  def year(self) -> int: return self._year

  @property
  def quarter(self) -> int: return self._quarter

  @property
  def month(self) -> int: return self._month

  @property
  def hold_length_days(self) -> int: return self._hold_length_days

  @property
  def net_change_in_price(self) -> float: return self._net_change_in_price

  @property
  def change_in_capital(self) -> float: return self._change_in_capital

  @property
  def has_profit(self) -> bool: return self._has_profit
  # endregion

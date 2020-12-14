from itertools import groupby
from typing import Dict, List
from pandas.core.frame import DataFrame
from app_utils.model_utils import ModelUtils
from app_utils.number_utils import NumberUtils
from app_utils.stat_utils import StatUtils
from models.db.symbol_master import SymbolMaster
from models.request_models.back_test_run_request import BackTestRunRequest
from models.transaction import Transaction


class BackTestResultItem:

  def __init__(self, target: str, is_benchmark: bool) -> None:
    self._target = target
    self._is_benchmark = is_benchmark
    self._capital = {}
    self._capital_available = {}
    self._ttl_no_days = 0
    self._transactions = []

  @property
  def target(self) -> str: return self._target

  @target.setter
  def target(self, val: str) -> None: self._target = val

  @property
  def is_benchmark(self) -> bool: return self._is_benchmark

  @is_benchmark.setter
  def is_benchmark(self, val: bool) -> None: self._is_benchmark = val

  @property
  def capital(self) -> Dict: return self._capital

  @capital.setter
  def capital(self, val: Dict) -> None: self._capital = val

  @property
  def capital_available(self) -> Dict: return self._capital_available

  @capital_available.setter
  def capital_available(self, val: Dict) -> None: self._capital_available = val

  @property
  def ttl_no_days(self) -> int: return self._ttl_no_days

  @ttl_no_days.setter
  def ttl_no_days(self, val: int) -> None: self._ttl_no_days = val

  @property
  def transactions(self) -> List[Transaction]: return self._transactions

  @transactions.setter
  def transactions(self, val: List[Transaction]) -> None: self._transactions = val

  # region [Readonly Props]

  def set_readonly_props(self) -> None:
    if not self._transactions:
      return

    self._start_capital = self._capital.get(ModelUtils.get_first_key(self._capital))
    self._end_capital = self._capital.get(ModelUtils.get_last_key(self._capital))
    self._hold_length_days_stats = StatUtils.get_descriptive_stats([t.hold_length_days for t in self._transactions])
    self._change_in_capital_stats = StatUtils.get_descriptive_stats([t.change_in_capital for t in self._transactions])
    self._has_profit_stats = StatUtils.get_descriptive_stats([NumberUtils.to_int(t.has_profit) for t in self._transactions])
    self._pct_return = NumberUtils.get_change(self._end_capital, self._start_capital)

    self._best_transactions = [t for t in sorted(self._transactions, key=lambda x: x.change_in_capital, reverse=True) if t.has_profit][:20]
    self._worst_transactions = [t for t in sorted(self._transactions, key=lambda x: x.change_in_capital) if not t.has_profit][:20]

    symbol_grouped: Dict = {}
    for t in self._transactions:
      if not t.symbol_master.symbol in symbol_grouped:
        symbol_grouped[t.symbol_master.symbol]: Dict = {
            'symbol_master': t.symbol_master,
            'change_in_capital': 0,
            'no_of_transactions': 0}
      symbol_grouped[t.symbol_master.symbol]['change_in_capital'] += t.change_in_capital
      symbol_grouped[t.symbol_master.symbol]['no_of_transactions'] += 1

    symbol_grouped_list: List[BackTestResultItemPerSymbol] = []
    for k, v in symbol_grouped.items():
      item: BackTestResultItemPerSymbol = BackTestResultItemPerSymbol()
      item.symbol_master = symbol_grouped[k]['symbol_master']
      item.change_in_capital = NumberUtils.round(symbol_grouped[k]['change_in_capital'])
      item.no_of_transactions = symbol_grouped[k]['no_of_transactions']
      symbol_grouped_list.append(item)
    self._best_symbols = [i for i in sorted(symbol_grouped_list, key=lambda x: x.change_in_capital, reverse=True) if i.change_in_capital > 0][:20]
    self._worst_symbols = [i for i in sorted(symbol_grouped_list, key=lambda x: x.change_in_capital) if i.change_in_capital < 0][:20]

  @property
  def start_capital(self) -> float: return self._start_capital

  @property
  def end_capital(self) -> float: return self._end_capital

  @property
  def hold_length_days_stats(self) -> Dict: return self._hold_length_days_stats

  @property
  def hold_length_days_stats_per_symbol(self) -> Dict: return self._hold_length_days_stats_per_symbol

  @property
  def change_in_capital_stats(self) -> Dict: return self._change_in_capital_stats

  @property
  def change_in_capital_stats_per_symbol(self) -> Dict: return self._change_in_capital_stats_per_symbol

  @property
  def has_profit_stats(self) -> bool: return self._has_profit_stats

  @property
  def has_profit_stats_per_symbol(self) -> bool: return self._has_profit_stats_per_symbol

  @property
  def pct_return(self) -> float: return self._pct_return

  @property
  def best_transactions(self) -> List[Transaction]: return self._best_transactions

  @property
  def worst_transactions(self) -> List[Transaction]: return self._worst_transactions

  @property
  def best_symbols(self) -> List[Dict]: return self._best_symbols

  @property
  def worst_symbols(self) -> List[Dict]: return self._best_symbols
  # endregion


class BackTestResultItemPerSymbol:

  @property
  def symbol_master(self) -> SymbolMaster: return self._symbol_master

  @symbol_master.setter
  def symbol_master(self, val: SymbolMaster) -> None: self._symbol_master = val

  @property
  def change_in_capital(self) -> float: return self._change_in_capital

  @change_in_capital.setter
  def change_in_capital(self, val: float) -> None: self._change_in_capital = val

  @property
  def no_of_transactions(self) -> int: return self._no_of_transactions

  @no_of_transactions.setter
  def no_of_transactions(self, val: int) -> None: self._no_of_transactions = val

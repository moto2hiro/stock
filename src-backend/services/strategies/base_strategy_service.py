from pandas.core.frame import DataFrame
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from datetime import date
from app_utils.model_utils import ModelUtils
from models.db.symbol_master import SymbolMaster
from services.calc_service import CalcService


class BaseStrategyService(ABC):

  def __init__(self, strategy_request: Any, symbols: List[SymbolMaster], prices: DataFrame) -> None:
    self._calc_service = CalcService()
    self._strategy_request = strategy_request
    self._symbols = symbols
    self._prices = prices

  @property
  def strategy_request(self): pass

  @property
  def symbols(self) -> List[SymbolMaster]: return self._symbols

  @property
  def prices(self) -> DataFrame: return self._prices

  @prices.setter
  def prices(self, val: DataFrame) -> None: self._prices = val

  @abstractmethod
  def _get_action(self) -> str: pass

  @abstractmethod
  def _is_valid_request(self) -> bool: pass

  @abstractmethod
  def _do_preparations(self) -> None: pass

  @abstractmethod
  def _do_calculations(self, symbol_id: int, current_date: date) -> None: pass

  @abstractmethod
  def _has_entry_conditions(self, symbol_id: int, current_date: date) -> bool: pass

  @abstractmethod
  def _has_exit_conditions(self, symbol_id: int, current_date: date) -> bool: pass

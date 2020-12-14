from datetime import date
from typing import Any, Dict, List
from app_consts import AppConsts
from app_utils.string_utils import StringUtils


class TradeSuggestionsRequest:
  def __init__(self) -> None:
    pass

  @property
  def is_job(self) -> bool: return self._is_job

  @is_job.setter
  def is_job(self, val: bool) -> None: self._is_job = val

  @property
  def strategy_type(self) -> str: return self._strategy_type

  @strategy_type.setter
  def strategy_type(self, val: str) -> None: self._strategy_type = val

  @property
  def strategy_request(self) -> Dict: return self._strategy_request

  @strategy_request.setter
  def strategy_request(self, val: Dict) -> None: self._strategy_request = val

  @property
  def current_capital(self) -> float: return self._current_capital

  @current_capital.setter
  def current_capital(self, val: float) -> None: self._current_capital = val

  @property
  def pct_risk_per_trade(self) -> float: return self._pct_risk_per_trade

  @pct_risk_per_trade.setter
  def pct_risk_per_trade(self, val: float) -> None: self._pct_risk_per_trade = val

  @property
  def volume_limit(self) -> float: return self._volume_limit

  @volume_limit.setter
  def volume_limit(self, val: float) -> None: self._volume_limit = val

  @property
  def test_limit_symbol(self) -> int: return self._test_limit_symbol

  @test_limit_symbol.setter
  def test_limit_symbol(self, val: int) -> None: self._test_limit_symbol = val

  @property
  def adv_min(self) -> int: return self._adv_min

  @adv_min.setter
  def adv_min(self, val: int) -> None: self._adv_min = val

  @property
  def adpv_min(self) -> int: return self._adpv_min

  @adpv_min.setter
  def adpv_min(self, val: int) -> None: self._adpv_min = val

  def is_valid_model(self) -> bool:
    return not StringUtils.isNullOrWhitespace(self.strategy_type) \
        and self.pct_risk_per_trade > 0 \
        and self.pct_risk_per_trade <= 100 \
        and self.volume_limit >= 0.01 \
        and self.volume_limit <= 100 \
        and self.test_limit_symbol >= 1

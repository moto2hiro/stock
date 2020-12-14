from datetime import date
from typing import Any, Dict, List
from app_consts import AppConsts
from app_utils.string_utils import StringUtils
from app_utils.date_utils import DateUtils


class BackTestRunRequest:
  def __init__(self) -> None:
    self._benchmark_etfs = []

  @property
  def strategy_type(self) -> str: return self._strategy_type

  @strategy_type.setter
  def strategy_type(self, val: str) -> None: self._strategy_type = val

  @property
  def strategy_request(self) -> Dict: return self._strategy_request

  @strategy_request.setter
  def strategy_request(self, val: Dict) -> None: self._strategy_request = val

  @property
  def start_capital(self) -> float: return self._start_capital

  @start_capital.setter
  def start_capital(self, val: float) -> None: self._start_capital = val

  @property
  def pct_risk_per_trade(self) -> float: return self._pct_risk_per_trade

  @pct_risk_per_trade.setter
  def pct_risk_per_trade(self, val: float) -> None: self._pct_risk_per_trade = val

  @property
  def portfolio_max(self) -> int: return self._portfolio_max

  @portfolio_max.setter
  def portfolio_max(self, val: int) -> None: self._portfolio_max = val

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
  def benchmark_etfs(self) -> List[str]: return self._benchmark_etfs

  @benchmark_etfs.setter
  def benchmark_etfs(self, val: List[str]) -> None: self._benchmark_etfs = val

  @property
  def slippage(self) -> int: return self._slippage

  @slippage.setter
  def slippage(self, val: int) -> None: self._slippage = val

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
        and self.start_capital > 0 \
        and self.pct_risk_per_trade > 0 \
        and self.pct_risk_per_trade <= 100 \
        and self.portfolio_max > 0 \
        and self.date_from_obj \
        and self.date_from_obj >= AppConsts.MIN_DATE \
        and self.date_to_obj \
        and self.date_to_obj >= AppConsts.MIN_DATE \
        and self.date_from_obj < self.date_to_obj \
        and self.slippage >= 0 \
        and self.volume_limit >= 0.01 \
        and self.volume_limit <= 100 \
        and self.test_limit_symbol >= 1

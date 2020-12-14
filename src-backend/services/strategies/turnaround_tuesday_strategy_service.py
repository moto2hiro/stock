import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from typing import Any, List
from datetime import date
from app_consts import AppConsts
from app_utils.log_utils import LogUtils
from models.db.symbol_master import SymbolMaster
from services.strategies.base_strategy_service import BaseStrategyService
pd.options.mode.chained_assignment = None


class TurnaroundTuesdayStrategyService(BaseStrategyService):

  def __init__(self, strategy_request: Any, symbols: List[SymbolMaster], prices: DataFrame) -> None:
    super().__init__(strategy_request, symbols, prices)

  def _get_action(self) -> str:
    return AppConsts.ACTION_BUY

  def _do_preparations(self) -> None:
    pass

  def _is_valid_request(self) -> bool:
    return True

  def _do_calculations(self, symbol_id: int, current_date: date) -> None:
    pass

  def _has_entry_conditions(self, symbol_id: int, current_date: date) -> bool:
    has_conditions: bool = False
    if current_date.weekday() == AppConsts.WEEKDAY_IDX_MON:
      current_price: Series = self._prices.loc[symbol_id, current_date]
      has_conditions = current_price.loc[AppConsts.PRICE_COL_OPEN] < current_price.loc[AppConsts.PRICE_COL_CLOSE]
    return has_conditions

  def _has_exit_conditions(self, symbol_id: int, current_date: date) -> bool:
    return True

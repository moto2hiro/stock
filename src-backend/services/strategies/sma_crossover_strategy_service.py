import numpy as np
import pandas as pd
import random
from numpy import ndarray
from datetime import date
from random import randrange
from typing import Any, List
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from app_consts import AppConsts
from app_utils.log_utils import LogUtils
from app_utils.model_utils import ModelUtils
from app_utils.number_utils import NumberUtils
from models.db.symbol_master import SymbolMaster
from models.request_models.strategies.sma_crossover_strategy_request import SmaCrossoverStrategyRequest
from services.strategies.base_strategy_service import BaseStrategyService

pd.options.mode.chained_assignment = None


class SmaCrossoverStrategyService(BaseStrategyService):

  def __init__(self, strategy_request: Any, symbols: List[SymbolMaster], prices: DataFrame) -> None:
    super().__init__(strategy_request, symbols, prices)
    self._target: Dict = {}

  @property
  def strategy_request(self) -> SmaCrossoverStrategyRequest:
    return ModelUtils.get_obj(SmaCrossoverStrategyRequest(), self._strategy_request)

  def _get_action(self) -> str:
    return AppConsts.ACTION_BUY

  def _do_preparations(self) -> None:

    for symbol in self.symbols:
      symbol_prices: DataFrame = self.prices.loc[[symbol.id]]
      if symbol_prices.empty:
        continue

      # SMA Fast
      self.prices = self._calc_service.append_sma(
          prices=self.prices,
          index=[symbol.id],
          sma_period=self.strategy_request.sma_period_fast,
          sma_column_name=AppConsts.CUSTOM_COL_SMA_FAST)

      # SMA Slow
      self.prices = self._calc_service.append_sma(
          prices=self.prices,
          index=[symbol.id],
          sma_period=self.strategy_request.sma_period_slow,
          sma_column_name=AppConsts.CUSTOM_COL_SMA_SLOW)

  def _is_valid_request(self) -> bool:
    return self.strategy_request \
        and self.strategy_request.sma_period_fast > 0 \
        and self.strategy_request.sma_period_slow > 0 \
        and self.strategy_request.sma_period_fast < self.strategy_request.sma_period_slow

  def _do_calculations(self, symbol_id: int, current_date: date) -> None:
    pass

  def _has_entry_conditions(self, symbol_id: int, current_date: date) -> bool:
    current_row: Series = self._prices.loc[symbol_id, current_date]
    if NumberUtils.to_float(current_row.loc[AppConsts.CUSTOM_COL_SMA_SLOW]) == 0:
      return False
    is_above: bool = (current_row.loc[AppConsts.CUSTOM_COL_SMA_FAST] > current_row.loc[AppConsts.CUSTOM_COL_SMA_SLOW])
    if not symbol_id in self._target:
      self._target[symbol_id] = {}
      self._target[symbol_id]['is_above'] = is_above
      return False
    was_above: bool = self._target[symbol_id]['is_above']
    self._target[symbol_id]['is_above'] = is_above
    return (is_above and not was_above)

  def _has_exit_conditions(self, symbol_id: int, current_date: date) -> bool:
    current_row: Series = self._prices.loc[symbol_id, current_date]
    is_below: bool = (current_row.loc[AppConsts.CUSTOM_COL_SMA_FAST] < current_row.loc[AppConsts.CUSTOM_COL_SMA_SLOW])
    return True  # is_below

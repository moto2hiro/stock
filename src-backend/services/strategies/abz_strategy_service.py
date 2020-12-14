import numpy as np
import pandas as pd
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
from models.request_models.strategies.abz_strategy_request import AbzStrategyRequest
from services.strategies.base_strategy_service import BaseStrategyService

pd.options.mode.chained_assignment = None


class AbzStrategyService(BaseStrategyService):

  def __init__(self, strategy_request: Any, symbols: List[SymbolMaster], prices: DataFrame) -> None:
    super().__init__(strategy_request, symbols, prices)

  @property
  def strategy_request(self) -> AbzStrategyRequest:
    return ModelUtils.get_obj(AbzStrategyRequest(), self._strategy_request)

  def _get_action(self) -> str:
    return AppConsts.ACTION_BUY

  def _do_preparations(self) -> None:

    for symbol in self.symbols:
      symbol_prices: DataFrame = self.prices.loc[[symbol.id]]
      if symbol_prices.empty:
        continue

      # ABZ
      self.prices = self._calc_service.append_abz(
          prices=self.prices,
          index=[symbol.id],
          abz_er_period=self.strategy_request.abz_er_period,
          abz_std_distance=self.strategy_request.abz_std_distance,
          abz_constant_k=self.strategy_request.abz_constant_k)

  def _is_valid_request(self) -> bool:
    return self.strategy_request \
        and self.strategy_request.abz_er_period >= 1 \
        and self.strategy_request.abz_er_period <= 100 \
        and self.strategy_request.abz_std_distance >= 0.01 \
        and self.strategy_request.abz_std_distance <= 5 \
        and self.strategy_request.abz_constant_k >= 0.01 \
        and self.strategy_request.abz_constant_k <= 200

  def _do_calculations(self, symbol_id: int, current_date: date) -> None:
    pass

  def _has_entry_conditions(self, symbol_id: int, current_date: date) -> bool:
    current_row: Series = self._prices.loc[symbol_id, current_date]
    close: bool = current_row.loc[AppConsts.PRICE_COL_CLOSE]
    upper: bool = current_row.loc[AppConsts.CUSTOM_COL_ABZ_UPPER]
    return close > upper

  def _has_exit_conditions(self, symbol_id: int, current_date: date) -> bool:
    current_row: Series = self._prices.loc[symbol_id, current_date]
    close: bool = current_row.loc[AppConsts.PRICE_COL_CLOSE]
    upper: bool = current_row.loc[AppConsts.CUSTOM_COL_ABZ_UPPER]
    return close < upper

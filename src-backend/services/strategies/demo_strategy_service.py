from datetime import date
from random import randrange
from typing import Any, List

import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from app_consts import AppConsts
from app_utils.model_utils import ModelUtils
from models.db.symbol_master import SymbolMaster
from models.request_models.strategies.demo_strategy_request import \
    DemoStrategyRequest
from services.strategies.base_strategy_service import BaseStrategyService

pd.options.mode.chained_assignment = None


class DemoStrategyService(BaseStrategyService):

  def __init__(self, strategy_request: Any, symbols: List[SymbolMaster], prices: DataFrame) -> None:
    super().__init__(strategy_request, symbols, prices)

  @property
  def strategy_request(self) -> DemoStrategyRequest:
    return ModelUtils.get_obj(DemoStrategyRequest(), self._strategy_request)

  def _get_action(self) -> str:
    return AppConsts.ACTION_BUY

  def _do_preparations(self) -> None:
    """
    Prepare custom_property column inside the Price DataFrame
    """
    self._prices['custom_property'] = 0

  def _is_valid_request(self) -> bool:
    """
    Validate strategy_request
    """
    return self.strategy_request \
        and self.strategy_request.param_1 >= 0.01 \
        and self.strategy_request.param_1 <= 100 \
        and self.strategy_request.param_2 != ''

  def _do_calculations(self, symbol_id: int, current_date: date) -> None:
    """
    Calculate/Set custom_property value
    """
    self._prices['custom_property'].loc[symbol_id, current_date] = randrange(2)

  def _has_entry_conditions(self, symbol_id: int, current_date: date) -> bool:
    """
    Check entry conditions 
    """
    current_price: Series = self._prices.loc[symbol_id, current_date]
    return (current_price.loc['custom_property'] == 0)

  def _has_exit_conditions(self, symbol_id: int, current_date: date) -> bool:
    """
    Check exit conditions
    """
    current_price: Series = self._prices.loc[symbol_id, current_date]
    return (current_price.loc['custom_property'] == 0)

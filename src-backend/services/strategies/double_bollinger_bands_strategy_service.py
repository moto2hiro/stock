import statistics
import json
import pandas as pd
import numpy as np
from datetime import date, timedelta
from typing import Any, List
from pandas.core.frame import DataFrame

from app_db import db
from app_consts import AppConsts
from app_utils.string_utils import StringUtils
from app_utils.model_utils import ModelUtils
from services.base_service import BaseService
from models.db.symbol_master import SymbolMaster as SM
from models.db.stock_price_daily import StockPriceDaily
from models.request_models.strategies.double_bollinger_bands_strategy_request import DoubleBollingerBandsStrategyRequest
from services.strategies.base_strategy_service import BaseStrategyService
from models.request_models.strategies.demo_strategy_request import DemoStrategyRequest

close_price_of_date_entered: dict = {}


class DoubleBollingerBandsStrategyService(BaseStrategyService):

  def __init__(self, strategy_request: Any, symbols: List[SM], prices: DataFrame) -> None:
    super().__init__(strategy_request, symbols, prices)

  @property
  def strategy_request(self) -> DoubleBollingerBandsStrategyRequest:
    return ModelUtils.get_obj(DoubleBollingerBandsStrategyRequest(), self._strategy_request)

  def _get_action(self) -> str:
    return AppConsts.ACTION_BUY

  def _do_preparations(self) -> None:
    for symbol in self.symbols:
      symbol_prices: DataFrame = self.prices.loc[[symbol.id]]
      if symbol_prices.empty:
        continue

      # SMA (Middle Band)
      self.prices = self._calc_service.append_sma(
          prices=self.prices,
          index=[symbol.id],
          sma_period=self.strategy_request.sma_period,
          sma_column_name=AppConsts.CUSTOM_COL_SMA)

      # STD
      self.prices = self._calc_service.append_std(
          prices=self.prices,
          index=[symbol.id],
          std_period=self.strategy_request.sma_period,
          std_column_name=AppConsts.CUSTOM_COL_STD)

      # Double Bollinger Bands
      self.prices = self._calc_service.append_double_bollinger_bands(
          prices=self.prices,
          index=[symbol.id],
          std_distance=self.strategy_request.std_distance)

  def _is_valid_request(self) -> bool:
    return self.strategy_request \
        and self.strategy_request.sma_period >= 1 \
        and self.strategy_request.std_distance >= 1 \
        and self.strategy_request.std_distance <= 5 \


  def _do_calculations(self, symbol_id: int, current_date: date) -> None:
    pass

  def _has_entry_conditions(self, symbol_id: int, current_date: date) -> bool:
    current_row: Series = self._prices.loc[symbol_id, current_date]
    is_enter: bool = (current_row.loc[AppConsts.CUSTOM_COL_DOUBLE_BOLLINGER_BANDS] == 1)
    return is_enter

  def _has_exit_conditions(self, symbol_id: int, current_date: date) -> bool:
    current_row: Series = self._prices.loc[symbol_id, current_date]
    is_exit: bool = (current_row.loc[AppConsts.CUSTOM_COL_DOUBLE_BOLLINGER_BANDS] == 0)
    return is_exit

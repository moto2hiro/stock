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
from models.request_models.strategies.inverted_head_and_shoulders_strategy_request import InvertedHeadAndShouldersRequest
from services.strategies.base_strategy_service import BaseStrategyService

pd.options.mode.chained_assignment = None


class InvertedHeadAndShouldersStrategyService(BaseStrategyService):

  def __init__(self, strategy_request: Any, symbols: List[SymbolMaster], prices: DataFrame) -> None:
    super().__init__(strategy_request, symbols, prices)
    self._target: Dict = {}

  @property
  def strategy_request(self) -> InvertedHeadAndShouldersRequest:
    return ModelUtils.get_obj(InvertedHeadAndShouldersRequest(), self._strategy_request)

  def _get_action(self) -> str:
    return AppConsts.ACTION_BUY

  def _do_preparations(self) -> None:

    for symbol in self.symbols:
      symbol_prices: DataFrame = self.prices.loc[[symbol.id]]
      if symbol_prices.empty:
        continue

      # Exponential Price Smoothing
      self.prices = self._calc_service.append_exponential_smoothing_price(
          prices=self.prices,
          index=[symbol.id],
          alpha=self.strategy_request.exponential_smoothing_alpha)

      # Exponential Price Smoothing Max/Min
      self.prices = self._calc_service.append_exponential_smoothing_max_min(
          prices=self.prices,
          index=[symbol.id],
          exponential_smoothing_max_min_diff=self.strategy_request.exponential_smoothing_max_min_diff)

      # region Inverted Head And Shoulders
      self.prices = self._calc_service.append_inverted_head_and_shoulders(
          prices=self.prices,
          index=[symbol.id],
          price_column=AppConsts.PRICE_COL_CLOSE,
          smooth_price_column=AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_PRICE,
          max_column=AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_MAX,
          min_column=AppConsts.CUSTOM_COL_EXPONENTIAL_SMOOTHING_MIN,
          shoulder_diff=self.strategy_request.shoulder_diff,
          neck_diff=self.strategy_request.neck_diff)

  def _is_valid_request(self) -> bool:
    return self.strategy_request \
        and self.strategy_request.exponential_smoothing_alpha >= 0.01 \
        and self.strategy_request.exponential_smoothing_alpha <= 1 \
        and self.strategy_request.exponential_smoothing_max_min_diff >= 0.01 \
        and self.strategy_request.exponential_smoothing_max_min_diff <= 5 \
        and self.strategy_request.shoulder_diff >= 0.01 \
        and self.strategy_request.shoulder_diff <= 5 \
        and self.strategy_request.neck_diff >= 0.01 \
        and self.strategy_request.neck_diff <= 5

  def _do_calculations(self, symbol_id: int, current_date: date) -> None:
    pass

  def _has_entry_conditions(self, symbol_id: int, current_date: date) -> bool:
    current_row: Series = self._prices.loc[symbol_id, current_date]
    has_inverted_head_and_shoulders: bool = (current_row.loc[AppConsts.CUSTOM_COL_INVERTED_HEAD_AND_SHOULDERS] == 1)
    if has_inverted_head_and_shoulders:
      self._target[symbol_id] = {}
      self._target[symbol_id]['target_price'] = current_row.loc[AppConsts.CUSTOM_COL_INVERTED_HEAD_AND_SHOULDERS_TARGET_PRICE]
      self._target[symbol_id]['stop_loss'] = current_row.loc[AppConsts.CUSTOM_COL_INVERTED_HEAD_AND_SHOULDERS_STOP_LOSS]
    return has_inverted_head_and_shoulders

  def _has_exit_conditions(self, symbol_id: int, current_date: date) -> bool:
    current_row: Series = self._prices.loc[symbol_id, current_date]
    is_exit: bool = current_row.loc[AppConsts.PRICE_COL_CLOSE] > self._target[symbol_id]['target_price'] \
        or current_row.loc[AppConsts.PRICE_COL_CLOSE] < self._target[symbol_id]['stop_loss']
    return is_exit

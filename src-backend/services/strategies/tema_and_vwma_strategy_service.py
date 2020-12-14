import statistics
import json
import pandas as pd
import numpy as np
from datetime import date, timedelta
from typing import Any, List
from pandas.core.frame import DataFrame, Series

from app_db import db
from app_consts import AppConsts
from app_utils.string_utils import StringUtils
from app_utils.model_utils import ModelUtils
from services.base_service import BaseService
from models.db.symbol_master import SymbolMaster as SM
from models.db.stock_price_daily import StockPriceDaily
from models.request_models.strategies.tema_and_vwma_strategy_request import TEMAandVWMAStrategyRequest
from services.strategies.base_strategy_service import BaseStrategyService
from models.request_models.strategies.demo_strategy_request import DemoStrategyRequest

close_price_of_date_entered: dict = {}


class TEMAandVWMAStrategyService(BaseStrategyService):

  def __init__(self, strategy_request: Any, symbols: List[SM], prices: DataFrame) -> None:
    super().__init__(strategy_request, symbols, prices)

  def _get_action(self) -> str:
    return AppConsts.ACTION_BUY

  def _do_preparations(self) -> None:
    def EMA(target_series) -> Series:
      ema = target_series.ewm(span=tema_period, adjust=False).mean()
      return ema

    tema_period: int = int(self.strategy_request.tema_period)
    vwma_period: int = int(self.strategy_request.vwma_period)
    
    for symbol in self.symbols:
      symbol_prices: DataFrame = self.prices.loc[[symbol.id]]
      close_price: Series = symbol_prices['close_price']
      volume: Series = symbol_prices['volume']

      # TEMA
      ema1: Series = EMA(close_price)
      ema2: Series = EMA(ema1)
      ema3: Series = EMA(ema2)
      tema: Series = (3 * ema1) - (3 * ema2) + ema3
      tema = pd.Series(tema, name='tema')

      # VWMA
      close_price_times_volume: Series = close_price * volume
      close_price_times_volume_rolling: Series = close_price_times_volume.rolling(tema_period).sum()
      volume_rolling: Series = volume.rolling(tema_period).sum()
      vwma: Series = close_price_times_volume_rolling / volume_rolling
      vwma = pd.Series(vwma, name='vwma')

      self._prices['tema'] = np.nan
      self._prices['vwma'] = np.nan

      for i in symbol_prices.index:
        t = tema.loc[i]
        v = vwma.loc[i]
        self._prices['tema'].loc[i] = t
        self._prices['vwma'].loc[i] = v
    

  @property
  def strategy_request(self) -> DemoStrategyRequest:
    return ModelUtils.get_obj(DemoStrategyRequest(), self._strategy_request)
  

  def _is_valid_request(self) -> bool:
    return self.strategy_request \
        and self.strategy_request.tema_period > 0 \
        and self.strategy_request.vwma_period > 0


  def _do_calculations(self, symbol_id: int, current_date: date) -> None:
    pass
    '''def append_ema(name, ema):
      if name == 1:
        ema1_list.append(ema)
      if name == 2:
        ema2_list.append(ema)
      if name == 3:
        ema3_list.append(ema)
    
    def calculate_ema(target_column, name):
      ema_close_price = df_by_symbol_id[target_column].iloc[index]
      ema_previous = df_by_symbol_id[ema_column].iloc[index - 1]
      ema = ema_previous + (multiplier * (ema_close_price - ema_previous))
      df_by_symbol_id.loc[index, ema_column] = ema
      append_ema(name, ema)

    df: DataFrame = self._prices
    tema_period: int = int(self.strategy_request.tema_period)
    vwma_period: int = int(self.strategy_request.vwma_period)

    df_by_symbol_id: DataFrame = df.xs(symbol_id, level='symbol_id', drop_level=False)
    df_by_symbol_id: DataFrame = df_by_symbol_id.reset_index(level=[0, 1])

    ema_period_name: list = [1, 2, 3]
    ema_target: list = ['close_price', 'ema1', 'ema2']
    volume_list: list = []
    close_price_times_volume_list: list = []


    for index, rows in df_by_symbol_id.iterrows():
      ema1_list: list = []
      ema2_list: list = []
      ema3_list: list = []
      close_price: float = rows['close_price']
      volume: float = rows['volume']
      for name, target in zip(ema_period_name, ema_target):
        ema_column: str = 'ema' + str(name)
        multiplier: float = (2 / (tema_period + 1))
        if index == 0:
          df_by_symbol_id.loc[index, ema_column] = close_price
          append_ema(name, close_price)
        else:
          calculate_ema(target, name)

      ema1 = ema1_list[0]
      ema2 = ema2_list[0]
      ema3 = ema3_list[0]
      tema: float = (3 * ema1) - (3 * ema2) + ema3
      df_by_symbol_id.loc[index, 'tema'] = tema

      close_price_times_volume: float = close_price * volume
      close_price_times_volume_list.append(close_price_times_volume)
      volume_list.append(volume)

      if index >= vwma_period - 1:
        close_price_times_volume_list = close_price_times_volume_list[-vwma_period:]
        volume_list = volume_list[-vwma_period:]
        sum_of_close_price_times_volume_list: float = sum(close_price_times_volume_list)
        sum_of_volume_list: float = sum(volume_list)
        vwma: float = sum_of_close_price_times_volume_list / sum_of_volume_list
        df_by_symbol_id.loc[index, 'vwma'] = vwma
      else:
        pass

    df_by_symbol_id_and_date: DataFrame = df_by_symbol_id.loc[(df_by_symbol_id['symbol_id'] == symbol_id) & (df_by_symbol_id['price_date'] == current_date)]
    df_by_symbol_id_and_date: DataFrame = df_by_symbol_id_and_date.reset_index(drop=True)

    if not df_by_symbol_id_and_date.empty:
      df_tema: float = df_by_symbol_id_and_date['tema'].iloc[0]
      df_vwma: float = df_by_symbol_id_and_date['vwma'].iloc[0]
      df_new_column_value: list = [df_tema, df_vwma]
      df_new_column_name: list = ['tema', 'vwma']

      for new_value, new_column in zip(df_new_column_value, df_new_column_name):
        self._prices[new_column].loc[symbol_id, current_date] = new_value'''


  def _has_entry_conditions(self, symbol_id: int, current_date: date) -> bool:
    df: DataFrame = self._prices

    df_by_symbol_id: DataFrame = df.xs(symbol_id, level='symbol_id', drop_level=False)
    df_by_symbol_id: DataFrame = df_by_symbol_id.reset_index(level=[0, 1])

    df_by_symbol_id_and_date: DataFrame = df_by_symbol_id.loc[(df_by_symbol_id['symbol_id'] == symbol_id) & (df_by_symbol_id['price_date'] <= current_date)]
    df_by_symbol_id_and_date: DataFrame = df_by_symbol_id_and_date.reset_index(drop=True)
    last_index = df_by_symbol_id_and_date.index[-1]

    for index, rows in df_by_symbol_id_and_date.iterrows():
      if index == last_index:
        if pd.notna(rows['vwma']) == True:
          cp = rows['close_price']
          tema = rows['tema']
          vwma = rows['vwma']
          if tema > vwma:
            current_price: Series = self._prices.loc[symbol_id, current_date]
            close_price_of_date_entered[symbol_id] = cp
            return True
          else:
            return False
        else:
          return False
      else:
        pass


  def _has_exit_conditions(self, symbol_id: int, current_date: date) -> bool:
    df: DataFrame = self._prices

    df_by_symbol_id: DataFrame = df.xs(symbol_id, level='symbol_id', drop_level=False)
    df_by_symbol_id: DataFrame = df_by_symbol_id.reset_index(level=[0, 1])

    df_by_symbol_id_and_date: DataFrame = df_by_symbol_id.loc[(df_by_symbol_id['symbol_id'] == symbol_id) & (df_by_symbol_id['price_date'] == current_date)]
    df_by_symbol_id_and_date: DataFrame = df_by_symbol_id_and_date.reset_index(drop=True)

    cp = df_by_symbol_id_and_date['close_price'].iloc[0]
    vwma = df_by_symbol_id_and_date['vwma'].iloc[0]
    cp_of_date_entered = close_price_of_date_entered.get(symbol_id)
    stop_loss = cp_of_date_entered * (1 - 2 / 100)
    if cp < vwma or cp < stop_loss:
      current_price: Series = self._prices.loc[symbol_id, current_date]
      del close_price_of_date_entered[symbol_id]
      return True
    else:
      False




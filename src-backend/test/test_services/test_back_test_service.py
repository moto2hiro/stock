import random
import pandas as pd
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from pandas import Timestamp
from datetime import date, datetime
from typing import List
from test.test_base import TestBase
from exceptions.bad_request_exception import BadRequestException
from exceptions.db_connection_exception import DbConnectionException
from app_consts import AppConsts
from models.db.symbol_master import SymbolMaster
from models.request_models.back_test_run_request import BackTestRunRequest
from services.back_test_service import BackTestService
from services.calc_service import CalcService


class TestBackTestService(TestBase):

  def __init__(self, *args, **kwargs):
    super(TestBackTestService, self).__init__(*args, **kwargs)
    self.__back_test_service: BackTestService = BackTestService()
    self.__calc_service: CalcService = CalcService()

  def __get_test_dataframe__(self) -> DataFrame:
    symbols: List[int] = [1, 2, 3, 4]
    prices: DataFrame = pd.DataFrame(
        data=[
            [1, date(2000, 1, 1), 50, 100, 100000],
            [1, date(2000, 1, 2), 150, 200, 200000],
            [1, date(2000, 1, 3), 250, 300, 300000],
            [2, date(2000, 1, 1), 650, 700, 700000],
            [2, date(2000, 1, 2), 750, 800, 800000],
            [2, date(2000, 1, 3), 850, 900, 900000],
            [3, date(2000, 1, 2), 650, 700, 700000],
            [3, date(2000, 1, 3), 750, 800, 800000],
            [3, date(2000, 1, 4), 850, 900, 900000],
            [4, date(2000, 1, 3), 750, 800, 800000],
            [4, date(2000, 1, 4), 850, 900, 900000],
            [4, date(2000, 1, 5), 850, 900, 900000],
            [4, date(2000, 1, 6), 650, 700, 700000],
        ],
        columns=[
            AppConsts.PRICE_COL_SYMBOL_ID,
            AppConsts.PRICE_COL_DATE,
            AppConsts.PRICE_COL_OPEN,
            AppConsts.PRICE_COL_CLOSE,
            AppConsts.PRICE_COL_VOLUME])
    prices = prices.set_index([AppConsts.PRICE_COL_SYMBOL_ID, AppConsts.PRICE_COL_DATE])
    for s in symbols:
      prices = self.__calc_service.append_sma(
          prices=prices,
          index=[s],
          sma_period=1,
          sma_column_name=AppConsts.CUSTOM_COL_ADV,
          target_column=AppConsts.PRICE_COL_VOLUME)

    return prices

  def __get_test_series__(self) -> Series:
    prices: DataFrame = self.__get_test_dataframe__()
    return prices.loc[1, date(2000, 1, 1)]

  def test_get_symbols_should_return_appropriately(self) -> None:
    # ARRANGE
    none_case = None
    no_test_limit_symbol_case: BackTestRunRequest = BackTestRunRequest()
    no_test_limit_symbol_case.test_limit_symbol = 0
    no_benchmark_case: BackTestRunRequest = BackTestRunRequest()
    no_benchmark_case.test_limit_symbol = 5
    benchmark_case: BackTestRunRequest = BackTestRunRequest()
    benchmark_case.test_limit_symbol = 5
    benchmark_case.benchmark_etfs = [AppConsts.BENCHMARK_ETF_SPY]
    invalid_benchmark_case: BackTestRunRequest = BackTestRunRequest()
    invalid_benchmark_case.test_limit_symbol = 5
    invalid_benchmark_case.benchmark_etfs = ['fake_etf']

    # ACT
    ret_no_benchmark_case: List[SymbolMaster] = self.__back_test_service.__get_symbols__(no_benchmark_case)
    ret_benchmark_case: List[SymbolMaster] = self.__back_test_service.__get_symbols__(benchmark_case)
    ret_invalid_benchmark_case: List[SymbolMaster] = self.__back_test_service.__get_symbols__(invalid_benchmark_case)

    # ASSERT
    self.assertRaises(BadRequestException, self.__back_test_service.__get_symbols__, none_case)
    self.assertRaises(BadRequestException, self.__back_test_service.__get_symbols__, no_test_limit_symbol_case)
    self.assertIsNotNone(ret_no_benchmark_case)
    self.assertEqual(5, len(ret_no_benchmark_case))
    self.assertEqual(6, len(ret_benchmark_case))
    self.assertEqual(5, len(ret_invalid_benchmark_case))

  def test_get_prices_should_return_appropriately(self) -> None:
    # ARRANGE
    none_case = None
    req: BackTestRunRequest = BackTestRunRequest()
    req.date_from = '2000-01-01'
    req.date_to = '2000-01-10'
    symbol: SymbolMaster = SymbolMaster()
    symbol.id = 519  # MSFT
    symbol.instrument = AppConsts.INSTRUMENT_STOCK
    symbols: List[SymbolMaster] = [symbol]
    symbol_etf: SymbolMaster = SymbolMaster()
    symbol_etf.instrument = AppConsts.INSTRUMENT_ETF
    symbol_etf.id = 810  # SPY
    symbols_with_benchmark: List[SymbolMaster] = [symbol, symbol_etf]

    # ACT
    ret_no_benchmark_case: DataFrame = self.__back_test_service.__get_prices__(req, symbols)
    ret_with_benchmark_case: DataFrame = self.__back_test_service.__get_prices__(req, symbols_with_benchmark)

    # ASSERT
    self.assertRaises(BadRequestException, self.__back_test_service.__get_prices__, none_case, symbols)
    self.assertRaises(BadRequestException, self.__back_test_service.__get_prices__, req, none_case)
    self.assertIsNotNone(ret_no_benchmark_case)
    self.assertIsNotNone(ret_no_benchmark_case.shape)
    self.assertEqual(6, ret_no_benchmark_case.shape[0])
    self.assertEqual(6, ret_no_benchmark_case.shape[1])
    self.assertTrue(AppConsts.PRICE_COL_SYMBOL_ID in ret_no_benchmark_case.index.names)
    self.assertTrue(AppConsts.PRICE_COL_DATE in ret_no_benchmark_case.index.names)
    self.assertEqual(symbol.id, ret_no_benchmark_case.index.values[0][0])
    self.assertEqual(date(2000, 1, 3), ret_no_benchmark_case.index.values[0][1])
    self.assertEqual(date(2000, 1, 10), ret_no_benchmark_case.index.values[-1][1])
    self.assertEqual(37.37, ret_no_benchmark_case[AppConsts.PRICE_COL_CLOSE].loc[symbol.id, date(2000, 1, 3)])
    self.assertEqual(36.01, ret_no_benchmark_case[AppConsts.PRICE_COL_CLOSE].loc[symbol.id, date(2000, 1, 10)])
    self.assertIsNotNone(ret_with_benchmark_case)
    self.assertIsNotNone(ret_with_benchmark_case.shape)
    self.assertEqual(12, ret_with_benchmark_case.shape[0])
    self.assertEqual(6, ret_with_benchmark_case.shape[1])
    self.assertEqual(symbol_etf.id, ret_with_benchmark_case.index.values[-1][0])

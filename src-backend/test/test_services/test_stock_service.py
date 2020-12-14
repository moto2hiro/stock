import random
import pandas as pd
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from datetime import date
from typing import List, Any
from test.test_base import TestBase
from app_consts import AppConsts
from models.db.symbol_master import SymbolMaster
from models.db.stock_price_daily import StockPriceDaily
from services.stock_service import StockService
from services.calc_service import CalcService


class TestStockService(TestBase):

  def __init__(self, *args, **kwargs):
    super(TestStockService, self).__init__(*args, **kwargs)
    self.__stock_service: StockService = StockService()
    self.__calc_service: CalcService = CalcService()

  def __get_test_dataframe__(self) -> DataFrame:
    symbols: List[int] = [1, 2, 3, 4]
    prices: DataFrame = pd.DataFrame(
        data=[
            [1, 1, date(2000, 1, 1), 50, 100, 100000],
            [2, 1, date(2000, 1, 2), 150, 200, 200000],
            [3, 1, date(2000, 1, 3), 250, 300, 300000],
            [4, 2, date(2000, 1, 1), 650, 700, 700000],
            [5, 2, date(2000, 1, 2), 750, 800, 800000],
            [6, 2, date(2000, 1, 3), 850, 900, 900000],
            [7, 3, date(2000, 1, 2), 650, 700, 700000],
            [8, 3, date(2000, 1, 3), 750, 800, 800000],
            [9, 3, date(2000, 1, 4), 850, 900, 900000],
            [10, 4, date(2000, 1, 3), 750, 800, 800000],
            [11, 4, date(2000, 1, 4), 850, 900, 900000],
            [12, 4, date(2000, 1, 5), 850, 900, 900000],
            [13, 4, date(2000, 1, 6), 650, 700, 700000],
        ],
        columns=[
            AppConsts.COL_ID,
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

  def test_get_vw_symbol_spd_as_df(self) -> None:
    # ARRANGE
    symbol_id: int = 519  # MSFT
    symbol_ids: List = random.sample(range(800), 10)

    # ACT
    ret_by_symbol_id = self.__stock_service.get_vw_symbol_spd_as_df(symbol_id)
    ret_by_symbol_ids = self.__stock_service.get_vw_symbol_spd_as_df(symbol_ids=symbol_ids)

    # ASSERT
    self.assertIsNotNone(ret_by_symbol_id)
    self.assertIsNotNone(ret_by_symbol_ids)
    self.assertTrue(AppConsts.PRICE_COL_SYMBOL_ID in ret_by_symbol_id.index.names)
    self.assertTrue(AppConsts.PRICE_COL_DATE in ret_by_symbol_id.index.names)

  def test_get_vw_symbol_epd_as_df(self) -> None:
    # ARRANGE
    symbol_id: int = 810  # SPY

    # ACT
    ret = self.__stock_service.get_vw_symbol_epd_as_df(symbol_id)

    # ASSERT
    self.assertIsNotNone(ret)
    self.assertTrue(AppConsts.PRICE_COL_SYMBOL_ID in ret.index.names)
    self.assertTrue(AppConsts.PRICE_COL_DATE in ret.index.names)

  def test_get_price_dataframe_should_return_appropriately(self) -> None:
    # ARRANGE
    none_case: List[Any] = None
    empty_case: List[Any] = []
    wrong_type_case: Dict = {'foo': 'bar'}
    wrong_content_case: List[Dict] = [{'foo': 'bar'}]
    spd: StockPriceDaily = StockPriceDaily()
    valid_case: List[StockPriceDaily] = [spd]

    # ACT
    ret_none_case: DataFrame = self.__stock_service.get_price_dataframe(none_case)
    ret_empty_case: DataFrame = self.__stock_service.get_price_dataframe(empty_case)
    ret_wrong_type_case: DataFrame = self.__stock_service.get_price_dataframe(wrong_type_case)
    ret_wrong_content_case: DataFrame = self.__stock_service.get_price_dataframe(wrong_content_case)
    ret_valid_case: DataFrame = self.__stock_service.get_price_dataframe(valid_case)

    # ASSERT
    self.assertIsNone(ret_none_case)
    self.assertIsNone(ret_wrong_type_case)
    self.assertIsNone(ret_empty_case)
    self.assertIsNone(ret_wrong_content_case)
    self.assertIsNotNone(ret_valid_case)
    self.assertTrue(AppConsts.PRICE_COL_SYMBOL_ID in ret_valid_case.index.names)
    self.assertTrue(AppConsts.PRICE_COL_DATE in ret_valid_case.index.names)

  def test_get_strategy_service_should_return_appropriately(self) -> None:
    # ACT
    ret_none_case: Any = self.__stock_service.get_strategy_service(None, None, None, None)
    ret_invalid_case: Any = self.__stock_service.get_strategy_service('invalid', None, None, None)
    ret_demo_case: Any = self.__stock_service.get_strategy_service(AppConsts.STRATEGY_DEMO, None, None, None)
    ret_abz_case: Any = self.__stock_service.get_strategy_service(AppConsts.STRATEGY_ABZ, None, None, None)
    ret_dbb_case: Any = self.__stock_service.get_strategy_service(AppConsts.STRATEGY_DBB, None, None, None)
    ret_double_bottoms_case: Any = self.__stock_service.get_strategy_service(AppConsts.STRATEGY_DOUBLE_BOTTOMS, None, None, None)
    ret_double_tops_case: Any = self.__stock_service.get_strategy_service(AppConsts.STRATEGY_DOUBLE_TOPS, None, None, None)
    ret_sma_crossover_case: Any = self.__stock_service.get_strategy_service(AppConsts.STRATEGY_SMA_CROSSOVER, None, None, None)
    ret_inverted_head_and_shoulders_case: Any = self.__stock_service.get_strategy_service(AppConsts.STRATEGY_INVERTED_HEAD_AND_SHOULDERS, None, None, None)
    ret_turnaround_tuesday_case: Any = self.__stock_service.get_strategy_service(AppConsts.STRATEGY_TURNAROUND_TUESDAY, None, None, None)

    # ASSERT
    self.assertIsNone(ret_none_case)
    self.assertIsNone(ret_invalid_case)
    self.assertIsNotNone(ret_demo_case)
    self.assertIsNotNone(ret_abz_case)
    self.assertIsNotNone(ret_dbb_case)
    self.assertIsNotNone(ret_double_bottoms_case)
    self.assertIsNotNone(ret_double_tops_case)
    self.assertIsNotNone(ret_sma_crossover_case)
    self.assertIsNotNone(ret_turnaround_tuesday_case)
    self.assertEqual('DemoStrategyService', ret_demo_case.__class__.__name__)
    self.assertEqual('AbzStrategyService', ret_abz_case.__class__.__name__)
    self.assertEqual('DoubleBollingerBandsStrategyService', ret_dbb_case.__class__.__name__)
    self.assertEqual('DoubleBottomsStrategyService', ret_double_bottoms_case.__class__.__name__)
    self.assertEqual('DoubleTopsStrategyService', ret_double_tops_case.__class__.__name__)
    self.assertEqual('SmaCrossoverStrategyService', ret_sma_crossover_case.__class__.__name__)
    self.assertEqual('InvertedHeadAndShouldersStrategyService', ret_inverted_head_and_shoulders_case.__class__.__name__)
    self.assertEqual('TurnaroundTuesdayStrategyService', ret_turnaround_tuesday_case.__class__.__name__)

  def test_get_dates_should_return_appropriately(self) -> None:
    # ARRANGE
    prices: DataFrame = self.__get_test_dataframe__()
    start_date: date = pd.to_datetime('1999-12-31')
    end_date: date = pd.to_datetime('2000-01-06')

    # ACT
    ret_valid_case: DataFrame = self.__stock_service.get_dates(prices, start_date, end_date)

    # ASSERT
    self.assertIsNotNone(ret_valid_case)
    self.assertIsNotNone(ret_valid_case.shape)
    self.assertEqual(6, ret_valid_case.shape[0])
    self.assertEqual(4, ret_valid_case.shape[1])
    self.assertTrue(ret_valid_case[AppConsts.PRICE_COL_DATE][1] > ret_valid_case[AppConsts.CUSTOM_COL_PREV_DATE][1])
    self.assertTrue(ret_valid_case[AppConsts.PRICE_COL_DATE][1] < ret_valid_case[AppConsts.CUSTOM_COL_NEXT_DATE][1])
    self.assertTrue(ret_valid_case[AppConsts.PRICE_COL_DATE][1] < ret_valid_case[AppConsts.CUSTOM_COL_NEXT_NEXT_DATE][1])
    self.assertTrue(ret_valid_case[AppConsts.CUSTOM_COL_NEXT_DATE][1] < ret_valid_case[AppConsts.CUSTOM_COL_NEXT_NEXT_DATE][1])

  def test_get_no_of_shares_should_return_appropriately(self) -> None:
    # ARRANGE
    price: Series = self.__get_test_series__()

    # ACT
    ret_no_of_shares: int = self.__stock_service.get_no_of_shares(
        capital=10000,
        pct_risk_per_trade=10,
        volume_limit=0.01,
        price=price,
        slippage=10)

    # ASSERT
    # open_price = 50
    # slippage_price = 50.05 = 50 + (50 * 0.0001 * 10)
    # no_of_shares = 19 = 10000 * 10 / 100 / slippage_price
    # max_volume = 10 = 100000 * 0.01 / 100
    self.assertNotEqual(0, ret_no_of_shares)
    self.assertEqual(10, ret_no_of_shares)

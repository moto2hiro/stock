import pandas as pd
from typing import List
from pandas.core.frame import DataFrame
from app_consts import AppConsts
from test.test_base import TestBase
from services.calc_service import CalcService


class TestCalcService(TestBase):

  def __init__(self, *args, **kwargs):
    super(TestCalcService, self).__init__(*args, **kwargs)
    self.__calc_service: CalcService = CalcService()

  def __get_test_dataframe(self) -> DataFrame:
    prices: DataFrame = pd.DataFrame(
        data=[
            [1, '2000-01', 1],
            [1, '2000-02', 2],
            [1, '2000-03', 3],
            [2, '2000-01', 7],
            [2, '2000-02', 8],
            [2, '2000-03', 9],
        ],
        columns=[AppConsts.PRICE_COL_SYMBOL_ID, AppConsts.PRICE_COL_DATE, AppConsts.PRICE_COL_CLOSE])
    prices = prices.set_index([AppConsts.PRICE_COL_SYMBOL_ID, AppConsts.PRICE_COL_DATE])
    return prices

  def test_append_exponential_smoothing_price_should_return_appropriately(self) -> None:
    # ARRANGE
    prices: DataFrame = self.__get_test_dataframe()
    index: List = [1]
    alpha: float = 0.5

    none_case: DataFrame = None
    wrong_type_case: List[Dict] = [{'foo': 'bar'}]
    alpha_negative_case: float = -1
    alpha_large_case: float = 10

    # ACT
    ret_none_case: DataFrame = self.__calc_service.append_exponential_smoothing_price(none_case, index, alpha)
    ret_wrong_type_case: DataFrame = self.__calc_service.append_exponential_smoothing_price(wrong_type_case, index, alpha)
    ret_alpha_negative_case: DataFrame = self.__calc_service.append_exponential_smoothing_price(prices, index, alpha_negative_case)
    ret_alpha_large_case: DataFrame = self.__calc_service.append_exponential_smoothing_price(prices, index, alpha_large_case)
    ret_valid_case: DataFrame = self.__calc_service.append_exponential_smoothing_price(prices, index, alpha)

    # ASSERT
    self.assertIsNone(ret_none_case)
    self.assertIsNone(ret_wrong_type_case)
    self.assertIsNone(ret_alpha_negative_case)
    self.assertIsNone(ret_alpha_large_case)
    self.assertIsNotNone(ret_valid_case)

  def test_append_exponential_smoothing_max_min_should_return_appropriately(self) -> None:
    # ARRANGE
    prices: DataFrame = self.__get_test_dataframe()
    index: List = [1]
    alpha: float = 0.5
    exponential_smoothing_max_min_diff: float = 0.7

    none_case: DataFrame = None
    valid_prices: DataFrame = self.__calc_service.append_exponential_smoothing_price(prices, index, alpha)

    # ACT
    ret_none_case: DataFrame = self.__calc_service.append_exponential_smoothing_max_min(none_case, index, exponential_smoothing_max_min_diff)
    ret_valid_case: DataFrame = self.__calc_service.append_exponential_smoothing_max_min(valid_prices, index, exponential_smoothing_max_min_diff)

    # ASSERT
    self.assertIsNone(ret_none_case)
    self.assertIsNotNone(ret_valid_case)

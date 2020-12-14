from typing import Any
from test.test_base import TestBase
from app_consts import AppConsts
from clients.iex_cloud_client import IexCloudClient
from models.db.symbol_master import SymbolMaster
from services.stock_service import StockService


class TestIexCloudClient(TestBase):

  def __init__(self, *args, **kwargs):
    super(TestIexCloudClient, self).__init__(*args, **kwargs)
    self.__iex_cloud_client: IexCloudClient = IexCloudClient()
    self.__stock_service: StockService = StockService()

  def test_get_company_profiles_should_return_appropriately(self) -> None:
    # ARRANGE
    symbol_msft: str = 'MSFT'
    symbol_aapl: str = 'AAPL'
    symbols: List[str] = [symbol_msft, symbol_aapl]

    # ACT
    ret: List[Dict] = self.__iex_cloud_client.get_company_profiles(symbols)

    # ASSERT
    self.assertIsNotNone(ret)
    self.assertEqual(len(symbols), len(ret))

  def test_get_key_stats_should_return_appropriately(self) -> None:
    # ARRANGE
    symbol_msft: str = 'MSFT'

    # ACT
    ret: Any = self.__iex_cloud_client.get_key_stats(symbol_msft)

    # ASSERT
    self.assertIsNotNone(ret)

  def test_get_news_should_return_appropriately(self) -> None:
    # ARRANGE
    symbol_msft: str = 'MSFT'

    # ACT
    ret: Any = self.__iex_cloud_client.get_news(symbol_msft)

    # ASSERT
    self.assertIsNotNone(ret)

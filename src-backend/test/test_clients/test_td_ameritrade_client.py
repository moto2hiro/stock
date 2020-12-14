from typing import Any
from test.test_base import TestBase
from clients.td_ameritrade_client import TdAmeritradeClient
from models.db.symbol_master import SymbolMaster


class TestTdAmeritradeClient(TestBase):

  def __init__(self, *args, **kwargs):
    super(TestTdAmeritradeClient, self).__init__(*args, **kwargs)
    self.__td_ameritrade_client: TdAmeritradeClient = TdAmeritradeClient()

  def test_get_key_stats_should_return_appropriately(self) -> None:
    # ARRANGE
    symbol_msft: str = 'MSFT'

    # ACT
    ret: Any = self.__td_ameritrade_client.get_key_stats(symbol_msft)

    # ASSERT
    self.assertIsNotNone(ret)

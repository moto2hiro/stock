from datetime import date
from pandas._libs.tslibs.timestamps import Timestamp
from alpaca_trade_api.entity import Account, BarSet, Bars, Bar, Order, Position
from test.test_base import TestBase
from app_consts import AppConsts
from clients.alpaca_client import AlpacaClient
from models.db.symbol_master import SymbolMaster
from models.db.trade_order import TradeOrder
from models.trade_order_custom import TradeOrderCustom
from services.stock_service import StockService


class TestAlpacaClient(TestBase):

  def __init__(self, *args, **kwargs):
    super(TestAlpacaClient, self).__init__(*args, **kwargs)
    self.__alpaca_client: AlpacaClient = AlpacaClient()
    self.__stock_service: StockService = StockService()

  def test_get_prices_should_return_appropriately(self) -> None:
    # ARRANGE
    symbol_msft: str = 'MSFT'
    symbol_aapl: str = 'AAPL'
    symbols: List[str] = [symbol_msft, symbol_aapl]
    limit: int = 5

    # ACT
    prices: BarSet = self.__alpaca_client.get_prices(symbols, limit)

    # ASSERT
    self.assertIsNotNone(prices)
    self.assertIsNotNone(prices[symbol_msft])
    self.assertIsNotNone(prices[symbol_aapl])
    self.assertEqual(limit, len(prices[symbol_msft]))
    self.assertEqual(limit, len(prices[symbol_aapl]))
    self.assertTrue(prices[symbol_msft][0].o > 0)
    self.assertTrue(prices[symbol_msft][0].h > 0)
    self.assertTrue(prices[symbol_msft][0].l > 0)
    self.assertTrue(prices[symbol_msft][0].c > 0)
    self.assertTrue(prices[symbol_msft][0].v > 0)
    self.assertIsNotNone(prices[symbol_msft][0].t)
    self.assertTrue(isinstance(prices[symbol_msft][0].t, Timestamp))

  def test_get_account_should_return_appropriately(self) -> None:
    # ACT
    ret: Account = self.__alpaca_client.get_account()

    # ASSERT
    self.assertIsNotNone(ret)

  def test_get_orders_should_return_appropriately(self) -> None:
    # ACT
    ret: List[Order] = self.__alpaca_client.get_orders()

    # ASSERT
    pass

  def test_submit_order_should_return_appropriately(self) -> None:
    # ARRANGE
    order: TradeOrderCustom = TradeOrderCustom(None)
    order.symbol_master = SymbolMaster()
    order.symbol_master.symbol = 'MSFT'
    order.trade_order = TradeOrder()
    order.trade_order.qty = 10
    order.trade_order.action = AppConsts.ACTION_BUY
    order.trade_order.order_type = AppConsts.ORDER_TYPE_MARKET
    order.trade_order.time_in_force = AppConsts.TIME_IN_FORCE_DAY

    # ACT
    # WARNING!!!!! DO NOT UNCOMMENT
    # ret = self.__alpaca_client.submit_order(order)
    # accnt: Account = self.__alpaca_client.get_account()
    # WARNING!!!!! DO NOT UNCOMMENT

    # ASSERT
    pass

  def test_cancel_order_should_return_appropriately(self) -> None:
    # ARRANGE
    order_id: str = '98bd950a-3e52-4a83-950b-e4bf42ef2e24'

    # ACT
    # WARNING!!!!! DO NOT UNCOMMENT
    # self.__alpaca_client.cancel_order(order_id)
    # WARNING!!!!! DO NOT UNCOMMENT

    # ASSERT
    pass

  def test_get_positions_should_return_appropriately(self) -> None:
    # ACT
    ret: List[Position] = self.__alpaca_client.get_positions()

    # ASSERT
    pass

  def test_is_tmrw_valid(self) -> None:
    # ACT
    ret: bool = self.__alpaca_client.is_tmrw_valid()

    # ASSERT
    pass

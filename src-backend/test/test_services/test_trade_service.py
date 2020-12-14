from datetime import date
from typing import List
from test.test_base import TestBase
from app_utils.string_utils import StringUtils
from models.request_models.get_trade_orders_request import GetTradeOrdersRequest
from models.response_models.key_info_response import KeyInfoResponse
from models.trade_order_custom import TradeOrderCustom
from services.trade_service import TradeService


class TestTradeService(TestBase):

  def __init__(self, *args, **kwargs):
    super(TestTradeService, self).__init__(*args, **kwargs)
    self.__trade_service: TradeService = TradeService()

  def test_get_key_info(self) -> None:
    # ARRANGE
    symbol: str = 'MSFT'

    # ACT
    ret: KeyInfoResponse = self.__trade_service.get_key_info(symbol)

    # ASSERT
    self.assertIsNotNone(ret)

  def test_get_trade_orders(self) -> None:
    # ARRANGE
    req: GetTradeOrdersRequest = GetTradeOrdersRequest()
    req.created: date = date(2020, 7, 28)

    # ACT
    ret: List[TradeOrderCustom] = self.__trade_service.get_trade_orders(req)

    # ASSERT
    pass

  def test_get_trade_order(self) -> None:
    # ARRANGE
    trade_order_id: int = 0

    # ACT
    ret = self.__trade_service.get_trade_order(trade_order_id)

    # ASSERT
    pass

  def test_close_positions(self) -> None:
    # ARRANGE

    # ACT
    # WARNING!!!!! DO NOT UNCOMMENT
    # self.__trade_service.close_positions()
    # WARNING!!!!! DO NOT UNCOMMENT

    # ASSERT
    pass

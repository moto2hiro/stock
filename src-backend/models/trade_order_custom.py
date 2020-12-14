from models.db.trade_order import TradeOrder
from models.db.stock_price_daily import StockPriceDaily
from models.db.symbol_master import SymbolMaster
from models.response_models.base_response import BaseResponse


class TradeOrderCustom(BaseResponse):

  def __init__(self, item: tuple) -> None:
    super().__init__()
    if item:
      self._trade_order = item[0]
      self._stock_price_daily = item[1]
      self._symbol_master = item[2]

  @property
  def trade_order(self) -> TradeOrder: return self._trade_order

  @trade_order.setter
  def trade_order(self, val: TradeOrder) -> None: self._trade_order = val

  @property
  def stock_price_daily(self) -> StockPriceDaily: return self._stock_price_daily

  @stock_price_daily.setter
  def stock_price_daily(self, val: StockPriceDaily) -> None: self._stock_price_daily = val

  @property
  def symbol_master(self) -> SymbolMaster: return self._symbol_master

  @symbol_master.setter
  def symbol_master(self, val: SymbolMaster) -> None: self._symbol_master = val

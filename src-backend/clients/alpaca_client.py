import alpaca_trade_api as tradeapi
from datetime import date, timedelta
from alpaca_trade_api.entity import Account, BarSet, Order, Position, Calendar
from typing import List
from app_config import app_config
from app_consts import AppConsts
from app_utils.date_utils import DateUtils
from app_utils.log_utils import LogUtils
from app_utils.string_utils import StringUtils
from models.trade_order_custom import TradeOrderCustom


class AlpacaClient:
  def __init__(self) -> None:
    self.__api = tradeapi.REST(
        key_id=app_config.APCA_API_KEY_ID,
        secret_key=app_config.APCA_API_SECRET_KEY,
        base_url=app_config.APCA_API_BASE_URL)

  def get_prices(self, symbols: List[str], limit: int) -> BarSet:
    """
    Max symbols: 200
    Max limit: 1000 (default = 100)
    https://alpaca.markets/docs/api-documentation/api-v2/market-data/bars/
    https://alpaca.markets/docs/api-documentation/how-to/market-data/
    """
    if not symbols:
      return None
    batch_size: int = 200
    ret: BarSet = {}
    for i in range(0, len(symbols), batch_size):
      batch: List[str] = symbols[i:i + batch_size]
      tmp: BarSet = self.__api.get_barset(batch, 'day', limit=limit)
      ret = {**ret, **tmp}
    return ret

  def get_account(self) -> Account:
    ret: Account = self.__api.get_account()
    LogUtils.debug('Account = {0}'.format(ret))
    return ret

  def get_orders(self) -> List[Order]:
    ret: List[Order] = self.__api.list_orders()
    LogUtils.debug('Orders = {0}'.format(ret))
    return ret

  def get_order(self, alpaca_id: str) -> Order:
    ret: Order = self.__api.get_order(alpaca_id)
    LogUtils.debug('Order = {0}'.format(ret))
    return ret

  def submit_order(
          self,
          symbol: str,
          qty: int,
          action: str,
          order_type: str = AppConsts.ORDER_TYPE_MARKET,
          time_in_force: str = AppConsts.TIME_IN_FORCE_DAY) -> Order:
    ret: Order = None
    try:

      ret = self.__api.submit_order(
          symbol=symbol,
          qty=qty,
          side=action,
          type=order_type,
          time_in_force=time_in_force
      )

      LogUtils.debug('Submit response = {0}'.format(ret))

    except Exception as ex:
      LogUtils.error('Submit Error for {0}'.format(symbol), ex)
      raise ex
    return ret

  def cancel_order(self, order_id: str) -> None:
    try:

      LogUtils.debug('Submit request = {0}'.format(order_id))

      self.__api.cancel_order(order_id)

    except Exception as ex:
      LogUtils.error('Submit Error for {0}'.format(StringUtils.to_json(order)), ex)
      raise ex

  def get_positions(self) -> List[Position]:
    ret: List[Position] = self.__api.list_positions()
    LogUtils.debug('Positions = {0}'.format(ret))
    return ret

  def close_position(self, symbol: str) -> Order:
    ret: Order = None
    try:
      LogUtils.debug('Close Position for = {0}'.format(symbol))

      ret = self.__api.close_position(symbol)

      LogUtils.debug('Close Position response = {0}'.format(ret))

    except Exception as ex:
      LogUtils.error('Close Position Error for {0}'.format(symbol), ex)
      raise ex
    return ret

  def is_tmrw_valid(self) -> bool:
    tmrw = date.today() + timedelta(days=1)
    tmrw_as_string: str = DateUtils.to_string(tmrw)
    calendars: List[Calendar] = self.__api.get_calendar(tmrw_as_string, tmrw_as_string)
    LogUtils.debug(calendars)
    return (calendars[0].date.to_pydatetime().date() == tmrw)

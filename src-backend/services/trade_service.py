import pandas as pd
from sqlalchemy import cast, Date, or_
from datetime import date, datetime, timedelta
from random import shuffle
from typing import List, Any, Dict
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from alpaca_trade_api.entity import Account, Order
from app_db import db
from app_consts import AppConsts
from app_utils.log_utils import LogUtils
from app_utils.date_utils import DateUtils
from app_utils.model_utils import ModelUtils
from app_utils.number_utils import NumberUtils
from app_utils.string_utils import StringUtils
from clients.alpaca_client import AlpacaClient
from clients.iex_cloud_client import IexCloudClient
from clients.td_ameritrade_client import TdAmeritradeClient
from clients.email_client import EmailClient
from exceptions.bad_request_exception import BadRequestException
from exceptions.db_connection_exception import DbConnectionException
from exceptions.not_found_exception import NotFoundException
from models.db.stock_price_daily import StockPriceDaily
from models.db.symbol_master import SymbolMaster
from models.db.trade_order import TradeOrder
from models.request_models.get_trade_orders_request import GetTradeOrdersRequest
from models.request_models.trade_suggestions_request import TradeSuggestionsRequest
from models.response_models.key_info_response import KeyInfoResponse
from models.trade_order_custom import TradeOrderCustom
from services.base_service import BaseService
from services.stock_service import StockService
from services.calc_service import CalcService


class TradeService(BaseService):
  def __init__(self) -> None:
    super().__init__()
    self.__alpaca_client: AlpacaClient = AlpacaClient()
    self.__iex_cloud_client: IexCloudClient = IexCloudClient()
    self.__td_ameritrade_client: TdAmeritradeClient = TdAmeritradeClient()
    self.__email_client: EmailClient = EmailClient()
    self.__stock_service: StockService = StockService()
    self.__calc_service: CalcService = CalcService()

  def get_account(self) -> Account:
    return self.__alpaca_client.get_account()

  def get_key_info(self, symbol: str) -> KeyInfoResponse:
    ret: KeyInfoResponse = KeyInfoResponse()
    ret.iex_cloud_key_stats: Any = self.__iex_cloud_client.get_key_stats(symbol)
    ret.news['iex_cloud'] = self.__iex_cloud_client.get_news(symbol)
    ret.td_ameritrade_key_stats: Any = self.__td_ameritrade_client.get_key_stats(symbol)
    return ret

  def get_trade_order(self, trade_order_id: int) -> TradeOrderCustom:
    return TradeOrderCustom(db.session.query(
        TradeOrder, StockPriceDaily, SymbolMaster,
    ).filter(
        TradeOrder.stock_price_daily_id == StockPriceDaily.id,
    ).filter(
        StockPriceDaily.symbol_id == SymbolMaster.id,
    ).filter(
        TradeOrder.id == trade_order_id,
    ).first())

  def get_trade_orders(self, req: GetTradeOrdersRequest) -> List[TradeOrderCustom]:
    if not req:
      return []
    query = db.session.query(
        TradeOrder, StockPriceDaily, SymbolMaster,
    ).filter(
        TradeOrder.stock_price_daily_id == StockPriceDaily.id,
    ).filter(
        StockPriceDaily.symbol_id == SymbolMaster.id,
    )
    if req.status:
      query = query.filter(or_(*[TradeOrder.status.op('|')(s) == TradeOrder.status for s in req.status]))
    if req.exact_status:
      query = query.filter(req.exact_status == TradeOrder.status)
    if req.created_obj:
      query = query.filter(req.created_obj == cast(TradeOrder.created, Date))
    query = query.order_by(SymbolMaster.symbol)
    items: List[Any] = query.all()
    return [] if not items else [TradeOrderCustom(i) for i in items]

  def get_all_suggestions(self) -> int:
    error: Exception = None
    try:

      accnt: Account = self.get_account()
      capital: float = NumberUtils.to_floor(NumberUtils.to_float(accnt._raw['buying_power']) / 2)  # 2 to trade everyday

      # Double Bottoms
      req: TradeSuggestionsRequest = TradeSuggestionsRequest()
      req.is_job = True
      req.current_capital = capital
      req.pct_risk_per_trade = 2.5
      req.volume_limit = 0.01
      req.test_limit_symbol = 800
      req.adv_min = AppConsts.ADV_MIN_DFLT
      req.adpv_min = AppConsts.ADPV_MIN_DFLT
      req.strategy_type = AppConsts.STRATEGY_DOUBLE_BOTTOMS
      req.strategy_request = {}
      req.strategy_request['exponential_smoothing_alpha'] = 0.8
      req.strategy_request['exponential_smoothing_max_min_diff'] = 0.7
      req.strategy_request['double_bottoms_diff'] = 1
      LogUtils.debug(StringUtils.to_json(req))
      self.get_suggestions(req)

      # Double Tops
      req: TradeSuggestionsRequest = TradeSuggestionsRequest()
      req.is_job = True
      req.current_capital = capital
      req.pct_risk_per_trade = 2.5
      req.volume_limit = 0.01
      req.test_limit_symbol = 800
      req.adv_min = AppConsts.ADV_MIN_DFLT
      req.adpv_min = AppConsts.ADPV_MIN_DFLT
      req.strategy_type = AppConsts.STRATEGY_DOUBLE_TOPS
      req.strategy_request = {}
      req.strategy_request['exponential_smoothing_alpha'] = 0.8
      req.strategy_request['exponential_smoothing_max_min_diff'] = 0.7
      req.strategy_request['double_tops_diff'] = 1
      LogUtils.debug(StringUtils.to_json(req))
      self.get_suggestions(req)

    except Exception as ex:
      error = ex
    finally:
      self.__email_client.send_html(
          subject=AppConsts.EMAIL_SUBJECT_GET_SUGGESTIONS,
          template_path=AppConsts.TEMPLATE_PATH_GET_SUGGESTIONS,
          model={'errors': [error] if error else []})
      if error:
        LogUtils.error('Get Suggestions Error', error)
      return 1

  def get_suggestions(self, req: TradeSuggestionsRequest) -> List[TradeOrder]:
    if not req or not req.is_valid_model():
      raise BadRequestException()
    response: List[TradeOrder] = []

    # Init Symbols
    symbols: List[SymbolMaster] = self.__get_symbols__(req)

    # Init Prices
    date_to: date = date.today()
    date_from: date = date_to - timedelta(days=100)  # fix this
    prices: DataFrame = self.__get_prices__(symbols, date_from, date_to)

    # Do Base Preparation
    prices[AppConsts.CUSTOM_COL_PV] = prices[AppConsts.PRICE_COL_CLOSE] * prices[AppConsts.PRICE_COL_VOLUME]
    for s in symbols:
      prices = self.__calc_service.append_sma(
          prices=prices,
          index=[s.id],
          sma_period=AppConsts.ADV_PERIOD_DFLT,
          sma_column_name=AppConsts.CUSTOM_COL_ADV,
          target_column=AppConsts.PRICE_COL_VOLUME)
      prices = self.__calc_service.append_sma(
          prices=prices,
          index=[s.id],
          sma_period=AppConsts.ADPV_PERIOD_DFLT,
          sma_column_name=AppConsts.CUSTOM_COL_ADPV,
          target_column=AppConsts.CUSTOM_COL_PV)

    LogUtils.debug('Prices shape after base preparation={0}'.format(prices.shape))

    # region Init Service
    strategy_service: Any = self.__stock_service.get_strategy_service(req.strategy_type, req.strategy_request, symbols, prices)
    if not strategy_service or not strategy_service._is_valid_request():
      raise BadRequestException()
    strategy_service._do_preparations()

    LogUtils.debug('Prices shape after strategy preparation={0}'.format(prices.shape))
    # endregion

    LogUtils.debug(prices.info())

    # region Init Dates
    end_date: date = prices.index.get_level_values(AppConsts.PRICE_COL_DATE).max()
    LogUtils.debug('End_date={0}'.format(end_date))

    for symbol in symbols:
      LogUtils.debug('Start {0}'.format(symbol.symbol))

      has_price: bool = (symbol.id, end_date) in prices.index
      if not has_price:
        continue
      price: Series = prices.loc[symbol.id, end_date]

      adv: float = price.loc[AppConsts.CUSTOM_COL_ADV] if price.loc[AppConsts.CUSTOM_COL_ADV] > 0 else price.loc[AppConsts.PRICE_COL_VOLUME]
      if adv < req.adv_min:
        continue
      adpv: float = price.loc[AppConsts.CUSTOM_COL_ADPV] if price.loc[AppConsts.CUSTOM_COL_ADPV] > 0 else price.loc[AppConsts.CUSTOM_COL_PV]
      if adpv < req.adpv_min:
        continue

      has_entry_conditions: bool = strategy_service._has_entry_conditions(symbol.id, end_date)
      if not has_entry_conditions:
        continue
      no_of_shares: int = self.__stock_service.get_no_of_shares(
          req.current_capital,
          req.pct_risk_per_trade,
          req.volume_limit,
          price)
      if no_of_shares == 0:
        continue
      LogUtils.debug('Has Entry Condition = {0}'.format(symbol.symbol))

      now: datetime = datetime.now()
      order: TradeOrder = TradeOrder()
      order.stock_price_daily_id = price.loc[AppConsts.COL_ID]
      order.strategy = req.strategy_type
      order.status = AppConsts.ORDER_STATUS_INIT

      order.action = strategy_service._get_action()

      order.qty = no_of_shares
      # order.target_price = price.loc[AppConsts.CUSTOM_COL_DOUBLE_BOTTOMS_TARGET_PRICE]
      # order.stop_loss = price.loc[AppConsts.CUSTOM_COL_DOUBLE_BOTTOMS_STOP_LOSS]
      order.created = now
      order.modified = now
      response.append(order)
      if req.is_job:
        org: TradeOrder = BaseService._get_first(TradeOrder, [
            TradeOrder.stock_price_daily_id == order.stock_price_daily_id,
            TradeOrder.strategy == order.strategy])
        if not org:
          BaseService._insert(order)

    return response

  def __get_symbols__(self, req: TradeSuggestionsRequest) -> List[SymbolMaster]:
    if not req or req.test_limit_symbol <= 0:
      raise BadRequestException()
    symbols: List[SymbolMaster] = self.__stock_service.get_symbols(AppConsts.INSTRUMENT_STOCK, [AppConsts.SYMBOL_STATUS_EXCLUDE_TRADE, AppConsts.SYMBOL_STATUS_ARCHIVED])
    if not symbols:
      raise DbConnectionException()
    shuffle(symbols)
    symbols = symbols[:req.test_limit_symbol]
    LogUtils.debug('Symbol Count={0}'.format(len(symbols)))
    return symbols

  def __get_prices__(self, symbols: List[SymbolMaster], date_from: date, date_to: date) -> DataFrame:
    if not symbols:
      raise BadRequestException()
    price_items: List[Any] = []
    for symbol in symbols:
      temp: List[StockPriceDaily] = self.__stock_service.get_stock_prices_daily(symbol.id, date_from, date_to)
      if temp:
        price_items.extend(temp)
    prices: DataFrame = self.__stock_service.get_price_dataframe(price_items)
    LogUtils.debug('Prices Init Shape={0}'.format(prices.shape))
    return prices

  def queue_positions(self) -> int:
    errors: List[Exception] = []
    try:
      is_tmrw_valid: bool = self.__alpaca_client.is_tmrw_valid()
      if not is_tmrw_valid:
        LogUtils.warning('Tmrw is not a valid trade date')
        raise BadRequestException('Date', DateUtils.to_string(date.today()))

      req: GetTradeOrdersRequest = GetTradeOrdersRequest()

      # If Sunday, check Friday's price.
      today: date = date.today()
      if today.weekday() == AppConsts.WEEKDAY_IDX_SUN:
        today = DateUtils.add_business_days(today, -1)
      req.created = today.strftime('%Y-%m-%d')

      req.exact_status = AppConsts.ORDER_STATUS_INIT
      orders: List[TradeOrderCustom] = self.get_trade_orders(req)

      req_to_ignore: GetTradeOrdersRequest = GetTradeOrdersRequest()
      req_to_ignore.status = [
          AppConsts.ORDER_STATUS_SUBMITTED_ENTRY,
          AppConsts.ORDER_STATUS_IN_POSITION,
          AppConsts.ORDER_STATUS_SUBMITTED_EXIT,
          AppConsts.ORDER_STATUS_CANCELLED_EXIT
      ]
      orders_to_ignore: List[TradeOrderCustom] = self.get_trade_orders(req_to_ignore)
      symbols_to_ignore: List[str] = [o.symbol_master.symbol for o in orders_to_ignore] if orders_to_ignore else []

      LogUtils.debug('symbols_to_ignore = {0}'.format(symbols_to_ignore))

      if not orders:
        LogUtils.debug('No orders suggested')

      shuffle(orders)
      prioritized_orders: List[TradeOrderCustom] = []
      for order in orders:
        if order.trade_order.strategy == AppConsts.STRATEGY_DOUBLE_BOTTOMS:
          prioritized_orders.append(order)
      for order in orders:
        if order.trade_order.strategy == AppConsts.STRATEGY_DOUBLE_TOPS:
          prioritized_orders.append(order)

      accnt: Account = self.__alpaca_client.get_account()
      capital: float = NumberUtils.to_floor(NumberUtils.to_float(accnt._raw['buying_power']) / 2)  # 2 to trade everyday
      for order in prioritized_orders:
        try:
          LogUtils.debug('Try symbol = {0}'.format(order.symbol_master.symbol))

          if order.symbol_master.symbol in symbols_to_ignore:
            LogUtils.debug('Ignore for = {0}'.format(order.symbol_master.symbol))
            continue

          cost: float = NumberUtils.to_float(order.stock_price_daily.close_price * order.trade_order.qty)

          if cost > capital:
            LogUtils.debug('Too expensive for = {0}'.format(order.symbol_master.symbol))
            continue
          capital = capital - cost

          resp: Order = self.__alpaca_client.submit_order(
              symbol=order.symbol_master.symbol,
              qty=order.trade_order.qty,
              action=order.trade_order.action)
          if resp:
            org: TradeOrder = BaseService._get_by_id(TradeOrder, order.trade_order.id)
            if not org:
              raise NotFoundException('TradeOrder', 'id', order.trade_order.id)
            org.alpaca_id = resp.id
            org.status = AppConsts.ORDER_STATUS_SUBMITTED_ENTRY
            org.order_type = AppConsts.ORDER_TYPE_MARKET
            org.time_in_force = AppConsts.TIME_IN_FORCE_DAY
            org.modified = datetime.now()
            BaseService._update()

        except Exception as ex:
          LogUtils.error('Queue Position Error', ex)
          errors.append(ex)

    except Exception as ex:
      LogUtils.error('Queue Position Error', ex)
      errors.append(ex)
    finally:
      self.__email_client.send_html(
          subject=AppConsts.EMAIL_SUBJECT_QUEUE_POSITIONS,
          template_path=AppConsts.TEMPLATE_PATH_QUEUE_POSITIONS,
          model={'errors': errors})
      return 1

  def sync_orders(self) -> int:
    errors: List[Exception] = []
    try:
      req: GetTradeOrdersRequest = GetTradeOrdersRequest()
      req.status = [
          AppConsts.ORDER_STATUS_SUBMITTED_ENTRY,
          AppConsts.ORDER_STATUS_SUBMITTED_EXIT
      ]
      orders: List[TradeOrderCustom] = self.get_trade_orders(req)

      if not orders:
        LogUtils.debug('No orders submitted')

      for order in orders:
        try:
          LogUtils.debug('Sync order for = {0}'.format(order.symbol_master.symbol))

          resp: Order = None
          if order.trade_order.status == AppConsts.ORDER_STATUS_SUBMITTED_ENTRY:
            resp = self.__alpaca_client.get_order(order.trade_order.alpaca_id)
          elif order.trade_order.status == AppConsts.ORDER_STATUS_SUBMITTED_EXIT:
            resp = self.__alpaca_client.get_order(order.trade_order.exit_alpaca_id)

          if resp:
            org: TradeOrder = BaseService._get_by_id(TradeOrder, order.trade_order.id)
            if not org:
              raise NotFoundException('TradeOrder', 'id', order.trade_order.id)

            if order.trade_order.status == AppConsts.ORDER_STATUS_SUBMITTED_ENTRY \
                    and resp.status == AppConsts.ALPACA_ORDER_STATUS_FILLED:
              org.status = AppConsts.ORDER_STATUS_IN_POSITION
              org.actual_qty = NumberUtils.to_int(resp.filled_qty)
              org.actual_entry_price = NumberUtils.to_float(resp.filled_avg_price)
              org.modified = datetime.now()
              BaseService._update()
            elif order.trade_order.status == AppConsts.ORDER_STATUS_SUBMITTED_ENTRY \
                    and resp.status == AppConsts.ALPACA_ORDER_STATUS_CANCELLED:
              org.status = AppConsts.ORDER_STATUS_CANCELLED_ENTRY
              org.modified = datetime.now()
              BaseService._update()
            elif order.trade_order.status == AppConsts.ORDER_STATUS_SUBMITTED_EXIT \
                    and resp.status == AppConsts.ALPACA_ORDER_STATUS_FILLED:
              exit_price: StockPriceDaily = self.__stock_service.get_single_stock_price_daily(
                  order.symbol_master.id,
                  DateUtils.get_date(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d'))
              if exit_price:
                org.exit_stock_price_daily_id = exit_price.id
              org.status = AppConsts.ORDER_STATUS_COMPLETED
              org.actual_exit_price = NumberUtils.to_float(resp.filled_avg_price)
              org.modified = datetime.now()
              BaseService._update()
            elif order.trade_order.status == AppConsts.ORDER_STATUS_SUBMITTED_EXIT \
                    and resp.status == AppConsts.ALPACA_ORDER_STATUS_CANCELLED:
              org.status = AppConsts.ORDER_STATUS_CANCELLED_EXIT
              org.modified = datetime.now()
              BaseService._update()
              raise Exception('Exit Error = {0}'.format(resp.status))
            else:
              raise Exception('Sync Status = {0}'.format(resp.status))
          else:
            raise NotFoundException('Alpaca Order', 'id', order.trade_order.alpaca_id)

        except Exception as ex:
          LogUtils.error('Sync Orders Error', ex)
          errors.append(ex)

    except Exception as ex:
      LogUtils.error('Sync Orders Error', ex)
      errors.append(ex)
    finally:
      self.__email_client.send_html(
          subject=AppConsts.EMAIL_SUBJECT_SYNC_ORDERS,
          template_path=AppConsts.TEMPLATE_PATH_SYNC_ORDERS,
          model={'errors': errors})
      return 1

  def close_positions(self) -> int:
    errors: List[Exception] = []
    try:
      is_tmrw_valid: bool = self.__alpaca_client.is_tmrw_valid()
      if not is_tmrw_valid:
        LogUtils.warning('Tmrw is not a valid trade date')
        raise BadRequestException('Date', DateUtils.to_string(date.today()))

      req: GetTradeOrdersRequest = GetTradeOrdersRequest()
      req.exact_status = AppConsts.ORDER_STATUS_IN_POSITION
      orders: List[TradeOrderCustom] = self.get_trade_orders(req)

      if not orders:
        LogUtils.debug('No positions')

      for order in orders:
        try:
          LogUtils.debug('Check position for = {0}'.format(order.symbol_master.symbol))
          spd: StockPriceDaily = self.__stock_service.get_last_single_stock_price_daily(order.symbol_master.id)
          if not spd:
            LogUtils.warning('No Stock Price Found')
            raise NotFoundException('SPD', 'symbol_id', order.symbol_master.id)

          LogUtils.debug('Last close price = {0}'.format(spd.close_price))
          # is_exit: bool = (spd.close_price > order.trade_order.target_price
          #                  or spd.close_price < order.trade_order.stop_loss)
          if True:  # To-do: fix this to use strategy service. is_exit:

            LogUtils.debug('Close position for = {0}'.format(order.symbol_master.symbol))

            resp: Order = self.__alpaca_client.submit_order(
                symbol=order.symbol_master.symbol,
                qty=order.trade_order.actual_qty,
                action=AppConsts.ACTION_SELL if order.trade_order.action == AppConsts.ACTION_BUY else AppConsts.ACTION_BUY)
            if resp:
              org: TradeOrder = BaseService._get_by_id(TradeOrder, order.trade_order.id)
              if not org:
                LogUtils.warning('Order not found.')
                raise NotFoundException('TradeOrder', 'id', order.trade_order.id)
              org.exit_alpaca_id = resp.id
              org.status = AppConsts.ORDER_STATUS_SUBMITTED_EXIT
              org.modified = datetime.now()
              BaseService._update()
            else:
              raise Exception('Close Position Error.')

        except Exception as ex:
          LogUtils.error('Close Position Error', ex)
          errors.append(ex)

    except Exception as ex:
      LogUtils.error('Close Position Error', ex)
      errors.append(ex)
    finally:
      self.__email_client.send_html(
          subject=AppConsts.EMAIL_SUBJECT_CLOSE_POSITIONS,
          template_path=AppConsts.TEMPLATE_PATH_CLOSE_POSITIONS,
          model={'errors': errors})
      return 1

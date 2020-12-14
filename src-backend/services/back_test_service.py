import pandas as pd
from pandas.core.frame import DataFrame
from pandas.core.indexes.datetimes import DatetimeIndex
from pandas.core.series import Series
from datetime import date, datetime, timedelta
from exceptions.bad_request_exception import BadRequestException
from exceptions.db_connection_exception import DbConnectionException
from random import shuffle
from typing import Dict, List, Any
from app_consts import AppConsts
from app_utils.date_utils import DateUtils
from app_utils.log_utils import LogUtils
from app_utils.number_utils import NumberUtils
from app_utils.string_utils import StringUtils
from models.back_test_result_item import BackTestResultItem
from models.db.etf_price_daily import EtfPriceDaily
from models.db.stock_price_daily import StockPriceDaily
from models.db.symbol_master import SymbolMaster
from models.request_models.back_test_run_request import BackTestRunRequest
from models.response_models.back_test_run_response import BackTestRunResponse
from models.transaction import Transaction
from services.base_service import BaseService
from services.stock_service import StockService
from services.calc_service import CalcService


class BackTestService(BaseService):
  def __init__(self) -> None:
    super().__init__()
    self.__stock_service = StockService()
    self.__calc_service = CalcService()

  def run(self, req: BackTestRunRequest) -> BackTestRunResponse:
    if not req or not req.is_valid_model():
      raise BadRequestException()
    response: BackTestRunResponse = BackTestRunResponse(req)

    # Init Symbols
    symbols: List[SymbolMaster] = self.__get_symbols__(req)

    # Init Prices
    prices: DataFrame = self.__get_prices__(req, symbols)

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
    start_date: date = DateUtils.add_business_days(req.date_from_obj, -1)
    start_date = DateUtils.add_business_days(start_date, 1)
    start_date_str: str = DateUtils.to_string(start_date)
    end_date: date = DateUtils.add_business_days(req.date_to_obj, -1)
    dates: DataFrame = self.__stock_service.get_dates(prices, start_date, end_date)

    LogUtils.debug('Dates actual_start={0}, actual_end={1}, shape={2}'.format(start_date, end_date, dates.shape))
    # endregion

    # region Loop Dates
    strategy_item: BackTestResultItem = next(b for b in response.back_test_result_items if b.target == req.strategy_type)
    strategy_item.capital[start_date_str] = req.start_capital
    strategy_item.capital_available[start_date_str] = req.start_capital
    portfolio: Dict = {}

    for i, date_row in dates.iterrows():
      current_date = date_row[AppConsts.PRICE_COL_DATE]
      current_date_str: str = DateUtils.to_string(current_date)
      next_date = date_row[AppConsts.CUSTOM_COL_NEXT_DATE]
      next_date_str = DateUtils.to_string(next_date)
      next_next_date = date_row[AppConsts.CUSTOM_COL_NEXT_NEXT_DATE]

      shuffle(symbols)
      for symbol in symbols:
        has_price: bool = (symbol.id, current_date) in prices.index
        if not has_price:
          continue
        price: Series = prices.loc[symbol.id, current_date]

        if symbol.instrument == AppConsts.INSTRUMENT_ETF:

          # region Benchmark
          b_result_item: BackTestResultItem = next(b for b in response.back_test_result_items if b.target == symbol.symbol)
          if not b_result_item:
            continue

          if not b_result_item.transactions:
            no_of_shares: int = self.__stock_service.get_no_of_shares(
                req.start_capital,
                req.pct_risk_per_trade,
                req.volume_limit,
                price,
                req.slippage)
            if no_of_shares == 0:
              LogUtils.warning('0 shares for ETF={0}'.format(symbol.symbol))
              continue

            b_transaction: Transaction = Transaction()
            b_transaction.symbol_master = symbol
            b_transaction.action = AppConsts.ACTION_BUY
            b_transaction.start_date = current_date
            b_transaction.start_price = price.loc[AppConsts.PRICE_COL_OPEN]
            b_transaction.no_of_shares = no_of_shares
            b_result_item.transactions.append(b_transaction)
            b_result_item.capital[current_date_str] = req.start_capital
          else:
            b_transaction: Transaction = b_result_item.transactions[0]
            b_transaction.end_date = current_date
            b_transaction.end_price = price.loc[AppConsts.PRICE_COL_CLOSE]
            b_transaction.set_readonly_props()
            b_result_item.capital[current_date_str] = self.__calc_benchmark_capital(
                req,
                b_transaction.start_price,
                b_transaction.end_price,
                b_transaction.no_of_shares)
          b_result_item.ttl_no_days += 1
          # endregion

        else:

          # region Strategy
          strategy_service._do_calculations(symbol.id, current_date)
          action: str = strategy_service._get_action()

          is_in_position: bool = symbol.id in portfolio
          if not is_in_position:

            if len(portfolio) == req.portfolio_max:  # todo: prioritize?
              continue
            if current_date == end_date or next_date >= end_date:
              continue
            has_next_price: bool = (symbol.id, next_date) in prices.index
            has_next_next_price: bool = (symbol.id, next_next_date) in prices.index
            if not has_next_price or not has_next_next_price:
              continue
            adv: float = price.loc[AppConsts.CUSTOM_COL_ADV] if price.loc[AppConsts.CUSTOM_COL_ADV] > 0 else price.loc[AppConsts.PRICE_COL_VOLUME]
            if adv < req.adv_min:
              continue
            adpv: float = price.loc[AppConsts.CUSTOM_COL_ADPV] if price.loc[AppConsts.CUSTOM_COL_ADPV] > 0 else price.loc[AppConsts.CUSTOM_COL_PV]
            if adpv < req.adpv_min:
              continue

            next_price: Series = prices.loc[symbol.id, next_date]

            has_entry_conditions: bool = strategy_service._has_entry_conditions(symbol.id, current_date)
            if has_entry_conditions:

              no_of_shares: int = self.__stock_service.get_no_of_shares(
                  strategy_item.capital_available[current_date_str],
                  req.pct_risk_per_trade,
                  req.volume_limit,
                  next_price,
                  req.slippage,
                  action == AppConsts.ACTION_BUY)
              if no_of_shares == 0:
                continue

              trans: Transaction = Transaction()
              trans.symbol_master = symbol
              trans.action = action
              trans.start_date = next_date
              trans.start_price = next_price.loc[AppConsts.PRICE_COL_OPEN]
              trans.no_of_shares = no_of_shares

              trans_amount: float = NumberUtils.round(trans.start_price * no_of_shares)
              strategy_item.capital_available[current_date_str] -= trans_amount

              # Add to portfolio
              portfolio[symbol.id] = trans

          elif is_in_position:

            has_exit_conditions: bool = strategy_service._has_exit_conditions(symbol.id, current_date)
            has_next_next_price: bool = (symbol.id, next_next_date) in prices.index
            if next_date == end_date or not has_next_next_price or has_exit_conditions:

              next_price: Series = prices.loc[symbol.id, next_date]
              next_open_price: float = next_price.loc[AppConsts.PRICE_COL_OPEN]
              slippage_price: float = 0
              if action == AppConsts.ACTION_BUY:
                slippage_price: float = NumberUtils.round(next_open_price - (next_open_price * AppConsts.BASIS_POINT * req.slippage))
              else:
                slippage_price: float = NumberUtils.round(next_open_price + (next_open_price * AppConsts.BASIS_POINT * req.slippage))
              trans: Transaction = portfolio.get(symbol.id)
              trans.end_date = next_date
              trans.end_price = slippage_price
              trans.set_readonly_props()
              strategy_item.transactions.append(trans)

              if action == AppConsts.ACTION_BUY:
                trans_amount = NumberUtils.round(trans.end_price * trans.no_of_shares)
                strategy_item.capital_available[current_date_str] += trans_amount
              else:
                init_trans_amount = NumberUtils.round(trans.start_price * trans.no_of_shares)
                strategy_item.capital_available[current_date_str] += init_trans_amount
                strategy_item.capital_available[current_date_str] += trans.change_in_capital

              # Remove from portfolio
              portfolio.pop(symbol.id, None)

          # endregion

      # capital = capital available + capital in portfolio
      capital: float = strategy_item.capital_available[current_date_str]
      for key, val in portfolio.items():
        price: Series = prices.loc[key, current_date]
        capital += price.loc[AppConsts.PRICE_COL_CLOSE] * val.no_of_shares
      strategy_item.capital[current_date_str] = NumberUtils.round(capital)
      strategy_item.ttl_no_days += 1
      strategy_item.capital[next_date_str] = strategy_item.capital[current_date_str]
      strategy_item.capital_available[next_date_str] = strategy_item.capital_available[current_date_str]

    # endregion

    for result_item in response.back_test_result_items:
      result_item.set_readonly_props()
    return response

  def __get_symbols__(self, req: BackTestRunRequest) -> List[SymbolMaster]:
    if not req or req.test_limit_symbol <= 0:
      raise BadRequestException()
    symbols: List[SymbolMaster] = self.__stock_service.get_symbols(AppConsts.INSTRUMENT_STOCK, [AppConsts.SYMBOL_STATUS_EXCLUDE_TRADE])
    if not symbols:
      raise DbConnectionException()
    shuffle(symbols)
    symbols = symbols[:req.test_limit_symbol]
    if req.benchmark_etfs:
      for benchmark_etf in req.benchmark_etfs:
        etf_symbol: SymbolMaster = self.__stock_service.get_symbol(benchmark_etf, AppConsts.INSTRUMENT_ETF)
        if not etf_symbol:
          continue
        symbols.append(etf_symbol)
    LogUtils.debug('Symbol Count={0}'.format(len(symbols)))
    return symbols

  def __get_prices__(self, req: BackTestRunRequest, symbols: List[SymbolMaster]) -> DataFrame:
    if not req or not symbols:
      raise BadRequestException()

    price_items: List[Any] = []
    for symbol in symbols:
      temp: List[Any] = []
      if symbol.instrument == AppConsts.INSTRUMENT_STOCK:
        temp = self.__stock_service.get_stock_prices_daily(
            symbol.id,
            req.date_from_obj,
            req.date_to_obj)
      elif symbol.instrument == AppConsts.INSTRUMENT_ETF:
        temp = self.__stock_service.get_etf_prices_daily(
            symbol.id,
            req.date_from_obj,
            req.date_to_obj)
      if temp:
        price_items.extend(temp)

    prices: DataFrame = self.__stock_service.get_price_dataframe(price_items)

    LogUtils.debug('Prices Init Shape={0}'.format(prices.shape))
    return prices

  def __calc_benchmark_capital(self, req: BackTestRunRequest, start_price: float, end_price: float, no_of_shares: int) -> float:
    capital: float = req.start_capital - (start_price * no_of_shares)
    return NumberUtils.round(capital + (end_price * no_of_shares))

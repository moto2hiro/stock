from flask import Blueprint, request
from app_utils.model_utils import ModelUtils
from app_utils.string_utils import StringUtils
from app_utils.date_utils import DateUtils
from models.request_models.get_trade_orders_request import GetTradeOrdersRequest
from models.request_models.trade_suggestions_request import TradeSuggestionsRequest
from models.response_models.response_model import ResponseModel
from services.trade_service import TradeService

trade_api: Blueprint = Blueprint('trade_api', __name__)
__trade_service = TradeService()


@trade_api.route('/getAccount', methods=['GET'])
def get_account() -> str:
  return StringUtils.to_json(ResponseModel(__trade_service.get_account()))


@trade_api.route('/getKeyInfo/<symbol>', methods=['GET'])
def get_key_info(symbol: str) -> str:
  return StringUtils.to_json(ResponseModel(__trade_service.get_key_info(symbol)))


@trade_api.route('/getTradeOrders', methods=['POST'])
def get_trade_orders() -> str:
  req: GetTradeOrdersRequest = ModelUtils.get_obj(GetTradeOrdersRequest(), request.get_json())
  return StringUtils.to_json(ResponseModel(__trade_service.get_trade_orders(req)))


@trade_api.route('/getSuggestions', methods=['POST'])
def get_suggestions() -> str:
  req: TradeSuggestionsRequest = ModelUtils.get_obj(TradeSuggestionsRequest(), request.get_json())
  return StringUtils.to_json(ResponseModel(__trade_service.get_suggestions(req)))


@trade_api.route('/getAllSuggestions', methods=['GET'])
def get_all_suggestions() -> str:
  return StringUtils.to_json(ResponseModel(__trade_service.get_all_suggestions()))


@trade_api.route('/queuePositions', methods=['GET'])
def queue_positions() -> str:
  return StringUtils.to_json(ResponseModel(__trade_service.queue_positions()))


@trade_api.route('/syncOrders', methods=['GET'])
def sync_orders() -> str:
  return StringUtils.to_json(ResponseModel(__trade_service.sync_orders()))


@trade_api.route('/closePositions', methods=['GET'])
def close_positions() -> str:
  return StringUtils.to_json(ResponseModel(__trade_service.close_positions()))

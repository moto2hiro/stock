from flask import Blueprint, request
from app_utils.model_utils import ModelUtils
from app_utils.string_utils import StringUtils
from app_utils.log_utils import LogUtils
from models.db.symbol_master import SymbolMaster
from models.request_models.chart_request import ChartRequest as CR
from models.response_models.response_model import ResponseModel
from services.stock_service import StockService

stock_api: Blueprint = Blueprint('stock_api', __name__)
__stock_service = StockService()


@stock_api.route('/get_symbols/<instrument>', methods=['GET'])
def get_symbols(instrument: str) -> str:
  return StringUtils.to_json(ResponseModel(__stock_service.get_symbols(instrument)))


@stock_api.route('/update_symbol', methods=['POST'])
def update_symbol() -> str:
  req: SymbolMaster = ModelUtils.get_obj(SymbolMaster(), request.get_json())
  return StringUtils.to_json(ResponseModel(__stock_service.update_symbol(req)))


@stock_api.route('/delete_old_prices', methods=['GET'])
def delete_old_prices() -> str:
  return StringUtils.to_json(ResponseModel(__stock_service.delete_old_prices()))


@stock_api.route('/get_sample_prices_for_charts', methods=['POST'])
def get_sample_prices_for_charts() -> str:
  req: CR = ModelUtils.get_obj(CR(), request.get_json())
  return StringUtils.to_json(ResponseModel(__stock_service.get_sample_prices_for_charts(req)))


@stock_api.route('/get_sp500_mismatches/<is_missing>', methods=['GET'])
def get_sp500_mismatches(is_missing: str) -> str:
  return StringUtils.to_json(ResponseModel(__stock_service.get_sp500_mismatches(is_missing == 'True')))

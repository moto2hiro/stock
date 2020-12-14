from flask import Blueprint
from app_utils.string_utils import StringUtils
from models.response_models.response_model import ResponseModel
from services.import_service import ImportService
from services.import_csv_service import ImportCsvService

import_api: Blueprint = Blueprint('import_api', __name__)
__import_service = ImportService()
__import_csv_service = ImportCsvService()


@import_api.route('/symbols', methods=['GET'])
def import_symbols() -> str:
  return StringUtils.to_json(ResponseModel(__import_service.import_symbols()))

# region Alpaca
@import_api.route('/prices', methods=['GET'])
def import_prices() -> str:
  return StringUtils.to_json(ResponseModel(__import_service.import_prices()))
# endregion

# region Csv

# Run First
@import_api.route('/csv/symbols', methods=['GET'])
def import_from_csv_symbols() -> str:
  return "1"  # __import_csv_service.import_from_csv_symbols()

# Run Second
@import_api.route('/csv/prices', methods=['GET'])
def import_from_csv_prices() -> str:
  return "1"  # __import_csv_service.import_from_csv_prices()

# Run Third
@import_api.route('/csv/companynames', methods=['GET'])
def import_from_csv_companynames() -> str:
  return "1"  # __import_csv_service.import_from_csv_companynames()

# Run Fourth
@import_api.route('/csv/incomestatements', methods=['GET'])
def import_from_csv_incomestatements() -> str:
  return "1"  # __import_csv_service.import_from_csv_incomestatements()

# Run Fifth
@import_api.route('/csv/balancesheets', methods=['GET'])
def import_from_csv_balancesheets() -> str:
  return "1"  # __import_csv_service.import_from_csv_balancesheets()

# Run Sixth
@import_api.route('/csv/calculations', methods=['GET'])
def import_from_csv_calculations() -> str:
  return "1"  # __import_csv_service.import_from_csv_calculations()

# Run Seventh
@import_api.route('/csv/filedates', methods=['GET'])
def import_from_csv_filedates() -> str:
  return "1"  # __import_csv_service.import_from_csv_filedates()

# Run Eigth
@import_api.route('/csv/yahoo', methods=['GET'])
def import_from_csv_yahoo() -> str:
  return "1"  # __import_csv_service.import_from_csv_yahoo()

# endregion

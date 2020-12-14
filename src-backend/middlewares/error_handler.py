import http
from flask import Blueprint
from app_utils.log_utils import LogUtils
from app_utils.string_utils import StringUtils
from exceptions.bad_request_exception import BadRequestException
from exceptions.db_connection_exception import DbConnectionException
from exceptions.not_found_exception import NotFoundException
from models.response_models.response_model import ResponseModel

error_handler: Blueprint = Blueprint('error_handler', __name__)


@error_handler.app_errorhandler(Exception)
def handle(ex: Exception) -> str:
  response: ResponseModel = ResponseModel()
  try:
    LogUtils.error('Handle error', ex)

    msg: str = str(ex)
    response.http_status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
    response.error_message = msg if msg else 'Error'
    if isinstance(ex, BadRequestException):
      response.http_status_code = http.HTTPStatus.BAD_REQUEST
    if isinstance(ex, NotFoundException):
      response.http_status_code = http.HTTPStatus.NOT_FOUND
    if isinstance(ex, DbConnectionException):
      response.http_status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
  except Exception as e:
    response.http_status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
    response.error_message = 'Error'
  return StringUtils.to_json(response)

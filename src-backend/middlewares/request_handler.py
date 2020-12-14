import json
from typing import Any
from flask import Blueprint, request
from app_utils.log_utils import LogUtils

request_handler: Blueprint = Blueprint('request_handler', __name__)


@request_handler.before_app_request
def handle_before_app_request() -> None:
  try:
    LogUtils.debug('START-Request={0}'.format(json.dumps(request.json, indent=2)))
  finally:
    pass


@request_handler.after_app_request
def handle_after_app_request(resp: Any) -> Any:
  try:
    LogUtils.debug('END-Request')
  finally:
    pass
  return resp

import http
import requests
from typing import Any
from app_utils.log_utils import LogUtils
from app_utils.model_utils import ModelUtils


class CustomHttpClient:
  def __init__(self) -> None:
    pass

  def get(self, path: str) -> Any:
    if not path:
      return None
    req = requests.get(path)
    LogUtils.debug('status code = {0}, path = {1}'.format(req.status_code, path))

    if req.status_code != http.HTTPStatus.OK:
      return None
    return req.json()

import http
from typing import Any
from models.response_models.base_response import BaseResponse


class ResponseModel(BaseResponse):

  def __init__(self, data: Any = None) -> None:
    super().__init__()
    self._http_status_code = http.client.OK
    self._error_message = ''
    self._data = data

  @property
  def http_status_code(self) -> int: return self._http_status_code

  @http_status_code.setter
  def http_status_code(self, val: int) -> None: self._http_status_code = val

  @property
  def error_message(self) -> str: return self._error_message

  @error_message.setter
  def error_message(self, val: str) -> None: self._error_message = val

  @property
  def data(self) -> Any: return self._data

  @data.setter
  def data(self, val: Any) -> None: self._data = val

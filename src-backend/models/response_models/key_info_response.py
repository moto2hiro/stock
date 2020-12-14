from typing import Any, Dict
from models.response_models.base_response import BaseResponse


class KeyInfoResponse(BaseResponse):

  def __init__(self) -> None:
    super().__init__()
    self._news = {}

  @property
  def iex_cloud_key_stats(self) -> Any: return self._iex_cloud_key_stats

  @iex_cloud_key_stats.setter
  def iex_cloud_key_stats(self, val: Any) -> None: self._iex_cloud_key_stats = val

  @property
  def news(self) -> Dict: return self._news

  @news.setter
  def news(self, val: Dict) -> None: self._news = val

  @property
  def td_ameritrade_key_stats(self) -> Any: return self._td_ameritrade_key_stats

  @td_ameritrade_key_stats.setter
  def td_ameritrade_key_stats(self, val: Any) -> None: self._td_ameritrade_key_stats = val

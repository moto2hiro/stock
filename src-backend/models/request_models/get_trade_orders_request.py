from datetime import date
from typing import Any, Dict, List
from app_utils.date_utils import DateUtils


class GetTradeOrdersRequest:
  def __init__(self) -> None:
    self._status = []
    self._exact_status = None
    self._created = None

  @property
  def status(self) -> List[int]: return self._status

  @status.setter
  def status(self, val: List[int]) -> None: self._status = val

  @property
  def exact_status(self) -> List[int]: return self._exact_status

  @exact_status.setter
  def exact_status(self, val: List[int]) -> None: self._exact_status = val

  @property
  def created(self) -> str: return self._created

  @created.setter
  def created(self, val: str) -> None: self._created = val

  @property
  def created_obj(self) -> date: return DateUtils.get_date(self._created, '%Y-%m-%d')

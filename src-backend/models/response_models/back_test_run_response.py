from typing import List, Dict
from itertools import groupby
from app_utils.log_utils import LogUtils
from app_utils.number_utils import NumberUtils
from app_utils.stat_utils import StatUtils
from app_utils.string_utils import StringUtils
from models.transaction import Transaction
from models.request_models.back_test_run_request import BackTestRunRequest
from models.response_models.base_response import BaseResponse
from models.back_test_result_item import BackTestResultItem


class BackTestRunResponse(BaseResponse):

  def __init__(self, req: BackTestRunRequest) -> None:
    super().__init__()
    self._back_test_result_items = []
    if not req:
      LogUtils.warning('BackTestRunRequest not found.')
      return
    self._back_test_result_items.append(BackTestResultItem(
        target=req.strategy_type,
        is_benchmark=False))
    if req.benchmark_etfs:
      for benchmark_etf in req.benchmark_etfs:
        self._back_test_result_items.append(BackTestResultItem(
            target=benchmark_etf,
            is_benchmark=True))
    LogUtils.debug('Count={0}'.format(len(self._back_test_result_items)))

  @property
  def back_test_result_items(self) -> List[BackTestResultItem]: return self._back_test_result_items

  @back_test_result_items.setter
  def back_test_result_items(self, val: List[BackTestResultItem]) -> None: self._back_test_result_items = val

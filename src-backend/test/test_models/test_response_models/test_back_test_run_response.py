from test.test_base import TestBase
from app_consts import AppConsts
from models.request_models.back_test_run_request import BackTestRunRequest
from models.response_models.back_test_run_response import BackTestRunResponse
from services.back_test_service import BackTestService


class TestBackTestRunResponse(TestBase):

  def __init__(self, *args, **kwargs):
    super(TestBackTestRunResponse, self).__init__(*args, **kwargs)

  def test_constructor_should_init_appropriately(self) -> None:
    # ARRANGE
    none_case = None
    no_benchmark_case: BackTestRunRequest = BackTestRunRequest()
    no_benchmark_case.strategy_type = 'some_strategy'
    benchmark_case: BackTestRunRequest = BackTestRunRequest()
    benchmark_case.strategy_type = 'some_strategy'
    benchmark_case.benchmark_etfs = [AppConsts.BENCHMARK_ETF_SPY]

    # ACT
    ret_none_case: BackTestRunResponse = BackTestRunResponse(none_case)
    ret_no_benchmark_case: BackTestRunResponse = BackTestRunResponse(no_benchmark_case)
    ret_benchmark_case: BackTestRunResponse = BackTestRunResponse(benchmark_case)

    # ASSERT
    self.assertEqual(0, len(ret_none_case.back_test_result_items))
    self.assertEqual(1, len(ret_no_benchmark_case.back_test_result_items))
    self.assertEqual(2, len(ret_benchmark_case.back_test_result_items))

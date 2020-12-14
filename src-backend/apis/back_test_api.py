from flask import Blueprint, request
from app_utils.model_utils import ModelUtils
from app_utils.string_utils import StringUtils
from models.request_models.back_test_run_request import BackTestRunRequest
from models.response_models.response_model import ResponseModel
from services.back_test_service import BackTestService

back_test_api: Blueprint = Blueprint('back_test_api', __name__)
__back_test_service = BackTestService()


@back_test_api.route('/run', methods=['POST'])
def run() -> str:
  req: BackTestRunRequest = ModelUtils.get_obj(BackTestRunRequest(), request.get_json())
  return StringUtils.to_json(ResponseModel(__back_test_service.run(req)))

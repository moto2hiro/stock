import http
import requests
from typing import List, Dict, Any
from app_consts import AppConsts
from app_utils.log_utils import LogUtils
from clients.custom_http_client import CustomHttpClient


class TdAmeritradeClient:
  def __init__(self) -> None:
    self._custom_http_client: CustomHttpClient = CustomHttpClient()

  def get_key_stats(self, symbol: str) -> Any:
    """
    https://developer.tdameritrade.com/instruments/apis/get/instruments
    """
    path: str = '/instruments?symbol={0}&projection=fundamental'.format(symbol)
    return self._custom_http_client.get(self.__get_full_path__(path))

  def __get_full_path__(self, path: str) -> str:
    return '{0}{1}&apikey={2}'.format(AppConsts.TD_AMERITRADE_API_BASE_URL, path, AppConsts.TD_AMERITRADE_API_KEY)

import http
import requests
from typing import List, Dict, Any
from app_consts import AppConsts
from app_utils.log_utils import LogUtils
from clients.custom_http_client import CustomHttpClient


class IexCloudClient:
  def __init__(self) -> None:
    self._custom_http_client: CustomHttpClient = CustomHttpClient()

  def get_company_profiles(self, symbols: List[str]) -> List[Dict]:
    """
    https://iexcloud.io/docs/api/#company
    """
    ret: List[Dict] = []
    if not symbols:
      return ret

    for symbol in symbols:
      path: str = '/stock/{0}/company'.format(symbol)
      r = requests.get(self.__get_full_path__(path))
      if r.status_code != http.HTTPStatus.OK:
        LogUtils.debug('{0}={1}', symbol, r.status_code)
        continue
      profile: Dict = r.json()
      if not profile:
        LogUtils.debug('{0} empty', symbol)
      else:
        ret.append(profile)
    return ret

  def get_key_stats(self, symbol: str) -> Any:
    """
    https://iexcloud.io/docs/api/#key-stats
    """
    path: str = '/stock/{0}/stats'.format(symbol)
    return self._custom_http_client.get(self.__get_full_path__(path))

  def get_news(self, symbol: str, last: int = 5, lang: str = 'en') -> Any:
    """
    https://iexcloud.io/docs/api/#news
    """
    path: str = '/stock/{0}/news/last/{1}'.format(symbol, last)
    items: List[Any] = self._custom_http_client.get(self.__get_full_path__(path))
    return [i for i in items if i['lang'] == lang]

  def __get_full_path__(self, path: str) -> str:
    return '{0}{1}?token={2}'.format(AppConsts.IEX_CLOUD_API_BASE_URL, path, AppConsts.IEX_CLOUD_API_KEY)

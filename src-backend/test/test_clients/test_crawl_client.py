from pandas.core.frame import DataFrame
from test.test_base import TestBase
from app_consts import AppConsts
from clients.crawl_client import CrawlClient


class TestCrawlClient(TestBase):

  def __init__(self, *args, **kwargs):
    super(TestCrawlClient, self).__init__(*args, **kwargs)
    self.__crawl_client: CrawlClient = CrawlClient()

  def test_get_html_table_should_return_appropriately(self) -> None:
    # ARRANGE
    url: str = AppConsts.WIKI_SP500_URL
    element_id: str = AppConsts.WIKI_SP500_ELEMENT_ID
    index_col: str = AppConsts.WIKI_SP500_COL_SYMBOL

    # ACT
    df: DataFrame = self.__crawl_client.get_html_table(url, element_id, [index_col])

    # ASSERT
    self.assertIsNotNone(df)

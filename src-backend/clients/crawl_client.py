import pandas as pd
from typing import List, Any
from pandas.core.frame import DataFrame
from app_utils.log_utils import LogUtils


class CrawlClient:

  def __init__(self) -> None:
    pass

  def get_html_table(self, url: str, element_id: str, index_cols: List[str]) -> DataFrame:

    LogUtils.debug('Url={0}, Element Id={1}'.format(url, element_id))

    table: List[Any] = pd.read_html(url, attrs={'id': element_id}, index_col=index_cols)
    df: DataFrame = table[0] if table else None

    LogUtils.debug('Df={0}'.format(df))

    return df

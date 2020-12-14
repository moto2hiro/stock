import numpy as np
import pandas as pd
from typing import List, Dict


class StatUtils:
  @staticmethod
  def get_descriptive_stats(items: List, round: int = 2) -> Dict:
    if not items:
      return {}
    return pd.Series(items) \
        .agg([
            'count',
            'sum',
            'mean',
            'max',
            'min',
            StatUtils.percentile(0.25),
            StatUtils.percentile(0.75),
            'std']) \
        .round(round) \
        .fillna(0) \
        .to_dict()

  @staticmethod
  def percentile(n):
    def percentile_(x):
      return x.quantile(n)
    percentile_.__name__ = 'percentile_{:2.0f}'.format(n*100)
    return percentile_

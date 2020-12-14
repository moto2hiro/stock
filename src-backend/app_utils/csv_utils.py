import csv
from typing import List, Dict
from app_utils.string_utils import StringUtils
from app_utils.log_utils import LogUtils


class CsvUtils:

  @staticmethod
  def parse_as_list(file_path: str) -> List[List[str]]:
    try:
      LogUtils.debug('START')
      if StringUtils.isNullOrWhitespace(file_path):
        return []
      with open(file_path) as f:
        return list(csv.reader(f)) if f else []
    finally:
      LogUtils.debug('END')

  @staticmethod
  def parse_as_dict(file_path: str) -> List[Dict]:
    try:
      LogUtils.debug('START')
      if StringUtils.isNullOrWhitespace(file_path):
        return []
      with open(file_path) as f:
        return list(csv.DictReader(f)) if f else []
    finally:
      LogUtils.debug('END')

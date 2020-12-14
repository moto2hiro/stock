import os
from typing import List, Tuple
from app_utils.string_utils import StringUtils


class FileUtils:

  @staticmethod
  def get_files(file_path: str, is_full: bool = False) -> List[str]:
    if StringUtils.isNullOrWhitespace(file_path):
      return []
    path: str = os.path.join(os.getcwd(), file_path)
    if is_full:
      return [os.path.join(path, f) for f in os.listdir(path)]
    return os.listdir(path)

  @staticmethod
  def get_file(file_path: str) -> str:
    if StringUtils.isNullOrWhitespace(file_path):
      return ''
    return os.path.join(os.getcwd(), file_path)

  @staticmethod
  def get_base_name(file_path: str) -> str:
    if StringUtils.isNullOrWhitespace(file_path):
      return ''
    return os.path.basename(file_path)

  @staticmethod
  def get_wo_ext(file_path: str) -> str:
    if StringUtils.isNullOrWhitespace(file_path):
      return ''
    split: Tuple[str] = os.path.splitext(file_path)
    return split[0] if split else ''

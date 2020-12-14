import json
from typing import Any
from app_utils.model_utils import ModelUtils


class StringUtils:

  @staticmethod
  def are_eq(first: str, second: str) -> bool:
    if first is None and second is None:
      return True
    if first is None and second is not None:
      return False
    if first is not None and second is None:
      return False
    return first.lower() == second.lower()

  @staticmethod
  def isNullOrWhitespace(src: str) -> bool:
    return (src is None or src == '' or src.strip() == '')

  @staticmethod
  def to_json(src: Any) -> str:
    if not src:
      return ''
    elif isinstance(src, list):
      return json.dumps(ModelUtils.get_dicts(src))
    else:
      return json.dumps(ModelUtils.get_dict(src))

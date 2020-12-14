import copy
import json
import datetime
import numpy as np
from typing import Any, List, Dict
from decimal import Decimal
from sqlalchemy.inspection import inspect
from alpaca_trade_api.entity import Entity
from app_db import db
from app_utils.number_utils import NumberUtils
from models.response_models.base_response import BaseResponse


class ModelUtils:

  @staticmethod
  def get_dict(item: Any) -> Dict:
    ret: Dict = {}
    if not item:
      return ret
    for key, val in vars(item).items():
      key = key.lstrip('_')
      if isinstance(val, int):
        ret[key] = NumberUtils.to_int(val)
      elif isinstance(val, (Decimal, float)):
        ret[key] = NumberUtils.to_float(val)
      elif isinstance(val, (bool, np.bool_)):
        ret[key] = bool(val)
      elif isinstance(val, (datetime.date, datetime.datetime)):
        ret[key] = val.isoformat()
      elif isinstance(val, list):
        ret[key] = ModelUtils.get_dicts(val)
      elif isinstance(val, Dict):
        ret[key] = val
      elif isinstance(val, db.Model):
        ret[key] = ModelUtils.get_dict(val)
      elif isinstance(val, (BaseResponse, Entity)):
        ret[key] = ModelUtils.get_dict(val)
      else:
        ret[key] = str(val)
    return ret

  @staticmethod
  def get_dicts(items: List[Any]) -> List[Dict]:
    if not items:
      return []
    return [ModelUtils.get_dicts(i) if isinstance(i, list) else ModelUtils.get_dict(i) for i in items]

  @staticmethod
  def get_first_key(src: Dict) -> Any:
    if not src:
      return None
    return next(iter(sorted(src)))

  @staticmethod
  def get_last_key(src: Dict) -> Any:
    if not src:
      return None
    return next(iter(sorted(src, reverse=True)))

  @staticmethod
  def get_obj(item: Any, dict_item: Dict) -> Any:
    if not item or not dict_item:
      return None
    for key, val in dict_item.items():
      setattr(item, key, val)
    return item

  @staticmethod
  def get_copy(item: Any) -> Any:
    if not item:
      return None
    return copy.deepcopy(item)

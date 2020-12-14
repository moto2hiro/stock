import math
from typing import Any


class NumberUtils:

  @staticmethod
  def to_int(src: Any, dflt: int = 0) -> int:
    if not src:
      return dflt
    try:
      ret: int = int(src)
      return ret if not math.isnan(ret) else dflt
    except:
      return dflt

  @staticmethod
  def to_floor(src: Any, dflt: int = 0) -> int:
    if not src:
      return dflt
    try:
      ret: int = math.floor(src)
      return ret if not math.isnan(ret) else dflt
    except:
      return dflt

  @staticmethod
  def to_float(src: Any, dflt: float = 0) -> float:
    if not src:
      return dflt
    try:
      ret: float = float(src)
      return ret if not math.isnan(ret) else dflt
    except:
      return dflt

  @staticmethod
  def round(src: float, decimals: int = 2) -> float:
    return round(src, decimals)

  @staticmethod
  def get_change(current: Any, previous: Any, decimals: int = 2) -> float:
    curr = NumberUtils.to_float(current)
    prev = NumberUtils.to_float(previous)
    if curr == prev:
      return 0
    try:
      return NumberUtils.round((curr - prev) / prev * 100.0, decimals)
    except ZeroDivisionError:
      return None

  @staticmethod
  def has_bit(org_number: int, bit_to_search: int) -> bool:
    return ((org_number | bit_to_search) == org_number)

  @staticmethod
  def add_bit(org_number: int, bit_to_add: int) -> int:
    return (org_number | bit_to_add)

  @staticmethod
  def delete_bit(org_number: int, bit_to_delete: int) -> int:
    if not NumberUtils.has_bit(org_number, bit_to_delete):
      return org_number
    return (org_number ^ bit_to_delete)

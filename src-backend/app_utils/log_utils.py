import inspect
import logging
import os
import sys
import traceback
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from typing import Tuple, List, Any
from app_config import app_config
from app_utils.file_utils import FileUtils
from app_utils.string_utils import StringUtils

handlers: List[Any] = [StreamHandler(sys.stdout)]
if False:  # To-do fix this b/c app_config not working, and can't handle multiple processes (file locks).
  handlers.append(RotatingFileHandler(
      filename='C:\\stock_stuff\\logs\\stock.log',
      maxBytes=100000,
      backupCount=10))

logging.basicConfig(
    handlers=handlers,
    level=logging.DEBUG,
    format='[%(asctime)s.%(msecs)03d] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d,%H:%M:%S')


class LogUtils:

  @staticmethod
  def debug(msg: str) -> None:
    logging.debug(LogUtils.__get_msg(msg))

  @staticmethod
  def info(msg: str) -> None:
    logging.info(LogUtils.__get_msg(msg))

  @staticmethod
  def warning(msg: str) -> None:
    logging.warning(LogUtils.__get_msg(msg))

  @staticmethod
  def error(msg: str, ex: Exception = None) -> None:
    logging.error(traceback.format_exc())
    logging.error(LogUtils.__get_msg(msg))
    if ex:
      logging.error(str(ex))

  @staticmethod
  def __get_msg(msg) -> str:
    file_name, func_name, line_no = LogUtils.__get_caller()
    return '[%s in %s:%i] %s' % (
        file_name,
        func_name,
        line_no,
        msg)

  @staticmethod
  def __get_caller() -> Tuple[str, str, int]:
    frame: FrameType = inspect.currentframe()
    frame = frame.f_back if frame else frame
    caller: Tuple[str, str, int] = ('(unknown file)', '(unknown function)', 0)
    while hasattr(frame, "f_code"):
      co: CodeType = frame.f_code
      if StringUtils.are_eq(co.co_filename, __file__):
        frame = frame.f_back
        continue
      caller = (FileUtils.get_base_name(co.co_filename), co.co_name, frame.f_lineno)
      break
    return caller

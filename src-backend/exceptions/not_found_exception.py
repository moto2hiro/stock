from typing import Any


class NotFoundException(Exception):

  def __init__(self, model: str = '', param: str = '', val: Any = ''):
    msg = '{0}.{1}={2} not found.'.format(model, param, val)
    super().__init__(msg)

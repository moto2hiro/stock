class BadRequestException(Exception):

  def __init__(self, model: str = '', param: str = ''):
    msg: str = 'Bad Request: {0}.{1} is invalid'.format(model, param)
    super().__init__(msg)

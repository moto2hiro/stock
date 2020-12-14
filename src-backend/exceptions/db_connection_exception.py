class DbConnectionException(Exception):

  def __init__(self):
    msg: str = 'Db Connection Error'
    super().__init__(msg)

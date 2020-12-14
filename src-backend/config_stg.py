from typing import List


class ConfigStg:
  DB_USER_NAME: str = 'xxxx'
  DB_PASSWORD: str = 'xxxx'
  DB_HOST: str = 'xxxx'
  DB_SCHEMA: str = 'xxxx'
  SQLALCHEMY_DATABASE_URI: str = 'mysql://{0}:{1}@{2}/{3}?charset=utf8mb4'.format(DB_USER_NAME,
                                                                                  DB_PASSWORD,
                                                                                  DB_HOST,
                                                                                  DB_SCHEMA)
  SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

  # region EMAIL
  DFLT_EMAIL_TO: List[str] = ['xxxx']
  EMAIL_SUBJECT_PREFIX: str = 'STAGE - '
  GMAIL_SERVER: str = 'smtp.gmail.com'
  GMAIL_PORT: int = 465
  GMAIL_USERNAME: str = 'xxxx'
  GMAIL_PW: str = 'xxxx'
  # endregion

  # region ALPACA
  APCA_API_KEY_ID: str = 'xxxx'  # PAPER ACCOUNT
  APCA_API_SECRET_KEY: str = 'xxxx'  # PAPER ACCOUNT
  APCA_API_BASE_URL: str = 'https://paper-api.alpaca.markets'  # Paper Trading URL
  APCA_API_DATA_URL: str = 'https://data.alpaca.markets'  # Data URL
  # endregion

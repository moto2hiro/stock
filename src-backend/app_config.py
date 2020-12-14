import os
from typing import List
from app_consts import AppConsts
from config_prod import ConfigProd
from config_stg import ConfigStg


class AppConfig:

  def __init__(self):
    flask_env: str = os.environ.get('FLASK_ENV', AppConsts.FLASK_ENV_STG)
    is_prod: bool = flask_env == AppConsts.FLASK_ENV_PROD
    self._DB_USER_NAME = ConfigProd.DB_USER_NAME if is_prod else ConfigStg.DB_USER_NAME
    self._DB_PASSWORD = ConfigProd.DB_PASSWORD if is_prod else ConfigStg.DB_PASSWORD
    self._DB_HOST = ConfigProd.DB_HOST if is_prod else ConfigStg.DB_HOST
    self._DB_SCHEMA = ConfigProd.DB_SCHEMA if is_prod else ConfigStg.DB_SCHEMA
    self._SQLALCHEMY_DATABASE_URI = ConfigProd.SQLALCHEMY_DATABASE_URI if is_prod else ConfigStg.SQLALCHEMY_DATABASE_URI
    self._SQLALCHEMY_TRACK_MODIFICATIONS = ConfigProd.SQLALCHEMY_TRACK_MODIFICATIONS if is_prod else ConfigStg.SQLALCHEMY_TRACK_MODIFICATIONS
    self._APCA_API_KEY_ID = ConfigProd.APCA_API_KEY_ID if is_prod else ConfigStg.APCA_API_KEY_ID
    self._APCA_API_SECRET_KEY = ConfigProd.APCA_API_SECRET_KEY if is_prod else ConfigStg.APCA_API_SECRET_KEY
    self._APCA_API_BASE_URL = ConfigProd.APCA_API_BASE_URL if is_prod else ConfigStg.APCA_API_BASE_URL
    self._APCA_API_DATA_URL = ConfigProd.APCA_API_DATA_URL if is_prod else ConfigStg.APCA_API_DATA_URL
    self._DFLT_EMAIL_TO = ConfigProd.DFLT_EMAIL_TO if is_prod else ConfigStg.DFLT_EMAIL_TO
    self._EMAIL_SUBJECT_PREFIX = ConfigProd.EMAIL_SUBJECT_PREFIX if is_prod else ConfigStg.EMAIL_SUBJECT_PREFIX
    self._GMAIL_SERVER = ConfigProd.GMAIL_SERVER if is_prod else ConfigStg.GMAIL_SERVER
    self._GMAIL_PORT = ConfigProd.GMAIL_PORT if is_prod else ConfigStg.GMAIL_PORT
    self._GMAIL_USERNAME = ConfigProd.GMAIL_USERNAME if is_prod else ConfigStg.GMAIL_USERNAME
    self._GMAIL_PW = ConfigProd.GMAIL_PW if is_prod else ConfigStg.GMAIL_PW

  @property
  def DB_USER_NAME(self) -> str: return self._DB_USER_NAME

  @property
  def DB_PASSWORD(self) -> str: return self._DB_PASSWORD

  @property
  def DB_HOST(self) -> str: return self._DB_HOST

  @property
  def DB_SCHEMA(self) -> str: return self._DB_SCHEMA

  @property
  def SQLALCHEMY_DATABASE_URI(self) -> str: return self._SQLALCHEMY_DATABASE_URI

  @property
  def SQLALCHEMY_TRACK_MODIFICATIONS(self) -> str: return self._SQLALCHEMY_TRACK_MODIFICATIONS

  @property
  def DFLT_EMAIL_TO(self) -> List[str]: return self._DFLT_EMAIL_TO

  @property
  def EMAIL_SUBJECT_PREFIX(self) -> str: return self._EMAIL_SUBJECT_PREFIX

  @property
  def GMAIL_SERVER(self) -> str: return self._GMAIL_SERVER

  @property
  def GMAIL_PORT(self) -> int: return self._GMAIL_PORT

  @property
  def GMAIL_USERNAME(self) -> int: return self._GMAIL_USERNAME

  @property
  def GMAIL_PW(self) -> int: return self._GMAIL_PW

  @property
  def APCA_API_KEY_ID(self) -> str: return self._APCA_API_KEY_ID

  @property
  def APCA_API_SECRET_KEY(self) -> str: return self._APCA_API_SECRET_KEY

  @property
  def APCA_API_BASE_URL(self) -> str: return self._APCA_API_BASE_URL

  @property
  def APCA_API_DATA_URL(self) -> str: return self._APCA_API_DATA_URL


app_config: AppConfig = AppConfig()

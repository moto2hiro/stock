from flask import Flask
from flask_testing import TestCase
from app_config import app_config
from app_db import db
from app_utils.log_utils import LogUtils


class TestBase(TestCase):

  def create_app(self):
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object('config_stg.ConfigStg')
    db.init_app(app)
    return app

  @classmethod
  def setUpClass(cls: type) -> None:

    # This runs once.
    if not TestInitObj.is_init:
      LogUtils.debug('START-Unit Tests')
      TestInitObj.init()

    # This runs before each test*.py
    LogUtils.debug('START-Unit Test for {0}'.format(cls.__name__))

  def setUp(self) -> None:

    # This runs before each test method
    self.beforeEach()

  def beforeEach(self) -> None:
    # Override this method to run before each test method
    pass


class TestInitObj(object):
  is_init: bool = False

  @staticmethod
  def init():
    TestInitObj.is_init = True

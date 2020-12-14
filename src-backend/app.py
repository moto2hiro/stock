import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from apis.back_test_api import back_test_api
from apis.import_api import import_api
from apis.stock_api import stock_api
from apis.trade_api import trade_api
from app_consts import AppConsts
from app_db import db
from app_utils.log_utils import LogUtils
from middlewares.error_handler import error_handler
from middlewares.request_handler import request_handler

LogUtils.debug('----- APP START -----')
flask_env: str = os.environ.get('FLASK_ENV', AppConsts.FLASK_ENV_STG)
LogUtils.debug('FLASK_ENV = {0}'.format(flask_env))

app: Flask = Flask(__name__, static_folder=AppConsts.STATIC_FOLDER)
app.config.from_object('config_prod.ConfigProd' if flask_env == AppConsts.FLASK_ENV_PROD else 'config_stg.ConfigStg')
app.register_blueprint(error_handler)
app.register_blueprint(request_handler)
app.register_blueprint(back_test_api, url_prefix=AppConsts.ROUTE_BACK_TEST)
app.register_blueprint(stock_api, url_prefix=AppConsts.ROUTE_STOCK)
app.register_blueprint(import_api, url_prefix=AppConsts.ROUTE_IMPORT)
app.register_blueprint(trade_api, url_prefix=AppConsts.ROUTE_TRADE)
CORS(app)

db.init_app(app)

if __name__ == '__main__':
  app.run(debug=True)

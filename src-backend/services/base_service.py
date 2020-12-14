import mysql.connector
from typing import Any
from app_db import db
from app_utils.log_utils import LogUtils
from app_config import app_config


class BaseService:

  def _get_by_id(db_type: Any, id: int) -> Any:
    return db.session.query(db_type).get(id)

  def _get_first(db_type: Any, predicates: Any) -> Any:
    query = db.session.query(db_type)
    for predicate in predicates:
      query = query.filter(predicate)
    return query.first()

  def _insert(model: Any) -> None:
    db.session.add(model)
    db.session.commit()

  def _update() -> None:
    db.session.commit()

  # region BULK - CAUTION!!
  def _insert_bulk(db_type: Any, models: Any) -> None:
    cols = db_type.__table__.columns.keys()
    cols.remove('id')
    stmt = 'INSERT INTO {0} ({1}) VALUES ({2})'.format(db_type.__tablename__,
                                                       ', '.join(cols),
                                                       ', '.join(['%s' for c in cols]))
    BaseService.__execute_bulk(stmt, models)

  def _truncate(db_type: Any) -> None:
    stmt = 'TRUNCATE TABLE {}'.format(db_type.__tablename__)
    BaseService.__execute_bulk(stmt)

  def __execute_bulk(stmt: str, models: Any = None):
    LogUtils.debug('START')

    try:
      LogUtils.debug(stmt)
      conn = mysql.connector.connect(
          host=app_config.DB_HOST,
          user=app_config.DB_USER_NAME,
          passwd=app_config.DB_PASSWORD,
          database=app_config.DB_SCHEMA
      )
      cur = conn.cursor()
      if models:
        LogUtils.debug('{} records.'.format(len(models)))
        cur.executemany(stmt, models)
      else:
        cur.execute(stmt)
      conn.commit()
    except Exception as e:
      LogUtils.error(e)
    finally:
      if cur:
        cur.close()
      if conn:
        conn.close()

    LogUtils.debug('END')
  # endregion

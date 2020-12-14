from app_db import db
from sqlalchemy import Column


class TradeOrder(db.Model):
  id: Column = db.Column(db.Integer, primary_key=True, nullable=False)
  stock_price_daily_id: Column = db.Column(db.Integer, nullable=False)
  strategy: Column = db.Column(db.String(50), nullable=False)
  alpaca_id: Column = db.Column(db.String(200))
  status: Column = db.Column(db.Integer, nullable=False)
  action: Column = db.Column(db.String(50), nullable=False)
  qty: Column = db.Column(db.Integer, nullable=False)
  order_type: Column = db.Column(db.String(50))
  time_in_force: Column = db.Column(db.String(50))
  target_price: Column = db.Column(db.Numeric(18, 2))
  stop_loss: Column = db.Column(db.Numeric(18, 2))
  created: Column = db.Column(db.DateTime, nullable=False)
  modified: Column = db.Column(db.DateTime, nullable=False)
  exit_stock_price_daily_id: Column = db.Column(db.Integer)
  exit_alpaca_id: Column = db.Column(db.String(200))
  actual_qty: Column = db.Column(db.Integer)
  actual_entry_price: Column = db.Column(db.Numeric(18, 2))
  actual_exit_price: Column = db.Column(db.Numeric(18, 2))

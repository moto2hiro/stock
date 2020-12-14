from app_db import db
from sqlalchemy import Column


class VwSymbolStockPriceDaily(db.Model):
  symbol_id: Column = db.Column(db.Integer, nullable=False)
  symbol: Column = db.Column(db.String(15), nullable=False)
  symbol_name: Column = db.Column(db.String(200), nullable=False)
  status: Column = db.Column(db.Integer, nullable=False)
  instrument: Column = db.Column(db.String(50), nullable=False)
  stock_price_daily_id: Column = db.Column(db.Integer, primary_key=True, nullable=False)
  price_date: Column = db.Column(db.DateTime, nullable=False)
  open_price: Column = db.Column(db.Numeric(18, 2), nullable=False)
  high_price: Column = db.Column(db.Numeric(18, 2), nullable=False)
  low_price: Column = db.Column(db.Numeric(18, 2), nullable=False)
  close_price: Column = db.Column(db.Numeric(18, 2), nullable=False)
  volume: Column = db.Column(db.Integer, nullable=False)

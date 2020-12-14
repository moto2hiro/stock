from app_db import db
from sqlalchemy import Column


class StockPriceDaily(db.Model):
  id: Column = db.Column(db.Integer, primary_key=True, nullable=False)
  symbol_id: Column = db.Column(db.Integer, nullable=False)
  price_date: Column = db.Column(db.DateTime, nullable=False)
  open_price: Column = db.Column(db.Numeric(18, 2), nullable=False)
  high_price: Column = db.Column(db.Numeric(18, 2), nullable=False)
  low_price: Column = db.Column(db.Numeric(18, 2), nullable=False)
  close_price: Column = db.Column(db.Numeric(18, 2), nullable=False)
  volume: Column = db.Column(db.Integer, nullable=False)

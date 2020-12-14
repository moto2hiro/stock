from app_db import db
from sqlalchemy import Column


class SymbolMaster(db.Model):
  id: Column = db.Column(db.Integer, primary_key=True, nullable=False)
  symbol: Column = db.Column(db.String(15), nullable=False)
  name: Column = db.Column(db.String(200), nullable=False)
  status: Column = db.Column(db.Integer, nullable=False)
  instrument: Column = db.Column(db.String(50), nullable=False)
  sector: Column = db.Column(db.String(200))
  industry: Column = db.Column(db.String(200))

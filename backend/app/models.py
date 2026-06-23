from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.database import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="Main Portfolio")
    cash_balance = Column(Float, default=100000.0)
    created_at = Column(DateTime, default=datetime.utcnow)

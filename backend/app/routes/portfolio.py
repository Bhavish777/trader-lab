from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Holding
from app.services.trading import get_or_create_portfolio

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.get("/holdings")
def get_holdings(db: Session = Depends(get_db)):
    return db.query(Holding).all()


@router.get("/cash")
def get_cash_balance(db: Session = Depends(get_db)):
    portfolio = get_or_create_portfolio(db)

    return {"cash_balance": portfolio.cash_balance}

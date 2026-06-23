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


@router.get("/summary")
def get_portfolio_summary(db: Session = Depends(get_db)):
    portfolio = get_or_create_portfolio(db)
    holdings = db.query(Holding).all()

    invested_amount = sum(
        holding.quantity * holding.average_price
        for holding in holdings
    )

    portfolio_value = portfolio.cash_balance + invested_amount

    return {
        "cash_balance": portfolio.cash_balance,
        "invested_amount": invested_amount,
        "portfolio_value": portfolio_value,
        "holdings_count": len(holdings),
    }

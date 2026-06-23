from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Holding, Trade
from app.schemas import (
    CashBalanceResponse,
    HoldingResponse,
    PortfolioResetResponse,
    PortfolioSummaryResponse,
)
from app.services.trading import get_or_create_portfolio

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

STARTING_BALANCE = 100000.0


@router.get("/holdings", response_model=list[HoldingResponse])
def get_holdings(db: Session = Depends(get_db)):
    return db.query(Holding).order_by(Holding.symbol).all()


@router.get("/cash", response_model=CashBalanceResponse)
def get_cash_balance(db: Session = Depends(get_db)):
    portfolio = get_or_create_portfolio(db)

    return {"cash_balance": portfolio.cash_balance}


@router.get("/summary", response_model=PortfolioSummaryResponse)
def get_portfolio_summary(db: Session = Depends(get_db)):
    portfolio = get_or_create_portfolio(db)
    holdings = db.query(Holding).all()

    invested_amount = sum(
        holding.quantity * holding.average_price
        for holding in holdings
    )

    portfolio_value = portfolio.cash_balance + invested_amount
    total_gain_loss = portfolio_value - STARTING_BALANCE
    total_return_percent = (total_gain_loss / STARTING_BALANCE) * 100

    return {
        "starting_balance": STARTING_BALANCE,
        "cash_balance": portfolio.cash_balance,
        "invested_amount": invested_amount,
        "portfolio_value": portfolio_value,
        "total_gain_loss": total_gain_loss,
        "total_return_percent": total_return_percent,
        "holdings_count": len(holdings),
    }


@router.post("/reset", response_model=PortfolioResetResponse)
def reset_portfolio(db: Session = Depends(get_db)):
    portfolio = get_or_create_portfolio(db)

    db.query(Trade).delete()
    db.query(Holding).delete()

    portfolio.cash_balance = STARTING_BALANCE

    db.commit()
    db.refresh(portfolio)

    return {
        "message": "Portfolio reset successfully",
        "cash_balance": portfolio.cash_balance,
    }

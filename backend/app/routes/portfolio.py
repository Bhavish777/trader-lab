from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas import (
    CashBalanceResponse,
    HoldingResponse,
    PortfolioResetResponse,
    PortfolioSummaryResponse,
    PricedHoldingResponse,
)
from app.services.portfolio import (
    calculate_portfolio_summary,
    get_holdings,
    reset_portfolio,
)
from app.services.portfolio_pricing import price_holdings
from app.services.trading import get_or_create_portfolio

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.get("/holdings", response_model=list[HoldingResponse])
def get_portfolio_holdings(db: Session = Depends(get_db)):
    return get_holdings(db)


@router.get("/priced-holdings", response_model=list[PricedHoldingResponse])
def get_priced_portfolio_holdings(db: Session = Depends(get_db)):
    """Return holdings with latest market value and unrealized P&L."""
    holdings = get_holdings(db)

    return price_holdings(holdings)


@router.get("/cash", response_model=CashBalanceResponse)
def get_cash_balance(db: Session = Depends(get_db)):
    portfolio = get_or_create_portfolio(db)

    return {"cash_balance": portfolio.cash_balance}


@router.get("/summary", response_model=PortfolioSummaryResponse)
def get_portfolio_summary(db: Session = Depends(get_db)):
    return calculate_portfolio_summary(db)


@router.post("/reset", response_model=PortfolioResetResponse)
def reset_demo_portfolio(db: Session = Depends(get_db)):
    return reset_portfolio(db)

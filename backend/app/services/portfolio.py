from sqlalchemy.orm import Session

from app.config import STARTING_BALANCE
from app.models import Holding, Trade
from app.services.portfolio_pricing import price_holdings
from app.services.trading import get_or_create_portfolio


def get_holdings(db: Session):
    """Return portfolio holdings sorted by ticker symbol."""
    return db.query(Holding).order_by(Holding.symbol).all()


def calculate_portfolio_summary(db: Session) -> dict:
    """Calculate portfolio value using latest available market prices."""
    portfolio = get_or_create_portfolio(db)
    holdings = db.query(Holding).all()
    priced_holdings = price_holdings(holdings)

    invested_amount = sum(
        holding["invested_amount"]
        for holding in priced_holdings
    )

    market_value = sum(
        holding["market_value"]
        for holding in priced_holdings
    )

    portfolio_value = portfolio.cash_balance + market_value
    total_gain_loss = portfolio_value - STARTING_BALANCE
    total_return_percent = (total_gain_loss / STARTING_BALANCE) * 100

    return {
        "starting_balance": STARTING_BALANCE,
        "cash_balance": round(portfolio.cash_balance, 2),
        "invested_amount": round(invested_amount, 2),
        "portfolio_value": round(portfolio_value, 2),
        "total_gain_loss": round(total_gain_loss, 2),
        "total_return_percent": round(total_return_percent, 2),
        "holdings_count": len(holdings),
    }


def reset_portfolio(db: Session) -> dict:
    """Reset the demo portfolio back to its starting state."""
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

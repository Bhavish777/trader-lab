from sqlalchemy.orm import Session

from app.models import Holding, Trade
from app.services.trading import get_or_create_portfolio

STARTING_BALANCE = 100000.0


def get_holdings(db: Session):
    return db.query(Holding).order_by(Holding.symbol).all()


def calculate_portfolio_summary(db: Session) -> dict:
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


def reset_portfolio(db: Session) -> dict:
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

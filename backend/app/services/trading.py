from sqlalchemy.orm import Session

from app.models import Portfolio


def get_or_create_portfolio(db: Session) -> Portfolio:
    portfolio = db.query(Portfolio).first()

    if portfolio:
        return portfolio

    portfolio = Portfolio()
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)

    return portfolio

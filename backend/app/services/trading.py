from sqlalchemy.orm import Session

from app.models import Holding, Portfolio, Trade


def clean_symbol(symbol: str) -> str:
    """Normalize stock symbols before storing or searching them."""
    return symbol.strip().upper()


def get_or_create_portfolio(db: Session) -> Portfolio:
    """Return the main demo portfolio, or create it if it does not exist."""
    portfolio = db.query(Portfolio).first()

    if portfolio:
        return portfolio

    portfolio = Portfolio()
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)

    return portfolio


def buy_stock(db: Session, symbol: str, quantity: int, price: float) -> Trade:
    """Buy a stock using virtual cash and update the user's holding."""
    symbol = clean_symbol(symbol)
    portfolio = get_or_create_portfolio(db)
    total_cost = quantity * price

    if total_cost > portfolio.cash_balance:
        raise ValueError("Not enough cash to complete this trade")

    holding = db.query(Holding).filter(Holding.symbol == symbol).first()

    if holding:
        old_value = holding.quantity * holding.average_price
        new_value = quantity * price
        new_quantity = holding.quantity + quantity

        holding.average_price = (old_value + new_value) / new_quantity
        holding.quantity = new_quantity
    else:
        holding = Holding(
            symbol=symbol,
            quantity=quantity,
            average_price=price,
        )
        db.add(holding)

    trade = Trade(
        symbol=symbol,
        trade_type="BUY",
        quantity=quantity,
        price=price,
    )

    portfolio.cash_balance -= total_cost

    db.add(trade)
    db.commit()
    db.refresh(trade)

    return trade


def sell_stock(db: Session, symbol: str, quantity: int, price: float) -> Trade:
    """Sell owned shares, update cash, and reduce or remove the holding."""
    symbol = clean_symbol(symbol)
    portfolio = get_or_create_portfolio(db)
    holding = db.query(Holding).filter(Holding.symbol == symbol).first()

    if not holding:
        raise ValueError("You do not own this stock")

    if quantity > holding.quantity:
        raise ValueError("Not enough shares to sell")

    trade = Trade(
        symbol=symbol,
        trade_type="SELL",
        quantity=quantity,
        price=price,
    )

    holding.quantity -= quantity
    portfolio.cash_balance += quantity * price

    if holding.quantity == 0:
        db.delete(holding)

    db.add(trade)
    db.commit()
    db.refresh(trade)

    return trade

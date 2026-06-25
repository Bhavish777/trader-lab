from app.config import DEFAULT_CURRENCY, STARTING_BALANCE
from app.models import Holding, Portfolio, Trade
from app.services.symbol_resolver import get_symbol_currency


def clean_symbol(symbol: str) -> str:
    """Normalize ticker symbols before saving trades."""
    return symbol.strip().upper()


def validate_trade_currency(symbol: str):
    """Prevent non-USD market prices from changing the USD demo portfolio."""
    currency = get_symbol_currency(symbol)

    if currency != DEFAULT_CURRENCY:
        raise ValueError(
            f"{symbol} trades in {currency}, but this demo portfolio is a "
            f"{DEFAULT_CURRENCY} portfolio. Multi-currency trading is coming later."
        )


def get_or_create_portfolio(db):
    """Return the demo portfolio, creating it if it does not exist yet."""
    portfolio = db.query(Portfolio).first()

    if portfolio is None:
        portfolio = Portfolio(
            name="Main Portfolio",
            cash_balance=STARTING_BALANCE,
            currency=DEFAULT_CURRENCY,
        )
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)

    return portfolio


def buy_stock(db, trade):
    """Buy shares if the portfolio has enough cash and currency is supported."""
    symbol = clean_symbol(trade.symbol)
    validate_trade_currency(symbol)

    portfolio = get_or_create_portfolio(db)
    total_cost = trade.quantity * trade.price

    if total_cost > portfolio.cash_balance:
        raise ValueError("Not enough cash to complete this trade")

    holding = db.query(Holding).filter(Holding.symbol == symbol).first()

    if holding:
        current_invested_amount = holding.quantity * holding.average_price
        new_invested_amount = trade.quantity * trade.price
        new_quantity = holding.quantity + trade.quantity

        holding.quantity = new_quantity
        holding.average_price = (
            current_invested_amount + new_invested_amount
        ) / new_quantity
    else:
        holding = Holding(
            symbol=symbol,
            quantity=trade.quantity,
            average_price=trade.price,
        )
        db.add(holding)

    portfolio.cash_balance -= total_cost

    trade_record = Trade(
        symbol=symbol,
        trade_type="buy",
        quantity=trade.quantity,
        price=trade.price,
    )

    db.add(trade_record)
    db.commit()
    db.refresh(trade_record)

    return trade_record


def sell_stock(db, trade):
    """Sell shares if the position exists and currency is supported."""
    symbol = clean_symbol(trade.symbol)
    validate_trade_currency(symbol)

    portfolio = get_or_create_portfolio(db)
    holding = db.query(Holding).filter(Holding.symbol == symbol).first()

    if holding is None:
        raise ValueError("You do not own this stock")

    if trade.quantity > holding.quantity:
        raise ValueError("You cannot sell more shares than you own")

    total_sale_value = trade.quantity * trade.price

    holding.quantity -= trade.quantity
    portfolio.cash_balance += total_sale_value

    if holding.quantity == 0:
        db.delete(holding)

    trade_record = Trade(
        symbol=symbol,
        trade_type="sell",
        quantity=trade.quantity,
        price=trade.price,
    )

    db.add(trade_record)
    db.commit()
    db.refresh(trade_record)

    return trade_record

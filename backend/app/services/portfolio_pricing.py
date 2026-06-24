from app.models import Holding
from app.services.market_data import get_latest_quote


def calculate_unrealized_return(
    unrealized_gain_loss: float,
    invested_amount: float,
) -> float:
    """Calculate unrealized return percentage for a holding."""
    if invested_amount == 0:
        return 0.0

    return round((unrealized_gain_loss / invested_amount) * 100, 2)


def price_holding(holding: Holding) -> dict:
    """Attach latest market price and unrealized P&L to one holding."""
    quote = get_latest_quote(holding.symbol)

    invested_amount = holding.quantity * holding.average_price
    current_price = quote["price"]
    market_value = holding.quantity * current_price
    unrealized_gain_loss = market_value - invested_amount

    return {
        "symbol": holding.symbol,
        "quantity": holding.quantity,
        "average_price": holding.average_price,
        "invested_amount": round(invested_amount, 2),
        "current_price": current_price,
        "market_value": round(market_value, 2),
        "unrealized_gain_loss": round(unrealized_gain_loss, 2),
        "unrealized_return_percent": calculate_unrealized_return(
            unrealized_gain_loss,
            invested_amount,
        ),
        "price_source": quote["source"],
    }


def price_holdings(holdings: list[Holding]) -> list[dict]:
    """Price all holdings in a portfolio."""
    return [price_holding(holding) for holding in holdings]

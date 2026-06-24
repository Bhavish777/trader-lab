from app.models import Holding
from app.services.portfolio_pricing import (
    calculate_unrealized_return,
    price_holding,
)


def test_calculate_unrealized_return():
    result = calculate_unrealized_return(
        unrealized_gain_loss=25.0,
        invested_amount=100.0,
    )

    assert result == 25.0


def test_calculate_unrealized_return_with_zero_investment():
    result = calculate_unrealized_return(
        unrealized_gain_loss=25.0,
        invested_amount=0.0,
    )

    assert result == 0.0


def test_price_holding_with_market_quote(monkeypatch):
    def fake_quote(symbol: str):
        return {
            "symbol": symbol,
            "price": 150.0,
            "currency": "USD",
            "source": "test",
            "last_updated": "2026-06-23T00:00:00",
        }

    monkeypatch.setattr(
        "app.services.portfolio_pricing.get_latest_quote",
        fake_quote,
    )

    holding = Holding(
        symbol="AAPL",
        quantity=2,
        average_price=100.0,
    )

    result = price_holding(holding)

    assert result["symbol"] == "AAPL"
    assert result["quantity"] == 2
    assert result["average_price"] == 100.0
    assert result["invested_amount"] == 200.0
    assert result["current_price"] == 150.0
    assert result["market_value"] == 300.0
    assert result["unrealized_gain_loss"] == 100.0
    assert result["unrealized_return_percent"] == 50.0
    assert result["price_source"] == "test"


def test_price_holding_uses_fallback_when_quote_fails(monkeypatch):
    def fake_quote_failure(symbol: str):
        raise ValueError("No market data found for this symbol")

    monkeypatch.setattr(
        "app.services.portfolio_pricing.get_latest_quote",
        fake_quote_failure,
    )

    holding = Holding(
        symbol="FAKE",
        quantity=3,
        average_price=80.0,
    )

    result = price_holding(holding)

    assert result["symbol"] == "FAKE"
    assert result["quantity"] == 3
    assert result["average_price"] == 80.0
    assert result["invested_amount"] == 240.0
    assert result["current_price"] == 80.0
    assert result["market_value"] == 240.0
    assert result["unrealized_gain_loss"] == 0.0
    assert result["unrealized_return_percent"] == 0.0
    assert result["price_source"] == "fallback"

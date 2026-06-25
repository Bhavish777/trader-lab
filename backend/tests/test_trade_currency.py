from fastapi.testclient import TestClient

from app.main import app
from app.services.symbol_resolver import get_symbol_currency

client = TestClient(app)


def test_symbol_currency_defaults_to_usd():
    assert get_symbol_currency("AAPL") == "USD"


def test_symbol_currency_detects_indian_stocks():
    assert get_symbol_currency("HDFCBANK.NS") == "INR"


def test_symbol_currency_detects_canadian_stocks():
    assert get_symbol_currency("SHOP.TO") == "CAD"


def test_buy_rejects_non_usd_stock():
    response = client.post(
        "/trades/buy",
        json={"symbol": "HDFCBANK.NS", "quantity": 1, "price": 1500},
    )

    assert response.status_code == 400
    assert "USD portfolio" in response.json()["detail"]

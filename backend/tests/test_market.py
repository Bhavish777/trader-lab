from fastapi.testclient import TestClient

from app.main import app
from app.services.market_data import clean_market_symbol
from app.services.symbol_resolver import search_symbols

client = TestClient(app)


def symbols_from(results):
    return [stock["symbol"] for stock in results]


def test_clean_market_symbol():
    assert clean_market_symbol(" aapl ") == "AAPL"


def test_symbol_search_finds_company_name():
    results = search_symbols("apple")
    symbols = symbols_from(results)

    assert "AAPL" in symbols
    assert results[0]["symbol"] == "AAPL"


def test_symbol_search_finds_indian_stock():
    results = search_symbols("reliance")
    symbols = symbols_from(results)

    assert "RELIANCE.NS" in symbols


def test_symbol_search_country_filter():
    results = search_symbols("shopify", country="Canada")
    symbols = symbols_from(results)

    assert "SHOP.TO" in symbols
    assert all(stock["country"] == "Canada" for stock in results)


def test_market_search_endpoint():
    response = client.get("/market/search?query=tesla")

    assert response.status_code == 200

    data = response.json()
    symbols = symbols_from(data)

    assert "TSLA" in symbols


def test_market_quote_endpoint_with_mock(monkeypatch):
    def fake_quote(symbol: str):
        return {
            "symbol": symbol,
            "price": 250.0,
            "currency": "USD",
            "source": "test",
            "last_updated": "2026-06-23T00:00:00",
        }

    monkeypatch.setattr("app.routes.market.get_latest_quote", fake_quote)

    response = client.get("/market/quote/AAPL")

    assert response.status_code == 200

    data = response.json()

    assert data["symbol"] == "AAPL"
    assert data["price"] == 250.0
    assert data["source"] == "test"


def test_market_quote_endpoint_not_found(monkeypatch):
    def fake_quote_failure(symbol: str):
        raise ValueError("No market data found for this symbol")

    monkeypatch.setattr("app.routes.market.get_latest_quote", fake_quote_failure)

    response = client.get("/market/quote/FAKE")

    assert response.status_code == 404

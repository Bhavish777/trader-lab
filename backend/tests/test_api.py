from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Trader Lab API is running"}


def test_basic_trading_flow(monkeypatch):
    def fake_price_holdings(holdings):
        return [
            {
                "symbol": "AAPL",
                "quantity": 1,
                "average_price": 100.0,
                "invested_amount": 100.0,
                "current_price": 120.0,
                "market_value": 120.0,
                "unrealized_gain_loss": 20.0,
                "unrealized_return_percent": 20.0,
                "price_source": "test",
            }
        ]

    monkeypatch.setattr("app.services.portfolio.price_holdings", fake_price_holdings)

    reset_response = client.post("/portfolio/reset")
    assert reset_response.status_code == 200
    assert reset_response.json()["cash_balance"] == 100000.0

    buy_response = client.post(
        "/trades/buy",
        json={
            "symbol": "AAPL",
            "quantity": 2,
            "price": 100,
        },
    )

    assert buy_response.status_code == 200

    buy_data = buy_response.json()
    assert buy_data["symbol"] == "AAPL"
    assert buy_data["trade_type"] == "BUY"
    assert buy_data["quantity"] == 2
    assert buy_data["price"] == 100.0
    assert buy_data["total_value"] == 200.0

    sell_response = client.post(
        "/trades/sell",
        json={
            "symbol": "AAPL",
            "quantity": 1,
            "price": 120,
        },
    )

    assert sell_response.status_code == 200

    sell_data = sell_response.json()
    assert sell_data["symbol"] == "AAPL"
    assert sell_data["trade_type"] == "SELL"
    assert sell_data["quantity"] == 1
    assert sell_data["price"] == 120.0
    assert sell_data["total_value"] == 120.0

    holdings_response = client.get("/portfolio/holdings")
    assert holdings_response.status_code == 200

    holdings = holdings_response.json()
    assert len(holdings) == 1
    assert holdings[0]["symbol"] == "AAPL"
    assert holdings[0]["quantity"] == 1
    assert holdings[0]["average_price"] == 100.0
    assert holdings[0]["invested_amount"] == 100.0

    summary_response = client.get("/portfolio/summary")
    assert summary_response.status_code == 200

    summary = summary_response.json()
    assert summary["starting_balance"] == 100000.0
    assert summary["cash_balance"] == 99920.0
    assert summary["invested_amount"] == 100.0
    assert summary["portfolio_value"] == 100040.0
    assert summary["total_gain_loss"] == 40.0
    assert summary["total_return_percent"] == 0.04
    assert summary["holdings_count"] == 1

    trades_response = client.get("/trades")
    assert trades_response.status_code == 200

    trades = trades_response.json()
    assert len(trades) == 2
    assert trades[0]["trade_type"] == "SELL"
    assert trades[1]["trade_type"] == "BUY"


def test_cannot_buy_without_enough_cash():
    client.post("/portfolio/reset")

    response = client.post(
        "/trades/buy",
        json={
            "symbol": "TSLA",
            "quantity": 1000,
            "price": 1000,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough cash to complete this trade"


def test_cannot_sell_stock_not_owned():
    client.post("/portfolio/reset")

    response = client.post(
        "/trades/sell",
        json={
            "symbol": "MSFT",
            "quantity": 1,
            "price": 300,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "You do not own this stock"


def test_cannot_sell_more_than_owned():
    client.post("/portfolio/reset")

    client.post(
        "/trades/buy",
        json={
            "symbol": "NVDA",
            "quantity": 2,
            "price": 100,
        },
    )

    response = client.post(
        "/trades/sell",
        json={
            "symbol": "NVDA",
            "quantity": 5,
            "price": 120,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough shares to sell"


def test_invalid_trade_quantity_is_rejected():
    response = client.post(
        "/trades/buy",
        json={
            "symbol": "AAPL",
            "quantity": 0,
            "price": 100,
        },
    )

    assert response.status_code == 422

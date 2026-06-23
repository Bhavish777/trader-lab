from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Trader Lab API is running"}


def test_basic_trading_flow():
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
    assert summary["portfolio_value"] == 100020.0
    assert summary["total_gain_loss"] == 20.0
    assert summary["total_return_percent"] == 0.02
    assert summary["holdings_count"] == 1

    trades_response = client.get("/trades")
    assert trades_response.status_code == 200

    trades = trades_response.json()
    assert len(trades) == 2
    assert trades[0]["trade_type"] == "SELL"
    assert trades[1]["trade_type"] == "BUY"

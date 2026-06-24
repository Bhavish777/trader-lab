import yfinance as yf


def clean_market_symbol(symbol: str) -> str:
    """Normalize ticker symbols before requesting market data."""
    return symbol.strip().upper()


def get_latest_quote(symbol: str) -> dict:
    """Fetch the latest available closing price for a stock symbol."""
    symbol = clean_market_symbol(symbol)
    ticker = yf.Ticker(symbol)

    # Use a few days because markets may be closed on weekends or holidays.
    history = ticker.history(period="5d", interval="1d")

    if history.empty:
        raise ValueError("No market data found for this symbol")

    latest_row = history.iloc[-1]
    latest_date = history.index[-1]

    try:
        currency = ticker.fast_info.get("currency") or "USD"
    except Exception:
        currency = "USD"

    return {
        "symbol": symbol,
        "price": round(float(latest_row["Close"]), 2),
        "currency": currency,
        "source": "yfinance",
        "last_updated": latest_date.isoformat(),
    }

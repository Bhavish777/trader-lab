from datetime import datetime, timedelta, timezone

import yfinance as yf

QUOTE_CACHE = {}
CACHE_TTL_SECONDS = 300


def clean_market_symbol(symbol: str) -> str:
    """Normalize ticker symbols before requesting market data."""
    return symbol.strip().upper()


def _is_cache_fresh(cached_quote: dict) -> bool:
    """Check whether a cached quote is still recent enough to reuse."""
    cached_at = cached_quote["cached_at"]
    expires_at = cached_at + timedelta(seconds=CACHE_TTL_SECONDS)

    return datetime.now(timezone.utc) < expires_at


def get_latest_quote(symbol: str) -> dict:
    """Fetch the latest available closing price, using cache when possible."""
    symbol = clean_market_symbol(symbol)

    cached_quote = QUOTE_CACHE.get(symbol)

    if cached_quote and _is_cache_fresh(cached_quote):
        return cached_quote["data"]

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

    quote = {
        "symbol": symbol,
        "price": round(float(latest_row["Close"]), 2),
        "currency": currency,
        "source": "yfinance",
        "last_updated": latest_date.isoformat(),
    }

    QUOTE_CACHE[symbol] = {
        "data": quote,
        "cached_at": datetime.now(timezone.utc),
    }

    return quote

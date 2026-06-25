import csv
import re
from functools import lru_cache
from pathlib import Path

from rapidfuzz import fuzz

STOCK_UNIVERSE_PATH = Path(__file__).resolve().parents[1] / "data" / "stocks.csv"

LOCAL_FALLBACK_STOCKS = [
    {
        "symbol": "SHOP.TO",
        "name": "Shopify Inc",
        "exchange": "TSX",
        "country": "Canada",
        "currency": "CAD",
    },
    {
        "symbol": "RY.TO",
        "name": "Royal Bank of Canada",
        "exchange": "TSX",
        "country": "Canada",
        "currency": "CAD",
    },
    {
        "symbol": "TD.TO",
        "name": "Toronto-Dominion Bank",
        "exchange": "TSX",
        "country": "Canada",
        "currency": "CAD",
    },
    {
        "symbol": "HDFCBANK.NS",
        "name": "HDFC Bank",
        "exchange": "NSE",
        "country": "India",
        "currency": "INR",
    },
    {
        "symbol": "ICICIBANK.NS",
        "name": "ICICI Bank",
        "exchange": "NSE",
        "country": "India",
        "currency": "INR",
    },
    {
        "symbol": "RELIANCE.NS",
        "name": "Reliance Industries",
        "exchange": "NSE",
        "country": "India",
        "currency": "INR",
    },
]

# Real search engines use popularity signals. We keep a tiny boost list so very
# common symbols rank above obscure companies with similar names.
POPULAR_SYMBOL_RANK = {
    "AAPL": 100,
    "MSFT": 96,
    "TSLA": 94,
    "NVDA": 92,
    "GOOGL": 90,
    "AMZN": 88,
    "META": 86,
    "RELIANCE.NS": 84,
    "HDFCBANK.NS": 82,
    "ICICIBANK.NS": 80,
    "SHOP": 70,
    "SHOP.TO": 68,
}


def normalize_query(value: str) -> str:
    """Normalize user search text for forgiving matching."""
    return re.sub(r"[^a-z0-9]", "", value.lower())


def tokenize(value: str) -> list[str]:
    """Split text into searchable words."""
    return [token for token in re.split(r"[^a-zA-Z0-9]+", value.lower()) if token]


def base_symbol(symbol: str) -> str:
    """Remove exchange suffixes so HDFCBANK.NS can also match HDFCBANK."""
    return symbol.split(".")[0]


def add_fallback_stocks(stocks: list[dict]) -> list[dict]:
    """Guarantee key demo symbols exist even if a source omits an exchange."""
    by_symbol = {stock["symbol"]: stock for stock in stocks}

    for stock in LOCAL_FALLBACK_STOCKS:
        by_symbol.setdefault(stock["symbol"], stock)

    return list(by_symbol.values())


@lru_cache(maxsize=1)
def load_stock_universe() -> list[dict]:
    """Load searchable stocks from the generated stock universe CSV."""
    if not STOCK_UNIVERSE_PATH.exists():
        return add_fallback_stocks([])

    with STOCK_UNIVERSE_PATH.open(newline="", encoding="utf-8") as csv_file:
        stocks = list(csv.DictReader(csv_file))

    return add_fallback_stocks(stocks)


def build_search_text(stock: dict) -> str:
    """Combine fields that should be searchable."""
    return " ".join(
        [
            stock["symbol"],
            base_symbol(stock["symbol"]),
            stock["name"],
            stock["exchange"],
            stock["country"],
        ]
    )


def token_similarity(query: str, stock: dict) -> int:
    """Find close typo matches against symbol and company-name tokens."""
    normalized_query = normalize_query(query)

    tokens = [
        normalize_query(base_symbol(stock["symbol"])),
        *[normalize_query(token) for token in tokenize(stock["name"])],
    ]

    best_score = 0

    for token in tokens:
        if not token:
            continue

        if token.startswith(normalized_query):
            best_score = max(best_score, 96)

        if normalized_query in token:
            best_score = max(best_score, 91)

        typo_score = fuzz.ratio(normalized_query, token)

        # Avoid very short unrelated ticker symbols beating real typo matches.
        if len(token) >= len(normalized_query):
            best_score = max(best_score, int(typo_score))

    return best_score


def score_stock(query: str, stock: dict) -> int:
    """Score how closely a stock matches the user's query."""
    normalized_query = normalize_query(query)

    symbol = normalize_query(stock["symbol"])
    base = normalize_query(base_symbol(stock["symbol"]))
    name = normalize_query(stock["name"])
    name_tokens = tokenize(stock["name"])

    if normalized_query in {symbol, base}:
        return 110

    if symbol.startswith(normalized_query) or base.startswith(normalized_query):
        return 105

    # Example: "apple" should rank Apple Inc above Apple Hospitality REIT.
    if name_tokens and normalize_query(name_tokens[0]) == normalized_query:
        if len(name_tokens) <= 2:
            return 102
        return 99

    if name.startswith(normalized_query):
        return 98

    if normalized_query in name:
        return 94

    token_score = token_similarity(query, stock)

    if token_score >= 84:
        return token_score + 5

    search_text = normalize_query(build_search_text(stock))

    if normalized_query in search_text:
        return 88

    fuzzy_score = fuzz.WRatio(normalized_query, search_text)

    return int(fuzzy_score)


def search_symbols(query: str, country: str | None = None, limit: int = 10) -> list[dict]:
    """Search stocks by ticker, company name, country, exchange, or close typo."""
    normalized_query = normalize_query(query)

    if not normalized_query:
        return []

    stocks = load_stock_universe()

    if country:
        normalized_country = normalize_query(country)
        stocks = [
            stock
            for stock in stocks
            if normalized_country in normalize_query(stock["country"])
        ]

    scored_results = []

    for stock in stocks:
        score = score_stock(query, stock)

        # Short searches like "hdf", "sbi", "tesl", or "icci" need lower cutoff.
        threshold = 55 if len(normalized_query) <= 4 else 65

        if score >= threshold:
            scored_results.append((score, stock))

    scored_results.sort(
        key=lambda item: (
            item[0],
            POPULAR_SYMBOL_RANK.get(item[1]["symbol"], 0),
            -len(item[1]["name"]),
            item[1]["symbol"],
        ),
        reverse=True,
    )

    return [stock for _, stock in scored_results[:limit]]


def get_symbol_currency(symbol: str) -> str:
    """Return the trading currency for a symbol when known."""
    normalized_symbol = symbol.strip().upper()

    for stock in load_stock_universe():
        if stock["symbol"].upper() == normalized_symbol:
            return stock["currency"]

    if normalized_symbol.endswith(".NS"):
        return "INR"

    if normalized_symbol.endswith(".TO"):
        return "CAD"

    return "USD"

STOCK_DIRECTORY = [
    {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "exchange": "NASDAQ",
        "country": "United States",
        "currency": "USD",
        "aliases": ["apple", "iphone", "mac"],
    },
    {
        "symbol": "TSLA",
        "name": "Tesla Inc.",
        "exchange": "NASDAQ",
        "country": "United States",
        "currency": "USD",
        "aliases": ["tesla", "elon"],
    },
    {
        "symbol": "MSFT",
        "name": "Microsoft Corporation",
        "exchange": "NASDAQ",
        "country": "United States",
        "currency": "USD",
        "aliases": ["microsoft", "windows", "xbox"],
    },
    {
        "symbol": "GOOGL",
        "name": "Alphabet Inc.",
        "exchange": "NASDAQ",
        "country": "United States",
        "currency": "USD",
        "aliases": ["google", "alphabet", "youtube"],
    },
    {
        "symbol": "AMZN",
        "name": "Amazon.com Inc.",
        "exchange": "NASDAQ",
        "country": "United States",
        "currency": "USD",
        "aliases": ["amazon", "aws"],
    },
    {
        "symbol": "NVDA",
        "name": "NVIDIA Corporation",
        "exchange": "NASDAQ",
        "country": "United States",
        "currency": "USD",
        "aliases": ["nvidia", "nvda", "gpu"],
    },
    {
        "symbol": "META",
        "name": "Meta Platforms Inc.",
        "exchange": "NASDAQ",
        "country": "United States",
        "currency": "USD",
        "aliases": ["meta", "facebook", "instagram"],
    },
    {
        "symbol": "RELIANCE.NS",
        "name": "Reliance Industries Limited",
        "exchange": "NSE",
        "country": "India",
        "currency": "INR",
        "aliases": ["reliance", "jio"],
    },
    {
        "symbol": "TCS.NS",
        "name": "Tata Consultancy Services",
        "exchange": "NSE",
        "country": "India",
        "currency": "INR",
        "aliases": ["tcs", "tata consultancy", "tata"],
    },
    {
        "symbol": "SHOP",
        "name": "Shopify Inc.",
        "exchange": "NYSE",
        "country": "United States",
        "currency": "USD",
        "aliases": ["shopify", "shop"],
    },
    {
        "symbol": "SHOP.TO",
        "name": "Shopify Inc.",
        "exchange": "TSX",
        "country": "Canada",
        "currency": "CAD",
        "aliases": ["shopify canada", "shopify"],
    },
]


def normalize_query(query: str) -> str:
    """Clean user search text before matching company names or tickers."""
    return query.strip().lower()


def search_symbols(query: str, country: str | None = None) -> list[dict]:
    """Return stock matches for a user-friendly company search."""
    query = normalize_query(query)

    if not query:
        return []

    results = []

    for stock in STOCK_DIRECTORY:
        searchable_values = [
            stock["symbol"].lower(),
            stock["name"].lower(),
            *stock["aliases"],
        ]

        has_match = any(query in value for value in searchable_values)

        if country:
            has_match = has_match and stock["country"].lower() == country.lower()

        if has_match:
            results.append(
                {
                    "symbol": stock["symbol"],
                    "name": stock["name"],
                    "exchange": stock["exchange"],
                    "country": stock["country"],
                    "currency": stock["currency"],
                }
            )

    return results

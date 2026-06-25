from app.services.symbol_resolver import load_stock_universe, search_symbols


def symbols_from(results):
    return [stock["symbol"] for stock in results]


def test_stock_universe_is_generated():
    stocks = load_stock_universe()

    assert len(stocks) > 1000


def test_search_finds_apple_by_company_name():
    results = search_symbols("apple")

    assert "AAPL" in symbols_from(results)


def test_search_handles_tesla_typo():
    results = search_symbols("tesl")

    assert "TSLA" in symbols_from(results)


def test_search_finds_hdfc_or_indian_fallback():
    results = search_symbols("hdfc")

    assert "HDFCBANK.NS" in symbols_from(results)


def test_search_handles_typo_for_icici():
    results = search_symbols("icci")

    assert "ICICIBANK.NS" in symbols_from(results)


def test_search_handles_typo_for_reliance():
    results = search_symbols("relaince")

    assert "RELIANCE.NS" in symbols_from(results)


def test_search_can_filter_by_country():
    results = search_symbols("shopify", country="United States")
    symbols = symbols_from(results)

    assert "SHOP" in symbols
    assert "SHOP.TO" not in symbols

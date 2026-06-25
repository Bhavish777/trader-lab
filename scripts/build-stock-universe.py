import csv
import io
import ssl
import urllib.request
from pathlib import Path

import certifi

OUTPUT_PATH = Path("backend/app/data/stocks.csv")

NASDAQ_LISTED_URL = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"
OTHER_LISTED_URL = "https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt"
NSE_EQUITY_URL = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"


FALLBACK_INDIA_STOCKS = [
    ("RELIANCE.NS", "Reliance Industries", "NSE", "India", "INR"),
    ("TCS.NS", "Tata Consultancy Services", "NSE", "India", "INR"),
    ("INFY.NS", "Infosys", "NSE", "India", "INR"),
    ("HDFCBANK.NS", "HDFC Bank", "NSE", "India", "INR"),
    ("ICICIBANK.NS", "ICICI Bank", "NSE", "India", "INR"),
    ("SBIN.NS", "State Bank of India", "NSE", "India", "INR"),
    ("AXISBANK.NS", "Axis Bank", "NSE", "India", "INR"),
    ("KOTAKBANK.NS", "Kotak Mahindra Bank", "NSE", "India", "INR"),
    ("LT.NS", "Larsen and Toubro", "NSE", "India", "INR"),
    ("WIPRO.NS", "Wipro", "NSE", "India", "INR"),
    ("TATAMOTORS.NS", "Tata Motors", "NSE", "India", "INR"),
    ("TATASTEEL.NS", "Tata Steel", "NSE", "India", "INR"),
    ("MARUTI.NS", "Maruti Suzuki India", "NSE", "India", "INR"),
    ("SUNPHARMA.NS", "Sun Pharmaceutical Industries", "NSE", "India", "INR"),
    ("BAJFINANCE.NS", "Bajaj Finance", "NSE", "India", "INR"),
    ("BHARTIARTL.NS", "Bharti Airtel", "NSE", "India", "INR"),
    ("ITC.NS", "ITC Limited", "NSE", "India", "INR"),
]


def download_text(url: str) -> str:
    """Download source text with a browser-like user agent."""
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/csv,text/plain,*/*",
        },
    )

    ssl_context = ssl.create_default_context(cafile=certifi.where())

    with urllib.request.urlopen(request, timeout=20, context=ssl_context) as response:
        return response.read().decode("utf-8", errors="replace")


def clean_security_name(name: str) -> str:
    """Remove common listing suffix noise from company/security names."""
    cleaned = name.strip()

    noisy_parts = [
        " - Common Stock",
        " Common Stock",
        " Ordinary Shares",
        " Class A",
        " Class B",
    ]

    for part in noisy_parts:
        cleaned = cleaned.replace(part, "")

    return cleaned.strip()


def is_valid_symbol(symbol: str) -> bool:
    """Skip symbols that yfinance usually cannot use cleanly."""
    if not symbol:
        return False

    ignored_markers = ["$", "^", "/"]

    return not any(marker in symbol for marker in ignored_markers)


def add_stock(stocks: dict, symbol: str, name: str, exchange: str, country: str, currency: str):
    """Add one stock if it has enough useful information."""
    symbol = symbol.strip().upper()
    name = clean_security_name(name)

    if not is_valid_symbol(symbol) or not name:
        return

    stocks[symbol] = {
        "symbol": symbol,
        "name": name,
        "exchange": exchange,
        "country": country,
        "currency": currency,
    }


def load_nasdaq_listed(stocks: dict):
    """Load Nasdaq-listed securities from Nasdaq Trader."""
    text = download_text(NASDAQ_LISTED_URL)

    for row in csv.DictReader(io.StringIO(text), delimiter="|"):
        symbol = row.get("Symbol", "")
        name = row.get("Security Name", "")
        test_issue = row.get("Test Issue", "")

        if symbol == "File Creation Time" or test_issue == "Y":
            continue

        add_stock(stocks, symbol, name, "NASDAQ", "United States", "USD")


def load_other_us_listed(stocks: dict):
    """Load other U.S. exchange-listed securities from Nasdaq Trader."""
    text = download_text(OTHER_LISTED_URL)

    exchange_names = {
        "A": "NYSE American",
        "N": "NYSE",
        "P": "NYSE Arca",
        "Z": "Cboe BZX",
        "V": "IEX",
    }

    for row in csv.DictReader(io.StringIO(text), delimiter="|"):
        symbol = row.get("ACT Symbol", "")
        name = row.get("Security Name", "")
        exchange_code = row.get("Exchange", "")
        test_issue = row.get("Test Issue", "")

        if symbol == "File Creation Time" or test_issue == "Y":
            continue

        exchange = exchange_names.get(exchange_code, exchange_code or "US")
        add_stock(stocks, symbol, name, exchange, "United States", "USD")


def load_nse_listed(stocks: dict):
    """Load NSE-listed Indian equities and convert symbols to Yahoo format."""
    text = download_text(NSE_EQUITY_URL)

    reader = csv.DictReader(io.StringIO(text))

    loaded_count = 0

    for row in reader:
        raw_symbol = row.get("SYMBOL", "").strip().upper()
        name = row.get("NAME OF COMPANY", "").strip()
        series = row.get(" SERIES", row.get("SERIES", "")).strip()

        if not raw_symbol or not name:
            continue

        # EQ is the normal equity series. This avoids many special instruments.
        if series and series != "EQ":
            continue

        yahoo_symbol = f"{raw_symbol}.NS"
        add_stock(stocks, yahoo_symbol, name, "NSE", "India", "INR")
        loaded_count += 1

    if loaded_count == 0:
        raise RuntimeError("NSE source returned zero usable stocks")


def load_india_fallback(stocks: dict):
    """Keep key Indian symbols available if NSE download is blocked."""
    for symbol, name, exchange, country, currency in FALLBACK_INDIA_STOCKS:
        add_stock(stocks, symbol, name, exchange, country, currency)


def write_stock_universe(stocks: dict):
    """Write all collected stocks to one CSV used by the backend search API."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows = sorted(stocks.values(), key=lambda stock: (stock["country"], stock["exchange"], stock["symbol"]))

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["symbol", "name", "exchange", "country", "currency"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


def main():
    stocks = {}

    print("Downloading Nasdaq-listed stocks...")
    load_nasdaq_listed(stocks)

    print("Downloading other U.S.-listed stocks...")
    load_other_us_listed(stocks)

    print("Downloading NSE-listed stocks...")
    try:
        load_nse_listed(stocks)
    except Exception as error:
        print(f"NSE download failed, using India fallback list: {error}")
        load_india_fallback(stocks)

    count = write_stock_universe(stocks)
    print(f"Wrote {count} stocks to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

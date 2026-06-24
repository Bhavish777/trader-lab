from fastapi import APIRouter, HTTPException, Query

from app.schemas import (
    StockHistoryPointResponse,
    StockQuoteResponse,
    StockSearchResultResponse,
)
from app.services.market_data import get_latest_quote, get_price_history
from app.services.symbol_resolver import search_symbols

router = APIRouter(prefix="/market", tags=["Market"])


@router.get("/search", response_model=list[StockSearchResultResponse])
def search_stock_symbols(
    query: str = Query(min_length=1, max_length=50),
    country: str | None = None,
):
    """Search stocks by company name, ticker, or common user-friendly terms."""
    return search_symbols(query, country)


@router.get("/quote/{symbol}", response_model=StockQuoteResponse)
def get_stock_quote(symbol: str):
    """Return the latest available quote for a ticker symbol."""
    try:
        return get_latest_quote(symbol)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail="Market data source is unavailable",
        ) from error


@router.get("/history/{symbol}", response_model=list[StockHistoryPointResponse])
def get_stock_history(
    symbol: str,
    period: str = Query(default="1mo", pattern="^(5d|1mo|3mo|6mo|1y|2y|5y)$"),
):
    """Return historical daily prices for charts."""
    try:
        return get_price_history(symbol, period)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail="Market data source is unavailable",
        ) from error

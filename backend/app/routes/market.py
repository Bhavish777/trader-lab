from fastapi import APIRouter, HTTPException

from app.schemas import StockQuoteResponse
from app.services.market_data import get_latest_quote

router = APIRouter(prefix="/market", tags=["Market"])


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

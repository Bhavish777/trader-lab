from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TradeCreate(BaseModel):
    symbol: str = Field(min_length=1, max_length=10)
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)


class TradeResponse(BaseModel):
    id: int
    symbol: str
    trade_type: str
    quantity: int
    price: float
    total_value: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HoldingResponse(BaseModel):
    id: int
    symbol: str
    quantity: int
    average_price: float
    invested_amount: float

    model_config = ConfigDict(from_attributes=True)


class CashBalanceResponse(BaseModel):
    cash_balance: float


class PortfolioSummaryResponse(BaseModel):
    starting_balance: float
    cash_balance: float
    invested_amount: float
    portfolio_value: float
    total_gain_loss: float
    total_return_percent: float
    holdings_count: int


class PortfolioResetResponse(BaseModel):
    message: str
    cash_balance: float

class StockQuoteResponse(BaseModel):
    symbol: str
    price: float
    currency: str
    source: str
    last_updated: str

class StockHistoryPointResponse(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int


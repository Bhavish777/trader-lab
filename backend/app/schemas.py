from pydantic import BaseModel, Field


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

    class Config:
        from_attributes = True

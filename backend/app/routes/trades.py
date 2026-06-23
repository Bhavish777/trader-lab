from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Trade
from app.schemas import TradeCreate, TradeResponse
from app.services.trading import buy_stock, sell_stock

router = APIRouter(prefix="/trades", tags=["Trades"])


@router.post("/buy", response_model=TradeResponse)
def buy_trade(trade: TradeCreate, db: Session = Depends(get_db)):
    try:
        return buy_stock(db, trade.symbol, trade.quantity, trade.price)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/sell", response_model=TradeResponse)
def sell_trade(trade: TradeCreate, db: Session = Depends(get_db)):
    try:
        return sell_stock(db, trade.symbol, trade.quantity, trade.price)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.get("", response_model=list[TradeResponse])
def get_trades(db: Session = Depends(get_db)):
    return db.query(Trade).order_by(Trade.created_at.desc()).all()

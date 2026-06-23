from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Holding

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.get("/holdings")
def get_holdings(db: Session = Depends(get_db)):
    return db.query(Holding).all()

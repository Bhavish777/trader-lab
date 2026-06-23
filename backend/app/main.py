from fastapi import FastAPI

from app import models
from app.database import Base, engine
from app.routes import trades

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Trader Lab API")

app.include_router(trades.router)


@app.get("/")
def health_check():
    return {"message": "Trader Lab API is running"}

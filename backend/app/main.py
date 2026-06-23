from fastapi import FastAPI

from app import models
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Trader Lab API")


@app.get("/")
def health_check():
    return {"message": "Trader Lab API is running"}

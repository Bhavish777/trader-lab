# Trader Lab

Trader Lab is a paper trading and portfolio analytics project.

The goal is to help users practice trading with virtual money, track holdings, review trade history, and understand basic portfolio performance before using real money.

## Version 1 Features

- Start with virtual cash
- Buy stocks
- Sell stocks
- Track holdings
- Track trade history
- Show cash balance
- Show portfolio value
- Show basic profit and loss
- Reset demo portfolio

## Tech Stack

- Backend: FastAPI
- Database: SQLite
- ORM: SQLAlchemy
- Validation: Pydantic
- Frontend: React later
- Market data: yfinance later

## Project Structure

trader-lab/
  backend/
    app/
      main.py
      database.py
      dependencies.py
      models.py
      schemas.py
      routes/
      services/
  frontend/
  docs/
  README.md

## Run Backend Locally

Go to the backend folder:

cd backend

Create a virtual environment:

python3 -m venv .venv

Activate it:

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run the API:

uvicorn app.main:app --reload --port 8002

Open:

http://127.0.0.1:8002

API docs:

http://127.0.0.1:8002/docs

## Main API Endpoints

GET  /
POST /trades/buy
POST /trades/sell
GET  /trades
GET  /portfolio/holdings
GET  /portfolio/cash
GET  /portfolio/summary
POST /portfolio/reset

## Current Status

Phase 1 backend is in progress.

The current backend supports basic paper trading, portfolio tracking, trade history, holdings, cash balance, portfolio summary, and portfolio reset.

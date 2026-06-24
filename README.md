# Trader Lab

Trader Lab is a paper trading and portfolio analytics project.

The goal is to help users practice trading with virtual money, track holdings, review trade history, search stocks, and understand portfolio performance before using real money.

## Phase 1 Status

Phase 1 backend MVP is complete.

The backend currently supports:

- Virtual cash balance
- Buy stock trades
- Sell stock trades
- Trade history
- Portfolio holdings
- Cash balance
- Portfolio summary
- Portfolio reset
- Stock quote lookup
- Stock price history
- Company name search
- Market-priced holdings
- Unrealized gain and loss
- Fallback pricing when market data is unavailable
- Backend tests
- Local smoke test script

## Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- yfinance
- pytest

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
    tests/
    requirements.txt
  docs/
  frontend/
  scripts/
  README.md

## Run Backend Locally

Go to the backend folder:

cd backend

Create a virtual environment:

python3 -m venv .venv

Activate it:

source .venv/bin/activate

Install dependencies:

python -m pip install -r requirements.txt

Run the API:

uvicorn app.main:app --reload --port 8002

Open the API:

http://127.0.0.1:8002

Open API docs:

http://127.0.0.1:8002/docs

## Core API Endpoints

Health check:

GET /

Trading:

POST /trades/buy
POST /trades/sell
GET /trades

Portfolio:

GET /portfolio/holdings
GET /portfolio/priced-holdings
GET /portfolio/cash
GET /portfolio/summary
POST /portfolio/reset

Market data:

GET /market/search?query=apple
GET /market/quote/AAPL
GET /market/history/AAPL
GET /market/history/AAPL?period=3mo

## Market Data Pipeline

Trader Lab uses a simple market data pipeline:

User search or ticker
  -> clean input
  -> resolve ticker or fetch quote
  -> fetch latest available market data
  -> clean response
  -> return data to API

Example:

Search:

apple

Result:

AAPL - Apple Inc.

Quote:

GET /market/quote/AAPL

History:

GET /market/history/AAPL?period=1mo

Market prices are latest available prices from the data provider and are not guaranteed real-time trading prices.

## Market-Priced Portfolio

Trader Lab can calculate portfolio values using latest available market prices.

Priced holdings include:

- Current price
- Market value
- Unrealized gain or loss
- Unrealized return percentage
- Price source

If market data is unavailable, Trader Lab falls back to the holding average price so the portfolio still works.

## Run Tests

From the backend folder:

python -m pytest -v

## Run Smoke Test

Start the backend first:

cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8002

Then in another terminal from the project root:

./scripts/smoke-test.sh

## Current Development Plan

Phase 1 is complete.

Next phase:

Phase 2 - Frontend MVP

Planned frontend features:

- Dashboard page
- Portfolio cards
- Buy form
- Sell form
- Stock search
- Holdings table
- Priced holdings table
- Trade history table
- Basic clean UI

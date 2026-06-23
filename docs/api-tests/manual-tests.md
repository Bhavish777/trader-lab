# Manual API Tests

These are manual backend tests for Trader Lab.

Base URL:
http://127.0.0.1:8002

## Health Check

Endpoint:
GET /

Expected:
Trader Lab API is running

## Buy Stock

Endpoint:
POST /trades/buy

Example body:
symbol: AAPL
quantity: 2
price: 100

Expected:
- Creates a BUY trade
- Reduces cash balance
- Adds or updates the stock holding

## Sell Stock

Endpoint:
POST /trades/sell

Example body:
symbol: AAPL
quantity: 1
price: 120

Expected:
- Creates a SELL trade
- Increases cash balance
- Reduces the stock holding quantity

## Trade History

Endpoint:
GET /trades

Expected:
- Returns all trades
- Newest trades appear first

## Portfolio Holdings

Endpoint:
GET /portfolio/holdings

Expected:
- Returns current stock holdings

## Cash Balance

Endpoint:
GET /portfolio/cash

Expected:
- Returns available virtual cash

## Portfolio Summary

Endpoint:
GET /portfolio/summary

Expected:
- Returns cash balance
- Returns invested amount
- Returns total portfolio value
- Returns number of holdings

Example response:
cash_balance: 99260.0
invested_amount: 800.0
portfolio_value: 100060.0
holdings_count: 2

Numbers may change depending on previous test trades.

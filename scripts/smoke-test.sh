#!/bin/bash

BASE_URL="http://127.0.0.1:8002"

echo "Testing Trader Lab API..."
echo

echo "1. Health check"
curl -s "$BASE_URL/"
echo
echo

echo "2. Reset portfolio"
curl -s -X POST "$BASE_URL/portfolio/reset"
echo
echo

echo "3. Buy stock"
curl -s -X POST "$BASE_URL/trades/buy" \
  -H "Content-Type: application/json" \
  -d '{"symbol":"AAPL","quantity":2,"price":100}'
echo
echo

echo "4. Sell stock"
curl -s -X POST "$BASE_URL/trades/sell" \
  -H "Content-Type: application/json" \
  -d '{"symbol":"AAPL","quantity":1,"price":120}'
echo
echo

echo "5. Portfolio holdings"
curl -s "$BASE_URL/portfolio/holdings"
echo
echo

echo "6. Priced portfolio holdings"
curl -s "$BASE_URL/portfolio/priced-holdings"
echo
echo

echo "7. Portfolio summary"
curl -s "$BASE_URL/portfolio/summary"
echo
echo

echo "8. Trade history"
curl -s "$BASE_URL/trades"
echo
echo

echo "9. Stock search"
curl -s "$BASE_URL/market/search?query=apple"
echo
echo

echo "10. Stock quote"
curl -s "$BASE_URL/market/quote/AAPL"
echo
echo

echo "11. Stock history"
curl -s "$BASE_URL/market/history/AAPL?period=5d"
echo
echo

echo "Smoke test complete."

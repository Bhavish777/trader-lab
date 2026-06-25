const API_BASE_URL = '/api'

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail || 'API request failed')
  }

  return data
}

export function getPortfolioSummary() {
  return apiRequest('/portfolio/summary')
}

export function getPricedHoldings() {
  return apiRequest('/portfolio/priced-holdings')
}

export function getTradeHistory() {
  return apiRequest('/trades')
}

export function searchStocks(query) {
  return apiRequest(`/market/search?query=${encodeURIComponent(query)}`)
}

export function getStockQuote(symbol) {
  return apiRequest(`/market/quote/${encodeURIComponent(symbol)}`)
}

export function buyStock(trade) {
  return apiRequest('/trades/buy', {
    method: 'POST',
    body: JSON.stringify(trade),
  })
}

export function sellStock(trade) {
  return apiRequest('/trades/sell', {
    method: 'POST',
    body: JSON.stringify(trade),
  })
}

export function resetPortfolio() {
  return apiRequest('/portfolio/reset', {
    method: 'POST',
  })
}

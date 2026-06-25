import { useState } from 'react'
import { getStockQuote, searchStocks } from '../api/client'
import { formatMoney } from '../utils/formatters'

function StockSearch() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [selectedStock, setSelectedStock] = useState(null)
  const [quote, setQuote] = useState(null)
  const [message, setMessage] = useState('')
  const [isSearching, setIsSearching] = useState(false)

  async function handleSearch(event) {
    event.preventDefault()

    if (!query.trim()) {
      setMessage('Type a company name or ticker first.')
      return
    }

    setIsSearching(true)
    setMessage('')
    setQuote(null)
    setSelectedStock(null)

    try {
      const data = await searchStocks(query)
      setResults(data)

      if (data.length === 0) {
        setMessage('No matching stocks found.')
      }
    } catch (error) {
      setResults([])
      setMessage(error.message)
    } finally {
      setIsSearching(false)
    }
  }

  async function handleSelectStock(stock) {
    setSelectedStock(stock)
    setResults([])
    setMessage('Loading quote...')

    try {
      const data = await getStockQuote(stock.symbol)
      setQuote(data)
      setMessage('')
    } catch (error) {
      setQuote(null)
      setMessage(error.message)
    }
  }

  return (
    <section className="panel">
      <div className="section-header compact">
        <div>
          <p className="section-kicker">Market</p>
          <h2>Stock search</h2>
        </div>
      </div>

      <form className="search-form" onSubmit={handleSearch}>
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Search Apple, Tesla, Reliance, Shopify..."
        />

        <button type="submit" disabled={isSearching}>
          {isSearching ? 'Searching...' : 'Search'}
        </button>
      </form>

      {message && <p className="inline-message">{message}</p>}

      {results.length > 0 && (
        <div className="stock-results">
          {results.map((stock) => (
            <button
              key={`${stock.symbol}-${stock.exchange}`}
              className="stock-result"
              type="button"
              onClick={() => handleSelectStock(stock)}
            >
              <strong>{stock.symbol}</strong>
              <span>{stock.name}</span>
              <small>
                {stock.exchange} · {stock.currency} · {stock.country}
              </small>
            </button>
          ))}
        </div>
      )}

      {selectedStock && quote && (
        <article className="quote-card">
          <div>
            <p className="quote-label">Selected stock</p>
            <h3>{selectedStock.name}</h3>
            <p className="muted">
              {selectedStock.symbol} · {selectedStock.exchange} · {selectedStock.country}
            </p>
          </div>

          <div className="quote-price">
            <span>Latest price</span>
            <strong>{formatMoney(quote.price, quote.currency)}</strong>
            <small>{quote.source}</small>
          </div>
        </article>
      )}
    </section>
  )
}

export default StockSearch

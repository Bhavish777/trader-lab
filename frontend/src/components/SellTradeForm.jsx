import { useEffect, useState } from 'react'
import { sellStock } from '../api/client'
import { formatMoney } from '../utils/formatters'

function SellTradeForm({ holdings, onTradeComplete }) {
  const [selectedSymbol, setSelectedSymbol] = useState('')
  const [quantity, setQuantity] = useState('')
  const [price, setPrice] = useState('')
  const [message, setMessage] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const selectedHolding = holdings.find((holding) => holding.symbol === selectedSymbol)

  useEffect(() => {
    if (selectedHolding) {
      setPrice(selectedHolding.current_price)
      setQuantity('')
      setMessage('')
    }
  }, [selectedHolding])

  async function handleSell(event) {
    event.preventDefault()

    if (!selectedHolding) {
      setMessage('Choose a holding before selling.')
      return
    }

    if (Number(quantity) <= 0 || Number(price) <= 0) {
      setMessage('Quantity and price must be greater than zero.')
      return
    }

    if (Number(quantity) > selectedHolding.quantity) {
      setMessage(`You only own ${selectedHolding.quantity} share(s) of ${selectedHolding.symbol}.`)
      return
    }

    setIsSubmitting(true)
    setMessage('')

    try {
      await sellStock({
        symbol: selectedHolding.symbol,
        quantity: Number(quantity),
        price: Number(price),
      })

      setMessage(`Sold ${quantity} share(s) of ${selectedHolding.symbol}`)
      setQuantity('')
      await onTradeComplete()
    } catch (error) {
      setMessage(error.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  if (holdings.length === 0) {
    return (
      <section className="panel">
        <div className="section-header compact">
          <div>
            <p className="section-kicker">Trading</p>
            <h2>Sell stock</h2>
          </div>
        </div>

        <p className="muted">No holdings to sell yet. Buy a stock first.</p>
      </section>
    )
  }

  return (
    <section className="panel">
      <div className="section-header compact">
        <div>
          <p className="section-kicker">Trading</p>
          <h2>Sell stock</h2>
        </div>
      </div>

      <form className="trade-form sell-form" onSubmit={handleSell}>
        <label>
          Holding
          <select
            value={selectedSymbol}
            onChange={(event) => setSelectedSymbol(event.target.value)}
          >
            <option value="">Choose a holding</option>
            {holdings.map((holding) => (
              <option key={holding.symbol} value={holding.symbol}>
                {holding.symbol} · {holding.quantity} share(s)
              </option>
            ))}
          </select>
        </label>

        {selectedHolding && (
          <div className="sell-preview">
            <div>
              <span>Owned</span>
              <strong>{selectedHolding.quantity}</strong>
            </div>

            <div>
              <span>Current price</span>
              <strong>{formatMoney(selectedHolding.current_price)}</strong>
            </div>

            <div>
              <span>Market value</span>
              <strong>{formatMoney(selectedHolding.market_value)}</strong>
            </div>
          </div>
        )}

        <label>
          Quantity
          <input
            value={quantity}
            onChange={(event) => setQuantity(event.target.value)}
            min="1"
            max={selectedHolding?.quantity}
            placeholder="Example: 1"
            type="number"
          />
        </label>

        <label>
          Price
          <input
            value={price}
            onChange={(event) => setPrice(event.target.value)}
            min="0"
            step="0.01"
            type="number"
          />
        </label>

        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Selling...' : 'Sell Stock'}
        </button>

        {message && <p className="inline-message">{message}</p>}
      </form>
    </section>
  )
}

export default SellTradeForm

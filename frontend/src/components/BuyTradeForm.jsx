import { useEffect, useState } from 'react'
import { buyStock } from '../api/client'
import { formatMoney } from '../utils/formatters'

function BuyTradeForm({ selectedStock, quote, onTradeComplete }) {
  const [quantity, setQuantity] = useState('')
  const [price, setPrice] = useState('')
  const [message, setMessage] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  useEffect(() => {
    if (selectedStock && quote) {
      setPrice(quote.price)
      setQuantity('')
      setMessage('')
    }
  }, [selectedStock, quote])

  async function handleBuy(event) {
    event.preventDefault()

    if (!selectedStock) {
      setMessage('Select a stock before buying.')
      return
    }

    if (Number(quantity) <= 0 || Number(price) <= 0) {
      setMessage('Quantity and price must be greater than zero.')
      return
    }

    setIsSubmitting(true)
    setMessage('')

    try {
      await buyStock({
        symbol: selectedStock.symbol,
        quantity: Number(quantity),
        price: Number(price),
      })

      setMessage(`Bought ${quantity} share(s) of ${selectedStock.symbol}`)
      setQuantity('')
      await onTradeComplete()
    } catch (error) {
      setMessage(error.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  if (!selectedStock || !quote) {
    return (
      <div className="trade-form muted-box">
        Search and select a stock to place a buy order.
      </div>
    )
  }

  return (
    <form className="trade-form" onSubmit={handleBuy}>
      <div className="trade-form-header">
        <div>
          <p className="quote-label">Buy order</p>
          <h3>{selectedStock.symbol}</h3>
        </div>

        <div className="mini-price">
          <span>Market price</span>
          <strong>{formatMoney(quote.price, quote.currency)}</strong>
        </div>
      </div>

      <label>
        Quantity
        <input
          value={quantity}
          onChange={(event) => setQuantity(event.target.value)}
          min="1"
          placeholder="Example: 2"
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
        {isSubmitting ? 'Buying...' : 'Buy Stock'}
      </button>

      {message && <p className="inline-message">{message}</p>}
    </form>
  )
}

export default BuyTradeForm

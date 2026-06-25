import { formatMoney, formatPercent } from '../utils/formatters'

function HoldingsTable({ holdings }) {
  if (holdings.length === 0) {
    return (
      <section className="panel">
        <div className="section-header compact">
          <div>
            <p className="section-kicker">Portfolio</p>
            <h2>Priced holdings</h2>
          </div>
        </div>

        <p className="muted">
          No holdings yet. Buy a stock and it will appear here.
        </p>
      </section>
    )
  }

  return (
    <section className="panel">
      <div className="section-header compact">
        <div>
          <p className="section-kicker">Portfolio</p>
          <h2>Priced holdings</h2>
        </div>
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Qty</th>
              <th>Avg Price</th>
              <th>Current</th>
              <th>Market Value</th>
              <th>P&L</th>
              <th>Return</th>
              <th>Source</th>
            </tr>
          </thead>

          <tbody>
            {holdings.map((holding) => {
              const isPositive = holding.unrealized_gain_loss > 0
              const isNegative = holding.unrealized_gain_loss < 0

              return (
                <tr key={holding.symbol}>
                  <td>
                    <strong>{holding.symbol}</strong>
                  </td>
                  <td>{holding.quantity}</td>
                  <td>{formatMoney(holding.average_price)}</td>
                  <td>{formatMoney(holding.current_price)}</td>
                  <td>{formatMoney(holding.market_value)}</td>
                  <td className={isPositive ? 'positive' : isNegative ? 'negative' : ''}>
                    {formatMoney(holding.unrealized_gain_loss)}
                  </td>
                  <td className={isPositive ? 'positive' : isNegative ? 'negative' : ''}>
                    {formatPercent(holding.unrealized_return_percent)}
                  </td>
                  <td>
                    <span className="source-pill">{holding.price_source}</span>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </section>
  )
}

export default HoldingsTable

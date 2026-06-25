import { formatMoney } from '../utils/formatters'

function TradeHistoryTable({ trades }) {
  if (trades.length === 0) {
    return (
      <section className="panel">
        <div className="section-header compact">
          <div>
            <p className="section-kicker">Activity</p>
            <h2>Trade history</h2>
          </div>
        </div>

        <p className="muted">
          No trades yet. Your buy and sell activity will appear here.
        </p>
      </section>
    )
  }

  return (
    <section className="panel">
      <div className="section-header compact">
        <div>
          <p className="section-kicker">Activity</p>
          <h2>Trade history</h2>
        </div>
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Type</th>
              <th>Symbol</th>
              <th>Qty</th>
              <th>Price</th>
              <th>Total</th>
              <th>Time</th>
            </tr>
          </thead>

          <tbody>
            {trades.map((trade) => (
              <tr key={trade.id}>
                <td>
                  <span className={`trade-pill trade-pill-${trade.trade_type}`}>
                    {trade.trade_type}
                  </span>
                </td>
                <td>
                  <strong>{trade.symbol}</strong>
                </td>
                <td>{trade.quantity}</td>
                <td>{formatMoney(trade.price)}</td>
                <td>{formatMoney(trade.total_value)}</td>
                <td>{new Date(trade.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

export default TradeHistoryTable

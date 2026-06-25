import { formatMoney, formatPercent } from '../utils/formatters'

function SummaryCard({ label, value, helper, tone = 'neutral' }) {
  return (
    <article className={`summary-card summary-card-${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
      {helper && <small>{helper}</small>}
    </article>
  )
}

function getReturnTone(value) {
  if (value > 0) return 'positive'
  if (value < 0) return 'negative'
  return 'neutral'
}

function SummaryCards({ summary }) {
  const returnTone = getReturnTone(summary.total_return_percent)
  const profitTone = getReturnTone(summary.total_gain_loss)

  return (
    <section className="summary-grid" aria-label="Portfolio summary">
      <SummaryCard
        label="Portfolio Value"
        value={formatMoney(summary.portfolio_value)}
        helper="Cash plus market value"
      />

      <SummaryCard
        label="Cash Balance"
        value={formatMoney(summary.cash_balance)}
        helper="Available buying power"
      />

      <SummaryCard
        label="Invested Amount"
        value={formatMoney(summary.invested_amount)}
        helper="Cost basis of holdings"
      />

      <SummaryCard
        label="Total P&L"
        value={formatMoney(summary.total_gain_loss)}
        helper="Since starting balance"
        tone={profitTone}
      />

      <SummaryCard
        label="Total Return"
        value={formatPercent(summary.total_return_percent)}
        helper="Portfolio performance"
        tone={returnTone}
      />

      <SummaryCard
        label="Holdings"
        value={summary.holdings_count}
        helper="Current open positions"
      />
    </section>
  )
}

export default SummaryCards

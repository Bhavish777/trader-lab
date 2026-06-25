export function formatMoney(value, currency = 'USD') {
  return Number(value || 0).toLocaleString('en-US', {
    style: 'currency',
    currency,
  })
}

export function formatPercent(value) {
  return `${Number(value || 0).toFixed(2)}%`
}

export function formatTradeTime(value) {
  if (!value) return '—'

  const utcValue = value.endsWith('Z') ? value : `${value}Z`

  return new Date(utcValue).toLocaleString('en-CA', {
    dateStyle: 'medium',
    timeStyle: 'short',
    timeZone: 'America/Vancouver',
  })
}

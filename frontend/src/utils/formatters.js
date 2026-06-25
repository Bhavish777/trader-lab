export function formatMoney(value, currency = 'USD') {
  return Number(value || 0).toLocaleString('en-US', {
    style: 'currency',
    currency,
  })
}

export function formatPercent(value) {
  return `${Number(value || 0).toFixed(2)}%`
}

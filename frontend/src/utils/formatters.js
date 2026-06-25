export function formatMoney(value) {
  return Number(value || 0).toLocaleString('en-US', {
    style: 'currency',
    currency: 'USD',
  })
}

export function formatPercent(value) {
  return `${Number(value || 0).toFixed(2)}%`
}

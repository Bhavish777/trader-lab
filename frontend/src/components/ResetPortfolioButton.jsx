import { useState } from 'react'
import { resetPortfolio } from '../api/client'

function ResetPortfolioButton({ onResetComplete }) {
  const [isResetting, setIsResetting] = useState(false)
  const [message, setMessage] = useState('')

  async function handleReset() {
    const shouldReset = window.confirm(
      'Reset the demo portfolio? This will clear all trades and holdings.'
    )

    if (!shouldReset) return

    setIsResetting(true)
    setMessage('')

    try {
      await resetPortfolio()
      await onResetComplete()
      setMessage('Portfolio reset')
    } catch (error) {
      setMessage(error.message)
    } finally {
      setIsResetting(false)
    }
  }

  return (
    <div className="reset-area">
      <button
        className="secondary-button"
        type="button"
        onClick={handleReset}
        disabled={isResetting}
      >
        {isResetting ? 'Resetting...' : 'Reset Portfolio'}
      </button>

      {message && <span className="reset-message">{message}</span>}
    </div>
  )
}

export default ResetPortfolioButton

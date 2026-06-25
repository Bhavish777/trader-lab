import { useEffect, useState } from 'react'
import { getPortfolioSummary } from './api/client'
import './App.css'

function formatMoney(value) {
  return Number(value || 0).toLocaleString('en-US', {
    style: 'currency',
    currency: 'USD',
  })
}

function App() {
  const [summary, setSummary] = useState(null)
  const [apiStatus, setApiStatus] = useState('Checking backend connection...')

  useEffect(() => {
    async function loadSummary() {
      try {
        const data = await getPortfolioSummary()
        setSummary(data)
        setApiStatus('Backend connected')
      } catch (error) {
        setApiStatus(`Backend not connected: ${error.message}`)
      }
    }

    loadSummary()
  }, [])

  return (
    <main className="app">
      <section className="hero">
        <p className="eyebrow">Trader Lab</p>
        <h1>Practice trading before using real money.</h1>
        <p className="hero-text">
          Trader Lab is a paper trading dashboard for testing trades, tracking holdings,
          and understanding portfolio performance.
        </p>
      </section>

      <section className="status-card">
        <h2>Phase 2 Frontend MVP</h2>
        <p>{apiStatus}</p>

        {summary && (
          <div className="api-preview">
            <span>Current portfolio value</span>
            <strong>{formatMoney(summary.portfolio_value)}</strong>
          </div>
        )}
      </section>
    </main>
  )
}

export default App

import { useEffect, useState } from 'react'
import {
  getPortfolioSummary,
  getPricedHoldings,
  getTradeHistory,
} from './api/client'
import HoldingsTable from './components/HoldingsTable'
import StockSearch from './components/StockSearch'
import SummaryCards from './components/SummaryCards'
import TradeHistoryTable from './components/TradeHistoryTable'
import './App.css'

function App() {
  const [summary, setSummary] = useState(null)
  const [holdings, setHoldings] = useState([])
  const [trades, setTrades] = useState([])
  const [apiStatus, setApiStatus] = useState('Checking backend connection...')
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [summaryData, holdingsData, tradesData] = await Promise.all([
          getPortfolioSummary(),
          getPricedHoldings(),
          getTradeHistory(),
        ])

        setSummary(summaryData)
        setHoldings(holdingsData)
        setTrades(tradesData)
        setApiStatus('Backend connected')
      } catch (error) {
        setApiStatus(`Backend not connected: ${error.message}`)
      } finally {
        setIsLoading(false)
      }
    }

    loadDashboard()
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

      <section className="dashboard-section">
        <div className="section-header">
          <div>
            <p className="section-kicker">Dashboard</p>
            <h2>Portfolio summary</h2>
          </div>

          <span className="connection-pill">{apiStatus}</span>
        </div>

        {isLoading && <p className="muted">Loading portfolio summary...</p>}

        {!isLoading && summary && <SummaryCards summary={summary} />}

        {!isLoading && !summary && (
          <p className="error-text">
            Start the backend on port 8002, then refresh this page.
          </p>
        )}
      </section>

      {!isLoading && summary && (
        <>
          <StockSearch />
          <HoldingsTable holdings={holdings} />
          <TradeHistoryTable trades={trades} />
        </>
      )}
    </main>
  )
}

export default App

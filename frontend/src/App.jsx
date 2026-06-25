import { useEffect, useState } from 'react'
import {
  getPortfolioSummary,
  getPricedHoldings,
  getTradeHistory,
} from './api/client'
import { ErrorState, LoadingState } from './components/AppState'
import HoldingsTable from './components/HoldingsTable'
import ResetPortfolioButton from './components/ResetPortfolioButton'
import SellTradeForm from './components/SellTradeForm'
import StockSearch from './components/StockSearch'
import SummaryCards from './components/SummaryCards'
import TradeHistoryTable from './components/TradeHistoryTable'
import './App.css'

function App() {
  const [summary, setSummary] = useState(null)
  const [holdings, setHoldings] = useState([])
  const [trades, setTrades] = useState([])
  const [apiStatus, setApiStatus] = useState('Checking backend connection...')
  const [errorMessage, setErrorMessage] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [isRefreshing, setIsRefreshing] = useState(false)

  async function loadDashboard({ showFullLoading = false } = {}) {
    if (showFullLoading) {
      setIsLoading(true)
    } else {
      setIsRefreshing(true)
    }

    setErrorMessage('')

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
      setApiStatus('Backend disconnected')
      setErrorMessage(error.message)
    } finally {
      setIsLoading(false)
      setIsRefreshing(false)
    }
  }

  useEffect(() => {
    loadDashboard({ showFullLoading: true })
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

      {isLoading && <LoadingState />}

      {!isLoading && errorMessage && !summary && (
        <ErrorState
          message={errorMessage}
          onRetry={() => loadDashboard({ showFullLoading: true })}
        />
      )}

      {!isLoading && summary && (
        <>
          <section className="dashboard-section">
            <div className="section-header">
              <div>
                <p className="section-kicker">Dashboard</p>
                <h2>Portfolio summary</h2>
              </div>

              <div className="header-actions">
                <span className="connection-pill">{apiStatus}</span>

                <button
                  className="secondary-button"
                  type="button"
                  onClick={() => loadDashboard()}
                  disabled={isRefreshing}
                >
                  {isRefreshing ? 'Refreshing...' : 'Refresh'}
                </button>

                <ResetPortfolioButton onResetComplete={loadDashboard} />
              </div>
            </div>

            {errorMessage && (
              <p className="warning-box">
                Latest refresh failed: {errorMessage}
              </p>
            )}

            <SummaryCards summary={summary} />
          </section>

          <StockSearch onTradeComplete={loadDashboard} />
          <SellTradeForm holdings={holdings} onTradeComplete={loadDashboard} />
          <HoldingsTable holdings={holdings} />
          <TradeHistoryTable trades={trades} />
        </>
      )}
    </main>
  )
}

export default App

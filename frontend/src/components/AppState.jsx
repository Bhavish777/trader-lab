function LoadingState() {
  return (
    <section className="state-panel">
      <div className="loading-dot" />
      <div>
        <h2>Loading Trader Lab...</h2>
        <p>Fetching your portfolio, holdings, and trade history.</p>
      </div>
    </section>
  )
}

function ErrorState({ message, onRetry }) {
  return (
    <section className="state-panel error-panel">
      <div>
        <p className="section-kicker">Connection issue</p>
        <h2>Backend is not responding</h2>
        <p>{message || 'Start the backend on port 8002, then try again.'}</p>
      </div>

      <button type="button" onClick={onRetry}>
        Try Again
      </button>
    </section>
  )
}

export { LoadingState, ErrorState }

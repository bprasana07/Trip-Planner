export default function Sidebar({ open, onClose, onClear }) {
  return (
    <>
      {open && <div className="sidebar-backdrop" onClick={onClose} />}
      <aside className={`sidebar ${open ? 'open' : ''}`}>
        <div className="sidebar-header">
          <span className="sidebar-logo">✈️ TripBot</span>
          <button className="sidebar-close" onClick={onClose} aria-label="Close">✕</button>
        </div>
        <nav className="sidebar-nav">
          <div className="sidebar-section">About</div>
          <p className="sidebar-text">
            TripBot is a multi-agent AI planner powered by Neuro SAN Studio. It coordinates three specialist agents:
          </p>
          <ul className="agent-list">
            <li><span className="agent-icon">🌤️</span> <div><strong>Weather Agent</strong><br /><small>Forecast & outdoor classification</small></div></li>
            <li><span className="agent-icon">🗺️</span> <div><strong>Activity Planner</strong><br /><small>Attractions & day-by-day itinerary</small></div></li>
            <li><span className="agent-icon">🏨</span> <div><strong>Stay Advisor</strong><br /><small>Budget, mid-range & luxury hotels</small></div></li>
          </ul>

          <div className="sidebar-section">Session</div>
          <button className="sidebar-action danger" onClick={() => { onClear(); onClose() }}>
            🗑️ Clear conversation
          </button>
        </nav>

        <div className="sidebar-footer">
          <a href="https://github.com/cognizant-ai-lab/neuro-san-studio" target="_blank" rel="noreferrer">
            Neuro SAN Studio ↗
          </a>
        </div>
      </aside>
    </>
  )
}

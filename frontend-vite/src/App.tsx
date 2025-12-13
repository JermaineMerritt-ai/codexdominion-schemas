import { useState, useEffect } from 'react'
import './App.css'
import { useAuth } from './hooks/useAuth'

interface HealthStatus {
  status: string
  service: string
  version: string
}

interface CapsuleStats {
  total: number
  by_kind?: Record<string, number>
  by_engine?: Record<string, number>
}

function App() {
  const { user, isAuthenticated, login, logout, loading: authLoading } = useAuth()
  const [health, setHealth] = useState<HealthStatus | null>(null)
  const [stats, setStats] = useState<CapsuleStats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const healthRes = await fetch('http://codex-api-eastus.eastus.azurecontainer.io:8000/health')
        const healthData = await healthRes.json()
        setHealth(healthData)

        const statsRes = await fetch('http://codex-api-eastus.eastus.azurecontainer.io:8000/api/capsules/stats')
        const statsData = await statsRes.json()
        setStats(statsData)
      } catch (error) {
        console.error('Failed to fetch data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
    const interval = setInterval(fetchData, 30000)
    return () => clearInterval(interval)
  }, [])

  if (loading || authLoading) {
    return (
      <div className="app">
        <div className="container">
          <h1>🔥 Codex Dominion</h1>
          <p>Loading system status...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="app">
      <header className="header">
        <div className="container">
          <div className="header-content">
            <div>
              <h1>👑 Codex Dominion</h1>
              <p className="subtitle">Sovereign Archive & Capsule Management System</p>
            </div>
            <div className="auth-section">
              {isAuthenticated && user ? (
                <>
                  <div className="user-info">
                    <div className="user-name">
                      {user.userDetails}
                    </div>
                    <div className="user-roles">
                      {user.userRoles.join(', ')}
                    </div>
                  </div>
                  <button onClick={logout} className="action-btn auth-btn">
                    Logout
                  </button>
                </>
              ) : (
                <button onClick={() => login('twitter')} className="action-btn auth-btn">
                  Login
                </button>
              )}
            </div>
          </div>
        </div>
      </header>

      <main className="container main-content">
        {/* System Health */}
        <section className="card">
          <h2>⚡ System Status</h2>
          {health && (
            <div className="status-grid">
              <div className="status-item">
                <span className="label">Status:</span>
                <span className={`badge ${health.status === 'healthy' ? 'success' : 'warning'}`}>
                  {health.status}
                </span>
              </div>
              <div className="status-item">
                <span className="label">Service:</span>
                <span>{health.service}</span>
              </div>
              <div className="status-item">
                <span className="label">Version:</span>
                <span>{health.version}</span>
              </div>
            </div>
          )}
        </section>

        {/* Capsule Statistics */}
        <section className="card">
          <h2>📦 Capsule Archive</h2>
          {stats && (
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-value">{stats.total}</div>
                <div className="stat-label">Total Capsules</div>
              </div>

              {stats.by_kind && Object.entries(stats.by_kind).map(([kind, count]) => (
                <div key={kind} className="stat-card">
                  <div className="stat-value">{count}</div>
                  <div className="stat-label">{kind}</div>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* Quick Actions */}
        <section className="card">
          <h2>🎯 Quick Actions</h2>
          <div className="actions-grid">
            <a
              href="http://codex-api-eastus.eastus.azurecontainer.io:8000/api/annotations/export?format=yaml"
              className="action-btn"
              target="_blank"
              rel="noopener noreferrer"
            >
              📜 Export YAML Archive
            </a>
            <a
              href="http://codex-api-eastus.eastus.azurecontainer.io:8000/api/annotations/export?format=markdown"
              className="action-btn"
              target="_blank"
              rel="noopener noreferrer"
            >
              📝 Export Markdown Scroll
            </a>
            <a
              href="http://codex-api-eastus.eastus.azurecontainer.io:8000/api/annotations/export?format=pdf"
              className="action-btn"
              target="_blank"
              rel="noopener noreferrer"
            >
              📄 Export PDF Ledger
            </a>
            <a
              href="http://codex-api-eastus.eastus.azurecontainer.io:8000/docs"
              className="action-btn"
              target="_blank"
              rel="noopener noreferrer"
            >
              📚 API Documentation
            </a>
          </div>
        </section>

        {/* API Endpoints */}
        <section className="card">
          <h2>🔌 API Endpoints</h2>
          <div className="endpoint-list">
            <div className="endpoint">
              <code>GET /health</code>
              <span>System health check</span>
            </div>
            <div className="endpoint">
              <code>GET /api/capsules/stats</code>
              <span>Capsule statistics</span>
            </div>
            <div className="endpoint">
              <code>GET /api/annotations/export</code>
              <span>Export sealed archives</span>
            </div>
            <div className="endpoint">
              <code>POST /api/seal/verify</code>
              <span>Verify cryptographic seals</span>
            </div>
          </div>
        </section>
      </main>

      <footer className="footer">
        <div className="container">
          <p>🔥 Codex Dominion Archive System v1.0.3</p>
          <p>Backend: <code>codex-api-eastus.eastus.azurecontainer.io</code></p>
        </div>
      </footer>
    </div>
  )
}

export default App

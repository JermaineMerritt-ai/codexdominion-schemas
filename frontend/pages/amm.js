// pages/amm.js
import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { apiClient } from '../lib/api';

export default function AMM() {
  const [pools, setPools] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filterState, setFilterState] = useState('all');

  useEffect(() => {
    fetchPools();
  }, [filterState]);

  const fetchPools = async () => {
    try {
      setLoading(true);
      const params = filterState !== 'all' ? { state: filterState } : {};
      const data = await apiClient.getPools(params);
      setPools(data.pools || []);
    } catch (err) {
      setError('Failed to load AMM pools');
      console.error('Error fetching pools:', err);
    } finally {
      setLoading(false);
    }
  };

  const getStateColor = (state) => {
    switch (state) {
      case 'active': return 'green';
      case 'paused': return 'orange';
      case 'closed': return 'red';
      default: return 'gray';
    }
  };

  const formatCurrency = (amount, currency = 'USD') => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency === 'USD' ? 'USD' : 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  if (loading && pools.length === 0) {
    return (
      <Layout>
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading AMM pools...</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="amm-page">
        <header className="page-header">
          <div className="header-content">
            <h1>🌊 AMM Pools</h1>
            <p>Automated Market Making and Liquidity Management</p>
          </div>
          <div className="header-actions">
            <select
              value={filterState}
              onChange={(e) => setFilterState(e.target.value)}
              className="filter-select"
            >
              <option value="all">All States</option>
              <option value="active">Active</option>
              <option value="paused">Paused</option>
              <option value="closed">Closed</option>
            </select>
          </div>
        </header>

        {error && (
          <div className="error-message">
            <p>{error}</p>
            <button onClick={fetchPools}>Retry</button>
          </div>
        )}

        {/* Summary Stats */}
        <section className="summary-section">
          <h2>📊 Pool Overview</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Total Pools</h3>
              <p className="stat-value">{pools.length}</p>
            </div>
            <div className="stat-card">
              <h3>Active Pools</h3>
              <p className="stat-value">
                {pools.filter(p => p.state === 'active').length}
              </p>
            </div>
            <div className="stat-card">
              <h3>Total TVL</h3>
              <p className="stat-value">
                {formatCurrency(pools.reduce((sum, p) => sum + (p.tvl || 0), 0))}
              </p>
            </div>
            <div className="stat-card">
              <h3>Avg APR</h3>
              <p className="stat-value">
                {pools.length > 0 
                  ? (pools.reduce((sum, p) => sum + (p.apr || 0), 0) / pools.length).toFixed(1)
                  : '0'
                }%
              </p>
            </div>
          </div>
        </section>

        {/* Pools Grid */}
        <section className="pools-section">
          <h2>🏊 Pool Details</h2>
          <div className="pools-grid">
            {pools.length > 0 ? (
              pools.map((pool) => (
                <div key={pool.id} className="pool-card">
                  <div className="pool-header">
                    <div className="pool-pair">
                      <h3>{pool.asset_pair}</h3>
                      <span className={`state-badge ${getStateColor(pool.state)}`}>
                        {pool.state}
                      </span>
                    </div>
                    <div className="pool-weight">
                      Weight: {pool.weight}%
                    </div>
                  </div>

                  <div className="pool-metrics">
                    <div className="metric">
                      <label>TVL</label>
                      <value>{formatCurrency(pool.tvl || 0)}</value>
                    </div>
                    <div className="metric">
                      <label>APR</label>
                      <value className="apr">{(pool.apr || 0).toFixed(2)}%</value>
                    </div>
                    <div className="metric">
                      <label>Cap</label>
                      <value>{formatCurrency(pool.cap)}</value>
                    </div>
                  </div>

                  <div className="pool-progress">
                    <div className="progress-label">
                      Utilization: {pool.cap > 0 ? ((pool.tvl || 0) / pool.cap * 100).toFixed(1) : '0'}%
                    </div>
                    <div className="progress-bar">
                      <div 
                        className="progress-fill"
                        style={{ 
                          width: `${pool.cap > 0 ? Math.min((pool.tvl || 0) / pool.cap * 100, 100) : 0}%` 
                        }}
                      ></div>
                    </div>
                  </div>

                  {pool.strategy_id && (
                    <div className="pool-strategy">
                      <small>Strategy ID: {pool.strategy_id}</small>
                    </div>
                  )}

                  <div className="pool-actions">
                    <button className="action-button primary">Manage</button>
                    <button className="action-button secondary">Analytics</button>
                  </div>

                  <div className="pool-updated">
                    <small>
                      Updated: {new Date(pool.updated_at).toLocaleDateString()}
                    </small>
                  </div>
                </div>
              ))
            ) : (
              <div className="no-pools">
                <h3>🔍 No Pools Found</h3>
                <p>
                  {filterState === 'all' 
                    ? 'No AMM pools available at the moment.'
                    : `No ${filterState} pools found.`
                  }
                </p>
              </div>
            )}
          </div>
        </section>

        <style jsx>{`
          .amm-page {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
          }

          .page-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #e2e8f0;
          }

          .header-content h1 {
            margin: 0;
            color: #2d3748;
            font-size: 2rem;
          }

          .header-content p {
            margin: 0.5rem 0 0 0;
            color: #718096;
          }

          .header-actions {
            display: flex;
            gap: 1rem;
            align-items: center;
          }

          .filter-select {
            padding: 0.5rem 1rem;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            background: white;
          }

          .summary-section {
            margin-bottom: 3rem;
          }

          .summary-section h2 {
            margin-bottom: 1.5rem;
            color: #2d3748;
          }

          .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
          }

          .stat-card {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border: 1px solid #e2e8f0;
          }

          .stat-card h3 {
            margin: 0 0 0.5rem 0;
            color: #4a5568;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
          }

          .stat-value {
            margin: 0;
            font-size: 1.8rem;
            font-weight: 700;
            color: #2d3748;
          }

          .pools-section {
            margin-bottom: 2rem;
          }

          .pools-section h2 {
            margin-bottom: 1.5rem;
            color: #2d3748;
          }

          .pools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 1.5rem;
          }

          .pool-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            border: 1px solid #e2e8f0;
            transition: transform 0.3s ease;
          }

          .pool-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
          }

          .pool-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
          }

          .pool-pair h3 {
            margin: 0;
            color: #2d3748;
            font-size: 1.2rem;
          }

          .state-badge {
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
          }

          .state-badge.green {
            background: #c6f6d5;
            color: #276749;
          }

          .state-badge.orange {
            background: #fbd38d;
            color: #c05621;
          }

          .state-badge.red {
            background: #fed7d7;
            color: #c53030;
          }

          .state-badge.gray {
            background: #e2e8f0;
            color: #4a5568;
          }

          .pool-weight {
            color: #718096;
            font-size: 0.9rem;
          }

          .pool-metrics {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 1rem;
            margin-bottom: 1rem;
            padding: 1rem;
            background: #f7fafc;
            border-radius: 8px;
          }

          .metric {
            text-align: center;
          }

          .metric label {
            display: block;
            color: #718096;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.25rem;
          }

          .metric value {
            display: block;
            color: #2d3748;
            font-weight: 600;
            font-size: 1rem;
          }

          .metric .apr {
            color: #38a169;
            font-weight: 700;
          }

          .pool-progress {
            margin-bottom: 1rem;
          }

          .progress-label {
            font-size: 0.9rem;
            color: #4a5568;
            margin-bottom: 0.5rem;
          }

          .progress-bar {
            background: #e2e8f0;
            height: 8px;
            border-radius: 4px;
            overflow: hidden;
          }

          .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s ease;
          }

          .pool-strategy {
            margin-bottom: 1rem;
          }

          .pool-strategy small {
            color: #718096;
            font-style: italic;
          }

          .pool-actions {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1rem;
          }

          .action-button {
            flex: 1;
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.3s ease;
          }

          .action-button.primary {
            background: #667eea;
            color: white;
          }

          .action-button.primary:hover {
            background: #5a67d8;
          }

          .action-button.secondary {
            background: #edf2f7;
            color: #4a5568;
            border: 1px solid #e2e8f0;
          }

          .action-button.secondary:hover {
            background: #e2e8f0;
          }

          .pool-updated {
            border-top: 1px solid #e2e8f0;
            padding-top: 1rem;
          }

          .pool-updated small {
            color: #718096;
            font-size: 0.8rem;
          }

          .no-pools {
            grid-column: 1 / -1;
            text-align: center;
            padding: 3rem;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
          }

          .no-pools h3 {
            margin: 0 0 1rem 0;
            color: #4a5568;
          }

          .no-pools p {
            margin: 0;
            color: #718096;
          }

          .loading-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 300px;
            color: #718096;
          }

          .loading-spinner {
            width: 40px;
            height: 40px;
            border: 4px solid #e2e8f0;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 1rem;
          }

          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }

          .error-message {
            background: #fed7d7;
            color: #c53030;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
          }

          .error-message button {
            background: #c53030;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            cursor: pointer;
          }

          @media (max-width: 768px) {
            .amm-page {
              padding: 0 1rem;
            }

            .page-header {
              flex-direction: column;
              gap: 1rem;
            }

            .stats-grid {
              grid-template-columns: repeat(2, 1fr);
            }

            .pools-grid {
              grid-template-columns: 1fr;
            }

            .pool-metrics {
              grid-template-columns: 1fr;
              gap: 0.5rem;
            }
          }
        `}</style>
      </div>
    </Layout>
  );
}
// pages/portfolio.js
import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';

export default function Portfolio() {
  const [portfolioData, setPortfolioData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Mock portfolio data - replace with actual API call
    const fetchPortfolio = async () => {
      try {
        setLoading(true);
        // Simulated API call delay
        await new Promise((resolve) => setTimeout(resolve, 1000));

        const mockData = {
          totalValue: 125847.32,
          dailyChange: 2.47,
          totalGain: 15847.32,
          positions: [
            {
              id: 1,
              symbol: 'AAPL',
              name: 'Apple Inc.',
              quantity: 50,
              avgPrice: 175.23,
              currentPrice: 182.41,
              value: 9120.5,
              gainLoss: 359.0,
              gainLossPercent: 4.09,
            },
            {
              id: 2,
              symbol: 'MSFT',
              name: 'Microsoft Corp',
              quantity: 30,
              avgPrice: 340.15,
              currentPrice: 348.22,
              value: 10446.6,
              gainLoss: 242.1,
              gainLossPercent: 2.37,
            },
            {
              id: 3,
              symbol: 'GOOGL',
              name: 'Alphabet Inc',
              quantity: 25,
              avgPrice: 138.45,
              currentPrice: 141.28,
              value: 3532.0,
              gainLoss: 70.75,
              gainLossPercent: 2.04,
            },
          ],
          recentTrades: [
            {
              id: 1,
              symbol: 'NVDA',
              action: 'BUY',
              quantity: 10,
              price: 875.23,
              timestamp: '2024-01-15T10:30:00Z',
              status: 'Executed',
            },
            {
              id: 2,
              symbol: 'TSLA',
              action: 'SELL',
              quantity: 5,
              price: 248.45,
              timestamp: '2024-01-15T09:15:00Z',
              status: 'Executed',
            },
          ],
        };

        setPortfolioData(mockData);
      } catch (err) {
        setError('Failed to load portfolio data');
      } finally {
        setLoading(false);
      }
    };

    fetchPortfolio();
  }, []);

  if (loading) {
    return (
      <Layout>
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading portfolio...</p>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div className="error-container">
          <p>⚠️ {error}</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="portfolio-page">
        <header className="page-header">
          <h1>📊 Portfolio Overview</h1>
          <p>Track your investments and trading performance</p>
        </header>

        <div className="portfolio-summary">
          <div className="summary-card total-value">
            <h3>Total Portfolio Value</h3>
            <p className="value">
              $
              {portfolioData.totalValue.toLocaleString('en-US', {
                minimumFractionDigits: 2,
              })}
            </p>
            <p className={`change ${portfolioData.dailyChange >= 0 ? 'positive' : 'negative'}`}>
              {portfolioData.dailyChange >= 0 ? '↗️' : '↘️'} {portfolioData.dailyChange}% today
            </p>
          </div>

          <div className="summary-card total-gain">
            <h3>Total Gain/Loss</h3>
            <p className={`value ${portfolioData.totalGain >= 0 ? 'positive' : 'negative'}`}>
              $
              {Math.abs(portfolioData.totalGain).toLocaleString('en-US', {
                minimumFractionDigits: 2,
              })}
            </p>
            <p className="change">All time performance</p>
          </div>
        </div>

        <div className="positions-section">
          <h2>Current Positions</h2>
          <div className="positions-table">
            <div className="table-header">
              <span>Symbol</span>
              <span>Quantity</span>
              <span>Avg Price</span>
              <span>Current Price</span>
              <span>Value</span>
              <span>Gain/Loss</span>
            </div>
            {portfolioData.positions.map((position) => (
              <div key={position.id} className="table-row">
                <div className="symbol-cell">
                  <span className="symbol">{position.symbol}</span>
                  <span className="name">{position.name}</span>
                </div>
                <span>{position.quantity}</span>
                <span>${position.avgPrice.toFixed(2)}</span>
                <span>${position.currentPrice.toFixed(2)}</span>
                <span>
                  $
                  {position.value.toLocaleString('en-US', {
                    minimumFractionDigits: 2,
                  })}
                </span>
                <div className={`gain-loss ${position.gainLoss >= 0 ? 'positive' : 'negative'}`}>
                  <span>${Math.abs(position.gainLoss).toFixed(2)}</span>
                  <span>
                    ({position.gainLossPercent >= 0 ? '+' : ''}
                    {position.gainLossPercent}%)
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="trades-section">
          <h2>Recent Trades</h2>
          <div className="trades-list">
            {portfolioData.recentTrades.map((trade) => (
              <div key={trade.id} className="trade-item">
                <div className="trade-symbol">
                  <span className={`action ${trade.action.toLowerCase()}`}>{trade.action}</span>
                  <span className="symbol">{trade.symbol}</span>
                </div>
                <div className="trade-details">
                  <span>
                    {trade.quantity} shares @ ${trade.price}
                  </span>
                  <span className="timestamp">
                    {new Date(trade.timestamp).toLocaleDateString()}{' '}
                    {new Date(trade.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                <span className={`status ${trade.status.toLowerCase()}`}>{trade.status}</span>
              </div>
            ))}
          </div>
        </div>

        <style jsx>{`
          .portfolio-page {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
          }

          .page-header {
            margin-bottom: 3rem;
            text-align: center;
            padding-bottom: 2rem;
            border-bottom: 2px solid #e2e8f0;
          }

          .page-header h1 {
            margin: 0;
            color: #2d3748;
            font-size: 2.5rem;
          }

          .page-header p {
            margin: 1rem 0 0 0;
            color: #718096;
            font-size: 1.2rem;
          }

          .loading-container,
          .error-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 300px;
            text-align: center;
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
            0% {
              transform: rotate(0deg);
            }
            100% {
              transform: rotate(360deg);
            }
          }

          .portfolio-summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
          }

          .summary-card {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
            text-align: center;
          }

          .summary-card h3 {
            margin: 0 0 1rem 0;
            color: #4a5568;
            font-size: 1.1rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
          }

          .summary-card .value {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
            color: #2d3748;
          }

          .summary-card .change {
            margin: 0.5rem 0 0 0;
            font-size: 0.9rem;
          }

          .positive {
            color: #48bb78;
          }

          .negative {
            color: #f56565;
          }

          .positions-section,
          .trades-section {
            margin-bottom: 3rem;
          }

          .positions-section h2,
          .trades-section h2 {
            margin: 0 0 1.5rem 0;
            color: #2d3748;
            font-size: 1.5rem;
          }

          .positions-table {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
          }

          .table-header {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr 1.5fr 1.5fr;
            gap: 1rem;
            padding: 1rem 1.5rem;
            background: #f7fafc;
            font-weight: 600;
            color: #4a5568;
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 0.5px;
          }

          .table-row {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr 1.5fr 1.5fr;
            gap: 1rem;
            padding: 1.5rem;
            border-top: 1px solid #e2e8f0;
            align-items: center;
          }

          .symbol-cell {
            display: flex;
            flex-direction: column;
          }

          .symbol {
            font-weight: 600;
            color: #2d3748;
          }

          .name {
            font-size: 0.9rem;
            color: #718096;
          }

          .gain-loss {
            display: flex;
            flex-direction: column;
            font-weight: 600;
          }

          .trades-list {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
          }

          .trade-item {
            display: grid;
            grid-template-columns: 2fr 3fr 1fr;
            gap: 1rem;
            padding: 1.5rem;
            border-bottom: 1px solid #e2e8f0;
            align-items: center;
          }

          .trade-item:last-child {
            border-bottom: none;
          }

          .trade-symbol {
            display: flex;
            align-items: center;
            gap: 1rem;
          }

          .action {
            padding: 0.25rem 0.75rem;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
          }

          .action.buy {
            background: #c6f6d5;
            color: #22543d;
          }

          .action.sell {
            background: #fed7d7;
            color: #742a2a;
          }

          .trade-details {
            display: flex;
            flex-direction: column;
          }

          .timestamp {
            font-size: 0.9rem;
            color: #718096;
          }

          .status {
            text-align: center;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.9rem;
          }

          .status.executed {
            background: #c6f6d5;
            color: #22543d;
          }

          @media (max-width: 768px) {
            .portfolio-page {
              padding: 0 1rem;
            }

            .table-header,
            .table-row {
              grid-template-columns: 1fr;
              text-align: left;
            }

            .trade-item {
              grid-template-columns: 1fr;
              text-align: left;
            }
          }
        `}</style>
      </div>
    </Layout>
  );
}

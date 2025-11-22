// pages/treasury.js
import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { apiClient } from '../lib/api';

export default function Treasury() {
  const [treasuryData, setTreasuryData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showNewTransaction, setShowNewTransaction] = useState(false);
  const [newTransaction, setNewTransaction] = useState({
    stream: 'deposit',
    amount: '',
    currency: 'USD',
    source: '',
  });

  useEffect(() => {
    fetchTreasuryData();
  }, []);

  const fetchTreasuryData = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getTreasury();
      setTreasuryData(data);
    } catch (err) {
      setError('Failed to load treasury data');
      console.error('Error fetching treasury:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTransaction = async (e) => {
    e.preventDefault();
    
    try {
      const transactionData = {
        ...newTransaction,
        amount: parseFloat(newTransaction.amount),
        status: 'completed'
      };

      await apiClient.createTreasuryTransaction(transactionData);
      
      // Reset form and refresh data
      setNewTransaction({ stream: 'deposit', amount: '', currency: 'USD', source: '' });
      setShowNewTransaction(false);
      fetchTreasuryData();
    } catch (err) {
      setError('Failed to create transaction');
      console.error('Error creating transaction:', err);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading treasury data...</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="treasury-page">
        <header className="page-header">
          <h1>💰 Treasury Management</h1>
          <p>Monitor balances and manage treasury transactions</p>
          <button 
            onClick={() => setShowNewTransaction(true)}
            className="primary-button"
          >
            + New Transaction
          </button>
        </header>

        {error && (
          <div className="error-message">
            <p>{error}</p>
            <button onClick={fetchTreasuryData}>Retry</button>
          </div>
        )}

        {/* Balance Overview */}
        {treasuryData?.treasury?.balances && (
          <section className="balances-section">
            <h2>💵 Current Balances</h2>
            <div className="balances-grid">
              {Object.entries(treasuryData.treasury.balances).map(([currency, amount]) => (
                <div key={currency} className="balance-card">
                  <h3>{currency}</h3>
                  <p className="balance-amount">
                    {currency === 'USD' ? '$' : ''}{amount.toLocaleString()}
                    {currency !== 'USD' && <span className="currency"> {currency}</span>}
                  </p>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Treasury Summary */}
        {treasuryData?.treasury?.summary && (
          <section className="summary-section">
            <h2>📊 Treasury Summary</h2>
            <div className="summary-grid">
              <div className="summary-card">
                <h4>Total Value (USD)</h4>
                <p className="summary-value">
                  ${treasuryData.treasury.summary.total_value_usd.toLocaleString()}
                </p>
              </div>
              <div className="summary-card">
                <h4>Daily Change</h4>
                <p className={`summary-value ${treasuryData.treasury.summary.daily_change >= 0 ? 'positive' : 'negative'}`}>
                  {treasuryData.treasury.summary.daily_change >= 0 ? '+' : ''}
                  {treasuryData.treasury.summary.daily_change.toFixed(2)}%
                </p>
              </div>
              <div className="summary-card">
                <h4>Monthly Change</h4>
                <p className={`summary-value ${treasuryData.treasury.summary.monthly_change >= 0 ? 'positive' : 'negative'}`}>
                  {treasuryData.treasury.summary.monthly_change >= 0 ? '+' : ''}
                  {treasuryData.treasury.summary.monthly_change.toFixed(2)}%
                </p>
              </div>
            </div>
          </section>
        )}

        {/* Recent Transactions */}
        {treasuryData?.treasury?.recent_transactions && (
          <section className="transactions-section">
            <h2>📋 Recent Transactions</h2>
            <div className="transactions-table">
              <table>
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Type</th>
                    <th>Amount</th>
                    <th>Currency</th>
                    <th>Source</th>
                  </tr>
                </thead>
                <tbody>
                  {treasuryData.treasury.recent_transactions.map((transaction) => (
                    <tr key={transaction.id}>
                      <td>{new Date(transaction.timestamp).toLocaleDateString()}</td>
                      <td>
                        <span className={`transaction-type ${transaction.type}`}>
                          {transaction.type}
                        </span>
                      </td>
                      <td className={`amount ${transaction.amount >= 0 ? 'positive' : 'negative'}`}>
                        {transaction.amount >= 0 ? '+' : ''}
                        ${Math.abs(transaction.amount).toLocaleString()}
                      </td>
                      <td>{transaction.currency}</td>
                      <td>{transaction.source}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}

        {/* New Transaction Modal */}
        {showNewTransaction && (
          <div className="modal-overlay">
            <div className="modal">
              <h3>Create New Transaction</h3>
              <form onSubmit={handleCreateTransaction}>
                <div className="form-group">
                  <label>Transaction Type</label>
                  <select
                    value={newTransaction.stream}
                    onChange={(e) => setNewTransaction({...newTransaction, stream: e.target.value})}
                    required
                  >
                    <option value="deposit">Deposit</option>
                    <option value="withdrawal">Withdrawal</option>
                    <option value="transfer">Transfer</option>
                  </select>
                </div>
                
                <div className="form-group">
                  <label>Amount</label>
                  <input
                    type="number"
                    step="0.01"
                    value={newTransaction.amount}
                    onChange={(e) => setNewTransaction({...newTransaction, amount: e.target.value})}
                    placeholder="0.00"
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label>Currency</label>
                  <select
                    value={newTransaction.currency}
                    onChange={(e) => setNewTransaction({...newTransaction, currency: e.target.value})}
                    required
                  >
                    <option value="USD">USD</option>
                    <option value="USDC">USDC</option>
                    <option value="ETH">ETH</option>
                    <option value="BTC">BTC</option>
                  </select>
                </div>
                
                <div className="form-group">
                  <label>Source</label>
                  <input
                    type="text"
                    value={newTransaction.source}
                    onChange={(e) => setNewTransaction({...newTransaction, source: e.target.value})}
                    placeholder="Transaction source"
                    required
                  />
                </div>
                
                <div className="form-actions">
                  <button type="button" onClick={() => setShowNewTransaction(false)}>
                    Cancel
                  </button>
                  <button type="submit" className="primary-button">
                    Create Transaction
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        <style jsx>{`
          .treasury-page {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
          }

          .page-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #e2e8f0;
          }

          .page-header h1 {
            margin: 0;
            color: #2d3748;
            font-size: 2rem;
          }

          .page-header p {
            margin: 0.5rem 0 0 0;
            color: #718096;
          }

          .primary-button {
            background: #667eea;
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.3s ease;
          }

          .primary-button:hover {
            background: #5a67d8;
          }

          .balances-section, .summary-section, .transactions-section {
            margin-bottom: 3rem;
          }

          .balances-section h2, .summary-section h2, .transactions-section h2 {
            margin-bottom: 1.5rem;
            color: #2d3748;
          }

          .balances-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
          }

          .balance-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            border: 1px solid #e2e8f0;
          }

          .balance-card h3 {
            margin: 0 0 0.5rem 0;
            color: #4a5568;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
          }

          .balance-amount {
            margin: 0;
            font-size: 1.8rem;
            font-weight: 700;
            color: #2d3748;
          }

          .currency {
            font-size: 1rem;
            color: #718096;
          }

          .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
          }

          .summary-card {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
          }

          .summary-card h4 {
            margin: 0 0 0.5rem 0;
            color: #718096;
            font-size: 0.9rem;
          }

          .summary-value {
            margin: 0;
            font-size: 1.5rem;
            font-weight: 700;
          }

          .summary-value.positive {
            color: #38a169;
          }

          .summary-value.negative {
            color: #e53e3e;
          }

          .transactions-table {
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
          }

          table {
            width: 100%;
            border-collapse: collapse;
          }

          th, td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
          }

          th {
            background: #f7fafc;
            font-weight: 600;
            color: #4a5568;
          }

          .transaction-type {
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.8rem;
            text-transform: uppercase;
            font-weight: 600;
          }

          .transaction-type.deposit {
            background: #c6f6d5;
            color: #276749;
          }

          .transaction-type.withdrawal {
            background: #fed7d7;
            color: #c53030;
          }

          .amount.positive {
            color: #38a169;
          }

          .amount.negative {
            color: #e53e3e;
          }

          .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
          }

          .modal {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            width: 90%;
            max-width: 500px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
          }

          .modal h3 {
            margin: 0 0 1.5rem 0;
            color: #2d3748;
          }

          .form-group {
            margin-bottom: 1.5rem;
          }

          .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            color: #4a5568;
            font-weight: 500;
          }

          .form-group input,
          .form-group select {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            font-size: 1rem;
          }

          .form-actions {
            display: flex;
            gap: 1rem;
            justify-content: flex-end;
          }

          .form-actions button {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 500;
          }

          .form-actions button[type="button"] {
            background: #edf2f7;
            color: #4a5568;
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
            .treasury-page {
              padding: 0 1rem;
            }

            .page-header {
              flex-direction: column;
              align-items: flex-start;
              gap: 1rem;
            }

            .balances-grid, .summary-grid {
              grid-template-columns: 1fr;
            }

            .transactions-table {
              overflow-x: auto;
            }

            table {
              min-width: 600px;
            }
          }
        `}</style>
      </div>
    </Layout>
  );
}
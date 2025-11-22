// components/Layout.js
import Link from 'next/link';
import { useRouter } from 'next/router';
import { useState, useEffect } from 'react';
import { apiClient } from '../lib/api';

export default function Layout({ children }) {
  const router = useRouter();
  const [isConnected, setIsConnected] = useState(false);
  const [isChecking, setIsChecking] = useState(true);

  useEffect(() => {
    const checkApiConnection = async () => {
      try {
        const connected = await apiClient.checkConnection();
        setIsConnected(connected);
      } catch (error) {
        setIsConnected(false);
      } finally {
        setIsChecking(false);
      }
    };

    checkApiConnection();
    
    // Check connection every 30 seconds
    const interval = setInterval(checkApiConnection, 30000);
    return () => clearInterval(interval);
  }, []);

  const navigationItems = [
    { href: '/', label: 'Dashboard', icon: '🏠' },
    { href: '/treasury', label: 'Treasury', icon: '💰' },
    { href: '/store', label: 'Store', icon: '🏪' },
    { href: '/signals', label: 'Signals', icon: '📡' },
    { href: '/amm', label: 'AMM', icon: '🌊' },
    { href: '/portfolio', label: 'Portfolio', icon: '📊' },
    { href: '/ledger', label: 'Ledger', icon: '📋' },
  ];

  return (
    <div className="layout">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <Link href="/" className="logo">
            <span className="logo-icon">🚀</span>
            <span className="logo-text">Codex Dominion</span>
          </Link>

          <div className="header-status">
            {isChecking ? (
              <div className="status-indicator checking">
                <span className="status-dot"></span>
                <span>Checking...</span>
              </div>
            ) : (
              <div className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
                <span className="status-dot"></span>
                <span>{isConnected ? 'API Connected' : 'API Disconnected'}</span>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="navigation">
        <div className="nav-content">
          {navigationItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`nav-item ${router.pathname === item.href ? 'active' : ''}`}
            >
              <span className="nav-icon">{item.icon}</span>
              <span className="nav-label">{item.label}</span>
            </Link>
          ))}
        </div>
      </nav>

      {/* Main content */}
      <main className="main-content">
        {!isConnected && !isChecking && (
          <div className="api-warning">
            <h3>⚠️ API Connection Issue</h3>
            <p>
              Unable to connect to the Codex Ledger API. 
              Please ensure the FastAPI service is running on port 8001.
            </p>
            <button 
              onClick={() => window.location.reload()}
              className="retry-button"
            >
              Retry Connection
            </button>
          </div>
        )}
        {children}
      </main>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <p>&copy; 2025 Codex Dominion. Advanced Trading Platform.</p>
          <div className="footer-links">
            <a href="/docs" target="_blank">API Docs</a>
            <a href="http://127.0.0.1:8001/docs" target="_blank">FastAPI Docs</a>
          </div>
        </div>
      </footer>

      <style jsx>{`
        .layout {
          min-height: 100vh;
          display: flex;
          flex-direction: column;
          background: #f7fafc;
        }

        /* Header Styles */
        .header {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 1rem 0;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        .header-content {
          max-width: 1200px;
          margin: 0 auto;
          padding: 0 2rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .logo {
          display: flex;
          align-items: center;
          text-decoration: none;
          color: white;
          font-size: 1.5rem;
          font-weight: 700;
        }

        .logo-icon {
          margin-right: 0.5rem;
          font-size: 2rem;
        }

        .status-indicator {
          display: flex;
          align-items: center;
          font-size: 0.9rem;
          padding: 0.5rem 1rem;
          border-radius: 20px;
          background: rgba(255,255,255,0.1);
        }

        .status-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          margin-right: 0.5rem;
        }

        .status-indicator.connected .status-dot {
          background: #48bb78;
          animation: pulse 2s infinite;
        }

        .status-indicator.disconnected .status-dot {
          background: #f56565;
        }

        .status-indicator.checking .status-dot {
          background: #ed8936;
          animation: blink 1s infinite;
        }

        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }

        @keyframes blink {
          0%, 50% { opacity: 1; }
          51%, 100% { opacity: 0.3; }
        }

        /* Navigation Styles */
        .navigation {
          background: white;
          border-bottom: 1px solid #e2e8f0;
          padding: 1rem 0;
        }

        .nav-content {
          max-width: 1200px;
          margin: 0 auto;
          padding: 0 2rem;
          display: flex;
          gap: 2rem;
          overflow-x: auto;
        }

        .nav-item {
          display: flex;
          align-items: center;
          text-decoration: none;
          color: #718096;
          padding: 0.5rem 1rem;
          border-radius: 8px;
          transition: all 0.3s ease;
          white-space: nowrap;
        }

        .nav-item:hover {
          background: #edf2f7;
          color: #2d3748;
        }

        .nav-item.active {
          background: #667eea;
          color: white;
        }

        .nav-icon {
          margin-right: 0.5rem;
          font-size: 1.2rem;
        }

        .nav-label {
          font-weight: 500;
        }

        /* Main Content */
        .main-content {
          flex: 1;
          padding: 2rem 0;
        }

        .api-warning {
          max-width: 1200px;
          margin: 0 auto 2rem auto;
          padding: 1.5rem 2rem;
          background: #fed7d7;
          border: 1px solid #feb2b2;
          border-radius: 8px;
          color: #c53030;
        }

        .api-warning h3 {
          margin: 0 0 0.5rem 0;
          font-size: 1.1rem;
        }

        .api-warning p {
          margin: 0 0 1rem 0;
          line-height: 1.5;
        }

        .retry-button {
          background: #c53030;
          color: white;
          border: none;
          padding: 0.5rem 1rem;
          border-radius: 6px;
          cursor: pointer;
          font-weight: 500;
          transition: background 0.3s ease;
        }

        .retry-button:hover {
          background: #9c2626;
        }

        /* Footer */
        .footer {
          background: #2d3748;
          color: white;
          padding: 2rem 0;
          margin-top: auto;
        }

        .footer-content {
          max-width: 1200px;
          margin: 0 auto;
          padding: 0 2rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .footer-links {
          display: flex;
          gap: 1rem;
        }

        .footer-links a {
          color: #cbd5e0;
          text-decoration: none;
          font-size: 0.9rem;
        }

        .footer-links a:hover {
          color: white;
        }

        /* Mobile Styles */
        @media (max-width: 768px) {
          .header-content {
            padding: 0 1rem;
          }

          .nav-content {
            padding: 0 1rem;
            gap: 1rem;
          }

          .footer-content {
            padding: 0 1rem;
            flex-direction: column;
            gap: 1rem;
            text-align: center;
          }

          .api-warning {
            margin: 0 1rem 2rem 1rem;
            padding: 1rem;
          }
        }
      `}</style>
    </div>
  );
}
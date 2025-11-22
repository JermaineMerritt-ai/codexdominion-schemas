// pages/store.js
import Layout from '../components/Layout';

export default function Store() {
  return (
    <Layout>
      <div className="store-page">
        <header className="page-header">
          <h1>🏪 AI Store Lab</h1>
          <p>Marketplace for AI tools and trading resources</p>
        </header>

        <div className="coming-soon">
          <div className="coming-soon-content">
            <h2>🚧 Coming Soon</h2>
            <p>The AI Store Lab marketplace is currently under development.</p>
            <p>This will be your one-stop shop for:</p>
            
            <ul className="features-list">
              <li>✨ Premium trading algorithms</li>
              <li>🤖 AI-powered market analysis tools</li>
              <li>📊 Custom dashboard widgets</li>
              <li>🔧 Trading automation scripts</li>
              <li>📚 Educational resources and courses</li>
              <li>🎯 Exclusive signal packages</li>
            </ul>

            <div className="notify-section">
              <h3>Get Notified</h3>
              <p>Be the first to know when we launch!</p>
              <div className="notify-form">
                <input 
                  type="email" 
                  placeholder="Enter your email"
                  className="email-input"
                />
                <button className="notify-button">
                  Notify Me
                </button>
              </div>
            </div>
          </div>
        </div>

        <style jsx>{`
          .store-page {
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

          .coming-soon {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 400px;
          }

          .coming-soon-content {
            background: white;
            padding: 3rem;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 600px;
          }

          .coming-soon-content h2 {
            margin: 0 0 1rem 0;
            color: #2d3748;
            font-size: 2rem;
          }

          .coming-soon-content p {
            margin: 1rem 0;
            color: #4a5568;
            line-height: 1.6;
          }

          .features-list {
            text-align: left;
            margin: 2rem 0;
            padding: 0;
            list-style: none;
          }

          .features-list li {
            margin: 0.75rem 0;
            color: #2d3748;
            font-size: 1.1rem;
          }

          .notify-section {
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid #e2e8f0;
          }

          .notify-section h3 {
            margin: 0 0 0.5rem 0;
            color: #2d3748;
          }

          .notify-form {
            display: flex;
            gap: 1rem;
            margin-top: 1.5rem;
            max-width: 400px;
            margin-left: auto;
            margin-right: auto;
          }

          .email-input {
            flex: 1;
            padding: 0.75rem 1rem;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            font-size: 1rem;
          }

          .notify-button {
            background: #667eea;
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.3s ease;
          }

          .notify-button:hover {
            background: #5a67d8;
          }

          @media (max-width: 768px) {
            .store-page {
              padding: 0 1rem;
            }

            .coming-soon-content {
              padding: 2rem 1.5rem;
            }

            .notify-form {
              flex-direction: column;
            }
          }
        `}</style>
      </div>
    </Layout>
  );
}
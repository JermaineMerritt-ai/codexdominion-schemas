import { useEffect, useState } from 'react';

interface Signal {
  symbol: string;
  tier: string;
  target_weight: number;
  rationale: string;
  risk_factors: string[];
}

interface SignalsSnapshot {
  timestamp: string;
  picks: Signal[];
  summary: {
    total_picks: number;
    by_tier: Record<string, number>;
  };
}

export default function SignalsEnhancedContent() {
  const [snapshot, setSnapshot] = useState<SignalsSnapshot | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadSignals() {
      try {
        setLoading(true);
        setError(null);

        // Mock data for demonstration
        const mockSnapshot: SignalsSnapshot = {
          timestamp: new Date().toISOString(),
          picks: [
            {
              symbol: 'MSFT',
              tier: 'Alpha',
              target_weight: 0.08,
              rationale: 'Strong fundamentals with AI momentum',
              risk_factors: ['Market volatility', 'Regulatory changes'],
            },
            {
              symbol: 'AAPL',
              tier: 'Beta',
              target_weight: 0.06,
              rationale: 'Stable growth with new product cycle',
              risk_factors: ['Supply chain risks', 'Competition'],
            },
            {
              symbol: 'ETH-USD',
              tier: 'Gamma',
              target_weight: 0.04,
              rationale: 'Cryptocurrency with smart contract platform',
              risk_factors: ['High volatility', 'Regulatory uncertainty'],
            },
          ],
          summary: {
            total_picks: 3,
            by_tier: { Alpha: 1, Beta: 1, Gamma: 1, Delta: 0 },
          },
        };

        setSnapshot(mockSnapshot);
      } catch (err) {
        console.error('Error loading signals:', err);
        setError(err instanceof Error ? err.message : 'Failed to load signals');
      } finally {
        setLoading(false);
      }
    }

    loadSignals();
  }, []);

  if (loading) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center' }}>
        <h2>Loading Signals...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '2rem', color: 'red' }}>
        <h2>Error</h2>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>Signals Dashboard - Enhanced</h1>

      {snapshot && (
        <>
          <div style={{ marginBottom: '2rem' }}>
            <h2>Summary</h2>
            <p>Total Picks: {snapshot.summary.total_picks}</p>
            <p>Timestamp: {new Date(snapshot.timestamp).toLocaleString()}</p>
            <div>
              {Object.entries(snapshot.summary.by_tier).map(([tier, count]) => (
                <span key={tier} style={{ marginRight: '1rem' }}>
                  {tier}: {count}
                </span>
              ))}
            </div>
          </div>

          <div>
            <h2>Signals</h2>
            {snapshot.picks.map((signal) => (
              <div
                key={signal.symbol}
                style={{
                  border: '1px solid #ccc',
                  borderRadius: '8px',
                  padding: '1rem',
                  marginBottom: '1rem',
                  backgroundColor: '#f9f9f9',
                }}
              >
                <h3>{signal.symbol} - {signal.tier}</h3>
                <p><strong>Target Weight:</strong> {(signal.target_weight * 100).toFixed(1)}%</p>
                <p><strong>Rationale:</strong> {signal.rationale}</p>
                <div>
                  <strong>Risk Factors:</strong>
                  <ul>
                    {signal.risk_factors.map((risk, idx) => (
                      <li key={idx}>{risk}</li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

import { useState, useEffect } from 'react';
import Head from 'next/head';

interface Metric {
  name: string;
  value: number;
  change: number;
  unit: string;
}

export default function ObservatoryHome() {
  const [metrics, setMetrics] = useState<Metric[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchMetrics = async () => {
    try {
      const response = await fetch('/api/metrics');
      const data = await response.json();
      setMetrics(data.metrics);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch metrics:', error);
    }
  };

  return (
    <>
      <Head>
        <title>Analytics Observatory - Codex Dominion</title>
      </Head>
      <div style={{ 
        minHeight: '100vh',
        backgroundColor: '#0f172a',
        color: '#f8fafc',
        fontFamily: 'system-ui, -apple-system, sans-serif'
      }}>
        <header style={{ 
          padding: '1rem 2rem',
          borderBottom: '1px solid #334155',
          backgroundColor: '#1e293b'
        }}>
          <h1 style={{ margin: 0, fontSize: '1.5rem' }}>
            📊 Analytics Observatory
          </h1>
          <p style={{ margin: '0.25rem 0 0 0', color: '#94a3b8', fontSize: '0.875rem' }}>
            Sovereign Analytics Service - Real-time System Insights
          </p>
        </header>

        <main style={{ padding: '2rem' }}>
          {loading ? (
            <div style={{ textAlign: 'center', padding: '4rem', color: '#64748b' }}>
              Loading metrics...
            </div>
          ) : (
            <>
              <div style={{ 
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                gap: '1.5rem',
                marginBottom: '2rem'
              }}>
                {metrics.map((metric, idx) => (
                  <div
                    key={idx}
                    style={{
                      backgroundColor: '#1e293b',
                      padding: '1.5rem',
                      borderRadius: '0.5rem',
                      border: '1px solid #334155'
                    }}
                  >
                    <div style={{ color: '#94a3b8', fontSize: '0.875rem', marginBottom: '0.5rem' }}>
                      {metric.name}
                    </div>
                    <div style={{ fontSize: '2rem', fontWeight: 700, marginBottom: '0.5rem' }}>
                      {metric.value.toFixed(2)}{metric.unit}
                    </div>
                    <div style={{ 
                      color: metric.change >= 0 ? '#10b981' : '#ef4444',
                      fontSize: '0.875rem'
                    }}>
                      {metric.change >= 0 ? '↑' : '↓'} {Math.abs(metric.change).toFixed(2)}%
                    </div>
                  </div>
                ))}
              </div>

              <div style={{
                backgroundColor: '#1e293b',
                padding: '1.5rem',
                borderRadius: '0.5rem',
                border: '1px solid #334155'
              }}>
                <h2 style={{ margin: '0 0 1rem 0', fontSize: '1.25rem' }}>System Status</h2>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  <StatusItem label="Council Seal" status="OPERATIONAL" health={100} />
                  <StatusItem label="Sovereigns (4)" status="OPERATIONAL" health={98} />
                  <StatusItem label="Custodians (4)" status="OPERATIONAL" health={99} />
                  <StatusItem label="Agents (4)" status="OPERATIONAL" health={97} />
                </div>
              </div>
            </>
          )}
        </main>
      </div>
    </>
  );
}

function StatusItem({ label, status, health }: { label: string; status: string; health: number }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <span>{label}</span>
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <span style={{ color: '#10b981', fontSize: '0.875rem' }}>{status}</span>
        <div style={{ 
          width: '100px',
          height: '8px',
          backgroundColor: '#334155',
          borderRadius: '4px',
          overflow: 'hidden'
        }}>
          <div style={{
            width: `${health}%`,
            height: '100%',
            backgroundColor: health > 80 ? '#10b981' : health > 50 ? '#f59e0b' : '#ef4444',
            transition: 'width 0.3s'
          }} />
        </div>
        <span style={{ fontSize: '0.875rem', color: '#94a3b8' }}>{health}%</span>
      </div>
    </div>
  );
}

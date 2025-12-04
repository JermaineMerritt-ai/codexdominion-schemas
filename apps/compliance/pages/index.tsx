import { useState, useEffect } from 'react';
import Head from 'next/head';

interface AuditLog {
  id: string;
  timestamp: string;
  actor: string;
  action: string;
  resource: string;
  status: string;
  severity: string;
}

export default function ComplianceHome() {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLogs();
  }, [filter]);

  const fetchLogs = async () => {
    try {
      const response = await fetch(`/api/audit?filter=${filter}`);
      const data = await response.json();
      setLogs(data.logs);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch logs:', error);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return '#ef4444';
      case 'high': return '#f59e0b';
      case 'medium': return '#3b82f6';
      case 'low': return '#10b981';
      default: return '#64748b';
    }
  };

  return (
    <>
      <Head>
        <title>Compliance & Audit - Codex Dominion</title>
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
            🛡️ Compliance & Audit System
          </h1>
          <p style={{ margin: '0.25rem 0 0 0', color: '#94a3b8', fontSize: '0.875rem' }}>
            Sovereign Compliance Service - Governance & Oversight
          </p>
        </header>

        <main style={{ padding: '2rem' }}>
          <div style={{ marginBottom: '1.5rem', display: 'flex', gap: '1rem' }}>
            <button
              onClick={() => setFilter('all')}
              style={{
                padding: '0.5rem 1rem',
                backgroundColor: filter === 'all' ? '#3b82f6' : '#334155',
                color: '#f8fafc',
                border: 'none',
                borderRadius: '0.375rem',
                cursor: 'pointer'
              }}
            >
              All
            </button>
            <button
              onClick={() => setFilter('critical')}
              style={{
                padding: '0.5rem 1rem',
                backgroundColor: filter === 'critical' ? '#ef4444' : '#334155',
                color: '#f8fafc',
                border: 'none',
                borderRadius: '0.375rem',
                cursor: 'pointer'
              }}
            >
              Critical
            </button>
            <button
              onClick={() => setFilter('high')}
              style={{
                padding: '0.5rem 1rem',
                backgroundColor: filter === 'high' ? '#f59e0b' : '#334155',
                color: '#f8fafc',
                border: 'none',
                borderRadius: '0.375rem',
                cursor: 'pointer'
              }}
            >
              High
            </button>
          </div>

          {loading ? (
            <div style={{ textAlign: 'center', padding: '4rem', color: '#64748b' }}>
              Loading audit logs...
            </div>
          ) : (
            <div style={{
              backgroundColor: '#1e293b',
              borderRadius: '0.5rem',
              border: '1px solid #334155',
              overflow: 'hidden'
            }}>
              <div style={{
                display: 'grid',
                gridTemplateColumns: '180px 150px 1fr 150px 100px 100px',
                padding: '1rem',
                backgroundColor: '#0f172a',
                fontWeight: 600,
                fontSize: '0.875rem',
                borderBottom: '1px solid #334155'
              }}>
                <div>Timestamp</div>
                <div>Actor</div>
                <div>Action</div>
                <div>Resource</div>
                <div>Status</div>
                <div>Severity</div>
              </div>
              {logs.map((log) => (
                <div
                  key={log.id}
                  style={{
                    display: 'grid',
                    gridTemplateColumns: '180px 150px 1fr 150px 100px 100px',
                    padding: '1rem',
                    borderBottom: '1px solid #334155',
                    fontSize: '0.875rem'
                  }}
                >
                  <div style={{ color: '#94a3b8' }}>{log.timestamp}</div>
                  <div>{log.actor}</div>
                  <div>{log.action}</div>
                  <div style={{ color: '#94a3b8' }}>{log.resource}</div>
                  <div style={{ color: log.status === 'SUCCESS' ? '#10b981' : '#ef4444' }}>
                    {log.status}
                  </div>
                  <div>
                    <span style={{
                      padding: '0.25rem 0.5rem',
                      borderRadius: '0.25rem',
                      backgroundColor: getSeverityColor(log.severity),
                      fontSize: '0.75rem',
                      textTransform: 'uppercase',
                      fontWeight: 600
                    }}>
                      {log.severity}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </main>
      </div>
    </>
  );
}

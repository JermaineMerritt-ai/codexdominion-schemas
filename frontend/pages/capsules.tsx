// pages/capsules.tsx
import React from "react";
import { GetServerSideProps } from "next";

interface Capsule {
  slug: string;
  title: string;
  kind: string;
  mode: string;
  version: string;
  status: string;
  entrypoint: string;
  schedule?: string;
  created_at: string;
  updated_at: string;
}

interface CapsuleRun {
  id: number;
  capsule_slug: string;
  actor: string;
  status: string;
  started_at: string;
  artifact_uri?: string;
  checksum?: string;
}

interface CapsulesProps {
  capsules: Capsule[];
  runs: CapsuleRun[];
  error?: string;
}

export default function Capsules({ capsules = [], runs = [], error }: CapsulesProps) {
  const formatDateTime = (dateStr: string) => {
    return new Date(dateStr).toLocaleString();
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success': return '#10b981';
      case 'error': return '#ef4444';
      case 'running': return '#f59e0b';
      default: return '#6b7280';
    }
  };

  const getModeColor = (mode: string) => {
    switch (mode) {
      case 'automated': return '#3b82f6';
      case 'custodian': return '#8b5cf6';
      case 'manual': return '#6b7280';
      default: return '#6b7280';
    }
  };

  if (error) {
    return (
      <div style={{ padding: 24 }}>
        <h1>Codex Capsules</h1>
        <div style={{ color: '#ef4444', padding: 16, backgroundColor: '#fef2f2', borderRadius: 8 }}>
          <strong>Error:</strong> {error}
        </div>
      </div>
    );
  }

  return (
    <div style={{ padding: 24, fontFamily: 'system-ui, sans-serif' }}>
      <div style={{ marginBottom: 32 }}>
        <h1 style={{ margin: 0, color: '#1f2937', fontSize: '2rem' }}>
          🏛️ Codex Capsules Registry
        </h1>
        <p style={{ color: '#6b7280', margin: '8px 0 0 0' }}>
          Operational sovereignty tracking for ceremonial and technical operations
        </p>
      </div>

      {/* Capsules Section */}
      <section style={{ marginBottom: 48 }}>
        <h2 style={{ 
          color: '#374151', 
          borderBottom: '2px solid #e5e7eb', 
          paddingBottom: 8,
          marginBottom: 16 
        }}>
          📦 Registered Capsules ({capsules.length})
        </h2>
        
        {capsules.length === 0 ? (
          <p style={{ color: '#6b7280', fontStyle: 'italic' }}>No capsules registered yet.</p>
        ) : (
          <div style={{ display: 'grid', gap: 16 }}>
            {capsules.map((c) => (
              <div 
                key={c.slug}
                style={{
                  border: '1px solid #e5e7eb',
                  borderRadius: 8,
                  padding: 16,
                  backgroundColor: '#fff'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: 8 }}>
                  <h3 style={{ margin: 0, color: '#1f2937' }}>{c.title}</h3>
                  <span style={{
                    backgroundColor: c.status === 'active' ? '#dcfce7' : '#fee2e2',
                    color: c.status === 'active' ? '#166534' : '#991b1b',
                    padding: '4px 8px',
                    borderRadius: 4,
                    fontSize: '0.75rem',
                    fontWeight: 'bold'
                  }}>
                    {c.status.toUpperCase()}
                  </span>
                </div>
                
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 12, fontSize: '0.875rem' }}>
                  <div>
                    <strong>Slug:</strong> <code style={{ backgroundColor: '#f3f4f6', padding: '2px 4px', borderRadius: 2 }}>{c.slug}</code>
                  </div>
                  <div>
                    <strong>Kind:</strong> {c.kind}
                  </div>
                  <div>
                    <strong>Mode:</strong> 
                    <span style={{
                      color: getModeColor(c.mode),
                      fontWeight: 'bold',
                      marginLeft: 4
                    }}>
                      {c.mode}
                    </span>
                  </div>
                  <div>
                    <strong>Version:</strong> {c.version}
                  </div>
                  <div>
                    <strong>Schedule:</strong> {c.schedule || '—'}
                  </div>
                </div>
                
                {c.entrypoint && (
                  <div style={{ marginTop: 8, fontSize: '0.875rem' }}>
                    <strong>Entrypoint:</strong> 
                    <code style={{ 
                      backgroundColor: '#f3f4f6', 
                      padding: '2px 4px', 
                      borderRadius: 2,
                      marginLeft: 4,
                      fontSize: '0.75rem'
                    }}>
                      {c.entrypoint}
                    </code>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Recent Runs Section */}
      <section>
        <h2 style={{ 
          color: '#374151', 
          borderBottom: '2px solid #e5e7eb', 
          paddingBottom: 8,
          marginBottom: 16 
        }}>
          🚀 Recent Execution Runs ({runs.length})
        </h2>
        
        {runs.length === 0 ? (
          <p style={{ color: '#6b7280', fontStyle: 'italic' }}>No execution runs recorded yet.</p>
        ) : (
          <div style={{ display: 'grid', gap: 12 }}>
            {runs.slice(0, 20).map((r, i) => (
              <div 
                key={i}
                style={{
                  border: '1px solid #e5e7eb',
                  borderRadius: 6,
                  padding: 12,
                  backgroundColor: '#fafafa',
                  fontSize: '0.875rem'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
                  <div>
                    <strong>{r.capsule_slug}</strong> executed by <em>{r.actor}</em>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span style={{
                      color: getStatusColor(r.status),
                      fontWeight: 'bold'
                    }}>
                      ●
                    </span>
                    <span style={{ color: '#6b7280' }}>
                      {formatDateTime(r.started_at)}
                    </span>
                  </div>
                </div>
                
                {r.artifact_uri && (
                  <div style={{ color: '#6b7280', fontSize: '0.75rem' }}>
                    📦 Artifact: 
                    <a 
                      href={r.artifact_uri} 
                      style={{ color: '#3b82f6', textDecoration: 'none', marginLeft: 4 }}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      {r.artifact_uri.split('/').pop()}
                    </a>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

export const getServerSideProps: GetServerSideProps = async () => {
  try {
    // Try to fetch from the capsules API
    const capsulesResponse = await fetch("http://localhost:8080/api/capsules", {
      method: 'GET',
      headers: { 'Accept': 'application/json' }
    });
    
    const runsResponse = await fetch("http://localhost:8080/api/capsules/runs", {
      method: 'GET', 
      headers: { 'Accept': 'application/json' }
    });

    let capsules: Capsule[] = [];
    let runs: CapsuleRun[] = [];

    if (capsulesResponse.ok && runsResponse.ok) {
      capsules = await capsulesResponse.json();
      runs = await runsResponse.json();
    } else {
      // Fallback to mock data
      capsules = [
        {
          slug: "signals-daily",
          title: "Daily Signals Engine",
          kind: "engine",
          mode: "custodian",
          version: "2.0.0",
          status: "active",
          entrypoint: "POST https://codex-signals.run.app/signals/daily",
          schedule: "0 6 * * *",
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }
      ];
      runs = [
        {
          id: 1,
          capsule_slug: "signals-daily",
          actor: "system-scheduler",
          status: "success",
          started_at: new Date().toISOString(),
          artifact_uri: "https://storage.googleapis.com/codex-artifacts/signals-daily-20251108.tar.gz"
        }
      ];
    }

    return {
      props: {
        capsules,
        runs
      }
    };
  } catch (error) {
    console.error("Error fetching capsules data:", error);
    
    // Return mock data on error
    return {
      props: {
        capsules: [
          {
            slug: "signals-daily",
            title: "Daily Signals Engine (Demo)",
            kind: "engine",
            mode: "custodian",
            version: "2.0.0",
            status: "active",
            entrypoint: "POST https://codex-signals.run.app/signals/daily",
            schedule: "0 6 * * *",
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
          }
        ],
        runs: [
          {
            id: 1,
            capsule_slug: "signals-daily",
            actor: "system-scheduler",
            status: "success",
            started_at: new Date().toISOString(),
            artifact_uri: "https://storage.googleapis.com/codex-artifacts/signals-daily-demo.tar.gz"
          }
        ],
        error: "Could not connect to Capsules API - showing demo data"
      }
    };
  }
};
interface Artifact {
  title: string;
  generated_at: string;
  execution_id?: string;
  status?: string;
  tier_counts: {
    Alpha: number;
    Beta: number;
    Gamma: number;
    Delta: number;
  };
  picks: Array<{
    symbol: string;
    tier: string;
    target_weight: number;
    rationale: string;
    risk_factors?: string[];
  }>;
}
import { useRouter } from 'next/router';
import React, { useEffect, useState } from 'react';
import CapsuleView from '../../components/CapsuleView';
import styles from './capsule-slug.module.css';

export default function CapsulePage() {
  const router = useRouter();
  const { slug } = router.query;
  interface Artifact {
    title: string;
    generated_at: string;
    execution_id?: string;
    status?: string;
    tier_counts: {
      Alpha: number;
      Beta: number;
      Gamma: number;
      Delta: number;
    };
    picks: Array<{
      symbol: string;
      tier: string;
      target_weight: number;
      rationale: string;
      risk_factors?: string[];
    }>;
  }
  const [artifact, setArtifact] = useState<Artifact | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [userRole, setUserRole] = useState('heir'); // Default role

  useEffect(() => {
    if (!slug || typeof slug !== 'string') return;

    async function loadArtifact() {
      try {
        setLoading(true);
        setError(null);

        // Fetch from our backend API
        const res = await fetch(`/api/artifacts/${slug}/latest`);

        if (!res.ok) {
          throw new Error(`Failed to load artifact: ${res.status} ${res.statusText}`);
        }

        const data = await res.json();
        setArtifact(data);
      } catch (err) {
        console.error('Error loading artifact:', err);
        setError(err instanceof Error ? err.message : 'Unknown error occurred');
      } finally {
        setLoading(false);
      }
    }

    loadArtifact();
  }, [slug]);

  if (loading) {
    return (
      <div className={styles.container}>
        <div className={styles.loadingContainer}>
          <div className={styles.spinner}></div>
          <p>Loading capsule artifact for {slug}...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.container}>
        <div className={styles.errorContainer}>
          <h1>❌ Error Loading Capsule</h1>
          <p>
            <strong>Capsule:</strong> {slug}
          </p>
          <p className={styles.errorMessage}>{error}</p>
          <button onClick={() => router.back()} className={styles.backButton}>
            ← Back to Capsules
          </button>
        </div>
      </div>
    );
  }

  if (!artifact) {
    return (
      <div className={styles.container}>
        <p>No artifact found for capsule: {slug}</p>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className="capsule-header">
        <button onClick={() => router.back()} className="back-button">
          ← Back
        </button>
        <h1>{artifact.title}</h1>
        <div className="meta-info">
          <p>
            <strong>Capsule:</strong> <code>{slug}</code>
          </p>
          <p>
            <strong>Generated:</strong> {new Date(artifact.generated_at).toLocaleString()}
          </p>
          {artifact.execution_id && (
            <p>
              <strong>Execution ID:</strong> <code>{artifact.execution_id}</code>
            </p>
          )}
          {artifact.status && (
            <p>
              <strong>Status:</strong>
              <span className={`status-badge ${artifact.status}`}>
                {artifact.status.toUpperCase()}
              </span>
            </p>
          )}
        </div>
      </div>

      <div className="role-selector">
        <label htmlFor="role-select">View Mode:</label>
        <select
          id="role-select"
          value={userRole}
          onChange={(e) => setUserRole(e.target.value)}
          className="role-dropdown"
        >
          <option value="heir">Heir View</option>
          <option value="customer">Customer View</option>
          <option value="custodian">Custodian View</option>
        </select>
      </div>

      <div className="capsule-view-container">
        <CapsuleView artifact={artifact} role={userRole} />
      </div>

      <div className="content-grid">
        <div className="tier-section">
          <h2>🎯 Tier Distribution</h2>
          <div className="tier-counts">
            <div className="tier-item alpha">
              <span className="tier-label">Alpha</span>
              <span className="tier-count">{artifact.tier_counts.Alpha}</span>
            </div>
            <div className="tier-item beta">
              <span className="tier-label">Beta</span>
              <span className="tier-count">{artifact.tier_counts.Beta}</span>
            </div>
            <div className="tier-item gamma">
              <span className="tier-label">Gamma</span>
              <span className="tier-count">{artifact.tier_counts.Gamma}</span>
            </div>
            <div className="tier-item delta">
              <span className="tier-label">Delta</span>
              <span className="tier-count">{artifact.tier_counts.Delta}</span>
            </div>
          </div>
        </div>

        <div className="picks-section">
          <h2>📊 Investment Picks</h2>
          <div className="picks-grid">
            {artifact.picks.map((pick, i) => (
              <div key={i} className="pick-card">
                <div className="pick-header">
                  <h3 className="symbol">{pick.symbol}</h3>
                  <div className="pick-meta">
                    <span className={`tier-badge tier-${pick.tier.toLowerCase()}`}>
                      {pick.tier}
                    </span>
                    <span className="weight">{(pick.target_weight * 100).toFixed(2)}%</span>
                  </div>
                </div>

                <div className="rationale">
                  <strong>Rationale:</strong>
                  <p>{pick.rationale}</p>
                </div>

                {pick.risk_factors && pick.risk_factors.length > 0 && (
                  <div className="risks">
                    <strong>Risk Factors:</strong>
                    <ul>
                      {pick.risk_factors.map((risk, idx) => (
                        <li key={idx}>{risk}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      <style jsx>{`
        .capsule-header {
          border-bottom: 2px solid #e1e5e9;
          padding-bottom: 1.5rem;
          margin-bottom: 2rem;
        }

        .back-button {
          background: #6c757d;
          color: white;
          border: none;
          padding: 0.5rem 1rem;
          border-radius: 4px;
          cursor: pointer;
          margin-bottom: 1rem;
          font-size: 0.9rem;
        }

        .back-button:hover {
          background: #5a6268;
        }

        .role-selector {
          display: flex;
          align-items: center;
          interface Artifact {
            title: string;
            generated_at: string;
            execution_id?: string;
            status?: string;
            tier_counts: {
              Alpha: number;
              Beta: number;
              Gamma: number;
              Delta: number;
            };
            picks: Array<{
              symbol: string;
              tier: string;
              target_weight: number;
              rationale: string;
              risk_factors?: string[];
            }>;
          }
          gap: 1rem;
          margin-bottom: 2rem;
          padding: 1rem;
          background: #f8f9fa;
          border-radius: 8px;
        }

        .role-dropdown {
          padding: 0.5rem;
        }

        .meta-info p {
          margin: 0.25rem 0;
          color: #6c757d;
        }

        .meta-info code {
          background: #f8f9fa;
          padding: 0.2rem 0.4rem;
          border-radius: 3px;
          font-family: "Courier New", monospace;
        }

        .status-badge {
          padding: 0.2rem 0.5rem;
          border-radius: 3px;
          font-size: 0.8rem;
          font-weight: bold;
          margin-left: 0.5rem;
        }

        .status-badge.success {
          background: #d4edda;
          color: #155724;
        }

        .banner-section {
          background: #f8f9fa;
          padding: 1.5rem;
          border-radius: 8px;
          border-left: 4px solid #0070f3;
          margin-bottom: 2rem;
        }

        .banner-section blockquote {
          margin: 0;
          font-size: 1.1rem;
          font-style: italic;
          color: #495057;
        }

        .content-grid {
          display: grid;
          grid-template-columns: 1fr 2fr;
          gap: 2rem;
        }

        @media (max-width: 768px) {
          .content-grid {
            grid-template-columns: 1fr;
          }
          .meta-info {
            flex-direction: column;
            gap: 0.5rem;
          }
        }

        .tier-section h2,
        .picks-section h2 {
          color: #343a40;
          border-bottom: 1px solid #dee2e6;
          padding-bottom: 0.5rem;
        }

        .tier-counts {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 1rem;
          margin-top: 1rem;
        }

        .tier-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 1rem;
          border-radius: 6px;
          font-weight: bold;
        }

        .tier-item.alpha {
          background: #fff3cd;
          border-left: 4px solid #ffc107;
        }

        .tier-item.beta {
          background: #d1ecf1;
          border-left: 4px solid #17a2b8;
        }

        .tier-item.gamma {
          background: #d4edda;
          border-left: 4px solid #28a745;
        }

        .tier-item.delta {
          background: #f8d7da;
          border-left: 4px solid #dc3545;
        }

        .tier-count {
          font-size: 1.25rem;
        }

        .picks-grid {
          display: flex;
          flex-direction: column;
          gap: 1rem;
          margin-top: 1rem;
        }

        .pick-card {
          border: 1px solid #dee2e6;
          border-radius: 8px;
          padding: 1.5rem;
          background: white;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .pick-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1rem;
        }

        .symbol {
          margin: 0;
          font-size: 1.25rem;
          font-family: monospace;
          color: #0070f3;
        }

        .pick-meta {
          display: flex;
          align-items: center;
          gap: 1rem;
        }

        .tier-badge {
          padding: 0.25rem 0.5rem;
          border-radius: 4px;
          font-size: 0.8rem;
          font-weight: bold;
          text-transform: uppercase;
        }

        .tier-badge.tier-alpha {
          background: #ffc107;
          color: #856404;
        }

        .tier-badge.tier-beta {
          background: #17a2b8;
          color: white;
        }

        .tier-badge.tier-gamma {
          background: #28a745;
          color: white;
        }

        .tier-badge.tier-delta {
          background: #dc3545;
          color: white;
        }

        .weight {
          font-size: 1.1rem;
          font-weight: bold;
          color: #495057;
        }

        .rationale,
        .risks {
          margin-top: 1rem;
        }

        .rationale p,
        .risks ul {
          margin-top: 0.5rem;
          color: #6c757d;
        }

        .risks ul {
          padding-left: 1.25rem;
        }

        .risks li {
          margin-bottom: 0.25rem;
        }
      `}</style>
    </div>
  );
}

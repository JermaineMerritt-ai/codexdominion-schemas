import { useEffect, useState } from 'react';
import styled from 'styled-components';
import Link from 'next/link';

interface Capsule {
  slug: string;
  name: string;
  description: string;
  schedule: string;
  archive_type: string;
}

const Container = styled.div`
  padding: 24px;
`;

export default function CapsulesWithLinks() {
  const [capsules, setCapsules] = useState<Capsule[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadCapsules() {
      try {
        setLoading(true);
        // Try local API first, fallback to external service
        const response = await fetch('/api/capsules');
        if (!response.ok) {
          throw new Error('Local API unavailable');
        }
        const data = await response.json();
        setCapsules(data.capsules || []);
      } catch (localError) {
        console.log('Local API unavailable, trying external service...');
        try {
          const externalResponse = await fetch('http://localhost:8080/api/capsules');
          const externalData = await externalResponse.json();
          // Map external data to our format
          const mappedCapsules = externalData.map((c: any) => ({
            slug: c.slug,
            name: c.title || c.slug,
            description: `External capsule: ${c.kind} mode ${c.mode}`,
            schedule: c.schedule || 'Not scheduled',
            archive_type: 'external',
          }));
          setCapsules(mappedCapsules);
        } catch (externalError) {
          console.error('Both APIs failed:', { localError, externalError });
          setError('Unable to load capsules from any source');
        }
      } finally {
        setLoading(false);
      }
    }
    loadCapsules();
  }, []);

  if (loading) {
    return (
      <Container>
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading capsules...</p>
        </div>
        <style jsx>{`
          .loading-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 2rem;
          }
          .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #0070f3;
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
        `}</style>
      </Container>
    );
  }

  if (error) {
    return (
      <Container>
        <h1>❌ Error Loading Capsules</h1>
        <p className="error-message">{error}</p>
        <style jsx>{`
          .error-message {
            color: #e74c3c;
            background: #fdf2f2;
            padding: 1rem;
            border-radius: 4px;
            border-left: 4px solid #e74c3c;
          }
        `}</style>
      </Container>
    );
  }

  return (
    <Container>
      <div className="header">
        <h1>🏛️ Codex Dominion Capsule Registry</h1>
        <p className="subtitle">Operational sovereignty through autonomous capsule execution</p>
      </div>
      <div className="stats-bar">
        <div className="stat">
          <span className="stat-number">{capsules.length}</span>
          <span className="stat-label">Active Capsules</span>
        </div>
        <div className="stat">
          <span className="stat-number">100%</span>
          <span className="stat-label">Operational</span>
        </div>
        <div className="stat">
          <span className="stat-number">24/7</span>
          <span className="stat-label">Monitoring</span>
        </div>
      </div>
      <div className="capsules-grid">
        {capsules.map((capsule) => (
          <Link key={capsule.slug} href={`/capsule/${capsule.slug}`}>
            <div className="capsule-card">
              <div className="capsule-header">
                <h3>{capsule.name}</h3>
                <span className={`archive-badge ${capsule.archive_type}`}>
                  {capsule.archive_type}
                </span>
              </div>
              <p className="description">{capsule.description}</p>
              <div className="capsule-meta">
                <div className="meta-item">
                  <span className="meta-label">Slug:</span>
                  <code>{capsule.slug}</code>
                </div>
                <div className="meta-item">
                  <span className="meta-label">Schedule:</span>
                  <code>{capsule.schedule}</code>
                </div>
              </div>
              <div className="action-area">
                <span className="view-link">View Latest Artifact →</span>
              </div>
            </div>
          </Link>
        ))}
      </div>
      <div className="footer-info">
        <p>
          💡 <strong>Tip:</strong> Click on any capsule to view its latest execution artifact and
          performance data.
        </p>
      </div>
      <style jsx>{`
        .header {
          text-align: center;
          margin-bottom: 2rem;
          border-bottom: 2px solid #e1e5e9;
          padding-bottom: 1.5rem;
        }
        .subtitle {
          color: #6c757d;
          font-size: 1.1rem;
          margin-top: 0.5rem;
        }
        .stats-bar {
          display: flex;
          justify-content: center;
          gap: 3rem;
          margin-bottom: 2rem;
          padding: 1.5rem;
          background: #f8f9fa;
          border-radius: 8px;
        }
        .stat {
          text-align: center;
        }
        .stat-number {
          display: block;
          font-size: 2rem;
          font-weight: bold;
          color: #0070f3;
        }
        .stat-label {
          font-size: 0.9rem;
          color: #6c757d;
          text-transform: uppercase;
        }
        .capsules-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
          gap: 1.5rem;
          margin-bottom: 2rem;
        }
        .capsule-card {
          border: 1px solid #dee2e6;
          border-radius: 8px;
          padding: 1.5rem;
          background: white;
          cursor: pointer;
          transition: all 0.2s ease;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .capsule-card:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
          border-color: #0070f3;
        }
        .capsule-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 1rem;
        }
        .capsule-header h3 {
          margin: 0;
          color: #343a40;
          font-size: 1.25rem;
        }
        .archive-badge {
          padding: 0.25rem 0.5rem;
          border-radius: 4px;
          font-size: 0.75rem;
          font-weight: bold;
          text-transform: uppercase;
        }
        .archive-badge.snapshot {
          background: #d1ecf1;
          color: #0c5460;
        }
        .archive-badge.bulletin {
          background: #d4edda;
          color: #155724;
        }
        .archive-badge.analysis_report {
          background: #fff3cd;
          color: #856404;
        }
        .archive-badge.external {
          background: #e2e3e5;
          color: #383d41;
        }
        .description {
          color: #6c757d;
          margin: 1rem 0;
          line-height: 1.5;
        }
        .capsule-meta {
          margin: 1rem 0;
        }
        .meta-item {
          display: flex;
          align-items: center;
          margin-bottom: 0.5rem;
        }
        .meta-label {
          font-weight: 500;
          margin-right: 0.5rem;
          min-width: 70px;
        }
        code {
          background: #f8f9fa;
          padding: 0.2rem 0.4rem;
          border-radius: 3px;
          font-family: 'Courier New', monospace;
          font-size: 0.9rem;
        }
        .action-area {
          border-top: 1px solid #e9ecef;
          padding-top: 1rem;
          margin-top: 1rem;
        }
        .view-link {
          color: #0070f3;
          font-weight: 500;
          font-size: 0.9rem;
        }
        .capsule-card:hover .view-link {
          text-decoration: underline;
        }
        .footer-info {
          text-align: center;
          padding: 1.5rem;
          background: #f8f9fa;
          border-radius: 8px;
          color: #6c757d;
        }
        @media (max-width: 768px) {
          .stats-bar {
            flex-direction: column;
            gap: 1rem;
          }
          .capsules-grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </Container>
  );
}

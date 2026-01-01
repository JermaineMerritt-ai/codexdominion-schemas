'use client';

import { useEffect, useState } from 'react';

const BASE_URL = "http://localhost:5000";

export default function HomePage() {
  const [workflowTypes, setWorkflowTypes] = useState({});
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadData() {
      try {
        const [typesRes, metricsRes] = await Promise.all([
          fetch(`${BASE_URL}/api/workflow-types`),
          fetch(`${BASE_URL}/api/workflows/metrics`)
        ]);
        
        if (!typesRes.ok || !metricsRes.ok) throw new Error('Failed to fetch');
        
        const types = await typesRes.json();
        const metricsData = await metricsRes.json();
        
        setWorkflowTypes(types);
        setMetrics(metricsData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) return <div style={{ padding: '2rem' }}>Loading...</div>;
  if (error) return <div style={{ padding: '2rem', color: 'red' }}>Error: {error}</div>;

  const typeCount = Object.keys(workflowTypes).length;

  return (
    <div style={{ minHeight: '100vh', background: '#0f172a', color: '#f1f5f9', padding: '2rem' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        {/* Header */}
        <div style={{ borderBottom: '1px solid #334155', paddingBottom: '1.5rem', marginBottom: '2rem' }}>
          <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#10b981', margin: '0 0 0.5rem 0' }}>
            🔥 Codex Dominion Workflows
          </h1>
          <p style={{ color: '#94a3b8', margin: 0 }}>Council Governance & Workflow Automation</p>
        </div>

        {/* Metrics */}
        {metrics && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
            <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '1.5rem' }}>
              <div style={{ color: '#94a3b8', fontSize: '0.875rem', marginBottom: '0.5rem' }}>Total Actions</div>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#10b981' }}>{metrics.total_actions}</div>
            </div>
            <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '1.5rem' }}>
              <div style={{ color: '#94a3b8', fontSize: '0.875rem', marginBottom: '0.5rem' }}>Completed</div>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#22c55e' }}>{metrics.status_counts.completed}</div>
            </div>
            <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '1.5rem' }}>
              <div style={{ color: '#94a3b8', fontSize: '0.875rem', marginBottom: '0.5rem' }}>Weekly Savings</div>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#10b981' }}>
                ${Math.round(metrics.total_savings.weekly).toLocaleString()}
              </div>
            </div>
            <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '1.5rem' }}>
              <div style={{ color: '#94a3b8', fontSize: '0.875rem', marginBottom: '0.5rem' }}>Yearly Savings</div>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#10b981' }}>
                ${Math.round(metrics.total_savings.yearly).toLocaleString()}
              </div>
            </div>
          </div>
        )}

        {/* Workflow Types */}
        <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem' }}>
          Available Workflow Types ({typeCount})
        </h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem' }}>
          {Object.entries(workflowTypes).map(([id, type]) => (
            <div key={id} style={{ 
              background: '#1e293b', 
              border: '1px solid #334155', 
              borderRadius: '8px', 
              padding: '1.5rem',
              transition: 'border-color 0.2s'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '0.75rem' }}>
                <h3 style={{ fontSize: '1.125rem', fontWeight: '600', margin: 0 }}>{type.name}</h3>
                <span style={{ 
                  fontSize: '0.75rem', 
                  padding: '0.25rem 0.5rem', 
                  borderRadius: '4px', 
                  background: 'rgba(16, 185, 129, 0.1)', 
                  color: '#10b981',
                  border: '1px solid rgba(16, 185, 129, 0.2)'
                }}>
                  {type.domain}
                </span>
              </div>
              <p style={{ color: '#94a3b8', fontSize: '0.875rem', margin: '0 0 1rem 0' }}>{type.description}</p>
              <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
                <div>Category: {type.category}</div>
                <div>Required Inputs: {type.required_inputs.length}</div>
                {metrics && metrics.actions_by_type[`create_workflow_${id}`] && (
                  <div style={{ color: '#10b981', marginTop: '0.5rem', paddingTop: '0.5rem', borderTop: '1px solid #334155' }}>
                    {metrics.actions_by_type[`create_workflow_${id}`]} active workflows
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div style={{ marginTop: '3rem', paddingTop: '1.5rem', borderTop: '1px solid #334155', textAlign: 'center', color: '#64748b', fontSize: '0.875rem' }}>
          <p>🔥 THE FLAME BURNS SOVEREIGN AND ETERNAL! 👑</p>
        </div>
      </div>
    </div>
  );
}

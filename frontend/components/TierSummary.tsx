// components/TierSummary.tsx
import React from 'react';

interface TierCounts {
  Alpha: number;
  Beta: number;
  Gamma: number;
  Delta: number;
}

interface TierSummaryProps {
  tierCounts: TierCounts;
  generatedAt: string;
  banner: string;
}

export const TierSummary: React.FC<TierSummaryProps> = ({ 
  tierCounts, 
  generatedAt, 
  banner 
}) => {
  const total = tierCounts.Alpha + tierCounts.Beta + tierCounts.Gamma + tierCounts.Delta;
  
  const tierData = [
    { name: 'Alpha', count: tierCounts.Alpha, color: '#10b981', description: 'High conviction' },
    { name: 'Beta', count: tierCounts.Beta, color: '#3b82f6', description: 'Balanced exposure' },
    { name: 'Gamma', count: tierCounts.Gamma, color: '#f59e0b', description: 'Elevated risk' },
    { name: 'Delta', count: tierCounts.Delta, color: '#ef4444', description: 'High turbulence' }
  ];

  return (
    <div style={{
      backgroundColor: '#1f2937',
      color: 'white',
      padding: '24px',
      borderRadius: '12px',
      marginBottom: '24px'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <h2 style={{ margin: 0, fontSize: '24px' }}>🔥 Codex Signals</h2>
        <div style={{ fontSize: '14px', opacity: 0.8 }}>
          {new Date(generatedAt).toLocaleString()}
        </div>
      </div>
      
      <div style={{
        backgroundColor: '#374151',
        padding: '12px',
        borderRadius: '8px',
        marginBottom: '20px',
        borderLeft: '4px solid #fbbf24'
      }}>
        <strong>📢 Market Banner:</strong> {banner}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '16px' }}>
        {tierData.map((tier) => (
          <div key={tier.name} style={{
            backgroundColor: '#374151',
            padding: '16px',
            borderRadius: '8px',
            textAlign: 'center',
            border: `2px solid ${tier.color}`
          }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: tier.color }}>
              {tier.count}
            </div>
            <div style={{ fontSize: '16px', fontWeight: 'bold', marginBottom: '4px' }}>
              {tier.name}
            </div>
            <div style={{ fontSize: '12px', opacity: 0.8 }}>
              {tier.description}
            </div>
            <div style={{ fontSize: '12px', opacity: 0.6, marginTop: '4px' }}>
              {total > 0 ? `${((tier.count / total) * 100).toFixed(1)}%` : '0%'}
            </div>
          </div>
        ))}
      </div>

      <div style={{ marginTop: '16px', textAlign: 'center', fontSize: '14px', opacity: 0.8 }}>
        <strong>Total Positions:</strong> {total} | 
        <strong> Portfolio Intelligence:</strong> Active |
        <strong> The Merritt Method™</strong> 👑
      </div>
    </div>
  );
};
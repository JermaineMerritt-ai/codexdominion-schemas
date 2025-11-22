// components/SignalsCard.tsx
import React from 'react';

type Pick = {
  symbol: string;
  tier: string;
  target_weight: number;
  rationale: string;
  risk_factors: string[];
};

interface SignalsCardProps {
  pick: Pick;
}

const tierColors = {
  Alpha: '#10b981', // green
  Beta: '#3b82f6',  // blue  
  Gamma: '#f59e0b', // orange
  Delta: '#ef4444'  // red
};

export const SignalsCard: React.FC<SignalsCardProps> = ({ pick }) => {
  const tierColor = tierColors[pick.tier as keyof typeof tierColors] || '#6b7280';
  
  return (
    <div style={{
      border: '1px solid #e5e7eb',
      borderRadius: '8px',
      padding: '16px',
      margin: '8px 0',
      backgroundColor: '#f9fafb',
      borderLeft: `4px solid ${tierColor}`
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
        <h3 style={{ margin: 0, fontSize: '18px', fontWeight: 'bold' }}>
          {pick.symbol}
        </h3>
        <div style={{
          backgroundColor: tierColor,
          color: 'white',
          padding: '4px 8px',
          borderRadius: '4px',
          fontSize: '12px',
          fontWeight: 'bold'
        }}>
          {pick.tier}
        </div>
      </div>
      
      <div style={{ marginBottom: '12px' }}>
        <strong>Target Weight:</strong> {(pick.target_weight * 100).toFixed(2)}%
      </div>
      
      <div style={{ marginBottom: '12px' }}>
        <strong>Rationale:</strong>
        <p style={{ margin: '4px 0 0 0', color: '#374151', fontSize: '14px' }}>
          {pick.rationale}
        </p>
      </div>
      
      {pick.risk_factors && pick.risk_factors.length > 0 && (
        <div>
          <strong>Risk Factors:</strong>
          <ul style={{ margin: '4px 0 0 0', paddingLeft: '16px' }}>
            {pick.risk_factors.map((risk, index) => (
              <li key={index} style={{ color: '#dc2626', fontSize: '14px' }}>
                {risk}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
// components/TierSummary.tsx
import React from 'react';
import styles from './TierSummary.module.css';

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
    <div className={styles.container}>
      <div className={styles.header}>
        <h2 className={styles.title}>🔥 Codex Signals</h2>
        <div className={styles.date}>{new Date(generatedAt).toLocaleString()}</div>
      </div>
      <div className={styles.banner}>
        <strong>📢 Market Banner:</strong> {banner}
      </div>
      <div className={styles.tierGrid}>
        {tierData.map((tier) => (
          <div
            key={tier.name}
            className={`${styles.tierCard} ${
              tier.name === 'Alpha' ? styles.tierAlpha :
              tier.name === 'Beta' ? styles.tierBeta :
              tier.name === 'Gamma' ? styles.tierGamma :
              tier.name === 'Delta' ? styles.tierDelta : ''
            }`}
          >
            <div className={`${styles.tierCount} ${
              tier.name === 'Alpha' ? styles.tierCountAlpha :
              tier.name === 'Beta' ? styles.tierCountBeta :
              tier.name === 'Gamma' ? styles.tierCountGamma :
              tier.name === 'Delta' ? styles.tierCountDelta : ''
            }`}>
              {tier.count}
            </div>
            <div className={styles.tierName}>{tier.name}</div>
            <div className={styles.tierDesc}>{tier.description}</div>
            <div className={styles.tierPercent}>
              {total > 0 ? `${((tier.count / total) * 100).toFixed(1)}%` : '0%'}
            </div>
          </div>
        ))}
      </div>
      <div className={styles.footer}>
        <strong>Total Positions:</strong> {total} | 
        <strong> Portfolio Intelligence:</strong> Active |
        <strong> The Merritt Method™</strong> 👑
      </div>
    </div>
  );
};
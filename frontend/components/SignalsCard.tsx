// components/SignalsCard.tsx
import React from 'react';
import styles from './SignalsCard.module.css';

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
  const borderClass =
    pick.tier === 'Alpha' ? styles.borderAlpha :
    pick.tier === 'Beta' ? styles.borderBeta :
    pick.tier === 'Gamma' ? styles.borderGamma :
    pick.tier === 'Delta' ? styles.borderDelta : '';
  const tierClass =
    pick.tier === 'Alpha' ? styles.tierAlpha :
    pick.tier === 'Beta' ? styles.tierBeta :
    pick.tier === 'Gamma' ? styles.tierGamma :
    pick.tier === 'Delta' ? styles.tierDelta : '';
  
  return (
    <div className={`${styles.card} ${borderClass}`}>
      <div className={styles.header}>
        <h3 className={styles.symbol}>{pick.symbol}</h3>
        <div className={`${styles.tier} ${tierClass}`}>
          {pick.tier}
        </div>
      </div>
      <div className={styles.targetWeight}>
        <strong>Target Weight:</strong> {(pick.target_weight * 100).toFixed(2)}%
      </div>
      <div className={styles.rationale}>
        <strong>Rationale:</strong>
        <p className={styles.rationaleText}>{pick.rationale}</p>
      </div>
      {pick.risk_factors && pick.risk_factors.length > 0 && (
        <div>
          <strong>Risk Factors:</strong>
          <ul className={styles.riskFactors}>
            {pick.risk_factors.map((risk, index) => (
              <li key={index} className={styles.riskItem}>
                {risk}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
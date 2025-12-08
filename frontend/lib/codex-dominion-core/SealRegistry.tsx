// SealRegistry - Lineage and timestamp tracking
import React, { useState, useEffect } from 'react';
import type { Seal } from './types';

interface SealRegistryProps {
  onSealSelect?: (seal: Seal) => void;
}

export const SealRegistry: React.FC<SealRegistryProps> = ({ onSealSelect }) => {
  const [seals, setSeals] = useState<Seal[]>([]);
  const [selectedSeal, setSelectedSeal] = useState<Seal | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Load seals
    const loadSeals = async () => {
      setIsLoading(true);

      // Mock data
      const mockSeals: Seal[] = [
        {
          id: 'seal-001',
          lineageTag: 'ETERNAL_COVENANT_ALPHA',
          timestamp: new Date('2024-01-15T10:30:00'),
        },
        {
          id: 'seal-002',
          lineageTag: 'RADIANT_DOMINION_BETA',
          timestamp: new Date('2024-02-20T14:45:00'),
        },
        {
          id: 'seal-003',
          lineageTag: 'SUPREME_ARCHIVE_GAMMA',
          timestamp: new Date('2024-03-10T08:15:00'),
        },
      ];

      setSeals(mockSeals);
      setIsLoading(false);
    };

    loadSeals();
  }, []);

  const handleSealClick = (seal: Seal) => {
    setSelectedSeal(seal);

    if (onSealSelect) {
      onSealSelect(seal);
    }
  };

  return (
    <div className="seal-registry">
      <header className="registry-header">
        <h2>🔱 Seal Registry</h2>
        <span className="seal-count">{seals.length} seals</span>
      </header>

      {isLoading ? (
        <div className="loading">Loading seals...</div>
      ) : (
        <div className="seal-grid">
          {seals.map((seal) => (
            <div
              key={seal.id}
              className={`seal-card ${selectedSeal?.id === seal.id ? 'selected' : ''}`}
              onClick={() => handleSealClick(seal)}
            >
              <div className="seal-icon">🔱</div>
              <div className="seal-content">
                <h3 className="seal-id">{seal.id}</h3>
                <p className="lineage-tag">{seal.lineageTag}</p>
                <span className="timestamp">{seal.timestamp.toLocaleString()}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {selectedSeal && (
        <div className="seal-details">
          <h3>Seal Details</h3>
          <dl>
            <dt>ID:</dt>
            <dd>{selectedSeal.id}</dd>
            <dt>Lineage Tag:</dt>
            <dd>{selectedSeal.lineageTag}</dd>
            <dt>Timestamp:</dt>
            <dd>{selectedSeal.timestamp.toLocaleString()}</dd>
          </dl>
        </div>
      )}
    </div>
  );
};

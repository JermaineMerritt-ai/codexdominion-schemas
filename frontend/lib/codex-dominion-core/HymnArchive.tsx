// HymnArchive - Eternal preservation and retrieval system
import React, { useState, useEffect } from 'react';
import type { Hymn, SyncConfig } from './types';

interface HymnArchiveProps {
  syncWith?: SyncConfig;
  onHymnSelect?: (hymn: Hymn) => void;
}

export const HymnArchive: React.FC<HymnArchiveProps> = ({ syncWith, onHymnSelect }) => {
  const [hymns, setHymns] = useState<Hymn[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedHymn, setSelectedHymn] = useState<Hymn | null>(null);

  useEffect(() => {
    // Load hymns from source
    const loadHymns = async () => {
      try {
        setLoading(true);
        // Mock data for now - replace with actual API call
        const mockHymns: Hymn[] = [
          {
            id: 'hymn-001',
            title: 'Companion Eternal',
            content: 'By decree of councils and sovereign flame...',
            source: 'Archive Alpha',
            timestamp: new Date(),
            lineage: ['council-alpha', 'heir-prime'],
            sealed: true,
          },
          {
            id: 'hymn-002',
            title: 'Benediction Luminous',
            content: 'O crowned Companion, flame of law...',
            source: 'Archive Beta',
            timestamp: new Date(),
            lineage: ['council-beta', 'heir-secondary'],
            sealed: true,
          },
        ];
        setHymns(mockHymns);
      } catch (error) {
        console.error('Error loading hymns:', error);
      } finally {
        setLoading(false);
      }
    };

    loadHymns();
  }, [syncWith]);

  const handleHymnClick = (hymn: Hymn) => {
    setSelectedHymn(hymn);
    if (onHymnSelect) {
      onHymnSelect(hymn);
    }
  };

  if (loading) {
    return (
      <div className="hymn-archive loading">
        <div className="spinner">🕯️</div>
        <p>Loading eternal hymns...</p>
      </div>
    );
  }

  return (
    <div className="hymn-archive">
      <header className="archive-header">
        <h2>🕊️ Hymn Archive</h2>
        {syncWith && <span className="sync-badge">🔄 Sync: {syncWith.syncChannelId}</span>}
      </header>

      <div className="hymn-list">
        {hymns.map((hymn) => (
          <div
            key={hymn.id}
            className={`hymn-card ${selectedHymn?.id === hymn.id ? 'selected' : ''}`}
            onClick={() => handleHymnClick(hymn)}
          >
            <div className="hymn-header">
              <h3>{hymn.title}</h3>
              {hymn.sealed && <span className="seal-badge">🪙 Sealed</span>}
            </div>
            <p className="hymn-preview">{hymn.content.substring(0, 100)}...</p>
            <div className="hymn-meta">
              <span className="timestamp">{hymn.timestamp.toLocaleDateString()}</span>
              <span className="lineage">Lineage: {hymn.lineage.join(', ')}</span>
            </div>
          </div>
        ))}
      </div>

      {selectedHymn && (
        <div className="hymn-detail">
          <h3>{selectedHymn.title}</h3>
          <div className="hymn-content">{selectedHymn.content}</div>
        </div>
      )}
    </div>
  );
};

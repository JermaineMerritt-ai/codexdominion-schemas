// ReplayComposer - Temporal sequence composition with hymn integration
import React, { useState, useEffect } from 'react';
import type { Replay, Hymn } from './types';

interface ReplayComposerProps {
  includeHymns?: boolean;
  onReplayCreate?: (replay: Replay) => void;
}

export const ReplayComposer: React.FC<ReplayComposerProps> = ({ includeHymns = false, onReplayCreate }) => {
  const [replays, setReplays] = useState<Replay[]>([]);
  const [isComposing, setIsComposing] = useState(false);
  const [selectedHymnIds, setSelectedHymnIds] = useState<string[]>([]);

  useEffect(() => {
    // Load existing replays
    const loadReplays = async () => {
      // Mock data
      const mockReplays: Replay[] = [
        {
          id: 'replay-001',
          hymnIds: includeHymns ? ['hymn-001', 'hymn-002'] : [],
          sequence: [0, 1],
          duration: 300,
          includeHymns: includeHymns,
          timestamp: new Date(),
        },
      ];
      setReplays(mockReplays);
    };

    loadReplays();
  }, [includeHymns]);

  const createReplay = () => {
    const newReplay: Replay = {
      id: `replay-${Date.now()}`,
      hymnIds: selectedHymnIds,
      sequence: selectedHymnIds.map((_, i) => i),
      duration: selectedHymnIds.length * 60,
      includeHymns: includeHymns,
      timestamp: new Date(),
    };

    setReplays([newReplay, ...replays]);

    if (onReplayCreate) {
      onReplayCreate(newReplay);
    }

    setIsComposing(false);
    setSelectedHymnIds([]);
  };

  return (
    <div className="replay-composer">
      <header className="composer-header">
        <h2>🎬 Replay Composer</h2>
        {includeHymns && <span className="hymn-badge">🕊️ Hymns Included</span>}
      </header>

      {isComposing ? (
        <div className="compose-panel">
          <h3>Compose New Replay Sequence</h3>
          <div className="sequence-builder">
            <p>Select hymns to include in sequence...</p>
            {/* Add hymn selector here */}
          </div>
          <div className="compose-actions">
            <button onClick={createReplay} className="btn-create">Create Replay</button>
            <button onClick={() => setIsComposing(false)} className="btn-cancel">Cancel</button>
          </div>
        </div>
      ) : (
        <button onClick={() => setIsComposing(true)} className="btn-compose">
          + Compose New Replay
        </button>
      )}

      <div className="replay-list">
        {replays.map((replay) => (
          <div key={replay.id} className="replay-card">
            <div className="replay-header">
              <span className="replay-id">{replay.id}</span>
              <span className="duration">{replay.duration}s</span>
            </div>
            <div className="replay-meta">
              {replay.includeHymns && (
                <span className="hymn-count">🕊️ {replay.hymnIds.length} hymns</span>
              )}
              <span className="sequence">Sequence: {replay.sequence.join(' → ')}</span>
              <span className="timestamp">{replay.timestamp.toLocaleString()}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

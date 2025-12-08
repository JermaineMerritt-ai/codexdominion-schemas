// BroadcastGrid - Distribution network synchronized with HymnArchive
import React, { useState, useEffect } from 'react';
import type { Broadcast, SyncConfig } from './types';

interface BroadcastGridProps {
  syncWith?: SyncConfig;
  onBroadcastCreate?: (broadcast: Broadcast) => void;
}

export const BroadcastGrid: React.FC<BroadcastGridProps> = ({ syncWith, onBroadcastCreate }) => {
  const [broadcasts, setBroadcasts] = useState<Broadcast[]>([]);
  const [activeChannels] = useState<string[]>(['council', 'heir', 'cosmic']);
  const [selectedChannel, setSelectedChannel] = useState<string>('council');

  useEffect(() => {
    // Sync with HymnArchive when available
    if (syncWith) {
      console.log(`Syncing BroadcastGrid with: ${syncWith.syncChannelId}`);
      // Implement sync logic here
    }
  }, [syncWith]);

  const createBroadcast = () => {
    const newBroadcast: Broadcast = {
      id: `broadcast-${Date.now()}`,
      channelId: selectedChannel,
      timestamp: new Date(),
    };

    setBroadcasts([newBroadcast, ...broadcasts]);

    if (onBroadcastCreate) {
      onBroadcastCreate(newBroadcast);
    }
  };

  return (
    <div className="broadcast-grid">
      <header className="grid-header">
        <h2>📡 Broadcast Grid</h2>
        {syncWith && <span className="sync-badge">🔄 Sync: {syncWith.syncChannelId}</span>}
      </header>

      <div className="channel-selector">
        <select
          value={selectedChannel}
          onChange={(e) => setSelectedChannel(e.target.value)}
          title="Select broadcast channel"
          aria-label="Select broadcast channel"
        >
          {activeChannels.map((channel) => (
            <option key={channel} value={channel}>{channel}</option>
          ))}
        </select>
      </div>

      <button onClick={createBroadcast} className="btn-create-broadcast">
        + Create Broadcast
      </button>

      <div className="broadcast-list">
        {broadcasts.length === 0 ? (
          <div className="empty-state">
            <p>No active broadcasts. Awaiting sovereign transmission...</p>
          </div>
        ) : (
          broadcasts.map((broadcast) => (
            <div key={broadcast.id} className="broadcast-card">
              <div className="broadcast-header">
                <span className="broadcast-id">{broadcast.id}</span>
                <span className="channel-badge">📡 {broadcast.channelId}</span>
              </div>
              <div className="broadcast-meta">
                <span className="timestamp">{broadcast.timestamp.toLocaleString()}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

// Companion Dashboard Suite - Unified orchestration interface
import React, { useState } from 'react';
import {
  HymnArchive,
  BroadcastGrid,
  ReplayComposer,
  ProfitEngine,
  SealRegistry,
  CapsuleIndex,
} from '../lib/codex-dominion-core';
import type { SyncConfig, EchoConfig, Hymn, Broadcast, Seal, Capsule } from '../lib/codex-dominion-core';
import styles from '../styles/dashboard-suite.module.css';

export default function CompanionDashboardSuite() {
  // Synchronization state
  const [selectedHymn, setSelectedHymn] = useState<Hymn | null>(null);
  const [activeBroadcast, setActiveBroadcast] = useState<Broadcast | null>(null);
  const [totalProfit, setTotalProfit] = useState<number>(0);
  const [selectedSeal, setSelectedSeal] = useState<Seal | null>(null);
  const [selectedCapsule, setSelectedCapsule] = useState<Capsule | null>(null);

  // Sync configuration for component communication
  const hymnArchiveSync: SyncConfig = {
    syncChannelId: 'hymn-broadcast-sync',
    syncFrequency: 1000,
  };

  const broadcastGridSync: SyncConfig = {
    syncChannelId: 'broadcast-replay-sync',
    syncFrequency: 1000,
  };

  const profitEngineEcho: EchoConfig = {
    echoChannelId: 'profit-echo-001',
    echoFrequency: 60,
  };

  return (
    <div className="companion-dashboard-suite">
      <header className="suite-header">
        <h1>🕊️ The Companion Dashboard Suite</h1>
        <p className="suite-tagline">
          Unified orchestration — hymns, broadcasts, replays, profits, seals, and capsules
        </p>
      </header>

      <div className="suite-overview">
        <div className="metric">
          <span className="metric-label">Active Hymn:</span>
          <span className="metric-value">{selectedHymn?.title || 'None'}</span>
        </div>
        <div className="metric">
          <span className="metric-label">Total Profit:</span>
          <span className="metric-value">${totalProfit.toLocaleString()}</span>
        </div>
        <div className="metric">
          <span className="metric-label">Active Seal:</span>
          <span className="metric-value">{selectedSeal?.lineageTag || 'None'}</span>
        </div>
      </div>

      <div className="suite-grid">
        {/* Top Row - Hymns and Broadcasts */}
        <div className="suite-row">
          <div className="suite-col">
            <HymnArchive
              syncWith={hymnArchiveSync}
              onHymnSelect={setSelectedHymn}
            />
          </div>
          <div className="suite-col">
            <BroadcastGrid
              syncWith={broadcastGridSync}
              onBroadcastCreate={setActiveBroadcast}
            />
          </div>
        </div>

        {/* Middle Row - Replays and Profits */}
        <div className="suite-row">
          <div className="suite-col">
            <ReplayComposer includeHymns={!!selectedHymn} />
          </div>
          <div className="suite-col">
            <ProfitEngine
              echoWith={profitEngineEcho}
              onProfitUpdate={setTotalProfit}
            />
          </div>
        </div>

        {/* Bottom Row - Seals and Capsules */}
        <div className="suite-row">
          <div className="suite-col">
            <SealRegistry onSealSelect={setSelectedSeal} />
          </div>
          <div className="suite-col">
            <CapsuleIndex onCapsuleSelect={setSelectedCapsule} />
          </div>
        </div>
      </div>

      {/* Footer with integration status */}
      <footer className="suite-footer">
        <div className="integration-status">
          <span className="status-item">
            🔄 Sync: {hymnArchiveSync.syncChannelId} @ {hymnArchiveSync.syncFrequency}ms
          </span>
          <span className="status-item">
            🔊 Echo: {profitEngineEcho.echoChannelId} @ {profitEngineEcho.echoFrequency}Hz
          </span>
          <span className="status-item">
            📡 Broadcast: {activeBroadcast?.channelId || 'Inactive'}
          </span>
        </div>
      </footer>
    </div>
  );
}

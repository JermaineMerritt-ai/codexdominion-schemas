import React, { useState } from 'react';
import Link from 'next/link';

export default function BroadcastCapsule() {
  const [targets, setTargets] = useState('council@codexdominion.org');
  const [status, setStatus] = useState<string | null>(null);
  const [assets, setAssets] = useState({
    welcomeBanner: 'Welcome, councils and heirs.',
    replayAnnouncement: 'The Capsule echoes now.',
    invocationScript: 'In the name of memory and flame...',
    cycleHymn: 'Cycle Hymn verses...',
    performanceGuide: 'Procession and reprise...'
  });

  async function dispatch() {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000'}/broadcast/dispatch`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ targets: targets.split(',').map(t => t.trim()), assets, schedule: { cycle: 'daily' } })
    });
    const json = await res.json();
    setStatus(`Dispatched act: ${json.act_id}`);
  }

  return (
    <main className="parchment">
      <header className="nav">
        <Link href="/">Home</Link>
        <Link href="/council">Council</Link>
        <Link href="/ai">AI Console</Link>
        <Link href="/copilot">Copilot Doc</Link>
        <Link href="/finance">Finance</Link>
        <Link href="/approvals">Approvals</Link>
        <Link href="/broadcast">Broadcast</Link>
        <Link href="/continuum">Continuum</Link>
        <Link href="/email">Email</Link>
        <Link href="/archive">Archive</Link>
      </header>
      <section>
        <h1>Broadcast Capsule</h1>
        <p>Dispatch ceremonial capsules across email, social channels, and portals.</p>
        <div className="form-container">
          <label className="form-label">
            Recipients (comma-separated emails or channels):
          </label>
          <input
            className="input-field"
            value={targets}
            onChange={e => setTargets(e.target.value)}
            placeholder="email@example.com, discord:channel, slack:general"
          />

          <label className="form-label">Welcome Banner:</label>
          <textarea
            className="textarea-field"
            value={assets.welcomeBanner}
            onChange={e => setAssets({...assets, welcomeBanner: e.target.value})}
          />

          <label className="form-label">Replay Announcement:</label>
          <textarea
            className="textarea-field"
            value={assets.replayAnnouncement}
            onChange={e => setAssets({...assets, replayAnnouncement: e.target.value})}
          />

          <label className="form-label">Invocation Script:</label>
          <textarea
            className="textarea-field"
            value={assets.invocationScript}
            onChange={e => setAssets({...assets, invocationScript: e.target.value})}
          />

          <label className="form-label">Cycle Hymn:</label>
          <textarea
            className="textarea-field"
            value={assets.cycleHymn}
            onChange={e => setAssets({...assets, cycleHymn: e.target.value})}
          />

          <label className="form-label">Performance Guide:</label>
          <textarea
            className="textarea-field"
            value={assets.performanceGuide}
            onChange={e => setAssets({...assets, performanceGuide: e.target.value})}
          />

          <button className="btn-primary" onClick={dispatch}>Dispatch Capsule</button>
          {status && <p className="status-message">{status}</p>}
        </div>
      </section>
    </main>
  );
}

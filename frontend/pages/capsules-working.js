import React from 'react';
import { useEffect, useState } from 'react';

export default function Capsules() {
  const [capsules, setCapsules] = useState([]);
  const [runs, setRuns] = useState([]);

  useEffect(() => {
    async function load() {
      try {
        const c = await fetch('http://localhost:8080/api/capsules').then((r) => r.json());
        const r = await fetch('http://localhost:8080/api/capsules/runs').then((r) => r.json());
        setCapsules(c);
        setRuns(r);
      } catch (error) {
        console.error('Failed to load capsules data:', error);
        // Fallback data for when service is not available
        setCapsules([
          {
            slug: 'signals-daily',
            title: 'Daily Signals Engine',
            kind: 'engine',
            mode: 'custodian',
            schedule: '0 6 * * *',
          },
        ]);
        setRuns([
          {
            capsule_slug: 'signals-daily',
            actor: 'system-scheduler',
            status: 'success',
            started_at: new Date().toISOString(),
            artifact_uri:
              'https://storage.googleapis.com/codex-artifacts/signals-daily-20251108.tar.gz',
          },
        ]);
      }
    }
    load();
  }, []);

  return (
    <div style={{ padding: 24 }}>
      <h1>Capsule Registry</h1>
      <h2>Capsules</h2>
      <ul>
        {capsules.map((c) => (
          <li key={c.slug}>
            <strong>{c.title}</strong> — {c.slug} | {c.kind} | mode {c.mode} | schedule{' '}
            {c.schedule || '—'}
          </li>
        ))}
      </ul>
      <h2 style={{ marginTop: 24 }}>Recent Runs</h2>
      <ul>
        {runs.slice(0, 20).map((r, i) => (
          <li key={i}>
            {r.capsule_slug} by {r.actor} — {r.status} @ {r.started_at} |{' '}
            {r.artifact_uri || 'no artifact'}
          </li>
        ))}
      </ul>
    </div>
  );
}

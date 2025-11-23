// pages/capsules-simple.tsx
import dynamic from 'next/dynamic';
import styles from './capsules-simple.module.css';
const Capsules = dynamic(() => import('../components/CapsulesSimple'), { ssr: false });
export default Capsules;

// ...existing code...
<div className={styles.container}>
  <h1>Capsule Registry</h1>
  <h2>Capsules</h2>
  <ul>
    {capsules.map((c) => (
      <li key={c.slug}>
        <strong>{c.title}</strong> — {c.slug} | {c.kind} | mode {c.mode} | schedule {c.schedule || "—"}
      </li>
    ))}
  </ul>
  <h2 className={styles.recentRuns}>Recent Runs</h2>
  <ul>
    {runs.slice(0, 20).map((r, i) => (
      <li key={i}>
        {r.capsule_slug} by {r.actor} — {r.status} @ {r.started_at} | {r.artifact_uri || "no artifact"}
      </li>
    ))}
  </ul>
</div>
// ...existing code...
// pages/capsules-simple.tsx
import dynamic from 'next/dynamic';
const Capsules = dynamic(() => import('../components/CapsulesSimple'), { ssr: false });
export default Capsules;
    <div style={{ padding: 24 }}>
      <h1>Capsule Registry</h1>
      <h2>Capsules</h2>
      <ul>
        {capsules.map((c) => (
          <li key={c.slug}>
            <strong>{c.title}</strong> — {c.slug} | {c.kind} | mode {c.mode} | schedule {c.schedule || "—"}
          </li>
        ))}
      </ul>
      <h2 style={{ marginTop: 24 }}>Recent Runs</h2>
      <ul>
        {runs.slice(0, 20).map((r, i) => (
          <li key={i}>
            {r.capsule_slug} by {r.actor} — {r.status} @ {r.started_at} | {r.artifact_uri || "no artifact"}
          </li>
        ))}
      </ul>
    </div>
  );
}
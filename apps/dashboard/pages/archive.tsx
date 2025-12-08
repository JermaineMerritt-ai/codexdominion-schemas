import React, { useEffect, useState } from 'react';
import Link from 'next/link';

export default function Archive() {
  const [groups, setGroups] = useState<Record<string, any[]> | null>(null);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000'}/ledger/index`)
      .then(r => r.json()).then(setGroups as any);
  }, []);

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
        <h1>Archive Portal</h1>
        <p>Sacred ledger of acts, seals, and lineage records.</p>
        {!groups ? <p className="loading-message">Loading archive...</p> :
          <div className="archive-container">
            {Object.entries(groups).map(([type, acts]) => (
              <div key={type} className="archive-section">
                <h2 className="archive-type">{type.toUpperCase()}</h2>
                <ul className="archive-list">
                  {acts.map((a: any) => (
                    <li key={a.id} className="archive-item">
                      <div className="archive-item-content">
                        <strong className="archive-title">{a.title}</strong>
                        <span className="archive-meta">
                          {a.status} • {a.cycle}
                        </span>
                      </div>
                      <button className="btn-secondary">Replay</button>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        }
      </section>
    </main>
  );
}

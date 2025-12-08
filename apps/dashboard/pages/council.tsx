import React from 'react';
import Link from 'next/link';

export default function Council() {
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
        <h1>Council Chamber</h1>
        <p>Strategic oversight and governance. View and manage council decisions.</p>
        <div style={{ marginTop: '2rem' }}>
          <h2>Recent Council Actions</h2>
          <p>No actions yet. Connect to API to view council activities.</p>
        </div>
      </section>
    </main>
  );
}

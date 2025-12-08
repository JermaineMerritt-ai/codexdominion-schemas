import React from 'react';
import Link from 'next/link';

export default function Continuum() {
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
        <h1>Continuum</h1>
        <p>Eternal timeline of cycles, epochs, and lineage.</p>
        <div style={{ marginTop: '2rem' }}>
          <h2>Current Cycle</h2>
          <p>Daily Cycle: Active</p>
          <p>Seasonal Cycle: Q4 2025</p>
          <p>Epochal Cycle: Genesis Era</p>
        </div>
      </section>
    </main>
  );
}

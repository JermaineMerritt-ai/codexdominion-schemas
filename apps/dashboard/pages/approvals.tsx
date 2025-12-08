import React from 'react';
import Link from 'next/link';

export default function Approvals() {
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
        <h1>Approvals</h1>
        <p>Review and approve prompts, acts, and ceremonial requests.</p>
        <div style={{ marginTop: '2rem' }}>
          <h2>Pending Approvals</h2>
          <p>No pending approvals. All systems clear.</p>
        </div>
      </section>
    </main>
  );
}

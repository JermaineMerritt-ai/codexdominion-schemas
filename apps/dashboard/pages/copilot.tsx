import React from 'react';
import Link from 'next/link';

export default function Copilot() {
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
        <h1>Copilot Documentation</h1>
        <p>AI assistant documentation and guides.</p>
        <div style={{ marginTop: '2rem' }}>
          <h2>Quick Start</h2>
          <p>Learn how to use the Codex Dominion Copilot for development.</p>
        </div>
      </section>
    </main>
  );
}

import React from 'react';
import Link from 'next/link';

export default function Home() {
  return (
    <main className="parchment">
      <header className="nav">
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
        <h1>Ceremonial Sovereign Dashboard</h1>
        <p>Unify councils, prompts, broadcasts, finance, and seals.</p>
      </section>
    </main>
  );
}

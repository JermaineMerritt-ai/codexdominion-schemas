import React from 'react';
import Link from 'next/link';

export default function Finance() {
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
        <h1>Finance Dashboard</h1>
        <p>Revenue tracking, MRR, and financial analytics.</p>
        <div style={{ marginTop: '2rem' }}>
          <h2>Revenue Summary</h2>
          <p>Total Revenue: $0.00</p>
          <p>MRR: $0.00</p>
          <p style={{ fontSize: '0.9rem', color: '#666' }}>Connect to API at {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000'} for live data.</p>
        </div>
      </section>
    </main>
  );
}

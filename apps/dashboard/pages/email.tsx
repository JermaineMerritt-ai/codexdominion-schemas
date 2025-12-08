import React from 'react';
import Link from 'next/link';

export default function Email() {
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
        <h1>Email Management</h1>
        <p>Ceremonial email campaigns and broadcast capsules.</p>
        <div style={{ marginTop: '2rem' }}>
          <h2>Recent Campaigns</h2>
          <p>No campaigns sent. Configure SendGrid integration.</p>
          <p style={{ fontSize: '0.9rem', color: '#666', marginTop: '1rem' }}>
            Set SENDGRID_API_KEY and EMAIL_FROM in environment variables.
          </p>
        </div>
      </section>
    </main>
  );
}

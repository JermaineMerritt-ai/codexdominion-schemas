import React, { useState } from 'react';
import Link from 'next/link';

export default function AIConsole() {
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');
  const [status, setStatus] = useState<string | null>(null);

  async function create() {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000'}/prompts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ dashboard_id: 'MAIN', title, body })
    });
    const json = await res.json();
    setStatus(`Prompt created: ${json.id}`);
  }

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
        <h1>Action AI Console</h1>
        <p>Create and manage AI prompts for automation.</p>
        <div className="form-container">
          <input
            className="input-field"
            placeholder="Prompt title"
            value={title}
            onChange={e => setTitle(e.target.value)}
          />
          <textarea
            className="textarea-field"
            placeholder="Prompt body"
            value={body}
            onChange={e => setBody(e.target.value)}
          />
          <button className="btn-primary" onClick={create}>Create Prompt</button>
          {status && <p className="status-message">{status}</p>}
        </div>
      </section>
    </main>
  );
}

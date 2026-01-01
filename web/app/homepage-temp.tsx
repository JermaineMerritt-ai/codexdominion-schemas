'use client';

import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center p-8">
      <div className="max-w-4xl w-full space-y-8">
        {/* Header */}
        <div className="text-center border-b border-slate-800 pb-8">
          <h1 className="text-6xl font-bold text-emerald-400 mb-4">
            🔥 Codex Dominion
          </h1>
          <p className="text-2xl text-slate-300 mb-2">
            The Flame Burns Sovereign and Eternal
          </p>
          <p className="text-slate-400">
            Council Governance & Workflow Automation System
          </p>
        </div>

        {/* Navigation Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Workflows */}
          <Link href="/workflows">
            <div className="bg-slate-900 border border-slate-800 rounded-lg p-8 hover:border-emerald-500 transition-all hover:scale-105 cursor-pointer">
              <div className="text-4xl mb-4">⚙️</div>
              <h2 className="text-2xl font-bold text-slate-100 mb-2">
                Workflows
              </h2>
              <p className="text-slate-400">
                View workflow types, metrics, and automation statistics
              </p>
              <div className="mt-4 text-emerald-400 font-medium">
                View Dashboard →
              </div>
            </div>
          </Link>

          {/* Agents */}
          <Link href="/agents/agent_jermaine_super_action">
            <div className="bg-slate-900 border border-slate-800 rounded-lg p-8 hover:border-emerald-500 transition-all hover:scale-105 cursor-pointer">
              <div className="text-4xl mb-4">🤖</div>
              <h2 className="text-2xl font-bold text-slate-100 mb-2">
                AI Agents
              </h2>
              <p className="text-slate-400">
                Chat with Super Action AI agent for workflow automation
              </p>
              <div className="mt-4 text-emerald-400 font-medium">
                Open Chat →
              </div>
            </div>
          </Link>
        </div>

        {/* System Status */}
        <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
          <h3 className="text-xl font-bold text-slate-100 mb-4">System Status</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center">
              <div className="text-green-400 text-2xl mb-2">✓</div>
              <div className="text-slate-300 font-medium">Council Engine</div>
              <div className="text-slate-500 text-sm">Operational</div>
            </div>
            <div className="text-center">
              <div className="text-green-400 text-2xl mb-2">✓</div>
              <div className="text-slate-300 font-medium">Workflow Catalog</div>
              <div className="text-slate-500 text-sm">6 Types Active</div>
            </div>
            <div className="text-center">
              <div className="text-green-400 text-2xl mb-2">✓</div>
              <div className="text-slate-300 font-medium">Background Worker</div>
              <div className="text-slate-500 text-sm">Running</div>
            </div>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="text-center text-slate-500 text-sm">
          <p>Powered by Council Seal Architecture</p>
          <p className="mt-2">Version 2.0.0 | Production Ready</p>
        </div>
      </div>
    </div>
  );
}

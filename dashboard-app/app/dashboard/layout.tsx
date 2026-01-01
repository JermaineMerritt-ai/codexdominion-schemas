'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

interface NavItem {
  id: string;
  label: string;
  icon: string;
  href: string;
}

const navItems: NavItem[] = [
  { id: 'overview', label: 'Overview', icon: '🏛️', href: '/dashboard/overview' },
  { id: 'capsules', label: 'Capsules', icon: '💊', href: '/dashboard/capsules' },
  { id: 'intelligence', label: 'Intelligence Core', icon: '🧠', href: '/dashboard/intelligence-core' },
  { id: 'agents', label: 'AI Agents', icon: '🤖', href: '/dashboard/ai-agents' },
  { id: 'leaderboard', label: 'Agent Leaderboard', icon: '🏆', href: '/dashboard/agents/leaderboard' },
  { id: 'councils', label: 'Councils', icon: '⚖️', href: '/dashboard/councils' },
  { id: 'review', label: 'Council Review', icon: '📋', href: '/dashboard/council/review' },
  { id: 'tools', label: 'Tools', icon: '🔧', href: '/dashboard/tools' },
  { id: 'analytics', label: 'Analytics', icon: '📊', href: '/dashboard/analytics' },
  { id: 'settings', label: 'Settings', icon: '⚙️', href: '/dashboard/settings' },
];

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [systemStatus] = useState({
    flask: true,
    nextjs: true,
    uptime: 99.9,
  });

  const isActive = (href: string) => {
    if (href === '/dashboard/overview') {
      return pathname === '/dashboard' || pathname === '/dashboard/overview';
    }
    return pathname?.startsWith(href);
  };

  return (
    <div className="flex h-screen bg-slate-900 text-white">
      {/* Left Sidebar */}
      <aside
        className={`${
          sidebarOpen ? 'w-64' : 'w-20'
        } bg-slate-800 border-r border-slate-700 transition-all duration-300 flex flex-col`}
      >
        {/* Logo Section */}
        <div className="h-16 flex items-center px-4 border-b border-slate-700">
          {sidebarOpen ? (
            <div className="flex items-center gap-3">
              <div className="text-2xl">👑</div>
              <div>
                <div className="font-bold text-lg text-amber-400">CODEX</div>
                <div className="text-xs text-gray-400">DOMINION</div>
              </div>
            </div>
          ) : (
            <div className="text-2xl mx-auto">👑</div>
          )}
        </div>

        {/* Toggle Sidebar Button */}
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="mx-4 my-2 py-2 text-sm text-gray-400 hover:text-white transition"
        >
          {sidebarOpen ? '« Collapse' : '»'}
        </button>

        {/* Navigation Items */}
        <nav className="flex-1 overflow-y-auto py-4">
          {navItems.map((item) => (
            <Link
              key={item.id}
              href={item.href}
              className={`flex items-center gap-3 px-4 py-3 mx-2 rounded-lg transition ${
                isActive(item.href)
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-300 hover:bg-slate-700 hover:text-white'
              }`}
            >
              <span className="text-xl">{item.icon}</span>
              {sidebarOpen && <span className="font-medium">{item.label}</span>}
            </Link>
          ))}
        </nav>

        {/* Footer */}
        {sidebarOpen && (
          <div className="p-4 border-t border-slate-700 text-xs text-gray-400">
            <div>Version 1.0.0</div>
            <div>🔥 The Flame Burns Eternal</div>
          </div>
        )}
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <header className="h-16 bg-slate-800 border-b border-slate-700 flex items-center justify-between px-6">
          {/* Left: Logo/Title */}
          <div className="flex items-center gap-4">
            <div className="text-xl font-bold text-amber-400">CODEXDOMINION</div>
          </div>

          {/* Center: Global Search */}
          <div className="flex-1 max-w-2xl mx-8">
            <div className="relative">
              <input
                type="text"
                placeholder="Search agents, workflows, councils..."
                className="w-full bg-slate-700 text-white px-4 py-2 pl-10 rounded-lg border border-slate-600 focus:border-blue-500 focus:outline-none"
              />
              <span className="absolute left-3 top-2.5 text-gray-400">🔍</span>
            </div>
          </div>

          {/* Right: Status & User */}
          <div className="flex items-center gap-4">
            {/* Status Pill */}
            <div
              className={`px-4 py-2 rounded-full text-sm font-medium flex items-center gap-2 ${
                systemStatus.flask && systemStatus.nextjs
                  ? 'bg-green-600 text-white'
                  : 'bg-yellow-600 text-white'
              }`}
            >
              <span className="w-2 h-2 bg-white rounded-full animate-pulse"></span>
              {systemStatus.flask && systemStatus.nextjs ? (
                <span>All Systems Operational</span>
              ) : (
                <span>⚠️ Partial Outage</span>
              )}
            </div>

            {/* Environment Badge */}
            <div className="px-3 py-1 bg-purple-600 text-white rounded-full text-xs font-bold">
              PRODUCTION
            </div>

            {/* User Profile */}
            <button className="flex items-center gap-2 hover:bg-slate-700 px-3 py-2 rounded-lg transition">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-sm font-bold">
                JM
              </div>
              <span className="text-sm">Jermaine</span>
            </button>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
          {children}
        </main>
      </div>
    </div>
  );
}

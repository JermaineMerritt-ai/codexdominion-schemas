'use client';

import { useState } from 'react';
import Link from 'next/link';

export function TopBar() {
  const [searchQuery, setSearchQuery] = useState('');
  const [showNotifications, setShowNotifications] = useState(false);

  return (
    <header className="flex items-center justify-between h-20 px-6 bg-[#0A0F29] text-white border-b border-[#FFD700]">
      {/* Left: Brand Seal & Status */}
      <div className="flex items-center space-x-4">
        <Link href="/" className="flex items-center space-x-2">
          <span className="text-2xl">🔥</span>
          <span className="font-cinzel text-xl text-[#FFD700] hover:text-[#FFA500] transition-colors">
            Codex Dominion
          </span>
        </Link>
        <span className="px-3 py-1 bg-green-600 rounded-full text-xs font-semibold">
          Stable
        </span>
        <span className="px-3 py-1 bg-blue-600 rounded-full text-xs font-semibold">
          Production
        </span>
      </div>

      {/* Center: Search */}
      <div className="flex-1 max-w-2xl mx-6">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search engines, avatars, documents..."
          className="w-full px-4 py-2 rounded-lg bg-[#1A1F3C] text-white placeholder-gray-400 border border-[#FFD700]/30 focus:border-[#FFD700] focus:outline-none focus:ring-2 focus:ring-[#FFD700]/50 transition-all"
        />
      </div>

      {/* Right: Alerts & Avatar */}
      <div className="flex items-center space-x-4">
        {/* Notifications */}
        <button
          onClick={() => setShowNotifications(!showNotifications)}
          className="relative px-3 py-2 rounded-lg hover:bg-[#1A1F3C] transition-colors"
          aria-label="Notifications"
        >
          <span className="text-xl">🔔</span>
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>

        {/* User Avatar */}
        <Link
          href="/profile"
          className="flex items-center space-x-2 px-3 py-2 rounded-lg hover:bg-[#1A1F3C] transition-colors"
        >
          <span className="text-xl">👤</span>
          <span className="font-semibold text-sm">Jermaine</span>
        </Link>
      </div>

      {/* Notifications Dropdown */}
      {showNotifications && (
        <div className="absolute top-20 right-6 w-80 bg-[#1A1F3C] border border-[#FFD700]/30 rounded-lg shadow-2xl z-50">
          <div className="p-4 border-b border-[#FFD700]/20">
            <h3 className="font-semibold text-[#FFD700]">Notifications</h3>
          </div>
          <div className="p-4 space-y-3 max-h-96 overflow-y-auto">
            <div className="p-3 bg-[#0A0F29] rounded border-l-4 border-green-500">
              <p className="text-sm">✅ Backend operational - Flame sovereign</p>
              <p className="text-xs text-gray-400 mt-1">2 minutes ago</p>
            </div>
            <div className="p-3 bg-[#0A0F29] rounded border-l-4 border-blue-500">
              <p className="text-sm">🌐 Frontend deployed to IONOS</p>
              <p className="text-xs text-gray-400 mt-1">1 hour ago</p>
            </div>
            <div className="p-3 bg-[#0A0F29] rounded border-l-4 border-[#FFD700]">
              <p className="text-sm">🔥 Codex Dominion is live</p>
              <p className="text-xs text-gray-400 mt-1">2 hours ago</p>
            </div>
          </div>
        </div>
      )}
    </header>
  );
}

'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

interface Realm {
  name: string;
  path: string;
  icon: string;
}

const realms: Realm[] = [
  { name: 'Home / Sovereign Bridge', path: '/', icon: '🏛️' },
  { name: 'Engines', path: '/engines', icon: '⚙️' },
  { name: 'Avatars & AIs', path: '/avatars', icon: '🤖' },
  { name: 'Automations & Tools', path: '/automations', icon: '🔧' },
  { name: 'Documents & Knowledge', path: '/documents', icon: '📚' },
  { name: 'AI Video Studio', path: '/video-studio', icon: '🎬' },
  { name: 'Commerce & Products', path: '/commerce', icon: '🛒' },
  { name: 'Settings & Ceremonies', path: '/settings', icon: '⚙️' },
];

export function LeftTabs() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);

  return (
    <nav className="bg-[#0A0F29] text-white border-r border-[#FFD700]/30 overflow-y-auto">
      {/* Collapse Toggle */}
      <div className="p-4 border-b border-[#FFD700]/20">
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="w-full flex items-center justify-between text-sm font-semibold text-[#FFD700] hover:text-[#FFA500] transition-colors"
          aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {!collapsed && <span>Realms</span>}
          <span className="text-lg">{collapsed ? '→' : '←'}</span>
        </button>
      </div>

      {/* Navigation Items */}
      <div className="p-4 space-y-2">
        {realms.map((realm, idx) => {
          const isActive = pathname === realm.path;

          return (
            <Link
              key={idx}
              href={realm.path}
              className={`
                block w-full text-left px-4 py-3 rounded-lg transition-all
                ${isActive
                  ? 'bg-[#FFD700] text-[#0A0F29] font-semibold shadow-lg'
                  : 'hover:bg-[#1A1F3C] hover:text-[#FFD700] hover:pl-6'
                }
              `}
            >
              <div className="flex items-center space-x-3">
                <span className="text-xl">{realm.icon}</span>
                {!collapsed && (
                  <span className="text-sm font-medium">{realm.name}</span>
                )}
              </div>
            </Link>
          );
        })}
      </div>

      {/* Footer Info */}
      {!collapsed && (
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-[#FFD700]/20 bg-[#0A0F29]">
          <div className="text-xs text-gray-400 space-y-1">
            <div className="flex items-center justify-between">
              <span>Status:</span>
              <span className="text-green-400 font-semibold">Operational</span>
            </div>
            <div className="flex items-center justify-between">
              <span>Flame:</span>
              <span className="text-[#FFD700] font-semibold">Sovereign</span>
            </div>
            <div className="text-[10px] text-gray-500 mt-2">
              v2.0.0 - Eternal
            </div>
          </div>
        </div>
      )}
    </nav>
  );
}

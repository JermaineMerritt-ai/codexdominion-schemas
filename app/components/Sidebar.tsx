'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useState } from 'react'

interface NavItem {
  href: string
  label: string
  icon: string
  category?: string
}

export default function Sidebar() {
  const pathname = usePathname()
  const [collapsed, setCollapsed] = useState(false)

  const navItems: NavItem[] = [
    { href: '/sovereign-bridge', label: 'Sovereign Bridge', icon: '⚡', category: 'Core' },
    { href: '/constellation', label: 'Constellation', icon: '⭐', category: 'Core' },
    { href: '/operations', label: 'Operations', icon: '⚙️', category: 'Core' },

    { href: '/commerce', label: 'Commerce', icon: '🛍️', category: 'Business' },
    { href: '/affiliate', label: 'Affiliate', icon: '🤝', category: 'Business' },

    { href: '/studio-video', label: 'Video Studio', icon: '🎬', category: 'Creation' },
    { href: '/studio-audio', label: 'Audio Studio', icon: '🎵', category: 'Creation' },
    { href: '/websites', label: 'Websites', icon: '🌐', category: 'Creation' },

    { href: '/knowledge', label: 'Knowledge', icon: '📚', category: 'Intelligence' },
    { href: '/avatars', label: 'Avatars', icon: '🤖', category: 'Intelligence' },

    { href: '/automations', label: 'Automations', icon: '⚡', category: 'Automation' },
    { href: '/social', label: 'Social', icon: '📱', category: 'Automation' },

    { href: '/governance', label: 'Governance', icon: '👁️', category: 'Control' },
    { href: '/settings', label: 'Settings', icon: '⚙️', category: 'Control' },
  ]

  const categories = Array.from(new Set(navItems.map(item => item.category)))

  return (
    <aside
      className={`${
        collapsed ? 'w-16' : 'w-64'
      } bg-codex-navy/95 backdrop-blur-sm border-r border-codex-gold/20 transition-all duration-300 flex flex-col`}
    >
      {/* Collapse Toggle */}
      <div className="p-4 border-b border-codex-gold/20">
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="w-full codex-button flex items-center justify-center"
        >
          <span className="text-xl">{collapsed ? '▶️' : '◀️'}</span>
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto p-4 space-y-6">
        {categories.map((category) => (
          <div key={category}>
            {!collapsed && (
              <h3 className="text-xs font-semibold text-codex-gold/70 uppercase mb-2 px-2">
                {category}
              </h3>
            )}
            <div className="space-y-1">
              {navItems
                .filter((item) => item.category === category)
                .map((item) => {
                  const isActive = pathname === item.href
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      className={`
                        flex items-center space-x-3 px-3 py-2 rounded-md transition-all
                        ${isActive
                          ? 'bg-codex-gold/20 text-codex-gold border-l-2 border-codex-gold'
                          : 'hover:bg-codex-gold/10 hover:text-codex-gold'
                        }
                      `}
                      title={collapsed ? item.label : undefined}
                    >
                      <span className="text-xl">{item.icon}</span>
                      {!collapsed && (
                        <span className="text-sm font-medium">{item.label}</span>
                      )}
                    </Link>
                  )
                })}
            </div>
          </div>
        ))}
      </nav>

      {/* Footer Status */}
      {!collapsed && (
        <div className="p-4 border-t border-codex-gold/20">
          <div className="codex-panel text-xs space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-codex-parchment/70">System Health</span>
              <span className="text-green-400 font-semibold">GOOD</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-codex-parchment/70">Active Rituals</span>
              <span className="text-codex-gold font-semibold">7/7</span>
            </div>
          </div>
        </div>
      )}
    </aside>
  )
}

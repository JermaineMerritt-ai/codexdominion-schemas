'use client'

import Link from 'next/link'
import { useState } from 'react'

export default function TopBar() {
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <header className="border-b border-codex-gold/20 bg-codex-navy/95 backdrop-blur-sm sticky top-0 z-50">
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          {/* Logo & Brand */}
          <div className="flex items-center space-x-6">
            <Link href="/sovereign-bridge" className="flex items-center space-x-2">
              <span className="text-2xl">🔥</span>
              <h1 className="text-2xl font-serif text-codex-gold hidden md:block">
                Codex Dominion
              </h1>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden lg:flex space-x-4 text-sm">
              <Link href="/sovereign-bridge" className="hover:text-codex-gold transition">
                Bridge
              </Link>
              <Link href="/constellation" className="hover:text-codex-gold transition">
                Constellation
              </Link>
              <Link href="/operations" className="hover:text-codex-gold transition">
                Operations
              </Link>
              <Link href="/commerce" className="hover:text-codex-gold transition">
                Commerce
              </Link>
              <Link href="/automations" className="hover:text-codex-gold transition">
                Rituals
              </Link>
              <Link href="/governance" className="hover:text-codex-gold transition">
                Governance
              </Link>
              <Link href="/settings" className="hover:text-codex-gold transition">
                Settings
              </Link>
            </nav>
          </div>

          {/* Status & Actions */}
          <div className="flex items-center space-x-4">
            {/* System Status */}
            <div className="hidden md:flex items-center space-x-2">
              <span className="text-xs text-codex-gold/70">Omega Seal</span>
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
            </div>

            {/* Quick Actions */}
            <button className="p-2 hover:bg-codex-gold/10 rounded transition">
              <span className="text-xl">🔔</span>
            </button>

            {/* Mobile Menu Toggle */}
            <button
              className="lg:hidden p-2 hover:bg-codex-gold/10 rounded transition"
              onClick={() => setMenuOpen(!menuOpen)}
            >
              <span className="text-xl">{menuOpen ? '✕' : '☰'}</span>
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {menuOpen && (
          <nav className="lg:hidden mt-4 pb-4 space-y-2">
            <Link
              href="/sovereign-bridge"
              className="block py-2 px-4 hover:bg-codex-gold/10 rounded transition"
              onClick={() => setMenuOpen(false)}
            >
              ⚡ Sovereign Bridge
            </Link>
            <Link
              href="/constellation"
              className="block py-2 px-4 hover:bg-codex-gold/10 rounded transition"
              onClick={() => setMenuOpen(false)}
            >
              ⭐ Constellation
            </Link>
            <Link
              href="/operations"
              className="block py-2 px-4 hover:bg-codex-gold/10 rounded transition"
              onClick={() => setMenuOpen(false)}
            >
              ⚙️ Operations
            </Link>
            <Link
              href="/commerce"
              className="block py-2 px-4 hover:bg-codex-gold/10 rounded transition"
              onClick={() => setMenuOpen(false)}
            >
              🛍️ Commerce
            </Link>
            <Link
              href="/studio-video"
              className="block py-2 px-4 hover:bg-codex-gold/10 rounded transition"
              onClick={() => setMenuOpen(false)}
            >
              🎬 Video Studio
            </Link>
            <Link
              href="/studio-audio"
              className="block py-2 px-4 hover:bg-codex-gold/10 rounded transition"
              onClick={() => setMenuOpen(false)}
            >
              🎵 Audio Studio
            </Link>
            <Link
              href="/automations"
              className="block py-2 px-4 hover:bg-codex-gold/10 rounded transition"
              onClick={() => setMenuOpen(false)}
            >
              ⚡ Automations
            </Link>
            <Link
              href="/governance"
              className="block py-2 px-4 hover:bg-codex-gold/10 rounded transition"
              onClick={() => setMenuOpen(false)}
            >
              👁️ Governance
            </Link>
            <Link
              href="/settings"
              className="block py-2 px-4 hover:bg-codex-gold/10 rounded transition"
              onClick={() => setMenuOpen(false)}
            >
              ⚙️ Settings
            </Link>
          </nav>
        )}
      </div>
    </header>
  )
}

import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from './providers'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Sovereign Bridge | Codex Dominion',
  description: 'Council Seal Command Center - Orchestration & Automation Dashboard',
  keywords: ['codex', 'dominion', 'sovereign', 'automation', 'AI', 'dashboard'],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-codex-navy text-codex-parchment`}>
        <Providers>
          <div className="min-h-screen flex flex-col">
            {/* Ceremonial Header */}
            <header className="border-b border-codex-gold/20 bg-codex-navy/95 backdrop-blur-sm sticky top-0 z-50">
              <div className="container mx-auto px-4 py-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-6">
                    <h1 className="text-2xl font-serif text-codex-gold">
                      🔥 Codex Dominion
                    </h1>
                    <nav className="hidden md:flex space-x-4 text-sm">
                      <a href="/sovereign-bridge" className="hover:text-codex-gold transition">Bridge</a>
                      <a href="/constellation" className="hover:text-codex-gold transition">Constellation</a>
                      <a href="/operations" className="hover:text-codex-gold transition">Operations</a>
                      <a href="/commerce" className="hover:text-codex-gold transition">Commerce</a>
                      <a href="/studio-video" className="hover:text-codex-gold transition">Video</a>
                      <a href="/studio-audio" className="hover:text-codex-gold transition">Audio</a>
                      <a href="/automations" className="hover:text-codex-gold transition">Rituals</a>
                      <a href="/governance" className="hover:text-codex-gold transition">Governance</a>
                    </nav>
                  </div>
                  <div className="flex items-center space-x-4">
                    <span className="text-xs text-codex-gold/70">Omega Seal: Active</span>
                    <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                  </div>
                </div>
              </div>
            </header>

            {/* Main Content */}
            <main className="flex-1">
              {children}
            </main>

            {/* Ceremonial Footer */}
            <footer className="border-t border-codex-gold/20 bg-codex-navy/95 backdrop-blur-sm mt-auto">
              <div className="container mx-auto px-4 py-4 text-center text-xs text-codex-parchment/60">
                <p>🔥 The Flame Burns Sovereign and Eternal 🔥</p>
                <p className="mt-1">Council Seal Authority • {new Date().getFullYear()}</p>
              </div>
            </footer>
          </div>
        </Providers>
      </body>
    </html>
  )
}

import type { Metadata } from 'next';
import './globals.css';
import { OfflineOverlay } from '@/components/offline/OfflineState';
import { CompactOfflineIndicator } from '@/components/offline/OfflineState';

export const metadata: Metadata = {
  title: "CodexDominion Master Dashboard Ultimate",
  description: "Complete Command Center for Capsules, Engines, Agents, Councils and Tools.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-950 text-slate-50">
        {/* Offline overlay - auto-shows when connection lost */}
        <OfflineOverlay
          hasCachedData={true}
          lastSyncTime={new Date()}
        />
        
        {children}
      </body>
    </html>
  );
}

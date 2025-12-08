import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { Providers } from '@/components/providers';
import { ReplayProvider } from '@/context/ReplayContext';
import { TopBar } from '@/components/layout/top-bar';
import { LeftTabs } from '@/components/layout/left-tabs';
import { AICommandStrip } from '@/components/layout/ai-command-strip';
import { Analytics } from '@/components/analytics';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: {
    default: 'CodexDominion - Faith-Based Digital Products',
    template: '%s | CodexDominion'
  },
  description: 'Biblical printables, coloring books, homeschool resources, wedding planners, and memory verse decor for faith-centered families.',
  keywords: ['bible printables', 'christian coloring books', 'homeschool curriculum', 'wedding planner', 'scripture art', 'memory verse'],
  authors: [{ name: 'CodexDominion' }],
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://codexdominion.app',
    siteName: 'CodexDominion',
    title: 'CodexDominion - Faith-Based Digital Products',
    description: 'Biblical printables, coloring books, homeschool resources, and more for faith-centered families.',
    images: [
      {
        url: '/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'CodexDominion'
      }
    ]
  },
  twitter: {
    card: 'summary_large_image',
    site: '@codexdominion',
    creator: '@codexdominion'
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1
    }
  },
  verification: {
    google: process.env.NEXT_PUBLIC_GOOGLE_SITE_VERIFICATION,
    yandex: process.env.NEXT_PUBLIC_YANDEX_VERIFICATION
  }
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>
          <ReplayProvider>
            <TopBar /> {/* Brand seal, status, search, alerts, avatar */}
            <div className="grid grid-cols-[260px_1fr] h-[calc(100vh-80px)]">
              <LeftTabs /> {/* Realms navigation */}
              <main className="relative">
                {children}
                <AICommandStrip /> {/* Always visible at bottom */}
              </main>
            </div>
            <Analytics />
          </ReplayProvider>
        </Providers>
      </body>
    </html>
  );
}

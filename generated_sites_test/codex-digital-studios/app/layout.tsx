import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Codex Digital Studios',
  description: 'AI-powered web development and digital solutions. Buy our premium templates and hire our expert team.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

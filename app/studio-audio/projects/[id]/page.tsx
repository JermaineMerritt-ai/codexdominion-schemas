import Link from 'next/link'

export default function AudioProjectDetailPage({ params }: { params: { id: string } }) {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-serif text-ceremonial mb-2">
          Audio Project Editor
        </h1>
        <p className="text-proclamation">
          Project ID: {params.id}
        </p>
      </div>

      <div className="codex-card">
        <div className="bg-codex-navy/50 rounded-lg p-8 mb-6">
          <div className="flex items-center space-x-4">
            <button className="text-4xl hover:scale-110 transition">▶️</button>
            <div className="flex-1 bg-codex-gold/20 h-16 rounded flex items-center px-4">
              <span className="text-codex-parchment/50">Waveform Visualization</span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button className="codex-button">🎵 Render</button>
          <button className="codex-button">💾 Save</button>
          <button className="codex-button">📤 Export</button>
          <Link href="/studio-audio">
            <button className="codex-button w-full">← Back</button>
          </Link>
        </div>
      </div>
    </div>
  )
}

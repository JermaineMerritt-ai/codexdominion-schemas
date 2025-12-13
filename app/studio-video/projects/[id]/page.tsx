import Link from 'next/link'

export default function VideoProjectDetailPage({ params }: { params: { id: string } }) {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-serif text-ceremonial mb-2">
          Video Project Editor
        </h1>
        <p className="text-proclamation">
          Project ID: {params.id}
        </p>
      </div>

      <div className="codex-card">
        <div className="aspect-video bg-codex-navy/50 rounded-lg flex items-center justify-center mb-6">
          <span className="text-codex-parchment/50">Preview Area</span>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button className="codex-button">▶️ Render</button>
          <button className="codex-button">💾 Save</button>
          <button className="codex-button">📤 Export</button>
          <Link href="/studio-video">
            <button className="codex-button w-full">← Back</button>
          </Link>
        </div>
      </div>
    </div>
  )
}

'use client'

export default function AssetLibrary() {
  return (
    <div className="codex-card">
      <h2 className="text-xl font-serif text-codex-gold mb-4">
        Asset Library
      </h2>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        <div className="codex-panel aspect-square flex items-center justify-center">
          <span className="text-4xl">🖼️</span>
        </div>
        <div className="codex-panel aspect-square flex items-center justify-center">
          <span className="text-4xl">🎵</span>
        </div>
        <div className="codex-panel aspect-square flex items-center justify-center">
          <span className="text-4xl">🎬</span>
        </div>
      </div>
    </div>
  )
}

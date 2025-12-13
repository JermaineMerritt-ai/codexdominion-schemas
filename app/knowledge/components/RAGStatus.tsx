'use client'

export default function RAGStatus() {
  return (
    <div className="codex-card">
      <h2 className="text-2xl font-serif text-codex-gold mb-6">
        RAG System Status
      </h2>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="codex-panel">
          <div className="text-2xl font-bold text-codex-gold">12,847</div>
          <div className="text-xs text-codex-parchment/60">Documents</div>
        </div>
        <div className="codex-panel">
          <div className="text-2xl font-bold text-green-400">892K</div>
          <div className="text-xs text-codex-parchment/60">Vectors</div>
        </div>
        <div className="codex-panel">
          <div className="text-2xl font-bold text-blue-400">1,523</div>
          <div className="text-xs text-codex-parchment/60">Queries Today</div>
        </div>
        <div className="codex-panel">
          <div className="text-2xl font-bold text-purple-400">98.7%</div>
          <div className="text-xs text-codex-parchment/60">Accuracy</div>
        </div>
      </div>
    </div>
  )
}

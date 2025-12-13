'use client'

export default function KnowledgeMap() {
  const categories = [
    { name: 'Products', count: 127 },
    { name: 'FAQs', count: 89 },
    { name: 'Documentation', count: 45 },
    { name: 'Tutorials', count: 32 },
  ]

  return (
    <div className="codex-card">
      <h2 className="text-xl font-serif text-codex-gold mb-4">
        Knowledge Categories
      </h2>

      <div className="space-y-3">
        {categories.map((cat, idx) => (
          <div key={idx} className="codex-panel">
            <div className="flex items-center justify-between">
              <span className="font-semibold text-sm">{cat.name}</span>
              <span className="text-lg font-bold text-codex-gold">{cat.count}</span>
            </div>
          </div>
        ))}
      </div>

      <button className="codex-button w-full mt-4 text-sm">
        🔍 Search Knowledge
      </button>
    </div>
  )
}

'use client'

export default function EngineDashboard() {
  const engineTypes = [
    { type: 'Content', count: 2, color: 'bg-blue-500' },
    { type: 'Business', count: 2, color: 'bg-green-500' },
    { type: 'Automation', count: 2, color: 'bg-purple-500' },
    { type: 'Media', count: 2, color: 'bg-pink-500' },
    { type: 'AI', count: 2, color: 'bg-yellow-500' },
    { type: 'Distribution', count: 1, color: 'bg-orange-500' },
    { type: 'Oversight', count: 1, color: 'bg-red-500' },
  ]

  return (
    <div className="codex-card">
      <h2 className="text-2xl font-serif text-codex-gold mb-6">
        Engine Distribution
      </h2>

      <div className="space-y-4">
        {engineTypes.map((item, idx) => (
          <div key={idx} className="codex-panel">
            <div className="flex items-center justify-between mb-2">
              <span className="font-semibold">{item.type}</span>
              <span className="text-sm text-codex-parchment/70">{item.count} engines</span>
            </div>
            <div className="w-full bg-codex-navy/50 rounded-full h-2">
              <div
                className={`${item.color} h-2 rounded-full`}
                style={{ width: `${(item.count / 12) * 100}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

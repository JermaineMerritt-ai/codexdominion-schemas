'use client'

export default function RenderQueue() {
  const queue = [
    { id: '1', name: 'Advent Promo', progress: 67, eta: '5 min' },
    { id: '2', name: 'Instagram Reel', progress: 0, eta: 'Queued' },
  ]

  return (
    <div className="codex-card">
      <h2 className="text-xl font-serif text-codex-gold mb-4">
        🎞️ Render Queue
      </h2>

      <div className="space-y-3">
        {queue.map((item) => (
          <div key={item.id} className="codex-panel">
            <div className="flex justify-between text-sm mb-2">
              <span className="font-semibold">{item.name}</span>
              <span className="text-codex-parchment/60">{item.eta}</span>
            </div>
            {item.progress > 0 && (
              <div className="w-full bg-codex-navy/50 rounded-full h-2">
                <div
                  className="bg-blue-500 h-2 rounded-full"
                  style={{ width: `${item.progress}%` }}
                ></div>
              </div>
            )}
          </div>
        ))}
      </div>

      <button className="codex-button w-full mt-4 text-sm">
        View All Renders
      </button>
    </div>
  )
}

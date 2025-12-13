'use client'

export default function RepurposingPanel() {
  return (
    <div className="codex-card">
      <h2 className="text-xl font-serif text-codex-gold mb-4">
        🔄 Content Repurposing
      </h2>

      <div className="space-y-3">
        <div className="codex-panel">
          <h3 className="font-semibold text-sm mb-2">Available Templates</h3>
          <div className="space-y-2">
            <div className="text-xs text-codex-parchment/70">📸 Instagram Story → Post</div>
            <div className="text-xs text-codex-parchment/70">🎬 YouTube → TikTok Shorts</div>
            <div className="text-xs text-codex-parchment/70">📝 Blog → Social Carousel</div>
          </div>
        </div>

        <button className="codex-button w-full text-sm">
          ✨ Auto-Repurpose
        </button>
      </div>
    </div>
  )
}

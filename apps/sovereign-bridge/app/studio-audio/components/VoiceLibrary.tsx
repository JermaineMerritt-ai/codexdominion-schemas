'use client'

export default function VoiceLibrary() {
  const voices = [
    { id: '1', name: 'Narrator Voice', type: 'Male, Deep' },
    { id: '2', name: 'Character Voice', type: 'Female, Young' },
    { id: '3', name: 'Podcast Host', type: 'Neutral, Warm' },
  ]

  return (
    <div className="codex-card">
      <h2 className="text-xl font-serif text-codex-gold mb-4">
        🎙️ Voice Library
      </h2>

      <div className="space-y-3">
        {voices.map((voice) => (
          <div key={voice.id} className="codex-panel">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-sm">{voice.name}</h3>
                <p className="text-xs text-codex-parchment/60">{voice.type}</p>
              </div>
              <button className="text-2xl hover:scale-110 transition">▶️</button>
            </div>
          </div>
        ))}
      </div>

      <button className="codex-button w-full mt-4 text-sm">
        ➕ Add Voice
      </button>
    </div>
  )
}

import AudioProjectCard from './components/AudioProjectCard'
import AudioRenderQueue from './components/AudioRenderQueue'

export default function StudioAudioPage() {
  const projects = [
    { id: '1', name: 'Advent Meditation Music', status: 'rendering', progress: 43 },
    { id: '2', name: 'Podcast Episode 12', status: 'draft', progress: 0 },
    { id: '3', name: 'Christmas Hymn Remix', status: 'completed', progress: 100 },
  ]

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-serif text-ceremonial mb-2">
          🎵 Audio Production Studio
        </h1>
        <p className="text-proclamation">
          AI Voice Generation, Music Production & Audio Rendering
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="codex-card">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-serif text-codex-gold">
                Audio Projects
              </h2>
              <button className="codex-button">
                ➕ New Project
              </button>
            </div>

            <div className="space-y-4">
              {projects.map((project) => (
                <AudioProjectCard key={project.id} project={project} />
              ))}
            </div>
          </div>
        </div>

        <div>
          <AudioRenderQueue />
        </div>
      </div>
    </div>
  )
}

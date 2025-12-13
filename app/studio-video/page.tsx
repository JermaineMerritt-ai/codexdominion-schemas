import VideoProjectCard from './components/VideoProjectCard'
import RenderQueue from './components/RenderQueue'

export default function StudioVideoPage() {
  const projects = [
    { id: '1', name: 'Advent Promo Video', status: 'rendering', progress: 67 },
    { id: '2', name: 'Kids Bible Story Animation', status: 'draft', progress: 0 },
    { id: '3', name: 'Wedding Testimonial', status: 'completed', progress: 100 },
  ]

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-serif text-ceremonial mb-2">
          🎬 Video Production Studio
        </h1>
        <p className="text-proclamation">
          AI-Powered Video Creation, Rendering & Asset Management
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="codex-card">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-serif text-codex-gold">
                Video Projects
              </h2>
              <button className="codex-button">
                ➕ New Project
              </button>
            </div>

            <div className="space-y-4">
              {projects.map((project) => (
                <VideoProjectCard key={project.id} project={project} />
              ))}
            </div>
          </div>
        </div>

        <div>
          <RenderQueue />
        </div>
      </div>
    </div>
  )
}

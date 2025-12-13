import AvatarCard from './components/AvatarCard'
import AvatarDashboard from './components/AvatarDashboard'

export default function AvatarsPage() {
  const avatars = [
    { id: '1', name: 'Customer Support Avatar', type: 'support', status: 'active', interactions: 2847 },
    { id: '2', name: 'Sales Agent Avatar', type: 'sales', status: 'active', interactions: 1523 },
    { id: '3', name: 'Analyst Avatar', type: 'analytics', status: 'active', interactions: 892 },
    { id: '4', name: 'Orchestrator Avatar', type: 'workflow', status: 'idle', interactions: 456 },
  ]

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-serif text-ceremonial mb-2">
          🤖 Avatar Systems
        </h1>
        <p className="text-proclamation">
          AI-Powered Autonomous Agents & Customer Interaction Layer
        </p>
      </div>

      <AvatarDashboard />

      <div className="codex-card mt-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-serif text-codex-gold">
            Active Avatars
          </h2>
          <button className="codex-button">
            ➕ Deploy New Avatar
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {avatars.map((avatar) => (
            <AvatarCard key={avatar.id} avatar={avatar} />
          ))}
        </div>
      </div>
    </div>
  )
}

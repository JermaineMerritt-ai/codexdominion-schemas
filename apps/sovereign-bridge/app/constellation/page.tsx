import ConstellationMap from './components/ConstellationMap'
import EngineTile from './components/EngineTile'
import EngineDashboard from './components/EngineDashboard'

export default function ConstellationPage() {
  return (
    <div className="container mx-auto px-4 py-8 space-y-6">
      <div className="mb-8">
        <h1 className="text-4xl font-serif text-ceremonial mb-2">
          ⭐ Engine Constellation
        </h1>
        <p className="text-proclamation">
          Visual Map of All Bound Engines & Service Modules
        </p>
      </div>

      <ConstellationMap />
      <EngineDashboard />
    </div>
  )
}

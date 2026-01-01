import { fetchIntelligenceCore } from "@/lib/intelligenceCore"
import type { IntelligenceEngine } from "@/types/intelligenceCore"

export default async function IntelligenceCorePage() {
  const engines = await fetchIntelligenceCore()
  
  // Group engines by lifecycle stage
  const grouped = {
    active: engines.filter(e => e.lifecycle === 'active'),
    beta: engines.filter(e => e.lifecycle === 'beta'),
    prototype: engines.filter(e => e.lifecycle === 'prototype'),
    concept: engines.filter(e => e.lifecycle === 'concept')
  }

  const lifecycleLabels = {
    active: 'Production Ready',
    beta: 'Beta Testing',
    prototype: 'Prototype Stage',
    concept: 'Conceptual Design'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-700 p-8">
      <header className="text-center mb-12">
        <h1 className="text-5xl font-bold text-yellow-400 mb-4">
          🧠 Intelligence Core
        </h1>
        <p className="text-xl text-white/90">
          {engines.length} Advanced Intelligence Engines - Grouped by Lifecycle Stage
        </p>
      </header>

      {/* Render lifecycle sections */}
      {(Object.entries(grouped) as [keyof typeof grouped, IntelligenceEngine[]][]).map(([lifecycle, lifecycleEngines]) => (
        lifecycleEngines.length > 0 && (
          <section key={lifecycle} className="mb-12">
            {/* Lifecycle header */}
            <div className="bg-yellow-400/20 border-l-4 border-yellow-400 p-4 rounded-lg mb-6">
              <h2 className="text-2xl text-yellow-400 font-bold">
                {lifecycleLabels[lifecycle]}
                <span className="text-sm ml-4 opacity-80 font-normal">
                  {lifecycleEngines.length} engine{lifecycleEngines.length !== 1 ? 's' : ''}
                </span>
              </h2>
            </div>

            {/* Engine cards grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {lifecycleEngines.map(engine => (
                <div
                  key={engine.id}
                  className="bg-white/10 backdrop-blur-md p-6 rounded-lg border-l-4 border-yellow-400 hover:transform hover:-translate-y-1 hover:shadow-2xl transition-all duration-300"
                >
                  {/* Header with name and status */}
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="text-xl font-bold text-yellow-400 flex-1">{engine.name}</h3>
                    <div className="flex flex-col gap-1 ml-2">
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-bold uppercase whitespace-nowrap ${
                          engine.status === 'active'
                            ? 'bg-green-500 text-white'
                            : engine.status === 'in_progress'
                            ? 'bg-orange-500 text-white'
                            : engine.status === 'planned'
                            ? 'bg-blue-500 text-white'
                            : 'bg-gray-500 text-white'
                        }`}
                      >
                        {engine.status.replace('_', ' ')}
                      </span>
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-bold uppercase whitespace-nowrap ${
                          engine.operational_mode === 'auto'
                            ? 'bg-purple-600 text-white'
                            : engine.operational_mode === 'hybrid'
                            ? 'bg-indigo-600 text-white'
                            : engine.operational_mode === 'assist'
                            ? 'bg-cyan-600 text-white'
                            : 'bg-gray-600 text-white'
                        }`}
                      >
                        {engine.operational_mode}
                      </span>
                    </div>
                  </div>

                  {/* Role quote */}
                  <p className="text-yellow-400/90 italic text-sm mb-3">"{engine.role}"</p>

                  {/* Description */}
                  <p className="text-white/90 text-sm mb-4 leading-relaxed">{engine.description}</p>

                  {/* Primary Capsules badges */}
                  <div className="mb-4">
                    <p className="text-yellow-400 text-xs font-bold mb-2 uppercase tracking-wide">
                      Primary Capsules
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {engine.primary_capsules.map(capsule => (
                        <span
                          key={capsule}
                          className="bg-blue-500/30 border border-blue-500/50 px-3 py-1 rounded-full text-xs text-white/90"
                        >
                          {capsule}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Capabilities badges */}
                  <div className="mb-4">
                    <p className="text-yellow-400 text-xs font-bold mb-2 uppercase tracking-wide">
                      Capabilities
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {engine.capabilities.map(capability => (
                        <span
                          key={capability}
                          className="bg-green-500/30 border border-green-500/50 px-3 py-1 rounded-full text-xs text-white/90"
                        >
                          {capability.replace(/_/g, ' ')}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Overlays grid (2x2) */}
                  <div className="grid grid-cols-2 gap-2 mt-4 pt-4 border-t border-white/20">
                    <div
                      className={`flex items-center gap-2 px-3 py-2 rounded text-xs ${
                        engine.overlays.stewardship
                          ? 'bg-green-500/25 border border-green-500/40 text-white'
                          : 'bg-gray-500/15 border border-gray-500/30 text-white/60 opacity-60'
                      }`}
                    >
                      <span className="font-bold">{engine.overlays.stewardship ? '✓' : '✗'}</span>
                      <span>Stewardship</span>
                    </div>
                    <div
                      className={`flex items-center gap-2 px-3 py-2 rounded text-xs ${
                        engine.overlays.wellbeing
                          ? 'bg-green-500/25 border border-green-500/40 text-white'
                          : 'bg-gray-500/15 border border-gray-500/30 text-white/60 opacity-60'
                      }`}
                    >
                      <span className="font-bold">{engine.overlays.wellbeing ? '✓' : '✗'}</span>
                      <span>Wellbeing</span>
                    </div>
                    <div
                      className={`flex items-center gap-2 px-3 py-2 rounded text-xs ${
                        engine.overlays.planetary
                          ? 'bg-green-500/25 border border-green-500/40 text-white'
                          : 'bg-gray-500/15 border border-gray-500/30 text-white/60 opacity-60'
                      }`}
                    >
                      <span className="font-bold">{engine.overlays.planetary ? '✓' : '✗'}</span>
                      <span>Planetary</span>
                    </div>
                    <div
                      className={`flex items-center gap-2 px-3 py-2 rounded text-xs ${
                        engine.overlays.intergenerational
                          ? 'bg-green-500/25 border border-green-500/40 text-white'
                          : 'bg-gray-500/15 border border-gray-500/30 text-white/60 opacity-60'
                      }`}
                    >
                      <span className="font-bold">
                        {engine.overlays.intergenerational ? '✓' : '✗'}
                      </span>
                      <span>Intergenerational</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )
      ))}

      {/* Empty state */}
      {engines.length === 0 && (
        <div className="text-center py-12">
          <p className="text-white/70 text-lg">No intelligence engines found.</p>
        </div>
      )}
    </div>
  )
}

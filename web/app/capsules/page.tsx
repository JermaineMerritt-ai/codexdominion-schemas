import { fetchCapsules } from "@/lib/capsules"
import { Capsule, CapsuleRealm } from "@/types/capsule"

export default async function CapsulesPage() {
  const capsules = await fetchCapsules()
  
  // Group capsules by realm
  const groupedByRealm = capsules.reduce((acc, capsule) => {
    if (!acc[capsule.realm]) {
      acc[capsule.realm] = []
    }
    acc[capsule.realm].push(capsule)
    return acc
  }, {} as Record<CapsuleRealm, Capsule[]>)

  const realmOrder: CapsuleRealm[] = ["foundation", "economic", "knowledge", "community", "automation", "media"]
  const realmColors = {
    foundation: "bg-amber-100 text-amber-800 border-amber-300",
    economic: "bg-green-100 text-green-800 border-green-300",
    knowledge: "bg-blue-100 text-blue-800 border-blue-300",
    community: "bg-purple-100 text-purple-800 border-purple-300",
    automation: "bg-cyan-100 text-cyan-800 border-cyan-300",
    media: "bg-pink-100 text-pink-800 border-pink-300",
  }

  const statusColors = {
    active: "bg-green-500 text-white",
    in_progress: "bg-yellow-500 text-white",
    planned: "bg-gray-500 text-white",
    deprecated: "bg-red-500 text-white",
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-white to-orange-50">
      <div className="container mx-auto px-4 py-12">
        {/* Header */}
        <div className="mb-12 text-center">
          <h1 className="text-5xl font-bold text-amber-900 mb-4">
            🏛️ Codex Dominion Capsules
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Sovereign system modules organized by realm. Each capsule represents a core architectural component.
          </p>
          <div className="mt-6 flex justify-center gap-4 text-sm text-gray-500">
            <span>Total Capsules: <strong>{capsules.length}</strong></span>
            <span>•</span>
            <span>Realms: <strong>{Object.keys(groupedByRealm).length}</strong></span>
          </div>
        </div>

        {capsules.length === 0 ? (
          <div className="text-center py-20">
            <div className="text-6xl mb-4">📦</div>
            <p className="text-xl text-gray-500">No capsules found</p>
          </div>
        ) : (
          <div className="space-y-16">
            {realmOrder.map((realm) => {
              const realmCapsules = groupedByRealm[realm]
              if (!realmCapsules || realmCapsules.length === 0) return null

              return (
                <div key={realm} className="space-y-6">
                  {/* Realm Header */}
                  <div className="flex items-center gap-4">
                    <div className={`px-6 py-3 rounded-lg border-2 ${realmColors[realm]} font-bold text-xl capitalize`}>
                      {realm} Realm
                    </div>
                    <div className="flex-1 h-0.5 bg-gradient-to-r from-gray-300 to-transparent"></div>
                    <span className="text-sm text-gray-500 font-medium">
                      {realmCapsules.length} capsule{realmCapsules.length !== 1 ? 's' : ''}
                    </span>
                  </div>

                  {/* Capsules Grid */}
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {realmCapsules.map((capsule) => (
                      <div
                        key={capsule.id}
                        className="bg-white rounded-xl shadow-lg border-2 border-gray-100 hover:shadow-2xl hover:border-amber-200 transition-all duration-300 overflow-hidden"
                      >
                        {/* Capsule Header */}
                        <div className={`p-4 border-b-2 ${realmColors[realm]}`}>
                          <div className="flex items-start justify-between mb-2">
                            <h3 className="text-xl font-bold text-gray-900">
                              {capsule.name}
                            </h3>
                            <span className={`px-2 py-1 rounded text-xs font-bold ${statusColors[capsule.status]}`}>
                              {capsule.status}
                            </span>
                          </div>
                          <p className="text-sm text-gray-600">{capsule.description}</p>
                        </div>

                        {/* Capsule Body */}
                        <div className="p-4 space-y-4">
                          {/* Tags */}
                          {capsule.tags.length > 0 && (
                            <div>
                              <h4 className="text-xs font-semibold text-gray-500 uppercase mb-2">Tags</h4>
                              <div className="flex flex-wrap gap-1">
                                {capsule.tags.map((tag) => (
                                  <span
                                    key={tag}
                                    className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs"
                                  >
                                    #{tag}
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}

                          {/* Primary Systems */}
                          {capsule.primary_systems.length > 0 && (
                            <div>
                              <h4 className="text-xs font-semibold text-gray-500 uppercase mb-2">Systems</h4>
                              <ul className="text-sm text-gray-700 space-y-1">
                                {capsule.primary_systems.map((system) => (
                                  <li key={system} className="flex items-center gap-2">
                                    <span className="text-amber-600">⚙️</span>
                                    {system}
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}

                          {/* Use Cases */}
                          {capsule.primary_use_cases.length > 0 && (
                            <div>
                              <h4 className="text-xs font-semibold text-gray-500 uppercase mb-2">Use Cases</h4>
                              <ul className="text-sm text-gray-700 space-y-1">
                                {capsule.primary_use_cases.map((useCase) => (
                                  <li key={useCase} className="flex items-center gap-2">
                                    <span className="text-blue-600">💡</span>
                                    {useCase}
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}

                          {/* Linked Modules */}
                          {capsule.linked_modules.length > 0 && (
                            <div>
                              <h4 className="text-xs font-semibold text-gray-500 uppercase mb-2">Linked Modules</h4>
                              <div className="flex flex-wrap gap-1">
                                {capsule.linked_modules.map((module) => (
                                  <span
                                    key={module}
                                    className="px-2 py-1 bg-blue-50 text-blue-700 rounded text-xs font-mono"
                                  >
                                    {module}
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}

                          {/* Indexes */}
                          <div className="pt-4 border-t border-gray-100 flex justify-between text-xs text-gray-400">
                            <span>Realm Index: {capsule.realm_index}</span>
                            <span>Capsule Index: {capsule.capsule_index}</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}

import { fetchEngines } from '@/lib/api/engines';
import Link from 'next/link';
import { Cpu, ChevronRight } from 'lucide-react';

export default async function IntelligenceCorePage() {
  let engines = [];
  try {
    engines = await fetchEngines();
  } catch (error) {
    console.error('Failed to fetch engines:', error);
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Intelligence Core</h1>
        <p className="text-gray-600">AI engines powering the Codex Dominion ecosystem</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <div className="flex items-center gap-3 mb-2">
            <Cpu className="text-purple-600" size={24} />
            <span className="text-gray-600 font-medium">Total Engines</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">{engines.length}</p>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <div className="flex items-center gap-3 mb-2">
            <Cpu className="text-green-600" size={24} />
            <span className="text-gray-600 font-medium">Operational</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">
            {engines.filter((e: any) => e.status === 'operational').length}
          </p>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <div className="flex items-center gap-3 mb-2">
            <Cpu className="text-orange-600" size={24} />
            <span className="text-gray-600 font-medium">Avg Capabilities</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">
            {engines.length > 0
              ? Math.round(
                  engines.reduce((sum: number, e: any) => sum + (e.capabilities?.length || 0), 0) /
                    engines.length
                )
              : 0}
          </p>
        </div>
      </div>

      {/* Engines Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {engines.map((engine: any) => (
          <Link
            key={engine.id}
            href={`/dashboard/intelligence-core/${engine.id}`}
            className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-all"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-gray-900">{engine.name}</h3>
              <ChevronRight className="text-gray-400" size={20} />
            </div>
            <p className="text-gray-600 text-sm mb-4">{engine.description}</p>
            <div className="flex items-center gap-2 mb-3">
              <span
                className={`px-3 py-1 rounded-full text-xs font-medium ${
                  engine.status === 'operational'
                    ? 'bg-green-100 text-green-700'
                    : engine.status === 'degraded'
                    ? 'bg-yellow-100 text-yellow-700'
                    : 'bg-gray-100 text-gray-700'
                }`}
              >
                {engine.status}
              </span>
              <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-medium">
                {engine.capabilities?.length || 0} capabilities
              </span>
            </div>
            <div className="text-xs text-gray-500">
              Connected to {engine.connected_capsules?.length || 0} capsules
            </div>
          </Link>
        ))}
      </div>

      {engines.length === 0 && (
        <div className="bg-white rounded-xl p-12 text-center shadow-lg">
          <Cpu className="mx-auto text-gray-400 mb-4" size={48} />
          <p className="text-gray-600">No engines found. Check Flask backend connection.</p>
        </div>
      )}
    </div>
  );
}

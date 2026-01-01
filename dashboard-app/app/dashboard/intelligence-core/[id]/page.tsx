import { fetchEngine, fetchEngineConnections } from '@/lib/api/engines';
import Link from 'next/link';
import { ArrowLeft, Cpu, Package } from 'lucide-react';

export default async function EngineDetailPage({ params }: { params: { id: string } }) {
  let engine: any = null;
  let connections: string[] = [];
  
  try {
    engine = await fetchEngine(params.id);
    connections = await fetchEngineConnections(params.id);
  } catch (error) {
    console.error('Failed to fetch engine:', error);
  }

  if (!engine) {
    return (
      <div className="bg-white rounded-xl p-12 text-center shadow-lg">
        <Cpu className="mx-auto text-gray-400 mb-4" size={48} />
        <p className="text-gray-600">Engine not found</p>
        <Link
          href="/dashboard/intelligence-core"
          className="text-purple-600 hover:underline mt-4 inline-block"
        >
          ← Back to Intelligence Core
        </Link>
      </div>
    );
  }

  return (
    <div>
      <Link
        href="/dashboard/intelligence-core"
        className="inline-flex items-center gap-2 text-purple-600 hover:underline mb-6"
      >
        <ArrowLeft size={20} />
        Back to Intelligence Core
      </Link>

      <div className="bg-white rounded-xl p-8 shadow-lg mb-6">
        <div className="flex items-center gap-4 mb-4">
          <div className="p-3 bg-purple-100 rounded-lg">
            <Cpu className="text-purple-600" size={32} />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{engine.name}</h1>
            <p className="text-gray-600 font-mono text-sm">{engine.id}</p>
          </div>
        </div>
        <p className="text-gray-700 mb-6">{engine.description}</p>
        <div className="flex items-center gap-4">
          <span
            className={`px-4 py-2 rounded-full font-medium ${
              engine.status === 'operational'
                ? 'bg-green-100 text-green-700'
                : engine.status === 'degraded'
                ? 'bg-yellow-100 text-yellow-700'
                : 'bg-gray-100 text-gray-700'
            }`}
          >
            {engine.status}
          </span>
        </div>
      </div>

      {/* Capabilities */}
      <div className="bg-white rounded-xl p-6 shadow-lg mb-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          Capabilities ({engine.capabilities?.length || 0})
        </h2>
        <div className="flex flex-wrap gap-3">
          {engine.capabilities?.map((capability: string, idx: number) => (
            <span
              key={idx}
              className="px-4 py-2 bg-blue-100 text-blue-700 rounded-lg font-medium"
            >
              {capability}
            </span>
          ))}
        </div>
      </div>

      {/* Connected Capsules */}
      <div className="bg-white rounded-xl p-6 shadow-lg">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          Connected Capsules ({connections.length})
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {connections.map((capsuleId: string) => (
            <Link
              key={capsuleId}
              href={`/dashboard/capsules/${capsuleId}`}
              className="flex items-center gap-2 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <Package className="text-purple-600" size={20} />
              <span className="font-medium text-gray-900">{capsuleId}</span>
            </Link>
          ))}
        </div>
        {connections.length === 0 && (
          <p className="text-gray-500 text-center py-8">No capsule connections</p>
        )}
      </div>
    </div>
  );
}

import { fetchCapsule } from '@/lib/api/capsules';
import Link from 'next/link';
import { ArrowLeft, Package, Cpu } from 'lucide-react';

export default async function CapsuleDetailPage({ params }: { params: { id: string } }) {
  let capsule: any = null;
  try {
    capsule = await fetchCapsule(params.id);
  } catch (error) {
    console.error('Failed to fetch capsule:', error);
  }

  if (!capsule) {
    return (
      <div className="bg-white rounded-xl p-12 text-center shadow-lg">
        <Package className="mx-auto text-gray-400 mb-4" size={48} />
        <p className="text-gray-600">Capsule not found</p>
        <Link href="/dashboard/capsules" className="text-purple-600 hover:underline mt-4 inline-block">
          ← Back to Capsules
        </Link>
      </div>
    );
  }

  return (
    <div>
      <Link
        href="/dashboard/capsules"
        className="inline-flex items-center gap-2 text-purple-600 hover:underline mb-6"
      >
        <ArrowLeft size={20} />
        Back to Capsules
      </Link>

      <div className="bg-white rounded-xl p-8 shadow-lg mb-6">
        <div className="flex items-center gap-4 mb-4">
          <div className="p-3 bg-purple-100 rounded-lg">
            <Package className="text-purple-600" size={32} />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{capsule.name}</h1>
            <p className="text-gray-600">{capsule.id}</p>
          </div>
        </div>
        <p className="text-gray-700 mb-6">{capsule.description}</p>
        <div className="flex items-center gap-4">
          <span
            className={`px-4 py-2 rounded-full font-medium ${
              capsule.status === 'active'
                ? 'bg-green-100 text-green-700'
                : 'bg-gray-100 text-gray-700'
            }`}
          >
            {capsule.status}
          </span>
          <span className="px-4 py-2 bg-blue-100 text-blue-700 rounded-full font-medium">
            {capsule.realm} Realm
          </span>
        </div>
      </div>

      {/* Modules */}
      <div className="bg-white rounded-xl p-6 shadow-lg mb-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Modules ({capsule.modules?.length || 0})</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {capsule.modules?.map((module: any, idx: number) => (
            <div key={idx} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-semibold text-gray-900">{module.name}</h3>
                <span
                  className={`px-2 py-1 rounded text-xs font-medium ${
                    module.status === 'enabled'
                      ? 'bg-green-100 text-green-700'
                      : 'bg-gray-100 text-gray-700'
                  }`}
                >
                  {module.status}
                </span>
              </div>
              <p className="text-sm text-gray-600">{module.type}</p>
              {module.description && (
                <p className="text-sm text-gray-500 mt-2">{module.description}</p>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Connected Engines */}
      <div className="bg-white rounded-xl p-6 shadow-lg">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          Connected Engines ({capsule.engines?.length || 0})
        </h2>
        <div className="flex flex-wrap gap-3">
          {capsule.engines?.map((engine: string) => (
            <Link
              key={engine}
              href={`/dashboard/intelligence-core/${engine}`}
              className="flex items-center gap-2 px-4 py-2 bg-purple-100 text-purple-700 rounded-lg hover:bg-purple-200 transition-colors"
            >
              <Cpu size={16} />
              {engine}
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}

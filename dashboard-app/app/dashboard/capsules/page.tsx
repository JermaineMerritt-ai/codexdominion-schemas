import { fetchCapsules } from '@/lib/api/capsules';
import Link from 'next/link';
import { Package, ChevronRight } from 'lucide-react';

export default async function CapsulesPage() {
  let capsules = [];
  try {
    capsules = await fetchCapsules();
  } catch (error) {
    console.error('Failed to fetch capsules:', error);
  }

  // Group by realm
  const realms = capsules.reduce((acc: any, capsule: any) => {
    const realm = capsule.realm || 'Unknown';
    if (!acc[realm]) acc[realm] = [];
    acc[realm].push(capsule);
    return acc;
  }, {});

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Capsules</h1>
        <p className="text-gray-600">Autonomous execution units across all realms</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <div className="flex items-center gap-3 mb-2">
            <Package className="text-purple-600" size={24} />
            <span className="text-gray-600 font-medium">Total Capsules</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">{capsules.length}</p>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <div className="flex items-center gap-3 mb-2">
            <Package className="text-green-600" size={24} />
            <span className="text-gray-600 font-medium">Active</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">
            {capsules.filter((c: any) => c.status === 'active').length}
          </p>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <div className="flex items-center gap-3 mb-2">
            <Package className="text-blue-600" size={24} />
            <span className="text-gray-600 font-medium">Realms</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">{Object.keys(realms).length}</p>
        </div>
      </div>

      {/* Capsules by Realm */}
      {Object.entries(realms).map(([realm, caps]: [string, any]) => (
        <div key={realm} className="mb-8">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            {realm} Realm ({caps.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {caps.map((capsule: any) => (
              <Link
                key={capsule.id}
                href={`/dashboard/capsules/${capsule.id}`}
                className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-all"
              >
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-bold text-gray-900">{capsule.name}</h3>
                  <ChevronRight className="text-gray-400" size={20} />
                </div>
                <p className="text-gray-600 text-sm mb-4">{capsule.description}</p>
                <div className="flex items-center gap-2">
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-medium ${
                      capsule.status === 'active'
                        ? 'bg-green-100 text-green-700'
                        : 'bg-gray-100 text-gray-700'
                    }`}
                  >
                    {capsule.status}
                  </span>
                  <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-medium">
                    {capsule.modules?.length || 0} modules
                  </span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      ))}

      {capsules.length === 0 && (
        <div className="bg-white rounded-xl p-12 text-center shadow-lg">
          <Package className="mx-auto text-gray-400 mb-4" size={48} />
          <p className="text-gray-600">No capsules found. Check Flask backend connection.</p>
        </div>
      )}
    </div>
  );
}

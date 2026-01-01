import { fetchCouncils } from '@/lib/api/councils';
import Link from 'next/link';
import { Users, CheckCircle, XCircle, ChevronRight } from 'lucide-react';

export default async function CouncilsPage() {
  let councils: any[] = [];
  try {
    councils = await fetchCouncils();
  } catch (error) {
    console.error('Failed to fetch councils:', error);
  }

  const getStatusColor = (status?: string) => {
    switch (status?.toLowerCase()) {
      case 'active':
      case 'operational':
        return 'text-green-600';
      case 'inactive':
      case 'paused':
        return 'text-gray-500';
      default:
        return 'text-blue-600';
    }
  };

  const getStatusIcon = (status?: string) => {
    switch (status?.toLowerCase()) {
      case 'active':
      case 'operational':
        return <CheckCircle className="text-green-600" size={20} />;
      case 'inactive':
      case 'paused':
        return <XCircle className="text-gray-500" size={20} />;
      default:
        return <CheckCircle className="text-blue-600" size={20} />;
    }
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Councils</h1>
        <p className="text-gray-600">Governance and decision-making bodies in Codex Dominion</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">
          <div className="flex items-center gap-3 mb-2">
            <Users className="text-blue-600" size={24} />
            <span className="text-gray-600 font-medium">Total Councils</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">{councils.length}</p>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">
          <div className="flex items-center gap-3 mb-2">
            <CheckCircle className="text-green-600" size={24} />
            <span className="text-gray-600 font-medium">Active</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">
            {councils.filter((c: any) => c.status?.toLowerCase() === 'active' || c.status?.toLowerCase() === 'operational').length}
          </p>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">
          <div className="flex items-center gap-3 mb-2">
            <Users className="text-purple-600" size={24} />
            <span className="text-gray-600 font-medium">Total Agents</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">
            {councils.reduce((sum: number, c: any) => sum + (c.agents?.length || 0), 0)}
          </p>
        </div>
      </div>

      {/* Councils Grid */}
      {councils.length === 0 ? (
        <div className="bg-white rounded-xl p-8 shadow-lg border border-gray-200 text-center">
          <Users className="mx-auto text-gray-400 mb-4" size={48} />
          <p className="text-gray-600">No councils found</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6">
          {councils.map((council: any) => (
            <Link
              key={council.id}
              href={`/dashboard/councils/${council.id}`}
              className="bg-white rounded-xl p-6 shadow-lg border border-gray-200 hover:shadow-xl transition-all hover:border-blue-400 group"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-3">
                    <Users className="text-blue-600 flex-shrink-0" size={24} />
                    <h3 className="text-xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors">
                      {council.name}
                    </h3>
                    {getStatusIcon(council.status)}
                  </div>
                  
                  <p className="text-gray-600 mb-4">{council.description}</p>

                  <div className="flex flex-wrap gap-4 text-sm">
                    {council.domain && (
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-gray-700">Domain:</span>
                        <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full">
                          {council.domain}
                        </span>
                      </div>
                    )}
                    
                    {council.agents && council.agents.length > 0 && (
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-gray-700">Agents:</span>
                        <span className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full">
                          {council.agents.length}
                        </span>
                      </div>
                    )}

                    {council.quorum !== undefined && (
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-gray-700">Quorum:</span>
                        <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full">
                          {council.quorum}
                        </span>
                      </div>
                    )}

                    {council.decision_threshold !== undefined && (
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-gray-700">Threshold:</span>
                        <span className="px-3 py-1 bg-orange-100 text-orange-800 rounded-full">
                          {council.decision_threshold}%
                        </span>
                      </div>
                    )}
                  </div>

                  {council.purpose && (
                    <div className="mt-4 pt-4 border-t border-gray-200">
                      <p className="text-sm text-gray-600">
                        <span className="font-semibold text-gray-700">Purpose:</span> {council.purpose}
                      </p>
                    </div>
                  )}
                </div>

                <ChevronRight
                  className="text-gray-400 group-hover:text-blue-600 group-hover:translate-x-1 transition-all flex-shrink-0 ml-4"
                  size={24}
                />
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

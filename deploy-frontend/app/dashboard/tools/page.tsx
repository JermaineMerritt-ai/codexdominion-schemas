import { fetchTools } from '@/lib/api/tools';
import Link from 'next/link';
import { Wrench, CheckCircle, XCircle, ChevronRight, Package } from 'lucide-react';

export default async function ToolsPage() {
  let tools: any[] = [];
  try {
    tools = await fetchTools();
  } catch (error) {
    console.error('Failed to fetch tools:', error);
  }

  const getStatusColor = (status?: string) => {
    switch (status?.toLowerCase()) {
      case 'active':
      case 'operational':
      case 'available':
        return 'text-green-600';
      case 'inactive':
      case 'deprecated':
        return 'text-gray-500';
      case 'beta':
      case 'experimental':
        return 'text-orange-600';
      default:
        return 'text-blue-600';
    }
  };

  const getStatusIcon = (status?: string) => {
    switch (status?.toLowerCase()) {
      case 'active':
      case 'operational':
      case 'available':
        return <CheckCircle className="text-green-600" size={20} />;
      case 'inactive':
      case 'deprecated':
        return <XCircle className="text-gray-500" size={20} />;
      case 'beta':
      case 'experimental':
        return <Package className="text-orange-600" size={20} />;
      default:
        return <CheckCircle className="text-blue-600" size={20} />;
    }
  };

  const getCategoryColor = (category?: string) => {
    switch (category?.toLowerCase()) {
      case 'automation':
        return 'bg-blue-100 text-blue-800';
      case 'analytics':
        return 'bg-purple-100 text-purple-800';
      case 'communication':
        return 'bg-green-100 text-green-800';
      case 'integration':
        return 'bg-orange-100 text-orange-800';
      case 'ai':
        return 'bg-pink-100 text-pink-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Tools</h1>
        <p className="text-gray-600">Available tools and utilities in Codex Dominion</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">
          <div className="flex items-center gap-3 mb-2">
            <Wrench className="text-blue-600" size={24} />
            <span className="text-gray-600 font-medium">Total Tools</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">{tools.length}</p>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">
          <div className="flex items-center gap-3 mb-2">
            <CheckCircle className="text-green-600" size={24} />
            <span className="text-gray-600 font-medium">Active</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">
            {tools.filter((t: any) => 
              t.status?.toLowerCase() === 'active' || 
              t.status?.toLowerCase() === 'operational' || 
              t.status?.toLowerCase() === 'available'
            ).length}
          </p>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">
          <div className="flex items-center gap-3 mb-2">
            <Package className="text-orange-600" size={24} />
            <span className="text-gray-600 font-medium">Beta/Experimental</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">
            {tools.filter((t: any) => 
              t.status?.toLowerCase() === 'beta' || 
              t.status?.toLowerCase() === 'experimental'
            ).length}
          </p>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">
          <div className="flex items-center gap-3 mb-2">
            <Wrench className="text-purple-600" size={24} />
            <span className="text-gray-600 font-medium">Categories</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">
            {new Set(tools.map((t: any) => t.category).filter(Boolean)).size}
          </p>
        </div>
      </div>

      {/* Tools Grid */}
      {tools.length === 0 ? (
        <div className="bg-white rounded-xl p-8 shadow-lg border border-gray-200 text-center">
          <Wrench className="mx-auto text-gray-400 mb-4" size={48} />
          <p className="text-gray-600">No tools found</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {tools.map((tool: any) => (
            <div
              key={tool.id}
              className="bg-white rounded-xl p-6 shadow-lg border border-gray-200 hover:shadow-xl transition-all hover:border-blue-400 group"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3 flex-1">
                  <Wrench className="text-blue-600 flex-shrink-0" size={24} />
                  <div>
                    <h3 className="text-xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors">
                      {tool.name}
                    </h3>
                    {tool.version && (
                      <span className="text-sm text-gray-500">v{tool.version}</span>
                    )}
                  </div>
                </div>
                {getStatusIcon(tool.status)}
              </div>
              
              <p className="text-gray-600 mb-4">{tool.description}</p>

              <div className="flex flex-wrap gap-2 mb-4">
                {tool.category && (
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getCategoryColor(tool.category)}`}>
                    {tool.category}
                  </span>
                )}
                {tool.status && (
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(tool.status)}`}>
                    {tool.status}
                  </span>
                )}
              </div>

              {tool.capabilities && tool.capabilities.length > 0 && (
                <div className="border-t border-gray-200 pt-4">
                  <p className="text-sm font-semibold text-gray-700 mb-2">Capabilities:</p>
                  <div className="flex flex-wrap gap-2">
                    {tool.capabilities.slice(0, 5).map((capability: string, index: number) => (
                      <span
                        key={index}
                        className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs"
                      >
                        {capability}
                      </span>
                    ))}
                    {tool.capabilities.length > 5 && (
                      <span className="px-2 py-1 bg-gray-100 text-gray-500 rounded text-xs">
                        +{tool.capabilities.length - 5} more
                      </span>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}


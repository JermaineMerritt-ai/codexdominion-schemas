import { TrendingUp, Package, Zap } from 'lucide-react';

const industries = [
  {
    id: 'creator_economy',
    name: 'Creator Economy',
    icon: '🎨',
    color: '#e83e8c',
    description: 'Empowering content creators and digital artists',
    readiness: 65,
    capsules: 3,
    revenue_potential: 'High',
    maturity: 'Emerging',
  },
  {
    id: 'diaspora_commerce',
    name: 'Diaspora Commerce',
    icon: '🌍',
    color: '#17a2b8',
    description: 'Connecting global diaspora communities',
    readiness: 80,
    capsules: 3,
    revenue_potential: 'Very High',
    maturity: 'Growth',
  },
  {
    id: 'youth_entrepreneurship',
    name: 'Youth Entrepreneurship',
    icon: '🚀',
    color: '#28a745',
    description: 'Building tomorrow\'s business leaders',
    readiness: 45,
    capsules: 3,
    revenue_potential: 'High',
    maturity: 'Emerging',
  },
  {
    id: 'education',
    name: 'Education',
    icon: '📚',
    color: '#667eea',
    description: 'Transforming learning experiences',
    readiness: 95,
    capsules: 4,
    revenue_potential: 'High',
    maturity: 'Established',
  },
  {
    id: 'media_culture',
    name: 'Media & Culture',
    icon: '🎬',
    color: '#fd7e14',
    description: 'Preserving and promoting cultural narratives',
    readiness: 70,
    capsules: 4,
    revenue_potential: 'Medium',
    maturity: 'Growth',
  },
];

function getReadinessStatus(readiness: number) {
  if (readiness >= 90) return { label: 'Excellent', color: 'bg-green-500' };
  if (readiness >= 70) return { label: 'Good', color: 'bg-cyan-500' };
  if (readiness >= 50) return { label: 'Fair', color: 'bg-yellow-500' };
  return { label: 'Needs Attention', color: 'bg-orange-500' };
}

export default function IndustriesPage() {
  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Industry Sectors</h1>
        <p className="text-gray-600">Key market sectors for Codex Dominion</p>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <div className="flex items-center gap-3 mb-2">
            <Building2 className="text-purple-600" size={24} />
            <span className="text-gray-600 font-medium">Total Industries</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">{industries.length}</p>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <div className="flex items-center gap-3 mb-2">
            <TrendingUp className="text-green-600" size={24} />
            <span className="text-gray-600 font-medium">High Potential</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">
            {industries.filter(i => i.revenue_potential.includes('High')).length}
          </p>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <div className="flex items-center gap-3 mb-2">
            <Package className="text-blue-600" size={24} />
            <span className="text-gray-600 font-medium">Total Capsules</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">
            {industries.reduce((sum, i) => sum + i.capsules, 0)}
          </p>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <div className="flex items-center gap-3 mb-2">
            <Zap className="text-orange-600" size={24} />
            <span className="text-gray-600 font-medium">Avg Readiness</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">
            {Math.round(industries.reduce((sum, i) => sum + i.readiness, 0) / industries.length)}%
          </p>
        </div>
      </div>

      {/* Industries Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {industries.map((industry) => {
          const status = getReadinessStatus(industry.readiness);
          return (
            <div
              key={industry.id}
              className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-all"
              style={{ borderLeft: `6px solid ${industry.color}` }}
            >
              <div className="flex items-center gap-4 mb-4">
                <div className="text-4xl">{industry.icon}</div>
                <div className="flex-1">
                  <h3 className="text-xl font-bold text-gray-900">{industry.name}</h3>
                  <p className="text-sm text-gray-500 font-mono">{industry.id}</p>
                </div>
              </div>

              <p className="text-gray-600 mb-4">{industry.description}</p>

              {/* Readiness Bar */}
              <div className="mb-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">Capsule Readiness</span>
                  <span className="text-sm font-bold text-purple-600">{industry.readiness}%</span>
                </div>
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className={`h-full ${status.color} transition-all`}
                    style={{ width: `${industry.readiness}%` }}
                  ></div>
                </div>
              </div>

              {/* Footer Info */}
              <div className="flex items-center gap-4 flex-wrap">
                <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-medium">
                  {industry.capsules} capsules
                </span>
                <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">
                  {industry.revenue_potential}
                </span>
                <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
                  {industry.maturity}
                </span>
                <span className={`px-3 py-1 ${status.color.replace('bg-', 'bg-opacity-20 text-')} rounded-full text-sm font-medium`}>
                  {status.label}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Heatmap */}
      <div className="bg-white rounded-xl p-6 shadow-lg">
        <h2 className="text-xl font-bold text-gray-900 mb-4">📊 Capsule Readiness Heatmap</h2>
        <div className="space-y-3">
          {industries.map((industry) => {
            const status = getReadinessStatus(industry.readiness);
            return (
              <div key={industry.id} className="flex items-center gap-4">
                <div className="w-32 font-medium text-gray-700">{industry.name}</div>
                <div className="flex-1 h-8 bg-gray-200 rounded-lg overflow-hidden">
                  <div
                    className={`h-full ${status.color} flex items-center justify-center text-white font-bold text-sm transition-all`}
                    style={{ width: `${industry.readiness}%` }}
                  >
                    {industry.readiness}%
                  </div>
                </div>
                <div className="w-24 text-sm text-gray-600">{industry.capsules} capsules</div>
                <div className={`w-32 px-3 py-1 ${status.color.replace('bg-', 'bg-opacity-20 text-')} rounded-full text-sm font-medium text-center`}>
                  {status.label}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

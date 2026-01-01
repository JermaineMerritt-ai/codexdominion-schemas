import Link from 'next/link';
import { Globe, ArrowRight } from 'lucide-react';

const platforms = [
  {
    id: 'diaspora',
    name: 'Diaspora Platform',
    icon: '🌍',
    description: 'Connecting global diaspora communities with cultural preservation and commerce',
    status: 'Active',
    users: '12,456',
    revenue: '$45,200',
  },
  {
    id: 'teens',
    name: 'Teens Platform',
    icon: '🚀',
    description: 'Youth entrepreneurship and education platform for the next generation',
    status: 'Beta',
    users: '8,234',
    revenue: '$23,100',
  },
];

export default function PlatformsPage() {
  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Platform Overview</h1>
        <p className="text-gray-600">Platform-specific dashboards and analytics</p>
      </div>

      {/* Platform Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {platforms.map((platform) => (
          <Link
            key={platform.id}
            href={`/dashboard/platforms/${platform.id}`}
            className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-all group"
          >
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-4">
                <div className="text-5xl">{platform.icon}</div>
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">{platform.name}</h2>
                  <span
                    className={`inline-block px-3 py-1 rounded-full text-sm font-medium mt-2 ${
                      platform.status === 'Active'
                        ? 'bg-green-100 text-green-700'
                        : 'bg-blue-100 text-blue-700'
                    }`}
                  >
                    {platform.status}
                  </span>
                </div>
              </div>
              <ArrowRight className="text-gray-400 group-hover:text-purple-600 transition-colors" size={24} />
            </div>

            <p className="text-gray-600 mb-6">{platform.description}</p>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <div className="text-2xl font-bold text-purple-600">{platform.users}</div>
                <div className="text-sm text-gray-500">Active Users</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-green-600">{platform.revenue}</div>
                <div className="text-sm text-gray-500">Monthly Revenue</div>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

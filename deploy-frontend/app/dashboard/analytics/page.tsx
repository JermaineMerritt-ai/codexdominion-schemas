import { BarChart3, TrendingUp, Users, DollarSign } from 'lucide-react';

export default function AnalyticsPage() {
  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Analytics Dashboard</h1>
        <p className="text-gray-600">Real-time metrics and insights</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <Users className="text-purple-600" size={32} />
            <span className="text-green-600 text-sm font-semibold">+12%</span>
          </div>
          <div className="text-3xl font-bold text-gray-900">20,690</div>
          <div className="text-sm text-gray-600">Total Users</div>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <DollarSign className="text-green-600" size={32} />
            <span className="text-green-600 text-sm font-semibold">+24%</span>
          </div>
          <div className="text-3xl font-bold text-gray-900">$68,300</div>
          <div className="text-sm text-gray-600">Monthly Revenue</div>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <TrendingUp className="text-blue-600" size={32} />
            <span className="text-green-600 text-sm font-semibold">+8%</span>
          </div>
          <div className="text-3xl font-bold text-gray-900">3,847</div>
          <div className="text-sm text-gray-600">Requests/Min</div>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <BarChart3 className="text-orange-600" size={32} />
            <span className="text-green-600 text-sm font-semibold">99.98%</span>
          </div>
          <div className="text-3xl font-bold text-gray-900">Uptime</div>
          <div className="text-sm text-gray-600">Last 30 Days</div>
        </div>
      </div>

      {/* Charts Placeholder */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Revenue Trend</h2>
          <div className="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
            <div className="text-center text-gray-500">
              <BarChart3 size={48} className="mx-auto mb-2" />
              <p>Chart visualization coming soon</p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <h2 className="text-xl font-bold text-gray-900 mb-4">User Growth</h2>
          <div className="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
            <div className="text-center text-gray-500">
              <TrendingUp size={48} className="mx-auto mb-2" />
              <p>Chart visualization coming soon</p>
            </div>
          </div>
        </div>
      </div>

      {/* Top Performing */}
      <div className="bg-white rounded-xl p-6 shadow-lg">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Top Performing Capsules</h2>
        <div className="space-y-4">
          {[
            { name: 'Treasury Audit', requests: '12,456', uptime: '99.9%' },
            { name: 'Content Creator Suite', requests: '8,234', uptime: '99.7%' },
            { name: 'Education Matrix', requests: '6,543', uptime: '100%' },
          ].map((item, idx) => (
            <div key={idx} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
              <div>
                <h3 className="font-semibold text-gray-900">{item.name}</h3>
                <p className="text-sm text-gray-600">{item.requests} requests</p>
              </div>
              <div className="text-right">
                <div className="text-green-600 font-semibold">{item.uptime}</div>
                <div className="text-xs text-gray-500">Uptime</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

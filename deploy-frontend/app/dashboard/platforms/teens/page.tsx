import Link from 'next/link';
import { ArrowLeft, Rocket, TrendingUp, Users } from 'lucide-react';

export default function TeensPlatformPage() {
  return (
    <div>
      <Link
        href="/dashboard/platforms"
        className="inline-flex items-center gap-2 text-purple-600 hover:underline mb-6"
      >
        <ArrowLeft size={20} />
        Back to Platforms
      </Link>

      <div className="bg-white rounded-xl p-8 shadow-lg mb-6">
        <div className="flex items-center gap-4 mb-4">
          <div className="text-5xl">🚀</div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Teens Platform</h1>
            <p className="text-gray-600">Youth entrepreneurship and education</p>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <Users className="text-purple-600 mb-3" size={32} />
          <div className="text-2xl font-bold text-gray-900">8,234</div>
          <div className="text-sm text-gray-600">Active Users</div>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <TrendingUp className="text-green-600 mb-3" size={32} />
          <div className="text-2xl font-bold text-gray-900">$23,100</div>
          <div className="text-sm text-gray-600">Monthly Revenue</div>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <Rocket className="text-blue-600 mb-3" size={32} />
          <div className="text-2xl font-bold text-gray-900">342</div>
          <div className="text-sm text-gray-600">Active Projects</div>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <TrendingUp className="text-orange-600 mb-3" size={32} />
          <div className="text-2xl font-bold text-gray-900">+42%</div>
          <div className="text-sm text-gray-600">Growth Rate</div>
        </div>
      </div>

      {/* Features */}
      <div className="bg-white rounded-xl p-6 shadow-lg">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Platform Features</h2>
        <div className="space-y-4">
          <div className="flex items-center gap-4 p-4 border border-gray-200 rounded-lg">
            <div className="text-2xl">🤖</div>
            <div>
              <h3 className="font-semibold text-gray-900">AI Business Builder</h3>
              <p className="text-sm text-gray-600">Guided business plan creation with AI</p>
            </div>
          </div>
          <div className="flex items-center gap-4 p-4 border border-gray-200 rounded-lg">
            <div className="text-2xl">🛡️</div>
            <div>
              <h3 className="font-semibold text-gray-900">Safety Systems</h3>
              <p className="text-sm text-gray-600">Age-appropriate content and moderation</p>
            </div>
          </div>
          <div className="flex items-center gap-4 p-4 border border-gray-200 rounded-lg">
            <div className="text-2xl">👨‍👩‍👧</div>
            <div>
              <h3 className="font-semibold text-gray-900">Parent Dashboard</h3>
              <p className="text-sm text-gray-600">Parental controls and progress tracking</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

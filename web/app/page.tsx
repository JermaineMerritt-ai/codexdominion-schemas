'use client';

import { useState, useEffect } from 'react';
import { FeedbackNotificationBadge } from '@/components/feedback-notification-badge';

interface HealthStatus {
  title: string;
  status: 'green' | 'orange' | 'red';
  uptime?: string;
}

interface Ritual {
  name: string;
  status: string;
  icon: string;
}

interface RevenueSnapshot {
  todayRevenue: number;
  weekRevenue: number;
  monthRevenue: number;
  newLeads: number;
  contentPublished: number;
  topProduct: string;
}

const healthSystems: HealthStatus[] = [
  { title: 'Distribution Engine', status: 'green', uptime: '99.8%' },
  { title: 'Marketing Engine', status: 'green', uptime: '99.5%' },
  { title: 'Commerce Engine', status: 'orange', uptime: '97.2%' },
  { title: 'Video Studio', status: 'green', uptime: '99.9%' },
  { title: 'Automations', status: 'red', uptime: '85.4%' },
  { title: 'Avatars', status: 'green', uptime: '99.7%' },
];

const currentRituals: Ritual[] = [
  { name: 'Publishing Flow', status: 'In Progress', icon: '📜' },
  { name: 'Email Sequence', status: 'Scheduled', icon: '⚙️' },
  { name: 'Video Render', status: 'Completed', icon: '🎥' },
];

export default function HomePage() {
  const [revenueData, setRevenueData] = useState<RevenueSnapshot>({
    todayRevenue: 1240,
    weekRevenue: 8930,
    monthRevenue: 32450,
    newLeads: 120,
    contentPublished: 45,
    topProduct: 'Women of Faith Devotional',
  });

  useEffect(() => {
    // TODO: Fetch real-time data from backend
    const fetchData = async () => {
      try {
        const response = await fetch('/api/dashboard-stats');
        if (response.ok) {
          const data = await response.json();
          setRevenueData(data);
        }
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-6 space-y-6 text-white bg-[#0A0F29] h-full overflow-y-auto pb-32">

      {/* Top Row: Health Map */}
      <div className="grid grid-cols-3 gap-4">
        {healthSystems.map((system, idx) => (
          <HealthTile key={idx} {...system} />
        ))}
      </div>

      {/* Current Rituals & Cycles */}
      <div className="bg-[#1A1F3C] p-6 rounded-lg border border-[#FFD700] shadow-xl">
        <h2 className="text-2xl font-bold text-[#FFD700] mb-4 flex items-center">
          <span className="mr-2">🔄</span>
          Current Rituals & Cycles
        </h2>
        <ul className="space-y-3">
          {currentRituals.map((ritual, idx) => (
            <li key={idx} className="flex items-center justify-between p-3 bg-[#0A0F29] rounded-lg">
              <span className="flex items-center space-x-2">
                <span className="text-xl">{ritual.icon}</span>
                <span className="font-medium">{ritual.name}</span>
              </span>
              <span className="px-3 py-1 bg-blue-600 rounded-full text-sm font-semibold">
                {ritual.status}
              </span>
            </li>
          ))}
        </ul>
      </div>

      {/* Revenue & Impact Snapshot */}
      <div className="bg-[#1A1F3C] p-6 rounded-lg border border-[#FFD700] shadow-xl">
        <h2 className="text-2xl font-bold text-[#FFD700] mb-4 flex items-center">
          <span className="mr-2">💰</span>
          Revenue & Impact Snapshot
        </h2>
        <div className="grid grid-cols-3 gap-4">
          <SnapshotCard label="Today's Revenue" value={`$${revenueData.todayRevenue.toLocaleString()}`} />
          <SnapshotCard label="7-Day Revenue" value={`$${revenueData.weekRevenue.toLocaleString()}`} />
          <SnapshotCard label="30-Day Revenue" value={`$${revenueData.monthRevenue.toLocaleString()}`} />
          <SnapshotCard label="New Leads" value={revenueData.newLeads.toString()} />
          <SnapshotCard label="Content Published" value={revenueData.contentPublished.toString()} />
          <SnapshotCard label="Top Product" value={revenueData.topProduct} />
        </div>
      </div>

      {/* Constellation Map + Alerts */}
      <div className="grid grid-cols-[2fr_1fr] gap-4">
        <div className="bg-[#1A1F3C] p-6 rounded-lg border border-[#FFD700] shadow-xl">
          <h2 className="text-2xl font-bold text-[#FFD700] mb-4 flex items-center">
            <span className="mr-2">🌌</span>
            Constellation Map
          </h2>
          <p className="text-sm text-gray-300 mb-4">
            Interactive network of Engines, Avatars, Automations, Video Channels, Commerce Nodes.
          </p>
          {/* Placeholder for graph visualization */}
          <div className="h-64 bg-[#0A0F29] border border-gray-700 rounded-lg flex items-center justify-center relative overflow-hidden group">
            <span className="text-gray-400 z-10">[Constellation Graph - Coming Soon]</span>
            <div className="absolute inset-0 bg-gradient-to-br from-[#FFD700]/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          </div>
        </div>

        <div className="bg-[#1A1F3C] p-6 rounded-lg border border-[#FFD700] shadow-xl">
          <h2 className="text-2xl font-bold text-[#FFD700] mb-4 flex items-center">
            <span className="mr-2">🚨</span>
            Alerts & Exceptions
          </h2>
          <ul className="space-y-3 text-sm">
            <li className="p-3 bg-[#0A0F29] rounded-lg border-l-4 border-red-500">
              <span className="text-red-400 font-semibold">⚠️ Automation Flow Failure</span>
              <p className="text-gray-400 text-xs mt-1">2 days ago</p>
            </li>
            <li className="p-3 bg-[#0A0F29] rounded-lg border-l-4 border-orange-500">
              <span className="text-orange-400 font-semibold">🔔 Video Render Queue</span>
              <p className="text-gray-400 text-xs mt-1">Delayed</p>
            </li>
            <li className="p-3 bg-[#0A0F29] rounded-lg border-l-4 border-yellow-500">
              <span className="text-yellow-400 font-semibold">📡 Grafana Alert</span>
              <p className="text-gray-400 text-xs mt-1">CPU spike in Commerce Engine</p>
            </li>
          </ul>
        </div>
      </div>

      {/* Quick Actions Dock */}
      <div className="flex flex-wrap gap-3 bg-[#1A1F3C] p-6 rounded-lg border border-[#FFD700] shadow-xl">
        <a href="/feedback" className="px-6 py-3 bg-[#FFD700] text-black font-semibold rounded-lg hover:bg-[#FFA500] transition-all flex items-center space-x-2">
          <span>📝</span>
          <span>Council Feedback</span>
        </a>
        <a href="/annotations" className="px-6 py-3 bg-[#FFD700] text-black font-semibold rounded-lg hover:bg-[#FFA500] transition-all flex items-center space-x-2">
          <span>📋</span>
          <span>Capsule Annotations</span>
        </a>
        <a href="/broadcast" className="px-6 py-3 bg-[#FFD700] text-black font-semibold rounded-lg hover:bg-[#FFA500] transition-all flex items-center space-x-2">
          <span>📡</span>
          <span>Sovereign Broadcast</span>
        </a>
        <button className="px-6 py-3 bg-[#FFD700] text-black font-semibold rounded-lg hover:bg-[#FFA500] transition-all flex items-center space-x-2">
          <span>📄</span>
          <span>New Document</span>
        </button>
        <button className="px-6 py-3 bg-[#FFD700] text-black font-semibold rounded-lg hover:bg-[#FFA500] transition-all flex items-center space-x-2">
          <span>🛒</span>
          <span>New Product</span>
        </button>
        <button className="px-6 py-3 bg-[#FFD700] text-black font-semibold rounded-lg hover:bg-[#FFA500] transition-all flex items-center space-x-2">
          <span>⚙️</span>
          <span>New Automation</span>
        </button>
        <button className="px-6 py-3 bg-[#FFD700] text-black font-semibold rounded-lg hover:bg-[#FFA500] transition-all flex items-center space-x-2">
          <span>🎬</span>
          <span>New Video Project</span>
        </button>
        <button className="px-6 py-3 bg-[#FFD700] text-black font-semibold rounded-lg hover:bg-[#FFA500] transition-all flex items-center space-x-2">
          <span>🔥</span>
          <span>Run Ritual</span>
        </button>
      </div>

      {/* Pinned AI Insights */}
      <div className="bg-[#1A1F3C] p-6 rounded-lg border border-[#FFD700] shadow-xl">
        <h2 className="text-2xl font-bold text-[#FFD700] mb-4 flex items-center">
          <span className="mr-2">✨</span>
          Pinned AI Insights
        </h2>
        <ul className="space-y-3">
          <li className="p-4 bg-[#0A0F29] rounded-lg border-l-4 border-green-500">
            <span className="text-green-400">✨</span>
            <span className="ml-2">"Your Christmas story funnel has 80% open rate."</span>
          </li>
          <li className="p-4 bg-[#0A0F29] rounded-lg border-l-4 border-red-500">
            <span className="text-red-400">⚠️</span>
            <span className="ml-2">"3 automations have been failing silently for 2 days."</span>
          </li>
          <li className="p-4 bg-[#0A0F29] rounded-lg border-l-4 border-blue-500">
            <span className="text-blue-400">💡</span>
            <span className="ml-2">"Consider bundling devotionals for higher conversion rate."</span>
          </li>
        </ul>
      </div>
    </div>
  );
}

// Health Tile Component
function HealthTile({ title, status, uptime }: HealthStatus) {
  const colors = {
    green: { bg: 'bg-green-600', text: 'text-green-400', border: 'border-green-500' },
    orange: { bg: 'bg-orange-600', text: 'text-orange-400', border: 'border-orange-500' },
    red: { bg: 'bg-red-600', text: 'text-red-400', border: 'border-red-500' },
  };

  const color = colors[status];

  return (
    <div className={`bg-[#1A1F3C] p-4 rounded-lg border ${color.border} flex flex-col justify-between hover:shadow-lg transition-shadow`}>
      <div className="flex items-center justify-between mb-2">
        <span className="font-semibold">{title}</span>
        <span className={`px-3 py-1 rounded-full text-xs font-bold ${color.bg} uppercase`}>
          {status}
        </span>
      </div>
      {uptime && (
        <div className="text-xs text-gray-400">
          <span className={color.text}>Uptime: {uptime}</span>
        </div>
      )}
    </div>
  );
}

// Snapshot Card Component
function SnapshotCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="bg-[#0A0F29] p-4 rounded-lg border border-gray-700 text-center hover:border-[#FFD700] transition-colors">
      <p className="text-sm text-gray-400 mb-2">{label}</p>
      <p className="text-xl font-bold text-[#FFD700]">{value}</p>
    </div>
  );
}

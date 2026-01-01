import React from 'react';
import Link from 'next/link';

interface AdminOverviewCardProps {
  activeYouth: number;
  activeCircles: number;
  missionsCompletedThisWeek: number;
  regionsActive: number;
}

export default function AdminOverviewCard({
  activeYouth,
  activeCircles,
  missionsCompletedThisWeek,
  regionsActive
}: AdminOverviewCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-red-500">
      <div className="flex items-center gap-2 mb-4">
        <span className="text-2xl">👑</span>
        <h2 className="text-xl font-bold text-gray-900">System Overview</h2>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        {/* Active Youth */}
        <div className="bg-blue-50 rounded-lg p-4">
          <p className="text-sm text-gray-600 mb-1">Active Youth</p>
          <p className="text-3xl font-bold text-blue-600">{activeYouth}</p>
        </div>

        {/* Active Circles */}
        <div className="bg-purple-50 rounded-lg p-4">
          <p className="text-sm text-gray-600 mb-1">Active Circles</p>
          <p className="text-3xl font-bold text-purple-600">{activeCircles}</p>
        </div>

        {/* Missions Completed */}
        <div className="bg-green-50 rounded-lg p-4">
          <p className="text-sm text-gray-600 mb-1">Missions (Week)</p>
          <p className="text-3xl font-bold text-green-600">{missionsCompletedThisWeek}</p>
        </div>

        {/* Regions Active */}
        <div className="bg-orange-50 rounded-lg p-4">
          <p className="text-sm text-gray-600 mb-1">Regions Active</p>
          <p className="text-3xl font-bold text-orange-600">{regionsActive}</p>
        </div>
      </div>

      <div className="space-y-2">
        <Link
          href="/admin/missions"
          className="block w-full px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors text-center"
        >
          Manage Missions
        </Link>
        <Link
          href="/admin/circles"
          className="block w-full px-4 py-2 border border-red-500 text-red-500 rounded hover:bg-red-50 transition-colors text-center"
        >
          Manage Circles
        </Link>
        <Link
          href="/admin/content"
          className="block w-full px-4 py-2 border border-red-500 text-red-500 rounded hover:bg-red-50 transition-colors text-center"
        >
          View Stories & Curriculum
        </Link>
      </div>
    </div>
  );
}

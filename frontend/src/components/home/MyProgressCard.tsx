import React from 'react';

interface MyProgressCardProps {
  missionsCompletedThisSeason: number;
  sessionsAttendedThisMonth: number;
  currentStreak: number;
}

export default function MyProgressCard({
  missionsCompletedThisSeason,
  sessionsAttendedThisMonth,
  currentStreak
}: MyProgressCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
      <div className="flex items-center gap-2 mb-4">
        <span className="text-2xl">📈</span>
        <h2 className="text-xl font-bold text-gray-900">My Progress</h2>
      </div>

      <div className="space-y-4">
        {/* Missions Completed */}
        <div className="flex items-center justify-between bg-gray-50 rounded-lg p-4">
          <div>
            <p className="text-sm text-gray-600">Missions Completed</p>
            <p className="text-xs text-gray-500">This Season</p>
          </div>
          <div className="text-3xl font-bold text-blue-600">
            {missionsCompletedThisSeason}
          </div>
        </div>

        {/* Sessions Attended */}
        <div className="flex items-center justify-between bg-gray-50 rounded-lg p-4">
          <div>
            <p className="text-sm text-gray-600">Sessions Attended</p>
            <p className="text-xs text-gray-500">This Month</p>
          </div>
          <div className="text-3xl font-bold text-purple-600">
            {sessionsAttendedThisMonth}
          </div>
        </div>

        {/* Streak */}
        <div className="flex items-center justify-between bg-gray-50 rounded-lg p-4">
          <div>
            <p className="text-sm text-gray-600">Participation Streak</p>
            <p className="text-xs text-gray-500">Consecutive Weeks</p>
          </div>
          <div className="flex items-center gap-1">
            <span className="text-3xl font-bold text-orange-600">{currentStreak}</span>
            <span className="text-xl">🔥</span>
          </div>
        </div>
      </div>
    </div>
  );
}

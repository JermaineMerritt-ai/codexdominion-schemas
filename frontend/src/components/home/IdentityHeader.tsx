import React from 'react';

interface IdentityHeaderProps {
  userName: string;
  role: 'YOUTH' | 'YOUTH_CAPTAIN' | 'CREATOR' | 'ADMIN' | 'REGIONAL_DIRECTOR' | 'COUNCIL';
  seasonName: string;
  currentWeek: number;
}

export default function IdentityHeader({ userName, role, seasonName, currentWeek }: IdentityHeaderProps) {
  const roleDisplay = {
    YOUTH: 'Youth',
    YOUTH_CAPTAIN: 'Youth Captain',
    CREATOR: 'Creator',
    ADMIN: 'Admin',
    REGIONAL_DIRECTOR: 'Regional Director',
    COUNCIL: 'Council'
  };

  const roleColors = {
    YOUTH: 'bg-blue-100 text-blue-800',
    YOUTH_CAPTAIN: 'bg-purple-100 text-purple-800',
    CREATOR: 'bg-green-100 text-green-800',
    ADMIN: 'bg-red-100 text-red-800',
    REGIONAL_DIRECTOR: 'bg-orange-100 text-orange-800',
    COUNCIL: 'bg-yellow-100 text-yellow-800'
  };

  return (
    <div className="bg-gradient-to-r from-slate-900 to-slate-800 text-white px-6 py-4 shadow-lg">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Left: Greeting + Role */}
        <div className="flex items-center gap-4">
          <div className="text-2xl">🔥</div>
          <div>
            <h1 className="text-2xl font-bold">Rise, {userName}.</h1>
            <span className={`inline-block mt-1 px-3 py-1 rounded-full text-sm font-medium ${roleColors[role]}`}>
              {roleDisplay[role]}
            </span>
          </div>
        </div>

        {/* Right: Season + Week */}
        <div className="text-right">
          <div className="text-lg font-semibold">Season: {seasonName}</div>
          <div className="text-sm text-gray-300">Week {currentWeek}</div>
        </div>
      </div>
    </div>
  );
}

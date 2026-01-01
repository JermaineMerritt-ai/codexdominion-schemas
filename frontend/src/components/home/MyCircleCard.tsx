import React from 'react';
import Link from 'next/link';

interface MyCircleCardProps {
  circleId: string;
  circleName: string;
  role: 'YOUTH' | 'YOUTH_CAPTAIN';
  nextSessionDate?: string;
  nextSessionTime?: string;
  memberCount?: number;
  lastAttendanceRate?: number;
}

export default function MyCircleCard({
  circleId,
  circleName,
  role,
  nextSessionDate,
  nextSessionTime,
  memberCount,
  lastAttendanceRate
}: MyCircleCardProps) {
  const isYouth = role === 'YOUTH';
  const isCaptain = role === 'YOUTH_CAPTAIN';

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-indigo-500">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-2xl">⭕</span>
        <h2 className="text-xl font-bold text-gray-900">My Circle</h2>
      </div>

      <h3 className="text-lg font-semibold text-gray-800 mb-4">{circleName}</h3>

      {/* Youth View */}
      {isYouth && (
        <>
          {nextSessionDate && nextSessionTime ? (
            <div className="mb-4">
              <p className="text-sm text-gray-600 mb-1">Next Session:</p>
              <p className="text-gray-800 font-medium">
                {new Date(nextSessionDate).toLocaleDateString()} at {nextSessionTime}
              </p>
            </div>
          ) : (
            <p className="text-gray-500 italic mb-4">No upcoming sessions scheduled</p>
          )}

          <div className="flex gap-3">
            <Link
              href={`/circles/${circleId}`}
              className="px-4 py-2 bg-indigo-500 text-white rounded hover:bg-indigo-600 transition-colors"
            >
              {nextSessionDate ? "Join This Week's Circle" : 'View Circle'}
            </Link>
            <Link
              href={`/circles/${circleId}/sessions`}
              className="px-4 py-2 border border-indigo-500 text-indigo-500 rounded hover:bg-indigo-50 transition-colors"
            >
              View Sessions
            </Link>
          </div>
        </>
      )}

      {/* Captain View */}
      {isCaptain && (
        <>
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div className="bg-gray-50 rounded p-3">
              <p className="text-sm text-gray-600">Members</p>
              <p className="text-2xl font-bold text-gray-900">{memberCount || 0}</p>
            </div>
            <div className="bg-gray-50 rounded p-3">
              <p className="text-sm text-gray-600">Last Session</p>
              <p className="text-2xl font-bold text-gray-900">
                {lastAttendanceRate !== undefined ? `${Math.round(lastAttendanceRate)}%` : 'N/A'}
              </p>
            </div>
          </div>

          <div className="flex gap-3">
            <Link
              href={`/circles/${circleId}/schedule-session`}
              className="px-4 py-2 bg-indigo-500 text-white rounded hover:bg-indigo-600 transition-colors"
            >
              Schedule Session
            </Link>
            <Link
              href={`/circles/${circleId}/attendance`}
              className="px-4 py-2 border border-indigo-500 text-indigo-500 rounded hover:bg-indigo-50 transition-colors"
            >
              Record Attendance
            </Link>
          </div>
        </>
      )}
    </div>
  );
}

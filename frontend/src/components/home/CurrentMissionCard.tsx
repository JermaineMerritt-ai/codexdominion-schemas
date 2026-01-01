import React from 'react';
import Link from 'next/link';

interface CurrentMissionCardProps {
  missionId: string;
  title: string;
  description: string;
  status: 'not-started' | 'in-progress' | 'submitted' | 'completed';
  dueDate?: string;
}

export default function CurrentMissionCard({ 
  missionId, 
  title, 
  description, 
  status,
  dueDate 
}: CurrentMissionCardProps) {
  const statusConfig = {
    'not-started': { color: 'text-gray-600', bg: 'bg-gray-100', label: 'Not Started' },
    'in-progress': { color: 'text-blue-600', bg: 'bg-blue-100', label: 'In Progress' },
    'submitted': { color: 'text-green-600', bg: 'bg-green-100', label: 'Submitted' },
    'completed': { color: 'text-green-700', bg: 'bg-green-200', label: 'Completed' }
  };

  const config = statusConfig[status];

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-2xl">🎯</span>
        <h2 className="text-xl font-bold text-gray-900">Your Mission This Week</h2>
      </div>

      <div className="mb-3">
        <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${config.bg} ${config.color}`}>
          {config.label}
        </span>
      </div>

      <h3 className="text-lg font-semibold text-gray-800 mb-2">{title}</h3>
      <p className="text-gray-600 mb-4">{description}</p>

      {dueDate && (
        <p className="text-sm text-gray-500 mb-4">
          Due: {new Date(dueDate).toLocaleDateString()}
        </p>
      )}

      <div className="flex gap-3">
        <Link 
          href={`/missions/${missionId}`}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
        >
          View Mission Details
        </Link>
        
        {status !== 'submitted' && status !== 'completed' && (
          <Link
            href={`/missions/${missionId}/submit`}
            className="px-4 py-2 border border-blue-500 text-blue-500 rounded hover:bg-blue-50 transition-colors"
          >
            Submit My Work
          </Link>
        )}
      </div>
    </div>
  );
}

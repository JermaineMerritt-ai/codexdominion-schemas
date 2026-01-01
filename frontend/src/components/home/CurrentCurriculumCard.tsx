import React from 'react';
import Link from 'next/link';

interface CurriculumModule {
  id: string;
  type: 'STORY' | 'LESSON' | 'ACTIVITY';
  title: string;
}

interface CurrentCurriculumCardProps {
  modules: CurriculumModule[];
  seasonName: string;
  week: number;
}

export default function CurrentCurriculumCard({ modules, seasonName, week }: CurrentCurriculumCardProps) {
  const typeColors = {
    STORY: 'bg-orange-100 text-orange-700',
    LESSON: 'bg-purple-100 text-purple-700',
    ACTIVITY: 'bg-green-100 text-green-700'
  };

  const typeIcons = {
    STORY: '📖',
    LESSON: '📝',
    ACTIVITY: '🎨'
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-2xl">📚</span>
        <h2 className="text-xl font-bold text-gray-900">This Week's Lesson & Activity</h2>
      </div>

      <div className="text-sm text-gray-500 mb-4">
        {seasonName} — Week {week}
      </div>

      {modules.length === 0 ? (
        <p className="text-gray-500 italic">No curriculum modules available for this week.</p>
      ) : (
        <div className="space-y-3 mb-4">
          {modules.map((module) => (
            <div key={module.id} className="flex items-start gap-3">
              <span className="text-xl">{typeIcons[module.type]}</span>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className={`px-2 py-1 rounded text-xs font-medium ${typeColors[module.type]}`}>
                    {module.type}
                  </span>
                </div>
                <p className="text-gray-800 font-medium">{module.title}</p>
              </div>
            </div>
          ))}
        </div>
      )}

      <Link
        href="/curriculum"
        className="inline-block px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600 transition-colors"
      >
        Open Session Guide
      </Link>
    </div>
  );
}

import React, { useState } from 'react';

interface CurrentStoryCardProps {
  title: string;
  content: string;
  seasonName?: string;
  week?: number;
}

export default function CurrentStoryCard({ title, content, seasonName, week }: CurrentStoryCardProps) {
  const [showFullStory, setShowFullStory] = useState(false);

  // Extract first 2-3 lines as excerpt
  const lines = content.split('\n').filter(line => line.trim());
  const excerpt = lines.slice(0, 3).join(' ').substring(0, 200) + '...';

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-2xl">📖</span>
        <h2 className="text-xl font-bold text-gray-900">Story of the Week</h2>
      </div>

      {seasonName && week && (
        <div className="text-xs text-gray-500 mb-2">
          {seasonName} — Week {week}
        </div>
      )}

      <h3 className="text-lg font-semibold text-gray-800 mb-2">{title}</h3>
      <p className="text-gray-600 mb-4">{excerpt}</p>

      <button
        onClick={() => setShowFullStory(true)}
        className="px-4 py-2 bg-orange-500 text-white rounded hover:bg-orange-600 transition-colors"
      >
        Read Full Story
      </button>

      {/* Modal for full story */}
      {showFullStory && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-3xl max-h-[80vh] overflow-y-auto p-8 relative">
            <button
              onClick={() => setShowFullStory(false)}
              className="absolute top-4 right-4 text-gray-500 hover:text-gray-700 text-2xl"
            >
              ×
            </button>
            <h2 className="text-2xl font-bold mb-4">{title}</h2>
            <div className="prose max-w-none text-gray-700 whitespace-pre-wrap">
              {content}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

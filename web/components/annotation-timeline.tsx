'use client';

import { useState, useEffect } from 'react';
import { CapsuleAnnotation, getCapsuleAnnotationManager } from '@/lib/annotations/capsule-annotations';

export interface AnnotationTimelineProps {
  capsuleId?: string;
  engine?: string;
  limit?: number;
}

export function AnnotationTimeline({ capsuleId, engine, limit }: AnnotationTimelineProps) {
  const [annotations, setAnnotations] = useState<CapsuleAnnotation[]>([]);
  const [filter, setFilter] = useState<'all' | 'correlation' | 'revenue-impact' | 'performance'>('all');

  useEffect(() => {
    const manager = getCapsuleAnnotationManager();

    const loadAnnotations = () => {
      let results: CapsuleAnnotation[];

      if (capsuleId) {
        results = manager.getAnnotationsByCapsule(capsuleId);
      } else if (engine) {
        results = manager.getAnnotationsByEngine(engine);
      } else {
        results = manager.getAllAnnotations();
      }

      if (filter !== 'all') {
        results = results.filter((a) => a.tags?.includes(filter));
      }

      if (limit) {
        results = results.slice(0, limit);
      }

      setAnnotations(results);
    };

    loadAnnotations();

    // Subscribe to new annotations
    manager.onAnnotation(() => {
      loadAnnotations();
    });
  }, [capsuleId, engine, filter, limit]);

  const handleDelete = (id: string) => {
    const manager = getCapsuleAnnotationManager();
    const success = manager.deleteAnnotation(id);
    if (success) {
      setAnnotations((prev) => prev.filter((a) => a.id !== id));
    }
  };

  return (
    <div className="bg-[#1A1F3C] rounded-lg border-2 border-[#FFD700] p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-[#FFD700]">
          📋 Annotation Timeline
          {annotations.length > 0 && (
            <span className="ml-2 text-sm text-gray-400">({annotations.length})</span>
          )}
        </h2>

        {/* Tag Filter */}
        <div className="flex gap-2">
          {['all', 'correlation', 'revenue-impact', 'performance'].map((tag) => (
            <button
              key={tag}
              onClick={() => setFilter(tag as typeof filter)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                filter === tag
                  ? 'bg-[#FFD700] text-[#0A0F29]'
                  : 'bg-[#0A0F29] text-gray-400 hover:bg-[#2A2F4C]'
              }`}
            >
              {tag === 'all' ? 'All' : `#${tag}`}
            </button>
          ))}
        </div>
      </div>

      {annotations.length === 0 ? (
        <div className="text-center py-8 text-gray-400">
          <p className="text-lg mb-2">📋</p>
          <p>No annotations found</p>
          {filter !== 'all' && (
            <p className="text-sm mt-2">Try changing the filter or add new annotations</p>
          )}
        </div>
      ) : (
        <div className="space-y-3">
          {annotations.map((annotation) => (
            <div
              key={annotation.id}
              className="bg-[#0A0F29] rounded-lg p-4 border-l-4 border-[#FFD700]"
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-2">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-bold text-white">👤 {annotation.author}</span>
                    <span className="text-xs text-gray-500">
                      {new Date(annotation.timestamp).toLocaleString()}
                    </span>
                  </div>
                  <p className="text-xs text-gray-400">
                    {annotation.engine} • Capsule: {annotation.capsuleId}
                  </p>
                </div>

                <button
                  onClick={() => handleDelete(annotation.id)}
                  className="text-gray-500 hover:text-red-400 text-xs px-2 py-1 transition-colors"
                  title="Delete annotation"
                >
                  🗑️
                </button>
              </div>

              {/* Note */}
              <p className="text-white leading-relaxed mb-3">{annotation.note}</p>

              {/* Tags */}
              {annotation.tags && annotation.tags.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-2">
                  {annotation.tags.map((tag) => (
                    <span
                      key={tag}
                      className="px-2 py-1 bg-[#1A1F3C] rounded text-xs text-[#FFD700] border border-[#FFD700]/30"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              )}

              {/* Metadata */}
              {annotation.metadata && Object.keys(annotation.metadata).length > 0 && (
                <details className="mt-3">
                  <summary className="cursor-pointer text-xs text-gray-500 hover:text-[#FFD700]">
                    📊 View Metadata
                  </summary>
                  <pre className="mt-2 bg-black/30 rounded p-2 text-xs text-gray-400 overflow-x-auto">
                    {JSON.stringify(annotation.metadata, null, 2)}
                  </pre>
                </details>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

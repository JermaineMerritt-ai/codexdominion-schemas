'use client';

import { useState, useEffect } from 'react';
import { CapsuleAnnotation, getCapsuleAnnotationManager } from '@/lib/annotations/capsule-annotations';
import { useSeedAnnotations } from '@/hooks/useSeedAnnotations';
import AnnotationArchive from '@/components/annotation-archive';
import AnnotationExport from '@/components/annotation-export';
import { ExportControls } from '@/components/export-controls';
import SpatialAudioControls from '@/components/spatial-audio-controls';

export default function AnnotationsPage() {
  useSeedAnnotations();

  const [annotations, setAnnotations] = useState<CapsuleAnnotation[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedEngine, setSelectedEngine] = useState<string>('all');
  const [selectedTag, setSelectedTag] = useState<string>('all');
  const [stats, setStats] = useState<ReturnType<typeof getCapsuleAnnotationManager.prototype.getStatistics>>();
  const [viewMode, setViewMode] = useState<'dashboard' | 'archive' | 'export'>('dashboard');

  useEffect(() => {
    const manager = getCapsuleAnnotationManager();
    loadAnnotations();
    setStats(manager.getStatistics());

    // Refresh every 10 seconds
    const interval = setInterval(() => {
      loadAnnotations();
      setStats(manager.getStatistics());
    }, 10000);

    return () => clearInterval(interval);
  }, [searchQuery, selectedEngine, selectedTag]);

  const loadAnnotations = () => {
    const manager = getCapsuleAnnotationManager();
    let results: CapsuleAnnotation[];

    if (searchQuery.trim()) {
      results = manager.searchAnnotations(searchQuery);
    } else {
      results = manager.getAllAnnotations();
    }

    if (selectedEngine !== 'all') {
      results = results.filter((a) => a.engine === selectedEngine);
    }

    if (selectedTag !== 'all') {
      results = results.filter((a) => a.tags?.includes(selectedTag));
    }

    setAnnotations(results);
  };

  const handleDelete = (id: string) => {
    const manager = getCapsuleAnnotationManager();
    const success = manager.deleteAnnotation(id);
    if (success) {
      loadAnnotations();
      setStats(manager.getStatistics());
    }
  };

  const handleExport = () => {
    const manager = getCapsuleAnnotationManager();
    const json = manager.exportToJSON();
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `capsule-annotations-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleClearAll = () => {
    if (confirm('Are you sure you want to delete all annotations? This cannot be undone.')) {
      const manager = getCapsuleAnnotationManager();
      manager.clearAll();
      loadAnnotations();
      setStats(manager.getStatistics());
    }
  };

  const engines = stats ? Object.keys(stats.byEngine) : [];
  const topTags = stats ? Object.entries(stats.topTags).sort((a, b) => (b[1] as number) - (a[1] as number)).map(([tag]) => tag) : [];

  return (
    <div className="min-h-screen bg-[#0A0F29] p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold text-[#FFD700]">📋 Capsule Annotations</h1>
          <div className="flex gap-3">
            <button
              onClick={() => setViewMode('dashboard')}
              className={`px-4 py-2 rounded font-medium transition-colors ${
                viewMode === 'dashboard'
                  ? 'bg-[#FFD700] text-[#0A0F29]'
                  : 'bg-[#2A2F4C] text-[#FFD700] hover:bg-[#3A3F5C]'
              }`}
            >
              📊 Dashboard
            </button>
            <button
              onClick={() => setViewMode('archive')}
              className={`px-4 py-2 rounded font-medium transition-colors ${
                viewMode === 'archive'
                  ? 'bg-[#FFD700] text-[#0A0F29]'
                  : 'bg-[#2A2F4C] text-[#FFD700] hover:bg-[#3A3F5C]'
              }`}
            >
              📚 Archive
            </button>
            <button
              onClick={() => setViewMode('export')}
              className={`px-4 py-2 rounded font-medium transition-colors ${
                viewMode === 'export'
                  ? 'bg-[#FFD700] text-[#0A0F29]'
                  : 'bg-[#2A2F4C] text-[#FFD700] hover:bg-[#3A3F5C]'
              }`}
            >
              📥 Export
            </button>
            <button
              onClick={handleClearAll}
              className="px-4 py-2 bg-red-900/30 text-red-400 rounded font-medium hover:bg-red-900/50 transition-colors"
            >
              🗑️ Clear All
            </button>
          </div>
        </div>

        {viewMode === 'archive' ? (
          <AnnotationArchive />
        ) : viewMode === 'export' ? (
          <div className="space-y-6">
            {/* Spatial Audio Experience */}
            <SpatialAudioControls />

            {/* Export Components */}
            <AnnotationExport
              cycle={undefined}
              engine={selectedEngine !== 'all' ? selectedEngine : undefined}
              role={undefined}
            />
            <ExportControls
              currentFilters={{
                engine: selectedEngine !== 'all' ? selectedEngine : undefined,
                role: undefined,
                cycle: undefined,
              }}
            />
          </div>
        ) : (
          <>
            {/* Statistics Grid */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-[#1A1F3C] rounded-lg p-4 border border-[#FFD700]/30">
              <p className="text-gray-400 text-sm mb-1">Total Annotations</p>
              <p className="text-3xl font-bold text-[#FFD700]">{stats.total}</p>
            </div>
            <div className="bg-[#1A1F3C] rounded-lg p-4 border border-[#FFD700]/30">
              <p className="text-gray-400 text-sm mb-1">Engines Monitored</p>
              <p className="text-3xl font-bold text-white">{Object.keys(stats.byEngine).length}</p>
            </div>
            <div className="bg-[#1A1F3C] rounded-lg p-4 border border-[#FFD700]/30">
              <p className="text-gray-400 text-sm mb-1">Contributors</p>
              <p className="text-3xl font-bold text-white">{Object.keys(stats.byAuthor).length}</p>
            </div>
            <div className="bg-[#1A1F3C] rounded-lg p-4 border border-[#FFD700]/30">
              <p className="text-gray-400 text-sm mb-1">Unique Tags</p>
              <p className="text-3xl font-bold text-white">{Object.keys(stats.topTags).length}</p>
            </div>
          </div>
        )}

        {/* Search and Filters */}
        <div className="bg-[#1A1F3C] rounded-lg p-6 mb-6 border border-[#FFD700]/30">
          <div className="space-y-4">
            {/* Search */}
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">🔍 Search</label>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search annotations, engines, authors..."
                className="w-full bg-[#0A0F29] text-white border border-[#FFD700]/30 rounded p-3 focus:border-[#FFD700] focus:outline-none"
              />
            </div>

            {/* Engine Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">⚙️ Engine</label>
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => setSelectedEngine('all')}
                  className={`px-4 py-2 rounded font-medium transition-colors ${
                    selectedEngine === 'all'
                      ? 'bg-[#FFD700] text-[#0A0F29]'
                      : 'bg-[#0A0F29] text-gray-400 hover:bg-[#2A2F4C]'
                  }`}
                >
                  All Engines
                </button>
                {engines.map((engine) => (
                  <button
                    key={engine}
                    onClick={() => setSelectedEngine(engine)}
                    className={`px-4 py-2 rounded font-medium transition-colors ${
                      selectedEngine === engine
                        ? 'bg-[#FFD700] text-[#0A0F29]'
                        : 'bg-[#0A0F29] text-gray-400 hover:bg-[#2A2F4C]'
                    }`}
                  >
                    {engine}
                    <span className="ml-2 text-xs opacity-70">({stats?.byEngine[engine]})</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Tag Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">🏷️ Tags</label>
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => setSelectedTag('all')}
                  className={`px-4 py-2 rounded font-medium transition-colors ${
                    selectedTag === 'all'
                      ? 'bg-[#FFD700] text-[#0A0F29]'
                      : 'bg-[#0A0F29] text-gray-400 hover:bg-[#2A2F4C]'
                  }`}
                >
                  All Tags
                </button>
                {topTags.slice(0, 8).map((tag) => (
                  <button
                    key={tag}
                    onClick={() => setSelectedTag(tag)}
                    className={`px-4 py-2 rounded font-medium transition-colors ${
                      selectedTag === tag
                        ? 'bg-[#FFD700] text-[#0A0F29]'
                        : 'bg-[#0A0F29] text-gray-400 hover:bg-[#2A2F4C]'
                    }`}
                  >
                    #{tag}
                    <span className="ml-2 text-xs opacity-70">({stats?.topTags[tag]})</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Annotations List */}
        <div className="space-y-4">
          {annotations.length === 0 ? (
            <div className="bg-[#1A1F3C] rounded-lg p-12 text-center border border-[#FFD700]/30">
              <p className="text-4xl mb-4">📋</p>
              <p className="text-xl text-gray-400 mb-2">No annotations found</p>
              <p className="text-sm text-gray-500">Try adjusting your search or filters</p>
            </div>
          ) : (
            annotations.map((annotation) => (
              <div
                key={annotation.id}
                className="bg-[#1A1F3C] rounded-lg p-6 border-l-4 border-[#FFD700] hover:bg-[#1A1F3C]/80 transition-colors"
              >
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="font-bold text-white">👤 {annotation.author}</span>
                      <span className="text-sm text-gray-500">
                        {new Date(annotation.timestamp).toLocaleString()}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium text-[#FFD700]">{annotation.engine}</span>
                      <span className="text-gray-600">•</span>
                      <span className="text-xs font-mono text-gray-400">{annotation.capsuleId}</span>
                    </div>
                  </div>

                  <button
                    onClick={() => handleDelete(annotation.id)}
                    className="text-gray-500 hover:text-red-400 px-3 py-1 transition-colors"
                    title="Delete annotation"
                  >
                    🗑️ Delete
                  </button>
                </div>

                {/* Note */}
                <p className="text-white text-lg leading-relaxed mb-4">{annotation.note}</p>

                {/* Tags */}
                {annotation.tags && annotation.tags.length > 0 && (
                  <div className="flex flex-wrap gap-2 mb-4">
                    {annotation.tags.map((tag) => (
                      <span
                        key={tag}
                        className="px-3 py-1 bg-[#0A0F29] rounded text-sm text-[#FFD700] border border-[#FFD700]/30"
                      >
                        #{tag}
                      </span>
                    ))}
                  </div>
                )}

                {/* Metadata */}
                {annotation.metadata && Object.keys(annotation.metadata).length > 0 && (
                  <details className="mt-4">
                    <summary className="cursor-pointer text-sm text-gray-400 hover:text-[#FFD700] font-medium">
                      📊 View Metadata
                    </summary>
                    <div className="mt-3 bg-[#0A0F29] rounded p-4">
                      <pre className="text-xs text-gray-300 overflow-x-auto">
                        {JSON.stringify(annotation.metadata, null, 2)}
                      </pre>
                    </div>
                  </details>
                )}
              </div>
            ))
          )}
        </div>
          </>
        )}
      </div>
    </div>
  );
}

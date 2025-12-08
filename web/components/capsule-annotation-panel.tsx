'use client';

import { useState } from 'react';
import { AnnotationForm } from './annotation-form';
import { AnnotationTimeline } from './annotation-timeline';
import { EventCorrelationViewer } from './event-correlation-viewer';

export function CapsuleAnnotationPanel({ capsuleId, engine }: { capsuleId: string; engine: string }) {
  const [refreshKey, setRefreshKey] = useState(0);
  const [showCorrelation, setShowCorrelation] = useState(true);

  const handleAnnotationAdded = () => {
    // Force timeline refresh
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div className="space-y-6">
      <AnnotationForm
        capsuleId={capsuleId}
        engine={engine}
        onAnnotationAdded={handleAnnotationAdded}
      />

      {/* Toggle Correlation View */}
      <div className="flex justify-end">
        <button
          onClick={() => setShowCorrelation(!showCorrelation)}
          className="text-sm text-[#FFD700] hover:text-[#FFA500] transition-colors"
        >
          {showCorrelation ? '📋 Show Timeline Only' : '🔗 Show Correlation Analysis'}
        </button>
      </div>

      {showCorrelation ? (
        <EventCorrelationViewer capsuleId={capsuleId} windowMinutes={10} />
      ) : (
        <AnnotationTimeline key={refreshKey} capsuleId={capsuleId} />
      )}
    </div>
  );
}

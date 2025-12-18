'use client';

import { useState } from 'react';
import { getCapsuleAnnotationManager } from '../lib/annotations/capsule-annotations';
import { getUnifiedEventManager } from '../lib/events/unified-event-manager';

export interface AnnotationFormProps {
  capsuleId: string;
  engine: string;
  author?: string;
  onAnnotationAdded?: () => void;
}

export function AnnotationForm({ capsuleId, engine, author = 'Council Member', onAnnotationAdded }: AnnotationFormProps) {
  const [note, setNote] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!note.trim()) return;

    setIsSubmitting(true);

    try {
      const manager = getCapsuleAnnotationManager();
      const annotation = manager.addAnnotation({
        capsuleId,
        engine,
        note: note.trim(),
        author,
      });

      // Also log to unified event manager
      const eventManager = getUnifiedEventManager();
      eventManager.addEvent({
        type: 'annotation',
        capsuleId,
        engine,
        user: author,
        role: 'council',
        content: note.trim(),
        tags: annotation.tags,
        metadata: annotation.metadata,
      });

      console.log('📋 Capsule annotation added:', annotation);

      setShowSuccess(true);
      setNote('');

      if (onAnnotationAdded) {
        onAnnotationAdded();
      }

      setTimeout(() => {
        setShowSuccess(false);
      }, 3000);
    } catch (error) {
      console.error('Failed to add annotation:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-[#1A1F3C] rounded-lg border-2 border-[#FFD700] p-4">
      <h3 className="text-lg font-bold text-[#FFD700] mb-3 flex items-center gap-2">
        📋 Add Capsule Annotation
      </h3>

      <div className="bg-[#0A0F29] rounded p-3 mb-4 text-sm">
        <p className="text-gray-400 mb-1">Annotating capsule:</p>
        <p className="text-[#FFD700] font-mono text-xs">{capsuleId}</p>
        <p className="text-white mt-2">
          <span className="font-bold">{engine}</span>
        </p>
      </div>

      <form onSubmit={handleSubmit}>
        <textarea
          value={note}
          onChange={(e) => setNote(e.target.value)}
          placeholder="Add your observation or analysis... (e.g., 'revenue dip aligned with degraded status')"
          className="w-full bg-[#0A0F29] text-white border border-[#FFD700]/30 rounded p-3 text-sm min-h-[80px] focus:border-[#FFD700] focus:outline-none resize-none"
          disabled={isSubmitting}
        />

        <div className="flex items-center justify-between mt-3">
          <span className="text-xs text-gray-500">{note.length} characters</span>

          <button
            type="submit"
            disabled={isSubmitting || !note.trim()}
            className="px-4 py-2 bg-[#FFD700] text-[#0A0F29] rounded font-bold hover:bg-[#FFC700] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? '💾 Saving...' : '📋 Add Annotation'}
          </button>
        </div>
      </form>

      {showSuccess && (
        <div className="mt-3 bg-green-900/30 border border-green-500 rounded p-3 text-sm text-green-400">
          ✅ Annotation saved successfully!
        </div>
      )}

      <div className="mt-4 pt-4 border-t border-[#FFD700]/20">
        <p className="text-xs text-gray-500">
          💡 <span className="font-bold">Tip:</span> Annotations are linked to this capsule and will be visible
          in the annotation timeline and correlation analysis.
        </p>
      </div>
    </div>
  );
}

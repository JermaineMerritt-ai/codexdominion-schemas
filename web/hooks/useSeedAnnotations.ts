'use client';

import { useEffect } from 'react';
import { getCapsuleAnnotationManager } from '@/lib/annotations/capsule-annotations';
import sampleAnnotations from '@/data/sample-capsule-annotations.json';

export function useSeedAnnotations() {
  useEffect(() => {
    if (typeof window === 'undefined') return;

    const manager = getCapsuleAnnotationManager();
    const existing = manager.getAllAnnotations();

    // Only seed if no annotations exist
    if (existing.length === 0) {
      try {
        const success = manager.importFromJSON(JSON.stringify(sampleAnnotations));
        if (success) {
          console.log('✅ Seeded', sampleAnnotations.length, 'sample capsule annotations');
        }
      } catch (error) {
        console.error('Failed to seed annotations:', error);
      }
    }
  }, []);
}

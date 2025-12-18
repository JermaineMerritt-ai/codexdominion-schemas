'use client';

import { useEffect } from 'react';
import { getUnifiedEventManager } from '../lib/events/unified-event-manager';
import sampleEvents from '../data/sample-unified-events.json';

export function useSeedUnifiedEvents() {
  useEffect(() => {
    if (typeof window === 'undefined') return;

    const manager = getUnifiedEventManager();
    const existing = manager.getAllEvents();

    // Only seed if no events exist
    if (existing.length === 0) {
      try {
        const success = manager.importFromJSON(JSON.stringify(sampleEvents));
        if (success) {
          console.log('✅ Seeded', sampleEvents.length, 'unified events');
        }
      } catch (error) {
        console.error('Failed to seed unified events:', error);
      }
    }
  }, []);
}

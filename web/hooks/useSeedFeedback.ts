'use client';

import { useEffect } from 'react';
import { getCouncilFeedbackManager } from '../lib/feedback/council-feedback';

/**
 * Seeds the feedback manager with sample council feedback data
 * Useful for development and demo purposes
 */
export function useSeedFeedback() {
  useEffect(() => {
    const manager = getCouncilFeedbackManager();

    // Check if already seeded
    const existing = manager.getFeedbackHistory();
    if (existing.length > 0) {
      console.log('✅ Feedback already seeded:', existing.length, 'items');
      return;
    }

    // Sample feedback data
    const sampleFeedback = [
      {
        id: 'feedback_1733615400000_abc123xyz',
        user: 'Council Member',
        role: 'council' as const,
        timestamp: '2025-12-07T06:20:00Z',
        message: 'This automation failure echoes last quarter\'s ritual.',
        capsuleId: 'cap_commerce_1733614740',
        engine: 'Commerce Engine',
        status: 'pending' as const,
        priority: 'high' as const,
        tags: ['historical', 'recurring-issue', 'automation', 'ritual'],
        metadata: {
          capsuleIndex: 12,
          capsuleTimestamp: '2025-12-07T05:39:00Z',
          capsuleStatus: 'degraded',
        },
      },
      {
        id: 'feedback_1733612800000_def456uvw',
        user: 'Senior Council',
        role: 'council' as const,
        timestamp: '2025-12-07T05:40:00Z',
        message: 'The Marketing Engine latency spike correlates with yesterday\'s deployment. Recommend rollback review.',
        capsuleId: 'cap_marketing_1733612740',
        engine: 'Marketing Engine',
        status: 'acknowledged' as const,
        priority: 'critical' as const,
        tags: ['engine', 'automation'],
        metadata: {
          capsuleIndex: 8,
          capsuleTimestamp: '2025-12-07T05:39:00Z',
          capsuleStatus: 'failed',
        },
      },
      {
        id: 'feedback_1733609200000_ghi789rst',
        user: 'Council Observer',
        role: 'council' as const,
        timestamp: '2025-12-07T04:40:00Z',
        message: 'Video Studio uptime has been exemplary this quarter. Commend the engineering team.',
        capsuleId: 'cap_video_1733609140',
        engine: 'Video Studio',
        status: 'resolved' as const,
        priority: 'low' as const,
        tags: [],
        metadata: {
          capsuleIndex: 3,
          capsuleTimestamp: '2025-12-07T04:39:00Z',
          capsuleStatus: 'operational',
        },
      },
      {
        id: 'feedback_1733605600000_jkl012mno',
        user: 'Council Member',
        role: 'council' as const,
        timestamp: '2025-12-07T03:40:00Z',
        message: 'Distribution Engine showing memory leak pattern similar to Q3 incident. Monitor closely.',
        capsuleId: 'cap_distribution_1733605540',
        engine: 'Distribution Engine',
        status: 'acknowledged' as const,
        priority: 'high' as const,
        tags: ['historical', 'recurring-issue', 'engine'],
        metadata: {
          capsuleIndex: 5,
          capsuleTimestamp: '2025-12-07T03:39:00Z',
          capsuleStatus: 'degraded',
        },
      },
      {
        id: 'feedback_1733602000000_pqr345stu',
        user: 'Senior Council',
        role: 'council' as const,
        timestamp: '2025-12-07T02:40:00Z',
        message: 'Avatar system responses are consistently under 200ms. Performance ritual is working.',
        capsuleId: 'cap_avatars_1733601940',
        engine: 'Avatars',
        status: 'resolved' as const,
        priority: 'low' as const,
        tags: ['ritual'],
        metadata: {
          capsuleIndex: 2,
          capsuleTimestamp: '2025-12-07T02:39:00Z',
          capsuleStatus: 'operational',
        },
      },
    ];

    // Import sample data
    const json = JSON.stringify(sampleFeedback);
    const success = manager.importFromJSON(json);

    if (success) {
      console.log('🌱 Successfully seeded feedback manager with', sampleFeedback.length, 'samples');
    } else {
      console.error('❌ Failed to seed feedback manager');
    }
  }, []);
}

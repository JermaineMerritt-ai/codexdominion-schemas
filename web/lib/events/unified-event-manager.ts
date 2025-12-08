/**
 * Unified Event Management System
 * Combines annotations, chat messages, and capsule events for contextual analysis
 */

export type EventType = 'annotation' | 'chat' | 'capsule' | 'feedback';

export interface UnifiedEvent {
  id: string;
  type: EventType;
  capsuleId?: string;
  engine?: string;
  user: string;
  role: 'sovereign' | 'council' | 'heir' | 'observer' | 'custodian';
  content: string;
  timestamp: string;
  tags?: string[];
  metadata?: Record<string, any>;
}

export interface EventCorrelation {
  capsuleId: string;
  timeWindow: string; // e.g., "2025-12-07T06:30-06:40"
  events: UnifiedEvent[];
  patterns: string[];
  summary?: string;
}

export class UnifiedEventManager {
  private events: UnifiedEvent[] = [];
  private onEventCallback?: (event: UnifiedEvent) => void;

  constructor() {
    this.loadFromStorage();
  }

  private loadFromStorage(): void {
    if (typeof window === 'undefined') return;

    const stored = localStorage.getItem('unified_events');
    if (stored) {
      try {
        this.events = JSON.parse(stored);
        console.log('📊 Loaded', this.events.length, 'unified events');
      } catch (error) {
        console.error('Failed to load unified events:', error);
      }
    }
  }

  private saveToStorage(): void {
    if (typeof window === 'undefined') return;

    try {
      localStorage.setItem('unified_events', JSON.stringify(this.events));
    } catch (error) {
      console.error('Failed to save unified events:', error);
    }
  }

  addEvent(data: {
    type: EventType;
    capsuleId?: string;
    engine?: string;
    user: string;
    role: UnifiedEvent['role'];
    content: string;
    tags?: string[];
    metadata?: Record<string, any>;
  }): UnifiedEvent {
    const event: UnifiedEvent = {
      id: `event_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      type: data.type,
      capsuleId: data.capsuleId,
      engine: data.engine,
      user: data.user,
      role: data.role,
      content: data.content,
      timestamp: new Date().toISOString(),
      tags: data.tags || this.extractTags(data.content),
      metadata: data.metadata,
    };

    this.events.unshift(event);
    this.saveToStorage();

    if (this.onEventCallback) {
      this.onEventCallback(event);
    }

    console.log('📊 Unified event added:', event);
    return event;
  }

  private extractTags(content: string): string[] {
    const tags: string[] = [];
    const lowerContent = content.toLowerCase();

    // Business impact
    if (lowerContent.includes('revenue') || lowerContent.includes('sales')) {
      tags.push('revenue-impact');
    }
    if (lowerContent.includes('performance') || lowerContent.includes('latency')) {
      tags.push('performance');
    }

    // Status
    if (lowerContent.includes('degraded') || lowerContent.includes('failing')) {
      tags.push('degraded-status');
    }
    if (lowerContent.includes('operational') || lowerContent.includes('stable')) {
      tags.push('operational');
    }

    // Analysis
    if (lowerContent.includes('aligned') || lowerContent.includes('correlate')) {
      tags.push('correlation');
    }
    if (lowerContent.includes('pattern') || lowerContent.includes('recurring')) {
      tags.push('pattern-analysis');
    }

    // Urgency
    if (lowerContent.includes('urgent') || lowerContent.includes('critical')) {
      tags.push('urgent');
    }

    return tags;
  }

  getEventsByCapsule(capsuleId: string): UnifiedEvent[] {
    return this.events.filter((e) => e.capsuleId === capsuleId);
  }

  getEventsByEngine(engine: string): UnifiedEvent[] {
    return this.events.filter((e) => e.engine === engine);
  }

  getEventsByType(type: EventType): UnifiedEvent[] {
    return this.events.filter((e) => e.type === type);
  }

  getEventsByTimeRange(startTime: string, endTime: string): UnifiedEvent[] {
    const start = new Date(startTime).getTime();
    const end = new Date(endTime).getTime();

    return this.events.filter((e) => {
      const eventTime = new Date(e.timestamp).getTime();
      return eventTime >= start && eventTime <= end;
    });
  }

  getEventsByUser(user: string): UnifiedEvent[] {
    return this.events.filter((e) => e.user === user);
  }

  getEventsByRole(role: UnifiedEvent['role']): UnifiedEvent[] {
    return this.events.filter((e) => e.role === role);
  }

  getAllEvents(): UnifiedEvent[] {
    return [...this.events];
  }

  searchEvents(query: string): UnifiedEvent[] {
    const lowerQuery = query.toLowerCase();
    return this.events.filter(
      (e) =>
        e.content.toLowerCase().includes(lowerQuery) ||
        e.engine?.toLowerCase().includes(lowerQuery) ||
        e.user.toLowerCase().includes(lowerQuery) ||
        e.tags?.some((tag) => tag.toLowerCase().includes(lowerQuery))
    );
  }

  /**
   * Find correlated events within a time window around a capsule event
   */
  correlateCapsuleEvents(capsuleId: string, windowMinutes: number = 10): EventCorrelation {
    const capsuleEvents = this.getEventsByCapsule(capsuleId);
    if (capsuleEvents.length === 0) {
      return {
        capsuleId,
        timeWindow: 'N/A',
        events: [],
        patterns: [],
      };
    }

    // Get time range
    const timestamps = capsuleEvents.map((e) => new Date(e.timestamp).getTime());
    const minTime = Math.min(...timestamps);
    const maxTime = Math.max(...timestamps);

    // Expand window by windowMinutes on each side
    const startTime = new Date(minTime - windowMinutes * 60 * 1000).toISOString();
    const endTime = new Date(maxTime + windowMinutes * 60 * 1000).toISOString();

    // Get all events in this window
    const correlatedEvents = this.getEventsByTimeRange(startTime, endTime);

    // Find patterns
    const patterns = this.detectPatterns(correlatedEvents);

    return {
      capsuleId,
      timeWindow: `${new Date(startTime).toLocaleString()} - ${new Date(endTime).toLocaleString()}`,
      events: correlatedEvents,
      patterns,
    };
  }

  private detectPatterns(events: UnifiedEvent[]): string[] {
    const patterns: string[] = [];

    // Count by type
    const typeCount = events.reduce((acc, e) => {
      acc[e.type] = (acc[e.type] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    if (typeCount.annotation && typeCount.chat) {
      patterns.push(`${typeCount.annotation} annotations and ${typeCount.chat} chat messages in same window`);
    }

    // Count by engine
    const engineCount = events.reduce((acc, e) => {
      if (e.engine) acc[e.engine] = (acc[e.engine] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    const multipleEngines = Object.keys(engineCount).length;
    if (multipleEngines > 1) {
      patterns.push(`Events span ${multipleEngines} different engines`);
    }

    // Count by role
    const roleCount = events.reduce((acc, e) => {
      acc[e.role] = (acc[e.role] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    if (roleCount.council && roleCount.sovereign) {
      patterns.push('Council and Sovereign both active in this window');
    }

    // Tag analysis
    const allTags = events.flatMap((e) => e.tags || []);
    const tagFrequency = allTags.reduce((acc, tag) => {
      acc[tag] = (acc[tag] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    const commonTags = Object.entries(tagFrequency)
      .filter(([_, count]) => count >= 2)
      .map(([tag]) => tag);

    if (commonTags.length > 0) {
      patterns.push(`Common themes: ${commonTags.join(', ')}`);
    }

    return patterns;
  }

  onEvent(callback: (event: UnifiedEvent) => void): void {
    this.onEventCallback = callback;
  }

  getStatistics() {
    const byType = this.events.reduce((acc, e) => {
      acc[e.type] = (acc[e.type] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    const byRole = this.events.reduce((acc, e) => {
      acc[e.role] = (acc[e.role] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    const byEngine = this.events.reduce((acc, e) => {
      if (e.engine) acc[e.engine] = (acc[e.engine] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    const allTags = this.events.flatMap((e) => e.tags || []);
    const tagFrequency = allTags.reduce((acc, tag) => {
      acc[tag] = (acc[tag] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    return {
      total: this.events.length,
      byType,
      byRole,
      byEngine,
      topTags: tagFrequency,
      uniqueUsers: new Set(this.events.map((e) => e.user)).size,
      uniqueCapsules: new Set(this.events.map((e) => e.capsuleId).filter(Boolean)).size,
    };
  }

  exportToJSON(): string {
    return JSON.stringify(this.events, null, 2);
  }

  importFromJSON(json: string): boolean {
    try {
      const imported = JSON.parse(json);
      if (Array.isArray(imported)) {
        this.events = imported;
        this.saveToStorage();
        return true;
      }
      return false;
    } catch (error) {
      console.error('Failed to import events:', error);
      return false;
    }
  }

  clearAll(): void {
    this.events = [];
    this.saveToStorage();
  }

  deleteEvent(id: string): boolean {
    const index = this.events.findIndex((e) => e.id === id);
    if (index !== -1) {
      this.events.splice(index, 1);
      this.saveToStorage();
      return true;
    }
    return false;
  }
}

// Singleton instance
let unifiedEventManagerInstance: UnifiedEventManager | null = null;

export function getUnifiedEventManager(): UnifiedEventManager {
  if (!unifiedEventManagerInstance) {
    unifiedEventManagerInstance = new UnifiedEventManager();
  }
  return unifiedEventManagerInstance;
}

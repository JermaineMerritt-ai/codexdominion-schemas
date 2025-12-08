/**
 * Capsule Annotation System
 * Allows council members to add contextual notes and observations to replay capsules
 */

export interface CapsuleAnnotation {
  id: string;
  capsuleId: string;
  engine: string;
  note: string;
  author: string;
  timestamp: string;
  tags?: string[];
  metadata?: {
    originalStatus?: string;
    relatedCapsules?: string[];
    impactMetrics?: Record<string, number>;
  };
}

export class CapsuleAnnotationManager {
  private annotations: CapsuleAnnotation[] = [];
  private onAnnotationCallback?: (annotation: CapsuleAnnotation) => void;

  constructor() {
    this.loadFromStorage();
  }

  private loadFromStorage(): void {
    if (typeof window === 'undefined') return;

    const stored = localStorage.getItem('capsule_annotations');
    if (stored) {
      try {
        this.annotations = JSON.parse(stored);
        console.log('📋 Loaded', this.annotations.length, 'capsule annotations');
      } catch (error) {
        console.error('Failed to load annotations:', error);
      }
    }
  }

  private saveToStorage(): void {
    if (typeof window === 'undefined') return;

    try {
      localStorage.setItem('capsule_annotations', JSON.stringify(this.annotations));
    } catch (error) {
      console.error('Failed to save annotations:', error);
    }
  }

  addAnnotation(data: {
    capsuleId: string;
    engine: string;
    note: string;
    author?: string;
    tags?: string[];
    metadata?: CapsuleAnnotation['metadata'];
  }): CapsuleAnnotation {
    const annotation: CapsuleAnnotation = {
      id: `annotation_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      capsuleId: data.capsuleId,
      engine: data.engine,
      note: data.note,
      author: data.author || 'Council Member',
      timestamp: new Date().toISOString(),
      tags: data.tags || this.extractTags(data.note),
      metadata: data.metadata,
    };

    this.annotations.unshift(annotation);
    this.saveToStorage();

    if (this.onAnnotationCallback) {
      this.onAnnotationCallback(annotation);
    }

    console.log('📝 Annotation added:', annotation);
    return annotation;
  }

  private extractTags(note: string): string[] {
    const tags: string[] = [];
    const lowerNote = note.toLowerCase();

    // Correlation tags
    if (lowerNote.includes('aligned') || lowerNote.includes('correlate') || lowerNote.includes('match')) {
      tags.push('correlation');
    }

    // Impact tags
    if (lowerNote.includes('revenue') || lowerNote.includes('sales') || lowerNote.includes('income')) {
      tags.push('revenue-impact');
    }
    if (lowerNote.includes('performance') || lowerNote.includes('latency') || lowerNote.includes('speed')) {
      tags.push('performance');
    }
    if (lowerNote.includes('uptime') || lowerNote.includes('downtime') || lowerNote.includes('availability')) {
      tags.push('availability');
    }

    // Status tags
    if (lowerNote.includes('degraded') || lowerNote.includes('failing') || lowerNote.includes('unstable')) {
      tags.push('degraded-status');
    }
    if (lowerNote.includes('recovered') || lowerNote.includes('restored') || lowerNote.includes('fixed')) {
      tags.push('recovery');
    }

    // Analysis tags
    if (lowerNote.includes('pattern') || lowerNote.includes('trend') || lowerNote.includes('recurring')) {
      tags.push('pattern-analysis');
    }

    return tags;
  }

  getAnnotationsByCapsule(capsuleId: string): CapsuleAnnotation[] {
    return this.annotations.filter((a) => a.capsuleId === capsuleId);
  }

  getAnnotationsByEngine(engine: string): CapsuleAnnotation[] {
    return this.annotations.filter((a) => a.engine === engine);
  }

  getAnnotationsByTag(tag: string): CapsuleAnnotation[] {
    return this.annotations.filter((a) => a.tags?.includes(tag));
  }

  getAllAnnotations(): CapsuleAnnotation[] {
    return [...this.annotations];
  }

  getAnnotationById(id: string): CapsuleAnnotation | undefined {
    return this.annotations.find((a) => a.id === id);
  }

  deleteAnnotation(id: string): boolean {
    const index = this.annotations.findIndex((a) => a.id === id);
    if (index !== -1) {
      this.annotations.splice(index, 1);
      this.saveToStorage();
      return true;
    }
    return false;
  }

  updateAnnotation(id: string, updates: Partial<Omit<CapsuleAnnotation, 'id' | 'timestamp'>>): boolean {
    const annotation = this.getAnnotationById(id);
    if (annotation) {
      Object.assign(annotation, updates);
      this.saveToStorage();
      return true;
    }
    return false;
  }

  onAnnotation(callback: (annotation: CapsuleAnnotation) => void): void {
    this.onAnnotationCallback = callback;
  }

  searchAnnotations(query: string): CapsuleAnnotation[] {
    const lowerQuery = query.toLowerCase();
    return this.annotations.filter(
      (a) =>
        a.note.toLowerCase().includes(lowerQuery) ||
        a.engine.toLowerCase().includes(lowerQuery) ||
        a.author.toLowerCase().includes(lowerQuery) ||
        a.tags?.some((tag) => tag.toLowerCase().includes(lowerQuery))
    );
  }

  getStatistics() {
    return {
      total: this.annotations.length,
      byEngine: this.annotations.reduce((acc, a) => {
        acc[a.engine] = (acc[a.engine] || 0) + 1;
        return acc;
      }, {} as Record<string, number>),
      byAuthor: this.annotations.reduce((acc, a) => {
        acc[a.author] = (acc[a.author] || 0) + 1;
        return acc;
      }, {} as Record<string, number>),
      topTags: this.annotations
        .flatMap((a) => a.tags || [])
        .reduce((acc, tag) => {
          acc[tag] = (acc[tag] || 0) + 1;
          return acc;
        }, {} as Record<string, number>),
    };
  }

  exportToJSON(): string {
    return JSON.stringify(this.annotations, null, 2);
  }

  importFromJSON(json: string): boolean {
    try {
      const imported = JSON.parse(json);
      if (Array.isArray(imported)) {
        this.annotations = imported;
        this.saveToStorage();
        return true;
      }
      return false;
    } catch (error) {
      console.error('Failed to import annotations:', error);
      return false;
    }
  }

  clearAll(): void {
    this.annotations = [];
    this.saveToStorage();
  }
}

// Singleton instance
let annotationManagerInstance: CapsuleAnnotationManager | null = null;

export function getCapsuleAnnotationManager(): CapsuleAnnotationManager {
  if (!annotationManagerInstance) {
    annotationManagerInstance = new CapsuleAnnotationManager();
  }
  return annotationManagerInstance;
}

/**
 * Council Feedback System
 * Allows council members to send contextual feedback during broadcasts
 */

export interface CouncilFeedback {
  user: string;
  role: 'council';
  timestamp: string;
  message: string;
  capsuleId?: string;
  engine?: string;
  metadata?: Record<string, any>;
}

export interface FeedbackMessage extends CouncilFeedback {
  id: string;
  status: 'pending' | 'acknowledged' | 'resolved';
  priority: 'low' | 'medium' | 'high' | 'critical';
  tags?: string[];
}

export class CouncilFeedbackManager {
  private feedbackHistory: FeedbackMessage[] = [];
  private onFeedbackCallback?: (feedback: FeedbackMessage) => void;

  constructor() {
    this.loadFromStorage();
  }

  private loadFromStorage(): void {
    if (typeof window === 'undefined') return;

    const stored = localStorage.getItem('council_feedback_history');
    if (stored) {
      try {
        this.feedbackHistory = JSON.parse(stored);
      } catch (error) {
        console.error('Failed to load feedback history:', error);
      }
    }
  }

  private saveToStorage(): void {
    if (typeof window === 'undefined') return;

    try {
      localStorage.setItem('council_feedback_history', JSON.stringify(this.feedbackHistory));
    } catch (error) {
      console.error('Failed to save feedback history:', error);
    }
  }

  submitFeedback(feedback: CouncilFeedback): FeedbackMessage {
    const enrichedFeedback: FeedbackMessage = {
      ...feedback,
      id: `feedback_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      status: 'pending',
      priority: this.calculatePriority(feedback),
      tags: this.extractTags(feedback.message),
    };

    this.feedbackHistory.unshift(enrichedFeedback);
    this.saveToStorage();

    if (this.onFeedbackCallback) {
      this.onFeedbackCallback(enrichedFeedback);
    }

    console.log('📝 Council feedback submitted:', enrichedFeedback);
    return enrichedFeedback;
  }

  private calculatePriority(feedback: CouncilFeedback): FeedbackMessage['priority'] {
    const message = feedback.message.toLowerCase();

    // Critical keywords
    if (message.includes('failure') || message.includes('critical') || message.includes('down')) {
      return 'critical';
    }

    // High priority keywords
    if (message.includes('error') || message.includes('issue') || message.includes('problem')) {
      return 'high';
    }

    // Medium priority keywords
    if (message.includes('concern') || message.includes('warning') || message.includes('review')) {
      return 'medium';
    }

    return 'low';
  }

  private extractTags(message: string): string[] {
    const tags: string[] = [];
    const lowerMessage = message.toLowerCase();

    // Temporal tags
    if (lowerMessage.includes('last quarter') || lowerMessage.includes('previous')) {
      tags.push('historical');
    }
    if (lowerMessage.includes('recurring') || lowerMessage.includes('echoes') || lowerMessage.includes('repeat')) {
      tags.push('recurring-issue');
    }

    // Issue type tags
    if (lowerMessage.includes('automation')) {
      tags.push('automation');
    }
    if (lowerMessage.includes('ritual')) {
      tags.push('ritual');
    }
    if (lowerMessage.includes('engine')) {
      tags.push('engine');
    }

    return tags;
  }

  getFeedbackHistory(limit?: number): FeedbackMessage[] {
    return limit ? this.feedbackHistory.slice(0, limit) : [...this.feedbackHistory];
  }

  getFeedbackById(id: string): FeedbackMessage | undefined {
    return this.feedbackHistory.find(f => f.id === id);
  }

  updateFeedbackStatus(id: string, status: FeedbackMessage['status']): boolean {
    const feedback = this.getFeedbackById(id);
    if (feedback) {
      feedback.status = status;
      this.saveToStorage();
      return true;
    }
    return false;
  }

  onFeedback(callback: (feedback: FeedbackMessage) => void): void {
    this.onFeedbackCallback = callback;
  }

  clearHistory(): void {
    this.feedbackHistory = [];
    this.saveToStorage();
  }

  exportToJSON(): string {
    return JSON.stringify(this.feedbackHistory, null, 2);
  }

  importFromJSON(json: string): boolean {
    try {
      const imported = JSON.parse(json);
      if (Array.isArray(imported)) {
        this.feedbackHistory = imported;
        this.saveToStorage();
        return true;
      }
      return false;
    } catch (error) {
      console.error('Failed to import feedback:', error);
      return false;
    }
  }
}

// Singleton instance
let feedbackManagerInstance: CouncilFeedbackManager | null = null;

export function getCouncilFeedbackManager(): CouncilFeedbackManager {
  if (!feedbackManagerInstance) {
    feedbackManagerInstance = new CouncilFeedbackManager();
  }
  return feedbackManagerInstance;
}

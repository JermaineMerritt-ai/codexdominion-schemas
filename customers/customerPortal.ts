/**
 * 👥 Customer Portal - External Customer Interface
 * 
 * Main entry point for external customers to interact with Codex Dominion system.
 * Routes customer requests to appropriate agents and sovereigns.
 */

import { Customer, Message } from '../packages/shared-types/src';
import { healthcareAgent } from '../agents/healthcare';
import { legalAgent } from '../agents/legal';
import { commerceAgent } from '../agents/commerce';
import { cybersecurityAgent } from '../agents/cybersecurity';

export class CustomerPortal {
  private customers: Map<string, Customer> = new Map();
  private sessions: Map<string, { customerId: string; startTime: Date; active: boolean }> = new Map();

  /**
   * Register a new customer
   */
  async registerCustomer(data: {
    email: string;
    name: string;
    company?: string;
  }): Promise<{ success: boolean; customerId?: string; message: string }> {
    const customerId = `cust-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    const customer: Customer = {
      id: customerId,
      email: data.email,
      name: data.name,
      company: data.company,
      tier: 'BASIC',
      status: 'ACTIVE',
      createdAt: new Date(),
      preferences: {
        notifications: true,
        dataSharing: false,
        theme: 'dark'
      },
      usage: {
        requestsThisMonth: 0,
        lastActive: new Date(),
        totalSpent: 0
      }
    };

    this.customers.set(customerId, customer);

    return {
      success: true,
      customerId,
      message: 'Customer registered successfully'
    };
  }

  /**
   * Start a customer session
   */
  async startSession(customerId: string): Promise<{ sessionId: string; message: string }> {
    const customer = this.customers.get(customerId);

    if (!customer) {
      throw new Error('Customer not found');
    }

    if (customer.status !== 'ACTIVE') {
      throw new Error('Customer account is not active');
    }

    const sessionId = `session-${Date.now()}`;
    this.sessions.set(sessionId, {
      customerId,
      startTime: new Date(),
      active: true
    });

    // Update customer usage
    customer.usage.lastActive = new Date();
    this.customers.set(customerId, customer);

    return {
      sessionId,
      message: 'Welcome to Codex Dominion! How can we help you today?'
    };
  }

  /**
   * Route customer message to appropriate agent
   */
  async processCustomerMessage(sessionId: string, message: string): Promise<{
    response: string;
    agent: string;
    actions?: string[];
  }> {
    const session = this.sessions.get(sessionId);

    if (!session || !session.active) {
      throw new Error('Invalid or expired session');
    }

    const customer = this.customers.get(session.customerId);
    if (!customer) {
      throw new Error('Customer not found');
    }

    // Update usage
    customer.usage.requestsThisMonth++;
    this.customers.set(customer.id, customer);

    // Route to appropriate agent based on message content
    const lowerMessage = message.toLowerCase();

    if (lowerMessage.includes('health') || lowerMessage.includes('medical') || lowerMessage.includes('appointment')) {
      const result = await healthcareAgent.processPatientQuery(message, customer.id);
      return {
        response: result.response,
        agent: 'healthcare',
        actions: result.action ? [result.action] : []
      };
    }

    if (lowerMessage.includes('legal') || lowerMessage.includes('contract') || lowerMessage.includes('compliance')) {
      return {
        response: 'I\'m connecting you with our legal compliance agent. How can I assist with legal matters?',
        agent: 'legal'
      };
    }

    if (lowerMessage.includes('product') || lowerMessage.includes('buy') || lowerMessage.includes('price')) {
      const recommendations = await commerceAgent.getProductRecommendations(customer.id);
      return {
        response: `I can help you with our products! Based on your interests, I recommend: ${recommendations.recommendations.map(r => r.name).join(', ')}`,
        agent: 'commerce'
      };
    }

    if (lowerMessage.includes('security') || lowerMessage.includes('threat') || lowerMessage.includes('vulnerability')) {
      return {
        response: 'I\'m connecting you with our cybersecurity agent. What security concerns can I help address?',
        agent: 'cybersecurity'
      };
    }

    // Default response
    return {
      response: 'Thank you for your message. Let me connect you with the right specialist. Could you provide more details about your request?',
      agent: 'general'
    };
  }

  /**
   * Get customer information
   */
  getCustomer(customerId: string): Customer | undefined {
    return this.customers.get(customerId);
  }

  /**
   * Update customer tier
   */
  upgradeTier(customerId: string, newTier: 'BASIC' | 'PREMIUM' | 'ENTERPRISE'): {
    success: boolean;
    message: string;
  } {
    const customer = this.customers.get(customerId);

    if (!customer) {
      return { success: false, message: 'Customer not found' };
    }

    customer.tier = newTier;
    this.customers.set(customerId, customer);

    return {
      success: true,
      message: `Customer upgraded to ${newTier} tier`
    };
  }

  /**
   * End customer session
   */
  endSession(sessionId: string): void {
    const session = this.sessions.get(sessionId);
    if (session) {
      session.active = false;
      this.sessions.set(sessionId, session);
    }
  }

  /**
   * Get customer usage statistics
   */
  getUsageStats(customerId: string): {
    requestsThisMonth: number;
    lastActive: Date;
    totalSpent: number;
    tier: string;
  } | null {
    const customer = this.customers.get(customerId);
    if (!customer) return null;

    return {
      requestsThisMonth: customer.usage.requestsThisMonth,
      lastActive: customer.usage.lastActive,
      totalSpent: customer.usage.totalSpent,
      tier: customer.tier
    };
  }

  /**
   * Get portal statistics
   */
  getPortalStats(): {
    totalCustomers: number;
    activeCustomers: number;
    activeSessions: number;
    tierDistribution: Record<string, number>;
  } {
    const customers = Array.from(this.customers.values());
    const activeSessions = Array.from(this.sessions.values()).filter(s => s.active);

    const tierDistribution = customers.reduce((acc, customer) => {
      acc[customer.tier] = (acc[customer.tier] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    return {
      totalCustomers: customers.length,
      activeCustomers: customers.filter(c => c.status === 'ACTIVE').length,
      activeSessions: activeSessions.length,
      tierDistribution
    };
  }
}

// Export singleton instance
export const customerPortal = new CustomerPortal();

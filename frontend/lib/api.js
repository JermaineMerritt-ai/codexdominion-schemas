// lib/api.js
/**
 * API client for Codex Dominion FastAPI backend
 * Connects Next.js frontend to the Ledger API (port 8001)
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8001';

class ApiClient {
  constructor(baseUrl = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      throw error;
    }
  }

  // Health check
  async getHealth() {
    return this.request('/health');
  }

  // System statistics
  async getStats() {
    return this.request('/stats');
  }

  // Ledger endpoints
  async getLedger(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const endpoint = queryString ? `/ledger?${queryString}` : '/ledger';
    return this.request(endpoint);
  }

  async createLedgerEntry(entry) {
    return this.request('/ledger', {
      method: 'POST',
      body: JSON.stringify(entry),
    });
  }

  // Treasury endpoints
  async getTreasury(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const endpoint = queryString ? `/treasury?${queryString}` : '/treasury';
    return this.request(endpoint);
  }

  async createTreasuryTransaction(transaction) {
    return this.request('/treasury', {
      method: 'POST',
      body: JSON.stringify(transaction),
    });
  }

  // Signals endpoints
  async getSignals(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const endpoint = queryString ? `/signals?${queryString}` : '/signals';
    return this.request(endpoint);
  }

  async createSignal(signal) {
    return this.request('/signals', {
      method: 'POST',
      body: JSON.stringify(signal),
    });
  }

  // Pools endpoints
  async getPools(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const endpoint = queryString ? `/pools?${queryString}` : '/pools';
    return this.request(endpoint);
  }

  async createPool(pool) {
    return this.request('/pools', {
      method: 'POST',
      body: JSON.stringify(pool),
    });
  }

  // Utility methods
  async checkConnection() {
    try {
      const health = await this.getHealth();
      return health.status === 'healthy';
    } catch {
      return false;
    }
  }
}

// Create and export the API client instance
export const apiClient = new ApiClient();

// Export individual methods for convenience
export const {
  getHealth,
  getStats,
  getLedger,
  createLedgerEntry,
  getTreasury,
  createTreasuryTransaction,
  getSignals,
  createSignal,
  getPools,
  createPool,
  checkConnection,
} = apiClient;

// Export API client class for custom instances
export { ApiClient };
/**
 * 👑 SOVEREIGN API CLIENT 🏛️
 * Frontend API client for CodexDominion Sovereign System
 * The Merritt Method™
 */

import {
  Crown,
  Scroll,
  Hymn,
  Capsule,
  LedgerEntry,
  EternalArchive,
  ForgeCrownRequest,
  UnfurlScrollRequest,
  ComposeHymnRequest,
  SealCapsuleRequest,
  InscribeLedgerRequest,
  EnshrineArchiveRequest,
  ApiResponse,
  SovereignMetrics,
} from '../types/sovereign';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000/api';

/**
 * Base API client class
 */
class SovereignApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Make API request
   */
  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
        ...options,
      });

      const data = await response.json();

      if (!response.ok) {
        return {
          success: false,
          error: data.error || 'Request failed',
        };
      }

      return {
        success: true,
        data,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  }

  // ==========================================================================
  // CROWNS API 👑
  // ==========================================================================

  /**
   * ⚔️ Forge a new Crown (Create Product)
   */
  async forgeCrown(request: ForgeCrownRequest): Promise<ApiResponse<Crown>> {
    return this.request<Crown>('/crowns', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * 📋 List all Crowns
   */
  async listCrowns(): Promise<ApiResponse<Crown[]>> {
    return this.request<Crown[]>('/crowns');
  }

  /**
   * 🔍 Get Crown by ID
   */
  async getCrown(id: string): Promise<ApiResponse<Crown>> {
    return this.request<Crown>(`/crowns/${id}`);
  }

  /**
   * ✏️ Update Crown
   */
  async updateCrown(id: string, updates: Partial<Crown>): Promise<ApiResponse<Crown>> {
    return this.request<Crown>(`/crowns/${id}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  }

  /**
   * 🗑️ Delete Crown
   */
  async deleteCrown(id: string): Promise<ApiResponse<void>> {
    return this.request<void>(`/crowns/${id}`, {
      method: 'DELETE',
    });
  }

  // ==========================================================================
  // SCROLLS API 📜
  // ==========================================================================

  /**
   * 📜 Unfurl a new Scroll (Launch Campaign)
   */
  async unfurlScroll(request: UnfurlScrollRequest): Promise<ApiResponse<Scroll>> {
    return this.request<Scroll>('/scrolls', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * 📋 List all Scrolls
   */
  async listScrolls(activeOnly: boolean = false): Promise<ApiResponse<Scroll[]>> {
    const query = activeOnly ? '?active=true' : '';
    return this.request<Scroll[]>(`/scrolls${query}`);
  }

  /**
   * 🔍 Get Scroll by ID
   */
  async getScroll(id: string): Promise<ApiResponse<Scroll>> {
    return this.request<Scroll>(`/scrolls/${id}`);
  }

  /**
   * ✏️ Update Scroll
   */
  async updateScroll(id: string, updates: Partial<Scroll>): Promise<ApiResponse<Scroll>> {
    return this.request<Scroll>(`/scrolls/${id}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  }

  /**
   * 🚫 Deactivate Scroll
   */
  async deactivateScroll(id: string): Promise<ApiResponse<Scroll>> {
    return this.request<Scroll>(`/scrolls/${id}/deactivate`, {
      method: 'POST',
    });
  }

  // ==========================================================================
  // HYMNS API 🎵
  // ==========================================================================

  /**
   * 🎵 Compose a new Hymn (Create Broadcast Cycle)
   */
  async composeHymn(request: ComposeHymnRequest): Promise<ApiResponse<Hymn>> {
    return this.request<Hymn>('/hymns', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * 📋 List all Hymns
   */
  async listHymns(): Promise<ApiResponse<Hymn[]>> {
    return this.request<Hymn[]>('/hymns');
  }

  /**
   * 🔍 Get Hymn by ID
   */
  async getHymn(id: string): Promise<ApiResponse<Hymn>> {
    return this.request<Hymn>(`/hymns/${id}`);
  }

  /**
   * 📡 Broadcast a Hymn
   */
  async broadcastHymn(id: string): Promise<ApiResponse<{ capsules_created: number }>> {
    return this.request<{ capsules_created: number }>(`/hymns/${id}/broadcast`, {
      method: 'POST',
    });
  }

  /**
   * ⏸️ Pause/Resume Hymn
   */
  async toggleHymn(id: string, active: boolean): Promise<ApiResponse<Hymn>> {
    return this.request<Hymn>(`/hymns/${id}/toggle`, {
      method: 'POST',
      body: JSON.stringify({ active }),
    });
  }

  // ==========================================================================
  // CAPSULES API 📦
  // ==========================================================================

  /**
   * 📦 Seal a new Capsule (Create Content Unit)
   */
  async sealCapsule(request: SealCapsuleRequest): Promise<ApiResponse<Capsule>> {
    return this.request<Capsule>('/capsules', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * 📋 List all Capsules
   */
  async listCapsules(hymnId?: string): Promise<ApiResponse<Capsule[]>> {
    const query = hymnId ? `?hymn_id=${hymnId}` : '';
    return this.request<Capsule[]>(`/capsules${query}`);
  }

  /**
   * 🔍 Get Capsule by ID
   */
  async getCapsule(id: string): Promise<ApiResponse<Capsule>> {
    return this.request<Capsule>(`/capsules/${id}`);
  }

  /**
   * 📊 Update Capsule performance metrics
   */
  async updateCapsuleMetrics(
    id: string,
    metrics: Partial<Capsule['performance']>
  ): Promise<ApiResponse<Capsule>> {
    return this.request<Capsule>(`/capsules/${id}/metrics`, {
      method: 'POST',
      body: JSON.stringify(metrics),
    });
  }

  // ==========================================================================
  // LEDGERS API 📊
  // ==========================================================================

  /**
   * 📊 Inscribe Ledger Entry (Record Transaction)
   */
  async inscribeLedger(request: InscribeLedgerRequest): Promise<ApiResponse<LedgerEntry>> {
    return this.request<LedgerEntry>('/ledgers', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * 📋 Inspect Ledgers (List entries)
   */
  async inspectLedgers(filters?: {
    ledger_type?: string;
    start_date?: string;
    end_date?: string;
  }): Promise<ApiResponse<LedgerEntry[]>> {
    const params = new URLSearchParams();
    if (filters?.ledger_type) params.append('ledger_type', filters.ledger_type);
    if (filters?.start_date) params.append('start_date', filters.start_date);
    if (filters?.end_date) params.append('end_date', filters.end_date);

    const query = params.toString() ? `?${params.toString()}` : '';
    return this.request<LedgerEntry[]>(`/ledgers${query}`);
  }

  /**
   * 📊 Get Ledger summary
   */
  async getLedgerSummary(): Promise<
    ApiResponse<{
      total_revenue: number;
      total_orders: number;
      average_order_value: number;
    }>
  > {
    return this.request('/ledgers/summary');
  }

  // ==========================================================================
  // ETERNAL ARCHIVE API 🏛️
  // ==========================================================================

  /**
   * 🏛️ Enshrine in Eternal Archive (Create Archive)
   */
  async enshrineArchive(request: EnshrineArchiveRequest): Promise<ApiResponse<EternalArchive>> {
    return this.request<EternalArchive>('/archives', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * 📋 List all Archives
   */
  async listArchives(): Promise<ApiResponse<EternalArchive[]>> {
    return this.request<EternalArchive[]>('/archives');
  }

  /**
   * 🔍 Get Archive by ID
   */
  async getArchive(id: string): Promise<ApiResponse<EternalArchive>> {
    return this.request<EternalArchive>(`/archives/${id}`);
  }

  /**
   * 📥 Download Archive
   */
  async downloadArchive(id: string): Promise<string> {
    return `${this.baseUrl}/archives/${id}/download`;
  }

  // ==========================================================================
  // DASHBOARD METRICS API 📊
  // ==========================================================================

  /**
   * 📊 Get overall metrics
   */
  async getMetrics(): Promise<ApiResponse<SovereignMetrics>> {
    return this.request<SovereignMetrics>('/metrics');
  }
}

// Export singleton instance
export const sovereignApi = new SovereignApiClient();

// Export class for custom instances
export default SovereignApiClient;

/**
 * CodexDominion API Client
 * Type-safe wrapper for backend REST API
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000/api/v1';

export interface ApiError {
  message: string;
  statusCode: number;
  error?: string;
}

class ApiClient {
  private baseURL: string;
  private accessToken: string | null = null;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  setAccessToken(token: string | null) {
    this.accessToken = token;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    }

    const url = `${this.baseURL}${endpoint}`;

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      if (!response.ok) {
        const error: ApiError = await response.json().catch(() => ({
          message: `HTTP ${response.status}: ${response.statusText}`,
          statusCode: response.status,
        }));
        throw error;
      }

      // Handle 204 No Content
      if (response.status === 204) {
        return {} as T;
      }

      return await response.json();
    } catch (error) {
      if ((error as ApiError).statusCode) {
        throw error;
      }
      throw {
        message: 'Network error - please check your connection',
        statusCode: 0,
      } as ApiError;
    }
  }

  // Auth
  async login(email: string, password: string) {
    return this.request<{
      user: any;
      accessToken: string;
      refreshToken: string;
    }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async refreshToken(refreshToken: string) {
    return this.request<{ accessToken: string; refreshToken?: string }>(
      '/auth/refresh',
      {
        method: 'POST',
        body: JSON.stringify({ refreshToken }),
      }
    );
  }

  // Health
  async getHealth() {
    return this.request<{ status: string; message: string; timestamp: string }>(
      '/health'
    );
  }

  // Missions
  async getCurrentMission() {
    return this.request<any>('/missions/current');
  }

  async getMissions(params?: { season_id?: string; month?: number }) {
    const query = params
      ? '?' + new URLSearchParams(params as any).toString()
      : '';
    return this.request<any[]>(`/missions${query}`);
  }

  async submitMission(missionId: string, data: any) {
    return this.request<any>(`/missions/${missionId}/submit`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Circles
  async getCircles() {
    return this.request<any[]>('/circles');
  }

  async getCircle(id: string) {
    return this.request<any>(`/circles/${id}`);
  }

  async recordAttendance(
    circleId: string,
    sessionId: string,
    data: { user_id: string; status: string } | { records: any[] }
  ) {
    return this.request<any>(
      `/circles/${circleId}/sessions/${sessionId}/attendance`,
      {
        method: 'POST',
        body: JSON.stringify(data),
      }
    );
  }

  // Culture
  async getCurrentStory() {
    return this.request<any>('/culture/story/current');
  }

  async getStories(seasonId?: string) {
    const query = seasonId ? `?season_id=${seasonId}` : '';
    return this.request<any[]>(`/culture/stories${query}`);
  }

  // Analytics
  async getAnalyticsDashboard() {
    return this.request<any>('/analytics/dashboard');
  }

  async getAnalyticsOverview() {
    return this.request<any>('/analytics/overview');
  }

  async getCircleAnalytics(circleId?: string) {
    const query = circleId ? `?circle_id=${circleId}` : '';
    return this.request<any>(`/analytics/circles${query}`);
  }

  async getMissionAnalytics(seasonId?: string) {
    const query = seasonId ? `?season_id=${seasonId}` : '';
    return this.request<any>(`/analytics/missions${query}`);
  }

  // Creators
  async getArtifacts(creatorId?: string) {
    const query = creatorId ? `?creator_id=${creatorId}` : '';
    return this.request<any[]>(`/creators/artifacts${query}`);
  }

  async createArtifact(data: any) {
    return this.request<any>('/creators/artifacts', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getChallenges(seasonId?: string) {
    const query = seasonId ? `?season_id=${seasonId}` : '';
    return this.request<any[]>(`/creators/challenges${query}`);
  }

  async submitChallenge(data: any) {
    return this.request<any>('/creators/submissions', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Regions & Expansion
  async getRegions() {
    return this.request<any[]>('/regions');
  }

  async getSchools(regionId?: string) {
    const query = regionId ? `?region_id=${regionId}` : '';
    return this.request<any[]>(`/schools${query}`);
  }

  async createSchool(data: any) {
    return this.request<any>('/schools', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Seasons
  async getCurrentSeason() {
    return this.request<any>('/seasons/current');
  }

  async getSeasons() {
    return this.request<any[]>('/seasons');
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
export default apiClient;

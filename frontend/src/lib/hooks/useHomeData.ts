// Custom React hooks for Home screen API calls
import { useState, useEffect } from 'react';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000/api/v1';

// Helper function to make authenticated API calls
async function fetchWithAuth(endpoint: string, token?: string) {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, { headers });
  
  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }
  
  return response.json();
}

// Hook: Get current user info
export function useCurrentUser(token?: string) {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    fetchWithAuth('/users/me', token)
      .then(setUser)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [token]);

  return { user, loading, error };
}

// Hook: Get user profile
export function useUserProfile(token?: string) {
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    fetchWithAuth('/profiles/me', token)
      .then(setProfile)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [token]);

  return { profile, loading, error };
}

// Hook: Get current season
export function useCurrentSeason() {
  const [season, setSeason] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchWithAuth('/seasons/current')
      .then(setSeason)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return { season, loading, error };
}

// Hook: Get current cultural story
export function useCurrentStory(token?: string) {
  const [story, setStory] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    fetchWithAuth('/culture/story/current', token)
      .then(setStory)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [token]);

  return { story, loading, error };
}

// Hook: Get current mission
export function useCurrentMission(token?: string) {
  const [mission, setMission] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    fetchWithAuth('/missions/current', token)
      .then(setMission)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [token]);

  return { mission, loading, error };
}

// Hook: Get current curriculum modules
export function useCurrentCurriculum(token?: string) {
  const [modules, setModules] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    fetchWithAuth('/curriculum/modules/current', token)
      .then(setModules)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [token]);

  return { modules, loading, error };
}

// Hook: Get user's circles
export function useUserCircles(token?: string) {
  const [circles, setCircles] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    fetchWithAuth('/circles', token)
      .then(setCircles)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [token]);

  return { circles, loading, error };
}

// Hook: Get analytics overview (admin only)
export function useAnalyticsOverview(token?: string) {
  const [analytics, setAnalytics] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    fetchWithAuth('/analytics/overview', token)
      .then(setAnalytics)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [token]);

  return { analytics, loading, error };
}

/**
 * Authentication Context for CodexDominion
 * Manages user auth state, JWT tokens, and identity-aware routing
 */

'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { apiClient } from '../api/client';

export type UserRole =
  | 'ADMIN'
  | 'COUNCIL'
  | 'AMBASSADOR'
  | 'REGIONAL_DIRECTOR'
  | 'YOUTH_CAPTAIN'
  | 'CREATOR'
  | 'EDUCATOR'
  | 'YOUTH';

export type Identity = 'YOUTH' | 'CREATOR' | 'DIASPORA' | 'LEGACY_BUILDER' | 'ADMIN';

export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  roles: { name: UserRole }[];
  profile?: {
    identity?: Identity;
    risePath?: string;
    culturalIdentity?: string;
    regionId?: string;
  };
}

interface AuthContextType {
  user: User | null;
  accessToken: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  identity: Identity;
  primaryRole: UserRole | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  hasRole: (role: UserRole) => boolean;
  hasAnyRole: (roles: UserRole[]) => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const ACCESS_TOKEN_KEY = 'codex_access_token';
const REFRESH_TOKEN_KEY = 'codex_refresh_token';
const USER_KEY = 'codex_user';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Load auth state from localStorage on mount
  useEffect(() => {
    const storedToken = localStorage.getItem(ACCESS_TOKEN_KEY);
    const storedUser = localStorage.getItem(USER_KEY);

    if (storedToken && storedUser) {
      try {
        const parsedUser = JSON.parse(storedUser);
        setUser(parsedUser);
        setAccessToken(storedToken);
        apiClient.setAccessToken(storedToken);
      } catch (error) {
        console.error('Failed to restore auth state:', error);
        localStorage.removeItem(ACCESS_TOKEN_KEY);
        localStorage.removeItem(REFRESH_TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
      }
    }

    setIsLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await apiClient.login(email, password);

      setUser(response.user);
      setAccessToken(response.accessToken);
      apiClient.setAccessToken(response.accessToken);

      localStorage.setItem(ACCESS_TOKEN_KEY, response.accessToken);
      localStorage.setItem(REFRESH_TOKEN_KEY, response.refreshToken);
      localStorage.setItem(USER_KEY, JSON.stringify(response.user));
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const logout = () => {
    setUser(null);
    setAccessToken(null);
    apiClient.setAccessToken(null);

    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  };

  const hasRole = (role: UserRole): boolean => {
    if (!user) return false;
    return user.roles.some((r) => r.name === role);
  };

  const hasAnyRole = (roles: UserRole[]): boolean => {
    if (!user) return false;
    return user.roles.some((r) => roles.includes(r.name));
  };

  // Determine primary identity from user roles
  const determineIdentity = (): Identity => {
    if (!user) return 'YOUTH';

    if (hasRole('ADMIN') || hasRole('COUNCIL')) return 'ADMIN';
    if (hasRole('AMBASSADOR') || hasRole('REGIONAL_DIRECTOR')) return 'LEGACY_BUILDER';
    if (hasRole('CREATOR')) return 'CREATOR';
    if (hasRole('YOUTH')) return 'YOUTH';

    return user.profile?.identity || 'YOUTH';
  };

  // Determine primary role (highest privilege)
  const determinePrimaryRole = (): UserRole | null => {
    if (!user || user.roles.length === 0) return null;

    const roleHierarchy: UserRole[] = [
      'ADMIN',
      'COUNCIL',
      'AMBASSADOR',
      'REGIONAL_DIRECTOR',
      'YOUTH_CAPTAIN',
      'EDUCATOR',
      'CREATOR',
      'YOUTH',
    ];

    for (const role of roleHierarchy) {
      if (hasRole(role)) return role;
    }

    return user.roles[0].name;
  };

  const identity = determineIdentity();
  const primaryRole = determinePrimaryRole();

  const value: AuthContextType = {
    user,
    accessToken,
    isLoading,
    isAuthenticated: !!user && !!accessToken,
    identity,
    primaryRole,
    login,
    logout,
    hasRole,
    hasAnyRole,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

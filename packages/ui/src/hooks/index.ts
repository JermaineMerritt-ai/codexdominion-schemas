// Hook exports

export function useTheme() {
  return { theme: 'dark' };
}

export function useAuth() {
  return { user: null, isAuthenticated: false };
}

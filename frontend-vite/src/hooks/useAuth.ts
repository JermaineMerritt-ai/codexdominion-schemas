import { useState, useEffect } from 'react'

interface ClientPrincipal {
  identityProvider: string
  userId: string
  userDetails: string
  userRoles: string[]
  claims: Array<{
    typ: string
    val: string
  }>
}

interface AuthState {
  user: ClientPrincipal | null
  loading: boolean
}

export function useAuth() {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    loading: true
  })

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await fetch('/.auth/me')
        const data = await response.json()
        setAuthState({
          user: data.clientPrincipal || null,
          loading: false
        })
      } catch (error) {
        console.error('Failed to fetch user:', error)
        setAuthState({ user: null, loading: false })
      }
    }

    fetchUser()
  }, [])

  const login = (provider: 'twitter' | 'github' | 'aad' = 'twitter') => {
    window.location.href = `/.auth/login/${provider}`
  }

  const logout = () => {
    window.location.href = '/.auth/logout'
  }

  return {
    user: authState.user,
    loading: authState.loading,
    isAuthenticated: !!authState.user,
    login,
    logout
  }
}

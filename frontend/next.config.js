/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  
  // API configuration
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8001',
    NEXT_PUBLIC_APP_NAME: 'Codex Dominion',
    NEXT_PUBLIC_APP_VERSION: '2.0.0',
    NEXT_PUBLIC_EMPIRE_STATUS: 'Operational',
    NEXT_PUBLIC_SOVEREIGNTY_LEVEL: 'Maximum'
  },

  // Headers for CORS and security
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Credentials', value: 'true' },
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,OPTIONS,PATCH,DELETE,POST,PUT' },
          { key: 'Access-Control-Allow-Headers', value: 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version' },
        ]
      }
    ]
  },

  // Rewrites for API proxy (optional - for production)
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8001'}/:path*`
      }
    ]
  },

  // Image optimization
  images: {
    domains: ['localhost', '127.0.0.1'],
    unoptimized: true
  },

  // Build output
  output: 'standalone',
  
  // Performance optimizations
  experimental: {
    optimizeCss: false,
    optimizePackageImports: ['react', 'react-dom']
  },

  // Webpack configuration
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // Custom webpack configuration if needed
    return config
  },

  // TypeScript configuration (if using TypeScript)
  typescript: {
    ignoreBuildErrors: false,
  },

  // ESLint configuration
  eslint: {
    ignoreDuringBuilds: false,
  },
}

module.exports = nextConfig
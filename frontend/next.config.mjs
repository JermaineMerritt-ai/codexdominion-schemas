/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  poweredByHeader: false,
  
  images: {
    unoptimized: true,
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost',
      },
      {
        protocol: 'http',
        hostname: '127.0.0.1',
      },
    ],
  },
  
  typescript: {
    ignoreBuildErrors: true,
  },

  // API configuration
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8080/api/v1',
    NEXT_PUBLIC_APP_NAME: 'Codex Dominion',
    NEXT_PUBLIC_APP_VERSION: '2.0.0',
    NEXT_PUBLIC_EMPIRE_STATUS: 'Operational',
    NEXT_PUBLIC_SOVEREIGNTY_LEVEL: 'Maximum',
  },

  // Compiler optimizations
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production' ? { exclude: ['error', 'warn'] } : false,
  },
};

export default nextConfig;

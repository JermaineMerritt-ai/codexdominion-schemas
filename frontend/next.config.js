/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  poweredByHeader: false,
  trailingSlash: true,
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
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL ||
      (process.env.NODE_ENV === 'production'
        ? 'https://codex-backend-app.azurewebsites.net'
        : 'http://localhost:4000'),
    NEXT_PUBLIC_APP_NAME: 'Codex Dominion',
    NEXT_PUBLIC_APP_VERSION: '2.0.0',
    NEXT_PUBLIC_EMPIRE_STATUS: 'Operational',
    NEXT_PUBLIC_SOVEREIGNTY_LEVEL: 'Maximum',
  },

  // SWC minification
  swcMinify: true,

  // Compiler optimizations
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production' ? { exclude: ['error', 'warn'] } : false,
  },
};

module.exports = nextConfig;

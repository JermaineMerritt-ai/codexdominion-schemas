/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  poweredByHeader: false,
  output: 'export',  // Enable static HTML export
  trailingSlash: true,  // Required for Azure Static Web Apps
  images: {
    unoptimized: true
  },
  eslint: {
    ignoreDuringBuilds: true,  // Disable ESLint during production builds
  },
  typescript: {
    ignoreBuildErrors: false,  // Keep TypeScript checking enabled
  },

  // API configuration
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL ||
      (process.env.NODE_ENV === 'production'
        ? 'https://codex-backend-app.azurewebsites.net'
        : 'http://127.0.0.1:8001'),
    NEXT_PUBLIC_APP_NAME: 'Codex Dominion',
    NEXT_PUBLIC_APP_VERSION: '2.0.0',
    NEXT_PUBLIC_EMPIRE_STATUS: 'Operational',
    NEXT_PUBLIC_SOVEREIGNTY_LEVEL: 'Maximum',
  },

  // Headers for CORS and security
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Credentials', value: 'true' },
          { key: 'Access-Control-Allow-Origin', value: '*' },
          {
            key: 'Access-Control-Allow-Methods',
            value: 'GET,OPTIONS,PATCH,DELETE,POST,PUT',
          },
          {
            key: 'Access-Control-Allow-Headers',
            value:
              'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version',
          },
        ],
      },
    ];
  },

  // Rewrites for API proxy (optional - for production)
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8001'}/:path*`,
      },
    ];
  },

  // Image optimization
  images: {
    domains: ['localhost', '127.0.0.1'],
    unoptimized: true,
  },

  // Build output - use 'standalone' for production deployment
  // This creates a minimal Node.js server that can serve dynamic pages
  output: 'standalone',

  // Performance optimizations
  experimental: {
    optimizePackageImports: ['react', 'react-dom', 'lucide-react', 'framer-motion'],
  },

  // SWC minification (faster than Terser)
  swcMinify: true,

  // Compiler optimizations
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production' ? { exclude: ['error', 'warn'] } : false,
  },

  // Ensure proper base path for production
  basePath: '',
  assetPrefix: '',

  // Webpack configuration
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // Add WebpackManifestPlugin for manifest.json generation
    const { WebpackManifestPlugin } = require('webpack-manifest-plugin');
    config.plugins = config.plugins || [];
    config.plugins.push(
      new WebpackManifestPlugin({
        fileName: 'manifest.json',
        publicPath: '/assets/',
      })
    );

    // Ensure React is properly externalized for server-side rendering
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
      };
    }

    return config;
  },

  // TypeScript configuration (if using TypeScript)
  typescript: {
    ignoreBuildErrors: false,
  },

  // ESLint configuration
  eslint: {
    ignoreDuringBuilds: false,
  },
};

module.exports = nextConfig;

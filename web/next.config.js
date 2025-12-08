/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  output: 'standalone', // For Docker production builds

  // Image optimization
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    domains: [
      'localhost',
      'codexdominion.app',
      'api.codexdominion.app',
      'codexdominion.azurewebsites.net',
      'codexdominion-api.azurewebsites.net',
      process.env.NEXT_PUBLIC_WP_URL?.replace('http://', '').replace('https://', '')
    ].filter(Boolean),
    minimumCacheTTL: 60,
  },

  // Performance optimizations
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },

  // Experimental features
  experimental: {
    // optimizeCss: true, // Disabled - requires critters package
    scrollRestoration: true,
  },

  // ISR and caching
  async headers() {
    return [
      {
        source: '/:all*(svg|jpg|jpeg|png|webp|avif|gif|ico)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/fonts/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ];
  },

  // Redirects for SEO
  async redirects() {
    return [
      {
        source: '/products/:slug',
        destination: '/shop/:slug',
        permanent: true,
      },
    ];
  },

  // Environment variables
  env: {
    NEXT_PUBLIC_SITE_URL: process.env.NEXT_PUBLIC_SITE_URL,
    NEXT_PUBLIC_WP_URL: process.env.NEXT_PUBLIC_WP_URL,
    NEXT_PUBLIC_GA_ID: process.env.NEXT_PUBLIC_GA_ID,
  },

  // Bundle analyzer
  ...(process.env.ANALYZE === 'true' && {
    webpack: (config) => {
      const { BundleAnalyzerPlugin } = require('@next/bundle-analyzer')();
      config.plugins.push(new BundleAnalyzerPlugin());
      return config;
    },
  }),
};

module.exports = nextConfig;

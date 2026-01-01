/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',  // Required for Docker deployment
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  // Disable static generation for all pages (force dynamic rendering)
  experimental: {
    dynamicIO: true,
  },
  env: {
    FLASK_API_URL: process.env.FLASK_API_URL || 'http://localhost:5000',
  },
};

export default nextConfig;

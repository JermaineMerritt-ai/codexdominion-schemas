/** @type {import('next').NextConfig} */
const nextConfig = {
  // Remove 'output: export' to enable API routes for Azure Static Web Apps
  // output: 'export',
  images: {
    unoptimized: true,
  },
  trailingSlash: false,
  // Azure Static Web Apps automatically detects Next.js and runs it with Node.js runtime
}

module.exports = nextConfig

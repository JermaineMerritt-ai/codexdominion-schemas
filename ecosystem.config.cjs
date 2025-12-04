// PM2 Ecosystem Configuration for Codex Dominion
// Optimized for efficient production deployment

module.exports = {
  apps: [
    {
      name: 'codex-backend',
      script: './server.js',
      instances: 1,
      exec_mode: 'fork',

      // Environment variables
      env: {
        NODE_ENV: 'development',
        PORT: 3000,
      },
      env_production: {
        NODE_ENV: 'production',
        PORT: 3000,
      },

      // Resource limits
      max_memory_restart: '512M',

      // Logging
      error_file: './logs/backend-error.log',
      out_file: './logs/backend-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,

      // Auto-restart configuration
      autorestart: true,
      watch: false,
      max_restarts: 10,
      min_uptime: '10s',

      // Advanced features
      listen_timeout: 3000,
      kill_timeout: 5000,
      wait_ready: true,

      // Process management
      vizion: false,
      post_update: ['npm install'],
    },

    {
      name: 'codex-frontend',
      script: 'npm',
      args: 'run dev',
      cwd: './frontend',
      instances: 1,
      exec_mode: 'fork',

      // Environment variables
      env: {
        NODE_ENV: 'development',
        PORT: 3001,
        NEXT_PUBLIC_API_URL: 'http://localhost:3000',
      },
      env_production: {
        NODE_ENV: 'production',
        PORT: 3001,
        NEXT_PUBLIC_API_URL: 'http://localhost:3000',
      },

      // Resource limits
      max_memory_restart: '768M',

      // Logging
      error_file: './logs/frontend-error.log',
      out_file: './logs/frontend-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,

      // Auto-restart configuration
      autorestart: true,
      watch: false,
      max_restarts: 10,
      min_uptime: '10s',

      // Advanced features
      listen_timeout: 10000,
      kill_timeout: 5000,

      // Process management
      vizion: false,
    }
  ],

  // Deployment configuration (optional)
  deploy: {
    production: {
      user: 'a3404521',
      host: 'access-5018657992.webspace-host.com',
      ref: 'origin/main',
      repo: 'git@github.com:JermaineMerritt-ai/codexdominion-schemas.git',
      path: '/var/www/codexdominion.app',
      'post-deploy': 'npm install && pm2 reload ecosystem.config.js --env production',
    }
  }
};

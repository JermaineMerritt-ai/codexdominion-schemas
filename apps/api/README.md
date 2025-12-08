# Codex Dominion API

Backend API server for Codex Dominion ecosystem.

## Features

- **Authentication** - JWT-based auth with role-based access control
- **Workflow Management** - Create, execute, and approve prompts
- **Ledger System** - Record and seal sovereign acts
- **Finance Tracking** - Multi-source revenue tracking and reporting
- **Broadcast System** - Dispatch messages across dashboards

## Setup

```bash
# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Run in development
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## Environment Variables

```env
DATABASE_URL=postgres://codex:codex@localhost:5432/dominion
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-key
EMAIL_FROM=broadcast@codexdominion.org
API_PORT=4000
```

## API Endpoints

### Authentication
- `POST /auth/login` - Login and get JWT token

### Prompts
- `POST /prompts` - Create new prompt (steward, council, sovereign)
- `GET /prompts/:id` - Get prompt details
- `POST /prompts/:id/execute` - Execute prompt (sovereign, council)
- `POST /prompts/:id/approve` - Approve prompt (sovereign, council)

### Broadcast
- `POST /broadcast/dispatch` - Dispatch broadcast capsule (sovereign, council)

### Finance
- `GET /finance/summary` - Get financial summary (finance, sovereign)

### Ledger
- `POST /ledger/acts` - Create act (steward, council, sovereign)
- `POST /ledger/acts/:id/seal` - Seal act (sovereign, council)

### Health
- `GET /health` - Health check endpoint

## Development

```bash
npm run dev
```

Server will start on `http://localhost:4000`

## Docker

```bash
# Build image
docker build -t codex-dominion-api .

# Run container
docker run -p 4000:4000 --env-file .env codex-dominion-api
```

# 🔥 CODEX SIGNALS FRONTEND 📊

**React/Next.js Dashboard for Portfolio Intelligence**

_The Merritt Method™ - Frontend Digital Sovereignty_

## Overview

Modern TypeScript/React frontend for the Codex Signals API, providing real-time portfolio intelligence visualization and bulletin generation.

## Features

### ✅ **Core Components**

- **SignalsCard**: Individual position display with tier colors
- **TierSummary**: Portfolio overview with risk distribution
- **Enhanced Dashboard**: Interactive signals management
- **TypeScript API Client**: Type-safe backend integration

### ✅ **Key Capabilities**

- Real-time signals generation
- Interactive tier visualization
- Bulletin download (Markdown)
- Responsive design
- Error handling & loading states

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Update API URL

Edit the Cloud Run URL in your components:

```typescript
const API_URL = 'https://codex-signals-YOUR-HASH.run.app';
```

### 3. Run Development Server

```bash
npm run dev
```

Visit: http://localhost:3000

## Project Structure

```
frontend/
├── components/
│   ├── SignalsCard.tsx      # Individual position cards
│   └── TierSummary.tsx      # Portfolio overview
├── pages/
│   ├── signals.tsx          # Basic signals page
│   └── signals-enhanced.tsx # Full-featured dashboard
├── utils/
│   └── api.ts              # API client & utilities
├── package.json            # Dependencies
├── tsconfig.json          # TypeScript config
└── next.config.js         # Next.js configuration
```

## API Integration

### CodexSignalsAPI Class

```typescript
const { api, utils } = useCodexSignals(API_URL);

// Generate daily signals
const snapshot = await api.generateDailySignals(market, positions);

// Get mock data
const mockData = await api.getMockSignals();

// Download bulletin
const bulletin = await api.generateBulletin('md');
```

### Type Safety

All API responses are fully typed:

```typescript
type SignalsSnapshot = {
  generated_at: string;
  banner: string;
  tier_counts: { Alpha: number; Beta: number; Gamma: number; Delta: number };
  picks: Pick[];
};
```

## Component Usage

### Signals Dashboard

```tsx
import { SignalsCard } from '../components/SignalsCard';
import { TierSummary } from '../components/TierSummary';

<TierSummary
  tierCounts={snapshot.tier_counts}
  generatedAt={snapshot.generated_at}
  banner={snapshot.banner}
/>;

{
  snapshot.picks.map((pick) => <SignalsCard key={pick.symbol} pick={pick} />);
}
```

### Utility Functions

```typescript
// Format weights
utils.formatWeight(0.06); // "6.00%"

// Get tier colors
utils.getTierColor('Alpha'); // "#10b981"

// Generate bulletin markdown
const markdown = utils.generateBulletinMD(snapshot);
```

## Styling & Theme

### Tier Colors

- **Alpha**: `#10b981` (Green - High conviction)
- **Beta**: `#3b82f6` (Blue - Balanced)
- **Gamma**: `#f59e0b` (Orange - Elevated risk)
- **Delta**: `#ef4444` (Red - High turbulence)

### Responsive Design

- Grid layouts adapt to screen size
- Mobile-friendly components
- Clean, modern interface

## Deployment Options

### 1. Vercel (Recommended)

```bash
npm install -g vercel
vercel --prod
```

### 2. Netlify

```bash
npm run build
# Upload dist/ folder to Netlify
```

### 3. Static Export

```bash
npm run build
npm run export
# Deploy static files
```

### 4. Docker Container

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
CMD ["npm", "start"]
```

## Environment Configuration

### Development

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENVIRONMENT=development
```

### Production

```bash
# .env.production
NEXT_PUBLIC_API_URL=https://codex-signals-YOUR-HASH.run.app
NEXT_PUBLIC_ENVIRONMENT=production
```

## Integration with Cloud Run

### CORS Setup

Your Cloud Run service should include CORS headers:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### API Proxy (Optional)

Next.js can proxy API calls:

```javascript
// next.config.js
async rewrites() {
  return [
    {
      source: '/api/signals/:path*',
      destination: 'https://codex-signals-<HASH>.run.app/signals/:path*'
    }
  ];
}
```

## Performance Optimization

### Code Splitting

- Automatic route-based splitting
- Dynamic imports for heavy components
- Optimized bundle sizes

### Caching Strategy

- API response caching
- Static asset optimization
- CDN deployment ready

### Loading States

- Skeleton screens
- Progressive loading
- Error boundaries

## Testing

### Unit Tests

```bash
npm install --save-dev @testing-library/react jest
npm run test
```

### E2E Tests

```bash
npm install --save-dev playwright
npm run test:e2e
```

## Security

### API Security

- HTTPS only in production
- CORS configuration
- Input validation
- XSS protection headers

### Data Privacy

- No sensitive data storage
- Secure API communication
- Environment variable protection

## Monitoring

### Error Tracking

```typescript
// Error boundary integration
try {
  await api.generateDailySignals(market, positions);
} catch (error) {
  console.error('Signals error:', error);
  // Send to monitoring service
}
```

### Analytics

- Page view tracking
- API usage metrics
- Performance monitoring

## Support

### Troubleshooting

1. Check API URL configuration
1. Verify CORS settings
1. Review browser console errors
1. Test API endpoints directly

### Development Tips

- Use TypeScript strict mode
- Enable ESLint for code quality
- Test with mock data first
- Monitor network requests

---

**🔥 The Merritt Method™ - Frontend Portfolio Intelligence 👑**

_Digital sovereignty through superior user experience and real-time financial intelligence visualization._

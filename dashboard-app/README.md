# Codex Dominion Dashboard - Next.js Frontend

Modern, responsive Next.js 14+ dashboard application for Codex Dominion, consuming the Flask backend API.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Flask backend running on `http://localhost:5000`

### Installation

```bash
cd dashboard-app
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) - redirects to `/dashboard/overview`

### Build for Production

```bash
npm run build
npm start
```

## 📁 Project Structure

```
dashboard-app/
├── app/
│   ├── layout.tsx                 # Root layout
│   ├── page.tsx                   # Home (redirects to /dashboard/overview)
│   └── dashboard/
│       ├── layout.tsx             # Dashboard shell with sidebar
│       ├── overview/              # 📊 Overview page
│       ├── capsules/              # 📦 Capsules list & detail
│       ├── intelligence-core/     # ⚙️ Engines list & detail
│       ├── industries/            # 🏭 Industries monitoring
│       ├── platforms/             # 🌐 Platform-specific pages
│       ├── analytics/             # 📈 Analytics dashboard
│       └── settings/              # ⚙️ Settings
│
├── components/
│   ├── layout/                    # Sidebar, Header, DashboardShell
│   ├── capsules/                  # Capsule-specific components
│   ├── engines/                   # Engine-specific components
│   ├── ui/                        # Reusable UI components
│   └── charts/                    # Chart components
│
├── lib/
│   ├── api/                       # API client functions
│   │   ├── client.ts              # Base fetch wrapper
│   │   ├── capsules.ts            # Capsules API
│   │   └── engines.ts             # Engines API
│   ├── models/                    # TypeScript interfaces
│   └── utils/                     # Utility functions
│
└── styles/
    └── globals.css                # Global styles
```

## 🎨 Features

### Implemented
- ✅ **Overview Dashboard** - System stats and recent activity
- ✅ **Industries Page** - 5 industries with readiness heatmap
- ✅ **Sidebar Navigation** - Active state tracking
- ✅ **Responsive Design** - Mobile-friendly layouts
- ✅ **TypeScript Models** - Full type safety
- ✅ **API Integration** - Flask backend proxy

### Coming Soon
- 🔄 **Capsules List & Detail** - Browse and inspect capsules
- 🔄 **Intelligence Core** - Engine monitoring and connections
- 🔄 **Platform Pages** - Diaspora & Teens platform dashboards
- 🔄 **Analytics** - Advanced charts and metrics
- 🔄 **Real-time Updates** - WebSocket integration
- 🔄 **Dark Mode** - Theme toggle

## 🔌 API Integration

The Next.js app proxies requests to the Flask backend running on `localhost:5000`.

### API Endpoints Used
- `GET /api/direct/capsules` - List all capsules
- `GET /api/direct/capsules/:id` - Get capsule details
- `GET /api/direct/intelligence-core` - List all engines
- `GET /api/direct/intelligence-core/:id` - Get engine details
- `GET /api/mapping/engine-to-capsules/:id` - Get engine connections

### Configuration
Set `FLASK_API_URL` in `.env.local`:
```env
FLASK_API_URL=http://localhost:5000
```

## 🎨 Styling

- **Tailwind CSS** - Utility-first styling
- **Custom Theme** - Codex purple gradient (#667eea → #764ba2)
- **Lucide Icons** - Beautiful, consistent icons
- **Responsive Grid** - Mobile-first approach

## 📦 Key Dependencies

- **Next.js 14+** - App Router with Server Components
- **React 18** - Latest React features
- **TypeScript 5** - Full type safety
- **Tailwind CSS 3** - Utility styling
- **Lucide React** - Icon library
- **Recharts** - Chart library (future use)

## 🔥 Development Tips

### Hot Reload
Next.js automatically reloads on file changes.

### Type Checking
```bash
npm run type-check
```

### Linting
```bash
npm run lint
```

### API Proxy
The `next.config.js` rewrites `/api/*` to `http://localhost:5000/api/*`.

## 🚀 Deployment

### Static Export (Azure Static Web Apps)
```bash
npm run build
# Outputs to ./out directory
```

### Vercel Deployment
```bash
vercel deploy
```

### Docker Deployment
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
CMD ["npm", "start"]
```

## 📚 Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Lucide Icons](https://lucide.dev/)

---

**🔥 The Flame Burns Sovereign and Eternal! 👑**

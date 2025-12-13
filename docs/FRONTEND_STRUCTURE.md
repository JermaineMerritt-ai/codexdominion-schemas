# CodexDominion Frontend Structure

## Directory Organization

This project follows a **feature-based architecture** with clear separation of concerns:

```
src/
├── main.tsx                         # Application entry point
├── App.tsx                          # Root component with providers
├── routes/
│   └── index.tsx                    # React Router configuration
├── config/
│   └── dashboard-config.ts          # Studio tiles, routes, labels
├── pages/                           # Top-level route pages
│   ├── DashboardHome/
│   │   └── DashboardHomePage.tsx    # Main dashboard landing
│   ├── AudioStudio/
│   │   ├── AudioStudioPage.tsx      # Audio home page
│   │   └── AudioSessionDetailPage.tsx
│   ├── VideoStudio/
│   │   └── VideoStudioPage.tsx
│   ├── AutomationStudio/
│   │   └── AutomationStudioPage.tsx
│   ├── NotebookStudio/
│   │   └── NotebookStudioPage.tsx
│   ├── PublishingStudio/
│   │   └── PublishingStudioPage.tsx
│   ├── BuilderStudio/
│   │   └── BuilderStudioPage.tsx
│   └── IntelligenceStudio/
│       └── IntelligenceStudioPage.tsx
├── features/                        # Feature modules by domain
│   ├── audio/
│   │   ├── components/
│   │   │   ├── AudioSessionList.tsx
│   │   │   ├── AudioSessionCard.tsx
│   │   │   ├── AudioRecorder.tsx
│   │   │   └── AudioUpload.tsx
│   │   ├── hooks/
│   │   │   ├── useAudioSessions.ts
│   │   │   └── useCreateAudioSession.ts
│   │   └── api/
│   │       └── audioApi.ts
│   ├── video/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── api/
│   ├── automation/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── api/
│   ├── notebook/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── api/
│   ├── publishing/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── api/
│   ├── builder/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── api/
│   └── intelligence/
│       ├── components/
│       ├── hooks/
│       └── api/
├── components/                      # Shared UI components
│   ├── layout/
│   │   ├── MainLayout.tsx           # App shell with sidebar/header
│   │   ├── Sidebar.tsx              # Navigation sidebar
│   │   ├── Header.tsx               # Top header bar
│   │   └── TileGrid.tsx             # Dashboard tile grid
│   └── common/
│       ├── Button.tsx               # Reusable button component
│       ├── Card.tsx                 # Card container
│       └── Spinner.tsx              # Loading spinner
├── styles/
│   ├── globals.css                  # Global styles
│   └── theme.css                    # Theme variables (colors, spacing)
├── lib/
│   ├── apiClient.ts                 # HTTP client wrapper
│   └── storage.ts                   # Azure Blob Storage utilities
└── types/
    ├── audio-studio.ts              # Audio Studio types (already created)
    ├── common.ts                    # Shared types
    └── api.ts                       # API response types
```

---

## Design Principles

### 1. Feature-Based Organization
- Each studio (audio, video, etc.) has its own **feature module**
- Feature modules are **self-contained**: components, hooks, and API clients
- Reduces cross-dependencies and improves maintainability

### 2. Page Components
- **Pages** are route entry points (loaded by React Router)
- Pages **compose** feature components
- Keep pages thin—business logic lives in features

### 3. Shared Components
- **Layout components** define app structure (MainLayout, Sidebar, Header)
- **Common components** are reusable primitives (Button, Card, Spinner)
- Avoid feature-specific logic in shared components

### 4. Configuration-Driven Dashboard
- **dashboard-config.ts** defines all studio tiles
- Single source of truth for routes, labels, and metadata
- Easy to add/remove/reorder studios

### 5. Type Safety
- TypeScript types in `types/` directory
- API responses, domain models, and UI props are all typed
- No `any` types without explicit justification

---

## Key Files

### `src/main.tsx`
Application entry point. Renders React app into DOM.

### `src/App.tsx`
Root component with:
- React Query provider
- React Router setup
- Global error boundary
- Theme provider (if applicable)

### `src/routes/index.tsx`
Defines all application routes using React Router.

### `src/config/dashboard-config.ts`
Central configuration for dashboard tiles, including:
- Studio IDs, names, icons
- Routes and actions
- 48 Intelligence Engines metadata

### `src/lib/apiClient.ts`
Axios/Fetch wrapper with:
- Base URL configuration
- Authentication headers
- Error handling
- Request/response interceptors

### `src/lib/storage.ts`
Azure Blob Storage utilities:
- Upload helpers
- Download/stream helpers
- URL generation

---

## Routing Structure

```
/                               → DashboardHomePage (studio tiles)
/studio/audio                   → AudioStudioPage (sessions list)
/studio/audio/:id               → AudioSessionDetailPage (detail view)
/studio/video                   → VideoStudioPage
/studio/automation              → AutomationStudioPage
/studio/notebook                → NotebookStudioPage
/studio/publishing              → PublishingStudioPage
/studio/builder                 → BuilderStudioPage
/studio/intelligence            → IntelligenceStudioPage
```

Each studio page can have nested routes as needed.

---

## Component Naming Conventions

### Pages
- **Suffix**: `Page` (e.g., `AudioStudioPage`, `AudioSessionDetailPage`)
- **Location**: `src/pages/{Studio}/`
- **Purpose**: Route entry points

### Feature Components
- **Location**: `src/features/{studio}/components/`
- **Naming**: Descriptive PascalCase (e.g., `AudioSessionList`, `AudioRecorder`)
- **Scope**: Used within feature or exposed for cross-feature use

### Shared Components
- **Location**: `src/components/common/` or `src/components/layout/`
- **Naming**: Generic, reusable names (e.g., `Button`, `Card`, `Modal`)
- **Scope**: Used across multiple features

---

## Hooks Naming Conventions

### Feature Hooks
- **Prefix**: `use` (e.g., `useAudioSessions`, `useCreateAudioSession`)
- **Location**: `src/features/{studio}/hooks/`
- **Responsibility**: Encapsulate data fetching, mutations, or complex state

### Shared Hooks
- **Location**: `src/hooks/` (if created)
- **Examples**: `useAuth`, `useToast`, `useLocalStorage`

---

## API Clients

### Feature API Clients
- **Location**: `src/features/{studio}/api/`
- **Naming**: `{studio}Api.ts` (e.g., `audioApi.ts`, `videoApi.ts`)
- **Exports**: Functions like `listSessions()`, `createSession()`, `updateSession()`

### Base API Client
- **Location**: `src/lib/apiClient.ts`
- **Provides**: HTTP client (Axios/Fetch), error handling, auth headers

---

## Styling Approach

### Tailwind CSS (Primary)
- Utility-first classes in components
- Use `className` prop for styling

### CSS Modules (Optional)
- For component-specific styles that need scoping
- Import as `styles.moduleName`

### Global Styles
- **globals.css**: Base styles, resets
- **theme.css**: CSS variables for colors, spacing, typography

---

## Testing Strategy

### Unit Tests
- Component tests: `*.test.tsx`
- Hook tests: `*.test.ts`
- Utility tests: `*.test.ts`

### Integration Tests
- Feature-level flows (e.g., create audio session → upload → view)

### E2E Tests (Future)
- Playwright or Cypress for critical user journeys

---

## State Management

### Local State
- `useState` for simple component state
- `useReducer` for complex state machines

### Server State
- **React Query** for all API data (sessions, assets, etc.)
- Automatic caching, refetching, and optimistic updates

### Global State (Minimal)
- Context API for user authentication, theme
- Avoid global state for feature-specific data

---

## Build & Development

### Development Server
```bash
npm run dev
# or
yarn dev
```

### Build for Production
```bash
npm run build
# or
yarn build
```

### Type Checking
```bash
npm run typecheck
# or
yarn typecheck
```

### Linting
```bash
npm run lint
# or
yarn lint
```

---

## Next Steps

1. ✅ Create `dashboard-config.ts` with studio tiles
2. ✅ Set up React Router in `routes/index.tsx`
3. ✅ Implement `MainLayout` with sidebar and header
4. ✅ Build `DashboardHomePage` with tile grid
5. ✅ Start with Audio Studio MVP (see AUDIO_STUDIO_SPEC.md)
6. 🔄 Iterate on other studios

---

**Last Updated**: December 12, 2025
**Status**: Structure Defined - Ready for Implementation

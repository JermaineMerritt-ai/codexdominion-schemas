# Frontend Build Fix Guide

## Problem Summary

Next.js static export is failing on 7 pages with identical React SSR error:
```
TypeError: Cannot read properties of null (reading 'useState')
```

This occurs because React hooks (useState, useEffect, useContext) are being called during server-side rendering/prerendering without proper client-side configuration.

---

## Affected Files

1. `frontend/pages/index.tsx` - Home page
2. `frontend/pages/faq.tsx` - FAQ page
3. `frontend/pages/products.tsx` - Products page
4. `frontend/pages/contact.tsx` - Contact page
5. `frontend/pages/order/success.tsx` - Order success page
6. `frontend/pages/temporal-rhythm.tsx` - Temporal rhythm page
7. `frontend/pages/compendium-master.tsx` - Compendium master page

---

## Solution 1: Add 'use client' Directive (Recommended for Next.js 13+)

Add `'use client';` as the first line of each affected component file:

### Example Fix for index.tsx
```typescript
'use client';

import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
// ... rest of imports

export default function Home() {
  const [state, setState] = useState(initialValue);
  // ... rest of component
}
```

### Apply to all 7 files:
```bash
# Add 'use client' to each file
echo "'use client';\n\n$(cat frontend/pages/index.tsx)" > frontend/pages/index.tsx
echo "'use client';\n\n$(cat frontend/pages/faq.tsx)" > frontend/pages/faq.tsx
echo "'use client';\n\n$(cat frontend/pages/products.tsx)" > frontend/pages/products.tsx
echo "'use client';\n\n$(cat frontend/pages/contact.tsx)" > frontend/pages/contact.tsx
echo "'use client';\n\n$(cat frontend/pages/order/success.tsx)" > frontend/pages/order/success.tsx
echo "'use client';\n\n$(cat frontend/pages/temporal-rhythm.tsx)" > frontend/pages/temporal-rhythm.tsx
echo "'use client';\n\n$(cat frontend/pages/compendium-master.tsx)" > frontend/pages/compendium-master.tsx
```

---

## Solution 2: Dynamic Imports with SSR Disabled

Wrap components using hooks in dynamic imports with `ssr: false`:

### Example: Create wrapper files

**frontend/components/HomeClient.tsx**
```typescript
import React, { useState, useEffect } from 'react';

export default function HomeClient() {
  const [state, setState] = useState(initialValue);
  // ... component logic
  return (/* JSX */);
}
```

**frontend/pages/index.tsx**
```typescript
import dynamic from 'next/dynamic';

const HomeClient = dynamic(() => import('../components/HomeClient'), {
  ssr: false,
  loading: () => <div>Loading...</div>
});

export default function Home() {
  return <HomeClient />;
}
```

---

## Solution 3: Disable Static Export (Use Standard Next.js Build)

Modify `frontend/next.config.js`:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  // Remove or comment out: output: 'export',
  images: {
    unoptimized: true
  },
  // ... rest of config
};

module.exports = nextConfig;
```

**Deployment Change Required**:
- Cannot deploy to Azure Static Web Apps as static HTML
- Must use Azure App Service or Container Instances for Node.js server
- Requires running `next start` instead of static file serving

---

## Solution 4: Separate Server/Client Components (Next.js 14 App Router)

Migrate to Next.js App Router architecture:

**Directory Structure**:
```
frontend/
  app/
    layout.tsx       (Server Component)
    page.tsx         (Server Component)
    ClientHome.tsx   (Client Component with 'use client')
```

**Example**:

**app/layout.tsx** (Server Component):
```typescript
export default function RootLayout({ children }) {
  return (
    <html>
      <body>{children}</body>
    </html>
  );
}
```

**app/ClientHome.tsx** (Client Component):
```typescript
'use client';

import { useState } from 'react';

export default function ClientHome() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

**app/page.tsx** (Server Component):
```typescript
import ClientHome from './ClientHome';

export default function Home() {
  return (
    <div>
      <h1>Server-rendered content</h1>
      <ClientHome />
    </div>
  );
}
```

---

## Recommended Approach

**For Quick Fix**: Use **Solution 1** (`'use client'` directive)
- Minimal code changes
- Works with existing Next.js 13 Pages Router
- Maintains static export capability (with proper configuration)
- Takes ~5 minutes to implement

**For Production-Ready**: Use **Solution 4** (App Router migration)
- Modern Next.js best practices
- Better performance with React Server Components
- Clear separation of server/client boundaries
- Better for long-term maintainability

---

## Implementation Steps

### Quick Fix (Solution 1)

1. **Edit each affected file** and add `'use client';` as first line
2. **Rebuild frontend**:
   ```bash
   cd frontend
   npm run build
   ```
3. **Verify all pages export successfully**:
   - Should see: `✓ Generating static pages (77/77)` without errors
4. **Deploy to Static Web App**:
   ```bash
   cd ../static-deploy
   npx @azure/static-web-apps-cli deploy . --deployment-token <TOKEN> --env production
   ```

### Verification

```bash
# Check build output for errors
cd frontend && npm run build 2>&1 | grep -i error

# Verify dist/out directory created
ls -la out/

# Count exported HTML files
find out/ -name "*.html" | wc -l  # Should be 77+
```

---

## Post-Fix Deployment

Once build succeeds, deploy using one of these methods:

### Option A: Azure Static Web Apps CLI
```bash
cd frontend/out
npx @azure/static-web-apps-cli deploy . \
  --deployment-token $AZURE_STATIC_WEB_APPS_API_TOKEN \
  --env production
```

### Option B: GitHub Actions (Automatic)
```bash
# Commit and push changes - workflow will auto-deploy
git add frontend/
git commit -m "Fix: Add 'use client' directives for SSR compatibility"
git push origin main
```

### Option C: Manual Upload via Azure CLI
```bash
az staticwebapp update \
  --name codexdominion-frontend \
  --resource-group codex-dominion \
  --source frontend/out
```

---

## Testing After Fix

1. **Build Test**:
   ```bash
   cd frontend && npm run build
   # Should complete without errors
   ```

2. **Local Preview**:
   ```bash
   cd frontend && npm run start
   # Visit http://localhost:3000
   ```

3. **Deployed Site Test**:
   ```
   https://happy-hill-0f1fded0f.3.azurestaticapps.net
   https://www.codexdominion.app
   ```

4. **Verify All Pages Load**:
   - Home: https://www.codexdominion.app/
   - FAQ: https://www.codexdominion.app/faq
   - Products: https://www.codexdominion.app/products
   - Contact: https://www.codexdominion.app/contact
   - Order Success: https://www.codexdominion.app/order/success
   - Temporal Rhythm: https://www.codexdominion.app/temporal-rhythm
   - Compendium Master: https://www.codexdominion.app/compendium-master

---

## Alternative: Keep Placeholder Until Full Refactor

If fixing all 7 pages is time-consuming, consider:

1. **Keep static placeholder active** at https://www.codexdominion.app
2. **Deploy functional pages** to subdomain (e.g., app.codexdominion.app)
3. **Complete full App Router migration** for production-ready solution
4. **Swap placeholder with full app** once migration complete

---

## Reference Links

- [Next.js App Router Documentation](https://nextjs.org/docs/app)
- [React Server Components](https://react.dev/blog/2023/03/22/react-labs-what-we-have-been-working-on-march-2023#react-server-components)
- [Next.js Static Exports](https://nextjs.org/docs/app/building-your-application/deploying/static-exports)
- [Azure Static Web Apps Deployment](https://learn.microsoft.com/en-us/azure/static-web-apps/getting-started)

---

## Troubleshooting

### Build still fails after adding 'use client'
- **Check**: Ensure directive is the FIRST line (before imports)
- **Verify**: No syntax errors in the file
- **Clear**: Delete `.next` and `out` directories, rebuild

### Static export not working
- **Check**: `next.config.js` has `output: 'export'`
- **Verify**: No unsupported features (Incremental Static Regeneration, Server Actions)
- **Check**: Images use `unoptimized: true` in config

### Pages still have SSR errors
- **Check**: All child components also have 'use client' or are wrapped
- **Verify**: No server-side-only code in client components
- **Consider**: Using dynamic imports for problematic components

---

**Status**: Ready to implement - Choose solution and execute

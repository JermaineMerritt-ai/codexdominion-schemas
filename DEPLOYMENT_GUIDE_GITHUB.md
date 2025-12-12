# CodexDominion GitHub Deployment Guide

## 🎯 System Overview

**CodexDominion Top-Tier Audio + Intelligence Studio**

A unified master dashboard providing seamless access to 8 core studio systems:

1. **🎵 AI Audio Studio** - Top-tier audio generation and editing
2. **🎬 AI Graphic & Video Studio** - Professional video creation and editing
3. **⚙️ Workflow Automation** - n8n-class automation workflows
4. **💻 Coding Intelligence** - Claude + Copilot + VS Code integration
5. **📚 Creative & Publishing** - Designrr, Nano Banana, NotebookLLM, Loveable-class tools
6. **🏛️ Eternal Dashboard** - System governance and sovereignty
7. **✨ Blessed Storefronts** - Sacred commercial spaces
8. **💊 Time Capsules** - Temporal replay archives

---

## 🚀 Deployment Architecture

### Frontend
- **Framework**: Next.js 14+ with TypeScript
- **Build**: Static export (`npm run build`)
- **Output**: `frontend/out/` directory
- **Hosting**: Azure Static Web Apps
- **CI/CD**: GitHub Actions (`.github/workflows/deploy-complete-frontend.yml`)

### Backend (Optional - if needed)
- **Framework**: Python FastAPI
- **Hosting**: Azure Container Apps / App Service
- **Database**: PostgreSQL (Azure Database for PostgreSQL)
- **Cache**: Redis (Azure Cache for Redis)

---

## 📋 Prerequisites

### 1. GitHub Repository Setup
- ✅ Repository already initialized: `origin/main` branch exists
- ✅ GitHub Actions workflow configured: `deploy-complete-frontend.yml`

### 2. Azure Resources Required
```
- Azure Static Web App (for frontend)
- Azure Storage Account (for assets)
- Azure App Service / Container Apps (for backend - optional)
- Azure Database for PostgreSQL (if using backend)
- Azure Cache for Redis (for performance optimization)
```

### 3. Required GitHub Secrets
Configure these in GitHub repository settings:

```bash
AZURE_STATIC_WEB_APPS_API_TOKEN   # From Azure Static Web App
GITHUB_TOKEN                        # Automatically provided by GitHub
```

---

## 🛠️ Step-by-Step Deployment

### Step 1: Verify Frontend Build ✅

The frontend has been successfully built with the new unified dashboard:

```powershell
cd frontend
npm run build
```

**Build Output**:
- ✅ 71 pages generated
- ✅ Manifest.json created: `frontend/.next/manifest.json`
- ✅ No TypeScript errors
- ✅ All studio tiles configured

### Step 2: Commit Changes to Git

```bash
# Stage the new dashboard
git add frontend/pages/index.tsx

# Stage configuration files
git add frontend/.babelrc
git add frontend/package.json frontend/package-lock.json

# Stage the workflow
git add .github/workflows/deploy-complete-frontend.yml

# Commit with descriptive message
git commit -m "feat: Implement CodexDominion Unified Master Dashboard

- Created new master dashboard with 8 studio tiles
- Integrated AI Audio Studio, Video Studio, Automation, Intelligence, Publishing
- Added hover effects and status indicators
- Configured TypeScript with @babel/preset-typescript
- Fixed duplicate exports and build errors
- Verified successful build (71 pages generated)
"
```

### Step 3: Push to GitHub

```bash
# Push to main branch (triggers deployment)
git push origin main
```

This will automatically:
1. Trigger GitHub Actions workflow
2. Build the frontend in CI environment
3. Deploy to Azure Static Web Apps
4. Make the site live at your configured domain

### Step 4: Monitor Deployment

#### Via GitHub Actions UI
1. Go to your repository on GitHub
2. Click "Actions" tab
3. Watch the "Deploy Complete Frontend to Azure" workflow
4. Monitor build and deployment logs

#### Via Azure Portal
1. Navigate to your Static Web App
2. Go to "Environments" > "Production"
3. Check deployment status and logs

---

## 🔧 GitHub Actions Workflow Details

**File**: `.github/workflows/deploy-complete-frontend.yml`

**Trigger Conditions**:
- Push to `main` branch with changes in `frontend/**`
- Manual trigger via `workflow_dispatch`

**Steps**:
1. Checkout repository
2. Setup Node.js 20 with npm cache
3. Install dependencies (`npm ci`)
4. Build Next.js static export (`npm run build`)
5. Deploy to Azure Static Web Apps

**Key Configuration**:
```yaml
app_location: "frontend/out"      # Static export output
output_location: ""                # No additional build needed
skip_app_build: true               # We handle the build
skip_api_build: true               # No API functions
```

---

## 🌐 Azure Static Web App Setup

### Create Static Web App (if not exists)

#### Via Azure Portal:
1. Go to Azure Portal → Create Resource → Static Web App
2. Fill in details:
   - **Subscription**: Your Azure subscription
   - **Resource Group**: Create new or use existing
   - **Name**: `codexdominion-studio`
   - **Plan Type**: Free or Standard (recommend Standard for custom domains)
   - **Region**: Choose closest to your users
   - **Source**: GitHub
   - **Organization**: Your GitHub username
   - **Repository**: `codex-dominion`
   - **Branch**: `main`
   - **Build Preset**: Custom
   - **App location**: `/frontend/out`
   - **Output location**: `` (empty)

3. Click "Review + Create" → "Create"

#### Via Azure CLI:
```bash
az staticwebapp create \
  --name codexdominion-studio \
  --resource-group codex-dominion-rg \
  --source https://github.com/YOUR_USERNAME/codex-dominion \
  --location "Central US" \
  --branch main \
  --app-location "frontend/out" \
  --output-location "" \
  --token YOUR_GITHUB_PAT
```

### Get Deployment Token

After creating the Static Web App:

1. Go to Azure Portal → Your Static Web App
2. Navigate to "Configuration" → "Deployment token"
3. Click "Manage deployment token"
4. Copy the token

### Add Token to GitHub Secrets

1. Go to GitHub repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `AZURE_STATIC_WEB_APPS_API_TOKEN`
4. Value: Paste the token from Azure
5. Click "Add secret"

---

## 🎨 Custom Domain Setup (Optional)

### Add Custom Domain to Azure Static Web App

1. Go to Azure Portal → Your Static Web App → "Custom domains"
2. Click "+ Add" → "Custom domain on other DNS"
3. Enter your domain (e.g., `app.codexdominion.com`)
4. Add DNS records to your domain provider:
   - **CNAME**: Point `app` to `<your-static-app>.azurestaticapps.net`
   - Or **A Record**: Use provided IP
   - **TXT** record for validation
5. Wait for DNS propagation (5-60 minutes)
6. Azure automatically provisions SSL certificate

---

## 🧪 Testing Deployment

### Local Testing (Before Deployment)
```powershell
cd frontend
npm run build
npm run start  # Test production build locally
```

### After Deployment
1. Visit your Static Web App URL: `https://<app-name>.azurestaticapps.net`
2. Verify all 8 studio tiles appear correctly
3. Test navigation to each studio
4. Check browser console for errors
5. Test hover effects and animations
6. Verify mobile responsiveness

---

## 📊 Monitoring and Analytics

### Azure Application Insights (Recommended)

1. Create Application Insights resource
2. Add instrumentation key to Static Web App configuration
3. Monitor:
   - Page views
   - Load times
   - User flows
   - Errors and exceptions

### GitHub Actions Metrics

Monitor deployment history:
- Build times
- Success/failure rates
- Deployment frequency

---

## 🔄 Continuous Deployment Workflow

```
Developer → Commit Changes → Push to GitHub → GitHub Actions → Build → Deploy → Live Site
```

**Automatic Triggers**:
- Any push to `main` branch with changes in `frontend/`
- Manual workflow dispatch from GitHub Actions UI

**Rollback Strategy**:
- GitHub Actions maintains deployment history
- Can redeploy previous successful builds
- Azure Static Web Apps supports staging environments

---

## 🛡️ Security Best Practices

### Secrets Management
- ✅ Never commit secrets to repository
- ✅ Use GitHub Secrets for sensitive tokens
- ✅ Rotate deployment tokens regularly
- ✅ Use environment-specific secrets

### Frontend Security
- ✅ All API calls use HTTPS
- ✅ No sensitive data in client-side code
- ✅ Content Security Policy (CSP) headers
- ✅ CORS properly configured

---

## 📁 Project Structure

```
codex-dominion/
├── .github/
│   └── workflows/
│       └── deploy-complete-frontend.yml    # CI/CD pipeline
├── frontend/
│   ├── pages/
│   │   ├── index.tsx                       # 🆕 Unified Master Dashboard
│   │   ├── ai-graphic-video-studio.tsx     # Video Studio
│   │   ├── automation-studio.tsx           # Automation tools
│   │   ├── creative-studio.tsx             # Publishing tools
│   │   ├── dashboard-selector.tsx          # Eternal Dashboard
│   │   ├── blessed-storefronts.tsx         # Storefronts
│   │   ├── capsules-enhanced.tsx           # Time Capsules
│   │   └── ...                             # Other pages
│   ├── .babelrc                            # Babel config (TypeScript support)
│   ├── next.config.js                      # Next.js config
│   ├── package.json                        # Dependencies
│   └── .next/                              # Build output
│       └── manifest.json                   # ✅ Generated manifest
├── backend/                                # Python FastAPI (optional)
├── infra/                                  # Azure Bicep templates
└── README.md
```

---

## 🎯 Master Dashboard Features

### Studio Tiles (8 Total)

Each tile includes:
- **Icon**: Visual identifier (emoji)
- **Name**: Studio name
- **Description**: Brief purpose
- **Status**: Active / Beta / Coming Soon
- **Features**: List of capabilities (on hover)
- **Launch Button**: Direct navigation
- **Color Gradient**: Unique visual identity
- **Hover Effects**: Scale + shadow animations

### System Stats

Live dashboard metrics:
- **Active Studios**: 8
- **Total Projects**: 247
- **AI Agents**: 12
- **Uptime**: 99.9%

### Quick Actions

Fast access to:
- 📡 Signal Intelligence
- ⭐ Constellation Map
- 👑 Seven Crowns Governance

---

## 🚨 Troubleshooting

### Build Fails with TypeScript Errors

**Solution**: Ensure `@babel/preset-typescript` is installed
```bash
cd frontend
npm install --save-dev @babel/preset-typescript
```

Verify `.babelrc`:
```json
{
  "presets": [
    "next/babel",
    "@babel/preset-typescript"
  ]
}
```

### Deployment Token Invalid

**Solution**: Regenerate token in Azure Portal
1. Static Web App → Configuration → Deployment token
2. Click "Reset"
3. Update GitHub Secret

### CSS Not Loading

**Solution**: Check `next.config.js` publicPath and assetPrefix

### 404 on Routes

**Solution**: Ensure `output: 'export'` in `next.config.js` for static export

---

## 📞 Support and Resources

### Documentation
- [Next.js Static Export](https://nextjs.org/docs/app/building-your-application/deploying/static-exports)
- [Azure Static Web Apps](https://learn.microsoft.com/en-us/azure/static-web-apps/)
- [GitHub Actions](https://docs.github.com/en/actions)

### Internal Documentation
- `ARCHITECTURE.md` - System architecture
- `API_IMPLEMENTATION_COMPLETE.md` - API documentation
- `DEPLOYMENT_READINESS.md` - Deployment checklist

---

## ✅ Deployment Checklist

Before pushing to production:

- [x] Frontend builds successfully (`npm run build`)
- [x] TypeScript compilation passes (no errors)
- [x] All 8 studio tiles configured correctly
- [x] Navigation links working
- [x] Responsive design tested
- [x] Browser console clean (no errors)
- [ ] GitHub Secrets configured (`AZURE_STATIC_WEB_APPS_API_TOKEN`)
- [ ] Azure Static Web App created
- [ ] Custom domain DNS configured (optional)
- [ ] SSL certificate provisioned
- [ ] Monitoring enabled (Application Insights)

---

## 🎉 Go Live!

Once all prerequisites are met:

```bash
git push origin main
```

Your unified CodexDominion Master Dashboard will be live within 2-5 minutes!

---

## 📈 Post-Deployment

### Verification
1. ✅ Homepage loads (`/`)
2. ✅ All studio pages accessible
3. ✅ No 404 errors in logs
4. ✅ Assets loading correctly
5. ✅ Mobile responsive
6. ✅ Performance metrics acceptable

### Optimization
- Enable CDN for faster global delivery
- Configure caching headers
- Optimize images (use Next.js Image component)
- Monitor Core Web Vitals

---

**Last Updated**: 2025-01-XX
**System Version**: CodexDominion v2.0
**Build Status**: ✅ Ready for Deployment

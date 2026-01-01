"""
🔥 CODEX DOMINION - WEBSITE CREATION WORKFLOW (STEPS 6-10) 🔥
================================================================
Advanced steps: React components, Git, Deployment, Metrics

EXECUTION STEPS:
6. Insert Generated Content Into React Components
7. Initialize Git Repository  
8. Trigger Deployment Pipeline (Vercel/Netlify)
9. Return Final Artifacts to CodexDominion
10. Update Workflow Status + Metrics

Author: Codex Dominion AI Systems
Date: December 20, 2025
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid


# =============================================================================
# STEP 6: INSERT GENERATED CONTENT INTO REACT COMPONENTS
# =============================================================================

def generate_nextjs_project(
    blueprint: Dict[str, Any],
    content: Dict[str, Any],
    theme: Dict[str, Any],
    seo: Dict[str, Any],
    site_name: str,
    output_dir: Path
) -> Dict[str, Any]:
    """
    Step 6: Convert JSON blueprints into actual Next.js project with React components.
    
    This is where the site becomes REAL - actual code files, not just JSON.
    """
    print("\n⚛️  STEP 6: Generating Next.js Project Files...")
    
    project_dir = output_dir / "nextjs-app"
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # Create directory structure
    app_dir = project_dir / "app"
    components_dir = project_dir / "components"
    styles_dir = project_dir / "styles"
    public_dir = project_dir / "public"
    
    for d in [app_dir, components_dir, styles_dir, public_dir]:
        d.mkdir(exist_ok=True)
    
    # Generate package.json
    package_json = {
        "name": site_name.lower().replace(" ", "-"),
        "version": "1.0.0",
        "private": True,
        "scripts": {
            "dev": "next dev",
            "build": "next build",
            "start": "next start",
            "lint": "next lint"
        },
        "dependencies": {
            "next": "14.2.0",
            "react": "^18.2.0",
            "react-dom": "^18.2.0"
        },
        "devDependencies": {
            "@types/node": "^20",
            "@types/react": "^18",
            "@types/react-dom": "^18",
            "typescript": "^5",
            "tailwindcss": "^3.4.0",
            "postcss": "^8",
            "autoprefixer": "^10"
        }
    }
    (project_dir / "package.json").write_text(json.dumps(package_json, indent=2))
    
    # Generate tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "ES2017",
            "lib": ["dom", "dom.iterable", "esnext"],
            "allowJs": True,
            "skipLibCheck": True,
            "strict": True,
            "noEmit": True,
            "esModuleInterop": True,
            "module": "esnext",
            "moduleResolution": "bundler",
            "resolveJsonModule": True,
            "isolatedModules": True,
            "jsx": "preserve",
            "incremental": True,
            "plugins": [{"name": "next"}],
            "paths": {"@/*": ["./*"]}
        },
        "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
        "exclude": ["node_modules"]
    }
    (project_dir / "tsconfig.json").write_text(json.dumps(tsconfig, indent=2))
    
    # Generate next.config.js
    next_config = """/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: { unoptimized: true }
}

module.exports = nextConfig
"""
    (project_dir / "next.config.js").write_text(next_config)
    
    # Generate tailwind.config.js with theme
    primary = theme['colors']['brand']['primary']
    secondary = theme['colors']['brand']['secondary']
    accent = theme['colors']['brand']['accent']
    heading_font = theme['typography']['fonts']['heading']
    body_font = theme['typography']['fonts']['body']
    
    tailwind_config = f"""/** @type {{import('tailwindcss').Config}} */
module.exports = {{
  content: [
    './pages/**/*.{{js,ts,jsx,tsx,mdx}}',
    './components/**/*.{{js,ts,jsx,tsx,mdx}}',
    './app/**/*.{{js,ts,jsx,tsx,mdx}}',
  ],
  theme: {{
    extend: {{
      colors: {{
        primary: '{primary}',
        secondary: '{secondary}',
        accent: '{accent}',
      }},
      fontFamily: {{
        heading: ['{heading_font}', 'sans-serif'],
        body: ['{body_font}', 'sans-serif'],
      }},
    }},
  }},
  plugins: [],
}}
"""
    (project_dir / "tailwind.config.js").write_text(tailwind_config)
    
    # Generate postcss.config.js
    postcss_config = """module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""
    (project_dir / "postcss.config.js").write_text(postcss_config)
    
    # Generate globals.css with theme
    globals_css = f"""{theme['css_variables']}

@tailwind base;
@tailwind components;
@tailwind utilities;

body {{
  font-family: var(--font-body);
  color: var(--foreground);
  background: var(--background);
}}

h1, h2, h3, h4, h5, h6 {{
  font-family: var(--font-heading);
}}

@layer components {{
  .btn-primary {{
    @apply px-6 py-3 bg-primary text-white rounded-lg hover:opacity-90 transition-opacity;
  }}
  
  .card {{
    @apply p-6 rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow;
  }}
}}
"""
    (styles_dir / "globals.css").write_text(globals_css)
    
    # Generate root layout
    layout_tsx = f"""import '../styles/globals.css'
import {{ Metadata }} from 'next'
import Header from '@/components/Header'
import Footer from '@/components/Footer'

export const metadata: Metadata = {{
  title: '{seo['global']['default_title']}',
  description: '{seo['global']['default_description']}',
  openGraph: {{
    siteName: '{site_name}',
    type: 'website',
  }},
}}

export default function RootLayout({{
  children,
}}: {{
  children: React.ReactNode
}}) {{
  return (
    <html lang="en">
      <body>
        <Header />
        {{children}}
        <Footer />
      </body>
    </html>
  )
}}
"""
    (app_dir / "layout.tsx").write_text(layout_tsx)
    
    # Generate page components for each page
    pages_created = []
    for page in blueprint["pages"]:
        page_slug = page["slug"]
        page_content = content["pages"].get(page_slug, {})
        page_seo = seo["pages"].get(page_slug, {})
        
        # Create page directory (App Router)
        if page_slug == "home":
            page_dir = app_dir
        else:
            page_dir = app_dir / page_slug
            page_dir.mkdir(exist_ok=True)
        
        # Generate page.tsx with actual content
        features = page_content.get('feature_items', [])
        features_html = ""
        if features:
            features_html = "\n        <div className=\"grid grid-cols-1 md:grid-cols-3 gap-8 mt-12\">\n"
            for feature in features[:3]:
                features_html += f"""          <div className="card">
            <h3 className="text-xl font-heading font-bold mb-2">{feature.get('title', '')}</h3>
            <p className="text-gray-600">{feature.get('description', '')}</p>
          </div>\n"""
            features_html += "        </div>"
        
        page_tsx = f"""import {{ Metadata }} from 'next'

export const metadata: Metadata = {{
  title: '{page_seo.get('title', page['title'])}',
  description: '{page_seo.get('description', '')}',
  openGraph: {{
    title: '{page_seo.get('og_title', page['title'])}',
    description: '{page_seo.get('og_description', '')}',
    images: ['{page_seo.get('og_image', '/og-image.png')}'],
  }},
}}

export default function {page['title'].replace(' ', '').replace('-', '')}Page() {{
  return (
    <main className="min-h-screen">
      {{/* Hero Section */}}
      <section className="container mx-auto px-4 py-16 md:py-24">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-heading font-bold mb-6">
            {page_content.get('hero_title', f'Welcome to {{page["title"]}}')}
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 mb-8">
            {page_content.get('hero_subtitle', page['title'])}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="btn-primary">
              {page_content.get('cta_text', 'Get Started')}
            </button>
            <button className="px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
              {page_content.get('cta_secondary_text', 'Learn More')}
            </button>
          </div>
        </div>{features_html}
      </section>
    </main>
  )
}}
"""
        page_file = page_dir / "page.tsx"
        page_file.write_text(page_tsx)
        pages_created.append(str(page_file))
        print(f"   ✓ {page_slug}/page.tsx")
    
    # Generate Header component with navigation
    nav_items = "\n            ".join([
        f'<a href="/{p["slug"] if p["slug"] != "home" else ""}" className="hover:text-primary transition-colors">{p["title"]}</a>'
        for p in blueprint["pages"][:5]
    ])
    
    header_tsx = f"""export default function Header() {{
  return (
    <header className="border-b">
      <nav className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <a href="/" className="text-2xl font-heading font-bold">
            {site_name}
          </a>
          <div className="hidden md:flex gap-6">
            {nav_items}
          </div>
        </div>
      </nav>
    </header>
  )
}}
"""
    (components_dir / "Header.tsx").write_text(header_tsx)
    print(f"   ✓ components/Header.tsx")
    
    # Generate Footer component
    footer_tsx = f"""export default function Footer() {{
  return (
    <footer className="bg-gray-900 text-white py-8 mt-16">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-xl font-heading font-bold mb-4">{site_name}</h3>
            <p className="text-gray-400">{blueprint['meta']['description']}</p>
          </div>
          <div>
            <h4 className="font-heading font-bold mb-4">Quick Links</h4>
            <div className="flex flex-col gap-2">
              {nav_items}
            </div>
          </div>
          <div>
            <h4 className="font-heading font-bold mb-4">Contact</h4>
            <p className="text-gray-400">info@example.com</p>
          </div>
        </div>
        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2025 {site_name}. All rights reserved.</p>
          <p className="text-sm mt-2">Generated by Codex Dominion</p>
        </div>
      </div>
    </footer>
  )
}}
"""
    (components_dir / "Footer.tsx").write_text(footer_tsx)
    print(f"   ✓ components/Footer.tsx")
    
    # Generate README.md
    readme = f"""# {site_name}

{blueprint['meta']['description']}

## 🚀 Generated by Codex Dominion Workflow Engine

This website was automatically generated using the Codex Dominion Website Creation Workflow.

- **Platform**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **Pages**: {len(blueprint['pages'])}
- **Components**: {len(blueprint['components_used'])}
- **Generated**: {datetime.now(timezone.utc).strftime('%B %d, %Y')}

## 📦 Getting Started

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view.

## 📁 Project Structure

```
├── app/              # Next.js App Router pages
│   ├── layout.tsx    # Root layout with Header/Footer
│   ├── page.tsx      # Home page
│   └── [page]/       # Dynamic pages
├── components/       # React components
│   ├── Header.tsx
│   └── Footer.tsx
├── styles/           # Global styles
│   └── globals.css
├── public/           # Static assets
└── package.json      # Dependencies
```

## 🔨 Build

```bash
npm run build
npm start
```

## 📄 Deployment

### Vercel (Recommended)
```bash
npm i -g vercel
vercel deploy
```

### Netlify
```bash
npm run build
# Drag `out/` folder to Netlify UI
```

### Manual
```bash
npm run build
# Upload `out/` directory to any static host
```

---

**Generated by**: Codex Dominion Workflow Engine  
**Timestamp**: {datetime.now(timezone.utc).isoformat()}
"""
    (project_dir / "README.md").write_text(readme, encoding='utf-8')
    print(f"   ✓ README.md")
    
    print(f"   ✅ Next.js project generated with {len(pages_created)} pages\n")
    
    return {
        "project_dir": str(project_dir),
        "pages_created": pages_created,
        "components_created": [
            str(components_dir / "Header.tsx"),
            str(components_dir / "Footer.tsx")
        ]
    }


# =============================================================================
# STEP 7: INITIALIZE GIT REPOSITORY
# =============================================================================

def initialize_git_repository(
    project_dir: Path,
    site_name: str,
    create_github_repo: bool = False,
    github_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Step 7: Initialize Git repo and optionally create GitHub repository.
    """
    print("\n📦 STEP 7: Initializing Git Repository...")
    
    try:
        # Initialize Git
        subprocess.run(["git", "init"], cwd=project_dir, check=True, capture_output=True)
        print(f"   ✓ Git initialized")
        
        # Create .gitignore
        gitignore = """# dependencies
node_modules/
.pnp/
.pnp.js

# testing
coverage/

# next.js
.next/
out/
build/

# misc
.DS_Store
*.pem

# debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# local env files
.env*.local

# vercel
.vercel

# typescript
*.tsbuildinfo
next-env.d.ts
"""
        (project_dir / ".gitignore").write_text(gitignore)
        print(f"   ✓ .gitignore created")
        
        # Add all files
        subprocess.run(["git", "add", "."], cwd=project_dir, check=True, capture_output=True)
        print(f"   ✓ Files staged")
        
        # Initial commit
        commit_msg = f"Initial commit — generated by CodexDominion Workflow Engine"
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=project_dir,
            check=True,
            capture_output=True
        )
        print(f"   ✓ Initial commit created")
        
        result = {
            "git_initialized": True,
            "local_repo": str(project_dir),
            "github_repo": None
        }
        
        # Create GitHub repo if requested
        if create_github_repo and github_token:
            try:
                import requests
                
                repo_name = site_name.lower().replace(" ", "-")
                response = requests.post(
                    "https://api.github.com/user/repos",
                    headers={
                        "Authorization": f"Bearer {github_token}",
                        "Accept": "application/vnd.github+json"
                    },
                    json={
                        "name": repo_name,
                        "description": f"Website generated by Codex Dominion",
                        "private": False,
                        "auto_init": False
                    }
                )
                
                if response.status_code == 201:
                    repo_data = response.json()
                    repo_url = repo_data["html_url"]
                    clone_url = repo_data["clone_url"]
                    
                    # Add remote and push
                    subprocess.run(
                        ["git", "remote", "add", "origin", clone_url],
                        cwd=project_dir,
                        check=True,
                        capture_output=True
                    )
                    subprocess.run(
                        ["git", "branch", "-M", "main"],
                        cwd=project_dir,
                        check=True,
                        capture_output=True
                    )
                    subprocess.run(
                        ["git", "push", "-u", "origin", "main"],
                        cwd=project_dir,
                        check=True,
                        capture_output=True
                    )
                    
                    result["github_repo"] = repo_url
                    print(f"   ✅ GitHub repo created: {repo_url}")
                else:
                    print(f"   ⚠️  GitHub repo creation failed: {response.status_code}")
            except Exception as e:
                print(f"   ⚠️  GitHub integration error: {str(e)}")
        
        print(f"   ✅ Git repository initialized\n")
        return result
        
    except subprocess.CalledProcessError as e:
        print(f"   ⚠️  Git initialization failed: {str(e)}")
        return {"git_initialized": False, "error": str(e)}
    except FileNotFoundError:
        print(f"   ⚠️  Git not found - install Git first")
        return {"git_initialized": False, "error": "Git not installed"}


# =============================================================================
# STEP 8: TRIGGER DEPLOYMENT PIPELINE
# =============================================================================

def deploy_to_vercel(
    project_dir: Path,
    site_name: str,
    vercel_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Step 8: Deploy Next.js project to Vercel.
    """
    print("\n🚀 STEP 8: Triggering Deployment to Vercel...")
    
    if not vercel_token:
        print(f"   ⚠️  No Vercel token provided - skipping deployment")
        print(f"   💡 Deploy manually: cd {project_dir} && vercel deploy")
        return {"deployed": False, "manual_command": f"cd {project_dir} && vercel deploy"}
    
    try:
        # Deploy to Vercel
        result = subprocess.run(
            ["vercel", "deploy", "--prod", "--token", vercel_token],
            cwd=project_dir,
            check=True,
            capture_output=True,
            text=True
        )
        
        # Extract deployment URL from output
        output = result.stdout
        deployment_url = None
        for line in output.split("\n"):
            if "https://" in line and "vercel.app" in line:
                deployment_url = line.strip()
                break
        
        print(f"   ✅ Deployed to Vercel: {deployment_url}\n")
        
        return {
            "deployed": True,
            "platform": "vercel",
            "url": deployment_url,
            "status": "success"
        }
        
    except subprocess.CalledProcessError as e:
        print(f"   ⚠️  Vercel deployment failed: {str(e)}")
        return {
            "deployed": False,
            "platform": "vercel",
            "error": str(e),
            "manual_command": f"cd {project_dir} && vercel deploy"
        }
    except FileNotFoundError:
        print(f"   ⚠️  Vercel CLI not found - install: npm i -g vercel")
        return {
            "deployed": False,
            "error": "Vercel CLI not installed",
            "manual_command": f"npm i -g vercel && cd {project_dir} && vercel deploy"
        }


def deploy_to_netlify(
    project_dir: Path,
    site_name: str,
    netlify_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Step 8: Deploy static site to Netlify.
    """
    print("\n🚀 STEP 8: Triggering Deployment to Netlify...")
    
    if not netlify_token:
        print(f"   ⚠️  No Netlify token provided - skipping deployment")
        print(f"   💡 Deploy manually: cd {project_dir} && npm run build && netlify deploy")
        return {"deployed": False, "manual_command": f"cd {project_dir} && netlify deploy"}
    
    try:
        # Build first
        subprocess.run(["npm", "run", "build"], cwd=project_dir, check=True, capture_output=True)
        print(f"   ✓ Build completed")
        
        # Deploy to Netlify
        result = subprocess.run(
            ["netlify", "deploy", "--prod", "--dir=out", "--auth", netlify_token],
            cwd=project_dir,
            check=True,
            capture_output=True,
            text=True
        )
        
        # Extract deployment URL
        output = result.stdout
        deployment_url = None
        for line in output.split("\n"):
            if "https://" in line and "netlify.app" in line:
                deployment_url = line.strip()
                break
        
        print(f"   ✅ Deployed to Netlify: {deployment_url}\n")
        
        return {
            "deployed": True,
            "platform": "netlify",
            "url": deployment_url,
            "status": "success"
        }
        
    except subprocess.CalledProcessError as e:
        print(f"   ⚠️  Netlify deployment failed: {str(e)}")
        return {"deployed": False, "error": str(e)}
    except FileNotFoundError:
        print(f"   ⚠️  Netlify CLI not found - install: npm i -g netlify-cli")
        return {"deployed": False, "error": "Netlify CLI not installed"}


# =============================================================================
# STEP 9: RETURN FINAL ARTIFACTS TO CODEX DOMINION
# =============================================================================

def collect_final_artifacts(
    site_name: str,
    blueprint: Dict[str, Any],
    content: Dict[str, Any],
    theme: Dict[str, Any],
    seo: Dict[str, Any],
    nextjs_result: Dict[str, Any],
    git_result: Dict[str, Any],
    deployment_result: Dict[str, Any],
    duration: float
) -> Dict[str, Any]:
    """
    Step 9: Collect all artifacts and metadata for return to workflow engine.
    
    These will appear in:
    - Workflow detail page
    - Agent profile (completed work)
    - Council analytics
    - Dashboard metrics
    """
    print("\n📊 STEP 9: Collecting Final Artifacts...")
    
    artifacts = {
        "execution_id": f"exec_{uuid.uuid4().hex[:12]}",
        "site_name": site_name,
        "status": "completed",
        "duration_seconds": round(duration, 2),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        
        # URLs
        "urls": {
            "deployed_site": deployment_result.get("url"),
            "github_repo": git_result.get("github_repo"),
            "preview_url": deployment_result.get("url")
        },
        
        # Generated artifacts
        "artifacts": {
            "blueprint": blueprint,
            "content": content,
            "theme": theme,
            "seo": seo,
            "project_directory": nextjs_result.get("project_dir"),
            "pages_created": nextjs_result.get("pages_created", []),
            "components_created": nextjs_result.get("components_created", [])
        },
        
        # Build info
        "build": {
            "platform": "nextjs",
            "framework_version": "14.2.0",
            "pages_count": len(blueprint["pages"]),
            "components_count": len(blueprint["components_used"]),
            "deployment_status": deployment_result.get("status", "pending")
        },
        
        # Performance metrics
        "metrics": {
            "generation_time_seconds": round(duration, 2),
            "estimated_weekly_savings": 225.0,  # 5 hours @ $45/hr
            "automation_level": "complete"
        }
    }
    
    print(f"   ✅ Artifacts collected and ready for database storage\n")
    
    return artifacts


# =============================================================================
# STEP 10: UPDATE WORKFLOW STATUS + METRICS
# =============================================================================

def update_workflow_status(
    workflow_id: str,
    artifacts: Dict[str, Any],
    estimated_savings: Optional[Dict[str, float]] = None
) -> bool:
    """
    Step 10: Update workflow status in database and record metrics.
    
    This feeds:
    - Leaderboards
    - Analytics
    - Council review history
    """
    print("\n✅ STEP 10: Updating Workflow Status + Metrics...")
    
    try:
        from db import SessionLocal
        from models import Workflow, WorkflowMetric
        
        session = SessionLocal()
        try:
            # Update workflow status
            workflow = session.query(Workflow).filter_by(id=workflow_id).first()
            if workflow:
                workflow.status = "completed"
                workflow.completed_at = datetime.now(timezone.utc)
                workflow.outputs = artifacts
                
                if estimated_savings:
                    workflow.calculated_savings = estimated_savings
                
                session.commit()
                print(f"   ✓ Workflow {workflow_id} marked as completed")
                
                # Record metrics
                metric = WorkflowMetric(
                    workflow_id=workflow_id,
                    metric_name="generation_time",
                    metric_value=artifacts["metrics"]["generation_time_seconds"],
                    recorded_at=datetime.now(timezone.utc)
                )
                session.add(metric)
                
                metric2 = WorkflowMetric(
                    workflow_id=workflow_id,
                    metric_name="weekly_savings",
                    metric_value=artifacts["metrics"]["estimated_weekly_savings"],
                    recorded_at=datetime.now(timezone.utc)
                )
                session.add(metric2)
                
                session.commit()
                print(f"   ✓ Metrics recorded for analytics")
                print(f"   ✅ Workflow status updated successfully\n")
                
                return True
            else:
                print(f"   ⚠️  Workflow {workflow_id} not found in database")
                return False
                
        finally:
            session.close()
            
    except ImportError:
        print(f"   ⚠️  Database models not available - running in standalone mode")
        return False
    except Exception as e:
        print(f"   ⚠️  Database update failed: {str(e)}")
        return False


# =============================================================================
# MASTER ORCHESTRATOR FOR ALL 10 STEPS
# =============================================================================

def execute_complete_workflow(
    site_name: str,
    description: str,
    pages: List[str],
    brand_colors: Dict[str, str],
    typography: Dict[str, str],
    tone: str = "professional",
    platform: str = "nextjs",
    output_dir: str = "./generated_sites",
    github_token: Optional[str] = None,
    vercel_token: Optional[str] = None,
    netlify_token: Optional[str] = None,
    workflow_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Execute complete 10-step website creation workflow.
    
    This is the MASTER function that orchestrates everything from
    blueprint generation to deployment and metrics tracking.
    """
    import time
    from website_creation_execution_complete import (
        generate_site_blueprint,
        generate_page_content,
        generate_seo_metadata,
        generate_brand_theme
    )
    
    print("\n" + "=" * 70)
    print("🔥 CODEX DOMINION - COMPLETE WEBSITE WORKFLOW (10 STEPS) 🔥")
    print("=" * 70)
    print(f"Site: {site_name}")
    print(f"Platform: {platform}")
    print(f"Pages: {len(pages)} pages")
    print("=" * 70 + "\n")
    
    start_time = time.time()
    
    # Create output directory
    site_dir = Path(output_dir) / site_name.lower().replace(" ", "-")
    site_dir.mkdir(parents=True, exist_ok=True)
    
    # STEPS 1-4: Generate JSON artifacts
    blueprint = generate_site_blueprint(site_name, description, pages, platform)
    content = generate_page_content(blueprint, site_name, description, tone)
    seo = generate_seo_metadata(blueprint, content, site_name, description)
    theme = generate_brand_theme(brand_colors, typography)
    
    # STEP 6: Generate Next.js project
    nextjs_result = generate_nextjs_project(blueprint, content, theme, seo, site_name, site_dir)
    
    # STEP 7: Initialize Git
    git_result = initialize_git_repository(
        Path(nextjs_result["project_dir"]),
        site_name,
        create_github_repo=(github_token is not None),
        github_token=github_token
    )
    
    # STEP 8: Deploy
    if vercel_token:
        deployment_result = deploy_to_vercel(
            Path(nextjs_result["project_dir"]),
            site_name,
            vercel_token
        )
    elif netlify_token:
        deployment_result = deploy_to_netlify(
            Path(nextjs_result["project_dir"]),
            site_name,
            netlify_token
        )
    else:
        deployment_result = {"deployed": False, "manual_deployment_required": True}
    
    duration = time.time() - start_time
    
    # STEP 9: Collect artifacts
    final_artifacts = collect_final_artifacts(
        site_name, blueprint, content, theme, seo,
        nextjs_result, git_result, deployment_result, duration
    )
    
    # STEP 10: Update workflow status
    if workflow_id:
        update_workflow_status(
            workflow_id,
            final_artifacts,
            estimated_savings={"weekly": 225.0, "monthly": 900.0, "yearly": 10800.0}
        )
    
    print("\n" + "=" * 70)
    print("🎉 COMPLETE WORKFLOW EXECUTION FINISHED!")
    print("=" * 70)
    print(f"Duration: {duration:.2f}s")
    print(f"Next.js Project: {nextjs_result['project_dir']}")
    if deployment_result.get("url"):
        print(f"Deployed URL: {deployment_result['url']}")
    if git_result.get("github_repo"):
        print(f"GitHub Repo: {git_result['github_repo']}")
    print("=" * 70 + "\n")
    
    return final_artifacts


if __name__ == "__main__":
    # Demo execution
    result = execute_complete_workflow(
        site_name="Demo Site",
        description="A demonstration website",
        pages=["home", "about", "contact"],
        brand_colors={"primary": "#1a1a1a", "secondary": "#f7f1e3", "accent": "#d4af37"},
        typography={"heading": "Inter", "body": "Open Sans"}
    )
    
    print("\n📋 Final Result:")
    print(json.dumps(result, indent=2))

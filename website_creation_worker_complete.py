"""
🔥 CODEX DOMINION - WEBSITE CREATION WORKER 🔥
================================================
Complete worker implementation for website.create_basic_site workflow

This is the RQ worker function that executes the complete 10-step workflow
when triggered by the workflow engine.

Author: Codex Dominion AI Systems
Date: December 20, 2025
"""

import os
import time
from pathlib import Path
from typing import Dict, Any, Optional

from db import SessionLocal
from models import Workflow, WorkflowMetric
from sqlalchemy import func

# Import workflow steps from Steps 6-10
from website_creation_steps_6_to_10 import (
    generate_nextjs_project,
    initialize_git_repository,
    deploy_to_vercel,
    deploy_to_netlify
)


# =============================================================================
# SIMPLE GENERATION FUNCTIONS (Steps 2-5)
# =============================================================================

def generate_site_structure(inputs):
    """Step 2: Generate site structure from inputs"""
    return {
        "site_name": inputs["site_name"],
        "pages": inputs["pages"],
        "navigation": [
            {"label": page.capitalize(), "href": f"/{page if page != 'home' else ''}"}
            for page in inputs["pages"]
        ],
        "layout": {
            "header": True,
            "footer": True,
            "theme": "theme.json"
        }
    }


def generate_page_content(page, inputs):
    """Step 3: Generate content for a single page (LLM placeholder)"""
    # TODO: Replace with your LLM call (GPT-4, Claude, etc.)
    return {
        "title": f"{inputs['site_name']} — {page.capitalize()}",
        "headline": f"Welcome to {inputs['site_name']}",
        "body": f"This is the {page} page for {inputs['site_name']}.",
        "cta": "Learn More"
    }


def generate_seo_metadata(inputs, pages):
    """Step 4: Generate SEO metadata from inputs"""
    return {
        "site_title": inputs["site_name"],
        "description": inputs["description"],
        "pages": {
            page: {
                "title": f"{inputs['site_name']} — {page.capitalize()}",
                "description": f"{inputs['description']} ({page})"
            }
            for page in pages
        }
    }


def generate_theme_file(inputs):
    """Step 5: Generate theme from brand colors and typography"""
    return {
        "colors": inputs["brand_colors"],
        "fonts": {
            "primary": inputs["primary_font"],
            "secondary": inputs["secondary_font"]
        },
        "tone": inputs["tone"]
    }


# =============================================================================
# STEP 6-8 FUNCTIONS (Next.js Scaffolding, Git, Deployment)
# =============================================================================

def scaffold_nextjs_project(site_name, structure, content, theme, seo):
    """
    Step 6: Creates the actual Next.js project folder.
    
    Structure:
      my-site/
        package.json
        next.config.mjs
        tsconfig.json
        postcss.config.mjs
        tailwind.config.mjs
        .gitignore
        /app
          layout.tsx
          page.tsx
          /about
            page.tsx
          /contact
            page.tsx
        /components
          Header.tsx
          Footer.tsx
          Section.tsx
          PageShell.tsx
        /lib
          site.ts
          theme.ts
        /public
          favicon.ico
        /styles
          globals.css
    
    Returns:
        dict with project_path and files_created
    """
    import json
    from pathlib import Path
    
    # Create project directory
    project_name = site_name.lower().replace(" ", "-")
    project_dir = Path("./generated_sites") / project_name
    project_dir.mkdir(parents=True, exist_ok=True)
    
    files_created = []
    
    # ---------------------------------------------------------
    # 1. package.json
    # ---------------------------------------------------------
    package_json = {
        "name": project_name,
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
            "react": "18.2.0",
            "react-dom": "18.2.0"
        },
        "devDependencies": {
            "typescript": "^5.6.0"
        }
    }
    (project_dir / "package.json").write_text(json.dumps(package_json, indent=2), encoding='utf-8')
    files_created.append("package.json")
    
    # ---------------------------------------------------------
    # 2. next.config.mjs
    # ---------------------------------------------------------
    next_config = """/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true
  }
};

export default nextConfig;
"""
    (project_dir / "next.config.mjs").write_text(next_config, encoding='utf-8')
    files_created.append("next.config.mjs")
    
    # ---------------------------------------------------------
    # 3. tsconfig.json
    # ---------------------------------------------------------
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
            "paths": {
                "@/*": ["./*"]
            }
        },
        "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
        "exclude": ["node_modules"]
    }
    (project_dir / "tsconfig.json").write_text(json.dumps(tsconfig, indent=2), encoding='utf-8')
    files_created.append("tsconfig.json")
    
    # ---------------------------------------------------------
    # 4. postcss.config.mjs
    # ---------------------------------------------------------
    postcss_config = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {}
  }
};
"""
    (project_dir / "postcss.config.mjs").write_text(postcss_config, encoding='utf-8')
    files_created.append("postcss.config.mjs")
    
    # ---------------------------------------------------------
    # 5. tailwind.config.mjs
    # ---------------------------------------------------------
    colors = theme.get("colors", {})
    tailwind_config = f"""/** @type {{import('tailwindcss').Config}} */
export default {{
  content: [
    './app/**/*.{{js,ts,jsx,tsx,mdx}}',
    './components/**/*.{{js,ts,jsx,tsx,mdx}}'
  ],
  theme: {{
    extend: {{
      colors: {{
        primary: '{colors.get("primary", "#1a1a1a")}',
        secondary: '{colors.get("secondary", "#f7f1e3")}',
        accent: '{colors.get("accent", "#d4af37")}'
      }}
    }}
  }},
  plugins: []
}};
"""
    (project_dir / "tailwind.config.mjs").write_text(tailwind_config, encoding='utf-8')
    files_created.append("tailwind.config.mjs")
    
    # ---------------------------------------------------------
    # 6. .gitignore
    # ---------------------------------------------------------
    gitignore = """# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# next.js
/.next/
/out/

# production
/build

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
    (project_dir / ".gitignore").write_text(gitignore, encoding='utf-8')
    files_created.append(".gitignore")
    
    # ---------------------------------------------------------
    # 7. /lib/site.ts
    # ---------------------------------------------------------
    lib_dir = project_dir / "lib"
    lib_dir.mkdir(exist_ok=True)
    
    # Build pages object with content
    pages_content = content.get("pages", {})
    
    site_ts = f"""export const siteConfig = {{
  id: "website.create_basic_site",
  name: "{site_name}",
  title: "{site_name}",
  description: "{seo.get("description", "")}",
  navigation: {json.dumps(structure.get("navigation", []), indent=4)},
  pages: {json.dumps(pages_content, indent=4)}
}};
"""
    (lib_dir / "site.ts").write_text(site_ts, encoding='utf-8')
    files_created.append("lib/site.ts")
    
    # ---------------------------------------------------------
    # 8. /lib/theme.ts
    # ---------------------------------------------------------
    colors = theme.get("colors", {})
    fonts = theme.get("fonts", {})
    
    theme_ts = f"""export const theme = {{
  colors: {{
    background: "{colors.get("background", "#020617")}",
    foreground: "{colors.get("foreground", "#F9FAFB")}",
    accent: "{colors.get("accent", "#22C55E")}",
    muted: "{colors.get("muted", "#64748B")}"
  }},
  fonts: {{
    primary: "{fonts.get("primary", "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif")}",
    secondary: "{fonts.get("secondary", "Georgia, 'Times New Roman', serif")}"
  }},
  mode: "{theme.get("tone", "dark")}"
}};
"""
    (lib_dir / "theme.ts").write_text(theme_ts, encoding='utf-8')
    files_created.append("lib/theme.ts")
    
    # ---------------------------------------------------------
    # 9. /components
    # ---------------------------------------------------------
    components_dir = project_dir / "components"
    components_dir.mkdir(exist_ok=True)
    
    # Header.tsx
    header_tsx = """"use client";

import Link from "next/link";
import { siteConfig } from "../lib/site";

export default function Header() {
  return (
    <header className="border-b border-slate-800">
      <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
        <div className="text-lg font-semibold">
          {siteConfig.name}
        </div>
        <nav className="flex gap-4 text-sm text-slate-300">
          {siteConfig.navigation.map(item => (
            <Link key={item.href} href={item.href}>
              {item.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
"""
    (components_dir / "Header.tsx").write_text(header_tsx, encoding='utf-8')
    files_created.append("components/Header.tsx")
    
    # Footer.tsx
    footer_tsx = """export default function Footer() {
  return (
    <footer className="border-t border-slate-800 mt-8">
      <div className="max-w-5xl mx-auto px-4 py-4 text-xs text-slate-500 flex justify-between">
        <span>&copy; {new Date().getFullYear()} Generated by CodexDominion</span>
        <span>Powered by Next.js</span>
      </div>
    </footer>
  );
}
"""
    (components_dir / "Footer.tsx").write_text(footer_tsx, encoding='utf-8')
    files_created.append("components/Footer.tsx")
    
    # Section.tsx
    section_tsx = """export default function Section({
  title,
  subtitle,
  body,
  cta
}: {
  title: string;
  subtitle?: string;
  body: string;
  cta?: string;
}) {
  return (
    <section className="mb-10">
      <h1 className="text-3xl font-bold mb-2">{title}</h1>
      {subtitle && (
        <p className="text-slate-400 mb-3">
          {subtitle}
        </p>
      )}
      <p className="text-slate-200 mb-4">
        {body}
      </p>
      {cta && (
        <button className="inline-flex items-center px-4 py-2 rounded bg-emerald-600 text-sm">
          {cta}
        </button>
      )}
    </section>
  );
}
"""
    (components_dir / "Section.tsx").write_text(section_tsx, encoding='utf-8')
    files_created.append("components/Section.tsx")
    
    # PageShell.tsx
    pageshell_tsx = """import { ReactNode } from 'react';
import { Header } from './Header';
import { Footer } from './Footer';

interface PageShellProps {
  children: ReactNode;
}

export function PageShell({ children }: PageShellProps) {
  return (
    <>
      <Header />
      <main className="min-h-screen">
        {children}
      </main>
      <Footer />
    </>
  );
}
"""
    (components_dir / "PageShell.tsx").write_text(pageshell_tsx, encoding='utf-8')
    files_created.append("components/PageShell.tsx")
    
    # ---------------------------------------------------------
    # 10. /app
    # ---------------------------------------------------------
    app_dir = project_dir / "app"
    app_dir.mkdir(exist_ok=True)
    
    # layout.tsx
    layout_tsx = f"""import "./../styles/globals.css";
import {{ siteConfig }} from "../lib/site";
import {{ theme }} from "../lib/theme";
import Header from "../components/Header";
import Footer from "../components/Footer";

export const metadata = {{
  title: siteConfig.title,
  description: siteConfig.description
}};

export default function RootLayout({{
  children
}}: {{
  children: React.ReactNode;
}}) {{
  return (
    <html lang="en" className={{theme.mode || "light"}}>
      <body
        style={{{{
          fontFamily: theme.fonts?.primary || "system-ui"
        }}}}
        className="min-h-screen flex flex-col bg-slate-950 text-slate-50"
      >
        <Header />
        <main className="flex-1 max-w-5xl mx-auto px-4 py-8">{{children}}</main>
        <Footer />
      </body>
    </html>
  );
}}
"""
    (app_dir / "layout.tsx").write_text(layout_tsx, encoding='utf-8')
    files_created.append("app/layout.tsx")
    
    # Generate pages
    pages = content.get("pages", {})
    for page_name, page_content in pages.items():
        if page_name == "home":
            # Home page at root
            page_tsx = f"""import Section from "../components/Section";
import {{ siteConfig }} from "../lib/site";

export default function HomePage() {{
  const page = siteConfig.pages.home;
  return (
    <Section
      title={{page.title}}
      subtitle={{page.headline}}
      body={{page.body}}
      cta={{page.cta}}
    />
  );
}}
"""
            (app_dir / "page.tsx").write_text(page_tsx, encoding='utf-8')
            files_created.append("app/page.tsx")
        else:
            # Other pages in subdirectories
            page_dir = app_dir / page_name
            page_dir.mkdir(exist_ok=True)
            
            page_tsx = f"""import Section from "../../components/Section";
import {{ siteConfig }} from "../../lib/site";

export default function {page_name.capitalize()}Page() {{
  const page = siteConfig.pages.{page_name};
  return (
    <Section
      title={{page.title}}
      subtitle={{page.headline}}
      body={{page.body}}
      cta={{page.cta}}
    />
  );
}}
"""
            (page_dir / "page.tsx").write_text(page_tsx, encoding='utf-8')
            files_created.append(f"app/{page_name}/page.tsx")
    
    # API health route
    api_dir = app_dir / "api" / "health"
    api_dir.mkdir(parents=True, exist_ok=True)
    
    health_route = """import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({ status: 'ok' });
}
"""
    (api_dir / "route.ts").write_text(health_route, encoding='utf-8')
    files_created.append("app/api/health/route.ts")
    
    # ---------------------------------------------------------
    # 11. /styles/globals.css
    # ---------------------------------------------------------
    styles_dir = project_dir / "styles"
    styles_dir.mkdir(exist_ok=True)
    
    globals_css = """*,
*::before,
*::after {
  box-sizing: border-box;
}

html,
body {
  padding: 0;
  margin: 0;
}

body {
  background-color: #020617;
  color: #e5e7eb;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

a {
  color: inherit;
  text-decoration: none;
}

button {
  cursor: pointer;
}
"""
    (styles_dir / "globals.css").write_text(globals_css, encoding='utf-8')
    files_created.append("styles/globals.css")
    
    # ---------------------------------------------------------
    # 12. /public/favicon.ico (empty placeholder)
    # ---------------------------------------------------------
    public_dir = project_dir / "public"
    public_dir.mkdir(exist_ok=True)
    (public_dir / "favicon.ico").touch()
    files_created.append("public/favicon.ico")
    
    return {
        "project_path": str(project_dir),
        "files_created": files_created
    }


def push_to_github(site_name, project_path):
    """
    Step 7: Creates a repo + pushes code.
    
    Uses:
    - GitHub API
    - PyGithub
    - Or a simple subprocess call to git
    
    Returns:
        GitHub repo URL
    """
    from github_service import create_repo, commit_and_push
from vercel_service import create_or_link_project, trigger_deployment, get_latest_deployment_url
    
    # Create repo
    repo_url = create_repo(site_name)
    
    # Push files
    commit_and_push(repo_url, project_path)
    
    return repo_url.replace(f"https://{os.getenv('GITHUB_TOKEN')}@", "https://")


def deploy_to_vercel_or_netlify(platform, repo_url, project_path):
    """
    Step 8: Triggers deployment.
    
    Uses:
    - Vercel REST API
    - Netlify REST API
    
    Returns:
        Deployed URL
    """
    if platform == "vercel":
        site_name = Path(project_path).name
        
        # Create/link Vercel project
        project_id = create_or_link_project(repo_url, site_name)
        
        # Trigger deployment
        deployment_id = trigger_deployment(project_id, repo_url)
        
        # Wait for deployment and get URL
        deployed_url = get_latest_deployment_url(project_id)
        
        return deployed_url
    
    elif platform == "netlify":
        netlify_token = os.getenv("NETLIFY_TOKEN")
        if not netlify_token:
            return None
        
        result = deploy_to_netlify(
            project_dir=Path(project_path),
            site_name=Path(project_path).name,
            token=netlify_token
        )
        return result.get("url")
    
    return None


# =============================================================================
# MAIN WORKER FUNCTION
# =============================================================================

def execute_website_creation(workflow_id: str) -> Dict[str, Any]:
    """
    Executes the website.create_basic_site workflow.
    
    Steps:
    1. Load workflow + inputs from DB
    2. Generate site structure JSON (Blueprint)
    3. Generate page content (AI-authored)
    4. Generate SEO metadata
    5. Generate theme file
    6. Scaffold Next.js project (React components)
    7. Commit to GitHub
    8. Trigger deployment (Vercel/Netlify)
    9. Save artifacts + update workflow status
    10. Record metrics for analytics
    
    Args:
        workflow_id: Workflow database ID
        
    Returns:
        Complete artifacts dictionary with URLs and metadata
    """
    
    session = SessionLocal()
    start_time = time.time()
    
    print(f"\n{'='*70}")
    print(f"🔥 EXECUTING WEBSITE CREATION WORKFLOW: {workflow_id}")
    print(f"{'='*70}\n")

    try:
        # ---------------------------------------------------------
        # STEP 1: Load workflow + inputs from database
        # ---------------------------------------------------------
        print("📋 STEP 1: Loading workflow from database...")
        workflow = session.query(Workflow).filter(Workflow.id == workflow_id).first()
        if not workflow:
            print(f"   ❌ Workflow {workflow_id} not found")
            return {"error": "Workflow not found"}

        # Mark as in progress
        workflow.status = "in_progress"
        workflow.started_at = func.now()
        session.commit()
        
        inputs = workflow.inputs or {}
        print(f"   ✓ Workflow loaded")
        print(f"   ✓ Site: {inputs.get('site_name', 'Unnamed')}")
        print(f"   ✓ Pages: {len(inputs.get('pages', []))} pages")
        print(f"   ✓ Platform: {inputs.get('platform', 'nextjs')}\n")
        
        # Extract inputs with defaults
        site_name = inputs.get("site_name", "Untitled Site")
        description = inputs.get("description", "A beautiful website")
        pages = inputs.get("pages", ["home", "about", "contact"])
        platform = inputs.get("platform", "nextjs")
        tone = inputs.get("tone", "professional")
        
        brand_colors = inputs.get("brand_colors", {
            "primary": "#1a1a1a",
            "secondary": "#f7f1e3",
            "accent": "#d4af37"
        })
        
        typography = inputs.get("typography", {
            "heading": "Inter",
            "body": "Open Sans"
        })
        
        # Optional tokens
        github_token = inputs.get("github_token") or os.getenv("GITHUB_TOKEN")
        vercel_token = inputs.get("vercel_token") or os.getenv("VERCEL_TOKEN")
        netlify_token = inputs.get("netlify_token") or os.getenv("NETLIFY_TOKEN")
        
        # Output directory
        output_base = inputs.get("output_dir", "./generated_sites")
        output_dir = Path(output_base) / site_name.lower().replace(" ", "-")
        output_dir.mkdir(parents=True, exist_ok=True)

        # ---------------------------------------------------------
        # STEP 2: Generate site structure JSON
        # ---------------------------------------------------------
        print("🏗️  STEP 2: Generating Site Structure...")
        site_structure = generate_site_structure(inputs)
        
        # Save to disk
        (output_dir / "site.json").write_text(
            __import__("json").dumps(site_structure, indent=2),
            encoding='utf-8'
        )
        print(f"   ✅ Structure: {len(site_structure['pages'])} pages, {len(site_structure['navigation'])} nav items\n")

        # ---------------------------------------------------------
        # STEP 3: Generate page content (AI-authored)
        # ---------------------------------------------------------
        print("✍️  STEP 3: Generating Page Content...")
        content = {
            "pages": {
                page: generate_page_content(page, inputs)
                for page in pages
            }
        }
        
        # Save to disk
        (output_dir / "content.json").write_text(
            __import__("json").dumps(content, indent=2),
            encoding='utf-8'
        )
        print(f"   ✅ Content: {len(content['pages'])} pages generated\n")

        # ---------------------------------------------------------
        # STEP 4: Generate SEO metadata
        # ---------------------------------------------------------
        print("🔍 STEP 4: Generating SEO Metadata...")
        seo = generate_seo_metadata(inputs, pages)
        
        # Save to disk
        (output_dir / "seo.json").write_text(
            __import__("json").dumps(seo, indent=2),
            encoding='utf-8'
        )
        print(f"   ✅ SEO: {len(seo['pages'])} pages\n")

        # ---------------------------------------------------------
        # STEP 5: Generate theme file
        # ---------------------------------------------------------
        print("🎨 STEP 5: Generating Brand Theme...")
        theme = generate_theme_file(inputs)
        
        # Save to disk
        (output_dir / "theme.json").write_text(
            __import__("json").dumps(theme, indent=2),
            encoding='utf-8'
        )
        (output_dir / "theme.css").write_text(theme["css_variables"], encoding='utf-8')
        print(f"   ✅ Theme: Colors, typography, spacing system\n")

        # ---------------------------------------------------------
        # STEP 6: Scafsite_structure.js project (React components)
        # ---------------------------------------------------------
        print("⚛️  STEP 6: Scaffolding Next.js Project...")
        nextjs_result = generate_nextjs_project(
            blueprint=blueprint,
            content=content,
            theme=theme,
            seo=seo,
            site_name=site_name,
            output_dir=output_dir
        )
        project_path = Path(nextjs_result["project_dir"])
        print(f"   ✅ Next.js: {len(nextjs_result['pages_created'])} pages, {len(nextjs_result['components_created'])} components\n")

        # ---------------------------------------------------------
        # STEP 7: Commit to GitHub
        # ---------------------------------------------------------
        print("📦 STEP 7: Initializing Git Repository...")
        git_result = initialize_git_repository(
            project_dir=project_path,
            site_name=site_name,
            create_github_repo=(github_token is not None),
            github_token=github_token
        )
        repo_url = git_result.get("github_repo")
        if repo_url:
            print(f"   ✅ GitHub: {repo_url}\n")
        else:
            print(f"   ✓ Local Git initialized (no GitHub token provided)\n")

        # ---------------------------------------------------------
        # STEP 8: Trigger deployment (Vercel/Netlify)
        # ---------------------------------------------------------
        print("🚀 STEP 8: Deploying Website...")
        deployment_result = {}
        
        if vercel_token:
            deployment_result = deploy_to_vercel(project_path, site_name, vercel_token)
        elif netlify_token:
            deployment_result = deploy_to_netlify(project_path, site_name, netlify_token)
        else:
            print(f"   ⚠️  No deployment tokens - skipping deployment")
            print(f"   💡 To deploy manually:")
            print(f"      cd {project_path}")
            print(f"      npm install && npm run build")
            print(f"      vercel deploy  # or netlify deploy\n")
            deployment_result = {
                "deployed": False,
                "manual_deployment_required": True
            }
        
        deployed_url = deployment_result.get("url")
        
        if deployed_url:
            print(f"   ✅ Deployed: {deployed_url}\n")
        else:
            print(f"   ⚠️  No deployment tokens - skipping deployment")
            print(f"   💡 To deploy manually:")
            print(f"      cd {project_path}")
            print(f"      npm install && npm run build")
            print(f"      vercel deploy  # or netlify deploy\n")

        # ---------------------------------------------------------
        # STEP 9: Collect final artifacts
        # ---------------------------------------------------------
        duration = time.time() - start_time
        
        print("📊 STEP 9: Collecting Final Artifacts...")
        final_artifacts = {
            "site_name": site_name,
            "project_path": str(project_path),
            "repo_url": repo_url,
            "deployed_url": deployed_url,
            "duration_seconds": duration,
            "files_created": nextjs_result["files_created"],
            "status": "success"
        }

        # ---------------------------------------------------------
        # STEP 10: Update workflow status + metrics
        # ---------------------------------------------------------
        print("✅ STEP 10: Updating Workflow Status...")
        
        workflow.status = "completed"
        workflow.completed_at = func.now()
        workflow.outputs = final_artifacts
        
        # Update calculated savings with URLs
        if not workflow.calculated_savings:
            workflow.calculated_savings = {}
        
        workflow.calculated_savings["deployed_url"] = deployed_url
        workflow.calculated_savings["repo_url"] = repo_url
        workflow.calculated_savings["project_directory"] = str(project_path)
        workflow.calculated_savings["duration_seconds"] = duration
        
        # Record metrics
        metric = WorkflowMetric(
            workflow_id=workflow_id,
            metric_name="generation_time",
            metric_value=duration,
            recorded_at=func.now()
        )
        session.add(metric)
        
        metric2 = WorkflowMetric(
            workflow_id=workflow_id,
            metric_name="weekly_savings",
            metric_value=225.0,  # 5 hours @ $45/hr
            recorded_at=func.now()
        )
        session.add(metric2)
        
        session.commit()
        print(f"   ✓ Workflow marked as completed")
        print(f"   ✓ Metrics recorded\n")

        # ---------------------------------------------------------
        # FINAL SUMMARY
        # ---------------------------------------------------------
        print(f"{'='*70}")
        print(f"🎉 WORKFLOW EXECUTION COMPLETE!")
        print(f"{'='*70}")
        print(f"Duration: {duration:.2f}s")
        print(f"Status: ✅ SUCCESS")
        print(f"\n📦 Outputs:")
        print(f"   • Project: {project_path}")
        if repo_url:
            print(f"   • GitHub: {repo_url}")
        if deployed_url:
            print(f"   • Deployed: {deployed_url}")
        print(f"{'='*70}\n")
        
        return final_artifacts

    except Exception as e:
        # Handle errors
        print(f"\n❌ ERROR: {str(e)}")
        
        session.rollback()
        workflow.status = "failed"
        workflow.completed_at = func.now()
        workflow.outputs = {
            "error": str(e),
            "status": "failed"
        }
        session.commit()
        
        raise

    finally:
        session.close()


# =============================================================================
# HELPER FUNCTIONS FOR RQ WORKER INTEGRATION
# =============================================================================

def enqueue_website_creation(workflow_id: str) -> str:
    """
    Enqueue website creation workflow to RQ worker.
    
    Usage:
        from website_creation_worker_complete import enqueue_website_creation
        job_id = enqueue_website_creation("workflow_12345")
    """
    from rq import Queue
    from redis import Redis
    
    redis_conn = Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        db=int(os.getenv("REDIS_DB", 0))
    )
    
    queue = Queue("workflows", connection=redis_conn)
    
    job = queue.enqueue(
        execute_website_creation,
        workflow_id,
        job_timeout="30m",  # 30 minutes max
        result_ttl=86400    # Keep result for 24 hours
    )
    
    print(f"✅ Job enqueued: {job.id}")
    return job.id


def get_job_status(job_id: str) -> Dict[str, Any]:
    """
    Get status of enqueued job.
    
    Returns:
        dict with keys: status, result, exc_info
    """
    from rq.job import Job
    from redis import Redis
    
    redis_conn = Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        db=int(os.getenv("REDIS_DB", 0))
    )
    
    job = Job.fetch(job_id, connection=redis_conn)
    
    return {
        "status": job.get_status(),
        "result": job.result if job.is_finished else None,
        "error": job.exc_info if job.is_failed else None
    }


# =============================================================================
# STANDALONE EXECUTION (FOR TESTING)
# =============================================================================

if __name__ == "__main__":
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Execute website creation workflow")
    parser.add_argument("--workflow-id", required=True, help="Workflow ID from database")
    parser.add_argument("--enqueue", action="store_true", help="Enqueue to RQ instead of direct execution")
    
    args = parser.parse_args()
    
    if args.enqueue:
        job_id = enqueue_website_creation(args.workflow_id)
        print(f"\n✅ Job enqueued: {job_id}")
        print(f"   Monitor with: rq info")
    else:
        result = execute_website_creation(args.workflow_id)
        print("\n📋 Final Result:")
        print(json.dumps(result, indent=2))

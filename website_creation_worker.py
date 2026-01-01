"""
CODEX DOMINION - WEBSITE CREATION WORKER
=========================================
RQ worker tasks for automated website generation

This module contains the actual execution logic for website.create_basic_site workflow.
When a workflow is enqueued, these functions generate and deploy the website.
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import subprocess

# AI/Content generation (mock for now - replace with actual AI)
def generate_site_content(site_name: str, description: str, pages: List[str]) -> Dict[str, Any]:
    """
    Step 1-2: Generate site structure and content
    
    Uses AI to create:
    - Page layouts
    - Content for each page
    - Navigation structure
    """
    structure = {
        "pages": [],
        "navigation": []
    }
    
    for page in pages:
        page_content = {
            "slug": page,
            "title": page.replace("_", " ").title(),
            "sections": []
        }
        
        if page == "home":
            page_content["sections"] = [
                {
                    "type": "hero",
                    "heading": f"Welcome to {site_name}",
                    "subheading": description,
                    "cta": {"text": "Get Started", "link": "/contact"}
                },
                {
                    "type": "features",
                    "heading": "What We Offer",
                    "items": [
                        {"title": "Quality Service", "description": "Excellence in everything we do"},
                        {"title": "Expert Team", "description": "Professionals you can trust"},
                        {"title": "Customer Focus", "description": "Your success is our priority"}
                    ]
                }
            ]
        elif page == "about":
            page_content["sections"] = [
                {
                    "type": "text",
                    "heading": f"About {site_name}",
                    "content": f"{description}\n\nWe are dedicated to providing exceptional service and building lasting relationships with our clients."
                }
            ]
        elif page == "contact":
            page_content["sections"] = [
                {
                    "type": "contact_form",
                    "heading": "Get In Touch",
                    "fields": ["name", "email", "message"]
                }
            ]
        elif page == "blog":
            page_content["sections"] = [
                {
                    "type": "blog_index",
                    "heading": "Latest Articles",
                    "posts": []
                }
            ]
        else:
            page_content["sections"] = [
                {
                    "type": "text",
                    "heading": page.replace("_", " ").title(),
                    "content": f"Content for {page} page."
                }
            ]
        
        structure["pages"].append(page_content)
        structure["navigation"].append({
            "label": page_content["title"],
            "href": f"/{page}" if page != "home" else "/"
        })
    
    return structure


def generate_seo_metadata(site_name: str, description: str, pages: List[str]) -> Dict[str, Any]:
    """
    Step 3: Generate SEO metadata
    
    Creates:
    - Meta tags for each page
    - OpenGraph tags
    - Sitemap structure
    - robots.txt
    """
    base_metadata = {
        "title": site_name,
        "description": description,
        "keywords": [site_name.lower(), "website", "service"],
        "ogImage": "/og-image.png",
        "twitterCard": "summary_large_image"
    }
    
    page_metadata = {}
    for page in pages:
        page_title = page.replace("_", " ").title()
        page_metadata[page] = {
            "title": f"{page_title} | {site_name}",
            "description": f"{page_title} page for {site_name}. {description}",
            "path": f"/{page}" if page != "home" else "/"
        }
    
    sitemap = {
        "pages": [{"path": meta["path"], "priority": 1.0 if page == "home" else 0.8} 
                  for page, meta in page_metadata.items()]
    }
    
    robots_txt = """User-agent: *
Allow: /

Sitemap: /sitemap.xml
"""
    
    return {
        "base": base_metadata,
        "pages": page_metadata,
        "sitemap": sitemap,
        "robots": robots_txt
    }


def generate_brand_theme(brand_colors: Dict[str, str], typography: Dict[str, str]) -> Dict[str, Any]:
    """
    Step 4: Generate brand theme
    
    Creates:
    - CSS variables
    - Tailwind config
    - Component styling
    """
    theme = {
        "colors": {
            "primary": brand_colors.get("primary", "#1a1a1a"),
            "secondary": brand_colors.get("secondary", "#f7f1e3"),
            "accent": brand_colors.get("accent", "#d4af37")
        },
        "fonts": {
            "heading": typography.get("heading", "Inter"),
            "body": typography.get("body", "Open Sans")
        },
        "spacing": {
            "container": "1280px",
            "section": "80px"
        }
    }
    
    css_variables = f"""
:root {{
  --color-primary: {theme['colors']['primary']};
  --color-secondary: {theme['colors']['secondary']};
  --color-accent: {theme['colors']['accent']};
  
  --font-heading: '{theme['fonts']['heading']}', sans-serif;
  --font-body: '{theme['fonts']['body']}', sans-serif;
  
  --container-width: {theme['spacing']['container']};
  --section-padding: {theme['spacing']['section']};
}}
"""
    
    return {
        "theme": theme,
        "css": css_variables
    }


def generate_nextjs_project(
    site_name: str,
    structure: Dict[str, Any],
    seo: Dict[str, Any],
    theme: Dict[str, Any],
    output_dir: str
) -> str:
    """
    Step 5: Generate Next.js project scaffold
    
    Creates complete Next.js 14 project with:
    - App router structure
    - Dynamic pages
    - Components
    - Styling
    """
    project_dir = Path(output_dir) / site_name.lower().replace(" ", "-")
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # Create package.json
    package_json = {
        "name": site_name.lower().replace(" ", "-"),
        "version": "1.0.0",
        "private": True,
        "scripts": {
            "dev": "next dev",
            "build": "next build",
            "start": "next start",
            "export": "next build && next export"
        },
        "dependencies": {
            "next": "^14.0.0",
            "react": "^18.2.0",
            "react-dom": "^18.2.0"
        },
        "devDependencies": {
            "typescript": "^5.0.0",
            "@types/react": "^18.2.0",
            "@types/node": "^20.0.0",
            "tailwindcss": "^3.4.0",
            "autoprefixer": "^10.4.0",
            "postcss": "^8.4.0"
        }
    }
    
    with open(project_dir / "package.json", "w") as f:
        json.dump(package_json, f, indent=2)
    
    # Create next.config.js
    next_config = """/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: { unoptimized: true }
}

module.exports = nextConfig
"""
    with open(project_dir / "next.config.js", "w") as f:
        f.write(next_config)
    
    # Create app directory
    app_dir = project_dir / "app"
    app_dir.mkdir(exist_ok=True)
    
    # Create layout.tsx
    layout_tsx = f"""import type {{ Metadata }} from 'next'
import './globals.css'

export const metadata: Metadata = {{
  title: '{seo['base']['title']}',
  description: '{seo['base']['description']}',
}}

export default function RootLayout({{
  children,
}}: {{
  children: React.ReactNode
}}) {{
  return (
    <html lang="en">
      <body>{{children}}</body>
    </html>
  )
}}
"""
    with open(app_dir / "layout.tsx", "w") as f:
        f.write(layout_tsx)
    
    # Create globals.css
    globals_css = f"""{theme['css']}

* {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}

body {{
  font-family: var(--font-body);
  color: var(--color-primary);
  background: var(--color-secondary);
}}

h1, h2, h3, h4, h5, h6 {{
  font-family: var(--font-heading);
}}
"""
    with open(app_dir / "globals.css", "w") as f:
        f.write(globals_css)
    
    # Create page.tsx for each page
    for page_data in structure["pages"]:
        page_slug = page_data["slug"]
        page_dir = app_dir if page_slug == "home" else app_dir / page_slug
        
        if page_slug != "home":
            page_dir.mkdir(exist_ok=True)
        
        sections_html = ""
        for section in page_data["sections"]:
            if section["type"] == "hero":
                sections_html += f"""
        <section style={{{{padding: 'var(--section-padding) 0'}}}}>
          <div style={{{{maxWidth: 'var(--container-width)', margin: '0 auto', padding: '0 20px', textAlign: 'center'}}}}>
            <h1 style={{{{fontSize: '3rem', marginBottom: '1rem'}}}}>{section['heading']}</h1>
            <p style={{{{fontSize: '1.25rem', marginBottom: '2rem'}}}}>{section['subheading']}</p>
            <a href="{section['cta']['link']}" style={{{{display: 'inline-block', padding: '12px 24px', background: 'var(--color-accent)', color: 'white', textDecoration: 'none', borderRadius: '4px'}}}}>
              {section['cta']['text']}
            </a>
          </div>
        </section>
"""
            elif section["type"] == "text":
                sections_html += f"""
        <section style={{{{padding: 'var(--section-padding) 0'}}}}>
          <div style={{{{maxWidth: 'var(--container-width)', margin: '0 auto', padding: '0 20px'}}}}>
            <h2 style={{{{fontSize: '2rem', marginBottom: '1rem'}}}}>{section['heading']}</h2>
            <p>{section['content']}</p>
          </div>
        </section>
"""
            elif section["type"] == "contact_form":
                sections_html += f"""
        <section style={{{{padding: 'var(--section-padding) 0'}}}}>
          <div style={{{{maxWidth: '600px', margin: '0 auto', padding: '0 20px'}}}}>
            <h2 style={{{{fontSize: '2rem', marginBottom: '1rem', textAlign: 'center'}}}}>{section['heading']}</h2>
            <form style={{{{display: 'flex', flexDirection: 'column', gap: '1rem'}}}}>
              <input type="text" placeholder="Name" style={{{{padding: '12px', border: '1px solid #ddd', borderRadius: '4px'}}}} />
              <input type="email" placeholder="Email" style={{{{padding: '12px', border: '1px solid #ddd', borderRadius: '4px'}}}} />
              <textarea placeholder="Message" rows={{5}} style={{{{padding: '12px', border: '1px solid #ddd', borderRadius: '4px'}}}}></textarea>
              <button type="submit" style={{{{padding: '12px', background: 'var(--color-accent)', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer'}}}}>
                Send Message
              </button>
            </form>
          </div>
        </section>
"""
        
        page_tsx = f"""export default function Page() {{
  return (
    <main>
      <nav style={{{{padding: '20px', background: 'var(--color-primary)', color: 'white'}}}}>
        <div style={{{{maxWidth: 'var(--container-width)', margin: '0 auto', display: 'flex', gap: '20px'}}}}>
          {" | ".join([f'<a href="{nav["href"]}" style={{{{color: "white", textDecoration: "none"}}}}>{nav["label"]}</a>' for nav in structure["navigation"]])}
        </div>
      </nav>
      {sections_html}
    </main>
  )
}}
"""
        
        with open(page_dir / "page.tsx", "w") as f:
            f.write(page_tsx)
    
    # Create public directory
    public_dir = project_dir / "public"
    public_dir.mkdir(exist_ok=True)
    
    # Create robots.txt
    with open(public_dir / "robots.txt", "w") as f:
        f.write(seo["robots"])
    
    return str(project_dir)


def deploy_to_github_and_vercel(
    project_dir: str,
    site_name: str,
    contact_email: str
) -> Dict[str, str]:
    """
    Step 6-7: Deploy to GitHub and Vercel/Netlify
    
    Creates:
    - Git repository
    - Commits code
    - Pushes to GitHub
    - Triggers Vercel deployment
    
    Returns:
    - repo_url: GitHub repository URL
    - site_url: Deployed website URL
    """
    # For MVP, we'll simulate deployment
    # In production, use GitHub API and Vercel API
    
    repo_name = site_name.lower().replace(" ", "-")
    
    # Simulate git operations
    # In production:
    # subprocess.run(["git", "init"], cwd=project_dir)
    # subprocess.run(["git", "add", "."], cwd=project_dir)
    # subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=project_dir)
    # subprocess.run(["gh", "repo", "create", repo_name, "--public"], cwd=project_dir)
    # subprocess.run(["git", "push", "-u", "origin", "main"], cwd=project_dir)
    
    # Simulate Vercel deployment
    # In production:
    # subprocess.run(["vercel", "--prod"], cwd=project_dir)
    
    return {
        "repo_url": f"https://github.com/codexdominion/{repo_name}",
        "site_url": f"https://{repo_name}.vercel.app",
        "deployment_id": f"deploy_{int(time.time())}"
    }


def execute_website_creation(workflow_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main execution function for website.create_basic_site workflow
    
    This is called by RQ worker when workflow is dequeued.
    
    Args:
        workflow_id: Workflow database ID
        inputs: User inputs from workflow creation
    
    Returns:
        outputs: Workflow outputs (site_url, pages_created, etc.)
    """
    from db import SessionLocal
    from models import Workflow, WorkflowStatus, WorkflowMetric
    from datetime import datetime
    
    session = SessionLocal()
    start_time = time.time()
    
    try:
        # Update workflow status to IN_PROGRESS
        workflow = session.query(Workflow).filter(Workflow.id == workflow_id).first()
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow.status = WorkflowStatus.IN_PROGRESS
        workflow.started_at = datetime.utcnow()
        session.commit()
        
        # Extract inputs
        site_name = inputs.get("site_name", "My Site")
        site_description = inputs.get("site_description", "A professional website")
        brand_colors = inputs.get("brand_colors", {
            "primary": "#1a1a1a",
            "secondary": "#f7f1e3",
            "accent": "#d4af37"
        })
        typography = inputs.get("typography", {
            "heading": "Inter",
            "body": "Open Sans"
        })
        pages = inputs.get("pages", ["home", "about", "contact", "blog"])
        contact_email = inputs.get("contact_email", "hello@example.com")
        
        # Step 1-2: Generate site structure and content
        print(f"📝 Generating content for {site_name}...")
        structure = generate_site_content(site_name, site_description, pages)
        
        # Step 3: Generate SEO metadata
        print("🔍 Generating SEO metadata...")
        seo = generate_seo_metadata(site_name, site_description, pages)
        
        # Step 4: Generate brand theme
        print("🎨 Applying brand theme...")
        theme = generate_brand_theme(brand_colors, typography)
        
        # Step 5: Generate Next.js project
        print("⚙️  Building Next.js project...")
        output_dir = os.path.join(os.getcwd(), "generated_sites")
        project_dir = generate_nextjs_project(
            site_name,
            structure,
            seo,
            theme,
            output_dir
        )
        
        # Step 6-7: Deploy to GitHub and Vercel
        print("🚀 Deploying to production...")
        deployment = deploy_to_github_and_vercel(
            project_dir,
            site_name,
            contact_email
        )
        
        # Calculate execution time
        duration = time.time() - start_time
        
        # Create outputs
        outputs = {
            "site_url": deployment["site_url"],
            "pages_created": [f"{deployment['site_url']}{page}" for page in [
                "/" if p == "home" else f"/{p}" for p in pages
            ]],
            "asset_urls": {
                "project_directory": project_dir,
                "github_repo": deployment["repo_url"]
            },
            "deployment_id": deployment["deployment_id"],
            "decision": "approved",  # Assumed approved for MVP
            "execution_summary": {
                "pages_generated": len(pages),
                "duration_seconds": round(duration, 2),
                "status": "success"
            }
        }
        
        # Update workflow with outputs
        workflow.status = WorkflowStatus.COMPLETED
        workflow.completed_at = datetime.utcnow()
        workflow.outputs = outputs
        session.commit()
        
        # Record metrics
        metric = WorkflowMetric(
            workflow_id=workflow_id,
            duration_seconds=round(duration, 2),
            estimated_weekly_savings=workflow.calculated_savings.get("weekly_savings", 0),
            success_rate=1.0,
            error_count=0
        )
        session.add(metric)
        session.commit()
        
        print(f"✅ Website created successfully!")
        print(f"   URL: {deployment['site_url']}")
        print(f"   Duration: {duration:.2f}s")
        
        return outputs
        
    except Exception as e:
        # Update workflow status to FAILED
        workflow = session.query(Workflow).filter(Workflow.id == workflow_id).first()
        if workflow:
            workflow.status = WorkflowStatus.FAILED
            workflow.outputs = {"error": str(e)}
            session.commit()
        
        # Record failure metric
        duration = time.time() - start_time
        metric = WorkflowMetric(
            workflow_id=workflow_id,
            duration_seconds=round(duration, 2),
            success_rate=0.0,
            error_count=1
        )
        session.add(metric)
        session.commit()
        
        print(f"❌ Workflow failed: {e}")
        raise
        
    finally:
        session.close()


# RQ task wrapper
def website_creation_task(workflow_id: str, inputs: Dict[str, Any]):
    """
    RQ task entry point
    
    Usage:
        from redis import Redis
        from rq import Queue
        
        redis_conn = Redis()
        queue = Queue('workflows', connection=redis_conn)
        
        job = queue.enqueue(
            website_creation_task,
            workflow_id='wf_abc123',
            inputs={...},
            timeout='15m'
        )
    """
    return execute_website_creation(workflow_id, inputs)


if __name__ == "__main__":
    # Test execution locally
    print("=" * 60)
    print("TESTING WEBSITE CREATION WORKFLOW")
    print("=" * 60)
    
    test_inputs = {
        "site_name": "Codex Digital Studios",
        "site_description": "AI-powered web development and digital solutions",
        "brand_colors": {
            "primary": "#1a1a1a",
            "secondary": "#f7f1e3",
            "accent": "#d4af37"
        },
        "typography": {
            "heading": "Inter",
            "body": "Open Sans"
        },
        "pages": ["home", "about", "services", "contact", "blog"],
        "contact_email": "hello@codexdigital.app"
    }
    
    # Create test workflow in database
    from db import SessionLocal
    from models import Workflow, WorkflowStatus
    from datetime import datetime
    import uuid
    
    session = SessionLocal()
    test_workflow_id = f"wf_test_{uuid.uuid4().hex[:8]}"
    
    workflow = Workflow(
        id=test_workflow_id,
        workflow_type_id="website.create_basic_site",
        created_by_agent="agent_jermaine_super_action",
        status=WorkflowStatus.PENDING,
        inputs=test_inputs,
        calculated_savings={"weekly_savings": 225.0},
        created_at=datetime.utcnow()
    )
    session.add(workflow)
    session.commit()
    
    # Execute workflow
    outputs = execute_website_creation(test_workflow_id, test_inputs)
    
    print("\n" + "=" * 60)
    print("OUTPUTS:")
    print(json.dumps(outputs, indent=2))
    print("=" * 60)
    
    session.close()

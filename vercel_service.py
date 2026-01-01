import os
import time
import json
import requests

VERCEL_TOKEN = os.getenv("VERCEL_TOKEN")
VERCEL_TEAM_ID = os.getenv("VERCEL_TEAM_ID")  # optional
VERCEL_SCOPE = os.getenv("VERCEL_SCOPE")      # optional

BASE_URL = "https://api.vercel.com"


def _headers():
    return {
        "Authorization": f"Bearer {VERCEL_TOKEN}",
        "Content-Type": "application/json"
    }


def _query_params():
    params = {}
    if VERCEL_TEAM_ID:
        params["teamId"] = VERCEL_TEAM_ID
    if VERCEL_SCOPE:
        params["scope"] = VERCEL_SCOPE
    return params


# =============================================================================
# 1. CREATE OR LINK PROJECT
# =============================================================================

def create_or_link_project(repo_url: str, project_name: str) -> str:
    """
    Creates a Vercel project or links an existing one to the given repo.
    Returns project ID.
    """
    payload = {
        "name": project_name,
        "framework": "nextjs",
        "gitRepository": {
            "type": "github",
            "repo": extract_repo_slug(repo_url)  # e.g. user/repo
        }
    }

    resp = requests.post(
        f"{BASE_URL}/v9/projects",
        params=_query_params(),
        headers=_headers(),
        data=json.dumps(payload)
    )

    if resp.status_code not in (200, 201):
        # If project already exists, try fetching it
        if resp.status_code == 409:  # conflict, likely exists
            existing = get_project_by_name(project_name)
            if not existing:
                raise RuntimeError(f"Vercel: failed to create or fetch project: {resp.text}")
            return existing["id"]
        raise RuntimeError(f"Vercel project creation failed: {resp.status_code} {resp.text}")

    data = resp.json()
    return data["id"]


def get_project_by_name(name: str):
    resp = requests.get(
        f"{BASE_URL}/v9/projects",
        params={**_query_params(), "search": name},
        headers=_headers()
    )
    if resp.status_code != 200:
        return None
    items = resp.json().get("projects", [])
    for p in items:
        if p.get("name") == name:
            return p
    return None


def extract_repo_slug(repo_url: str) -> str:
    """
    Converts git https URL into 'owner/repo' form.
    Example: https://github.com/owner/repo.git -> owner/repo
    """
    clean = repo_url.replace(".git", "")
    parts = clean.split("/")
    if len(parts) < 2:
        return clean
    owner = parts[-2]
    repo = parts[-1]
    return f"{owner}/{repo}"


def trigger_deployment(project_id: str, repo_url: str) -> str:
    """
    Triggers a deployment for the given project.
    Returns deployment ID.
    """
    payload = {
        "name": None,  # use project name
        "projectId": project_id
    }

    resp = requests.post(
        f"{BASE_URL}/v13/deployments",
        params=_query_params(),
        headers=_headers(),
        data=json.dumps(payload)
    )

    if resp.status_code not in (200, 202):
        raise RuntimeError(f"Vercel deployment failed: {resp.status_code} {resp.text}")

    data = resp.json()
    return data["id"]


def get_latest_deployment_url(project_id: str, timeout_seconds: int = 300) -> str:
    """
    Polls Vercel for the latest deployment's URL until ready or timeout.
    """
    start = time.time()

    while time.time() - start < timeout_seconds:
        resp = requests.get(
            f"{BASE_URL}/v6/deployments",
            params={**_query_params(), "projectId": project_id, "limit": 1},
            headers=_headers()
        )
        if resp.status_code != 200:
            time.sleep(5)
            continue

        deployments = resp.json().get("deployments", [])
        if not deployments:
            time.sleep(5)
            continue

        d = deployments[0]
        state = d.get("state")
        url = d.get("url")

        if state in ("READY", "READY_TO_FUNCTION"):
            return f"https://{url}"
        elif state in ("ERROR", "CANCELED"):
            raise RuntimeError(f"Vercel deployment error: {state}")

        time.sleep(5)

    raise TimeoutError("Timed out waiting for Vercel deployment.")


# =============================================================================
# 4. SET ENVIRONMENT VARIABLES
# =============================================================================

def set_env_vars(project_id: str, env_vars: dict):
    """
    Sets environment variables for a Vercel project.
    
    Args:
        project_id: Vercel project ID
        env_vars: Dict of environment variables (e.g., {"API_KEY": "secret"})
        
    Returns:
        bool: Success status
    """
    url = f"{BASE_URL}/v9/projects/{project_id}/env"
    
    for key, value in env_vars.items():
        payload = {
            "key": key,
            "value": value,
            "type": "encrypted",
            "target": ["production", "preview", "development"]
        }
        
        response = requests.post(url, headers=_headers(), params=_query_params(), json=payload)
        
        if response.status_code in [200, 201]:
            print(f"✅ Set env var: {key}")
        else:
            print(f"⚠️  Failed to set {key}: {response.text}")
    
    return True


# =============================================================================
# CONVENIENCE WRAPPER
# =============================================================================

def deploy_to_vercel(repo_url: str, project_name: str, env_vars: dict = None):
    """
    Complete deployment flow: create project + trigger deployment + wait for URL.
    
    Args:
        repo_url: GitHub repo URL
        project_name: Project name
        env_vars: Optional environment variables
        
    Returns:
        dict with keys: project_id, deployment_url, ready
    """
    # Step 1: Create/link project
    project = create_or_link_project(repo_url, project_name)
    
    # Step 2: Set env vars (optional)
    if env_vars:
        set_env_vars(project["project_id"], env_vars)
    
    # Step 3: Trigger deployment
    deployment = trigger_deployment(project["project_id"], repo_url)
    
    # Step 4: Wait for deployment URL
    deployment_url = get_latest_deployment_url(project["project_id"], wait_for_ready=True)
    
    return {
        "project_id": project["project_id"],
        "deployment_url": deployment_url,
        "ready": True
    }


# =============================================================================
# TESTING
# =============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Vercel Deployment Service CLI")
    parser.add_argument("command", choices=["create", "deploy", "status"], help="Command to execute")
    parser.add_argument("--repo", help="GitHub repo URL")
    parser.add_argument("--project", help="Project name or ID")
    
    args = parser.parse_args()
    
    if args.command == "create":
        result = create_or_link_project(args.repo, args.project)
        print(f"\n✅ Project: {result['project_name']}")
        print(f"   URL: {result['url']}")
        
    elif args.command == "deploy":
        result = deploy_to_vercel(args.repo, args.project)
        print(f"\n✅ Deployed: {result['deployment_url']}")
        
    elif args.command == "status":
        url = get_latest_deployment_url(args.project, wait_for_ready=False)
        print(f"\n📊 Latest deployment: {url}")

"""
🔥 CODEX DOMINION - GITHUB INTEGRATION SERVICE 🔥
===================================================
High-Level GitHub API for Workflow Engine

This module is the "bridge" between CodexDominion and your external digital empire.

Author: Codex Dominion AI Systems
Date: December 20, 2025
"""

import os
import subprocess
from github import Github

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_ORG = os.getenv("GITHUB_ORG")  # optional

gh = Github(GITHUB_TOKEN)


def create_repo(repo_name: str):
    """
    Creates a GitHub repo and returns the clone URL.
    """
    if GITHUB_ORG:
        org = gh.get_organization(GITHUB_ORG)
        repo = org.create_repo(repo_name, private=True)
    else:
        user = gh.get_user()
        repo = user.create_repo(repo_name, private=True)

    return repo.clone_url.replace("https://", f"https://{GITHUB_TOKEN}@")


def commit_and_push(repo_url: str, project_path: str):
    """
    Initializes git, commits all files, and pushes to GitHub.
    """
    subprocess.run(["git", "init"], cwd=project_path)
    subprocess.run(["git", "add", "."], cwd=project_path)
    subprocess.run(["git", "commit", "-m", "Initial commit from CodexDominion"], cwd=project_path)
    subprocess.run(["git", "branch", "-M", "main"], cwd=project_path)
    subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=project_path)
    subprocess.run(["git", "push", "-u", "origin", "main"], cwd=project_path)

    return True

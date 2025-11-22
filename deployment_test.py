#!/usr/bin/env python3
"""
Codex Dominion - Cloud Deployment Readiness Test
===============================================

Tests all components required for Google Cloud Run deployment.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def test_file_exists(filepath, description):
    """Test if a required file exists."""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (MISSING)")
        return False

def test_python_import(module_name, description):
    """Test if a Python module can be imported."""
    try:
        __import__(module_name)
        print(f"✅ {description}: {module_name}")
        return True
    except ImportError:
        print(f"⚠️  {description}: {module_name} (optional)")
        return True  # Don't fail for optional modules
    except Exception as e:
        print(f"❌ {description}: {module_name} - {e}")
        return False

def test_command_available(command, description):
    """Test if a command is available."""
    try:
        result = subprocess.run([command, "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ {description}: {command}")
            return True
        else:
            print(f"❌ {description}: {command} (not working)")
            return False
    except FileNotFoundError:
        print(f"❌ {description}: {command} (not installed)")
        return False
    except Exception as e:
        print(f"❌ {description}: {command} - {e}")
        return False

def test_gcloud_config():
    """Test gcloud configuration."""
    try:
        # Test if project is set
        result = subprocess.run(["gcloud", "config", "get-value", "project"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and result.stdout.strip():
            project_id = result.stdout.strip()
            print(f"✅ GCloud Project: {project_id}")
            return True, project_id
        else:
            print(f"⚠️  GCloud Project: Not configured")
            return False, None
    except Exception as e:
        print(f"❌ GCloud Config Error: {e}")
        return False, None

def test_codex_system():
    """Test Codex system functionality."""
    try:
        # Test unified launcher
        from codex_unified_launcher import CodexUnifiedLauncher
        launcher = CodexUnifiedLauncher()
        print("✅ Codex Unified Launcher: Ready")
        
        # Test treasury system
        if launcher.treasury:
            print("✅ Treasury System: Operational")
        else:
            print("✅ Treasury System: JSON-only mode")
        
        return True
    except Exception as e:
        print(f"❌ Codex System Error: {e}")
        return False

def main():
    """Run all deployment readiness tests."""
    print("🔥 Codex Dominion - Cloud Deployment Readiness Test")
    print("=" * 55)
    print()
    
    all_passed = True
    
    # Test required files
    print("📁 REQUIRED FILES:")
    print("-" * 20)
    files_to_test = [
        ("Dockerfile", "Docker Configuration"),
        ("requirements.txt", "Python Dependencies"),
        ("cloudbuild.yaml", "Cloud Build Config"),
        ("codex_unified_launcher.py", "Unified Launcher"),
        ("codex_treasury_database.py", "Treasury System"),
        ("codex_ledger.json", "Ledger Data")
    ]
    
    for filepath, description in files_to_test:
        if not test_file_exists(filepath, description):
            all_passed = False
    
    print()
    
    # Test Python modules
    print("🐍 PYTHON MODULES:")
    print("-" * 20)
    modules_to_test = [
        ("flask", "Web Server"),
        ("json", "JSON Processing"),
        ("datetime", "Date/Time"),
        ("argparse", "CLI Arguments"),
        ("pathlib", "File Paths")
    ]
    
    for module_name, description in modules_to_test:
        if not test_python_import(module_name, description):
            all_passed = False
    
    print()
    
    # Test external commands
    print("🛠️  EXTERNAL TOOLS:")
    print("-" * 20)
    commands_to_test = [
        ("docker", "Docker Engine"),
        ("gcloud", "Google Cloud CLI")
    ]
    
    for command, description in commands_to_test:
        if not test_command_available(command, description):
            if command == "gcloud":
                print("   📝 Install: https://cloud.google.com/sdk/docs/install")
            all_passed = False
    
    print()
    
    # Test gcloud configuration
    print("☁️  CLOUD CONFIGURATION:")
    print("-" * 25)
    gcloud_ok, project_id = test_gcloud_config()
    if not gcloud_ok:
        print("   📝 Configure: gcloud auth login && gcloud config set project YOUR_PROJECT_ID")
    
    print()
    
    # Test Codex system
    print("🔥 CODEX SYSTEM:")
    print("-" * 15)
    codex_ok = test_codex_system()
    if not codex_ok:
        all_passed = False
    
    print()
    
    # Summary
    print("📋 DEPLOYMENT READINESS SUMMARY:")
    print("=" * 35)
    
    if all_passed and gcloud_ok:
        print("✅ READY FOR DEPLOYMENT!")
        print(f"🚀 Project ID: {project_id}")
        print("🔥 Run deployment:")
        print(f"   gcloud builds submit --tag gcr.io/{project_id}/codex-backend")
        print(f"   gcloud run deploy codex-backend --image gcr.io/{project_id}/codex-backend \\")
        print("     --platform managed --region us-central1 --allow-unauthenticated \\")
        print("     --memory 512Mi --cpu 1 --port 8080")
        
    elif all_passed:
        print("⚠️  ALMOST READY - Configure gcloud:")
        print("   gcloud auth login")
        print("   gcloud config set project YOUR_PROJECT_ID")
        
    else:
        print("❌ NOT READY - Fix the issues above first")
    
    print()
    print("📚 For detailed instructions, see: DEPLOYMENT_GUIDE.md")
    
    return all_passed and gcloud_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
#!/usr/bin/env python3
"""
🔥 CODEX SIGNALS CONTAINER VALIDATION 📊
Validate container setup without requiring Docker

The Merritt Method™ - Pre-Container Validation
"""

import os
import sys

def validate_container_setup():
    """Validate all container files are present and correct"""
    print("🔥 CODEX SIGNALS CONTAINER VALIDATION 📊")
    print("=" * 45)
    
    validation_results = []
    
    # Check required files
    required_files = [
        ("main.py", "Main application entry point"),
        ("requirements.txt", "Python dependencies"),
        ("codex_signals/Dockerfile", "Container definition"),
        ("codex_signals/.dockerignore", "Docker ignore rules"),
        ("codex_signals/docker-compose.yml", "Local development setup"),
        ("codex_signals/api.py", "FastAPI application"),
        ("codex_signals/engine.py", "Signals engine"),
        ("codex_signals/integration.py", "Integration layer"),
        ("deploy_signals_container.ps1", "Deployment script")
    ]
    
    print("📁 Checking required files...")
    for filepath, description in required_files:
        if os.path.exists(filepath):
            print(f"✅ {description}: {filepath}")
            validation_results.append(True)
        else:
            print(f"❌ {description}: {filepath} (MISSING)")
            validation_results.append(False)
    
    # Validate main.py content
    print("\n🔍 Validating main.py...")
    try:
        with open("main.py", 'r') as f:
            main_content = f.read()
            
        if "from codex_signals.api import app" in main_content:
            print("✅ Main app import found")
            validation_results.append(True)
        else:
            print("❌ Main app import missing")
            validation_results.append(False)
            
        if "uvicorn.run" in main_content:
            print("✅ Uvicorn server setup found")
            validation_results.append(True)
        else:
            print("❌ Uvicorn server setup missing")
            validation_results.append(False)
            
    except Exception as e:
        print(f"❌ Error reading main.py: {e}")
        validation_results.append(False)
    
    # Validate Dockerfile
    print("\n🐳 Validating Dockerfile...")
    try:
        with open("codex_signals/Dockerfile", 'r') as f:
            dockerfile_content = f.read()
            
        docker_checks = [
            ("FROM python:3.11-slim", "Base image"),
            ("COPY requirements.txt", "Requirements copy"),
            ("RUN pip install", "Dependencies install"),
            ("COPY codex_signals/", "Source code copy"),
            ("CMD [\"uvicorn\"", "Uvicorn command")
        ]
        
        for check, description in docker_checks:
            if check in dockerfile_content:
                print(f"✅ {description}")
                validation_results.append(True)
            else:
                print(f"❌ {description} missing")
                validation_results.append(False)
                
    except Exception as e:
        print(f"❌ Error reading Dockerfile: {e}")
        validation_results.append(False)
    
    # Validate requirements.txt
    print("\n📦 Validating requirements.txt...")
    try:
        with open("requirements.txt", 'r') as f:
            requirements_content = f.read()
            
        required_packages = [
            "fastapi",
            "uvicorn",
            "pandas",
            "numpy",
            "requests"
        ]
        
        for package in required_packages:
            if package in requirements_content.lower():
                print(f"✅ {package} dependency found")
                validation_results.append(True)
            else:
                print(f"❌ {package} dependency missing")
                validation_results.append(False)
                
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        validation_results.append(False)
    
    # Summary
    total_checks = len(validation_results)
    passed_checks = sum(validation_results)
    
    print("\n" + "=" * 45)
    print(f"🎯 VALIDATION RESULTS: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("✅ CONTAINER SETUP VALIDATION PASSED")
        print("\n🚀 Ready for deployment:")
        print("1. Local test: .\\deploy_signals_container.ps1 -ProjectId test -LocalTest")
        print("2. Cloud deploy: .\\deploy_signals_container.ps1 -ProjectId YOUR_PROJECT_ID")
        print("3. Docker compose: docker-compose -f codex_signals/docker-compose.yml up")
        return True
    else:
        print("❌ CONTAINER SETUP VALIDATION FAILED")
        print(f"\n🔧 Fix {total_checks - passed_checks} issues above before deployment")
        return False

if __name__ == "__main__":
    success = validate_container_setup()
    sys.exit(0 if success else 1)
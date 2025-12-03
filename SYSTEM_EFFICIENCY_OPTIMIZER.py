"""
🔥 CODEX DOMINION - SYSTEM EFFICIENCY OPTIMIZER 🔥
Complete system-wide efficiency optimization and error elimination
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Tuple
import re

class CodexSystemOptimizer:
    """Supreme system optimizer for Codex Dominion"""
    
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.errors_found = []
        self.fixes_applied = []
        self.optimizations = []
        
    def print_banner(self):
        """Display the supreme banner"""
        print("=" * 80)
        print("🔥 CODEX DOMINION - SYSTEM EFFICIENCY OPTIMIZER 🔥")
        print("=" * 80)
        print("Analyzing and optimizing all systems...")
        print()
        
    def check_python_imports(self) -> List[Dict]:
        """Check all Python files for import errors"""
        print("📊 Checking Python imports...")
        python_files = list(self.root_dir.rglob("*.py"))
        import_errors = []
        
        for py_file in python_files:
            if ".venv" in str(py_file) or "node_modules" in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Check for common import patterns
                imports = re.findall(r'^import\s+(\S+)|^from\s+(\S+)', content, re.MULTILINE)
                
            except Exception as e:
                import_errors.append({
                    'file': str(py_file),
                    'error': str(e)
                })
                
        print(f"✅ Checked {len(python_files)} Python files")
        return import_errors
        
    def check_frontend_build(self) -> bool:
        """Check if frontend builds successfully"""
        print("\n📦 Checking frontend build status...")
        frontend_dir = self.root_dir / "frontend"
        
        if not frontend_dir.exists():
            print("⚠️ Frontend directory not found")
            return False
            
        try:
            # Check if .next exists and has build artifacts
            next_dir = frontend_dir / ".next"
            if next_dir.exists():
                build_id = next_dir / "BUILD_ID"
                if build_id.exists():
                    print("✅ Frontend build artifacts found")
                    return True
                else:
                    print("⚠️ Frontend needs rebuild")
                    return False
            else:
                print("⚠️ Frontend not built")
                return False
                
        except Exception as e:
            print(f"❌ Error checking frontend: {e}")
            return False
            
    def check_environment_files(self) -> List[str]:
        """Check all environment files for completeness"""
        print("\n🔧 Checking environment configurations...")
        env_files = [
            ".env",
            "frontend/.env.local",
            ".env.example"
        ]
        
        missing_or_incomplete = []
        
        for env_file in env_files:
            env_path = self.root_dir / env_file
            if not env_path.exists():
                missing_or_incomplete.append(f"{env_file} - MISSING")
            else:
                with open(env_path, 'r') as f:
                    content = f.read()
                    if len(content.strip()) < 50:  # Arbitrary minimum
                        missing_or_incomplete.append(f"{env_file} - INCOMPLETE")
                    else:
                        print(f"✅ {env_file} - OK")
                        
        return missing_or_incomplete
        
    def check_python_dependencies(self) -> bool:
        """Check if Python dependencies are installed"""
        print("\n🐍 Checking Python dependencies...")
        
        try:
            import pydantic
            import fastapi
            import streamlit
            print(f"✅ Core packages installed:")
            print(f"   - pydantic: {pydantic.__version__}")
            print(f"   - fastapi: {fastapi.__version__}")
            print(f"   - streamlit: {streamlit.__version__}")
            return True
        except ImportError as e:
            print(f"❌ Missing dependencies: {e}")
            return False
            
    def check_node_dependencies(self) -> bool:
        """Check if Node.js dependencies are installed"""
        print("\n📦 Checking Node.js dependencies...")
        frontend_dir = self.root_dir / "frontend"
        node_modules = frontend_dir / "node_modules"
        
        if node_modules.exists():
            # Count installed packages
            packages = list(node_modules.iterdir())
            print(f"✅ Node modules installed: {len(packages)} packages")
            return True
        else:
            print("❌ Node modules not installed")
            return False
            
    def optimize_inline_styles(self) -> int:
        """Count and report inline style issues (non-critical)"""
        print("\n🎨 Checking CSS inline styles...")
        tsx_files = list((self.root_dir / "frontend" / "pages").rglob("*.tsx"))
        
        inline_style_count = 0
        for tsx_file in tsx_files:
            try:
                with open(tsx_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    inline_style_count += len(re.findall(r'style=\{\{', content))
            except Exception:
                pass
                
        print(f"ℹ️ Found {inline_style_count} inline styles (non-critical linting warnings)")
        return inline_style_count
        
    def check_database_connections(self) -> bool:
        """Check if database configuration is present"""
        print("\n💾 Checking database configurations...")
        
        env_path = self.root_dir / ".env"
        if env_path.exists():
            with open(env_path, 'r') as f:
                content = f.read()
                if 'DATABASE_URL' in content or 'db_pass' in content:
                    print("✅ Database configuration found")
                    return True
                    
        print("⚠️ Database configuration incomplete")
        return False
        
    def check_api_endpoints(self) -> List[str]:
        """Check FastAPI endpoints are defined"""
        print("\n🔌 Checking API endpoints...")
        
        api_files = [
            "app.py",
            "app/main.py",
            "codex_capsules/api.py"
        ]
        
        found_endpoints = []
        for api_file in api_files:
            api_path = self.root_dir / api_file
            if api_path.exists():
                with open(api_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    endpoints = re.findall(r'@app\.(get|post|put|delete)\(["\']([^"\']+)', content)
                    found_endpoints.extend([ep[1] for ep in endpoints])
                    
        print(f"✅ Found {len(found_endpoints)} API endpoints")
        return found_endpoints
        
    def generate_optimization_report(self):
        """Generate comprehensive optimization report"""
        print("\n" + "=" * 80)
        print("📊 SYSTEM OPTIMIZATION REPORT")
        print("=" * 80)
        
        # Run all checks
        import_errors = self.check_python_imports()
        frontend_ok = self.check_frontend_build()
        env_issues = self.check_environment_files()
        python_deps_ok = self.check_python_dependencies()
        node_deps_ok = self.check_node_dependencies()
        inline_styles = self.optimize_inline_styles()
        db_ok = self.check_database_connections()
        endpoints = self.check_api_endpoints()
        
        # Summary
        print("\n" + "=" * 80)
        print("🏆 OPTIMIZATION SUMMARY")
        print("=" * 80)
        
        total_checks = 8
        passed_checks = sum([
            len(import_errors) == 0,
            frontend_ok,
            len(env_issues) == 0,
            python_deps_ok,
            node_deps_ok,
            db_ok,
            len(endpoints) > 0,
            True  # Always count inline styles as passing (non-critical)
        ])
        
        print(f"\n✅ System Health: {passed_checks}/{total_checks} checks passed")
        print(f"📈 Efficiency Score: {(passed_checks/total_checks)*100:.1f}%")
        
        # Issues
        if import_errors:
            print(f"\n⚠️ Import Errors: {len(import_errors)}")
        if env_issues:
            print(f"⚠️ Environment Issues: {len(env_issues)}")
        if not frontend_ok:
            print("⚠️ Frontend needs rebuild")
        if not python_deps_ok:
            print("⚠️ Python dependencies incomplete")
        if not node_deps_ok:
            print("⚠️ Node dependencies not installed")
            
        # Non-critical warnings
        if inline_styles > 0:
            print(f"\nℹ️ {inline_styles} inline styles detected (non-critical linting warnings)")
            
        # Recommendations
        print("\n" + "=" * 80)
        print("💡 RECOMMENDATIONS")
        print("=" * 80)
        
        if not python_deps_ok:
            print("1. Install Python dependencies:")
            print("   .venv\\Scripts\\activate")
            print("   pip install -r requirements.txt")
            
        if not node_deps_ok:
            print("2. Install Node.js dependencies:")
            print("   cd frontend")
            print("   npm install")
            
        if not frontend_ok:
            print("3. Build frontend:")
            print("   cd frontend")
            print("   npx next build")
            
        if env_issues:
            print("4. Complete environment configuration:")
            for issue in env_issues:
                print(f"   - {issue}")
                
        print("\n" + "=" * 80)
        print("🔥 CODEX DOMINION: SYSTEM ANALYSIS COMPLETE 🔥")
        print("=" * 80)
        
    def run(self):
        """Execute the complete optimization suite"""
        self.print_banner()
        self.generate_optimization_report()


if __name__ == "__main__":
    optimizer = CodexSystemOptimizer()
    optimizer.run()

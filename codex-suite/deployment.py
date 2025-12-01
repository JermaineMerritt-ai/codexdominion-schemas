#!/usr/bin/env python3
"""
Deployment Configuration & Health Checks
========================================

Production deployment utilities for the Codex Dominion Suite.
"""

import asyncio
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


# Health Check System
class HealthChecker:
    """System health monitoring and diagnostics"""

    def __init__(self):
        self.checks = {}
        self.last_check_time = None
        self.health_status = "unknown"

    async def check_dependencies(self) -> Dict[str, Any]:
        """Check if all required dependencies are installed"""
        required_packages = [
            "streamlit",
            "fastapi",
            "uvicorn",
            "pydantic",
            "python-dotenv",
            "redis",
            "requests",
            "faiss-cpu",
        ]

        results = {"status": "healthy", "issues": [], "installed": []}

        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
                results["installed"].append(package)
            except ImportError:
                results["issues"].append(f"Missing package: {package}")
                results["status"] = "unhealthy"

        return results

    async def check_redis_connection(self) -> Dict[str, Any]:
        """Check Redis connection status"""
        try:
            import redis

            r = redis.Redis(host="127.0.0.1", port=6379, db=0, socket_timeout=5)
            r.ping()
            return {
                "status": "healthy",
                "connected": True,
                "host": "127.0.0.1",
                "port": 6379,
            }
        except Exception as e:
            return {
                "status": "warning",
                "connected": False,
                "error": str(e),
                "recommendation": "Redis is optional but improves performance",
            }

    async def check_file_system(self) -> Dict[str, Any]:
        """Check file system permissions and structure"""
        base_path = Path(__file__).parent.parent
        required_dirs = ["apps", "core", "data", "modules", "static"]

        results = {"status": "healthy", "issues": [], "directories": []}

        for dir_name in required_dirs:
            dir_path = base_path / dir_name
            if dir_path.exists() and dir_path.is_dir():
                results["directories"].append(str(dir_path))
            else:
                results["issues"].append(f"Missing directory: {dir_path}")
                results["status"] = "unhealthy"

        # Check write permissions
        try:
            test_file = base_path / "data" / ".write_test"
            test_file.write_text("test")
            test_file.unlink()
        except Exception as e:
            results["issues"].append(f"Write permission error: {e}")
            results["status"] = "unhealthy"

        return results

    async def check_ports(self) -> Dict[str, Any]:
        """Check if required ports are available"""
        import socket

        required_ports = [8531, 8000]  # Streamlit and FastAPI
        results = {"status": "healthy", "available_ports": [], "occupied_ports": []}

        for port in required_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.bind(("127.0.0.1", port))
                results["available_ports"].append(port)
                sock.close()
            except OSError:
                results["occupied_ports"].append(port)
                if port in [8531, 8000]:  # Critical ports
                    results["status"] = "warning"

        return results

    async def run_full_health_check(self) -> Dict[str, Any]:
        """Run comprehensive health check"""
        self.last_check_time = datetime.now()

        checks = {
            "dependencies": await self.check_dependencies(),
            "redis": await self.check_redis_connection(),
            "filesystem": await self.check_file_system(),
            "ports": await self.check_ports(),
            "timestamp": self.last_check_time.isoformat(),
        }

        # Determine overall health
        statuses = [
            check.get("status", "unknown")
            for check in checks.values()
            if isinstance(check, dict)
        ]
        if "unhealthy" in statuses:
            self.health_status = "unhealthy"
        elif "warning" in statuses:
            self.health_status = "warning"
        else:
            self.health_status = "healthy"

        checks["overall_status"] = self.health_status
        self.checks = checks

        return checks


class DeploymentManager:
    """Manage deployment configurations and startup"""

    def __init__(self):
        self.config_path = Path(__file__).parent.parent / "deployment.json"
        self.health_checker = HealthChecker()

    def generate_deployment_config(self) -> Dict[str, Any]:
        """Generate deployment configuration"""
        config = {
            "application": {
                "name": "Codex Dominion Suite",
                "version": "1.0.0",
                "environment": "production",
            },
            "services": {
                "dashboard": {
                    "command": "streamlit run apps/codex_dashboard.py --server.port 8531",
                    "port": 8531,
                    "health_check": "/health",
                    "auto_restart": True,
                },
                "api": {
                    "command": "uvicorn main:app --host 0.0.0.0 --port 8000",
                    "port": 8000,
                    "health_check": "/health",
                    "auto_restart": True,
                },
            },
            "dependencies": {
                "python_version": ">=3.8",
                "packages": [
                    "streamlit>=1.28.0",
                    "fastapi>=0.104.0",
                    "uvicorn[standard]>=0.24.0",
                    "pydantic>=2.4.0",
                    "python-dotenv>=1.0.0",
                    "redis>=5.0.0",
                    "requests>=2.31.0",
                    "faiss-cpu>=1.7.4",
                ],
            },
            "optional_services": {
                "redis": {
                    "enabled": False,
                    "host": "127.0.0.1",
                    "port": 6379,
                    "benefit": "Improves performance with caching",
                }
            },
            "security": {
                "allowed_hosts": ["127.0.0.1", "localhost"],
                "cors_enabled": True,
                "api_key_required": False,
            },
            "monitoring": {
                "health_checks": True,
                "performance_tracking": True,
                "log_level": "INFO",
            },
        }

        return config

    def save_deployment_config(self):
        """Save deployment configuration to file"""
        config = self.generate_deployment_config()
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=2)

        print(f"✅ Deployment config saved to: {self.config_path}")
        return config

    def load_deployment_config(self) -> Optional[Dict[str, Any]]:
        """Load deployment configuration from file"""
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                return json.load(f)
        return None

    def install_dependencies(self, upgrade: bool = False):
        """Install required dependencies"""
        config = self.generate_deployment_config()
        packages = config["dependencies"]["packages"]

        for package in packages:
            try:
                cmd = [sys.executable, "-m", "pip", "install"]
                if upgrade:
                    cmd.append("--upgrade")
                cmd.append(package)

                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ Installed: {package}")
                else:
                    print(f"⚠️  Failed to install {package}: {result.stderr}")

            except Exception as e:
                print(f"❌ Error installing {package}: {e}")

    async def start_service(self, service_name: str, background: bool = True):
        """Start a specific service"""
        config = self.load_deployment_config() or self.generate_deployment_config()

        if service_name not in config["services"]:
            print(f"❌ Unknown service: {service_name}")
            return False

        service_config = config["services"][service_name]
        command = service_config["command"]

        try:
            if background:
                process = subprocess.Popen(
                    command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                print(f"🚀 Started {service_name} (PID: {process.pid})")
                return process
            else:
                subprocess.run(command.split())

        except Exception as e:
            print(f"❌ Failed to start {service_name}: {e}")
            return False

    async def deploy_full_system(self):
        """Deploy the complete system"""
        print("🚀 Deploying Codex Dominion Suite...")

        # Run health checks
        print("\n📋 Running health checks...")
        health_results = await self.health_checker.run_full_health_check()

        if health_results["overall_status"] == "unhealthy":
            print("❌ System is not healthy for deployment")
            self._print_health_issues(health_results)
            return False

        # Save deployment config
        print("\n📝 Generating deployment configuration...")
        self.save_deployment_config()

        # Install dependencies if needed
        if health_results["dependencies"]["status"] != "healthy":
            print("\n📦 Installing missing dependencies...")
            self.install_dependencies()

        print("\n✅ System ready for deployment!")
        print("\nTo start services manually:")
        print("  Dashboard: streamlit run apps/codex_dashboard.py --server.port 8531")
        print("  API: uvicorn main:app --host 0.0.0.0 --port 8000")

        return True

    def _print_health_issues(self, health_results: Dict[str, Any]):
        """Print health check issues"""
        for check_name, results in health_results.items():
            if isinstance(results, dict) and "issues" in results and results["issues"]:
                print(f"\n{check_name.upper()} Issues:")
                for issue in results["issues"]:
                    print(f"  ❌ {issue}")


class StartupScript:
    """Automated startup script for the Codex Dominion Suite"""

    @staticmethod
    async def quick_start():
        """Quick start with basic health checks"""
        print("🚀 Codex Dominion Suite - Quick Start")
        print("=" * 50)

        # Basic dependency check
        try:
            import streamlit

            print("✅ Streamlit available")
        except ImportError:
            print("❌ Streamlit not installed - run: pip install streamlit")
            return

        # Start dashboard
        print("\n🎯 Starting Codex Dashboard...")
        os.chdir(Path(__file__).parent.parent)

        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "streamlit",
                    "run",
                    "apps/codex_dashboard.py",
                    "--server.port",
                    "8531",
                ]
            )
        except KeyboardInterrupt:
            print("\n👋 Codex Dominion Suite stopped")

    @staticmethod
    async def full_deployment():
        """Full deployment with comprehensive checks"""
        deployment_manager = DeploymentManager()
        success = await deployment_manager.deploy_full_system()

        if success:
            print("\n🎯 Starting services...")
            # Start dashboard in foreground for now
            await deployment_manager.start_service("dashboard", background=False)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "health":
            # Health check only
            async def run_health():
                checker = HealthChecker()
                results = await checker.run_full_health_check()
                print(json.dumps(results, indent=2))

            asyncio.run(run_health())

        elif sys.argv[1] == "deploy":
            # Full deployment
            asyncio.run(StartupScript.full_deployment())

        elif sys.argv[1] == "install":
            # Install dependencies
            manager = DeploymentManager()
            manager.install_dependencies(upgrade=True)

        else:
            print("Usage: python deployment.py [health|deploy|install]")
    else:
        # Quick start
        asyncio.run(StartupScript.quick_start())

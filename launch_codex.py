#!/usr/bin/env python3
"""
Codex Dominion Suite - Master Launcher
======================================

Unified launcher for all Codex Dominion systems and services.
Provides intelligent startup, monitoring, and management capabilities.
"""

import sys
import os
import asyncio
import subprocess
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add the codex-suite to Python path
sys.path.insert(0, str(Path(__file__).parent / "codex-suite"))

class CodexLauncher:
    """Master launcher for the Codex Dominion Suite"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.codex_path = self.base_path / "codex-suite"
        self.processes = {}
        self.startup_log = []
        
        # Ensure we're in the right directory
        os.chdir(self.codex_path)
    
    def log_message(self, message: str, level: str = "INFO"):
        """Log startup messages"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.startup_log.append(log_entry)
        print(log_entry)
    
    def check_python_environment(self) -> bool:
        """Verify Python environment is suitable"""
        self.log_message("Checking Python environment...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            self.log_message(f"Python 3.8+ required, found {sys.version_info}", "ERROR")
            return False
        
        self.log_message(f"Python {sys.version_info.major}.{sys.version_info.minor} ✅")
        return True
    
    def check_dependencies(self) -> Dict[str, bool]:
        """Check if required dependencies are installed"""
        self.log_message("Checking dependencies...")
        
        dependencies = {
            "streamlit": False,
            "fastapi": False,
            "uvicorn": False,
            "pydantic": False,
            "python-dotenv": False,
            "redis": False,
            "requests": False,
            "faiss-cpu": False
        }
        
        for package in dependencies:
            try:
                __import__(package.replace("-", "_"))
                dependencies[package] = True
                self.log_message(f"  ✅ {package}")
            except ImportError:
                self.log_message(f"  ❌ {package}", "WARN")
        
        return dependencies
    
    def install_missing_dependencies(self, missing: List[str]):
        """Install missing dependencies"""
        if not missing:
            return
        
        self.log_message(f"Installing {len(missing)} missing packages...")
        
        for package in missing:
            try:
                self.log_message(f"Installing {package}...")
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", package
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.log_message(f"  ✅ {package} installed")
                else:
                    self.log_message(f"  ❌ Failed to install {package}", "ERROR")
                    
            except Exception as e:
                self.log_message(f"  ❌ Error installing {package}: {e}", "ERROR")
    
    def setup_environment(self):
        """Set up the runtime environment"""
        self.log_message("Setting up environment...")
        
        # Create necessary directories
        directories = ["data", "static", "logs"]
        for dir_name in directories:
            dir_path = self.codex_path / dir_name
            dir_path.mkdir(exist_ok=True)
            self.log_message(f"  📁 {dir_name} directory ready")
    
    def start_service(self, name: str, command: List[str], port: int = None) -> Optional[subprocess.Popen]:
        """Start a service process"""
        try:
            self.log_message(f"Starting {name}...")
            
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.codex_path
            )
            
            self.processes[name] = {
                "process": process,
                "command": command,
                "port": port,
                "start_time": datetime.now()
            }
            
            # Give it a moment to start
            time.sleep(2)
            
            if process.poll() is None:  # Still running
                port_info = f" on port {port}" if port else ""
                self.log_message(f"  ✅ {name} started{port_info} (PID: {process.pid})")
                return process
            else:
                self.log_message(f"  ❌ {name} failed to start", "ERROR")
                return None
                
        except Exception as e:
            self.log_message(f"  ❌ Error starting {name}: {e}", "ERROR")
            return None
    
    def check_service_health(self, name: str) -> bool:
        """Check if a service is running healthy"""
        if name not in self.processes:
            return False
        
        process_info = self.processes[name]
        process = process_info["process"]
        
        # Check if process is still running
        if process.poll() is not None:
            self.log_message(f"  ⚠️  {name} process stopped", "WARN")
            return False
        
        return True
    
    def launch_codex_dashboard(self) -> bool:
        """Launch the Codex Dashboard"""
        command = [
            sys.executable, "-m", "streamlit", "run",
            "apps/codex_dashboard.py",
            "--server.port", "8531",
            "--server.address", "0.0.0.0"
        ]
        
        process = self.start_service("Codex Dashboard", command, 8531)
        return process is not None
    
    def launch_api_server(self) -> bool:
        """Launch the FastAPI server"""
        command = [
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ]
        
        process = self.start_service("API Server", command, 8000)
        return process is not None
    
    def launch_technical_operations_council(self) -> bool:
        """Launch the enhanced Technical Operations Council"""
        # First check if the file exists in the parent directory
        council_path = self.base_path / "technical_operations_council.py"
        if council_path.exists():
            command = [
                sys.executable, "-m", "streamlit", "run",
                str(council_path),
                "--server.port", "8532"
            ]
            
            process = self.start_service("Technical Operations Council", command, 8532)
            return process is not None
        else:
            self.log_message("Technical Operations Council not found", "WARN")
            return False
    
    def display_startup_summary(self):
        """Display startup summary and access information"""
        self.log_message("🚀 CODEX DOMINION SUITE - STARTUP COMPLETE")
        print("=" * 60)
        
        running_services = []
        for name, info in self.processes.items():
            if self.check_service_health(name):
                port = info.get("port")
                if port:
                    url = f"http://localhost:{port}"
                    running_services.append((name, url))
                    print(f"  🌐 {name}: {url}")
                else:
                    running_services.append((name, "Running"))
                    print(f"  ✅ {name}: Running")
        
        print("\n📊 SYSTEM STATUS:")
        print(f"  • Active Services: {len(running_services)}")
        print(f"  • Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if running_services:
            print("\n🎯 QUICK ACCESS:")
            print("  • Codex Dashboard: http://localhost:8531")
            print("  • API Documentation: http://localhost:8000/docs")
            print("  • Technical Council: http://localhost:8532")
            
            print("\n⌨️  KEYBOARD SHORTCUTS:")
            print("  • Ctrl+C: Stop all services")
            print("  • View logs in terminal for each service")
        
        print("\n" + "=" * 60)
    
    def monitor_services(self):
        """Monitor running services"""
        try:
            while True:
                time.sleep(30)  # Check every 30 seconds
                
                for name in list(self.processes.keys()):
                    if not self.check_service_health(name):
                        self.log_message(f"Service {name} stopped", "WARN")
                        # Could implement auto-restart here
                
        except KeyboardInterrupt:
            self.shutdown_all_services()
    
    def shutdown_all_services(self):
        """Shutdown all running services"""
        self.log_message("🛑 Shutting down all services...")
        
        for name, info in self.processes.items():
            try:
                process = info["process"]
                if process.poll() is None:  # Still running
                    process.terminate()
                    process.wait(timeout=5)
                    self.log_message(f"  ✅ {name} stopped")
            except Exception as e:
                self.log_message(f"  ⚠️  Error stopping {name}: {e}", "WARN")
        
        self.log_message("👋 Codex Dominion Suite shutdown complete")
    
    async def full_startup(self):
        """Complete startup sequence"""
        self.log_message("🌟 CODEX DOMINION SUITE STARTUP INITIATED")
        print("=" * 60)
        
        # 1. Environment checks
        if not self.check_python_environment():
            return False
        
        # 2. Dependency checks
        deps = self.check_dependencies()
        missing = [pkg for pkg, installed in deps.items() if not installed]
        
        if missing:
            self.log_message(f"Found {len(missing)} missing dependencies")
            user_input = input("Install missing dependencies? (y/N): ")
            if user_input.lower() in ['y', 'yes']:
                self.install_missing_dependencies(missing)
            else:
                self.log_message("Continuing without installing dependencies", "WARN")
        
        # 3. Environment setup
        self.setup_environment()
        
        # 4. Launch services
        services_started = 0
        
        if self.launch_codex_dashboard():
            services_started += 1
        
        if self.launch_api_server():
            services_started += 1
        
        if self.launch_technical_operations_council():
            services_started += 1
        
        # 5. Display summary
        if services_started > 0:
            self.display_startup_summary()
            
            # 6. Monitor services
            self.monitor_services()
        else:
            self.log_message("❌ No services started successfully", "ERROR")
            return False
        
        return True
    
    async def quick_launch(self, service_name: str = "dashboard"):
        """Quick launch a single service"""
        self.log_message(f"🚀 Quick launching {service_name}...")
        
        if service_name == "dashboard":
            success = self.launch_codex_dashboard()
        elif service_name == "api":
            success = self.launch_api_server()
        elif service_name == "council":
            success = self.launch_technical_operations_council()
        else:
            self.log_message(f"Unknown service: {service_name}", "ERROR")
            return False
        
        if success:
            self.display_startup_summary()
            self.monitor_services()
        
        return success

async def main():
    """Main entry point"""
    launcher = CodexLauncher()
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "quick":
            service = sys.argv[2] if len(sys.argv) > 2 else "dashboard"
            await launcher.quick_launch(service)
        elif command == "dashboard":
            await launcher.quick_launch("dashboard")
        elif command == "api":
            await launcher.quick_launch("api")
        elif command == "council":
            await launcher.quick_launch("council")
        elif command == "full":
            await launcher.full_startup()
        else:
            print("Codex Dominion Suite Launcher")
            print("Usage:")
            print("  python launch_codex.py [command]")
            print("")
            print("Commands:")
            print("  full      - Full startup with all services")
            print("  dashboard - Launch Codex Dashboard only")
            print("  api       - Launch API server only")
            print("  council   - Launch Technical Operations Council only")
            print("  quick     - Quick launch (default: dashboard)")
    else:
        # Default to full startup
        await launcher.full_startup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Codex Dominion Suite launcher stopped")
    except Exception as e:
        print(f"❌ Launcher error: {e}")
        sys.exit(1)
"""
Codex Dashboard Launcher
Bulletproof Streamlit launcher with enhanced error handling and port management
"""

import json
import logging
import os
import socket
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

# Configure logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("dashboard_launcher.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

# Set console output to UTF-8 on Windows
if sys.platform == "win32":
    import locale

    locale.setlocale(locale.LC_ALL, "")
    # Fallback to ASCII for console output
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
logger = logging.getLogger(__name__)


class DashboardLauncher:
    """Enhanced dashboard launcher with error recovery"""

    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.processes = {}
        self.available_ports = []
        self.dashboard_configs = {
            "monetization_crown": {
                "file": "monetization_crown.py",
                "name": "Enhanced Monetization Crown",
                "description": "Creator Economy Dashboard",
                "preferred_port": 8503,
            },
            "portfolio_dashboard": {
                "file": "codex_portfolio_dashboard.py",
                "name": "Portfolio Manager",
                "description": "Trading & Portfolio Management",
                "preferred_port": 8501,
            },
            "trading_api": {
                "file": "codex_trading_api.py",
                "name": "Trading API",
                "description": "FastAPI REST endpoints",
                "preferred_port": 8000,
            },
        }

    def check_port_availability(self, port):
        """Check if port is available"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(("127.0.0.1", port))
            sock.close()
            return result != 0
        except Exception:
            return False

    def find_available_port(self, start_port=8501, max_attempts=50):
        """Find next available port"""
        for port in range(start_port, start_port + max_attempts):
            if self.check_port_availability(port):
                return port
        return None

    def kill_processes_on_port(self, port):
        """Kill any processes using the specified port"""
        try:
            if sys.platform == "win32":
                # Windows
                cmd = f"netstat -ano | findstr :{port}"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

                if result.stdout:
                    lines = result.stdout.strip().split("\n")
                    pids = set()

                    for line in lines:
                        if "LISTENING" in line:
                            parts = line.split()
                            if len(parts) >= 5:
                                pid = parts[-1]
                                pids.add(pid)

                    for pid in pids:
                        try:
                            subprocess.run(
                                f"taskkill /F /PID {pid}",
                                shell=True,
                                capture_output=True,
                            )
                            logger.info(f"Killed process {pid} using port {port}")
                        except Exception as e:
                            logger.warning(f"Could not kill process {pid}: {e}")
            else:
                # Linux/Mac
                cmd = f"lsof -ti:{port}"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

                if result.stdout:
                    pids = result.stdout.strip().split("\n")
                    for pid in pids:
                        try:
                            subprocess.run(f"kill -9 {pid}", shell=True)
                            logger.info(f"Killed process {pid} using port {port}")
                        except Exception as e:
                            logger.warning(f"Could not kill process {pid}: {e}")

        except Exception as e:
            logger.error(f"Error killing processes on port {port}: {e}")

    def validate_dashboard_file(self, dashboard_key):
        """Validate that dashboard file exists and can be imported"""
        config = self.dashboard_configs[dashboard_key]
        file_path = self.base_dir / config["file"]

        if not file_path.exists():
            logger.error(f"Dashboard file not found: {file_path}")
            return False

        # Test import
        try:
            if dashboard_key == "trading_api":
                # For FastAPI, just check file syntax
                with open(file_path, "r", encoding="utf-8") as f:
                    compile(f.read(), file_path, "exec")
            else:
                # For Streamlit apps, test import
                import importlib.util

                spec = importlib.util.spec_from_file_location("temp_module", file_path)
                module = importlib.util.module_from_spec(spec)
                # Don't execute, just validate syntax
                with open(file_path, "r", encoding="utf-8") as f:
                    compile(f.read(), file_path, "exec")

            logger.info(f"✅ {config['name']} file validation passed")
            return True

        except Exception as e:
            logger.error(f"❌ {config['name']} file validation failed: {e}")
            return False

    def launch_streamlit_dashboard(self, dashboard_key, port):
        """Launch a Streamlit dashboard"""
        config = self.dashboard_configs[dashboard_key]
        file_path = self.base_dir / config["file"]

        logger.info(f"🚀 Launching {config['name']} on port {port}...")

        # Prepare command
        python_exe = sys.executable
        cmd = [
            python_exe,
            "-m",
            "streamlit",
            "run",
            str(file_path),
            "--server.port",
            str(port),
            "--server.address",
            "127.0.0.1",
            "--server.headless",
            "true",
            "--browser.gatherUsageStats",
            "false",
            "--server.enableCORS",
            "false",
            "--server.enableXsrfProtection",
            "false",
        ]

        try:
            # Launch process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                cwd=str(self.base_dir),
            )

            # Store process info
            self.processes[dashboard_key] = {
                "process": process,
                "port": port,
                "config": config,
                "start_time": datetime.now(),
            }

            logger.info(f"✅ {config['name']} launched successfully on port {port}")
            logger.info(f"🌐 Access at: http://127.0.0.1:{port}")

            return True

        except Exception as e:
            logger.error(f"❌ Failed to launch {config['name']}: {e}")
            return False

    def launch_fastapi_server(self, dashboard_key, port):
        """Launch FastAPI server"""
        config = self.dashboard_configs[dashboard_key]
        file_path = self.base_dir / config["file"]

        logger.info(f"🚀 Launching {config['name']} on port {port}...")

        # Prepare command
        python_exe = sys.executable
        cmd = [
            python_exe,
            "-m",
            "uvicorn",
            f"{config['file'].replace('.py', '')}:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
            "--reload",
        ]

        try:
            # Launch process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                cwd=str(self.base_dir),
            )

            # Store process info
            self.processes[dashboard_key] = {
                "process": process,
                "port": port,
                "config": config,
                "start_time": datetime.now(),
            }

            logger.info(f"✅ {config['name']} launched successfully on port {port}")
            logger.info(f"🌐 API Docs at: http://127.0.0.1:{port}/docs")

            return True

        except Exception as e:
            logger.error(f"❌ Failed to launch {config['name']}: {e}")
            return False

    def monitor_process(self, dashboard_key):
        """Monitor a dashboard process"""
        if dashboard_key not in self.processes:
            return

        process_info = self.processes[dashboard_key]
        process = process_info["process"]
        config = process_info["config"]

        # Check if process is still running
        if process.poll() is not None:
            # Process has terminated
            return_code = process.returncode
            logger.error(f"❌ {config['name']} terminated with code {return_code}")

            # Try to get output
            try:
                stdout, _ = process.communicate(timeout=1)
                if stdout:
                    logger.error(f"Process output: {stdout}")
            except:
                pass

            # Remove from processes
            del self.processes[dashboard_key]

    def launch_dashboard(self, dashboard_key, force_port=None):
        """Launch a specific dashboard with error recovery"""

        if dashboard_key not in self.dashboard_configs:
            logger.error(f"Unknown dashboard: {dashboard_key}")
            return False

        config = self.dashboard_configs[dashboard_key]

        # Validate file first
        if not self.validate_dashboard_file(dashboard_key):
            return False

        # Determine port
        if force_port:
            port = force_port
        else:
            preferred_port = config["preferred_port"]
            if self.check_port_availability(preferred_port):
                port = preferred_port
            else:
                logger.warning(
                    f"Preferred port {preferred_port} not available, finding alternative..."
                )
                self.kill_processes_on_port(preferred_port)
                time.sleep(2)  # Wait for cleanup

                if self.check_port_availability(preferred_port):
                    port = preferred_port
                else:
                    port = self.find_available_port(preferred_port + 1)

        if not port:
            logger.error(f"No available ports found for {config['name']}")
            return False

        # Launch appropriate server
        if dashboard_key == "trading_api":
            return self.launch_fastapi_server(dashboard_key, port)
        else:
            return self.launch_streamlit_dashboard(dashboard_key, port)

    def launch_all_dashboards(self):
        """Launch all available dashboards"""
        logger.info("🎯 Launching Codex Dominion Dashboard Suite...")

        results = {}

        for dashboard_key in self.dashboard_configs:
            config = self.dashboard_configs[dashboard_key]
            logger.info(f"📊 Preparing {config['name']}...")

            success = self.launch_dashboard(dashboard_key)
            results[dashboard_key] = success

            if success:
                time.sleep(3)  # Stagger launches

        return results

    def status_report(self):
        """Generate status report"""
        logger.info("📊 Codex Dominion Dashboard Status Report")
        logger.info("=" * 60)

        if not self.processes:
            logger.info("No dashboards currently running")
            return

        for dashboard_key, process_info in self.processes.items():
            config = process_info["config"]
            port = process_info["port"]
            start_time = process_info["start_time"]
            uptime = datetime.now() - start_time

            # Check if process is healthy
            self.monitor_process(dashboard_key)

            if dashboard_key in self.processes:  # Still running
                logger.info(f"✅ {config['name']}")
                logger.info(f"   Port: {port}")
                logger.info(f"   Uptime: {str(uptime).split('.')[0]}")
                if dashboard_key == "trading_api":
                    logger.info(f"   URL: http://127.0.0.1:{port}/docs")
                else:
                    logger.info(f"   URL: http://127.0.0.1:{port}")
            else:
                logger.info(f"❌ {config['name']} (terminated)")

    def shutdown_all(self):
        """Shutdown all running dashboards"""
        logger.info("🛑 Shutting down all dashboards...")

        for dashboard_key, process_info in self.processes.items():
            process = process_info["process"]
            config = process_info["config"]

            logger.info(f"Stopping {config['name']}...")

            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logger.warning(f"Force killing {config['name']}...")
                process.kill()
            except Exception as e:
                logger.error(f"Error stopping {config['name']}: {e}")

        self.processes.clear()
        logger.info("✅ All dashboards stopped")


def main():
    """Main launcher function"""
    launcher = DashboardLauncher()

    try:
        print("🎯 Codex Dominion Dashboard Launcher")
        print("=" * 50)

        # Launch all dashboards
        results = launcher.launch_all_dashboards()

        # Report results
        print("\n📊 Launch Results:")
        print("-" * 30)

        success_count = 0
        for dashboard_key, success in results.items():
            config = launcher.dashboard_configs[dashboard_key]
            status = "✅ SUCCESS" if success else "❌ FAILED"
            print(f"{config['name']}: {status}")
            if success:
                success_count += 1

        if success_count > 0:
            print(
                f"\n🎉 {success_count}/{len(results)} dashboards launched successfully!"
            )
            print("\n🌐 Access URLs:")
            for dashboard_key, process_info in launcher.processes.items():
                config = process_info["config"]
                port = process_info["port"]
                if dashboard_key == "trading_api":
                    print(f"   {config['name']}: http://127.0.0.1:{port}/docs")
                else:
                    print(f"   {config['name']}: http://127.0.0.1:{port}")

            print("\n⌨️ Press Ctrl+C to stop all dashboards")

            # Keep running and monitor
            while True:
                time.sleep(30)
                launcher.status_report()
        else:
            print("\n❌ No dashboards launched successfully")
            return False

    except KeyboardInterrupt:
        print("\n\n🛑 Shutdown requested...")
        launcher.shutdown_all()
        print("👋 Goodbye!")
        return True

    except Exception as e:
        logger.error(f"Fatal error in launcher: {e}")
        launcher.shutdown_all()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

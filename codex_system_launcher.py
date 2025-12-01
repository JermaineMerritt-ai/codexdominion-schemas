#!/usr/bin/env python3
"""
Codex Market Dominion - Complete System Launcher
Launches API + Dashboards in production-ready configuration
"""

import logging
import os
import signal
import subprocess
import sys
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("codex_system.log", mode="a"),
    ],
)
logger = logging.getLogger(__name__)


class CodexSystemLauncher:
    def __init__(self):
        self.processes = []
        self.services = {
            "api": {
                "name": "Codex Market Dominion API",
                "command": [
                    sys.executable,
                    "-m",
                    "uvicorn",
                    "app.main:app",
                    "--host",
                    "0.0.0.0",
                    "--port",
                    "8000",
                    "--reload",
                ],
                "port": 8000,
                "url": "http://127.0.0.1:8000",
                "health_endpoint": "/health",
                "docs_url": "http://127.0.0.1:8000/docs",
            },
            "main_dashboard": {
                "name": "Main Trading Dashboard",
                "command": [
                    sys.executable,
                    "-m",
                    "streamlit",
                    "run",
                    "dashboard/app.py",
                    "--server.port",
                    "8502",
                    "--server.address",
                    "127.0.0.1",
                ],
                "port": 8502,
                "url": "http://127.0.0.1:8502",
            },
            "monetization_crown": {
                "name": "Enhanced Monetization Crown",
                "command": [
                    sys.executable,
                    "-m",
                    "streamlit",
                    "run",
                    "monetization_crown.py",
                    "--server.port",
                    "8503",
                    "--server.address",
                    "127.0.0.1",
                ],
                "port": 8503,
                "url": "http://127.0.0.1:8503",
            },
            "portfolio_dashboard": {
                "name": "Portfolio Management Dashboard",
                "command": [
                    sys.executable,
                    "-m",
                    "streamlit",
                    "run",
                    "codex_portfolio_dashboard.py",
                    "--server.port",
                    "8501",
                    "--server.address",
                    "127.0.0.1",
                ],
                "port": 8501,
                "url": "http://127.0.0.1:8501",
            },
        }
        self.running_services = {}

        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        logger.info(f"Received signal {signum}. Initiating graceful shutdown...")
        self.shutdown_all_services()
        sys.exit(0)

    def check_port_available(self, port):
        """Check if port is available"""
        import socket

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(("127.0.0.1", port)) != 0

    def wait_for_service(self, service_name, timeout=30):
        """Wait for service to become available"""
        service = self.services[service_name]
        port = service["port"]

        logger.info(f"Waiting for {service['name']} to start on port {port}...")

        start_time = time.time()
        while time.time() - start_time < timeout:
            if not self.check_port_available(port):
                logger.info(f"✅ {service['name']} is ready!")
                return True
            time.sleep(1)

        logger.error(f"❌ {service['name']} failed to start within {timeout}s")
        return False

    def launch_service(self, service_name):
        """Launch a single service"""
        service = self.services[service_name]

        logger.info(f"🚀 Starting {service['name']}...")

        try:
            process = subprocess.Popen(
                service["command"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
            )

            self.processes.append(process)
            self.running_services[service_name] = {
                "process": process,
                "started_at": datetime.now(),
                "config": service,
            }

            # Wait for service to start
            if self.wait_for_service(service_name):
                logger.info(f"✅ SUCCESS: {service['name']} launched successfully!")
                logger.info(f"🔗 ACCESS: {service['url']}")

                # Log additional info for API
                if service_name == "api" and "docs_url" in service:
                    logger.info(f"📚 API DOCS: {service['docs_url']}")

                return True
            else:
                logger.error(f"❌ FAILED: {service['name']} launch failed")
                return False

        except Exception as e:
            logger.error(f"❌ ERROR launching {service['name']}: {e}")
            return False

    def launch_all_services(self):
        """Launch all services in order"""
        logger.info("🌟 CODEX MARKET DOMINION - SYSTEM STARTUP")
        logger.info("=" * 60)

        # Launch API first (most critical)
        if self.launch_service("api"):
            time.sleep(2)  # Brief pause between services

        # Launch dashboards
        self.launch_service("monetization_crown")
        time.sleep(1)
        self.launch_service("portfolio_dashboard")

        # Summary
        successful_services = len(self.running_services)
        total_services = len(self.services)

        logger.info("")
        logger.info("🎯 SYSTEM STATUS SUMMARY")
        logger.info("-" * 40)
        logger.info(f"✅ Services Running: {successful_services}/{total_services}")

        if successful_services > 0:
            logger.info("")
            logger.info("🌐 ACCESS POINTS:")
            for service_name, running_service in self.running_services.items():
                config = running_service["config"]
                logger.info(f"  📊 {config['name']}: {config['url']}")

            # Special info for API
            if "api" in self.running_services:
                logger.info("  📚 API Documentation: http://127.0.0.1:8000/docs")
                logger.info("  📋 API Health Check: http://127.0.0.1:8000/health")

            logger.info("")
            logger.info("🚀 CODEX MARKET DOMINION IS OPERATIONAL!")
            logger.info("Press Ctrl+C to stop all services")
            return True
        else:
            logger.error("❌ No services started successfully")
            return False

    def monitor_services(self):
        """Monitor running services"""
        try:
            while True:
                time.sleep(5)

                # Check if any processes have died
                for service_name, running_service in list(
                    self.running_services.items()
                ):
                    process = running_service["process"]
                    if process.poll() is not None:
                        logger.error(
                            f"❌ {running_service['config']['name']} has stopped unexpectedly"
                        )
                        del self.running_services[service_name]

                # If all services have died, exit
                if not self.running_services:
                    logger.error("💀 All services have stopped. Exiting.")
                    break

        except KeyboardInterrupt:
            logger.info("🛑 Shutdown signal received")

    def shutdown_all_services(self):
        """Gracefully shutdown all services"""
        logger.info("🛑 Shutting down all services...")

        for process in self.processes:
            if process.poll() is None:
                try:
                    process.terminate()
                    # Wait up to 5 seconds for graceful termination
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    logger.warning("Force killing unresponsive process")
                    process.kill()
                except Exception as e:
                    logger.error(f"Error stopping process: {e}")

        self.processes.clear()
        self.running_services.clear()
        logger.info("✅ All services stopped gracefully")

    def run(self):
        """Main run method"""
        try:
            if self.launch_all_services():
                self.monitor_services()

        except Exception as e:
            logger.error(f"💥 Critical error: {e}")

        finally:
            self.shutdown_all_services()


def main():
    """Main entry point"""
    launcher = CodexSystemLauncher()
    launcher.run()


if __name__ == "__main__":
    main()

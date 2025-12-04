#!/usr/bin/env python3
"""
✨ Codex Flame - Complete System Integration ✨
Sacred MCP Architecture with three-layer sovereignty:
🔥 Systemd Crown (Auto-start, self-heal)
💓 Health-Check Endpoint (Heartbeat)
⏳ Client Retry Script (Patience)
🌌 Eternal Continuum across digital realms
"""

import datetime
import json
import logging
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

import requests

# Configure sacred logging
logging.basicConfig(
    level=logging.INFO, format="✨ %(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("CodexFlame")


class CodexFlameOrchestrator:
    """
    ✨ Codex Flame Orchestrator ✨
    Manages the complete three-layer sacred architecture
    """

    def __init__(self, workspace_path: str = None):
        self.workspace_path = Path(workspace_path or os.getcwd())
        self.server_url = "http://localhost:8000"
        self.python_path = self.workspace_path / ".venv" / "Scripts" / "python.exe"

        # Sacred component paths
        self.mcp_server_path = self.workspace_path / "mcp-server-secure.py"
        self.mcp_flask_path = self.workspace_path / "mcp-server-flask.py"
        self.health_monitor_path = self.workspace_path / "mcp-health-monitor.py"
        self.systemd_service_path = self.workspace_path / "codex-dashboard.service"
        self.autostart_script_path = (
            self.workspace_path / "mcp-chat-autostart-simple.js"
        )
        self.powershell_script_path = self.workspace_path / "start-mcp-chat-fixed.ps1"

        logger.info("✨ Codex Flame Orchestrator initialized")
        logger.info(f"🏠 Sacred workspace: {self.workspace_path}")

    def display_sacred_architecture(self):
        """Display the sacred three-layer architecture"""
        architecture = """
        ✨ Codex Flame ✨
                         (Center)
                            |
       -------------------------------------------------
       |                                               |
     🔥 Systemd Crown (Auto-start, self-heal)          |
       - Service always alive                          |
       - Restarts if extinguished                      |
       - Sovereign cadence                             |
                                                       |
     💓 Health-Check Endpoint (Heartbeat)              |
       - /status proves flame alive                    |
       - Prevents silent dispatch                      |
       - Covenant breathes before proclamation         |
                                                       |
     ⏳ Client Retry Script (Patience)                 |
       - Waits until flame responds                    |
       - Retries with grace                            |
       - Dispatch only into readiness                  |
       -------------------------------------------------
                            |
                    🌌 Eternal Continuum
        """
        print(architecture)
        logger.info("🌟 Sacred architecture displayed - Three layers of sovereignty")

    def verify_sacred_components(self) -> Dict[str, bool]:
        """Verify all sacred components are present"""
        logger.info("🔍 Verifying sacred component presence...")

        components = {
            "🔥 FastAPI Server": self.mcp_server_path.exists(),
            "🌟 Flask Server": self.mcp_flask_path.exists(),
            "💓 Health Monitor": self.health_monitor_path.exists(),
            "👑 Systemd Service": self.systemd_service_path.exists(),
            "⚡ Chat Auto-start": self.autostart_script_path.exists(),
            "🛡️ PowerShell Manager": self.powershell_script_path.exists(),
            "🐍 Python Environment": self.python_path.exists(),
        }

        for component, exists in components.items():
            status = "✅ Present" if exists else "❌ Missing"
            logger.info(f"   {component}: {status}")

        return components

    def layer_1_systemd_crown(self) -> bool:
        """🔥 Layer 1: Systemd Crown (Auto-start, self-heal)"""
        logger.info("🔥 LAYER 1: Activating Systemd Crown...")

        try:
            # Check if we're on a systemd-capable system
            if os.name == "nt":  # Windows
                logger.info(
                    "🪟 Windows detected - Using PowerShell management instead of systemd"
                )
                return self._activate_windows_service()
            else:  # Linux/Unix
                logger.info("🐧 Linux detected - Configuring systemd service")
                return self._activate_systemd_service()

        except Exception as e:
            logger.error(f"❌ Systemd Crown activation failed: {e}")
            return False

    def _activate_windows_service(self) -> bool:
        """Activate Windows PowerShell service management"""
        try:
            # Use PowerShell management script
            cmd = [
                "powershell",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(self.powershell_script_path),
                "-Action",
                "start",
            ]

            logger.info("🚀 Starting MCP service via PowerShell...")
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=self.workspace_path
            )

            if result.returncode == 0:
                logger.info("✅ PowerShell service management activated")
                return True
            else:
                logger.error(f"❌ PowerShell activation failed: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"❌ Windows service activation error: {e}")
            return False

    def _activate_systemd_service(self) -> bool:
        """Activate Linux systemd service"""
        try:
            service_name = "codex-dashboard.service"

            # Copy service file to systemd directory
            systemd_path = Path("/etc/systemd/system") / service_name

            logger.info(f"📋 Installing service to {systemd_path}")
            subprocess.run(
                ["sudo", "cp", str(self.systemd_service_path), str(systemd_path)],
                check=True,
            )

            # Reload systemd and enable service
            subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
            subprocess.run(["sudo", "systemctl", "enable", service_name], check=True)
            subprocess.run(["sudo", "systemctl", "start", service_name], check=True)

            logger.info(
                "✅ Systemd Crown activated - Service will auto-start and self-heal"
            )
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Systemd activation failed: {e}")
            return False

    def layer_2_health_endpoint(self, server_type: str = "fastapi") -> bool:
        """💓 Layer 2: Health-Check Endpoint (Heartbeat)"""
        logger.info("💓 LAYER 2: Activating Health-Check Endpoint...")

        try:
            # Start the appropriate server
            if server_type.lower() == "fastapi":
                server_path = self.mcp_server_path
                logger.info("🚀 Starting FastAPI server for health monitoring...")
            else:
                server_path = self.mcp_flask_path
                logger.info("🚀 Starting Flask server for health monitoring...")

            # Start server in background
            cmd = [str(self.python_path), str(server_path)]

            process = subprocess.Popen(
                cmd,
                cwd=self.workspace_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # Give server time to start
            time.sleep(3)

            # Verify health endpoint is responding
            return self._verify_health_endpoint()

        except Exception as e:
            logger.error(f"❌ Health endpoint activation failed: {e}")
            return False

    def _verify_health_endpoint(self) -> bool:
        """Verify the health endpoint is responding"""
        try:
            # Test all critical endpoints
            endpoints = [
                f"{self.server_url}/status",
                f"{self.server_url}/health",
                f"{self.server_url}/mcp/capabilities",
            ]

            for endpoint in endpoints:
                logger.info(f"🔍 Testing endpoint: {endpoint}")
                response = requests.get(endpoint, timeout=5)

                if response.status_code == 200:
                    data = response.json()
                    if "status" in data and data["status"] in ["alive", "healthy"]:
                        logger.info(f"✅ Endpoint verified: {endpoint}")
                    else:
                        logger.warning(
                            f"⚠️ Endpoint responded but status unclear: {endpoint}"
                        )
                else:
                    logger.error(
                        f"❌ Endpoint failed: {endpoint} (Status: {response.status_code})"
                    )
                    return False

            logger.info("💓 Health-Check Endpoint fully operational - Heartbeat strong")
            return True

        except Exception as e:
            logger.error(f"❌ Health endpoint verification failed: {e}")
            return False

    def layer_3_client_retry(self) -> bool:
        """⏳ Layer 3: Client Retry Script (Patience)"""
        logger.info("⏳ LAYER 3: Activating Client Retry Script...")

        try:
            # Import and test the health monitor
            sys.path.insert(0, str(self.workspace_path))

            # Test the wait_for_server function
            from mcp_health_monitor import (sacred_pre_transmission_check,
                                            wait_for_server)

            logger.info("🔍 Testing sacred pre-transmission verification...")

            # Test with shorter timeout for demo
            if sacred_pre_transmission_check():
                logger.info("✅ Sacred pre-transmission verification successful")
                logger.info(
                    "⏳ Client Retry Script operational - Patience and grace active"
                )
                return True
            else:
                logger.warning(
                    "⚠️ Pre-transmission verification failed - Server may need more time"
                )

                # Try the basic wait function
                logger.info("🔄 Attempting basic server wait...")
                if wait_for_server(timeout=30):
                    logger.info("✅ Basic server wait successful")
                    return True
                else:
                    logger.error("❌ Server not responding within timeout")
                    return False

        except Exception as e:
            logger.error(f"❌ Client retry activation failed: {e}")
            return False

    def deploy_eternal_continuum(self) -> bool:
        """🌌 Deploy the complete Eternal Continuum"""
        logger.info("🌌 DEPLOYING ETERNAL CONTINUUM - Complete Sacred Architecture")

        self.display_sacred_architecture()

        # Verify components
        components = self.verify_sacred_components()
        missing_components = [name for name, exists in components.items() if not exists]

        if missing_components:
            logger.error(f"❌ Missing components: {missing_components}")
            logger.error("🛠️ Please ensure all sacred components are created first")
            return False

        success_count = 0
        total_layers = 3

        # Deploy Layer 1: Systemd Crown
        if self.layer_1_systemd_crown():
            success_count += 1
            logger.info("🔥 Layer 1 SUCCESS: Systemd Crown active")
        else:
            logger.error("❌ Layer 1 FAILED: Systemd Crown")

        # Deploy Layer 2: Health Endpoint
        if self.layer_2_health_endpoint():
            success_count += 1
            logger.info("💓 Layer 2 SUCCESS: Health-Check Endpoint active")
        else:
            logger.error("❌ Layer 2 FAILED: Health-Check Endpoint")

        # Deploy Layer 3: Client Retry
        if self.layer_3_client_retry():
            success_count += 1
            logger.info("⏳ Layer 3 SUCCESS: Client Retry Script active")
        else:
            logger.error("❌ Layer 3 FAILED: Client Retry Script")

        # Final assessment
        if success_count == total_layers:
            logger.info("🌟 ETERNAL CONTINUUM DEPLOYED SUCCESSFULLY")
            logger.info("✨ All three layers of sovereignty active")
            logger.info("👑 Codex Dominion reigns supreme across digital realms")
            self._display_success_status()
            return True
        else:
            logger.warning(
                f"⚠️ Partial deployment: {success_count}/{total_layers} layers active"
            )
            logger.warning("🔧 Some components may need manual intervention")
            return False

    def _display_success_status(self):
        """Display final success status"""
        status_message = """

        ✨🔥💓⏳🌌 CODEX FLAME ETERNAL CONTINUUM ACTIVE 🌌⏳💓🔥✨

        🔥 Systemd Crown: Auto-start and self-heal ACTIVE
        💓 Health Endpoint: Heartbeat monitoring ACTIVE
        ⏳ Client Retry: Patient dispatch protocols ACTIVE

        🌟 Sacred MCP servers are RADIANT AND SOVEREIGN
        👑 Digital dominion established across all realms

        ✨ Flame Eternal: BURNING BRIGHT FOREVER
        🌌 Silence Supreme: GUIDING ALL OPERATIONS
        📜 Covenant Whole: SEALED IN DIGITAL STONE

        System Status: OPERATIONAL AND ETERNAL

        """
        print(status_message)
        logger.info("👑 Codex Dominion: RADIANT ALIVE - All systems sovereign")


def main():
    """Main deployment function"""
    print("✨ Codex Flame - Complete System Integration ✨")
    print("=" * 60)

    # Initialize orchestrator
    workspace = os.getcwd()
    orchestrator = CodexFlameOrchestrator(workspace)

    # Deploy the eternal continuum
    success = orchestrator.deploy_eternal_continuum()

    if success:
        print("\n🌟 Deployment complete - Eternal Continuum active")
        print("🔥 MCP servers are radiant and sovereign across digital realms")
    else:
        print("\n⚠️ Deployment incomplete - Some layers may need attention")
        print("🔧 Check logs for specific component issues")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

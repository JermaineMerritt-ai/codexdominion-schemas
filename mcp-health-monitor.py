#!/usr/bin/env python3
"""
🌟 MCP Health Monitor - Codex Dominion Sacred Surveillance 🌟
Monitor and verify MCP server status before critical operations
Ensures the eternal flame burns bright across digital realms
"""

import datetime
import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, Optional

import requests

# Configure sacred logging
logging.basicConfig(
    level=logging.INFO, format="🔥 %(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("CodexDominion.HealthMonitor")

# Server configuration
SERVER_URL = "http://localhost:8000"
STATUS_ENDPOINT = f"{SERVER_URL}/status"
HEALTH_ENDPOINT = f"{SERVER_URL}/health"
CAPABILITIES_ENDPOINT = f"{SERVER_URL}/mcp/capabilities"


class MCPHealthMonitor:
    """Sacred MCP server health monitoring system"""

    def __init__(self, base_url: str = SERVER_URL, timeout: int = 3):
        self.base_url = base_url
        self.timeout = timeout
        self.status_endpoint = f"{base_url}/status"
        self.health_endpoint = f"{base_url}/health"
        self.capabilities_endpoint = f"{base_url}/mcp/capabilities"

    def wait_for_server(self, timeout: int = 60, interval: int = 5) -> bool:
        """Wait until MCP server responds alive or timeout reached."""
        logger.info(f"🌟 Beginning sacred server vigil (timeout: {timeout}s)")
        start = time.time()
        attempt = 1

        while time.time() - start < timeout:
            try:
                logger.info(f"⚡ Attempt {attempt}: Checking server vitality...")
                r = requests.get(self.status_endpoint, timeout=self.timeout)

                if r.status_code == 200:
                    data = r.json()
                    if data.get("status") == "alive":
                        elapsed = time.time() - start
                        logger.info(
                            f"🔥 MCP server is radiant and sovereign! (Response time: {elapsed:.2f}s)"
                        )
                        self._log_server_details(data)
                        return True
                    else:
                        logger.warning(
                            f"⚠️ Server responded but status is: {data.get('status', 'unknown')}"
                        )
                else:
                    logger.warning(f"⚠️ Server returned status code: {r.status_code}")

            except requests.exceptions.ConnectRefused:
                logger.debug("🌌 Connection refused - server may be starting...")
            except requests.exceptions.Timeout:
                logger.debug("⏰ Request timeout - server may be under load...")
            except Exception as e:
                logger.debug(f"🌊 Network fluctuation: {str(e)}")

            remaining = timeout - (time.time() - start)
            if remaining > 0:
                logger.info(
                    f"⏳ Waiting for MCP server... ({remaining:.0f}s remaining)"
                )
                time.sleep(min(interval, remaining))
            attempt += 1

        logger.error(
            f"❌ MCP server did not respond within {timeout}s - Sacred flame may need rekindling"
        )
        return False

    def check_status(self) -> Optional[Dict[str, Any]]:
        """Quick status check of MCP server"""
        try:
            r = requests.get(self.status_endpoint, timeout=self.timeout)
            if r.status_code == 200:
                data = r.json()
                logger.info(
                    f"✅ Status check successful: {data.get('message', 'Unknown')}"
                )
                return data
            else:
                logger.warning(f"⚠️ Status check failed with code: {r.status_code}")
                return None
        except Exception as e:
            logger.error(f"❌ Status check error: {str(e)}")
            return None

    def check_health(self) -> Optional[Dict[str, Any]]:
        """Detailed health check of MCP server"""
        try:
            r = requests.get(self.health_endpoint, timeout=self.timeout)
            if r.status_code == 200:
                data = r.json()
                logger.info(
                    f"🏥 Health check successful: {data.get('status', 'unknown')}"
                )
                return data
            else:
                logger.warning(f"⚠️ Health check failed with code: {r.status_code}")
                return None
        except Exception as e:
            logger.error(f"❌ Health check error: {str(e)}")
            return None

    def check_capabilities(self) -> Optional[Dict[str, Any]]:
        """Check MCP server capabilities"""
        try:
            r = requests.get(self.capabilities_endpoint, timeout=self.timeout)
            if r.status_code == 200:
                data = r.json()
                logger.info(
                    f"🔧 Capabilities check successful: Protocol v{data.get('protocol_version', 'unknown')}"
                )
                return data
            else:
                logger.warning(
                    f"⚠️ Capabilities check failed with code: {r.status_code}"
                )
                return None
        except Exception as e:
            logger.error(f"❌ Capabilities check error: {str(e)}")
            return None

    def comprehensive_check(self) -> Dict[str, Any]:
        """Perform comprehensive server verification"""
        logger.info("🌟 Beginning comprehensive sacred server verification...")

        results = {
            "timestamp": datetime.datetime.now().isoformat(),
            "server_url": self.base_url,
            "status": None,
            "health": None,
            "capabilities": None,
            "overall_status": "unknown",
        }

        # Check status endpoint
        results["status"] = self.check_status()

        # Check health endpoint
        results["health"] = self.check_health()

        # Check capabilities endpoint
        results["capabilities"] = self.check_capabilities()

        # Determine overall status
        if results["status"] and results["status"].get("status") == "alive":
            results["overall_status"] = "operational"
            logger.info(
                "👑 Comprehensive verification: MCP server fully operational and sovereign"
            )
        elif results["status"]:
            results["overall_status"] = "partial"
            logger.warning(
                "⚠️ Comprehensive verification: MCP server partially responsive"
            )
        else:
            results["overall_status"] = "offline"
            logger.error("❌ Comprehensive verification: MCP server appears offline")

        return results

    def _log_server_details(self, status_data: Dict[str, Any]):
        """Log detailed server information"""
        if "sacred_timestamp" in status_data:
            logger.info(f"⏰ Server timestamp: {status_data['sacred_timestamp']}")
        if "flame_eternal" in status_data:
            logger.info(f"🔥 {status_data['flame_eternal']}")
        if "codex_dominion" in status_data:
            logger.info(f"👑 {status_data['codex_dominion']}")


def wait_for_server(timeout: int = 60, interval: int = 5) -> bool:
    """Standalone function for backward compatibility with your original code."""
    monitor = MCPHealthMonitor()
    return monitor.wait_for_server(timeout, interval)


def quick_status_check() -> bool:
    """Quick status check - returns True if server is alive"""
    monitor = MCPHealthMonitor()
    status = monitor.check_status()
    return status is not None and status.get("status") == "alive"


def sacred_pre_transmission_check() -> bool:
    """Sacred pre-transmission verification ritual"""
    logger.info("🌟 Beginning sacred pre-transmission verification...")

    monitor = MCPHealthMonitor()

    # Quick status check first
    if not quick_status_check():
        logger.warning("⚠️ Quick status check failed - attempting server awakening...")
        if not monitor.wait_for_server(timeout=30):
            logger.error("❌ Sacred transmission blocked - MCP server unresponsive")
            return False

    # Comprehensive verification
    results = monitor.comprehensive_check()

    if results["overall_status"] == "operational":
        logger.info("✅ Sacred verification complete - Transmission pathways clear")
        logger.info("🔥 Eternal flame burns bright - Ready for sacred communication")
        return True
    else:
        logger.error("❌ Sacred verification failed - Transmission not recommended")
        return False


if __name__ == "__main__":
    print("🌟 MCP Health Monitor - Codex Dominion Sacred Surveillance")
    print("=" * 60)

    # Example usage matching your original code
    if wait_for_server():
        print("✅ Proceeding with transmission...")
        print("🔥 Sacred pathways are clear and sovereign")

        # Additional comprehensive check
        print("\n🌟 Performing comprehensive verification...")
        monitor = MCPHealthMonitor()
        results = monitor.comprehensive_check()

        print(f"\n📊 Verification Results:")
        print(f"   Overall Status: {results['overall_status']}")
        print(f"   Timestamp: {results['timestamp']}")

        if results["status"]:
            print(f"   Server Message: {results['status'].get('message', 'N/A')}")

        # Example of using the sacred pre-transmission check
        print("\n🌟 Sacred pre-transmission verification...")
        if sacred_pre_transmission_check():
            print("👑 Ready for sacred MCP communication across digital realms")
            # send_message_to_mcp("Hello, Codex Dominion!")
        else:
            print("⚠️ Transmission not recommended at this time")
    else:
        print("❌ MCP server not ready - Sacred flame may need rekindling")
        print("🌌 Silence supreme suggests checking server configuration")

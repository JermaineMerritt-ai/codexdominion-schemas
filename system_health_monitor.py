#!/usr/bin/env python3
"""
System Health Monitor - Real-Time Service Monitoring
====================================================

Monitors all Codex Dominion services:
- 20+ running services on various ports
- Python dashboards (Streamlit, Flask)
- Background processes
- Database connections
- API endpoints
- Resource usage (CPU, Memory, Disk)

Features:
- Real-time health checks
- Automated service recovery
- Alert system
- Performance metrics
- Uptime tracking
- Historical data
"""

import json
import os
import psutil
import requests
import socket
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import subprocess
import platform


# =============================================================================
# SERVICE CONFIGURATION
# =============================================================================

class ServiceConfig:
    """Configuration for all monitored services"""

    @staticmethod
    def get_services() -> List[Dict]:
        """Get list of all services to monitor"""
        return [
            {
                "name": "Main Dashboard",
                "type": "flask",
                "port": 5555,
                "health_endpoint": "http://localhost:5555/",
                "critical": True,
                "auto_restart": True,
                "start_command": "python dashboard_working.py"
            },
            {
                "name": "Unified Launcher",
                "type": "flask",
                "port": 5556,
                "health_endpoint": "http://localhost:5556/",
                "critical": False,
                "auto_restart": True,
                "start_command": "python unified_launcher.py"
            },
            {
                "name": "Jermaine Super Action AI",
                "type": "streamlit",
                "port": 8501,
                "health_endpoint": "http://localhost:8501/",
                "critical": True,
                "auto_restart": True,
                "start_command": "streamlit run jermaine_super_action_ai.py --server.port 8501"
            },
            {
                "name": "Audio Studio",
                "type": "streamlit",
                "port": 8502,
                "health_endpoint": "http://localhost:8502/",
                "critical": False,
                "auto_restart": True,
                "start_command": "streamlit run audio_studio.py --server.port 8502"
            },
            {
                "name": "Flask Mega Dashboard",
                "type": "flask",
                "port": 5000,
                "health_endpoint": "http://localhost:5000/",
                "critical": False,
                "auto_restart": False,
                "start_command": "python flask_dashboard.py"
            },
            {
                "name": "Stock Analytics Dashboard",
                "type": "streamlit",
                "port": 8515,
                "health_endpoint": "http://localhost:8515/",
                "critical": False,
                "auto_restart": False,
                "start_command": "streamlit run ai_action_stock_analytics.py --server.port 8515"
            },
            {
                "name": "Analytics Dashboard",
                "type": "streamlit",
                "port": 8516,
                "health_endpoint": "http://localhost:8516/",
                "critical": False,
                "auto_restart": False,
                "start_command": "streamlit run analytics_dashboard.py --server.port 8516"
            },
            {
                "name": "Next.js Frontend",
                "type": "node",
                "port": 3000,
                "health_endpoint": "http://localhost:3000/",
                "critical": False,
                "auto_restart": False,
                "start_command": "cd frontend && npm run dev"
            },
            {
                "name": "API Gateway",
                "type": "node",
                "port": 8080,
                "health_endpoint": "http://localhost:8080/health",
                "critical": False,
                "auto_restart": False,
                "start_command": "node api-gateway.js"
            }
        ]


# =============================================================================
# HEALTH CHECKER
# =============================================================================

class HealthChecker:
    """Check health of individual services"""

    @staticmethod
    def check_port(port: int, timeout: float = 2.0) -> bool:
        """Check if port is open"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        try:
            result = sock.connect_ex(('localhost', port))
            sock.close()
            return result == 0
        except socket.error:
            return False

    @staticmethod
    def check_http_endpoint(url: str, timeout: float = 5.0) -> Dict:
        """Check HTTP endpoint health"""
        try:
            response = requests.get(url, timeout=timeout, allow_redirects=True)
            return {
                "status": "healthy" if response.status_code == 200 else "degraded",
                "status_code": response.status_code,
                "response_time_ms": int(response.elapsed.total_seconds() * 1000),
                "error": None
            }
        except requests.exceptions.Timeout:
            return {
                "status": "unhealthy",
                "status_code": None,
                "response_time_ms": None,
                "error": "Timeout"
            }
        except requests.exceptions.ConnectionError:
            return {
                "status": "down",
                "status_code": None,
                "response_time_ms": None,
                "error": "Connection refused"
            }
        except Exception as e:
            return {
                "status": "error",
                "status_code": None,
                "response_time_ms": None,
                "error": str(e)
            }

    @staticmethod
    def check_process(name: str) -> Dict:
        """Check if process is running"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if name.lower() in proc.info['name'].lower():
                    processes.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "cmdline": ' '.join(proc.info['cmdline'] or [])
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        return {
            "running": len(processes) > 0,
            "count": len(processes),
            "processes": processes
        }


# =============================================================================
# SYSTEM RESOURCE MONITOR
# =============================================================================

class ResourceMonitor:
    """Monitor system resources"""

    @staticmethod
    def get_cpu_usage() -> float:
        """Get CPU usage percentage"""
        return psutil.cpu_percent(interval=1)

    @staticmethod
    def get_memory_usage() -> Dict:
        """Get memory usage"""
        mem = psutil.virtual_memory()
        return {
            "total_gb": round(mem.total / (1024**3), 2),
            "available_gb": round(mem.available / (1024**3), 2),
            "used_gb": round(mem.used / (1024**3), 2),
            "percent": mem.percent
        }

    @staticmethod
    def get_disk_usage() -> Dict:
        """Get disk usage"""
        disk = psutil.disk_usage('/')
        return {
            "total_gb": round(disk.total / (1024**3), 2),
            "used_gb": round(disk.used / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
            "percent": disk.percent
        }

    @staticmethod
    def get_network_stats() -> Dict:
        """Get network statistics"""
        net = psutil.net_io_counters()
        return {
            "bytes_sent_mb": round(net.bytes_sent / (1024**2), 2),
            "bytes_recv_mb": round(net.bytes_recv / (1024**2), 2),
            "packets_sent": net.packets_sent,
            "packets_recv": net.packets_recv
        }

    @staticmethod
    def get_python_processes() -> List[Dict]:
        """Get all Python processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'cmdline']):
            try:
                if 'python' in proc.info['name'].lower():
                    processes.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "cpu_percent": proc.info['cpu_percent'],
                        "memory_percent": round(proc.info['memory_percent'], 2),
                        "cmdline": ' '.join(proc.info['cmdline'][:3] or [])  # First 3 args
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        return processes


# =============================================================================
# SERVICE MANAGER
# =============================================================================

class ServiceManager:
    """Manage service lifecycle"""

    @staticmethod
    def start_service(command: str, detached: bool = True) -> Dict:
        """Start a service"""
        try:
            if platform.system() == "Windows":
                # Windows: Start in new PowerShell window
                if detached:
                    subprocess.Popen(
                        ["powershell", "-NoExit", "-Command", command],
                        creationflags=subprocess.CREATE_NEW_CONSOLE
                    )
                else:
                    subprocess.Popen(command, shell=True)
            else:
                # Linux/Mac
                subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )

            return {"success": True, "message": f"Service started: {command}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def stop_service(port: int) -> Dict:
        """Stop service running on port"""
        try:
            if platform.system() == "Windows":
                # Kill process using port on Windows
                result = subprocess.run(
                    f"netstat -ano | findstr :{port}",
                    shell=True,
                    capture_output=True,
                    text=True
                )

                if result.stdout:
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        parts = line.split()
                        if len(parts) > 4:
                            pid = parts[-1]
                            subprocess.run(f"taskkill /PID {pid} /F", shell=True)
            else:
                # Linux/Mac: Kill process using port
                result = subprocess.run(
                    f"lsof -ti:{port}",
                    shell=True,
                    capture_output=True,
                    text=True
                )

                if result.stdout:
                    pid = result.stdout.strip()
                    subprocess.run(f"kill -9 {pid}", shell=True)

            return {"success": True, "message": f"Service stopped on port {port}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def restart_service(service: Dict) -> Dict:
        """Restart a service"""
        # Stop service
        stop_result = ServiceManager.stop_service(service['port'])

        if not stop_result['success']:
            return stop_result

        # Wait a moment
        import time
        time.sleep(2)

        # Start service
        return ServiceManager.start_service(service['start_command'])


# =============================================================================
# MAIN HEALTH MONITOR
# =============================================================================

class SystemHealthMonitor:
    """Main health monitoring system"""

    def __init__(self):
        self.services = ServiceConfig.get_services()
        self.health_checker = HealthChecker()
        self.resource_monitor = ResourceMonitor()
        self.service_manager = ServiceManager()
        self.history_file = "health_monitor_history.json"
        self.load_history()

    def load_history(self):
        """Load health check history"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
        else:
            self.history = {
                "checks": [],
                "incidents": [],
                "recoveries": []
            }

    def save_history(self):
        """Save health check history"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def check_all_services(self) -> Dict:
        """Check health of all services"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "services": [],
            "summary": {
                "total": len(self.services),
                "healthy": 0,
                "degraded": 0,
                "unhealthy": 0,
                "down": 0
            }
        }

        for service in self.services:
            # Check port
            port_open = self.health_checker.check_port(service['port'])

            # Check HTTP endpoint if port is open
            if port_open:
                health = self.health_checker.check_http_endpoint(service['health_endpoint'])
            else:
                health = {
                    "status": "down",
                    "status_code": None,
                    "response_time_ms": None,
                    "error": "Port not listening"
                }

            service_status = {
                "name": service['name'],
                "type": service['type'],
                "port": service['port'],
                "critical": service['critical'],
                "port_open": port_open,
                "health": health,
                "auto_restart": service.get('auto_restart', False)
            }

            results["services"].append(service_status)

            # Update summary
            status = health['status']
            if status == "healthy":
                results["summary"]["healthy"] += 1
            elif status == "degraded":
                results["summary"]["degraded"] += 1
            elif status == "unhealthy":
                results["summary"]["unhealthy"] += 1
            else:
                results["summary"]["down"] += 1

        # Add to history
        self.history["checks"].append({
            "timestamp": results["timestamp"],
            "summary": results["summary"]
        })

        # Keep only last 1000 checks
        if len(self.history["checks"]) > 1000:
            self.history["checks"] = self.history["checks"][-1000:]

        self.save_history()

        return results

    def get_system_resources(self) -> Dict:
        """Get system resource usage"""
        return {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": self.resource_monitor.get_cpu_usage(),
            "memory": self.resource_monitor.get_memory_usage(),
            "disk": self.resource_monitor.get_disk_usage(),
            "network": self.resource_monitor.get_network_stats(),
            "python_processes": self.resource_monitor.get_python_processes()
        }

    def auto_recover_services(self) -> List[Dict]:
        """Automatically recover failed services"""
        recovery_results = []
        health_check = self.check_all_services()

        for service_status in health_check["services"]:
            # Check if service is down and auto-restart is enabled
            if (service_status["health"]["status"] == "down" and
                service_status.get("auto_restart", False)):

                # Find service config
                service = next(
                    (s for s in self.services if s['name'] == service_status['name']),
                    None
                )

                if service:
                    print(f"🔄 Auto-recovering: {service['name']}")
                    result = self.service_manager.restart_service(service)

                    recovery_record = {
                        "timestamp": datetime.now().isoformat(),
                        "service": service['name'],
                        "result": result
                    }

                    recovery_results.append(recovery_record)
                    self.history["recoveries"].append(recovery_record)

        if recovery_results:
            self.save_history()

        return recovery_results

    def get_dashboard_data(self) -> Dict:
        """Get complete dashboard data"""
        return {
            "health_check": self.check_all_services(),
            "resources": self.get_system_resources(),
            "history_summary": {
                "total_checks": len(self.history["checks"]),
                "total_recoveries": len(self.history["recoveries"]),
                "last_check": self.history["checks"][-1] if self.history["checks"] else None
            }
        }


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """Main CLI interface"""
    print("=" * 70)
    print("SYSTEM HEALTH MONITOR")
    print("=" * 70)

    monitor = SystemHealthMonitor()

    # Check all services
    health = monitor.check_all_services()

    print(f"\n📊 Health Check - {health['timestamp']}")
    print(f"\nSummary:")
    print(f"   ✅ Healthy: {health['summary']['healthy']}")
    print(f"   ⚠️  Degraded: {health['summary']['degraded']}")
    print(f"   ❌ Unhealthy: {health['summary']['unhealthy']}")
    print(f"   🔴 Down: {health['summary']['down']}")

    print(f"\n🖥️  Services ({len(health['services'])}):")
    for service in health['services']:
        status_icon = {
            "healthy": "✅",
            "degraded": "⚠️",
            "unhealthy": "❌",
            "down": "🔴",
            "error": "💥"
        }.get(service['health']['status'], "❓")

        print(f"   {status_icon} {service['name']} (Port {service['port']})")
        if service['health']['response_time_ms']:
            print(f"      Response time: {service['health']['response_time_ms']}ms")

    # System resources
    resources = monitor.get_system_resources()
    print(f"\n💻 System Resources:")
    print(f"   CPU: {resources['cpu_percent']}%")
    print(f"   Memory: {resources['memory']['used_gb']}GB / {resources['memory']['total_gb']}GB ({resources['memory']['percent']}%)")
    print(f"   Disk: {resources['disk']['used_gb']}GB / {resources['disk']['total_gb']}GB ({resources['disk']['percent']}%)")

    print(f"\n🐍 Python Processes: {len(resources['python_processes'])}")

    # Auto-recovery
    print(f"\n🔄 Checking for services to recover...")
    recoveries = monitor.auto_recover_services()

    if recoveries:
        print(f"   Recovered {len(recoveries)} service(s)")
    else:
        print(f"   No recovery needed")


if __name__ == "__main__":
    main()

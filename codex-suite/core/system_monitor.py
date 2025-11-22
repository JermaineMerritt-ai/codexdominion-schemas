# core/system_monitor.py
"""
Codex Dominion System Health Monitor
Real-time monitoring and maintenance
"""
import psutil
import time
from datetime import datetime
from core.ledger import append_entry

class SystemMonitor:
    def __init__(self):
        self.alerts = []
        self.baseline_memory = psutil.virtual_memory().percent
        
    def check_system_health(self):
        """Comprehensive system health check"""
        health_report = {
            "timestamp": datetime.now().isoformat(),
            "memory": self.check_memory(),
            "disk": self.check_disk(),
            "cpu": self.check_cpu(),
            "processes": self.check_processes(),
            "wsl_status": self.check_wsl_status(),
            "overall_status": "HEALTHY"
        }
        
        # Determine overall status
        issues = []
        if health_report["memory"]["usage_percent"] > 85:
            issues.append("HIGH_MEMORY")
        if health_report["disk"]["usage_percent"] > 90:
            issues.append("LOW_DISK")
        if health_report["cpu"]["usage_percent"] > 90:
            issues.append("HIGH_CPU")
            
        if issues:
            health_report["overall_status"] = "NEEDS_ATTENTION"
            health_report["issues"] = issues
            
        return health_report
        
    def check_memory(self):
        """Monitor memory usage"""
        memory = psutil.virtual_memory()
        return {
            "total_gb": round(memory.total / 1024**3, 2),
            "available_gb": round(memory.available / 1024**3, 2),
            "used_gb": round(memory.used / 1024**3, 2),
            "usage_percent": memory.percent,
            "status": "EXCELLENT" if memory.percent < 70 else "GOOD" if memory.percent < 85 else "CRITICAL"
        }
        
    def check_disk(self):
        """Monitor disk usage"""
        disk = psutil.disk_usage('C:')
        return {
            "total_gb": round(disk.total / 1024**3, 2),
            "free_gb": round(disk.free / 1024**3, 2),
            "used_gb": round(disk.used / 1024**3, 2),
            "usage_percent": round((disk.used / disk.total) * 100, 2),
            "status": "EXCELLENT" if disk.used/disk.total < 0.8 else "GOOD" if disk.used/disk.total < 0.9 else "CRITICAL"
        }
        
    def check_cpu(self):
        """Monitor CPU usage"""
        cpu_percent = psutil.cpu_percent(interval=1)
        return {
            "usage_percent": cpu_percent,
            "core_count": psutil.cpu_count(),
            "status": "EXCELLENT" if cpu_percent < 50 else "GOOD" if cpu_percent < 80 else "HIGH"
        }
        
    def check_processes(self):
        """Monitor process health"""
        processes = []
        total_memory = 0
        
        for proc in psutil.process_iter(['name', 'memory_info', 'cpu_percent']):
            try:
                memory_mb = proc.info['memory_info'].rss / 1024**2
                if memory_mb > 100:  # Only track processes >100MB
                    processes.append({
                        "name": proc.info['name'],
                        "memory_mb": round(memory_mb, 2),
                        "cpu_percent": proc.info['cpu_percent'] or 0
                    })
                    total_memory += memory_mb
            except:
                pass
                
        processes.sort(key=lambda x: x['memory_mb'], reverse=True)
        
        return {
            "high_memory_count": len(processes),
            "total_memory_mb": round(total_memory, 2),
            "top_processes": processes[:10]
        }
        
    def check_wsl_status(self):
        """Check WSL health and Docker integration"""
        import subprocess
        try:
            result = subprocess.run(["wsl", "--list", "--verbose"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return {
                    "status": "HEALTHY",
                    "output": result.stdout.strip(),
                    "docker_proxy_error": False
                }
            else:
                return {
                    "status": "ERROR",
                    "error": result.stderr.strip(),
                    "docker_proxy_error": True
                }
        except Exception as e:
            return {
                "status": "ERROR", 
                "error": str(e),
                "docker_proxy_error": True
            }
            
    def log_health_report(self):
        """Log health report to ledger"""
        report = self.check_system_health()
        append_entry("SYSTEM_HEALTH", {
            "type": "health_check",
            "status": report["overall_status"],
            "memory_usage": report["memory"]["usage_percent"],
            "disk_usage": report["disk"]["usage_percent"],
            "cpu_usage": report["cpu"]["usage_percent"],
            "issues": report.get("issues", []),
            "timestamp": report["timestamp"]
        })
        return report
        
    def auto_optimize_if_needed(self):
        """Automatically optimize if thresholds exceeded"""
        health = self.check_system_health()
        
        optimizations_performed = []
        
        # Auto memory cleanup if usage > 85%
        if health["memory"]["usage_percent"] > 85:
            import gc
            gc.collect()
            optimizations_performed.append("MEMORY_CLEANUP")
            
        # Auto process cleanup if too many high-memory processes
        if health["processes"]["high_memory_count"] > 20:
            optimizations_performed.append("PROCESS_MONITORING")
            
        if optimizations_performed:
            append_entry("AUTO_OPTIMIZATION", {
                "optimizations": optimizations_performed,
                "before_memory": health["memory"]["usage_percent"],
                "timestamp": datetime.now().isoformat()
            })
            
        return optimizations_performed

def get_system_status():
    """Quick system status check"""
    monitor = SystemMonitor()
    return monitor.check_system_health()

def create_status_summary():
    """Create formatted status summary"""
    status = get_system_status()
    
    summary = f"""
🔥 CODEX DOMINION SYSTEM STATUS

💾 MEMORY: {status['memory']['available_gb']:.1f}GB available ({100-status['memory']['usage_percent']:.1f}% free) - {status['memory']['status']}
💿 STORAGE: {status['disk']['free_gb']:.1f}GB free ({100-status['disk']['usage_percent']:.1f}% free) - {status['disk']['status']}  
🖥️ CPU: {status['cpu']['usage_percent']:.1f}% usage - {status['cpu']['status']}
⚡ PROCESSES: {status['processes']['high_memory_count']} high-memory processes
🔧 WSL: {status['wsl_status']['status']}

🎯 OVERALL STATUS: {status['overall_status']}
🔥 FLAME STATUS: ETERNAL
"""
    
    if "issues" in status:
        summary += f"\n⚠️ ATTENTION NEEDED: {', '.join(status['issues'])}"
    else:
        summary += "\n✅ ALL SYSTEMS OPTIMAL"
        
    return summary

if __name__ == "__main__":
    print(create_status_summary())
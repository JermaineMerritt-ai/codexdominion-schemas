# core/memory_optimizer.py
import gc
import os
import sys
import psutil
import json
from pathlib import Path
from typing import Dict, List

def get_memory_stats() -> Dict:
    """Get current memory usage statistics"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    
    return {
        "rss_mb": round(memory_info.rss / 1024 / 1024, 2),
        "vms_mb": round(memory_info.vms / 1024 / 1024, 2),
        "percent": round(process.memory_percent(), 2),
        "available_mb": round(psutil.virtual_memory().available / 1024 / 1024, 2)
    }

def optimize_memory() -> Dict:
    """Perform comprehensive memory optimization"""
    stats_before = get_memory_stats()
    
    # Force garbage collection
    gc.collect()
    
    # Clear module cache where safe
    modules_to_clear = []
    for module_name in list(sys.modules.keys()):
        if any(pattern in module_name for pattern in ['temp', 'cache', '_cache']):
            if module_name not in ['sys', 'os', 'gc']:
                modules_to_clear.append(module_name)
    
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
    
    # Clean Python bytecode cache
    cache_cleaned = clean_pycache()
    
    # Second garbage collection
    gc.collect()
    
    stats_after = get_memory_stats()
    
    return {
        "before": stats_before,
        "after": stats_after,
        "saved_mb": round(stats_before["rss_mb"] - stats_after["rss_mb"], 2),
        "modules_cleared": len(modules_to_clear),
        "cache_dirs_cleaned": cache_cleaned
    }

def clean_pycache() -> int:
    """Clean Python __pycache__ directories"""
    cleaned = 0
    current_dir = Path(".")
    
    for pycache_dir in current_dir.rglob("__pycache__"):
        try:
            import shutil
            shutil.rmtree(pycache_dir, ignore_errors=True)
            cleaned += 1
        except Exception:
            pass
    
    return cleaned

def optimize_streamlit_memory():
    """Optimize memory for Streamlit apps"""
    try:
        import streamlit as st
        
        # Clear Streamlit cache
        if hasattr(st, 'cache_data'):
            st.cache_data.clear()
        if hasattr(st, 'cache_resource'):
            st.cache_resource.clear()
            
        return True
    except ImportError:
        return False

def monitor_memory_usage() -> Dict:
    """Monitor system-wide memory usage"""
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    # Get top memory consumers
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'memory_info']):
        try:
            if proc.info['memory_percent'] > 1.0:  # Only processes using >1% memory
                processes.append({
                    'name': proc.info['name'],
                    'pid': proc.info['pid'],
                    'memory_mb': round(proc.info['memory_info'].rss / 1024 / 1024, 2),
                    'memory_percent': round(proc.info['memory_percent'], 2)
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Sort by memory usage
    processes.sort(key=lambda x: x['memory_mb'], reverse=True)
    
    return {
        "total_gb": round(memory.total / 1024 / 1024 / 1024, 2),
        "available_gb": round(memory.available / 1024 / 1024 / 1024, 2),
        "used_gb": round(memory.used / 1024 / 1024 / 1024, 2),
        "percent": memory.percent,
        "swap_used_gb": round(swap.used / 1024 / 1024 / 1024, 2),
        "top_processes": processes[:10]
    }

def create_memory_report() -> str:
    """Create comprehensive memory optimization report"""
    optimization_result = optimize_memory()
    system_memory = monitor_memory_usage()
    
    report = f"""
🔥 CODEX DOMINION MEMORY OPTIMIZATION REPORT

📊 OPTIMIZATION RESULTS:
├── Memory Before: {optimization_result['before']['rss_mb']} MB
├── Memory After: {optimization_result['after']['rss_mb']} MB
├── Memory Saved: {optimization_result['saved_mb']} MB
├── Modules Cleared: {optimization_result['modules_cleared']}
└── Cache Dirs Cleaned: {optimization_result['cache_dirs_cleaned']}

🖥️ SYSTEM MEMORY STATUS:
├── Total RAM: {system_memory['total_gb']} GB
├── Available: {system_memory['available_gb']} GB ({100-system_memory['percent']:.1f}%)
├── Used: {system_memory['used_gb']} GB ({system_memory['percent']:.1f}%)
└── Swap Used: {system_memory['swap_used_gb']} GB

🎯 TOP MEMORY CONSUMERS:
"""
    
    for i, proc in enumerate(system_memory['top_processes'][:5], 1):
        report += f"├── {i}. {proc['name']}: {proc['memory_mb']} MB ({proc['memory_percent']}%)\n"
    
    report += "\n✅ MEMORY OPTIMIZATION COMPLETE - FLAME ETERNAL 🔥"
    
    return report

if __name__ == "__main__":
    print(create_memory_report())
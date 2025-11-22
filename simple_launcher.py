"""
Simple Codex Dashboard Launcher
ASCII-only version for compatibility
"""

import subprocess
import sys
import time
import socket
import os
from pathlib import Path
import logging

# Simple logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

def check_port_availability(port):
    """Check if port is available"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result != 0
    except Exception:
        return False

def kill_port_processes(port):
    """Kill processes using specified port"""
    try:
        if sys.platform == "win32":
            subprocess.run(f'netstat -ano | findstr :{port}', shell=True, capture_output=True)
            # Simple approach - kill all python processes (be careful in production!)
            subprocess.run('taskkill /f /im python.exe /t', shell=True, capture_output=True)
        time.sleep(2)
    except Exception as e:
        logger.warning(f"Could not clean port {port}: {e}")

def launch_monetization_crown():
    """Launch the Enhanced Monetization Crown dashboard"""
    port = 8503
    
    logger.info("Starting Enhanced Monetization Crown Dashboard...")
    
    # Clean port if needed
    if not check_port_availability(port):
        logger.info(f"Port {port} in use, cleaning...")
        kill_port_processes(port)
    
    # Find available port
    while not check_port_availability(port) and port < 8600:
        port += 1
    
    if port >= 8600:
        logger.error("No available ports found")
        return False
    
    # Launch dashboard
    try:
        cmd = [
            sys.executable, '-m', 'streamlit', 'run',
            'monetization_crown.py',
            '--server.port', str(port),
            '--server.address', '127.0.0.1',
            '--server.headless', 'true',
            '--browser.gatherUsageStats', 'false'
        ]
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        logger.info(f"SUCCESS: Enhanced Monetization Crown launched on port {port}")
        logger.info(f"ACCESS: http://127.0.0.1:{port}")
        
        return process, port
        
    except Exception as e:
        logger.error(f"Failed to launch monetization crown: {e}")
        return False

def launch_portfolio_dashboard():
    """Launch the Portfolio Management dashboard"""
    port = 8501
    
    logger.info("Starting Portfolio Management Dashboard...")
    
    # Find available port
    while not check_port_availability(port) and port < 8600:
        port += 1
    
    if port >= 8600:
        logger.error("No available ports found")
        return False
    
    # Launch dashboard
    try:
        cmd = [
            sys.executable, '-m', 'streamlit', 'run',
            'codex_portfolio_dashboard.py',
            '--server.port', str(port),
            '--server.address', '127.0.0.1',
            '--server.headless', 'true',
            '--browser.gatherUsageStats', 'false'
        ]
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        logger.info(f"SUCCESS: Portfolio Dashboard launched on port {port}")
        logger.info(f"ACCESS: http://127.0.0.1:{port}")
        
        return process, port
        
    except Exception as e:
        logger.error(f"Failed to launch portfolio dashboard: {e}")
        return False

def main():
    """Main launcher"""
    print("Codex Dominion Dashboard Launcher")
    print("=" * 50)
    
    processes = []
    
    # Launch Enhanced Monetization Crown
    result1 = launch_monetization_crown()
    if result1:
        processes.append(result1)
        time.sleep(3)  # Stagger launches
    
    # Launch Portfolio Dashboard
    result2 = launch_portfolio_dashboard()
    if result2:
        processes.append(result2)
    
    if processes:
        print(f"\nSUCCESS: {len(processes)} dashboard(s) launched!")
        print("\nACCESS URLs:")
        for process, port in processes:
            print(f"  http://127.0.0.1:{port}")
        
        print("\nPress Ctrl+C to stop all dashboards")
        
        try:
            while True:
                time.sleep(10)
                # Check if processes are still running
                for i, (process, port) in enumerate(processes):
                    if process.poll() is not None:
                        logger.error(f"Dashboard on port {port} terminated")
                        
        except KeyboardInterrupt:
            print("\nShutting down dashboards...")
            for process, port in processes:
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except Exception as e:
                    logger.warning(f"Error stopping process on port {port}: {e}")
            
            print("All dashboards stopped. Goodbye!")
    else:
        print("FAILED: No dashboards launched successfully")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
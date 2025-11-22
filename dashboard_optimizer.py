#!/usr/bin/env python3
"""
Dashboard Enhancement Script
===========================
Applies performance optimizations to specific Codex dashboard files
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path

class DashboardOptimizer:
    """Optimize existing dashboard files with performance enhancements"""
    
    def __init__(self, base_path=None):
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.optimizations_applied = []
    
    def optimize_all_dashboards(self):
        """Apply optimizations to all dashboard files"""
        print("OPTIMIZING CODEX DASHBOARDS")
        print("=" * 40)
        
        # Find all Python dashboard files
        dashboard_files = list(self.base_path.glob("*dashboard*.py"))
        dashboard_files.extend(list(self.base_path.glob("*_crown.py")))
        dashboard_files.extend(list(self.base_path.glob("*analytics*.py")))
        
        for file_path in dashboard_files:
            if file_path.name.startswith("enhanced_"):
                continue  # Skip already enhanced files
            
            print(f"\nOptimizing: {file_path.name}")
            self.optimize_dashboard_file(file_path)
        
        self.generate_optimization_report()
    
    def optimize_dashboard_file(self, file_path: Path):
        """Optimize a single dashboard file"""
        try:
            # Read original file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Apply optimizations
            optimized_content = self.apply_optimizations(content)
            
            # Create enhanced version
            enhanced_name = f"enhanced_{file_path.name}"
            enhanced_path = file_path.parent / enhanced_name
            
            with open(enhanced_path, 'w', encoding='utf-8') as f:
                f.write(optimized_content)
            
            print(f"  -> Created enhanced version: {enhanced_name}")
            self.optimizations_applied.append(str(file_path.name))
            
        except Exception as e:
            print(f"  -> Error optimizing {file_path.name}: {e}")
    
    def apply_optimizations(self, content: str) -> str:
        """Apply specific optimizations to dashboard content"""
        
        # Add performance monitoring imports
        imports_section = '''"""
Enhanced Dashboard with Performance Optimizations
===============================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from pathlib import Path
import time
from functools import wraps

# Performance monitoring decorator
def performance_monitor(operation_name=None):
    """Monitor performance of functions"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Store performance data
                if 'performance_data' not in st.session_state:
                    st.session_state.performance_data = {}
                
                op_name = operation_name or func.__name__
                if op_name not in st.session_state.performance_data:
                    st.session_state.performance_data[op_name] = []
                
                st.session_state.performance_data[op_name].append(execution_time)
                
                # Keep only last 100 measurements
                if len(st.session_state.performance_data[op_name]) > 100:
                    st.session_state.performance_data[op_name] = st.session_state.performance_data[op_name][-100:]
                
                return result
            except Exception as e:
                st.error(f"Error in {operation_name or func.__name__}: {str(e)}")
                raise
        return wrapper
    return decorator

# Enhanced data loading with caching
@st.cache_data(ttl=300)  # Cache for 5 minutes
@performance_monitor("load_json_file")
def load_json_enhanced(filename, default_data):
    """Enhanced JSON loading with caching and error handling"""
    try:
        path = Path(filename)
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data if data else default_data
        else:
            return default_data
    except Exception as e:
        st.error(f"Error loading {filename}: {str(e)}")
        return default_data

# Performance dashboard component
def show_performance_dashboard():
    """Show performance statistics"""
    if 'performance_data' in st.session_state and st.session_state.performance_data:
        with st.expander("Performance Dashboard"):
            st.subheader("Operation Performance")
            
            for operation, times in st.session_state.performance_data.items():
                if times:
                    avg_time = sum(times) / len(times)
                    max_time = max(times)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(f"{operation} Avg", f"{avg_time:.3f}s")
                    with col2:
                        st.metric("Max", f"{max_time:.3f}s")
                    with col3:
                        st.metric("Calls", len(times))

# Enhanced styling
def apply_enhanced_styling():
    """Apply enhanced styling"""
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    .enhanced-header {
        text-align: center;
        padding: 30px;
        margin-bottom: 30px;
        background: linear-gradient(45deg, rgba(138,43,226,0.4), rgba(75,0,130,0.3));
        border: 2px solid #8B2BE2;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(138,43,226,0.3);
    }
    
    .enhanced-card {
        background: rgba(255,255,255,0.1);
        padding: 25px;
        border-radius: 20px;
        border: 2px solid rgba(138,43,226,0.3);
        backdrop-filter: blur(15px);
        margin: 15px 0;
        transition: all 0.4s ease;
    }
    
    .enhanced-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 40px rgba(138,43,226,0.4);
        border-color: #8B2BE2;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #8B2BE2, #9370DB);
        border: none;
        border-radius: 15px;
        color: white;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #9370DB, #8B2BE2);
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(138,43,226,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

'''
        
        # Replace basic imports with enhanced imports
        if 'import streamlit as st' in content:
            # Find the end of imports section
            lines = content.split('\n')
            import_end = 0
            
            for i, line in enumerate(lines):
                if line.strip() and not (line.startswith('import ') or line.startswith('from ') or line.startswith('#') or line.startswith('"""') or line.startswith("'''")):
                    import_end = i
                    break
            
            # Insert enhanced imports at the beginning
            enhanced_content = imports_section + '\n'.join(lines[import_end:])
        else:
            enhanced_content = imports_section + '\n\n' + content
        
        # Add performance monitoring to main functions
        enhanced_content = self.add_performance_monitoring(enhanced_content)
        
        # Add enhanced styling calls
        enhanced_content = self.add_styling_calls(enhanced_content)
        
        return enhanced_content
    
    def add_performance_monitoring(self, content: str) -> str:
        """Add performance monitoring to key functions"""
        
        # Find and enhance load_json functions
        content = re.sub(
            r'def load_json\(([^)]*)\):',
            r'@performance_monitor("load_json")\ndef load_json(\1):',
            content
        )
        
        # Find and enhance main dashboard functions
        content = re.sub(
            r'def (show_|render_|display_)([^(]*)\(([^)]*)\):',
            r'@performance_monitor("\1\2")\ndef \1\2(\3):',
            content
        )
        
        return content
    
    def add_styling_calls(self, content: str) -> str:
        """Add enhanced styling calls"""
        
        # Find st.title or st.header calls and add styling before them
        if 'st.title(' in content or 'st.header(' in content:
            lines = content.split('\n')
            enhanced_lines = []
            
            for line in lines:
                if 'st.title(' in line or 'st.header(' in line:
                    enhanced_lines.append('    # Apply enhanced styling')
                    enhanced_lines.append('    apply_enhanced_styling()')
                    enhanced_lines.append('')
                
                enhanced_lines.append(line)
            
            content = '\n'.join(enhanced_lines)
        
        return content
    
    def generate_optimization_report(self):
        """Generate optimization report"""
        print(f"\nOPTIMIZATION COMPLETE!")
        print(f"Enhanced {len(self.optimizations_applied)} dashboard files:")
        
        for file_name in self.optimizations_applied:
            print(f"  -> {file_name} -> enhanced_{file_name}")
        
        print(f"\nOptimizations Applied:")
        print("  - Performance monitoring decorators")
        print("  - Enhanced data loading with caching")
        print("  - Advanced UI styling and animations")
        print("  - Error handling and validation")
        print("  - Real-time performance dashboard")
        
        # Save optimization report
        report = {
            "timestamp": datetime.now().isoformat(),
            "files_optimized": self.optimizations_applied,
            "total_files": len(self.optimizations_applied),
            "optimizations": [
                "Performance monitoring",
                "Data caching",
                "Enhanced styling",
                "Error handling",
                "Performance dashboard"
            ]
        }
        
        report_path = self.base_path / "DASHBOARD_OPTIMIZATION_REPORT.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"\nReport saved: {report_path}")

if __name__ == "__main__":
    optimizer = DashboardOptimizer()
    optimizer.optimize_all_dashboards()
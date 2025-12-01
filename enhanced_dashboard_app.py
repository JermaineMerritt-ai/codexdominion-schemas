"""
Enhanced Dashboard with Performance Optimizations
===============================================
"""

import json
import time
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


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
@performance_monitor("show_performance_dashboard")
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

🌍 CODEX DOMINION DASHBOARD - Digital Empire Command Center
Supreme dashboard for monitoring and controlling the entire digital empire
Production URL: https://aistorelab.com | Staging: https://staging.aistorelab.com
"""

import streamlit as st
import json
import time
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import yaml
import subprocess
import sys
import os
from typing import Dict, List, Any

# Configure page
st.set_page_config(
    page_title="Codex Dominion - Digital Empire Dashboard",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

class CodexDashboard:
    """Comprehensive digital empire dashboard."""
    
    def __init__(self):
        self.workspace_root = Path(__file__).parent
        self.load_empire_data()
    
    def load_empire_data(self):
        """Load all empire data from configuration files."""
        try:
            # Load configuration files
            with open(self.workspace_root / "config" / "app.config.json", "r") as f:
                self.app_config = json.load(f)
            
            with open(self.workspace_root / "cycles.json", "r") as f:
                self.cycles_data = json.load(f)
            
            with open(self.workspace_root / "ledger.json", "r") as f:
                self.ledger_data = json.load(f)
            
            with open(self.workspace_root / "heartbeat.json", "r") as f:
                self.heartbeat_data = json.load(f)
                
            # Load dashboard capsule configurations
            self.capsules_data = self.load_dashboard_capsules()
            
        except Exception as e:
            st.error(f"Error loading empire data: {str(e)}")
            # Set default values if files don't exist
            self.app_config = {"app": {"name": "Codex Dominion", "version": "1.0.0"}}
            self.cycles_data = []
            self.ledger_data = []
            self.heartbeat_data = {"status": "Unknown"}
            self.capsules_data = {}
    
    def load_dashboard_capsules(self) -> Dict:
        """Load dashboard capsule configurations."""
        capsules = {}
        dashboard_dir = self.workspace_root / "apps" / "dashboard"
        
        if dashboard_dir.exists():
            for capsule_file in dashboard_dir.glob("*_capsule.yaml"):
                try:
                    with open(capsule_file, "r", encoding="utf-8") as f:
                        capsule_data = yaml.safe_load(f)
                        capsule_name = capsule_file.stem.replace("_capsule", "")
                        capsules[capsule_name] = capsule_data
                except Exception as e:
                    st.warning(f"Could not load {capsule_file.name}: {str(e)}")
        
        return capsules
    
    @performance_monitor("render_header")
def render_header(self):
        """Render dashboard header with empire status."""
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
    # Apply enhanced styling
    apply_enhanced_styling()

            st.title("👑 Codex Dominion - Digital Empire")
            st.caption(f"v{self.app_config.get('app', {}).get('version', '1.0.0')} | Command Center")
        
        with col2:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.metric("🕐 Current Time", current_time)
        
        with col3:
            empire_status = self.heartbeat_data.get("status", "SUPREME").upper()
            status_color = "🟢" if empire_status == "SUPREME" else "🟡"
            st.metric("🏛️ Empire Status", f"{status_color} {empire_status}")
    
    @performance_monitor("render_empire_overview")
def render_empire_overview(self):
        """Render empire overview metrics."""
        st.subheader("🌟 Empire Overview")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("🎬 Video Studio", "OMEGA", help="Video Studio Omega - GenSpark Obliterator")
        
        with col2:
            st.metric("🚀 Web Development", "DESTROYER", help="Lovable Destroyer - Web Dev Revolution")
        
        with col3:
            st.metric("⚡ Automation", "FLOW ENGINE", help="Codex Flow Engine - N8N Annihilator")
        
        with col4:
            st.metric("🌐 Hosting Empire", "IONOS", help="IONOS Dominion Manager")
        
        with col5:
            active_systems = len([k for k, v in self.app_config.get("features", {}).items() if v])
            st.metric("⚙️ Active Systems", active_systems)
    
    @performance_monitor("render_performance_dashboard")
def render_performance_dashboard(self):
        """Render system performance metrics."""
        st.subheader("📊 Performance Dashboard")
        
        # Create performance metrics charts
        col1, col2 = st.columns(2)
        
        with col1:
            # System Performance Chart
            performance_data = {
                "System": ["Video Studio", "Web Dev", "Automation", "Hosting", "AI Models"],
                "Performance": [98.5, 97.2, 99.1, 96.8, 99.9],
                "Target": [95, 95, 95, 95, 95]
            }
            
            df_performance = pd.DataFrame(performance_data)
            fig_performance = px.bar(
                df_performance, 
                x="System", 
                y="Performance",
                title="System Performance vs Target",
                color="Performance",
                color_continuous_scale="Viridis"
            )
            fig_performance.add_scatter(
                x=df_performance["System"],
                y=df_performance["Target"],
                mode="markers",
                marker=dict(color="red", size=10),
                name="Target"
            )
            st.plotly_chart(fig_performance, use_container_width=True)
        
        with col2:
            # Competitive Advantage Chart
            competitive_data = {
                "Competitor": ["GenSpark", "Lovable", "N8N", "Zapier", "NotebookLLM"],
                "Advantage_Multiplier": [10.0, 8.5, 5.0, 4.2, 12.0]
            }
            
            df_competitive = pd.DataFrame(competitive_data)
            fig_competitive = px.pie(
                df_competitive,
                values="Advantage_Multiplier",
                names="Competitor",
                title="Competitive Obliteration Matrix"
            )
            st.plotly_chart(fig_competitive, use_container_width=True)
    
    @performance_monitor("render_empire_ledger")
def render_empire_ledger(self):
        """Render empire operations ledger."""
        st.subheader("📖 Empire Operations Ledger")
        
        if self.ledger_data:
            # Convert to DataFrame for better display
            df_ledger = pd.DataFrame(self.ledger_data)
            
            # Display as interactive table
            st.dataframe(
                df_ledger[['date', 'entry', 'custodian']],
                use_container_width=True,
                hide_index=True
            )
            
            # Achievement timeline
            fig_timeline = px.scatter(
                df_ledger,
                x='date',
                y=range(len(df_ledger)),
                hover_data=['entry'],
                title="Achievement Timeline",
                size=[100] * len(df_ledger)
            )
            fig_timeline.update_layout(yaxis_title="Achievement Order")
            st.plotly_chart(fig_timeline, use_container_width=True)
        else:
            st.info("No ledger entries found. Empire achievements will appear here.")
    
    @performance_monitor("render_dashboard_capsules")
def render_dashboard_capsules(self):
        """Render dashboard capsules status."""
        st.subheader("💊 Dashboard Capsules Status")
        
        if self.capsules_data:
            capsule_cols = st.columns(3)
            
            for idx, (capsule_name, capsule_data) in enumerate(self.capsules_data.items()):
                col = capsule_cols[idx % 3]
                
                with col:
                    with st.container():
                        st.write(f"**{capsule_data.get('capsule', {}).get('name', capsule_name.title())}**")
                        
                        capsule_type = capsule_data.get('capsule', {}).get('type', 'unknown')
                        version = capsule_data.get('capsule', {}).get('version', '1.0.0')
                        
                        st.caption(f"Type: {capsule_type} | v{version}")
                        
                        description = capsule_data.get('capsule', {}).get('description', 'No description')
                        if len(description) > 100:
                            description = description[:100] + "..."
                        st.write(description)
                        
                        # Status indicator
                        if capsule_data.get('deployment'):
                            st.success("✅ Configured")
                        else:
                            st.warning("⚠️ Needs Setup")
        else:
            st.info("No capsules configured yet. Deploy capsules to see status here.")
    
    @performance_monitor("render_system_cycles")
def render_system_cycles(self):
        """Render system cycles and seasons."""
        st.subheader("🔄 System Cycles & Seasons")
        
        if self.cycles_data:
            df_cycles = pd.DataFrame(self.cycles_data)
            
            # Timeline visualization
            fig_cycles = px.timeline(
                df_cycles,
                x_start='date',
                x_end='date',
                y='season',
                color='cycle',
                title="Digital Empire Seasonal Cycles"
            )
            st.plotly_chart(fig_cycles, use_container_width=True)
            
            # Current cycle indicator
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            current_cycle = None
            
            for cycle in self.cycles_data:
                if cycle['date'] <= current_date:
                    current_cycle = cycle
            
            if current_cycle:
                st.info(f"🌟 Current Cycle: **{current_cycle['cycle']}** ({current_cycle['season']})")
        else:
            st.info("No cycle data found. System cycles will appear here.")
    
    @performance_monitor("render_quick_actions")
def render_quick_actions(self):
        """Render quick action buttons."""
        st.subheader("⚡ Quick Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🎬 Launch Video Studio"):
                st.success("Video Studio Omega launching...")
                # Add actual command execution here
        
        with col2:
            if st.button("🚀 Deploy Website"):
                st.success("Lovable Destroyer activating...")
                # Add actual command execution here
        
        with col3:
            if st.button("⚡ Run Automation"):
                st.success("Codex Flow Engine starting...")
                # Add actual command execution here
        
        with col4:
            if st.button("📊 Generate Report"):
                st.success("Empire status report generating...")
                # Add actual command execution here
    
    @performance_monitor("render_ssl_monitoring")
def render_ssl_monitoring(self):
        """Render SSL certificate monitoring."""
        st.subheader("🔐 SSL Certificate Monitoring")
        
        domains = self.app_config.get("domains", {})
        
        ssl_data = []
        for domain_type, domain_url in domains.items():
            # Mock SSL status - in production, check actual certificates
            ssl_data.append({
                "Domain": domain_url,
                "Type": domain_type.title(),
                "Status": "✅ Valid",
                "Expires": "2024-12-15",
                "Days_Remaining": 45
            })
        
        if ssl_data:
            df_ssl = pd.DataFrame(ssl_data)
            st.dataframe(df_ssl, use_container_width=True, hide_index=True)
        else:
            st.info("No SSL certificates configured.")
    
    @performance_monitor("render_sidebar")
def render_sidebar(self):
        """Render sidebar navigation."""
        st.sidebar.title("🏛️ Empire Control")
        
        # Navigation
        page = st.sidebar.selectbox(
            "Select Dashboard View",
            ["🏠 Overview", "📊 Performance", "💊 Capsules", "🔄 Cycles", "🔐 Security", "📖 Ledger"]
        )
        
        st.sidebar.divider()
        
        # Quick stats
        st.sidebar.subheader("⚡ Quick Stats")
        st.sidebar.metric("🎯 Uptime", "99.9%")
        st.sidebar.metric("⚡ Performance", "98.5%")
        st.sidebar.metric("🛡️ Security", "MAXIMUM")
        
        # System info
        st.sidebar.subheader("🔧 System Info")
        st.sidebar.caption(f"Version: {self.app_config.get('app', {}).get('version', '1.0.0')}")
        st.sidebar.caption(f"Environment: {self.app_config.get('app', {}).get('environment', 'production')}")
        st.sidebar.caption(f"Last Updated: {datetime.datetime.now().strftime('%H:%M')}")
        
        return page
    
    @performance_monitor("render_dashboard")
def render_dashboard(self):
        """Main dashboard rendering function."""
        page = self.render_sidebar()
        self.render_header()
        
        st.divider()
        
        # Route to different pages based on selection
        if page == "🏠 Overview":
            self.render_empire_overview()
            st.divider()
            self.render_quick_actions()
        
        elif page == "📊 Performance":
            self.render_performance_dashboard()
        
        elif page == "💊 Capsules":
            self.render_dashboard_capsules()
        
        elif page == "🔄 Cycles":
            self.render_system_cycles()
        
        elif page == "🔐 Security":
            self.render_ssl_monitoring()
        
        elif page == "📖 Ledger":
            self.render_empire_ledger()
        
        # Footer
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col2:
            st.caption("👑 **Codex Dominion Digital Empire** - Supreme Automation Platform")

def main():
    """Main dashboard application."""
    dashboard = CodexDashboard()
    dashboard.render_dashboard()

if __name__ == "__main__":
    main()
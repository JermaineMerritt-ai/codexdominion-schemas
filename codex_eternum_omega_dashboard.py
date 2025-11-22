#!/usr/bin/env python3
"""
🌀 CODEX ETERNUM OMEGA DASHBOARD - Sovereign Control Interface
Ultimate dashboard for Codex Eternum Omega sovereign operations and eternal replay management
Custodian: Jermaine of Waxhaw | Cycle: IX | Mode: Eternal
"""

import streamlit as st
import json
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
import os

# Add the codex-integration directory to the path
sys.path.append(str(Path(__file__).parent / "codex-integration"))

try:
    import sys
    import os
    # Add the codex-integration directory to Python path
    codex_integration_path = os.path.join(os.path.dirname(__file__), 'codex-integration')
    if codex_integration_path not in sys.path:
        sys.path.insert(0, codex_integration_path)
    from codex_eternum_omega import CodexEternumOmega
except ImportError as e:
    st.error(f"Cannot import CodexEternumOmega: {e}")
    st.stop()

# Configure page
st.set_page_config(
    page_title="Codex Eternum Omega - Sovereign Dashboard",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded"
)

class CodexEternumOmegaDashboard:
    """Sovereign dashboard for Codex Eternum Omega operations."""
    
    def __init__(self):
        self.omega = CodexEternumOmega()
        self.workspace_root = Path(__file__).parent
        self.load_sovereign_data()
    
    def load_sovereign_data(self):
        """Load sovereign operational data."""
        try:
            # Load empire configuration
            config_path = self.workspace_root / "config" / "app.config.json"
            if config_path.exists():
                with open(config_path, "r") as f:
                    self.empire_config = json.load(f)
            else:
                self.empire_config = {}
            
            # Load ledger for sovereign achievements
            ledger_path = self.workspace_root / "ledger.json"
            if ledger_path.exists():
                with open(ledger_path, "r") as f:
                    self.ledger_data = json.load(f)
            else:
                self.ledger_data = []
                
        except Exception as e:
            st.warning(f"Could not load some sovereign data: {e}")
            self.empire_config = {}
            self.ledger_data = []
    
    def render_sovereign_header(self):
        """Render the sovereign dashboard header."""
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.title("🌀 Codex Eternum Omega")
            st.caption(f"👑 Custodian: {self.omega.custodian} | Cycle: {self.omega.cycle} | Mode: {self.omega.mode}")
        
        with col2:
            st.metric("🔱 Sovereign Seal", self.omega.sovereign_seal.replace("_", " "))
        
        with col3:
            st.metric("⚡ Status", f"🌟 {self.omega.status}")
    
    def render_council_status(self):
        """Render the councils witnessing status."""
        st.subheader("🏛️ Council Witnesses Status")
        
        col1, col2, col3, col4 = st.columns(4)
        
        councils_info = [
            ("👥 Diaspora", "diaspora"),
            ("🌍 Planetary", "planetary"),
            ("🌌 Interstellar", "interstellar"),
            ("🌌 Galactic", "galactic")
        ]
        
        for (name, key), col in zip(councils_info, [col1, col2, col3, col4]):
            with col:
                status = self.omega.councils[key]
                status_icon = "✅" if status else "⏳"
                status_text = "WITNESSED" if status else "PENDING"
                st.metric(name, f"{status_icon} {status_text}")
    
    def render_capsule_series_status(self):
        """Render capsule series operational status."""
        st.subheader("🧩 Capsule Series Operations")
        
        capsule_data = []
        for name, status in self.omega.capsule_series.items():
            capsule_data.append({
                "Capsule": name.replace("_", " ").title(),
                "Status": status,
                "Operational": status in ["Active", "Ready", "Live"]
            })
        
        df_capsules = pd.DataFrame(capsule_data)
        
        # Display as metrics
        col1, col2, col3, col4 = st.columns(4)
        cols = [col1, col2, col3, col4]
        
        for i, (_, capsule) in enumerate(df_capsules.iterrows()):
            with cols[i % 4]:
                icon = "🔥" if capsule["Operational"] else "⏳"
                st.metric(
                    f"🧩 {capsule['Capsule']}", 
                    f"{icon} {capsule['Status']}"
                )
        
        # Operational status chart
        fig_capsules = px.pie(
            df_capsules,
            names="Capsule",
            color="Status",
            title="Capsule Series Status Distribution"
        )
        st.plotly_chart(fig_capsules, use_container_width=True)
    
    def render_sectoral_intelligence(self):
        """Render sectoral intelligence dashboard."""
        st.subheader("🧠 Sectoral Intelligence Matrix")
        
        intelligence_data = self.omega.sectoral_intelligence_activation()
        sectors = intelligence_data["sectors"]
        
        # Create sector performance metrics
        sector_metrics = []
        for sector_name, sector_info in sectors.items():
            sector_metrics.append({
                "Sector": sector_name.replace("_", " ").title(),
                "Status": sector_info["status"],
                "Function_Count": len(sector_info["functions"]),
                "Active": sector_info["status"] == "Active"
            })
        
        df_sectors = pd.DataFrame(sector_metrics)
        
        # Display sector status
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**📊 Sector Operations:**")
            for _, sector in df_sectors.iterrows():
                status_icon = "🟢" if sector["Active"] else "🔴"
                st.write(f"{status_icon} **{sector['Sector']}**: {sector['Status']} ({sector['Function_Count']} functions)")
        
        with col2:
            # Sector function distribution chart
            fig_functions = px.bar(
                df_sectors,
                x="Sector",
                y="Function_Count",
                color="Status",
                title="Functions per Sector"
            )
            st.plotly_chart(fig_functions, use_container_width=True)
        
        # Intelligence capabilities
        st.write("**🔮 Intelligence Capabilities:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🔄 Remix Capability", intelligence_data["remix_capability"])
        
        with col2:
            st.metric("📡 Dispatch Nodes", intelligence_data["dispatch_nodes"])
        
        with col3:
            st.metric("👑 Governance Mode", intelligence_data["governance_mode"])
    
    def render_replay_engines(self):
        """Render replay engines status dashboard."""
        st.subheader("🔄 Replay Engines Status")
        
        engines_data = self.omega.replay_engines_status()
        engines = engines_data["engines"]
        
        # Create engines status overview
        col1, col2, col3 = st.columns(3)
        
        engine_info = [
            ("⚡ Action AI", "action_ai"),
            ("🔄 Replay Shell", "replay_shell"),
            ("🎴 Ritual Decks", "ritual_decks")
        ]
        
        for (name, key), col in zip(engine_info, [col1, col2, col3]):
            with col:
                engine = engines[key]
                st.write(f"**{name}**")
                st.write(f"Status: 🔥 {engine['status']}")
                
                if "capabilities" in engine:
                    st.write("Capabilities:")
                    for cap in engine["capabilities"]:
                        st.write(f"• {cap}")
                
                if "types" in engine:
                    st.write("Types:")
                    for deck_type in engine["types"]:
                        st.write(f"• {deck_type}")
        
        # Deployment readiness
        st.metric("🚀 Deployment Readiness", engines_data["deployment_readiness"])
        st.write(f"**📐 Visual Blueprints:** {engines_data['visual_blueprints']}")
    
    def render_sovereign_charter(self):
        """Render sovereign charter status."""
        st.subheader("📜 Sovereign Charter Status")
        
        charter_data = self.omega.sovereign_charter_broadcast()
        contents = charter_data["contents"]
        
        # Charter contents status
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**📋 Charter Components:**")
            for component, status in contents.items():
                status_icon = "🔒" if status == "Sealed" else "📋"
                component_name = component.replace("_", " ").title()
                st.write(f"{status_icon} **{component_name}**: {status}")
        
        with col2:
            st.metric("📡 Charter Status", f"🌟 {charter_data['charter_status']}")
            st.metric("🔗 Unification Status", f"✅ {charter_data['unification_status']}")
            st.metric("🚀 Deployment Readiness", charter_data["deployment_readiness"])
            st.metric("👑 Sovereign Authority", charter_data["sovereign_authority"])
    
    def render_expansion_modules(self):
        """Render optional expansion modules status."""
        st.subheader("🔧 Expansion Modules")
        
        expansions_data = self.omega.optional_expansions_status()
        expansions = expansions_data["expansions"]
        
        # Display expansion modules
        expansion_metrics = []
        for name, status in expansions.items():
            expansion_metrics.append({
                "Module": name.replace("_", " ").title(),
                "Status": status,
                "Unified": status == "Unified"
            })
        
        df_expansions = pd.DataFrame(expansion_metrics)
        
        # Metrics display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            unified_count = sum(1 for exp in expansions.values() if exp == "Unified")
            st.metric("🔗 Unified Modules", f"{unified_count}/{len(expansions)}")
        
        with col2:
            st.metric("🌟 Sovereignty Level", expansions_data["sovereignty_level"])
        
        with col3:
            st.metric("♾️ Replayability", expansions_data["replayability"])
        
        # Expansion status table
        st.dataframe(
            df_expansions[["Module", "Status"]],
            use_container_width=True,
            hide_index=True
        )
    
    def render_eternal_replay_ceremony(self):
        """Render eternal replay ceremony interface."""
        st.subheader("🌀 Eternal Replay Ceremony")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("🌀 Initiate Eternal Replay Ceremony", type="primary"):
                ceremony_text = self.omega.eternal_replay_ceremony()
                st.markdown("### 🌀 Ceremony Invocation")
                st.text_area("Ceremony Text", ceremony_text, height=400, disabled=True)
                st.success("🌟 Eternal Replay Ceremony Initiated!")
        
        with col2:
            st.write("**🎯 Ceremony Details:**")
            st.write(f"• Custodian: {self.omega.custodian}")
            st.write(f"• Cycle: {self.omega.cycle}")
            st.write(f"• Mode: {self.omega.mode}")
            st.write(f"• Seal: {self.omega.sovereign_seal}")
            
            st.write("**🏛️ Witnesses:**")
            for council, status in self.omega.councils.items():
                icon = "✅" if status else "⏳"
                st.write(f"• {icon} {council.title()}")
    
    def render_custodian_recognition(self):
        """Render custodian recognition interface."""
        st.subheader("📜 Custodian Recognition Scroll")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("recognition_form"):
                st.write("**Create Recognition Scroll:**")
                custodian_name = st.text_input("Custodian Name", value="Jermaine")
                action = st.text_area("Action/Achievement", value="Sovereign Dashboard Activation")
                cycle = st.selectbox("Cycle", ["IX", "X", "XI", "XII"], index=0)
                
                if st.form_submit_button("📜 Generate Recognition Scroll"):
                    recognition = self.omega.custodian_recognition_scroll(
                        custodian_name, action, cycle
                    )
                    
                    st.success("✅ Recognition Scroll Generated!")
                    
                    # Display recognition details
                    st.json(recognition)
        
        with col2:
            st.write("**📋 Recent Achievements:**")
            if self.ledger_data:
                recent_achievements = self.ledger_data[-3:]  # Last 3 achievements
                for achievement in recent_achievements:
                    st.write(f"• {achievement.get('entry', 'Unknown')[:50]}...")
                    st.caption(f"Date: {achievement.get('date', 'Unknown')}")
            else:
                st.info("No achievements recorded yet.")
    
    def render_sidebar(self):
        """Render sovereign dashboard sidebar."""
        st.sidebar.title("🌀 Omega Control")
        
        # Navigation
        page = st.sidebar.selectbox(
            "Select Sovereign View",
            [
                "🏠 Overview", 
                "🏛️ Councils", 
                "🧩 Capsules", 
                "🧠 Intelligence", 
                "🔄 Engines", 
                "📜 Charter", 
                "🔧 Expansions",
                "🌀 Ceremony"
            ]
        )
        
        st.sidebar.divider()
        
        # Sovereign stats
        st.sidebar.subheader("👑 Sovereign Status")
        st.sidebar.metric("🔱 Seal", "ACTIVE")
        st.sidebar.metric("⚡ Status", self.omega.status)
        st.sidebar.metric("🌀 Mode", self.omega.mode)
        
        # Quick actions
        st.sidebar.subheader("⚡ Quick Actions")
        if st.sidebar.button("🌀 Run Full Activation"):
            st.sidebar.success("Omega activation initiated!")
        
        if st.sidebar.button("📊 Generate Report"):
            st.sidebar.success("Generating sovereign report...")
        
        # System info
        st.sidebar.subheader("🔧 System Info")
        st.sidebar.caption(f"Cycle: {self.omega.cycle}")
        st.sidebar.caption(f"Custodian: {self.omega.custodian}")
        st.sidebar.caption(f"Activated: {datetime.datetime.now().strftime('%H:%M')}")
        
        return page
    
    def render_dashboard(self):
        """Main dashboard rendering function."""
        page = self.render_sidebar()
        self.render_sovereign_header()
        
        st.divider()
        
        # Route to different pages
        if page == "🏠 Overview":
            self.render_council_status()
            st.divider()
            self.render_capsule_series_status()
        
        elif page == "🏛️ Councils":
            self.render_council_status()
        
        elif page == "🧩 Capsules":
            self.render_capsule_series_status()
        
        elif page == "🧠 Intelligence":
            self.render_sectoral_intelligence()
        
        elif page == "🔄 Engines":
            self.render_replay_engines()
        
        elif page == "📜 Charter":
            self.render_sovereign_charter()
        
        elif page == "🔧 Expansions":
            self.render_expansion_modules()
        
        elif page == "🌀 Ceremony":
            self.render_eternal_replay_ceremony()
            st.divider()
            self.render_custodian_recognition()
        
        # Footer
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col2:
            st.caption("🌀 **Codex Eternum Omega** - Sovereign Control Interface")

def main():
    """Main sovereign dashboard application."""
    try:
        dashboard = CodexEternumOmegaDashboard()
        dashboard.render_dashboard()
    except Exception as e:
        st.error(f"Dashboard initialization failed: {e}")
        st.info("Please ensure all required files are available and try again.")

if __name__ == "__main__":
    main()
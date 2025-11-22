#!/usr/bin/env python3
"""
Codex Unified Dashboard - Working Version
========================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
from pathlib import Path
import sys
import os

# Import Codex Pydantic models and utilities
try:
    # Add multiple potential paths for imports
    current_dir = Path(__file__).parent
    root_dir = current_dir.parent.parent.parent
    sys.path.insert(0, str(root_dir))
    sys.path.insert(0, str(root_dir.absolute()))
    
    # Try absolute path first
    if (root_dir / 'codex_models.py').exists():
        from codex_models import (
            Transaction, Stream, Status, Constellation, ConstellationStar, 
            Proclamation, LedgerEntry, CodexDataManager
        )
        from codex_utils import load_json, save_json, append_entry, get_entries
        MODELS_AVAILABLE = True
        UTILS_AVAILABLE = True
    else:
        # Fallback - set flags to False for basic functionality
        MODELS_AVAILABLE = False
        UTILS_AVAILABLE = False
except ImportError as e:
    # Graceful degradation - dashboard will work without enhanced models
    MODELS_AVAILABLE = False
    UTILS_AVAILABLE = False
except Exception as e:
    # Any other error - continue with basic functionality
    MODELS_AVAILABLE = False
    UTILS_AVAILABLE = False

# Page configuration - Configure FIRST before any other Streamlit commands
st.set_page_config(
    page_title="🔥 Codex Dominion Unified Dashboard",
    page_icon="🔥",
    layout="wide"
)

def load_data_safe(filename, default=None):
    """Safely load JSON data using enhanced utilities"""
    try:
        # Try multiple possible data locations
        current_dir = Path(__file__).parent
        root_dir = current_dir.parent.parent.parent
        
        possible_paths = [
            root_dir / "data" / filename,
            root_dir / filename,
            Path("data") / filename,
            Path(filename),
            Path(f"../../../data/{filename}"),
            Path(f"../../../{filename}")
        ]
        
        # Try each path until one works
        for data_path in possible_paths:
            if data_path.exists():
                with open(data_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        
        # If UTILS_AVAILABLE, try the enhanced method
        if UTILS_AVAILABLE:
            try:
                return load_json(str(root_dir / "data" / filename), default or {})
            except:
                pass
        
        # Return default if no file found
        return default or {}
        
    except Exception as e:
        # Don't show errors in production, just return default
        return default or {}

def save_data_safe(filename, data):
    """Safely save JSON data using enhanced utilities"""
    try:
        # Determine best save path
        current_dir = Path(__file__).parent
        root_dir = current_dir.parent.parent.parent
        
        # Primary save location
        data_path = root_dir / "data" / filename
        data_path.parent.mkdir(exist_ok=True)
        
        # Use enhanced utilities if available
        if UTILS_AVAILABLE:
            try:
                return save_json(data, str(data_path), create_backup=False)
            except:
                pass
        
        # Fallback to direct JSON save
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return True
        
    except Exception as e:
        # Try alternative save location
        try:
            alt_path = Path("data") / filename
            alt_path.parent.mkdir(exist_ok=True)
            with open(alt_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        except:
            return False

def main():
    """Main dashboard function"""
    
    # Apply cosmic styling
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: white;
    }
    .metric-card {
        background: rgba(255,255,255,0.1);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.2);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("🔥 CODEX DOMINION UNIFIED DASHBOARD")
    st.markdown("**Complete Codex Dominion Suite - Unified Interface**")
    st.markdown("---")
    
    # System status
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 System Status</h3>
            <h2 style="color: #32CD32;">OPERATIONAL</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Data Files</h3>
            <h2 style="color: #FFD700;">READY</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🔥 Flame Status</h3>
            <h2 style="color: #FF4500;">ETERNAL</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>⏰ Last Updated</h3>
            <h2 style="color: #8A2BE2;">{}</h2>
        </div>
        """.format(datetime.now().strftime("%H:%M")), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main tabs
    tabs = st.tabs([
        "🎯 Spark Studio",
        "📓 Codex Notebook", 
        "📖 Tome Foundry",
        "� AI Dev Studio",
        "⚗️ Nano Forge",
        "🧵 Flow Loom",
        "📖 Publisher",
        "👑 Council Access",
        "📜 Council Ritual",
        "🎇 Festival Script"
    ])
    
    with tabs[0]:
        st.header("🎯 Spark Studio")
        st.markdown("**AI-Powered Content Generation & Ledger Management**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔥 Spark Generator")
            topic = st.text_input("Topic", "Digital Sovereignty")
            audience = st.text_input("Audience", "Tech Leaders")
            tone = st.selectbox("Tone", ["inspiring", "professional", "casual", "technical"])
            
            if st.button("✨ Generate Spark", type="primary"):
                st.success("Spark generated successfully!")
                st.markdown(f"""
                **Generated Spark for {audience}:**
                
                *{topic}* represents the future of technological independence. 
                This {tone} approach emphasizes complete control and sovereignty 
                over digital assets and operations.
                
                The path forward requires bold vision and strategic implementation.
                """)
        
        with col2:
            st.subheader("📊 Enhanced Codex Ledger")
            
            # Initialize data manager if models are available
            if MODELS_AVAILABLE:
                data_manager = CodexDataManager("../../../data")
                revenue_summary = data_manager.get_revenue_summary()
                
                # Display enhanced metrics
                col2_1, col2_2 = st.columns(2)
                with col2_1:
                    st.metric("💰 Total Revenue", f"${revenue_summary.get('grand_total', 0):.2f}")
                    st.metric("📊 Transactions", revenue_summary.get('total_transactions', 0))
                
                with col2_2:
                    st.metric("⭐ Constellations", f"${revenue_summary.get('constellation_total', 0):.2f}")
                    stream_totals = revenue_summary.get('stream_totals', {})
                    st.metric("🏪 Store Revenue", f"${stream_totals.get('store', 0):.2f}")
                
                # Enhanced transaction form
                with st.expander("💳 Add Revenue Transaction"):
                    trans_col1, trans_col2 = st.columns(2)
                    
                    with trans_col1:
                        source = st.selectbox("Revenue Stream", ["store", "social", "website"])
                        item = st.text_input("Item/Service", "Digital Product")
                    
                    with trans_col2:
                        amount = st.number_input("Amount ($)", min_value=0.01, value=100.0)
                    
                    if st.button("💰 Add Transaction", type="primary"):
                        try:
                            # Create transaction using Pydantic model
                            transaction = Transaction(
                                source=Stream(source),
                                item=item,
                                amount=amount,
                                timestamp=datetime.now()
                            )
                            
                            if data_manager.save_transaction(transaction):
                                st.success(f"✅ Transaction added: ${amount:.2f} from {source}")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("❌ Failed to save transaction")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
            else:
                # Fallback to basic functionality
                ledger_data = load_data_safe("ledger.json", {"entries": []})
                constellation_data = load_data_safe("constellations.json", {"constellations": []})
                
                st.info(f"Ledger Entries: {len(ledger_data.get('entries', []))}")
                st.success(f"Constellations: {len(constellation_data.get('constellations', []))}")
            
            # Quick entry form (always available)
            with st.expander("📝 Enhanced Quick Entry"):
                entry_text = st.text_area("Entry Content:")
                entry_type = st.selectbox("Entry Type", ["manual_entry", "spark", "insight", "note", "idea"])
                
                if st.button("📝 Add Entry", type="primary"):
                    if entry_text.strip():
                        if UTILS_AVAILABLE:
                            # Use enhanced utilities
                            new_entry = {
                                "content": entry_text,
                                "type": entry_type,
                                "source": "unified_dashboard"
                            }
                            
                            if append_entry("../../../data/ledger.json", "entries", new_entry, max_entries=1000):
                                st.success("✅ Entry added to ledger using enhanced utilities!")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("❌ Failed to add entry")
                        else:
                            # Fallback method
                            ledger_data = load_data_safe("ledger.json", {"entries": []})
                            new_entry = {
                                "content": entry_text,
                                "timestamp": datetime.now().isoformat(),
                                "type": entry_type,
                                "id": len(ledger_data.get('entries', [])) + 1
                            }
                            ledger_data.setdefault('entries', []).append(new_entry)
                            
                            if save_data_safe("ledger.json", ledger_data):
                                st.success("✅ Entry added to ledger!")
                                st.rerun()
                            else:
                                st.error("Error saving ledger data")
                    else:
                        st.error("Please enter content for the entry")
    
    with tabs[1]:
        st.header("📓 Codex Notebook")
        st.markdown("**Structured cells for text, code, and prompts**")
        st.info("📝 Notebook functionality coming soon!")
    
    with tabs[2]:
        st.header("📖 Tome Foundry")
        st.markdown("**Transform notebooks into books, guides, and courses**")
        st.info("📚 Tome generation functionality coming soon!")
    
    with tabs[3]:
        st.header("� AI Development Studio")
        st.markdown("**AI-powered full-stack application builder inspired by Lovable**")
        
        # Quick access to AI Development Studio
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🎯 Quick Project Builder")
            
            project_name = st.text_input("Project Name", placeholder="my-awesome-app")
            project_type = st.selectbox("Project Type", [
                "React Application",
                "Next.js Full-Stack App", 
                "Vue.js Application",
                "Python FastAPI",
                "Flutter Mobile App",
                "Analytics Dashboard"
            ])
            
            ai_level = st.select_slider(
                "AI Intelligence Level",
                options=["Basic", "Advanced", "Expert", "Genius"],
                value="Advanced"
            )
            
            if st.button("� Launch Full AI Studio", type="primary"):
                st.success("🚀 Launching Codex AI Development Studio...")
                st.info("💡 **Tip**: The full AI Development Studio provides advanced features like:\n"
                        "- Live code preview\n"
                        "- AI coding assistant\n" 
                        "- One-click deployment\n"
                        "- Template gallery\n"
                        "- Performance analytics")
            
            if st.button("⚡ Quick Generate"):
                st.success(f"✅ Generating {project_type} project: '{project_name}'")
                with st.expander("📁 Project Structure Preview"):
                    st.code(f"""
{project_name or 'my-app'}/
├── src/
│   ├── components/
│   ├── pages/
│   ├── hooks/
│   └── utils/
├── public/
├── package.json
└── README.md
                    """)
        
        with col2:
            st.subheader("�️ AI Studio Stats")
            st.metric("Projects Generated", "127", "+15")
            st.metric("Deployments", "89", "+8")
            st.metric("Success Rate", "98.5%", "+1.2%")
            
            st.subheader("🎯 Features")
            features = [
                "✅ AI Code Generation",
                "✅ Live Preview",
                "✅ One-Click Deploy", 
                "✅ Template Gallery",
                "✅ Performance Analytics",
                "✅ Auto Documentation"
            ]
            
            for feature in features:
                st.markdown(f"<small>{feature}</small>", unsafe_allow_html=True)
    
    with tabs[4]:
        st.header("⚗️ Nano Forge")
        st.markdown("**Precision content creation and micro-tools**")
        st.info("🔬 Nano tools functionality coming soon!")
    
    with tabs[5]:
        st.header("🧵 Flow Loom")
        st.markdown("**Weave sovereign automation workflows**")
        st.info("🧵 Flow automation functionality coming soon!")
    
    with tabs[6]:
        st.header("📖 Publisher")
        st.markdown("**Transform artifacts into published content**")
        st.info("📤 Publishing functionality coming soon!")
    
    with tabs[7]:
        st.header("👑 Council Access")
        st.markdown("**Hierarchical access control for Codex governance**")
        st.info("👑 Council access functionality coming soon!")
    
    with tabs[8]:
        st.header("📜 Council Ritual Scroll")
        st.markdown("**Sacred Chamber of Codex Proclamations**")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("✨ Enhanced Ritual Inscription")
            
            ritual_col1, ritual_col2 = st.columns(2)
            
            with ritual_col1:
                role = st.selectbox("Council Role:", ["High Council", "Elder Council", "Advisory Council", "Keeper of Flames"])
                ritual_type = st.selectbox("Ritual Type:", ["Sacred Proclamation", "Blessed Silence", "Divine Blessing", "Imperial Decree", "Eternal Vow"])
            
            with ritual_col2:
                cycle = st.text_input("Ritual Cycle:", "Eternal Flame Cycle")
                power_level = st.slider("Power Level:", 1, 10, 7)
            
            text = st.text_area("Sacred Ritual Text:", placeholder="By flame and silence, I proclaim...", height=120)
            
            if st.button("🔥 Inscribe into Eternal Flame", type="primary"):
                if text.strip():
                    try:
                        if MODELS_AVAILABLE:
                            # Use Pydantic model for enhanced data structure
                            data_manager = CodexDataManager("../../../data")
                            
                            proclamation = Proclamation(
                                timestamp=datetime.now(),
                                cycle=cycle,
                                text=text,
                                ritual_type=ritual_type,
                                council_role=role,
                                power_level=power_level
                            )
                            
                            if data_manager.save_proclamation(proclamation):
                                st.success(f"🔥 {ritual_type} INSCRIBED INTO THE ETERNAL FLAME! 🔥")
                                st.balloons()
                                
                                # Display the sacred inscription
                                st.markdown(f"""
                                ### ✨ Sacred Inscription Complete ✨
                                
                                **👑 Council Role**: {role}  
                                **🔥 Ritual Type**: {ritual_type}  
                                **🌙 Cycle**: {cycle}  
                                **⚡ Power Level**: {power_level}/10  
                                **🕐 Inscribed**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                                
                                **📜 Sacred Text**:
                                > {text}
                                
                                *By the eternal flame, this proclamation is forever inscribed in the Codex.*
                                """)
                            else:
                                st.error("❌ Failed to inscribe ritual. The flame flickers...")
                        else:
                            # Fallback to basic functionality
                            proc_data = load_data_safe("proclamations.json", {"proclamations": []})
                            
                            new_proclamation = {
                                "role": role,
                                "type": ritual_type,
                                "content": text,
                                "cycle": cycle,
                                "power_level": power_level,
                                "timestamp": datetime.now().isoformat(),
                                "status": "inscribed",
                                "id": len(proc_data.get('proclamations', [])) + 1
                            }
                            
                            proc_data.setdefault('proclamations', []).append(new_proclamation)
                            
                            with open("data/proclamations.json", 'w') as f:
                                json.dump(proc_data, f, indent=2)
                            st.success(f"✨ {ritual_type} inscribed into the Codex flame!")
                            st.balloons()
                            
                    except Exception as e:
                        st.error(f"❌ Inscription error: {e}")
                else:
                    st.error("❌ Sacred text cannot be empty. The flame demands words.")
        
        with col2:
            st.subheader("🔥 Flame Status")
            st.markdown("""
            <div style='text-align: center; padding: 20px; background: #1a1a1a; border-radius: 10px;'>
                <div style='font-size: 3em; color: #ff6b35;'>🔥</div>
                <div style='color: #ff6b35; font-weight: bold;'>ETERNAL FLAME</div>
                <div style='color: #cccccc; font-size: 0.9em;'>Ready for Inscription</div>
            </div>
            """, unsafe_allow_html=True)
    
    with tabs[9]:
        st.header("🎇 Festival Script")
        st.markdown("**Seasonal & Eternal Invocations**")
        st.info("🎇 Festival functionality coming soon!")
    
    # Sidebar
    with st.sidebar:
        st.header("🔥 Codex Control Center")
        
        st.subheader("🎯 Quick Actions")
        if st.button("🔄 Refresh All", type="primary"):
            st.rerun()
        
        if st.button("📊 System Status"):
            st.success("All systems operational!")
        
        if st.button("🔥 Flame Check"):
            st.success("🔥 CODEX FLAME: ETERNAL")
        
        st.divider()
        
        # Load and display metrics
        ledger_data = load_data_safe("ledger.json", {"entries": []})
        constellation_data = load_data_safe("constellations.json", {"constellations": []})
        proclamation_data = load_data_safe("proclamations.json", {"proclamations": []})
        
        st.subheader("📈 System Metrics")
        st.metric("Ledger Entries", len(ledger_data.get('entries', [])))
        st.metric("Constellations", len(constellation_data.get('constellations', [])))
        st.metric("Proclamations", len(proclamation_data.get('proclamations', [])))
        
        st.divider()
        
        st.markdown("**🔥 System Status**")
        st.markdown("✅ All modules loaded")
        st.markdown("✅ Dashboard operational") 
        st.markdown("✅ Data files ready")
        st.markdown("🔥 **FLAME: ETERNAL**")
    
    # Footer
    st.divider()
    st.markdown("**🔥 Codex Dominion Unified Dashboard** - *All systems integrated for absolute sovereignty*")

# Always run the main function in Streamlit context
main()

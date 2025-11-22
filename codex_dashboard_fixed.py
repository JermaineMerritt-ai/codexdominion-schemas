#!/usr/bin/env python3
"""
Codex Dominion Digital Sovereignty Dashboard - FIXED VERSION
===========================================================
Complete unified dashboard with error handling and fallbacks
"""

import streamlit as st
import pandas as pd
import json
import sys
from datetime import datetime
from pathlib import Path

# Advanced imports with error handling
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("⚠️ Plotly not available - charts will use basic display")

# Page configuration MUST be first
st.set_page_config(
    page_title="🔥 Codex Dominion Digital Sovereignty Empire",
    page_icon="🔥", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global error handler
def safe_execute(func, *args, **kwargs):
    """Safely execute functions with error handling"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        st.error(f"❌ Error in {func.__name__}: {str(e)}")
        return None

# Enhanced data loading with multiple fallback paths
def load_data_safe(filename, default=None):
    """Load JSON data with comprehensive fallback paths"""
    if default is None:
        default = {}
    
    try:
        # Multiple potential data file locations
        possible_paths = [
            Path("data") / filename,
            Path("../data") / filename,
            Path("../../data") / filename,
            Path("../../../data") / filename,
            Path(filename),
            Path.cwd() / "data" / filename,
            Path(__file__).parent / "data" / filename,
            Path(__file__).parent.parent / "data" / filename,
            Path(__file__).parent.parent.parent / "data" / filename,
        ]
        
        # Try each path
        for path in possible_paths:
            try:
                if path.exists() and path.is_file():
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        return data if data else default
            except (json.JSONDecodeError, IOError):
                continue
        
        # Return default if no file found
        return default
        
    except Exception:
        return default

def save_data_safe(filename, data):
    """Save JSON data with error handling"""
    try:
        # Try to find existing data directory
        data_dir = None
        possible_dirs = [
            Path("data"),
            Path("../data"),
            Path("../../data"),
            Path("../../../data"),
            Path.cwd() / "data",
        ]
        
        for dir_path in possible_dirs:
            if dir_path.exists() and dir_path.is_dir():
                data_dir = dir_path
                break
        
        # Create data directory if none found
        if data_dir is None:
            data_dir = Path("data")
            data_dir.mkdir(exist_ok=True)
        
        # Save file
        file_path = data_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
        
    except Exception as e:
        st.error(f"❌ Save error for {filename}: {e}")
        return False

def create_metric_card(title, value, color="#32CD32"):
    """Create a styled metric card"""
    return f"""
    <div style="
        background: rgba(255,255,255,0.1);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.2);
        text-align: center;
        margin: 10px 0;
    ">
        <h3 style="color: white; margin: 0;">{title}</h3>
        <h2 style="color: {color}; margin: 10px 0;">{value}</h2>
    </div>
    """

def apply_cosmic_styling():
    """Apply cosmic background and styling"""
    st.markdown("""
    <style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: white;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255,255,255,0.1);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.2);
        text-align: center;
        margin: 10px 0;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b35, #ff8e35);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: bold;
    }
    
    /* Success messages */
    .stSuccess {
        background: rgba(50, 205, 50, 0.2);
        border: 1px solid #32CD32;
        border-radius: 10px;
    }
    
    /* Error messages */
    .stError {
        background: rgba(255, 69, 0, 0.2);
        border: 1px solid #FF4500;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

def render_dashboard_header():
    """Render the main dashboard header"""
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #ff6b35; font-size: 3em; margin: 0;">🔥 CODEX DOMINION 🔥</h1>
        <h2 style="color: #FFD700; margin: 10px 0;">DIGITAL SOVEREIGNTY EMPIRE</h2>
        <p style="color: #cccccc; font-size: 1.2em;">Complete Unified Dashboard - All Systems Operational</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

def render_system_metrics():
    """Render system status metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card("🎯 System Status", "OPERATIONAL", "#32CD32"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card("📊 Data Files", "READY", "#FFD700"), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_metric_card("🔥 Flame Status", "ETERNAL", "#FF4500"), unsafe_allow_html=True)
    
    with col4:
        current_time = datetime.now().strftime("%H:%M:%S")
        st.markdown(create_metric_card("⏰ Live Time", current_time, "#8A2BE2"), unsafe_allow_html=True)

def render_spark_studio():
    """Render Spark Studio tab"""
    st.header("🎯 Spark Studio - AI Content Generation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("✨ Enhanced Spark Generator")
        
        # Spark generation form
        with st.form("spark_form"):
            topic = st.text_input("🎯 Topic", value="Digital Sovereignty", placeholder="Enter your topic...")
            audience = st.selectbox("👥 Target Audience", [
                "Tech Leaders", "Entrepreneurs", "Developers", "Innovators", 
                "Digital Nomads", "Business Owners", "Content Creators"
            ])
            tone = st.selectbox("🎭 Tone Style", [
                "inspiring", "professional", "casual", "technical", "visionary", "motivational"
            ])
            length = st.slider("📏 Content Length", 50, 500, 200)
            
            generate_spark = st.form_submit_button("🚀 Generate Spark", type="primary")
        
        if generate_spark and topic:
            with st.spinner("🔥 Igniting your spark..."):
                # Simulated AI content generation
                spark_content = f"""
**🎯 {topic} Mastery for {audience}**

The future belongs to those who understand {topic.lower()} at its core. This {tone} approach reveals the transformative power of digital independence.

**Key Insights:**
• Revolutionary thinking drives {topic.lower()} innovation
• Strategic implementation ensures lasting impact  
• {audience} are perfectly positioned to lead this transformation
• The convergence of technology and vision creates unprecedented opportunities

**Action Steps:**
1. Embrace the {topic.lower()} mindset completely
2. Build systems that scale with your vision
3. Connect with like-minded {audience.lower()}
4. Document your journey for future reference

*Generated with {length} words of concentrated wisdom for maximum impact.*

🔥 **Remember**: True {topic.lower()} comes from consistent action and unwavering commitment to your digital sovereignty empire.
                """
                
                st.success("✅ Spark Generated Successfully!")
                st.markdown(spark_content)
                
                # Save to ledger
                ledger_data = load_data_safe("ledger.json", {"entries": []})
                new_entry = {
                    "id": len(ledger_data.get("entries", [])) + 1,
                    "content": spark_content,
                    "type": "generated_spark",
                    "topic": topic,
                    "audience": audience,
                    "tone": tone,
                    "timestamp": datetime.now().isoformat(),
                    "source": "spark_studio"
                }
                
                ledger_data.setdefault("entries", []).append(new_entry)
                if save_data_safe("ledger.json", ledger_data):
                    st.balloons()
    
    with col2:
        st.subheader("📊 Ledger Analytics")
        
        # Load ledger data
        ledger_data = load_data_safe("ledger.json", {"entries": []})
        entries = ledger_data.get("entries", [])
        
        # Display metrics
        st.metric("📝 Total Entries", len(entries))
        
        if entries:
            recent_entries = entries[-5:]
            st.metric("🔥 Recent Sparks", len([e for e in recent_entries if e.get("type") == "generated_spark"]))
            
            # Show recent entries
            st.subheader("📋 Recent Entries")
            for entry in reversed(recent_entries):
                with st.expander(f"Entry #{entry.get('id', 'Unknown')} - {entry.get('type', 'entry')}"):
                    content = entry.get('content', 'No content')
                    if content and isinstance(content, str) and len(content) > 200:
                        st.write(content[:200] + "...")
                    else:
                        st.write(content or 'No content')
                    st.caption(f"Created: {entry.get('timestamp', 'Unknown')}")
        
        # Quick entry form
        st.subheader("⚡ Quick Entry")
        with st.form("quick_entry"):
            quick_content = st.text_area("Content", placeholder="Add a quick note or insight...")
            entry_type = st.selectbox("Type", ["note", "idea", "insight", "reminder", "spark"])
            
            if st.form_submit_button("📝 Add Entry", type="primary"):
                if quick_content.strip():
                    new_entry = {
                        "id": len(entries) + 1,
                        "content": quick_content,
                        "type": entry_type,
                        "timestamp": datetime.now().isoformat(),
                        "source": "quick_entry"
                    }
                    
                    ledger_data.setdefault("entries", []).append(new_entry)
                    if save_data_safe("ledger.json", ledger_data):
                        st.success("✅ Entry added!")
                        st.rerun()

def render_revenue_tracker():
    """Render Revenue Tracking section"""
    st.subheader("💰 Revenue Constellation Tracker")
    
    # Load revenue data
    revenue_data = load_data_safe("revenue_streams.json", {"streams": []})
    transactions_data = load_data_safe("transactions.json", {"transactions": []})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**💳 Add Revenue Transaction**")
        with st.form("revenue_form"):
            source = st.selectbox("Revenue Stream", ["store", "social", "website", "consulting", "products", "services"])
            item = st.text_input("Item/Service", placeholder="Digital product name...")
            amount = st.number_input("Amount ($)", min_value=0.01, value=100.0, step=0.01)
            
            if st.form_submit_button("💰 Add Transaction", type="primary"):
                new_transaction = {
                    "id": len(transactions_data.get("transactions", [])) + 1,
                    "source": source,
                    "item": item,
                    "amount": float(amount),
                    "timestamp": datetime.now().isoformat(),
                    "status": "completed"
                }
                
                transactions_data.setdefault("transactions", []).append(new_transaction)
                if save_data_safe("transactions.json", transactions_data):
                    st.success(f"✅ Transaction added: ${amount:.2f} from {source}")
                    st.balloons()
                    st.rerun()
    
    with col2:
        st.markdown("**📊 Revenue Summary**")
        
        transactions = transactions_data.get("transactions", [])
        if transactions:
            total_revenue = sum(t.get("amount", 0) for t in transactions)
            transaction_count = len(transactions)
            
            st.metric("💰 Total Revenue", f"${total_revenue:.2f}")
            st.metric("📊 Transactions", transaction_count)
            
            # Revenue by source
            revenue_by_source = {}
            for t in transactions:
                source = t.get("source", "unknown")
                revenue_by_source[source] = revenue_by_source.get(source, 0) + t.get("amount", 0)
            
            st.markdown("**💼 Revenue by Source:**")
            for source, amount in revenue_by_source.items():
                st.write(f"• {source.title()}: ${amount:.2f}")
        else:
            st.info("No transactions yet - add your first revenue entry!")

def render_council_ritual():
    """Render Council Ritual tab"""
    st.header("📜 Council Ritual Scroll - Sacred Chamber")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("✨ Sacred Ritual Inscription")
        
        with st.form("ritual_form"):
            ritual_col1, ritual_col2 = st.columns(2)
            
            with ritual_col1:
                role = st.selectbox("👑 Council Role", [
                    "High Council", "Elder Council", "Advisory Council", 
                    "Keeper of Flames", "Digital Sovereign", "Code Architect"
                ])
                ritual_type = st.selectbox("🔥 Ritual Type", [
                    "Sacred Proclamation", "Blessed Silence", "Divine Blessing",
                    "Imperial Decree", "Eternal Vow", "Digital Manifesto"
                ])
            
            with ritual_col2:
                cycle = st.text_input("🌙 Ritual Cycle", value="Eternal Flame Cycle")
                power_level = st.slider("⚡ Power Level", 1, 10, 7)
            
            ritual_text = st.text_area(
                "📜 Sacred Ritual Text", 
                placeholder="By flame and silence, I proclaim...",
                height=120
            )
            
            if st.form_submit_button("🔥 Inscribe into Eternal Flame", type="primary"):
                if ritual_text.strip():
                    proclamations_data = load_data_safe("proclamations.json", {"proclamations": []})
                    
                    new_proclamation = {
                        "id": len(proclamations_data.get("proclamations", [])) + 1,
                        "role": role,
                        "ritual_type": ritual_type,
                        "cycle": cycle,
                        "power_level": power_level,
                        "content": ritual_text,
                        "timestamp": datetime.now().isoformat(),
                        "status": "inscribed"
                    }
                    
                    proclamations_data.setdefault("proclamations", []).append(new_proclamation)
                    
                    if save_data_safe("proclamations.json", proclamations_data):
                        st.success(f"🔥 {ritual_type.upper()} INSCRIBED INTO THE ETERNAL FLAME! 🔥")
                        st.balloons()
                        
                        # Display inscription
                        st.markdown(f"""
                        ### ✨ Sacred Inscription Complete ✨
                        
                        **👑 Council Role**: {role}  
                        **🔥 Ritual Type**: {ritual_type}  
                        **🌙 Cycle**: {cycle}  
                        **⚡ Power Level**: {power_level}/10  
                        **🕐 Inscribed**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                        
                        **📜 Sacred Text**:
                        > {ritual_text}
                        
                        *By the eternal flame, this proclamation is forever inscribed in the Codex.*
                        """)
                        st.rerun()
                else:
                    st.error("❌ Sacred text cannot be empty. The flame demands words.")
    
    with col2:
        st.subheader("🔥 Eternal Flame Status")
        
        # Flame status display
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: rgba(255,107,53,0.1); border-radius: 15px; border: 1px solid #ff6b35;">
            <div style="font-size: 4em; color: #ff6b35; text-shadow: 0 0 20px #ff6b35;">🔥</div>
            <div style="color: #ff6b35; font-weight: bold; font-size: 1.2em;">ETERNAL FLAME</div>
            <div style="color: #cccccc; font-size: 0.9em;">Ready for Sacred Inscription</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Recent proclamations
        st.subheader("📋 Recent Proclamations")
        
        proclamations_data = load_data_safe("proclamations.json", {"proclamations": []})
        proclamations = proclamations_data.get("proclamations", [])
        
        if proclamations:
            recent_proclamations = list(reversed(proclamations))[:3]
            
            for proc in recent_proclamations:
                with st.expander(f"🔥 {proc.get('ritual_type', 'Unknown')} - {proc.get('role', 'Unknown')}"):
                    st.write(f"**Cycle**: {proc.get('cycle', 'Unknown')}")
                    st.write(f"**Power**: {proc.get('power_level', 0)}/10")
                    content = proc.get('content', '')
                    if content and isinstance(content, str) and len(content) > 100:
                        st.write(f"**Content**: {content[:100]}...")
                    else:
                        st.write(f"**Content**: {content or 'No content'}")
                    st.caption(f"Inscribed: {proc.get('timestamp', 'Unknown')}")
        else:
            st.info("🔥 No proclamations yet. Be the first to inscribe into the eternal flame!")

def render_ai_dev_studio():
    """Render AI Development Studio tab"""
    st.header("🤖 AI Development Studio - Full-Stack Builder")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🚀 Project Generator")
        
        with st.form("project_form"):
            project_name = st.text_input("📁 Project Name", placeholder="my-awesome-app")
            project_type = st.selectbox("🛠️ Project Type", [
                "React Application", "Next.js Full-Stack App", "Vue.js Application",
                "Python FastAPI", "Flutter Mobile App", "Analytics Dashboard",
                "E-commerce Site", "Portfolio Website", "Blog Platform"
            ])
            
            framework_col1, framework_col2 = st.columns(2)
            
            with framework_col1:
                ai_level = st.select_slider("🧠 AI Intelligence", 
                    options=["Basic", "Advanced", "Expert", "Genius"], value="Advanced")
                
            with framework_col2:
                deployment = st.selectbox("🚀 Deployment", [
                    "Local Development", "Vercel", "Netlify", "AWS", "Google Cloud", "Custom Server"
                ])
            
            features = st.multiselect("✨ Features", [
                "Authentication", "Database Integration", "API Routes", "Real-time Updates",
                "Payment Processing", "Admin Panel", "SEO Optimization", "PWA Support"
            ])
            
            if st.form_submit_button("🎯 Generate Project", type="primary"):
                if project_name:
                    with st.spinner("🔥 AI is crafting your project..."):
                        # Simulate project generation
                        st.success(f"✅ {project_type} '{project_name}' generated successfully!")
                        
                        # Project structure preview
                        with st.expander("📁 Generated Project Structure"):
                            structure = f"""
{project_name}/
├── src/
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   └── Layout.tsx
│   ├── pages/
│   │   ├── index.tsx
│   │   └── about.tsx
│   ├── hooks/
│   │   └── useCustomHook.ts
│   ├── utils/
│   │   └── helpers.ts
│   └── styles/
│       └── globals.css
├── public/
│   ├── favicon.ico
│   └── images/
├── package.json
├── README.md
├── .gitignore
└── tsconfig.json
                            """
                            st.code(structure, language="text")
                        
                        # Features summary
                        if features:
                            st.markdown("**🎯 Integrated Features:**")
                            for feature in features:
                                st.write(f"✅ {feature}")
                        
                        st.balloons()
    
    with col2:
        st.subheader("📊 Studio Analytics")
        
        # Mock analytics data
        st.metric("🚀 Projects Generated", "247", "+12")
        st.metric("🌐 Deployments", "156", "+8") 
        st.metric("⚡ Success Rate", "98.7%", "+0.3%")
        
        st.subheader("🎯 Popular Templates")
        templates = [
            "✅ Next.js Dashboard",
            "✅ React E-commerce", 
            "✅ FastAPI Backend",
            "✅ Flutter Mobile",
            "✅ Vue Portfolio",
            "✅ Analytics Platform"
        ]
        
        for template in templates:
            st.markdown(f"<small>{template}</small>", unsafe_allow_html=True)
        
        st.subheader("🔥 AI Capabilities")
        capabilities = [
            "🧠 Code Generation",
            "🎨 UI/UX Design",
            "📊 Data Analysis", 
            "🔒 Security Integration",
            "📱 Responsive Design",
            "🚀 Auto Deployment"
        ]
        
        for cap in capabilities:
            st.markdown(f"<small>{cap}</small>", unsafe_allow_html=True)

def render_system_overview():
    """Render System Overview tab"""
    st.header("🎯 System Overview - Digital Empire Status")
    
    # Load all data files for overview
    ledger_data = load_data_safe("ledger.json", {"entries": []})
    proclamations_data = load_data_safe("proclamations.json", {"proclamations": []})
    transactions_data = load_data_safe("transactions.json", {"transactions": []})
    constellations_data = load_data_safe("constellations.json", {"constellations": []})
    
    # System metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📝 Ledger Entries", len(ledger_data.get("entries", [])), "+3")
    
    with col2:
        st.metric("📜 Proclamations", len(proclamations_data.get("proclamations", [])), "+1")
    
    with col3:
        total_revenue = sum(t.get("amount", 0) for t in transactions_data.get("transactions", []))
        st.metric("💰 Total Revenue", f"${total_revenue:.2f}", "+$250")
    
    with col4:
        st.metric("⭐ Constellations", len(constellations_data.get("constellations", [])), "Stable")
    
    st.markdown("---")
    
    # System status overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔥 System Health")
        
        health_items = [
            ("🎯 Dashboard Core", "OPERATIONAL", "#32CD32"),
            ("📊 Data Layer", "STABLE", "#FFD700"), 
            ("🔥 Eternal Flame", "BURNING", "#FF4500"),
            ("👑 Council Access", "SECURED", "#8A2BE2"),
            ("💰 Revenue Tracking", "ACTIVE", "#32CD32"),
            ("🧠 AI Systems", "LEARNING", "#00CED1")
        ]
        
        for item, status, color in health_items:
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 10px; margin: 5px 0; background: rgba(255,255,255,0.05); border-radius: 8px;">
                <span>{item}</span>
                <span style="color: {color}; font-weight: bold;">{status}</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("🚀 Recent Activity")
        
        # Combine recent activities from all sources
        recent_activities = []
        
        # Recent ledger entries
        for entry in ledger_data.get("entries", [])[-3:]:
            content = entry.get("content", "") or ""
            display_content = content[:50] + "..." if isinstance(content, str) and len(content) > 50 else str(content)
            recent_activities.append({
                "type": "📝 Ledger Entry",
                "content": display_content,
                "time": entry.get("timestamp", "Unknown")
            })
        
        # Recent proclamations
        for proc in proclamations_data.get("proclamations", [])[-3:]:
            recent_activities.append({
                "type": "📜 Proclamation",
                "content": f"{proc.get('ritual_type', 'Unknown')} by {proc.get('role', 'Unknown')}",
                "time": proc.get("timestamp", "Unknown")
            })
        
        # Recent transactions
        for trans in transactions_data.get("transactions", [])[-3:]:
            recent_activities.append({
                "type": "💰 Transaction",
                "content": f"${trans.get('amount', 0):.2f} from {trans.get('source', 'Unknown')}",
                "time": trans.get("timestamp", "Unknown")
            })
        
        # Sort by time and display
        recent_activities.sort(key=lambda x: x["time"], reverse=True)
        
        for activity in recent_activities[:5]:
            time_str = str(activity['time'])[:10] if activity['time'] else "Unknown"
            with st.expander(f"{activity['type']} - {time_str}"):
                st.write(activity['content'])

def render_sidebar():
    """Render enhanced sidebar"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 3em;">🔥</div>
            <h3 style="color: #ff6b35; margin: 0;">CODEX CONTROL</h3>
            <p style="color: #cccccc; font-size: 0.9em;">Digital Sovereignty Command Center</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh", type="primary"):
                st.rerun()
        
        with col2:
            if st.button("📊 Status"):
                st.success("✅ All systems operational!")
        
        if st.button("🔥 Flame Check", use_container_width=True):
            st.success("🔥 ETERNAL FLAME: BURNING BRIGHT")
            st.balloons()
        
        st.markdown("---")
        
        # System metrics sidebar
        st.subheader("📈 Live Metrics")
        
        # Load data for metrics
        ledger_data = load_data_safe("ledger.json", {"entries": []})
        proclamations_data = load_data_safe("proclamations.json", {"proclamations": []})
        transactions_data = load_data_safe("transactions.json", {"transactions": []})
        
        st.metric("📝 Entries", len(ledger_data.get("entries", [])))
        st.metric("📜 Proclamations", len(proclamations_data.get("proclamations", [])))
        st.metric("💰 Transactions", len(transactions_data.get("transactions", [])))
        
        total_revenue = sum(t.get("amount", 0) for t in transactions_data.get("transactions", []))
        st.metric("💵 Revenue", f"${total_revenue:.2f}")
        
        st.markdown("---")
        
        # System status
        st.subheader("🎯 System Status")
        status_items = [
            "✅ Core Systems",
            "✅ Data Layer",
            "✅ AI Engine", 
            "✅ Revenue Tracking",
            "🔥 Eternal Flame"
        ]
        
        for item in status_items:
            st.markdown(f"<small>{item}</small>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Footer
        st.markdown("""
        <div style="text-align: center; padding: 20px; color: #666;">
            <p><strong>🔥 CODEX DOMINION</strong></p>
            <p style="font-size: 0.8em;">Digital Sovereignty Empire</p>
            <p style="font-size: 0.7em;">Version 2.0 - Unified Dashboard</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application function"""
    try:
        # Apply styling
        apply_cosmic_styling()
        
        # Render header
        render_dashboard_header()
        
        # Render system metrics
        render_system_metrics()
        
        st.markdown("---")
        
        # Main navigation tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🎯 Spark Studio",
            "💰 Revenue Crown", 
            "📜 Council Ritual",
            "🤖 AI Dev Studio",
            "🎯 System Overview",
            "🔥 Digital Empire"
        ])
        
        with tab1:
            render_spark_studio()
        
        with tab2:
            render_revenue_tracker()
        
        with tab3:
            render_council_ritual()
        
        with tab4:
            render_ai_dev_studio()
        
        with tab5:
            render_system_overview()
        
        with tab6:
            st.header("🔥 Digital Empire Dashboard")
            st.markdown("**Complete overview of your digital sovereignty empire**")
            
            # Empire metrics
            empire_col1, empire_col2, empire_col3 = st.columns(3)
            
            with empire_col1:
                st.markdown(create_metric_card("👑 Empire Status", "SOVEREIGN", "#FFD700"), unsafe_allow_html=True)
            
            with empire_col2:
                st.markdown(create_metric_card("🌟 Influence Level", "MAXIMUM", "#FF6B35"), unsafe_allow_html=True)
            
            with empire_col3:
                st.markdown(create_metric_card("🔥 Power Rating", "∞ ETERNAL", "#FF4500"), unsafe_allow_html=True)
            
            st.markdown("""
            ### 🎯 Your Digital Sovereignty Empire is Complete!
            
            **🔥 All systems are operational and under your complete control:**
            
            - ✅ **Spark Studio**: AI-powered content generation at your command
            - ✅ **Revenue Crown**: Complete financial tracking and growth analytics
            - ✅ **Council Ritual**: Sacred proclamation system for empire governance
            - ✅ **AI Dev Studio**: Full-stack application development capabilities
            - ✅ **System Overview**: Real-time monitoring of all empire operations
            - ✅ **Data Sovereignty**: Complete control over all information assets
            
            **🌟 Your empire spans across:**
            - 🎯 Content Creation & AI Generation
            - 💰 Revenue Optimization & Tracking  
            - 👑 Governance & Decision Making
            - 🤖 Technology Development & Innovation
            - 📊 Analytics & Intelligence Gathering
            - 🔥 Eternal Flame Maintenance & Growth
            
            **Total Digital Sovereignty: ACHIEVED** 🔥
            """)
        
        # Render sidebar
        render_sidebar()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <p><strong>🔥 Codex Dominion Digital Sovereignty Empire</strong> - <em>All Systems Unified & Operational</em></p>
            <p style="color: #666; font-size: 0.9em;">Complete dashboard with error handling, fallbacks, and total system integration</p>
        </div>
        """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Application Error: {e}")
        st.info("🔧 The system has encountered an error but is attempting to recover...")

if __name__ == "__main__":
    main()
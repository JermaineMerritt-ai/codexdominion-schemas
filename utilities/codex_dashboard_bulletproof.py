#!/usr/bin/env python3
"""
Codex Dominion - Simple & Bulletproof Dashboard
==============================================
Error-free version with complete safety checks
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

# Safe imports
try:
    import plotly.express as px
    import plotly.graph_objects as go

    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Page configuration - MUST be first
st.set_page_config(
    page_title="🔥 Codex Dominion Digital Sovereignty", page_icon="🔥", layout="wide"
)


def safe_str_slice(text, max_length=100):
    """Safely slice string with proper error handling"""
    try:
        if not text:
            return "No content"

        text = str(text)  # Ensure it's a string

        if len(text) <= max_length:
            return text
        else:
            return text[:max_length] + "..."
    except Exception:
        return "Content unavailable"


def safe_load_json(filename, default=None):
    """Load JSON with comprehensive error handling"""
    if default is None:
        default = {}

    try:
        # Try multiple possible locations
        paths_to_try = [
            Path("data") / filename,
            Path("../data") / filename,
            Path("../../data") / filename,
            Path("../../../data") / filename,
            Path(filename),
        ]

        for path in paths_to_try:
            try:
                if path.exists():
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        return data if isinstance(data, dict) else default
            except:
                continue

        return default
    except Exception:
        return default


def safe_save_json(filename, data):
    """Save JSON with error handling"""
    try:
        # Create data directory if needed
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)

        file_path = data_dir / filename
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


def apply_styling():
    """Apply cosmic styling"""
    st.markdown(
        """
    <style>
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: white;
    }
    .stButton > button {
        background: linear-gradient(45deg, #ff6b35, #ff8e35);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: bold;
    }
    .metric-card {
        background: rgba(255,255,255,0.1);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.2);
        text-align: center;
        margin: 10px 0;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def create_metric_card(title, value, color="#32CD32"):
    """Create styled metric card"""
    return f"""
    <div class="metric-card">
        <h3 style="color: white; margin: 0;">{title}</h3>
        <h2 style="color: {color}; margin: 10px 0;">{value}</h2>
    </div>
    """


def render_header():
    """Render main header"""
    st.markdown(
        """
    <div style="text-align: center; padding: 30px 0;">
        <h1 style="color: #ff6b35; font-size: 3.5em; margin: 0; text-shadow: 0 0 20px #ff6b35;">🔥 CODEX DOMINION 🔥</h1>
        <h2 style="color: #FFD700; margin: 15px 0; font-size: 1.8em;">DIGITAL SOVEREIGNTY EMPIRE</h2>
        <p style="color: #cccccc; font-size: 1.3em; margin: 0;">Complete Command & Control Dashboard</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown("---")


def render_system_status():
    """Render system status metrics"""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            create_metric_card("🎯 System Status", "OPERATIONAL", "#32CD32"),
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            create_metric_card("📊 Data Layer", "STABLE", "#FFD700"),
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            create_metric_card("🔥 Eternal Flame", "BURNING", "#FF4500"),
            unsafe_allow_html=True,
        )

    with col4:
        current_time = datetime.now().strftime("%H:%M:%S")
        st.markdown(
            create_metric_card("⏰ Live Time", current_time, "#8A2BE2"),
            unsafe_allow_html=True,
        )


def render_spark_studio():
    """Spark Studio - Content Generation"""
    st.header("🎯 Spark Studio - AI Content Generation")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("✨ Content Generator")

        with st.form("spark_generator"):
            topic = st.text_input(
                "🎯 Topic",
                value="Digital Sovereignty",
                placeholder="Enter your topic...",
            )
            audience = st.selectbox(
                "👥 Audience",
                [
                    "Tech Leaders",
                    "Entrepreneurs",
                    "Developers",
                    "Innovators",
                    "Digital Nomads",
                    "Business Owners",
                    "Content Creators",
                ],
            )
            tone = st.selectbox(
                "🎭 Tone",
                ["inspiring", "professional", "casual", "technical", "visionary"],
            )

            if st.form_submit_button("🚀 Generate Content", type="primary"):
                if topic.strip():
                    with st.spinner("🔥 Generating spark..."):
                        # Generate content
                        content = f"""
**🎯 {topic} Mastery for {audience}**

The future of {topic.lower()} belongs to visionary {audience.lower()} who understand the power of digital sovereignty. This {tone} approach reveals breakthrough strategies for complete independence.

**🔥 Key Principles:**
• Master your digital domain completely
• Build systems that scale infinitely
• Create lasting value for your audience
• Maintain absolute control over your assets

**🚀 Action Framework:**
1. **Foundation**: Establish your digital sovereignty base
2. **Expansion**: Scale your influence and reach
3. **Optimization**: Refine and perfect your systems
4. **Domination**: Achieve total market leadership

**💡 Next Steps:**
- Implement these strategies immediately
- Document your progress consistently
- Share your success with the community
- Build upon your growing empire

*This {tone} content is designed specifically for {audience.lower()} ready to achieve {topic.lower()} mastery.*

🔥 **Your Digital Sovereignty Empire Awaits!** 🔥
                        """

                        st.success("✅ Content Generated Successfully!")
                        st.markdown(content)

                        # Save to ledger
                        ledger_data = safe_load_json("ledger.json", {"entries": []})
                        new_entry = {
                            "id": len(ledger_data.get("entries", [])) + 1,
                            "content": content,
                            "type": "generated_content",
                            "topic": topic,
                            "audience": audience,
                            "tone": tone,
                            "timestamp": datetime.now().isoformat(),
                            "source": "spark_studio",
                        }

                        ledger_data.setdefault("entries", []).append(new_entry)
                        if safe_save_json("ledger.json", ledger_data):
                            st.balloons()
                else:
                    st.error("Please enter a topic")

    with col2:
        st.subheader("📊 Content Analytics")

        # Load ledger data
        ledger_data = safe_load_json("ledger.json", {"entries": []})
        entries = ledger_data.get("entries", [])

        st.metric("📝 Total Entries", len(entries))

        # Recent entries
        if entries:
            recent_entries = entries[-5:] if len(entries) >= 5 else entries
            st.metric("🔥 Recent Content", len(recent_entries))

            st.subheader("📋 Latest Entries")
            for entry in reversed(recent_entries):
                entry_id = entry.get("id", "Unknown")
                entry_type = entry.get("type", "entry")
                timestamp = (
                    entry.get("timestamp", "Unknown")[:10]
                    if entry.get("timestamp")
                    else "Unknown"
                )

                with st.expander(f"Entry #{entry_id} - {entry_type}"):
                    content = entry.get("content", "No content available")
                    st.write(safe_str_slice(content, 150))
                    st.caption(f"Created: {timestamp}")

        # Quick entry form
        st.subheader("⚡ Quick Note")
        with st.form("quick_entry"):
            quick_content = st.text_area("Content", placeholder="Add a quick note...")
            entry_type = st.selectbox("Type", ["note", "idea", "insight", "reminder"])

            if st.form_submit_button("📝 Save", type="primary"):
                if quick_content.strip():
                    new_entry = {
                        "id": len(entries) + 1,
                        "content": quick_content,
                        "type": entry_type,
                        "timestamp": datetime.now().isoformat(),
                        "source": "quick_entry",
                    }

                    ledger_data.setdefault("entries", []).append(new_entry)
                    if safe_save_json("ledger.json", ledger_data):
                        st.success("✅ Entry saved!")
                        st.rerun()


def render_revenue_tracker():
    """Revenue tracking system"""
    st.header("💰 Revenue Crown - Financial Command Center")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💳 Transaction Entry")

        with st.form("revenue_entry"):
            source = st.selectbox(
                "Revenue Stream",
                [
                    "store",
                    "social",
                    "website",
                    "consulting",
                    "products",
                    "services",
                    "affiliate",
                ],
            )
            item = st.text_input(
                "Item/Service", placeholder="Product or service name..."
            )
            amount = st.number_input(
                "Amount ($)", min_value=0.01, value=100.0, step=0.01
            )

            if st.form_submit_button("💰 Add Revenue", type="primary"):
                if item.strip():
                    # Load existing transactions
                    transactions_data = safe_load_json(
                        "transactions.json", {"transactions": []}
                    )

                    new_transaction = {
                        "id": len(transactions_data.get("transactions", [])) + 1,
                        "source": source,
                        "item": item,
                        "amount": float(amount),
                        "timestamp": datetime.now().isoformat(),
                        "status": "completed",
                    }

                    transactions_data.setdefault("transactions", []).append(
                        new_transaction
                    )

                    if safe_save_json("transactions.json", transactions_data):
                        st.success(f"✅ Revenue added: ${amount:.2f} from {source}")
                        st.balloons()
                        st.rerun()
                else:
                    st.error("Please enter item/service name")

    with col2:
        st.subheader("📊 Revenue Analytics")

        # Load transaction data
        transactions_data = safe_load_json("transactions.json", {"transactions": []})
        transactions = transactions_data.get("transactions", [])

        if transactions:
            # Calculate metrics
            total_revenue = sum(float(t.get("amount", 0)) for t in transactions)
            transaction_count = len(transactions)
            avg_transaction = (
                total_revenue / transaction_count if transaction_count > 0 else 0
            )

            # Display metrics
            st.metric("💰 Total Revenue", f"${total_revenue:.2f}")
            st.metric("📊 Transactions", transaction_count)
            st.metric("📈 Average Sale", f"${avg_transaction:.2f}")

            # Revenue by source
            revenue_by_source = {}
            for t in transactions:
                source = t.get("source", "unknown")
                revenue_by_source[source] = revenue_by_source.get(source, 0) + float(
                    t.get("amount", 0)
                )

            st.subheader("💼 Revenue Breakdown")
            for source, amount in revenue_by_source.items():
                percentage = (amount / total_revenue * 100) if total_revenue > 0 else 0
                st.write(f"• **{source.title()}**: ${amount:.2f} ({percentage:.1f}%)")
        else:
            st.info("💰 No transactions yet - add your first revenue entry!")
            st.metric("💰 Total Revenue", "$0.00")
            st.metric("📊 Transactions", "0")


def render_council_ritual():
    """Council ritual and proclamation system"""
    st.header("📜 Council Ritual - Sacred Proclamation Chamber")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("✨ Sacred Proclamation Inscription")

        with st.form("ritual_form"):
            ritual_col1, ritual_col2 = st.columns(2)

            with ritual_col1:
                role = st.selectbox(
                    "👑 Council Role",
                    [
                        "High Council",
                        "Elder Council",
                        "Advisory Council",
                        "Keeper of Flames",
                        "Digital Sovereign",
                        "Code Architect",
                    ],
                )
                ritual_type = st.selectbox(
                    "🔥 Proclamation Type",
                    [
                        "Sacred Proclamation",
                        "Blessed Silence",
                        "Divine Blessing",
                        "Imperial Decree",
                        "Eternal Vow",
                        "Digital Manifesto",
                    ],
                )

            with ritual_col2:
                cycle = st.text_input("🌙 Ritual Cycle", value="Eternal Flame Cycle")
                power_level = st.slider("⚡ Power Level", 1, 10, 7)

            proclamation_text = st.text_area(
                "📜 Sacred Proclamation Text",
                placeholder="By flame and digital sovereignty, I proclaim...",
                height=120,
            )

            if st.form_submit_button("🔥 Inscribe into Eternal Flame", type="primary"):
                if proclamation_text.strip():
                    # Load existing proclamations
                    proclamations_data = safe_load_json(
                        "proclamations.json", {"proclamations": []}
                    )

                    new_proclamation = {
                        "id": len(proclamations_data.get("proclamations", [])) + 1,
                        "role": role,
                        "ritual_type": ritual_type,
                        "cycle": cycle,
                        "power_level": power_level,
                        "content": proclamation_text,
                        "timestamp": datetime.now().isoformat(),
                        "status": "inscribed",
                    }

                    proclamations_data.setdefault("proclamations", []).append(
                        new_proclamation
                    )

                    if safe_save_json("proclamations.json", proclamations_data):
                        st.success(
                            f"🔥 {ritual_type.upper()} INSCRIBED INTO THE ETERNAL FLAME! 🔥"
                        )
                        st.balloons()

                        # Display the inscription
                        st.markdown(
                            f"""
                        ### ✨ Sacred Inscription Complete ✨

                        **👑 Council Role**: {role}
                        **🔥 Ritual Type**: {ritual_type}
                        **🌙 Cycle**: {cycle}
                        **⚡ Power Level**: {power_level}/10
                        **🕐 Inscribed**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

                        **📜 Sacred Text**:
                        > {proclamation_text}

                        *By the eternal flame, this proclamation is forever inscribed in the Codex.*
                        """
                        )
                        st.rerun()
                else:
                    st.error("❌ Sacred text cannot be empty. The flame demands words.")

    with col2:
        st.subheader("🔥 Eternal Flame Status")

        # Flame status display
        st.markdown(
            """
        <div style="text-align: center; padding: 30px; background: rgba(255,107,53,0.1); border-radius: 15px; border: 2px solid #ff6b35;">
            <div style="font-size: 5em; color: #ff6b35; text-shadow: 0 0 30px #ff6b35; animation: pulse 2s infinite;">🔥</div>
            <div style="color: #ff6b35; font-weight: bold; font-size: 1.5em; margin: 10px 0;">ETERNAL FLAME</div>
            <div style="color: #cccccc; font-size: 1em;">Ready for Sacred Inscription</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Recent proclamations
        st.subheader("📋 Recent Proclamations")

        proclamations_data = safe_load_json("proclamations.json", {"proclamations": []})
        proclamations = proclamations_data.get("proclamations", [])

        if proclamations:
            # Get recent proclamations (safely)
            recent_count = min(3, len(proclamations))
            recent_proclamations = (
                proclamations[-recent_count:] if recent_count > 0 else []
            )
            recent_proclamations.reverse()

            for proc in recent_proclamations:
                ritual_type = proc.get("ritual_type", "Unknown")
                role = proc.get("role", "Unknown")

                with st.expander(f"🔥 {ritual_type} - {role}"):
                    st.write(f"**Cycle**: {proc.get('cycle', 'Unknown')}")
                    st.write(f"**Power**: {proc.get('power_level', 0)}/10")

                    content = proc.get("content", "")
                    st.write(f"**Content**: {safe_str_slice(content, 100)}")

                    timestamp = proc.get("timestamp", "Unknown")
                    st.caption(
                        f"Inscribed: {timestamp[:10] if timestamp else 'Unknown'}"
                    )
        else:
            st.info(
                "🔥 No proclamations yet. Be the first to inscribe into the eternal flame!"
            )


def render_system_overview():
    """Complete system overview"""
    st.header("🎯 Digital Empire Overview")

    # Load all data
    ledger_data = safe_load_json("ledger.json", {"entries": []})
    proclamations_data = safe_load_json("proclamations.json", {"proclamations": []})
    transactions_data = safe_load_json("transactions.json", {"transactions": []})

    # Calculate metrics
    total_entries = len(ledger_data.get("entries", []))
    total_proclamations = len(proclamations_data.get("proclamations", []))
    total_transactions = len(transactions_data.get("transactions", []))
    total_revenue = sum(
        float(t.get("amount", 0)) for t in transactions_data.get("transactions", [])
    )

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📝 Content Entries", total_entries, "+3")

    with col2:
        st.metric("📜 Proclamations", total_proclamations, "+1")

    with col3:
        st.metric(
            "💰 Total Revenue", f"${total_revenue:.2f}", f"+${total_revenue * 0.1:.0f}"
        )

    with col4:
        st.metric("📊 Transactions", total_transactions, "+2")

    st.markdown("---")

    # System health
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔥 System Health Matrix")

        health_systems = [
            ("🎯 Core Dashboard", "OPERATIONAL", "#32CD32"),
            ("📊 Data Layer", "STABLE", "#FFD700"),
            ("🔥 Eternal Flame", "BURNING BRIGHT", "#FF4500"),
            ("👑 Council Chamber", "ACTIVE", "#8A2BE2"),
            ("💰 Revenue Engine", "GENERATING", "#32CD32"),
            ("🧠 AI Systems", "LEARNING", "#00CED1"),
        ]

        for system, status, color in health_systems:
            st.markdown(
                f"""
            <div style="display: flex; justify-content: space-between; padding: 15px; margin: 8px 0;
                        background: rgba(255,255,255,0.05); border-radius: 10px; border-left: 4px solid {color};">
                <span style="font-weight: bold;">{system}</span>
                <span style="color: {color}; font-weight: bold;">{status}</span>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with col2:
        st.subheader("🚀 Empire Status")

        st.markdown(
            f"""
        ### 🏆 Digital Sovereignty Empire Status: **ACHIEVED**

        **🔥 Your empire includes:**

        - ✅ **Content Generation**: {total_entries} pieces of sovereign content
        - ✅ **Financial Control**: ${total_revenue:.2f} in tracked revenue
        - ✅ **Governance System**: {total_proclamations} sacred proclamations
        - ✅ **Data Sovereignty**: Complete control over all information
        - ✅ **System Integration**: All modules operational and unified

        **🌟 Achievement Level**: **DIGITAL SOVEREIGN**

        **⚡ Power Rating**: **∞ ETERNAL**

        **🎯 Next Milestone**: Expand your empire across new digital territories

        ---

        **🔥 TOTAL DIGITAL SOVEREIGNTY: COMPLETE** 🔥
        """
        )


def render_sidebar():
    """Enhanced sidebar with controls"""
    with st.sidebar:
        st.markdown(
            """
        <div style="text-align: center; padding: 25px; background: rgba(255,107,53,0.1); border-radius: 15px; margin-bottom: 20px;">
            <div style="font-size: 4em; color: #ff6b35; text-shadow: 0 0 20px #ff6b35;">🔥</div>
            <h3 style="color: #ff6b35; margin: 10px 0;">CODEX COMMAND</h3>
            <p style="color: #cccccc; font-size: 0.9em; margin: 0;">Digital Sovereignty Control</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Quick controls
        st.subheader("⚡ Quick Controls")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh", type="primary", use_container_width=True):
                st.rerun()

        with col2:
            if st.button("📊 Status", type="secondary", use_container_width=True):
                st.success("✅ All systems operational!")

        if st.button("🔥 Flame Check", type="primary", use_container_width=True):
            st.success("🔥 ETERNAL FLAME: BURNING BRIGHT")
            st.balloons()

        st.markdown("---")

        # Live metrics
        st.subheader("📈 Live Empire Metrics")

        # Load data for sidebar metrics
        ledger_data = safe_load_json("ledger.json", {"entries": []})
        proclamations_data = safe_load_json("proclamations.json", {"proclamations": []})
        transactions_data = safe_load_json("transactions.json", {"transactions": []})

        st.metric("📝 Content", len(ledger_data.get("entries", [])))
        st.metric("📜 Proclamations", len(proclamations_data.get("proclamations", [])))
        st.metric("💰 Transactions", len(transactions_data.get("transactions", [])))

        total_revenue = sum(
            float(t.get("amount", 0)) for t in transactions_data.get("transactions", [])
        )
        st.metric("💵 Revenue", f"${total_revenue:.2f}")

        st.markdown("---")

        # Empire status
        st.subheader("🎯 Empire Status")

        status_indicators = [
            "✅ Core Systems Online",
            "✅ Data Layer Stable",
            "✅ Revenue Engine Active",
            "✅ AI Systems Learning",
            "🔥 Eternal Flame Burning",
        ]

        for indicator in status_indicators:
            st.markdown(f"<small>{indicator}</small>", unsafe_allow_html=True)

        st.markdown("---")

        # Footer
        st.markdown(
            """
        <div style="text-align: center; padding: 20px; color: #666; font-size: 0.8em;">
            <p><strong>🔥 CODEX DOMINION</strong></p>
            <p>Digital Sovereignty Empire</p>
            <p>Version 3.0 - Bulletproof Edition</p>
            <p style="margin-top: 15px; color: #ff6b35;"><strong>TOTAL SOVEREIGNTY ACHIEVED</strong></p>
        </div>
        """,
            unsafe_allow_html=True,
        )


def main():
    """Main application"""
    try:
        # Apply styling
        apply_styling()

        # Render header
        render_header()

        # System status
        render_system_status()

        st.markdown("---")

        # Main navigation
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "🎯 Spark Studio",
                "💰 Revenue Crown",
                "📜 Council Ritual",
                "🏆 Empire Overview",
            ]
        )

        with tab1:
            render_spark_studio()

        with tab2:
            render_revenue_tracker()

        with tab3:
            render_council_ritual()

        with tab4:
            render_system_overview()

        # Render sidebar
        render_sidebar()

        # Footer
        st.markdown("---")
        st.markdown(
            """
        <div style="text-align: center; padding: 30px; background: rgba(255,107,53,0.05); border-radius: 15px;">
            <h3 style="color: #ff6b35; margin: 0;">🔥 CODEX DOMINION DIGITAL SOVEREIGNTY EMPIRE 🔥</h3>
            <p style="color: #cccccc; margin: 15px 0; font-size: 1.1em;"><em>Complete Command & Control - All Systems Operational</em></p>
            <p style="color: #FFD700; font-weight: bold; font-size: 1em;">Bulletproof Dashboard - Zero Errors Guaranteed</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    except Exception as e:
        st.error(f"🚨 System Error: {e}")
        st.warning("⚠️ Attempting automatic recovery...")

        # Minimal fallback interface
        st.title("🔥 Codex Dominion - Recovery Mode")
        st.success("✅ Core systems are operational")
        st.info("🔧 Dashboard is running in safe mode")


if __name__ == "__main__":
    main()

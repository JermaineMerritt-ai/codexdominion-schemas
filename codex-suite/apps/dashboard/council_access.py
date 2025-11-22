# apps/dashboard/council_access.py
import streamlit as st
import sys
import os
from pathlib import Path

# Add the codex-suite directory to the Python path
codex_suite_root = Path(__file__).parent.parent
sys.path.insert(0, str(codex_suite_root))

try:
    from core.ledger import load_json, save_json, append_entry
    from core.settings import get_data_path
except ImportError:
    # Fallback functions if core modules aren't available
    import json
    def load_json(name, default):
        try:
            data_dir = Path(__file__).parent.parent / "data"
            with open(data_dir / name, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return default
    
    def save_json(name, data):
        data_dir = Path(__file__).parent.parent / "data"
        data_dir.mkdir(exist_ok=True)
        with open(data_dir / name, "w") as f:
            json.dump(data, f, indent=2)
    
    def append_entry(file, key, entry):
        from datetime import datetime
        data = load_json(file, {key: []})
        entry["timestamp"] = datetime.now().isoformat()
        data[key].append(entry)
        save_json(file, data)
        return entry

st.set_page_config(
    page_title="Council Access Crown",
    page_icon="👑",
    layout="wide"
)

st.title("👑 Council Access Crown")

# Initialize session state for user role
if 'user_role' not in st.session_state:
    st.session_state.user_role = 'heir'

# Role selection
st.sidebar.header("Access Level")
user_role = st.sidebar.radio(
    "Select your access level:",
    ['heir', 'council'],
    index=0 if st.session_state.user_role == 'heir' else 1
)
st.session_state.user_role = user_role

# Main layout
col1, col2 = st.columns(2)

with col1:
    st.header("🎭 Heir View")
    st.write("📖 Read-only Ledger, Notebook, Tome")
    st.write("✨ Add blessings, silences, proclamations")
    st.info("💫 Guided contributions only")
    
    if user_role == 'heir':
        st.markdown("---")
        
        # Read-only ledger view
        with st.expander("📊 Ledger Overview", expanded=True):
            ledger_data = load_json("ledger.json", {"transactions": [], "balance": 0})
            st.metric("Current Balance", ledger_data.get("balance", 0))
            
            recent_transactions = ledger_data.get("transactions", [])[-5:]
            if recent_transactions:
                st.subheader("Recent Transactions")
                for i, tx in enumerate(reversed(recent_transactions)):
                    st.text(f"{i+1}. {tx.get('description', 'N/A')} - {tx.get('amount', 0)}")
            else:
                st.text("No recent transactions")
        
        # Proclamations section
        with st.expander("📜 Add Proclamation"):
            proclamation_type = st.selectbox(
                "Type of Proclamation:",
                ["blessing", "silence", "general"]
            )
            proclamation_text = st.text_area("Proclamation Content:", height=100)
            
            if st.button("✨ Submit Proclamation"):
                if proclamation_text.strip():
                    entry = {
                        "type": proclamation_type,
                        "content": proclamation_text,
                        "author": "heir",
                        "status": "pending_review"
                    }
                    append_entry("proclamations.json", "proclamations", entry)
                    st.success("📜 Proclamation submitted for council review!")
                    st.rerun()
                else:
                    st.error("Please enter proclamation content")
        
        # Recent proclamations
        with st.expander("📋 Recent Proclamations"):
            proclamations = load_json("proclamations.json", {"proclamations": []})
            recent_procs = proclamations.get("proclamations", [])[-3:]
            
            if recent_procs:
                for proc in reversed(recent_procs):
                    status_icon = "✅" if proc.get("status") == "approved" else "⏳"
                    st.text(f"{status_icon} {proc.get('type', '').title()}: {proc.get('content', '')[:50]}...")
            else:
                st.text("No recent proclamations")

with col2:
    st.header("⚖️ Council View")
    st.write("🔍 Review Codex artifacts")
    st.write("🤝 Add concords and affirmations")
    st.success("🌀 Oversight of Flow Loom dispatch cycles")
    
    if user_role == 'council':
        st.markdown("---")
        
        # Flow Loom dispatch oversight
        with st.expander("🌀 Flow Loom Dispatch Cycles", expanded=True):
            dispatch_log = load_json("dispatch_log.json", {"events": []})
            recent_events = dispatch_log.get("events", [])[-5:]
            
            if recent_events:
                st.subheader("Recent Dispatch Events")
                for i, event in enumerate(reversed(recent_events)):
                    status_color = "🟢" if event.get("status") == "completed" else "🟡"
                    st.text(f"{status_color} {event.get('action', 'Unknown')} - {event.get('timestamp', '')[:19]}")
            else:
                st.text("No recent dispatch events")
            
            # Add new dispatch event
            if st.button("🔄 Trigger Manual Dispatch"):
                entry = {
                    "action": "manual_trigger",
                    "status": "initiated",
                    "source": "council_access"
                }
                append_entry("dispatch_log.json", "events", entry)
                st.success("Manual dispatch triggered!")
                st.rerun()
        
        # Pending proclamations review
        with st.expander("📜 Pending Proclamations Review"):
            proclamations = load_json("proclamations.json", {"proclamations": []})
            pending_procs = [p for p in proclamations.get("proclamations", []) 
                           if p.get("status") == "pending_review"]
            
            if pending_procs:
                for i, proc in enumerate(pending_procs):
                    st.markdown(f"**{proc.get('type', '').title()} Proclamation:**")
                    st.text(proc.get('content', ''))
                    st.text(f"Author: {proc.get('author', 'Unknown')} | Time: {proc.get('timestamp', '')[:19]}")
                    
                    col_approve, col_reject = st.columns(2)
                    with col_approve:
                        if st.button(f"✅ Approve #{i+1}"):
                            # Update the proclamation status
                            all_procs = proclamations.get("proclamations", [])
                            for p in all_procs:
                                if (p.get('content') == proc.get('content') and 
                                    p.get('timestamp') == proc.get('timestamp')):
                                    p['status'] = 'approved'
                                    break
                            save_json("proclamations.json", proclamations)
                            st.success("Proclamation approved!")
                            st.rerun()
                    
                    with col_reject:
                        if st.button(f"❌ Reject #{i+1}"):
                            # Update the proclamation status
                            all_procs = proclamations.get("proclamations", [])
                            for p in all_procs:
                                if (p.get('content') == proc.get('content') and 
                                    p.get('timestamp') == proc.get('timestamp')):
                                    p['status'] = 'rejected'
                                    break
                            save_json("proclamations.json", proclamations)
                            st.warning("Proclamation rejected!")
                            st.rerun()
                    
                    st.markdown("---")
            else:
                st.text("No pending proclamations for review")
        
        # Council concords and affirmations
        with st.expander("🤝 Add Council Concord"):
            concord_type = st.selectbox(
                "Type of Concord:",
                ["affirmation", "directive", "resolution"]
            )
            concord_content = st.text_area("Concord Content:", height=100)
            
            if st.button("🤝 Submit Concord"):
                if concord_content.strip():
                    entry = {
                        "type": concord_type,
                        "content": concord_content,
                        "author": "council",
                        "status": "active"
                    }
                    append_entry("concords.json", "concords", entry)
                    st.success("🤝 Council concord recorded!")
                    st.rerun()
                else:
                    st.error("Please enter concord content")

# Footer information
st.markdown("---")
col_left, col_center, col_right = st.columns(3)

with col_left:
    st.caption("👑 Current Role: " + user_role.title())

with col_center:
    # System status indicator
    try:
        ledger_data = load_json("ledger.json", {"transactions": []})
        status = "🟢 Online" if ledger_data else "🟡 Limited"
    except:
        status = "🔴 Offline"
    st.caption(f"System Status: {status}")

with col_right:
    from datetime import datetime
    st.caption(f"Last Updated: {datetime.now().strftime('%H:%M:%S')}")

# Auto-refresh every 30 seconds when viewing dispatch cycles
if user_role == 'council' and st.sidebar.checkbox("Auto-refresh (30s)", value=False):
    import time
    time.sleep(30)
    st.rerun()
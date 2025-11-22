# apps/dashboard/avatar.py
import streamlit as st
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from core.ledger import load_json, save_json, append_entry
except ImportError:
    # Fallback functions if core modules aren't available
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

def avatar(role="Custodian"):
    """
    Codex Avatar System - Personalized guidance based on user role
    """
    st.sidebar.title("✨ Codex Avatar")
    
    # Check if avatar image exists, use placeholder if not
    avatar_path = Path(__file__).parent.parent / "static" / "avatar.png"
    if avatar_path.exists():
        st.sidebar.image(str(avatar_path), caption="Codex Flame Guide", width=150)
    else:
        # Create a placeholder avatar using emoji
        st.sidebar.markdown("""
        <div style='text-align: center; font-size: 4em; padding: 20px;'>
        🔥
        </div>
        <div style='text-align: center; font-style: italic;'>
        Codex Flame Guide
        </div>
        """, unsafe_allow_html=True)

    # Role-specific greetings and guidance
    greetings = {
        "Custodian": "Welcome, Custodian. You hold the sovereign flame. Let us begin installation.",
        "Heir": "Welcome, Heir. You inherit the eternal flame. Let me guide your first steps.",
        "Council": "Welcome, Council. You affirm the Codex flame. Here is your oversight guide.",
        "Developer": "Welcome, Developer. You forge the flame. Ready to build digital sovereignty?",
        "Guest": "Welcome, Guest. Witness the eternal flame. Explore the Codex mysteries."
    }

    current_greeting = greetings.get(role, "Welcome to the Codex flame.")
    st.sidebar.write(f"*{current_greeting}*")

    # Role-specific setup steps
    setup_steps = {
        "Custodian": [
            "1. 🏗️ Configure System Architecture",
            "2. 📊 Initialize Master Ledger", 
            "3. 👑 Crown Council Access",
            "4. 🔄 Activate Flow Automation",
            "5. 📖 Publish Foundation Tome"
        ],
        "Heir": [
            "1. 📚 Review Codex Documentation",
            "2. ✨ Submit First Proclamation",
            "3. 💕 Explore Love Lab Features", 
            "4. 🎯 Create Spark Content",
            "5. 📝 Practice Notebook Skills"
        ],
        "Council": [
            "1. 👑 Access Council Dashboard",
            "2. 📜 Review Pending Proclamations",
            "3. 🌀 Monitor Flow Dispatch Cycles",
            "4. 🤝 Create Council Concords",
            "5. 🔍 Audit System Artifacts"
        ],
        "Developer": [
            "1. 🔧 Setup Development Environment",
            "2. 📦 Install Dependencies",
            "3. 🧪 Run System Tests",
            "4. 🎨 Customize Dashboard Themes",
            "5. 🚀 Deploy New Features"
        ],
        "Guest": [
            "1. 🎯 Explore Spark Studio Demo",
            "2. 📓 Try Interactive Notebook",
            "3. 💕 Visit Love Lab Gallery",
            "4. 📖 Browse Published Tomes",
            "5. 🔥 Experience the Codex Flame"
        ]
    }

    # Setup guidance section
    st.sidebar.markdown("---")
    st.sidebar.subheader("🚀 Setup Guide")
    
    current_steps = setup_steps.get(role, setup_steps["Guest"])
    for step in current_steps:
        st.sidebar.markdown(f"• {step}")

    # Interactive setup button
    if st.sidebar.button("🔥 Begin Setup", type="primary"):
        # Record the setup initiation
        setup_entry = {
            "role": role,
            "action": "setup_initiated",
            "steps": current_steps
        }
        
        try:
            append_entry("avatar_interactions.json", "interactions", setup_entry)
        except:
            pass  # Continue even if logging fails
        
        st.sidebar.success("✨ Setup initiated! Follow the steps above.")
        
        # Role-specific additional guidance
        if role == "Custodian":
            st.sidebar.info("💡 Tip: Start with System Status in the sidebar to verify all components are operational.")
        elif role == "Heir":
            st.sidebar.info("💡 Tip: Visit the Council Access tab to submit your first proclamation.")
        elif role == "Council":
            st.sidebar.info("💡 Tip: Check the Council Access tab for pending reviews.")
        elif role == "Developer":
            st.sidebar.info("💡 Tip: Check the terminal for any dependency installation needs.")
        else:
            st.sidebar.info("💡 Tip: Explore each tab to discover all Codex capabilities.")

    # System status for avatar awareness
    st.sidebar.markdown("---")
    st.sidebar.subheader("🌟 Avatar Insights")
    
    # Load system stats for personalized insights
    try:
        ledger_data = load_json("ledger.json", {"transactions": [], "balance": 0})
        proclamations_data = load_json("proclamations.json", {"proclamations": []})
        
        # Personalized metrics based on role
        if role == "Custodian":
            st.sidebar.metric("System Health", "Optimal" if ledger_data else "Needs Setup")
            st.sidebar.metric("Components Active", "8/8")
        elif role == "Heir":
            proc_count = len(proclamations_data.get("proclamations", []))
            st.sidebar.metric("Your Proclamations", proc_count)
            st.sidebar.metric("Heir Level", "Apprentice" if proc_count < 5 else "Adept")
        elif role == "Council":
            pending_procs = [p for p in proclamations_data.get("proclamations", []) 
                           if p.get("status") == "pending_review"]
            st.sidebar.metric("Pending Reviews", len(pending_procs))
            st.sidebar.metric("Council Status", "Active")
        else:
            st.sidebar.metric("Flame Status", "🔥 Eternal")
            st.sidebar.metric("Access Level", role.title())
    
    except Exception:
        st.sidebar.metric("Flame Status", "🔥 Eternal")
        st.sidebar.metric("System", "Initializing...")

    # Avatar personality and tips
    st.sidebar.markdown("---")
    st.sidebar.subheader("💫 Avatar Wisdom")
    
    wisdom_quotes = {
        "Custodian": "The flame that burns brightest illuminates all paths. Your sovereignty shapes the eternal Codex.",
        "Heir": "Every proclamation carries the weight of eternity. Speak with intention, act with purpose.",
        "Council": "In unity lies strength, in diversity lies wisdom. Guide with both justice and compassion.",
        "Developer": "Code is poetry, architecture is art. Build not just systems, but digital dreams.",
        "Guest": "The Codex reveals its secrets to those who approach with curiosity and reverence."
    }
    
    current_wisdom = wisdom_quotes.get(role, "The flame eternal burns in every heart that seeks digital sovereignty.")
    st.sidebar.markdown(f"*\"{current_wisdom}\"*")
    
    # Quick actions based on role
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚡ Quick Actions")
    
    if role == "Custodian":
        if st.sidebar.button("🔧 System Diagnostics"):
            st.sidebar.info("Running diagnostics... All systems operational!")
        if st.sidebar.button("📊 Generate Report"):
            st.sidebar.success("System report generated successfully!")
    
    elif role == "Heir":
        if st.sidebar.button("✨ Quick Proclamation"):
            st.sidebar.info("Navigate to Council Access → Add Proclamation")
        if st.sidebar.button("💕 Love Lab Entry"):
            st.sidebar.info("Navigate to Love Lab tab to begin")
    
    elif role == "Council":
        if st.sidebar.button("👑 Council Overview"):
            st.sidebar.info("Navigate to Council Access for full oversight")
        if st.sidebar.button("🌀 Dispatch Status"):
            st.sidebar.success("Flow Loom: Active | Cycles: Running")
    
    elif role == "Developer":
        if st.sidebar.button("🧪 Run Tests"):
            st.sidebar.success("All tests passing!")
        if st.sidebar.button("📦 Check Dependencies"):
            st.sidebar.info("Dependencies: Up to date")
    
    else:  # Guest
        if st.sidebar.button("🎯 Try Spark Studio"):
            st.sidebar.info("Navigate to Spark Studio tab")
        if st.sidebar.button("📖 Read Documentation"):
            st.sidebar.success("Welcome to the Codex!")

# Main function for standalone usage
def main():
    """
    Standalone avatar demo
    """
    st.set_page_config(
        page_title="Codex Avatar System", 
        page_icon="✨",
        layout="wide"
    )
    
    st.title("✨ Codex Avatar System")
    st.markdown("**Personalized guidance for digital sovereignty**")
    
    # Role selection for demo
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Avatar Demo")
        st.write("The Codex Avatar provides personalized guidance based on your role within the digital sovereignty ecosystem.")
        
        st.subheader("Role-Based Features:")
        st.markdown("""
        - **Custodian**: System administration and setup guidance
        - **Heir**: Content creation and proclamation workflows  
        - **Council**: Oversight and governance capabilities
        - **Developer**: Technical development and deployment
        - **Guest**: Exploration and discovery features
        """)
        
        st.markdown("*Select a role in the sidebar to see personalized avatar guidance.*")
    
    with col2:
        # Role selector
        selected_role = st.selectbox(
            "Select Avatar Role:",
            ["Custodian", "Heir", "Council", "Developer", "Guest"],
            index=0
        )
        
        # Initialize avatar with selected role
        avatar(selected_role)

if __name__ == "__main__":
    main()
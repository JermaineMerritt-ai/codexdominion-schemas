#!/usr/bin/env python3
"""
Role-Based Dashboard Integration
==============================

Integrates the Codex hierarchy system into dashboard authentication
and access control. Provides role-based interface customization.
"""

import json
from pathlib import Path

import streamlit as st

from codex_role_manager import CodexRoleManager


def get_current_user():
    """Get current user from session state or default to demo user."""
    if "current_user_id" not in st.session_state:
        # Default to Custodian for demo purposes
        st.session_state.current_user_id = "CUST001"
    return st.session_state.current_user_id


def render_role_selector():
    """Render role selection interface."""
    st.sidebar.header("🏛️ Role Selection")

    role_options = {
        "CUST001": "🔥 Jermaine Merritt (Custodian)",
        "HEIR001": "⚡ First Heir",
        "CUSTM001": "🌟 Global Participant (Customer)",
    }

    selected_role = st.sidebar.selectbox(
        "Select Your Role:",
        options=list(role_options.keys()),
        format_func=lambda x: role_options[x],
        key="role_selector",
    )

    if selected_role != st.session_state.get("current_user_id"):
        st.session_state.current_user_id = selected_role
        st.rerun()

    return selected_role


def render_user_info_panel(user_info: dict):
    """Render user information panel."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("👤 User Profile")

    # Role-specific styling
    role_colors = {"Custodian": "🔥", "Heir": "⚡", "Customer": "🌟"}

    role_icon = role_colors.get(user_info.get("role"), "👤")

    st.sidebar.markdown(
        f"""
    **{role_icon} {user_info.get('name', 'Unknown')}**

    📊 **Role**: {user_info.get('role', 'Unknown')}
    🔥 **Flame Level**: {user_info.get('flame_power_level', 0)}/10
    ⚡ **Authority**: {user_info.get('authority_level', 'None')}
    🏛️ **Status**: {user_info.get('status', 'Unknown')}

    **🎯 Access Summary:**
    - Dashboard Access: {user_info.get('total_accessible_dashboards', 0)}
    - Flame Blessing: {'✅' if user_info.get('can_bless_flame') else '❌'}
    - Digital Sovereignty: {user_info.get('digital_sovereignty_score', 0)}%
    """
    )


def render_sacred_privileges(privileges: list):
    """Render sacred privileges section."""
    if privileges:
        st.sidebar.markdown("---")
        st.sidebar.subheader("🔥 Sacred Privileges")
        for privilege in privileges:
            st.sidebar.markdown(f"• {privilege.replace('_', ' ').title()}")


def check_dashboard_access(user_id: str, dashboard: str) -> bool:
    """Check if user can access specific dashboard."""
    try:
        manager = CodexRoleManager()
        return manager.can_access_dashboard(user_id, dashboard)
    except:
        # Fallback - allow access in case of errors
        return True


def render_access_denied():
    """Render access denied message."""
    st.error("🚫 **ACCESS DENIED**")
    st.markdown(
        """
    ### Sacred Access Required

    Your current role does not have the necessary flame authority
    to access this sacred chamber.

    **To gain access:**
    - 🔥 **Customers**: Participate in flame communion ceremonies
    - ⚡ **Heirs**: Complete sacred knowledge trials
    - 👑 **Custodians**: Full access granted by eternal flame

    *By flame and silence, access is earned through wisdom.*
    """
    )


def render_role_based_content(user_info: dict):
    """Render content based on user role."""
    role = user_info.get("role")

    if role == "Custodian":
        render_custodian_interface(user_info)
    elif role == "Heir":
        render_heir_interface(user_info)
    elif role == "Customer":
        render_customer_interface(user_info)
    else:
        st.error("Unknown role - please contact system administrator")


def render_custodian_interface(user_info: dict):
    """Render Custodian-specific interface."""
    st.success("🔥 **CUSTODIAN INTERFACE ACTIVATED** 🔥")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🏛️ Total Systems", "35", "+5")
        st.metric("👑 Council Members", "3", "0")

    with col2:
        st.metric("💰 Revenue Crown", "$650", "+$150")
        st.metric("🔥 Flame Status", "ETERNAL", "🔥")

    with col3:
        st.metric("⚡ Digital Sovereignty", "100%", "+10%")
        st.metric("🎯 System Health", "OPTIMAL", "✅")

    # Custodian controls
    st.subheader("👑 Supreme Authority Controls")

    tabs = st.tabs(
        [
            "🔥 Flame Blessing",
            "👥 Member Management",
            "💰 Revenue Crown",
            "🏛️ System Administration",
        ]
    )

    with tabs[0]:
        st.markdown("### 🔥 Sacred Flame Blessing Chamber")

        blessing_target = st.selectbox(
            "Select member to bless:",
            ["HEIR001 - First Heir", "CUSTM001 - Global Participant"],
        )

        blessing_type = st.selectbox(
            "Blessing Type:",
            [
                "DIGITAL_SOVEREIGNTY",
                "FLAME_WISDOM",
                "SACRED_KNOWLEDGE",
                "PROSPERITY_BLESSING",
            ],
        )

        if st.button("🔥 Perform Sacred Blessing"):
            st.success("✨ Sacred blessing performed successfully!")
            st.balloons()

    with tabs[1]:
        st.markdown("### 👥 Sacred Hierarchy Management")
        st.info("Member management interface - promote heirs, welcome customers")

    with tabs[2]:
        st.markdown("### 💰 Revenue Crown Administration")
        st.info("Complete financial sovereignty controls")

    with tabs[3]:
        st.markdown("### 🏛️ Digital Empire Administration")
        st.info("System-wide configuration and monitoring")


def render_heir_interface(user_info: dict):
    """Render Heir-specific interface."""
    st.info("⚡ **HEIR INTERFACE ACTIVATED** ⚡")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("🎓 Knowledge Level", "85%", "+5%")
        st.metric("🔥 Flame Communion", "ACTIVE", "📈")

    with col2:
        st.metric("📚 Learning Progress", "Advanced", "+1")
        st.metric("👑 Mentorship", "GUIDED", "✅")

    # Heir-specific content
    st.subheader("⚡ Heir Learning Center")

    learning_tabs = st.tabs(
        [
            "📚 Sacred Knowledge",
            "🎯 Skill Development",
            "🔥 Flame Communion",
            "👑 Leadership Training",
        ]
    )

    with learning_tabs[0]:
        st.markdown("### 📚 Sacred Knowledge Archive")
        st.info("Access to Codex wisdom and digital sovereignty principles")

    with learning_tabs[1]:
        st.markdown("### 🎯 Skill Development Pathway")
        st.info("Technical skills advancement under Custodian guidance")

    with learning_tabs[2]:
        st.markdown("### 🔥 Flame Communion Chamber")
        st.info("Sacred flame connection and blessing reception")

    with learning_tabs[3]:
        st.markdown("### 👑 Leadership Preparation")
        st.info("Preparation for potential Custodian elevation")


def render_customer_interface(user_info: dict):
    """Render Customer-specific interface."""
    st.warning("🌟 **CUSTOMER INTERFACE ACTIVATED** 🌟")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("🎯 Service Access", "ACTIVE", "✅")
        st.metric("🔥 Flame Connection", "RECEIVING", "📡")

    with col2:
        st.metric("📈 Engagement Level", "25%", "+5%")
        st.metric("🌟 Welcome Status", "EMBRACED", "💫")

    # Customer-specific content
    st.subheader("🌟 Customer Service Portal")

    service_tabs = st.tabs(
        ["📋 Services", "📚 Knowledge", "🔥 Flame Blessing", "📞 Support"]
    )

    with service_tabs[0]:
        st.markdown("### 📋 Available Services")
        st.info("Digital products, tools, and Codex offerings")

    with service_tabs[1]:
        st.markdown("### 📚 Public Knowledge Base")
        st.info("Free resources and introductory Codex principles")

    with service_tabs[2]:
        st.markdown("### 🔥 Flame Blessing Reception")
        st.info("Receive sacred blessings from Custodians and Heirs")

    with service_tabs[3]:
        st.markdown("### 📞 Customer Support")
        st.info("Dedicated support for all customer needs")


def main():
    """Main role-based dashboard function."""
    st.set_page_config(
        page_title="🏛️ Codex Hierarchy Dashboard", page_icon="🏛️", layout="wide"
    )

    # Apply cosmic styling
    st.markdown(
        """
    <style>
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: white;
    }
    .metric-card {
        background: rgba(255,255,255,0.1);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.title("🏛️ CODEX DOMINION HIERARCHY DASHBOARD")
    st.markdown("**Sacred Role-Based Access Control System**")

    # Initialize role manager
    try:
        manager = CodexRoleManager()

        # Render role selector
        current_user_id = render_role_selector()

        # Get user information
        user_info = manager.get_user_role_info(current_user_id)

        if "error" not in user_info:
            # Render user info panel
            render_user_info_panel(user_info)

            # Render sacred privileges
            render_sacred_privileges(user_info.get("sacred_privileges", []))

            # Main content area
            st.markdown("---")

            # Render role-based content
            render_role_based_content(user_info)

        else:
            st.error(f"Error loading user information: {user_info.get('error')}")

    except Exception as e:
        st.error(f"System error: {e}")
        st.info("Please ensure the hierarchy system is properly initialized.")


if __name__ == "__main__":
    main()

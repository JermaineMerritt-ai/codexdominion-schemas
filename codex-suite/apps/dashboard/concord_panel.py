import json
from datetime import datetime
from pathlib import Path

import streamlit as st


# Load accounts from codex_hierarchy.json
def load_accounts():
    """Load accounts from the Codex Dominion hierarchy system"""
    hierarchy_file = Path("codex_hierarchy.json")

    if hierarchy_file.exists():
        with open(hierarchy_file, "r") as f:
            hierarchy_data = json.load(f)

        # Return in the expected format
        return {
            "custodians": hierarchy_data.get("custodians", []),
            "heirs": hierarchy_data.get("heirs", []),
            "customers": hierarchy_data.get("customers", []),
        }
    else:
        # Create default structure if file doesn't exist
        default_data = {
            "custodians": [
                {
                    "id": "CUST001",
                    "name": "Jermaine Merritt",
                    "role": "Custodian",
                    "status": "sovereign",
                    "flame_power_level": 10,
                    "authority_level": "MAXIMUM",
                }
            ],
            "heirs": [
                {
                    "id": "HEIR001",
                    "name": "First Heir",
                    "role": "Heir",
                    "status": "inducted",
                    "flame_power_level": 8,
                    "authority_level": "HIGH",
                }
            ],
            "customers": [
                {
                    "id": "CUSTM001",
                    "name": "Global Participant",
                    "role": "Customer",
                    "status": "welcomed",
                    "flame_power_level": 3,
                    "authority_level": "STANDARD",
                }
            ],
        }

        # Create the full hierarchy structure
        full_hierarchy = {
            "codex_hierarchy": {
                "timestamp": datetime.now().isoformat(),
                "system_version": "2.0.0",
                "hierarchy_status": "ACTIVE_AND_SOVEREIGN",
                "flame_blessing": "ETERNAL_PROTECTION_GRANTED",
            },
            "custodians": default_data["custodians"],
            "heirs": default_data["heirs"],
            "customers": default_data["customers"],
            "metadata": {
                "total_members": 3,
                "active_custodians": 1,
                "active_heirs": 1,
                "active_customers": 1,
                "hierarchy_health": "FULLY_OPERATIONAL",
            },
        }

        # Save the default hierarchy
        with open(hierarchy_file, "w") as f:
            json.dump(full_hierarchy, f, indent=2)

        return default_data


def save_accounts(accounts_data):
    """Save accounts back to the Codex Dominion hierarchy system"""
    hierarchy_file = Path("codex_hierarchy.json")

    # Load existing hierarchy data
    if hierarchy_file.exists():
        with open(hierarchy_file, "r") as f:
            hierarchy_data = json.load(f)
    else:
        hierarchy_data = {"codex_hierarchy": {}, "metadata": {}}

    # Update with new account data
    hierarchy_data["custodians"] = accounts_data["custodians"]
    hierarchy_data["heirs"] = accounts_data["heirs"]
    hierarchy_data["customers"] = accounts_data["customers"]

    # Update metadata
    hierarchy_data["metadata"] = {
        "total_members": len(accounts_data["custodians"])
        + len(accounts_data["heirs"])
        + len(accounts_data["customers"]),
        "active_custodians": len(accounts_data["custodians"]),
        "active_heirs": len(accounts_data["heirs"]),
        "active_customers": len(accounts_data["customers"]),
        "last_updated": datetime.now().isoformat(),
        "hierarchy_health": "FULLY_OPERATIONAL",
    }

    # Update system timestamp
    hierarchy_data["codex_hierarchy"]["timestamp"] = datetime.now().isoformat()

    # Save back to file
    with open(hierarchy_file, "w") as f:
        json.dump(hierarchy_data, f, indent=2)


def create_heir_profile(name: str, heir_count: int):
    """Create a complete heir profile with Codex Dominion standards"""
    return {
        "id": f"HEIR{heir_count+1:03d}",
        "name": name,
        "role": "Heir",
        "status": "inducted",
        "authority_level": "HIGH",
        "sacred_privileges": [
            "FLAME_INHERITOR",
            "COUNCIL_PARTICIPANT",
            "KNOWLEDGE_KEEPER",
            "SYSTEM_OPERATOR",
        ],
        "access_permissions": {
            "heir_avatar_dashboard": True,
            "learning_systems": True,
            "council_participation": True,
            "flame_communion": True,
            "knowledge_access": True,
            "limited_administration": True,
        },
        "inducted_date": datetime.now().isoformat(),
        "flame_power_level": 8,
        "digital_sovereignty_score": 85,
        "mentorship_status": "GUIDED_BY_CUSTODIAN",
    }


def create_customer_profile(name: str, customer_count: int):
    """Create a complete customer profile with Codex Dominion standards"""
    return {
        "id": f"CUSTM{customer_count+1:03d}",
        "name": name,
        "role": "Customer",
        "status": "welcomed",
        "authority_level": "STANDARD",
        "sacred_privileges": [
            "FLAME_OBSERVER",
            "KNOWLEDGE_SEEKER",
            "SERVICE_RECIPIENT",
        ],
        "access_permissions": {
            "public_dashboards": True,
            "service_interfaces": True,
            "knowledge_consumption": True,
            "flame_blessing_recipient": True,
            "customer_support": True,
            "limited_interaction": True,
        },
        "welcomed_date": datetime.now().isoformat(),
        "flame_power_level": 3,
        "digital_sovereignty_score": 25,
        "service_tier": "STANDARD",
    }


# Set up page config
st.set_page_config(
    page_title="🌟 Custodian–Heirs Concord Panel", page_icon="🏛️", layout="wide"
)

# Apply Codex styling
st.markdown(
    """
<style>
.main {
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    color: white;
}
.role-card {
    background: rgba(255,255,255,0.1);
    padding: 15px;
    border-radius: 10px;
    border-left: 4px solid;
    margin: 10px 0;
}
.custodian-card { border-left-color: #ff6b35; }
.heir-card { border-left-color: #4ecdc4; }
.customer-card { border-left-color: #45b7d1; }
</style>
""",
    unsafe_allow_html=True,
)

st.title("🌟 Custodian–Heirs Concord Panel")
st.markdown("**Sacred Hierarchy Management for the Codex Dominion**")

# Load accounts from Codex hierarchy
accounts = load_accounts()

# Display summary metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🔥 Custodians", len(accounts["custodians"]), "0")

with col2:
    st.metric("⚡ Heirs", len(accounts["heirs"]), "0")

with col3:
    st.metric("🌟 Customers", len(accounts["customers"]), "0")

with col4:
    total_members = (
        len(accounts["custodians"])
        + len(accounts["heirs"])
        + len(accounts["customers"])
    )
    st.metric("🏛️ Total Members", total_members, "0")

st.markdown("---")

# Tabs for Custodian, Heir, Customer
tab1, tab2, tab3 = st.tabs(["👑 Custodians", "⚡ Heirs", "🌟 Customers"])

with tab1:
    st.header("🔥 Custodians - Supreme Authority")

    if accounts["custodians"]:
        for c in accounts["custodians"]:
            st.markdown(
                f"""
            <div class="role-card custodian-card">
                <h3>🛡️ {c['name']}</h3>
                <p><strong>ID:</strong> {c.get('id', 'N/A')}</p>
                <p><strong>Status:</strong> {c['status'].title()}</p>
                <p><strong>Flame Level:</strong> {c.get('flame_power_level', 10)}/10</p>
                <p><strong>Authority:</strong> {c.get('authority_level', 'MAXIMUM')}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No custodians currently in the hierarchy.")

    st.subheader("🏛️ Custodian Management")
    st.info("Custodian elevation requires special sacred ceremony protocols.")

with tab2:
    st.header("⚡ Heirs - Flame Inheritors")

    if accounts["heirs"]:
        for h in accounts["heirs"]:
            st.markdown(
                f"""
            <div class="role-card heir-card">
                <h3>🌱 {h['name']}</h3>
                <p><strong>ID:</strong> {h.get('id', 'N/A')}</p>
                <p><strong>Status:</strong> {h['status'].title()}</p>
                <p><strong>Flame Level:</strong> {h.get('flame_power_level', 8)}/10</p>
                <p><strong>Authority:</strong> {h.get('authority_level', 'HIGH')}</p>
                <p><strong>Mentorship:</strong> {h.get('mentorship_status', 'GUIDED_BY_CUSTODIAN')}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No heirs currently in the hierarchy.")

    st.subheader("⚡ Heir Induction")

    col1, col2 = st.columns(2)

    with col1:
        new_heir = st.text_input("👤 New Heir Name", placeholder="Enter heir name...")

    with col2:
        if st.button("🔥 Induct Heir", type="primary"):
            if new_heir.strip():
                # Create complete heir profile
                heir_profile = create_heir_profile(new_heir, len(accounts["heirs"]))
                accounts["heirs"].append(heir_profile)
                save_accounts(accounts)

                st.success(
                    f"⚡ Heir {new_heir} successfully inducted into the sacred hierarchy!"
                )
                st.balloons()
                st.markdown(
                    f"""
                ### 🔥 Sacred Induction Complete
                
                **New Heir Profile:**
                - **Name:** {new_heir}
                - **ID:** {heir_profile['id']}
                - **Flame Level:** 8/10 (Sacred Flame Inheritor)
                - **Authority:** HIGH 
                - **Status:** Inducted and Blessed
                
                *By flame and silence, {new_heir} is now an eternal inheritor of Codex wisdom.*
                """
                )
                st.rerun()
            else:
                st.error("Please enter a valid heir name.")

with tab3:
    st.header("🌟 Customers - Global Participants")

    if accounts["customers"]:
        for cu in accounts["customers"]:
            st.markdown(
                f"""
            <div class="role-card customer-card">
                <h3>🌍 {cu['name']}</h3>
                <p><strong>ID:</strong> {cu.get('id', 'N/A')}</p>
                <p><strong>Status:</strong> {cu['status'].title()}</p>
                <p><strong>Flame Level:</strong> {cu.get('flame_power_level', 3)}/10</p>
                <p><strong>Authority:</strong> {cu.get('authority_level', 'STANDARD')}</p>
                <p><strong>Service Tier:</strong> {cu.get('service_tier', 'STANDARD')}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No customers currently in the hierarchy.")

    st.subheader("🌟 Customer Welcome")

    col1, col2 = st.columns(2)

    with col1:
        new_customer = st.text_input(
            "👤 New Customer Name", placeholder="Enter customer name..."
        )

    with col2:
        if st.button("🌍 Welcome Customer", type="primary"):
            if new_customer.strip():
                # Create complete customer profile
                customer_profile = create_customer_profile(
                    new_customer, len(accounts["customers"])
                )
                accounts["customers"].append(customer_profile)
                save_accounts(accounts)

                st.success(
                    f"🌟 Customer {new_customer} warmly welcomed to the Codex Dominion!"
                )
                st.balloons()
                st.markdown(
                    f"""
                ### 🌟 Sacred Welcome Complete
                
                **New Customer Profile:**
                - **Name:** {new_customer}
                - **ID:** {customer_profile['id']}
                - **Flame Level:** 3/10 (Blessed Flame Receiver)
                - **Authority:** STANDARD
                - **Status:** Welcomed and Embraced
                
                *By flame and silence, {new_customer} is now part of our global community.*
                """
                )
                st.rerun()
            else:
                st.error("Please enter a valid customer name.")

# Sidebar with hierarchy information
with st.sidebar:
    st.header("🏛️ Hierarchy Overview")

    st.subheader("🔥 System Status")
    st.success("✅ Hierarchy Active")
    st.success("✅ Flame Eternal")
    st.success("✅ All Roles Blessed")

    st.subheader("⚡ Quick Stats")
    total = (
        len(accounts["custodians"])
        + len(accounts["heirs"])
        + len(accounts["customers"])
    )

    if total > 0:
        custodian_pct = (len(accounts["custodians"]) / total) * 100
        heir_pct = (len(accounts["heirs"]) / total) * 100
        customer_pct = (len(accounts["customers"]) / total) * 100

        st.metric("Custodians", f"{custodian_pct:.1f}%")
        st.metric("Heirs", f"{heir_pct:.1f}%")
        st.metric("Customers", f"{customer_pct:.1f}%")

    st.subheader("🎯 Sacred Actions")

    if st.button("💾 Save Hierarchy"):
        save_accounts(accounts)
        st.success("Hierarchy saved!")

    if st.button("🔄 Refresh Data"):
        st.rerun()

    st.markdown("---")
    st.markdown("**🔥 By Flame and Silence**")
    st.markdown("*Wisdom Eternal*")

# Footer
st.markdown("---")
st.markdown(
    "**🌟 Custodian–Heirs Concord Panel** - *Sacred Hierarchy Management for Digital Sovereignty*"
)

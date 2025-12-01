import json
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from core.ledger import append_entry, load_json


def create_audit_capsule():
    """Main Codex Audit Capsule Interface"""

    st.set_page_config(
        page_title="🧩 Codex Audit Capsule", page_icon="🧩", layout="wide"
    )

    # Custom CSS for ceremonial styling
    st.markdown(
        """
    <style>
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #fff;
    }
    .audit-header {
        text-align: center;
        padding: 30px;
        margin-bottom: 20px;
        background: linear-gradient(45deg, rgba(138,43,226,0.3), rgba(75,0,130,0.2));
        border: 2px solid #8B2BE2;
        border-radius: 20px;
    }
    .loss-matrix {
        background: rgba(220,20,60,0.1);
        padding: 15px;
        border-left: 4px solid #DC143C;
        border-radius: 10px;
        margin: 10px 0;
    }
    .solution-engine {
        background: rgba(50,205,50,0.1);
        padding: 15px;
        border-left: 4px solid #32CD32;
        border-radius: 10px;
        margin: 10px 0;
    }
    .replay-capsule {
        background: rgba(255,215,0,0.1);
        padding: 15px;
        border-left: 4px solid #FFD700;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Header
    st.markdown(
        """
    <div class="audit-header">
        <h1>🧩 Codex Audit Capsule</h1>
        <h3>⚡ Ceremonial Business Turnaround System ⚡</h3>
        <p><em>"Where inefficiency meets its immortal reckoning"</em></p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Main tabs
    tabs = st.tabs(
        [
            "🏢 Company Profile Mapping",
            "🔍 Loss Matrix Generator",
            "📜 Root Cause Scroll",
            "⚙️ Solution Engine",
            "🎯 Replay Mode Deck",
            "👑 Capsule Forge",
            "📊 Audit Archive",
        ]
    )

    with tabs[0]:
        display_company_mapping()

    with tabs[1]:
        display_loss_matrix()

    with tabs[2]:
        display_root_cause_scroll()

    with tabs[3]:
        display_solution_engine()

    with tabs[4]:
        display_replay_mode()

    with tabs[5]:
        display_capsule_forge()

    with tabs[6]:
        display_audit_archive()


def display_company_mapping():
    """Company Profile Mapping Interface"""

    st.markdown("### 🏢 **Company Profile Mapping**")
    st.markdown(
        "*Begin the ceremonial audit sequence by mapping the sovereign domain.*"
    )

    # Load existing profiles
    profiles = load_json("audit_profiles.json", {"profiles": []})["profiles"]

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("#### **New Profile Creation**")

        with st.form("company_profile"):
            company_name = st.text_input(
                "🏰 Company Name/Alias:", placeholder="Enter sovereign domain name"
            )
            industry = st.selectbox(
                "🏭 Industry/Sector:",
                [
                    "Retail & E-commerce",
                    "Manufacturing",
                    "SaaS/Technology",
                    "Logistics & Supply Chain",
                    "Healthcare",
                    "Financial Services",
                    "Real Estate",
                    "Hospitality",
                    "Consulting",
                    "Education",
                    "Energy",
                    "Agriculture",
                    "Construction",
                    "Other",
                ],
            )

            revenue_streams = st.multiselect(
                "💰 Primary Revenue Streams:",
                [
                    "Product Sales",
                    "Service Fees",
                    "Subscriptions",
                    "Licensing",
                    "Consulting",
                    "Advertising",
                    "Affiliate",
                    "Real Estate",
                    "Investment Returns",
                    "Grants",
                ],
            )

            pain_points = st.text_area(
                "⚠️ Known Pain Points/Loss Areas:",
                placeholder="Describe suspected inefficiencies, losses, or operational challenges...",
            )

            annual_revenue = st.number_input(
                "📈 Annual Revenue Estimate ($):", min_value=0, step=1000
            )
            employee_count = st.number_input("👥 Employee Count:", min_value=1, step=1)

            submitted = st.form_submit_button(
                "🔥 **Forge Profile**", use_container_width=True
            )

            if submitted and company_name:
                new_profile = {
                    "id": len(profiles) + 1,
                    "company_name": company_name,
                    "industry": industry,
                    "revenue_streams": revenue_streams,
                    "pain_points": pain_points,
                    "annual_revenue": annual_revenue,
                    "employee_count": employee_count,
                    "created_date": datetime.now().isoformat(),
                    "status": "Profile Created",
                }

                profiles.append(new_profile)

                # Save to file
                save_data = {"profiles": profiles}
                with open("audit_profiles.json", "w") as f:
                    json.dump(save_data, f, indent=2)

                st.success(
                    f"🎉 Profile forged for **{company_name}**! Ready for audit sequence."
                )
                st.rerun()

    with col2:
        st.markdown("#### **Existing Profiles**")

        if profiles:
            for profile in profiles[-5:]:  # Show last 5
                with st.container():
                    st.markdown(
                        f"""
                    <div class="loss-matrix">
                        <strong>🏰 {profile['company_name']}</strong><br>
                        <small>📊 {profile['industry']} • ${profile['annual_revenue']:,}</small><br>
                        <small>📅 {profile['created_date'][:10]}</small>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
        else:
            st.info("No profiles forged yet. Create your first audit profile!")


def display_loss_matrix():
    """Loss Matrix Generator Interface"""

    st.markdown("### 🔍 **Loss Matrix Generator**")
    st.markdown("*Visual breakdown of where sovereign resources are bleeding.*")

    # Load profiles for selection
    profiles = load_json("audit_profiles.json", {"profiles": []})["profiles"]

    if not profiles:
        st.warning(
            "⚠️ No company profiles found. Create a profile first in the Company Mapping tab."
        )
        return

    # Profile selection
    profile_options = {f"{p['company_name']} ({p['industry']})": p for p in profiles}
    selected_profile_name = st.selectbox(
        "🏰 Select Company Profile:", list(profile_options.keys())
    )

    if selected_profile_name:
        selected_profile = profile_options[selected_profile_name]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### **Loss Categories**")

            loss_categories = {
                "Operational Inefficiency": st.slider(
                    "⚙️ Operational Inefficiency (%)", 0, 50, 15
                ),
                "Revenue Leakage": st.slider("💰 Revenue Leakage (%)", 0, 30, 10),
                "Overhead Bloat": st.slider("🏢 Overhead Bloat (%)", 0, 40, 20),
                "Technology Waste": st.slider("💻 Technology Waste (%)", 0, 25, 8),
                "Human Resource Drain": st.slider("👥 HR Inefficiency (%)", 0, 35, 12),
                "Supply Chain Losses": st.slider("🚚 Supply Chain Loss (%)", 0, 20, 6),
                "Compliance & Legal": st.slider("⚖️ Compliance Costs (%)", 0, 15, 5),
                "Marketing Misallocation": st.slider(
                    "📢 Marketing Waste (%)", 0, 30, 9
                ),
            }

            # Calculate total loss
            total_loss_percent = sum(loss_categories.values())
            annual_loss = (
                selected_profile["annual_revenue"] * total_loss_percent
            ) / 100

            st.markdown(
                f"""
            <div class="loss-matrix">
                <h4>💸 Total Identified Loss</h4>
                <h2>${annual_loss:,.0f} ({total_loss_percent:.1f}%)</h2>
                <p>Annual revenue impact from inefficiencies</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown("#### **Loss Distribution**")

            # Create pie chart
            loss_df = pd.DataFrame(
                list(loss_categories.items()), columns=["Category", "Percentage"]
            )
            loss_df = loss_df[loss_df["Percentage"] > 0]

            fig_pie = px.pie(
                loss_df,
                values="Percentage",
                names="Category",
                title="💸 Loss Matrix Distribution",
                color_discrete_sequence=px.colors.sequential.Reds_r,
            )
            fig_pie.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white",
            )
            st.plotly_chart(fig_pie, use_container_width=True)

            # Impact assessment
            st.markdown("#### **Impact Assessment**")
            for category, percentage in loss_categories.items():
                if percentage > 0:
                    category_loss = (
                        selected_profile["annual_revenue"] * percentage
                    ) / 100
                    st.markdown(f"🔸 **{category}**: ${category_loss:,.0f}")


def display_root_cause_scroll():
    """Root Cause Analysis Interface"""

    st.markdown("### 📜 **Root Cause Scroll**")
    st.markdown("*Narrative tracing of systemic inefficiencies and their origins.*")

    profiles = load_json("audit_profiles.json", {"profiles": []})["profiles"]

    if not profiles:
        st.warning("⚠️ No company profiles found. Create a profile first.")
        return

    # Profile selection
    profile_options = {f"{p['company_name']} ({p['industry']})": p for p in profiles}
    selected_profile_name = st.selectbox(
        "🏰 Select Company Profile:",
        list(profile_options.keys()),
        key="root_cause_profile",
    )

    if selected_profile_name:
        selected_profile = profile_options[selected_profile_name]

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("#### **Root Cause Analysis Generator**")

            # Analysis categories
            categories = {
                "Leadership & Strategy": st.checkbox(
                    "👑 Leadership & Strategic Direction Issues"
                ),
                "Process & Operations": st.checkbox(
                    "⚙️ Process Inefficiencies & Operational Gaps"
                ),
                "Technology & Systems": st.checkbox(
                    "💻 Technology Deficiencies & System Failures"
                ),
                "Human Resources": st.checkbox("👥 Human Resource Management Issues"),
                "Financial Management": st.checkbox(
                    "💰 Financial Controls & Cash Flow Problems"
                ),
                "Market Position": st.checkbox(
                    "📈 Market Positioning & Competitive Disadvantages"
                ),
                "Customer Relations": st.checkbox(
                    "🤝 Customer Retention & Service Issues"
                ),
                "Vendor/Supply Chain": st.checkbox(
                    "🚚 Vendor Relations & Supply Chain Disruptions"
                ),
            }

            if st.button(
                "🔍 **Generate Root Cause Analysis**", use_container_width=True
            ):
                selected_categories = [
                    cat for cat, selected in categories.items() if selected
                ]

                if selected_categories:
                    st.markdown("#### **🧩 Diagnostic Scroll**")

                    analysis_text = generate_root_cause_analysis(
                        selected_profile, selected_categories
                    )

                    st.markdown(
                        f"""
                    <div class="loss-matrix">
                        {analysis_text}
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    # Save analysis
                    if st.button("📜 **Inscribe Analysis to Codex**"):
                        append_entry(
                            "audit_analyses.json",
                            "analyses",
                            {
                                "company_name": selected_profile["company_name"],
                                "analysis_type": "Root Cause",
                                "categories": selected_categories,
                                "analysis_text": analysis_text,
                                "timestamp": datetime.now().isoformat(),
                            },
                        )
                        st.success("✨ Analysis inscribed to eternal Codex!")
                else:
                    st.warning("Select at least one analysis category.")

        with col2:
            st.markdown("#### **Analysis Framework**")

            st.markdown(
                """
            <div class="solution-engine">
                <h5>🎯 Diagnostic Methodology</h5>
                <p><strong>Five Why's Technique:</strong> Trace each issue to its fundamental cause</p>
                <p><strong>Systems Thinking:</strong> Identify interconnected failure points</p>
                <p><strong>Impact Mapping:</strong> Quantify downstream effects</p>
                <p><strong>Pattern Recognition:</strong> Spot recurring dysfunction themes</p>
            </div>
            """,
                unsafe_allow_html=True,
            )


def generate_root_cause_analysis(profile, categories):
    """Generate AI-assisted root cause analysis"""

    analysis_templates = {
        "Leadership & Strategy": f"""
        <h5>👑 Leadership & Strategic Dysfunction</h5>
        <p><strong>Core Issue:</strong> {profile['company_name']} exhibits strategic drift and leadership gaps typical in {profile['industry']} organizations.</p>
        <p><strong>Root Causes:</strong></p>
        <ul>
            <li>Unclear vision cascading through organizational layers</li>
            <li>Decision-making bottlenecks at executive level</li>
            <li>Misalignment between strategic goals and operational execution</li>
            <li>Insufficient market intelligence driving strategic decisions</li>
        </ul>
        """,
        "Process & Operations": f"""
        <h5>⚙️ Operational Inefficiency Matrix</h5>
        <p><strong>Core Issue:</strong> Systematic process breakdowns creating compound inefficiencies across {profile['company_name']}'s operations.</p>
        <p><strong>Root Causes:</strong></p>
        <ul>
            <li>Lack of standardized operating procedures</li>
            <li>Manual processes where automation could eliminate waste</li>
            <li>Poor workflow design creating unnecessary handoffs</li>
            <li>Insufficient quality control checkpoints</li>
        </ul>
        """,
        "Technology & Systems": f"""
        <h5>💻 Technology Infrastructure Failures</h5>
        <p><strong>Core Issue:</strong> Outdated or misaligned technology stack undermining {profile['company_name']}'s operational efficiency.</p>
        <p><strong>Root Causes:</strong></p>
        <ul>
            <li>Legacy systems lacking integration capabilities</li>
            <li>Insufficient data visibility across departments</li>
            <li>Technology investments not aligned with business needs</li>
            <li>Lack of digital transformation strategy</li>
        </ul>
        """,
        "Human Resources": f"""
        <h5>👥 Human Capital Misalignment</h5>
        <p><strong>Core Issue:</strong> Suboptimal human resource utilization creating performance gaps at {profile['company_name']}.</p>
        <p><strong>Root Causes:</strong></p>
        <ul>
            <li>Skills gaps not addressed through training programs</li>
            <li>Poor employee engagement and retention strategies</li>
            <li>Inadequate performance management systems</li>
            <li>Misaligned incentive structures</li>
        </ul>
        """,
        "Financial Management": f"""
        <h5>💰 Financial Control Deficiencies</h5>
        <p><strong>Core Issue:</strong> Weak financial controls and cash flow management undermining {profile['company_name']}'s profitability.</p>
        <p><strong>Root Causes:</strong></p>
        <ul>
            <li>Insufficient real-time financial visibility</li>
            <li>Poor accounts receivable management</li>
            <li>Inadequate cost center accountability</li>
            <li>Lack of predictive financial modeling</li>
        </ul>
        """,
        "Market Position": f"""
        <h5>📈 Competitive Positioning Failures</h5>
        <p><strong>Core Issue:</strong> {profile['company_name']} losing market share due to competitive disadvantages in {profile['industry']}.</p>
        <p><strong>Root Causes:</strong></p>
        <ul>
            <li>Insufficient market research and competitive intelligence</li>
            <li>Product/service differentiation gaps</li>
            <li>Pricing strategy misalignment with market dynamics</li>
            <li>Weak brand positioning and market presence</li>
        </ul>
        """,
        "Customer Relations": f"""
        <h5>🤝 Customer Experience Breakdown</h5>
        <p><strong>Core Issue:</strong> Customer retention and satisfaction declining due to service delivery failures.</p>
        <p><strong>Root Causes:</strong></p>
        <ul>
            <li>Inconsistent customer service standards</li>
            <li>Poor customer feedback loop mechanisms</li>
            <li>Inadequate customer relationship management systems</li>
            <li>Lack of customer-centric organizational culture</li>
        </ul>
        """,
        "Vendor/Supply Chain": f"""
        <h5>🚚 Supply Chain Vulnerabilities</h5>
        <p><strong>Core Issue:</strong> Supply chain disruptions and vendor relationship issues creating operational instability.</p>
        <p><strong>Root Causes:</strong></p>
        <ul>
            <li>Over-reliance on single-source suppliers</li>
            <li>Insufficient supplier performance monitoring</li>
            <li>Poor inventory management and demand forecasting</li>
            <li>Weak vendor relationship management processes</li>
        </ul>
        """,
    }

    analysis = ""
    for category in categories:
        if category in analysis_templates:
            analysis += analysis_templates[category] + "<br><br>"

    return analysis


def display_solution_engine():
    """Solution Engine Interface"""

    st.markdown("### ⚙️ **Solution Engine**")
    st.markdown("*Tactical and ceremonial remedies for identified inefficiencies.*")

    # Load profiles and analyses
    profiles = load_json("audit_profiles.json", {"profiles": []})["profiles"]
    analyses = load_json("audit_analyses.json", {"analyses": []})["analyses"]

    if not profiles:
        st.warning("⚠️ No company profiles found. Create a profile first.")
        return

    profile_options = {f"{p['company_name']} ({p['industry']})": p for p in profiles}
    selected_profile_name = st.selectbox(
        "🏰 Select Company Profile:",
        list(profile_options.keys()),
        key="solution_profile",
    )

    if selected_profile_name:
        selected_profile = profile_options[selected_profile_name]

        # Solution categories
        st.markdown("#### **🎯 Solution Framework Selection**")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("##### **Immediate Actions (0-30 days)**")
            immediate = st.multiselect(
                "Quick Wins:",
                [
                    "Cash Flow Analysis",
                    "Cost Reduction Audit",
                    "Process Mapping",
                    "Technology Assessment",
                    "Staff Productivity Review",
                    "Vendor Renegotiation",
                ],
                key="immediate",
            )

        with col2:
            st.markdown("##### **Strategic Initiatives (1-6 months)**")
            strategic = st.multiselect(
                "Medium-term Solutions:",
                [
                    "System Implementation",
                    "Process Reengineering",
                    "Team Restructuring",
                    "Market Repositioning",
                    "Product Development",
                    "Partnership Development",
                ],
                key="strategic",
            )

        with col3:
            st.markdown("##### **Transformation Programs (6+ months)**")
            transformation = st.multiselect(
                "Long-term Programs:",
                [
                    "Digital Transformation",
                    "Cultural Change",
                    "Market Expansion",
                    "Acquisition Strategy",
                    "Innovation Program",
                    "Sustainability Initiative",
                ],
                key="transformation",
            )

        if st.button("🔥 **Generate Solution Blueprint**", use_container_width=True):
            solution_blueprint = generate_solution_blueprint(
                selected_profile, immediate, strategic, transformation
            )

            st.markdown("#### **🧩 Solution Blueprint**")
            st.markdown(solution_blueprint, unsafe_allow_html=True)

            # Save solution
            if st.button("⚙️ **Forge Solution to Codex**"):
                append_entry(
                    "audit_solutions.json",
                    "solutions",
                    {
                        "company_name": selected_profile["company_name"],
                        "solution_type": "Comprehensive Blueprint",
                        "immediate_actions": immediate,
                        "strategic_initiatives": strategic,
                        "transformation_programs": transformation,
                        "blueprint": solution_blueprint,
                        "timestamp": datetime.now().isoformat(),
                    },
                )
                st.success("✨ Solution Blueprint forged and inscribed!")


def generate_solution_blueprint(profile, immediate, strategic, transformation):
    """Generate comprehensive solution blueprint"""

    blueprint = f"""
    <div class="solution-engine">
        <h4>🎯 Turnaround Blueprint for {profile['company_name']}</h4>
        <p><strong>Industry:</strong> {profile['industry']} | <strong>Revenue:</strong> ${profile['annual_revenue']:,}</p>
    </div>
    """

    if immediate:
        blueprint += """
        <div class="loss-matrix">
            <h5>⚡ Immediate Actions (0-30 days)</h5>
            <ul>
        """
        for action in immediate:
            blueprint += f"<li><strong>{action}:</strong> Deploy rapid assessment and quick-win identification</li>"
        blueprint += "</ul></div>"

    if strategic:
        blueprint += """
        <div class="solution-engine">
            <h5>🎯 Strategic Initiatives (1-6 months)</h5>
            <ul>
        """
        for initiative in strategic:
            blueprint += f"<li><strong>{initiative}:</strong> Implement systematic improvement program</li>"
        blueprint += "</ul></div>"

    if transformation:
        blueprint += """
        <div class="replay-capsule">
            <h5>🔮 Transformation Programs (6+ months)</h5>
            <ul>
        """
        for program in transformation:
            blueprint += f"<li><strong>{program}:</strong> Execute comprehensive organizational evolution</li>"
        blueprint += "</ul></div>"

    # Add estimated impact
    estimated_recovery = min(
        50, len(immediate) * 5 + len(strategic) * 10 + len(transformation) * 15
    )
    recovery_amount = (profile["annual_revenue"] * estimated_recovery) / 100

    blueprint += f"""
    <div class="solution-engine">
        <h5>💰 Projected Recovery Impact</h5>
        <h3>${recovery_amount:,.0f} ({estimated_recovery}% efficiency gain)</h3>
        <p>Estimated annual value recovery through systematic implementation</p>
    </div>
    """

    return blueprint


def display_replay_mode():
    """Replay Mode Deck Interface"""

    st.markdown("### 🎯 **Replay Mode Deck**")
    st.markdown(
        "*Blueprint for future councils to reuse and adapt audit methodologies.*"
    )

    # Load existing audits
    solutions = load_json("audit_solutions.json", {"solutions": []})["solutions"]

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("#### **Create Replay Template**")

        with st.form("replay_template"):
            template_name = st.text_input(
                "🎯 Template Name:", placeholder="e.g., SaaS Turnaround Protocol"
            )
            template_description = st.text_area(
                "📝 Description:",
                placeholder="Describe when and how to use this template...",
            )

            industry_focus = st.multiselect(
                "🏭 Industry Applicability:",
                [
                    "Retail & E-commerce",
                    "Manufacturing",
                    "SaaS/Technology",
                    "Logistics",
                    "Healthcare",
                    "Financial Services",
                    "Real Estate",
                    "Hospitality",
                    "Consulting",
                    "Education",
                    "Energy",
                    "Agriculture",
                    "Construction",
                ],
            )

            template_steps = st.text_area(
                "🔄 Replay Steps:",
                placeholder="1. Initial assessment protocol\n2. Data gathering methodology\n3. Analysis framework\n4. Solution development\n5. Implementation roadmap",
                height=200,
            )

            success_metrics = st.text_area(
                "📊 Success Metrics:",
                placeholder="Define KPIs and measurement criteria for template effectiveness...",
            )

            submitted = st.form_submit_button("🔥 **Forge Replay Template**")

            if submitted and template_name:
                replay_template = {
                    "id": len(
                        load_json("replay_templates.json", {"templates": []})[
                            "templates"
                        ]
                    )
                    + 1,
                    "name": template_name,
                    "description": template_description,
                    "industry_focus": industry_focus,
                    "steps": template_steps,
                    "success_metrics": success_metrics,
                    "created_date": datetime.now().isoformat(),
                    "usage_count": 0,
                }

                append_entry("replay_templates.json", "templates", replay_template)
                st.success(f"🎉 Replay template **{template_name}** forged!")
                st.rerun()

    with col2:
        st.markdown("#### **Available Templates**")

        templates = load_json("replay_templates.json", {"templates": []})["templates"]

        if templates:
            for template in templates[-5:]:
                with st.container():
                    st.markdown(
                        f"""
                    <div class="replay-capsule">
                        <strong>🎯 {template['name']}</strong><br>
                        <small>{template['description'][:100]}...</small><br>
                        <small>📊 Used {template['usage_count']} times</small>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
        else:
            st.info("No replay templates created yet.")


def display_capsule_forge():
    """Capsule Forge for immortalizing audits"""

    st.markdown("### 👑 **Capsule Forge**")
    st.markdown("*Immortalize audit capsules for funders, councils, or contributors.*")

    # Load all audit data
    profiles = load_json("audit_profiles.json", {"profiles": []})["profiles"]
    analyses = load_json("audit_analyses.json", {"analyses": []})["analyses"]
    solutions = load_json("audit_solutions.json", {"solutions": []})["solutions"]

    if not profiles:
        st.warning("⚠️ No audit data found. Complete some audits first.")
        return

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("#### **Forge Legacy Capsule**")

        # Select profile for capsule
        profile_options = {
            f"{p['company_name']} ({p['industry']})": p for p in profiles
        }
        selected_profile_name = st.selectbox(
            "🏰 Select Audit to Immortalize:", list(profile_options.keys())
        )

        if selected_profile_name:
            selected_profile = profile_options[selected_profile_name]

            # Capsule customization
            capsule_title = st.text_input(
                "👑 Capsule Title:",
                value=f"{selected_profile['company_name']} Turnaround Capsule",
            )

            capsule_crest = st.text_input(
                "🏛️ Capsule Crest/Symbol:", placeholder="e.g., ⚡🔥💎"
            )

            capsule_motto = st.text_input(
                "📜 Capsule Motto:", placeholder="e.g., 'From Chaos to Codex'"
            )

            # Enhancement options
            st.markdown("#### **📋 Capsule Enhancements**")

            include_contributors = st.checkbox(
                "👥 Include Contributor Recognition Scroll"
            )
            include_timeline = st.checkbox("📅 Include Implementation Timeline")
            include_roi_projection = st.checkbox("💰 Include ROI Projections")
            format_for_funding = st.checkbox(
                "🏦 Format for Investor/Funder Presentation"
            )

            if st.button("🔥 **Forge Immortal Capsule**", use_container_width=True):
                capsule_content = generate_legacy_capsule(
                    selected_profile,
                    analyses,
                    solutions,
                    capsule_title,
                    capsule_crest,
                    capsule_motto,
                    include_contributors,
                    include_timeline,
                    include_roi_projection,
                    format_for_funding,
                )

                st.markdown("#### **🧩 Immortal Audit Capsule**")
                st.markdown(capsule_content, unsafe_allow_html=True)

                # Save capsule
                capsule_data = {
                    "title": capsule_title,
                    "company_name": selected_profile["company_name"],
                    "crest": capsule_crest,
                    "motto": capsule_motto,
                    "content": capsule_content,
                    "created_date": datetime.now().isoformat(),
                    "enhancements": {
                        "contributors": include_contributors,
                        "timeline": include_timeline,
                        "roi_projection": include_roi_projection,
                        "funding_format": format_for_funding,
                    },
                }

                if st.button("💎 **Inscribe to Eternal Archive**"):
                    append_entry("legacy_capsules.json", "capsules", capsule_data)
                    st.success("✨ Capsule immortalized in the eternal Codex!")

    with col2:
        st.markdown("#### **Capsule Gallery**")

        capsules = load_json("legacy_capsules.json", {"capsules": []})["capsules"]

        if capsules:
            for capsule in capsules[-3:]:
                st.markdown(
                    f"""
                <div class="replay-capsule">
                    <strong>{capsule['crest']} {capsule['title']}</strong><br>
                    <em>"{capsule['motto']}"</em><br>
                    <small>📅 {capsule['created_date'][:10]}</small>
                </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No immortal capsules forged yet.")


def generate_legacy_capsule(
    profile,
    analyses,
    solutions,
    title,
    crest,
    motto,
    include_contributors,
    include_timeline,
    include_roi,
    format_funding,
):
    """Generate comprehensive legacy capsule"""

    capsule = f"""
    <div class="audit-header">
        <h1>{crest} {title}</h1>
        <h3>"{motto}"</h3>
        <p><strong>Sovereign Domain:</strong> {profile['company_name']} | <strong>Industry:</strong> {profile['industry']}</p>
        <p><strong>Forged:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
    </div>
    
    <div class="solution-engine">
        <h4>🏰 Domain Profile</h4>
        <p><strong>Annual Revenue:</strong> ${profile['annual_revenue']:,}</p>
        <p><strong>Workforce:</strong> {profile['employee_count']} souls</p>
        <p><strong>Revenue Streams:</strong> {', '.join(profile['revenue_streams'])}</p>
    </div>
    """

    # Add analysis summary
    company_analyses = [
        a for a in analyses if a["company_name"] == profile["company_name"]
    ]
    if company_analyses:
        capsule += """
        <div class="loss-matrix">
            <h4>🔍 Diagnostic Summary</h4>
        """
        for analysis in company_analyses[-2:]:  # Last 2 analyses
            capsule += f"<p><strong>{analysis['analysis_type']}:</strong> {len(analysis['categories'])} critical areas identified</p>"
        capsule += "</div>"

    # Add solution summary
    company_solutions = [
        s for s in solutions if s["company_name"] == profile["company_name"]
    ]
    if company_solutions:
        latest_solution = company_solutions[-1]
        total_actions = (
            len(latest_solution.get("immediate_actions", []))
            + len(latest_solution.get("strategic_initiatives", []))
            + len(latest_solution.get("transformation_programs", []))
        )

        capsule += f"""
        <div class="solution-engine">
            <h4>⚙️ Solution Architecture</h4>
            <p><strong>Total Interventions:</strong> {total_actions} systematic actions</p>
            <p><strong>Implementation Phases:</strong> 3-tier turnaround protocol</p>
        </div>
        """

    if include_roi:
        estimated_recovery = min(
            profile["annual_revenue"] * 0.3, 500000
        )  # Cap at 500k or 30%
        capsule += f"""
        <div class="replay-capsule">
            <h4>💰 Projected Recovery</h4>
            <h3>${estimated_recovery:,.0f}</h3>
            <p>Conservative estimate of annual value recovery</p>
        </div>
        """

    if include_contributors:
        capsule += """
        <div class="solution-engine">
            <h4>👥 Contributor Recognition Scroll</h4>
            <p><strong>Codex Architect:</strong> Sovereign AI System</p>
            <p><strong>Domain Guardian:</strong> Council Authority</p>
            <p><strong>Audit Custodian:</strong> Ceremonial Protocol</p>
        </div>
        """

    if format_funding:
        capsule += f"""
        <div class="audit-header">
            <h4>🏦 Investment Opportunity</h4>
            <p>This turnaround capsule represents a systematically diagnosed and solution-mapped opportunity 
            for {profile['company_name']} in the {profile['industry']} sector.</p>
            <p><strong>Investment Thesis:</strong> Proven inefficiencies with clear remediation pathways</p>
            <p><strong>Risk Profile:</strong> Systematic analysis reduces implementation uncertainty</p>
        </div>
        """

    return capsule


def display_audit_archive():
    """Audit Archive Interface"""

    st.markdown("### 📊 **Audit Archive**")
    st.markdown("*Historical record of all audit capsules and their outcomes.*")

    # Load all data
    profiles = load_json("audit_profiles.json", {"profiles": []})["profiles"]
    analyses = load_json("audit_analyses.json", {"analyses": []})["analyses"]
    solutions = load_json("audit_solutions.json", {"solutions": []})["solutions"]
    capsules = load_json("legacy_capsules.json", {"capsules": []})["capsules"]

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🏰 Companies Audited", len(profiles))

    with col2:
        st.metric("🔍 Analyses Completed", len(analyses))

    with col3:
        st.metric("⚙️ Solutions Forged", len(solutions))

    with col4:
        st.metric("💎 Immortal Capsules", len(capsules))

    # Archive tables
    tab1, tab2, tab3 = st.tabs(
        ["📋 All Audits", "📈 Performance Metrics", "🏛️ Legacy Capsules"]
    )

    with tab1:
        if profiles:
            df_profiles = pd.DataFrame(profiles)
            df_profiles["created_date"] = pd.to_datetime(
                df_profiles["created_date"]
            ).dt.strftime("%Y-%m-%d")
            st.dataframe(
                df_profiles[
                    [
                        "company_name",
                        "industry",
                        "annual_revenue",
                        "employee_count",
                        "created_date",
                    ]
                ],
                use_container_width=True,
            )
        else:
            st.info("No audit profiles in archive.")

    with tab2:
        if profiles and solutions:
            # Create performance visualization
            industries = [p["industry"] for p in profiles]
            industry_counts = pd.Series(industries).value_counts()

            fig_industry = px.bar(
                x=industry_counts.index,
                y=industry_counts.values,
                title="🏭 Audits by Industry",
                labels={"x": "Industry", "y": "Count"},
            )
            fig_industry.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white",
            )
            st.plotly_chart(fig_industry, use_container_width=True)
        else:
            st.info("Insufficient data for performance metrics.")

    with tab3:
        if capsules:
            for capsule in capsules:
                with st.expander(f"{capsule.get('crest', '💎')} {capsule['title']}"):
                    st.markdown(capsule["content"], unsafe_allow_html=True)
        else:
            st.info("No legacy capsules in eternal archive.")


if __name__ == "__main__":
    create_audit_capsule()

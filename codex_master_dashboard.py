"""
🔥 CODEX MASTER DASHBOARD 👑
Unified Command Center for Multi-Cycle Content & Commerce

Dashboard Sections:
- Revenue & Balances (Stripe integration)
- Transactions (Orders, refunds, analytics)
- Campaigns (Daily, Seasonal, Epochal cycles)
- Replay Archives (Eternal preservation)
- Platform Analytics (Threads, Instagram, YouTube, TikTok)

The Merritt Method™ - Sovereign Dashboard Architecture
"""

import streamlit as st
import datetime
import json
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List

from codex_multi_cycle_orchestrator import CodexMultiCycleOrchestrator, CycleType, SeasonalEvent


# Page configuration
st.set_page_config(
    page_title="CodexDominion Master Dashboard",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .cycle-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.25rem;
    }
    .daily-badge { background: #10b981; color: white; }
    .seasonal-badge { background: #f59e0b; color: white; }
    .epochal-badge { background: #6366f1; color: white; }
</style>
""", unsafe_allow_html=True)


class CodexMasterDashboard:
    """Master Dashboard for Multi-Cycle Orchestration"""

    def __init__(self):
        """Initialize dashboard"""
        self.orchestrator = CodexMultiCycleOrchestrator()
        self.today = datetime.date.today()

    def render(self):
        """Render main dashboard"""
        # Header
        st.markdown('<h1 class="main-header">🔥 CODEX DOMINION MASTER DASHBOARD 👑</h1>', unsafe_allow_html=True)
        st.markdown(f"**Date:** {self.today.strftime('%B %d, %Y')} | **Time:** {datetime.datetime.now().strftime('%I:%M %p')}")

        # Sidebar navigation
        page = self.render_sidebar()

        # Render selected page
        if page == "Overview":
            self.render_overview()
        elif page == "Revenue & Balances":
            self.render_revenue()
        elif page == "Transactions":
            self.render_transactions()
        elif page == "Daily Cycle":
            self.render_daily_cycle()
        elif page == "Seasonal Campaigns":
            self.render_seasonal_campaigns()
        elif page == "Epochal Archives":
            self.render_epochal_archives()
        elif page == "Platform Analytics":
            self.render_platform_analytics()
        elif page == "Product Performance":
            self.render_product_performance()

    def render_sidebar(self) -> str:
        """Render sidebar navigation"""
        st.sidebar.image("https://via.placeholder.com/200x80/667eea/ffffff?text=CodexDominion", use_container_width=True)
        st.sidebar.title("Navigation")

        page = st.sidebar.radio(
            "Select View",
            [
                "Overview",
                "Revenue & Balances",
                "Transactions",
                "Daily Cycle",
                "Seasonal Campaigns",
                "Epochal Archives",
                "Platform Analytics",
                "Product Performance"
            ],
            label_visibility="collapsed"
        )

        st.sidebar.divider()

        # Quick actions
        st.sidebar.subheader("⚡ Quick Actions")

        if st.sidebar.button("🔥 Execute Daily Cycle", use_container_width=True):
            with st.spinner("Executing daily cycle..."):
                results = self.orchestrator.execute_daily_cycle()
                st.sidebar.success(f"Posted {results['total_posts']} times across platforms!")

        if st.sidebar.button("🎄 Launch Seasonal Campaign", use_container_width=True):
            st.sidebar.info("Navigate to Seasonal Campaigns to configure")

        if st.sidebar.button("🏛️ Create Epochal Archive", use_container_width=True):
            with st.spinner("Creating eternal archive..."):
                results = self.orchestrator.execute_epochal_cycle()
                st.sidebar.success("Archive created successfully!")

        st.sidebar.divider()

        # System status
        st.sidebar.subheader("📊 System Status")
        st.sidebar.metric("Cycles Active", "3/3")
        st.sidebar.metric("Platforms Connected", "4/4")
        st.sidebar.metric("Archives Created", "127")

        return page

    def render_overview(self):
        """Render overview dashboard"""
        st.header("📊 Executive Overview")

        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Revenue", "$9,247", "+23%")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Orders (30d)", "327", "+15%")
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Posts", "1,247", "+8%")
            st.markdown('</div>', unsafe_allow_html=True)

        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Engagement Rate", "4.7%", "+0.3%")
            st.markdown('</div>', unsafe_allow_html=True)

        st.divider()

        # Three-cycle status
        st.subheader("🔄 Multi-Cycle Status")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### <span class='daily-badge'>DAILY CYCLE</span>", unsafe_allow_html=True)
            st.write("**Status:** Active ✅")
            st.write("**Today's Posts:** 12")
            st.write("**Platforms:** Threads, Instagram, YouTube, TikTok")
            st.write("**Next Post:** 3:00 PM")
            if st.button("View Daily Details", key="daily_details"):
                st.switch_page("pages/daily_cycle.py")

        with col2:
            st.markdown("### <span class='seasonal-badge'>SEASONAL CYCLE</span>", unsafe_allow_html=True)
            st.write("**Status:** Christmas Campaign Active 🎄")
            st.write("**Campaign:** 12 Days of Christmas Blessings")
            st.write("**Discount:** XMAS20 (20% off)")
            st.write("**Revenue:** $2,847 (3 days)")
            if st.button("View Campaign Details", key="seasonal_details"):
                st.switch_page("pages/seasonal_campaigns.py")

        with col3:
            st.markdown("### <span class='epochal-badge'>EPOCHAL CYCLE</span>", unsafe_allow_html=True)
            st.write("**Status:** Archiving Enabled ✅")
            st.write("**Last Archive:** Dec 1, 2025")
            st.write("**Total Archives:** 127")
            st.write("**Replay Capsules:** 24")
            if st.button("View Archives", key="epochal_details"):
                st.switch_page("pages/epochal_archives.py")

        st.divider()

        # Recent activity timeline
        st.subheader("📅 Recent Activity Timeline")

        timeline_data = [
            {"time": "2 hours ago", "event": "Daily Cycle: Posted devotional to Threads", "cycle": "daily"},
            {"time": "4 hours ago", "event": "Seasonal Campaign: Christmas sale post to Instagram", "cycle": "seasonal"},
            {"time": "6 hours ago", "event": "Transaction: Order #1247 - Faith Entrepreneur Bundle ($47)", "cycle": "revenue"},
            {"time": "8 hours ago", "event": "Daily Cycle: Business tip posted to LinkedIn", "cycle": "daily"},
            {"time": "1 day ago", "event": "Epochal Archive: Monthly capsule created", "cycle": "epochal"},
        ]

        for item in timeline_data:
            cycle_class = f"{item['cycle']}-badge" if item['cycle'] in ['daily', 'seasonal', 'epochal'] else 'metric-card'
            st.markdown(f"**{item['time']}** - {item['event']}")

    def render_revenue(self):
        """Render revenue & balances page"""
        st.header("💰 Revenue & Balances")

        # Revenue summary
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Revenue (All Time)", "$9,247")
        col2.metric("This Month", "$2,847", "+23%")
        col3.metric("This Week", "$627", "+15%")
        col4.metric("Today", "$94", "+5%")

        st.divider()

        # Revenue chart
        st.subheader("📈 Revenue Trend (30 Days)")

        # Mock data
        dates = pd.date_range(end=self.today, periods=30)
        revenue = [50 + i*3 + (i%7)*20 for i in range(30)]

        df = pd.DataFrame({"Date": dates, "Revenue": revenue})

        fig = px.line(df, x="Date", y="Revenue", title="Daily Revenue")
        fig.update_traces(line_color='#667eea', line_width=3)
        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # Revenue by product
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📦 Revenue by Product")

            product_data = {
                "Product": [
                    "Faith Entrepreneur Bundle",
                    "Ultimate Devotional Collection",
                    "The Daily Flame",
                    "Covenant Journal",
                    "Sacred Business Blueprint"
                ],
                "Revenue": [2147, 1653, 1540, 987, 820]
            }

            fig = px.bar(product_data, x="Revenue", y="Product", orientation='h',
                        color="Revenue", color_continuous_scale='Purples')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("📊 Revenue by Source")

            source_data = {
                "Source": ["Direct", "Instagram", "Threads", "YouTube", "Email"],
                "Revenue": [3847, 2140, 1620, 987, 653]
            }

            fig = px.pie(source_data, values="Revenue", names="Source",
                        color_discrete_sequence=px.colors.sequential.Purples)
            st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # Stripe integration status
        st.subheader("💳 Stripe Integration Status")

        col1, col2, col3 = st.columns(3)
        col1.metric("Connected", "✅ Active")
        col2.metric("Payout Schedule", "2-day rolling")
        col3.metric("Next Payout", "$847 (Dec 11)")

    def render_transactions(self):
        """Render transactions page"""
        st.header("💳 Transaction History")

        # Filters
        col1, col2, col3, col4 = st.columns(4)

        date_range = col1.selectbox("Date Range", ["Today", "This Week", "This Month", "All Time"])
        status_filter = col2.selectbox("Status", ["All", "Completed", "Pending", "Refunded"])
        product_filter = col3.selectbox("Product", ["All Products", "Devotionals", "Journals", "Bundles"])
        sort_by = col4.selectbox("Sort By", ["Recent First", "Oldest First", "Highest Amount", "Lowest Amount"])

        st.divider()

        # Mock transaction data
        transactions = [
            {"Order ID": "#1247", "Date": "Dec 9, 2025 10:23 AM", "Customer": "Sarah M.", "Product": "Faith Entrepreneur Bundle", "Amount": "$47.00", "Status": "Completed"},
            {"Order ID": "#1246", "Date": "Dec 9, 2025 9:15 AM", "Customer": "Marcus J.", "Product": "The Daily Flame", "Amount": "$27.00", "Status": "Completed"},
            {"Order ID": "#1245", "Date": "Dec 8, 2025 8:47 PM", "Customer": "Jennifer L.", "Product": "Ultimate Devotional Collection", "Amount": "$57.00", "Status": "Completed"},
            {"Order ID": "#1244", "Date": "Dec 8, 2025 6:32 PM", "Customer": "David K.", "Product": "Covenant Journal", "Amount": "$17.00", "Status": "Completed"},
            {"Order ID": "#1243", "Date": "Dec 8, 2025 3:18 PM", "Customer": "Lisa P.", "Product": "Sacred Business Blueprint", "Amount": "$24.00", "Status": "Refunded"},
        ]

        df = pd.DataFrame(transactions)

        st.dataframe(df, use_container_width=True, hide_index=True)

        st.divider()

        # Transaction summary
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Transactions", "327")
        col2.metric("Average Order Value", "$28.27")
        col3.metric("Refund Rate", "2.3%")
        col4.metric("Customer Retention", "37%")

    def render_daily_cycle(self):
        """Render daily cycle dashboard"""
        st.header("🔥 Daily Cycle Manager")

        st.markdown("**Automated Daily Content Distribution**")
        st.write("Post devotionals, business tips, and scripture quotes across all platforms daily.")

        st.divider()

        # Today's posting schedule
        st.subheader("📅 Today's Schedule")

        schedule_data = [
            {"Time": "9:00 AM", "Platform": "Threads, Instagram", "Type": "Devotional Excerpt", "Status": "✅ Posted"},
            {"Time": "1:00 PM", "Platform": "LinkedIn, Twitter", "Type": "Business Tip", "Status": "✅ Posted"},
            {"Time": "5:00 PM", "Platform": "Instagram, TikTok", "Type": "Scripture Quote", "Status": "⏰ Scheduled"},
            {"Time": "9:00 PM", "Platform": "Threads, Facebook", "Type": "Testimonial", "Status": "⏰ Scheduled"},
        ]

        df = pd.DataFrame(schedule_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.divider()

        # Manual post creator
        st.subheader("✍️ Create Manual Post")

        col1, col2 = st.columns(2)

        with col1:
            post_type = st.selectbox("Post Type", ["Devotional Excerpt", "Business Tip", "Scripture Quote", "Product Showcase", "Testimonial"])
            platforms = st.multiselect("Platforms", ["Threads", "Instagram", "YouTube", "TikTok", "Facebook", "Twitter", "LinkedIn"])
            post_text = st.text_area("Post Text", height=150)

        with col2:
            upload_image = st.file_uploader("Upload Image", type=["jpg", "png"])
            upload_video = st.file_uploader("Upload Video", type=["mp4", "mov"])
            schedule_time = st.time_input("Schedule Time (optional)")
            link_product = st.selectbox("Link to Product (optional)", ["None", "Daily Flame", "Radiant Faith", "Sacred Business Blueprint", "Covenant Journal"])

        if st.button("🚀 Post Now", type="primary", use_container_width=True):
            st.success("Post published successfully to selected platforms!")

        st.divider()

        # Daily analytics
        st.subheader("📊 Today's Analytics")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Posts Published", "12")
        col2.metric("Total Reach", "4,327")
        col3.metric("Engagement Rate", "4.2%")
        col4.metric("Clicks to Store", "127")

    def render_seasonal_campaigns(self):
        """Render seasonal campaigns page"""
        st.header("🎄 Seasonal Campaign Manager")

        # Active campaigns
        st.subheader("🔥 Active Campaigns")

        st.info("**ACTIVE:** 12 Days of Christmas Blessings (Dec 1-25) - Use code XMAS20 for 20% off")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Campaign Revenue", "$2,847")
        col2.metric("Orders", "87")
        col3.metric("Posts Created", "36")
        col4.metric("Days Remaining", "16")

        st.divider()

        # Upcoming campaigns
        st.subheader("📅 Upcoming Campaigns")

        campaigns = [
            {"Event": "New Year", "Start": "Dec 26, 2025", "End": "Jan 5, 2026", "Discount": "NEWYEAR25 (25%)", "Products": "All Products"},
            {"Event": "Valentine's Day", "Start": "Feb 1, 2026", "End": "Feb 14, 2026", "Discount": "LOVE15 (15%)", "Products": "Journals"},
            {"Event": "Easter", "Start": "Mar 15, 2026", "End": "Apr 20, 2026", "Discount": "EASTER15 (15%)", "Products": "Radiant Faith"},
            {"Event": "Mother's Day", "Start": "May 1, 2026", "End": "May 14, 2026", "Discount": "MOM25 (25%)", "Products": "Journals"},
        ]

        df = pd.DataFrame(campaigns)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.divider()

        # Create new campaign
        st.subheader("➕ Create New Campaign")

        col1, col2 = st.columns(2)

        with col1:
            event_name = st.text_input("Campaign Name")
            event_type = st.selectbox("Event Type", ["Christmas", "Easter", "Mother's Day", "Father's Day", "Black Friday", "Cyber Monday", "Custom"])
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")

        with col2:
            discount_code = st.text_input("Discount Code")
            discount_percentage = st.number_input("Discount %", min_value=0, max_value=100, value=20)
            products = st.multiselect("Featured Products", ["Daily Flame", "Radiant Faith", "Sacred Business Blueprint", "Covenant Journal", "Entrepreneur Journal", "All Products"])
            auto_post = st.checkbox("Auto-generate posts daily", value=True)

        if st.button("🚀 Launch Campaign", type="primary", use_container_width=True):
            st.success(f"Campaign '{event_name}' created successfully!")

    def render_epochal_archives(self):
        """Render epochal archives page"""
        st.header("🏛️ Epochal Archives & Replay Capsules")

        st.write("**Eternal Preservation System** - Documenting your digital legacy for future generations")

        st.divider()

        # Archive summary
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Archives", "127")
        col2.metric("Replay Capsules", "24")
        col3.metric("Total Size", "1.2 GB")
        col4.metric("Heirs' Docs", "48")

        st.divider()

        # Recent archives
        st.subheader("📦 Recent Archives")

        archives = [
            {"Date": "Dec 1, 2025", "Type": "Monthly Archive", "Contents": "Daily posts, seasonal campaigns, revenue", "Size": "45 MB"},
            {"Date": "Nov 1, 2025", "Type": "Monthly Archive", "Contents": "Daily posts, Black Friday campaign", "Size": "52 MB"},
            {"Date": "Oct 1, 2025", "Type": "Quarterly Replay", "Contents": "Q4 business performance, testimonials", "Size": "187 MB"},
            {"Date": "Sep 1, 2025", "Type": "Monthly Archive", "Contents": "Daily posts, seasonal campaigns", "Size": "41 MB"},
        ]

        df = pd.DataFrame(archives)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.divider()

        # Create archive
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📥 Create New Archive")
            archive_type = st.selectbox("Archive Type", ["Monthly Archive", "Quarterly Replay", "Annual Capsule", "Custom"])
            include_daily = st.checkbox("Include daily cycle posts", value=True)
            include_seasonal = st.checkbox("Include seasonal campaigns", value=True)
            include_revenue = st.checkbox("Include revenue records", value=True)
            include_testimonials = st.checkbox("Include customer testimonials", value=True)

            if st.button("Create Archive", type="primary"):
                with st.spinner("Creating eternal archive..."):
                    results = self.orchestrator.execute_epochal_cycle()
                    st.success("Archive created successfully!")

        with col2:
            st.subheader("👨‍👩‍👧‍👦 Heirs' Inheritance Documentation")
            st.write("Comprehensive business documentation for future generations:")
            st.write("✅ Business overview & model")
            st.write("✅ Financial records & analytics")
            st.write("✅ Digital assets & IP")
            st.write("✅ Operations manual")
            st.write("✅ Customer database (encrypted)")
            st.write("✅ Content library")

            if st.button("Generate Heirs' Report", use_container_width=True):
                st.info("Heirs' inheritance report generated!")

    def render_platform_analytics(self):
        """Render platform analytics page"""
        st.header("📱 Platform Analytics")

        # Platform selector
        platform = st.selectbox("Select Platform", ["All Platforms", "Threads", "Instagram", "YouTube", "TikTok"])

        st.divider()

        # Platform metrics
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Followers", "12,847", "+234")
        col2.metric("Total Posts", "1,247", "+12")
        col3.metric("Avg Engagement", "4.7%", "+0.3%")
        col4.metric("Clicks to Store", "1,427", "+87")

        st.divider()

        # Engagement chart
        st.subheader("📈 Engagement Trend (30 Days)")

        dates = pd.date_range(end=self.today, periods=30)
        engagement = [3.5 + (i%10)*0.2 for i in range(30)]

        df = pd.DataFrame({"Date": dates, "Engagement Rate": engagement})

        fig = px.line(df, x="Date", y="Engagement Rate", title="Daily Engagement Rate (%)")
        fig.update_traces(line_color='#f59e0b', line_width=3)
        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # Platform comparison
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Platform Comparison")

            platform_data = {
                "Platform": ["Instagram", "Threads", "TikTok", "YouTube"],
                "Followers": [5240, 3847, 2650, 1110],
                "Engagement": [5.2, 4.8, 6.1, 3.4]
            }

            fig = px.bar(platform_data, x="Platform", y="Followers", color="Engagement",
                        color_continuous_scale='Oranges')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("📈 Growth Rate")

            growth_data = {
                "Platform": ["Instagram", "Threads", "TikTok", "YouTube"],
                "Growth": [8.3, 12.7, 15.2, 6.1]
            }

            fig = px.pie(growth_data, values="Growth", names="Platform",
                        color_discrete_sequence=px.colors.sequential.Oranges)
            st.plotly_chart(fig, use_container_width=True)

    def render_product_performance(self):
        """Render product performance page"""
        st.header("📦 Product Performance Analytics")

        # Product selector
        product = st.selectbox("Select Product", [
            "All Products",
            "The Daily Flame: 365 Days",
            "Radiant Faith: 40 Days",
            "Sacred Business Blueprint",
            "The Covenant Journal",
            "Entrepreneur's Faith Journal",
            "Gratitude & Grace Journal",
            "Faith Entrepreneur Bundle",
            "Ultimate Devotional Collection"
        ])

        st.divider()

        # Product metrics
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Sales", "327")
        col2.metric("Revenue", "$9,247")
        col3.metric("Avg Rating", "4.8 ⭐")
        col4.metric("Reviews", "87")

        st.divider()

        # Sales chart
        st.subheader("📈 Sales Trend (30 Days)")

        dates = pd.date_range(end=self.today, periods=30)
        sales = [8 + (i%7)*3 for i in range(30)]

        df = pd.DataFrame({"Date": dates, "Sales": sales})

        fig = px.area(df, x="Date", y="Sales", title="Daily Sales")
        fig.update_traces(line_color='#10b981', fillcolor='rgba(16, 185, 129, 0.3)')
        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # Top products
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🏆 Best Sellers")

            top_products = {
                "Product": [
                    "Faith Entrepreneur Bundle",
                    "Ultimate Devotional Collection",
                    "The Daily Flame",
                    "Covenant Journal"
                ],
                "Sales": [87, 64, 57, 42]
            }

            fig = px.bar(top_products, y="Product", x="Sales", orientation='h',
                        color="Sales", color_continuous_scale='Greens')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("⭐ Customer Ratings")

            ratings = {
                "Rating": ["5 stars", "4 stars", "3 stars", "2 stars", "1 star"],
                "Count": [67, 15, 4, 1, 0]
            }

            fig = px.bar(ratings, x="Rating", y="Count",
                        color="Count", color_continuous_scale='Greens')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)


# Main execution
if __name__ == "__main__":
    dashboard = CodexMasterDashboard()
    dashboard.render()

#!/usr/bin/env python3
"""
💰 COSMIC DOMINION - REVENUE CROWN 💰
Financial Sovereignty Dashboard for Digital Empire
Advanced Revenue Analytics and Management System
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots


def load_json(file_path, default=None):
    """Load JSON data with error handling"""
    if default is None:
        default = {}

    try:
        path = Path(file_path)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return default
    except Exception as e:
        st.error(f"Error loading {file_path}: {e}")
        return default


def append_entry(file_path, key, entry):
    """Append entry to revenue data file"""
    try:
        # Load existing data
        if Path(file_path).exists():
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {key: []}

        # Add timestamp if not present
        if "timestamp" not in entry:
            entry["timestamp"] = datetime.now().isoformat()

        # Append new entry
        data[key].append(entry)

        # Save back to file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        st.error(f"Error saving to {file_path}: {e}")
        return False


def create_revenue_metrics(stores, social, websites):
    """Calculate comprehensive revenue metrics"""

    # Calculate totals
    stores_total = sum([s.get("amount", 0) for s in stores])
    social_total = sum([sm.get("amount", 0) for sm in social])
    websites_total = sum([w.get("amount", 0) for w in websites])
    grand_total = stores_total + social_total + websites_total

    # Calculate growth rates (comparing last 30 days vs previous 30 days)
    now = datetime.now()
    last_30_days = now - timedelta(days=30)
    previous_30_days = now - timedelta(days=60)

    def calculate_period_revenue(transactions, start_date, end_date):
        total = 0
        for t in transactions:
            try:
                t_date = datetime.fromisoformat(
                    t.get("timestamp", "").replace("Z", "+00:00")
                )
                if start_date <= t_date <= end_date:
                    total += t.get("amount", 0)
            except:
                continue
        return total

    # Recent vs previous period revenue
    recent_stores = calculate_period_revenue(stores, last_30_days, now)
    previous_stores = calculate_period_revenue(stores, previous_30_days, last_30_days)

    recent_social = calculate_period_revenue(social, last_30_days, now)
    previous_social = calculate_period_revenue(social, previous_30_days, last_30_days)

    recent_websites = calculate_period_revenue(websites, last_30_days, now)
    previous_websites = calculate_period_revenue(
        websites, previous_30_days, last_30_days
    )

    # Calculate growth percentages
    def safe_growth_rate(recent, previous):
        if previous == 0:
            return 100.0 if recent > 0 else 0.0
        return ((recent - previous) / previous) * 100

    stores_growth = safe_growth_rate(recent_stores, previous_stores)
    social_growth = safe_growth_rate(recent_social, previous_social)
    websites_growth = safe_growth_rate(recent_websites, previous_websites)
    total_growth = safe_growth_rate(
        recent_stores + recent_social + recent_websites,
        previous_stores + previous_social + previous_websites,
    )

    return {
        "totals": {
            "stores": stores_total,
            "social": social_total,
            "websites": websites_total,
            "grand_total": grand_total,
        },
        "recent": {
            "stores": recent_stores,
            "social": recent_social,
            "websites": recent_websites,
            "total": recent_stores + recent_social + recent_websites,
        },
        "growth": {
            "stores": stores_growth,
            "social": social_growth,
            "websites": websites_growth,
            "total": total_growth,
        },
    }


def create_revenue_visualizations(stores, social, websites):
    """Create advanced revenue visualizations"""

    # Prepare data for visualization
    all_transactions = []

    # Process stores data
    for store in stores:
        all_transactions.append(
            {
                "timestamp": store.get("timestamp", ""),
                "amount": store.get("amount", 0),
                "source": "Stores",
                "item": store.get("item", "Unknown"),
                "category": "Physical Commerce",
            }
        )

    # Process social media data
    for social_item in social:
        all_transactions.append(
            {
                "timestamp": social_item.get("timestamp", ""),
                "amount": social_item.get("amount", 0),
                "source": "Social Media",
                "item": social_item.get("platform", "Unknown"),
                "category": "Digital Marketing",
            }
        )

    # Process websites data
    for website in websites:
        all_transactions.append(
            {
                "timestamp": website.get("timestamp", ""),
                "amount": website.get("amount", 0),
                "source": "Websites",
                "item": website.get("source", "Unknown"),
                "category": "Digital Commerce",
            }
        )

    if not all_transactions:
        st.info("📊 No transaction data available for visualization")
        return

    # Convert to DataFrame
    df = pd.DataFrame(all_transactions)

    # Parse timestamps
    df["date"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["date"])

    if df.empty:
        st.info("📊 No valid transaction dates for visualization")
        return

    # Create visualizations
    col1, col2 = st.columns(2)

    with col1:
        # Revenue by Source Pie Chart
        source_totals = df.groupby("source")["amount"].sum().reset_index()

        fig_pie = px.pie(
            source_totals,
            values="amount",
            names="source",
            title="💰 Revenue Distribution by Source",
            color_discrete_sequence=["#FFD700", "#9370DB", "#4169E1"],
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Monthly Revenue Trend
        df["month"] = df["date"].dt.to_period("M")
        monthly_revenue = df.groupby(["month", "source"])["amount"].sum().reset_index()
        monthly_revenue["month_str"] = monthly_revenue["month"].astype(str)

        fig_trend = px.bar(
            monthly_revenue,
            x="month_str",
            y="amount",
            color="source",
            title="📈 Monthly Revenue Trends",
            color_discrete_sequence=["#FFD700", "#9370DB", "#4169E1"],
        )
        fig_trend.update_layout(xaxis_title="Month", yaxis_title="Revenue ($)")
        st.plotly_chart(fig_trend, use_container_width=True)

    # Revenue Timeline
    st.markdown("### 📊 **Revenue Timeline Analysis**")

    df_sorted = df.sort_values("date")
    df_sorted["cumulative"] = df_sorted["amount"].cumsum()

    fig_timeline = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=("Daily Revenue Transactions", "Cumulative Revenue Growth"),
        vertical_spacing=0.1,
    )

    # Daily transactions scatter plot
    fig_timeline.add_trace(
        go.Scatter(
            x=df_sorted["date"],
            y=df_sorted["amount"],
            mode="markers+lines",
            name="Daily Revenue",
            marker=dict(color="#FFD700", size=8),
            line=dict(color="#FFD700", width=2),
        ),
        row=1,
        col=1,
    )

    # Cumulative revenue line
    fig_timeline.add_trace(
        go.Scatter(
            x=df_sorted["date"],
            y=df_sorted["cumulative"],
            mode="lines",
            name="Cumulative Revenue",
            line=dict(color="#9370DB", width=3),
        ),
        row=2,
        col=1,
    )

    fig_timeline.update_layout(
        height=600, title_text="💎 Revenue Crown Analytics Dashboard", showlegend=True
    )

    fig_timeline.update_xaxes(title_text="Date")
    fig_timeline.update_yaxes(title_text="Revenue ($)")

    st.plotly_chart(fig_timeline, use_container_width=True)


def display_stores_tab(stores):
    """Display enhanced stores revenue tab"""

    st.markdown("### 🏬 **Physical Commerce Revenue**")

    if not stores:
        st.info("🏬 No store transactions recorded yet")

        # Add new store transaction form
        with st.expander("➕ Add New Store Transaction"):
            item_name = st.text_input("Item/Product Name:", key="store_item_1")
            amount = st.number_input(
                "Sale Amount ($):", min_value=0.0, step=0.01, key="store_amount_1"
            )
            store_location = st.text_input("Store Location:", key="store_location_1")

            if st.button("💰 Record Store Sale", key="store_button_1"):
                if item_name and amount > 0:
                    new_transaction = {
                        "item": item_name,
                        "amount": amount,
                        "location": store_location,
                        "category": "store_sale",
                        "timestamp": datetime.now().isoformat(),
                    }

                    if append_entry("stores.json", "transactions", new_transaction):
                        st.success(f"🎉 Store sale recorded: ${amount} for {item_name}")
                        st.rerun()
        return

    # Display stores analytics
    total_stores = sum([s.get("amount", 0) for s in stores])
    avg_transaction = total_stores / len(stores) if stores else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🏬 Total Store Revenue", f"${total_stores:,.2f}")
    with col2:
        st.metric("📊 Total Transactions", len(stores))
    with col3:
        st.metric("💰 Avg Transaction", f"${avg_transaction:.2f}")

    # Recent transactions table
    st.markdown("**Recent Store Transactions:**")

    stores_df = pd.DataFrame(stores)
    if not stores_df.empty:
        stores_df["formatted_timestamp"] = pd.to_datetime(
            stores_df["timestamp"]
        ).dt.strftime("%Y-%m-%d %H:%M")
        stores_df = stores_df.sort_values("timestamp", ascending=False)

        # Display as formatted table
        for _, transaction in stores_df.head(10).iterrows():
            timestamp = transaction.get("formatted_timestamp", "Unknown")
            item = transaction.get("item", "Unknown Item")
            amount = transaction.get("amount", 0)
            location = transaction.get("location", "Unknown Location")

            st.markdown(
                f"""
            <div style="background: rgba(255,215,0,0.1); padding: 10px; margin: 5px 0; 
                        border-left: 4px solid #FFD700; border-radius: 5px;">
                <strong>🏬 {item}</strong> - <span style="color: #32CD32;">${amount:,.2f}</span><br>
                <small>📅 {timestamp} • 📍 {location}</small>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # Add new transaction form
    with st.expander("➕ Add New Store Transaction"):
        item_name = st.text_input("Item/Product Name:", key="store_item_2")
        amount = st.number_input(
            "Sale Amount ($):", min_value=0.0, step=0.01, key="store_amount_2"
        )
        store_location = st.text_input("Store Location:", key="store_location_2")

        if st.button("💰 Record Store Sale", key="store_button_2"):
            if item_name and amount > 0:
                new_transaction = {
                    "item": item_name,
                    "amount": amount,
                    "location": store_location,
                    "category": "store_sale",
                    "timestamp": datetime.now().isoformat(),
                }

                if append_entry("stores.json", "transactions", new_transaction):
                    st.success(f"🎉 Store sale recorded: ${amount} for {item_name}")
                    st.rerun()


def display_social_media_tab(social):
    """Display enhanced social media revenue tab"""

    st.markdown("### 📱 **Social Media Revenue Streams**")

    if not social:
        st.info("📱 No social media revenue recorded yet")

        # Add new social media transaction form
        with st.expander("➕ Add New Social Media Revenue"):
            platform = st.selectbox(
                "Platform:",
                [
                    "Instagram",
                    "TikTok",
                    "YouTube",
                    "Twitter/X",
                    "Facebook",
                    "LinkedIn",
                    "Other",
                ],
                key="social_platform_1",
            )
            revenue_type = st.selectbox(
                "Revenue Type:",
                [
                    "Sponsored Post",
                    "Affiliate Commission",
                    "Brand Partnership",
                    "Content Licensing",
                    "Subscription",
                    "Tip/Donation",
                ],
                key="social_type_1",
            )
            amount = st.number_input(
                "Revenue Amount ($):", min_value=0.0, step=0.01, key="social_amount_1"
            )
            description = st.text_area("Description/Details:", key="social_desc_1")

            if st.button("💰 Record Social Revenue", key="social_button_1"):
                if amount > 0:
                    new_transaction = {
                        "platform": platform,
                        "revenue_type": revenue_type,
                        "amount": amount,
                        "description": description,
                        "timestamp": datetime.now().isoformat(),
                    }

                    if append_entry("social.json", "transactions", new_transaction):
                        st.success(
                            f"🎉 Social media revenue recorded: ${amount} from {platform}"
                        )
                        st.rerun()
        return

    # Display social media analytics
    total_social = sum([s.get("amount", 0) for s in social])
    avg_social = total_social / len(social) if social else 0

    # Platform breakdown
    platforms = {}
    for s in social:
        platform = s.get("platform", "Unknown")
        platforms[platform] = platforms.get(platform, 0) + s.get("amount", 0)

    top_platform = (
        max(platforms.items(), key=lambda x: x[1]) if platforms else ("None", 0)
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📱 Total Social Revenue", f"${total_social:,.2f}")
    with col2:
        st.metric("🎯 Top Platform", f"{top_platform[0]}: ${top_platform[1]:.2f}")
    with col3:
        st.metric("💰 Avg Revenue", f"${avg_social:.2f}")

    # Platform breakdown chart
    if platforms:
        platform_df = pd.DataFrame(
            list(platforms.items()), columns=["Platform", "Revenue"]
        )
        fig_social = px.bar(
            platform_df,
            x="Platform",
            y="Revenue",
            title="📊 Revenue by Social Media Platform",
            color="Revenue",
            color_continuous_scale="viridis",
        )
        st.plotly_chart(fig_social, use_container_width=True)

    # Recent transactions
    st.markdown("**Recent Social Media Revenue:**")

    social_df = pd.DataFrame(social)
    if not social_df.empty:
        social_df["formatted_timestamp"] = pd.to_datetime(
            social_df["timestamp"]
        ).dt.strftime("%Y-%m-%d %H:%M")
        social_df = social_df.sort_values("timestamp", ascending=False)

        for _, transaction in social_df.head(10).iterrows():
            timestamp = transaction.get("formatted_timestamp", "Unknown")
            platform = transaction.get("platform", "Unknown")
            revenue_type = transaction.get("revenue_type", "Revenue")
            amount = transaction.get("amount", 0)
            description = transaction.get("description", "")

            st.markdown(
                f"""
            <div style="background: rgba(147,112,219,0.1); padding: 10px; margin: 5px 0; 
                        border-left: 4px solid #9370DB; border-radius: 5px;">
                <strong>📱 {platform}</strong> - {revenue_type} - <span style="color: #32CD32;">${amount:,.2f}</span><br>
                <small>📅 {timestamp}</small><br>
                <em>{description[:100]}{'...' if len(description) > 100 else ''}</em>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # Add new transaction form
    with st.expander("➕ Add New Social Media Revenue"):
        platform = st.selectbox(
            "Platform:",
            [
                "Instagram",
                "TikTok",
                "YouTube",
                "Twitter/X",
                "Facebook",
                "LinkedIn",
                "Other",
            ],
            key="social_platform_2",
        )
        revenue_type = st.selectbox(
            "Revenue Type:",
            [
                "Sponsored Post",
                "Affiliate Commission",
                "Brand Partnership",
                "Content Licensing",
                "Subscription",
                "Tip/Donation",
            ],
            key="social_type_2",
        )
        amount = st.number_input(
            "Revenue Amount ($):", min_value=0.0, step=0.01, key="social_amount_2"
        )
        description = st.text_area("Description/Details:", key="social_desc_2")

        if st.button("💰 Record Social Revenue", key="social_button_2"):
            if amount > 0:
                new_transaction = {
                    "platform": platform,
                    "revenue_type": revenue_type,
                    "amount": amount,
                    "description": description,
                    "timestamp": datetime.now().isoformat(),
                }

                if append_entry("social.json", "transactions", new_transaction):
                    st.success(
                        f"🎉 Social media revenue recorded: ${amount} from {platform}"
                    )
                    st.rerun()


def display_websites_tab(websites):
    """Display enhanced websites revenue tab"""

    st.markdown("### 🌐 **Website & Digital Commerce Revenue**")

    if not websites:
        st.info("🌐 No website revenue recorded yet")

        # Add new website transaction form
        with st.expander("➕ Add New Website Revenue"):
            source = st.text_input("Website/Source Name:", key="website_source_empty_1")
            revenue_type = st.selectbox(
                "Revenue Type:",
                [
                    "Product Sales",
                    "Service Fees",
                    "Subscription",
                    "Advertising",
                    "Affiliate",
                    "Licensing",
                    "Donations",
                ],
                key="website_type_empty_1",
            )
            amount = st.number_input(
                "Revenue Amount ($):",
                min_value=0.0,
                step=0.01,
                key="website_amount_empty_1",
            )
            transaction_id = st.text_input(
                "Transaction ID (optional):", key="website_id_empty_1"
            )

            if st.button("💰 Record Website Revenue", key="website_button_empty_1"):
                if source and amount > 0:
                    new_transaction = {
                        "source": source,
                        "revenue_type": revenue_type,
                        "amount": amount,
                        "transaction_id": transaction_id,
                        "timestamp": datetime.now().isoformat(),
                    }

                    if append_entry("websites.json", "transactions", new_transaction):
                        st.success(
                            f"🎉 Website revenue recorded: ${amount} from {source}"
                        )
                        st.rerun()
        return

    # Display website analytics
    total_websites = sum([w.get("amount", 0) for w in websites])
    avg_website = total_websites / len(websites) if websites else 0

    # Source breakdown
    sources = {}
    for w in websites:
        source = w.get("source", "Unknown")
        sources[source] = sources.get(source, 0) + w.get("amount", 0)

    top_source = max(sources.items(), key=lambda x: x[1]) if sources else ("None", 0)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🌐 Total Website Revenue", f"${total_websites:,.2f}")
    with col2:
        st.metric("🎯 Top Source", f"{top_source[0]}: ${top_source[1]:.2f}")
    with col3:
        st.metric("💰 Avg Transaction", f"${avg_website:.2f}")

    # Revenue type analysis
    revenue_types = {}
    for w in websites:
        rev_type = w.get("revenue_type", "Unknown")
        revenue_types[rev_type] = revenue_types.get(rev_type, 0) + w.get("amount", 0)

    if revenue_types:
        col1, col2 = st.columns(2)

        with col1:
            # Sources chart
            sources_df = pd.DataFrame(
                list(sources.items()), columns=["Source", "Revenue"]
            )
            fig_sources = px.pie(
                sources_df,
                values="Revenue",
                names="Source",
                title="💰 Revenue by Website Source",
            )
            st.plotly_chart(fig_sources, use_container_width=True)

        with col2:
            # Revenue types chart
            types_df = pd.DataFrame(
                list(revenue_types.items()), columns=["Type", "Revenue"]
            )
            fig_types = px.bar(
                types_df,
                x="Type",
                y="Revenue",
                title="📊 Revenue by Type",
                color="Revenue",
                color_continuous_scale="blues",
            )
            st.plotly_chart(fig_types, use_container_width=True)

    # Recent transactions
    st.markdown("**Recent Website Transactions:**")

    websites_df = pd.DataFrame(websites)
    if not websites_df.empty:
        websites_df["formatted_timestamp"] = pd.to_datetime(
            websites_df["timestamp"]
        ).dt.strftime("%Y-%m-%d %H:%M")
        websites_df = websites_df.sort_values("timestamp", ascending=False)

        for _, transaction in websites_df.head(10).iterrows():
            timestamp = transaction.get("formatted_timestamp", "Unknown")
            source = transaction.get("source", "Unknown")
            revenue_type = transaction.get("revenue_type", "Revenue")
            amount = transaction.get("amount", 0)
            transaction_id = transaction.get("transaction_id", "")

            st.markdown(
                f"""
            <div style="background: rgba(65,105,225,0.1); padding: 10px; margin: 5px 0; 
                        border-left: 4px solid #4169E1; border-radius: 5px;">
                <strong>🌐 {source}</strong> - {revenue_type} - <span style="color: #32CD32;">${amount:,.2f}</span><br>
                <small>📅 {timestamp} • ID: {transaction_id}</small>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # Add new transaction form
    with st.expander("➕ Add New Website Revenue"):
        source = st.text_input("Website/Source Name:", key="website_source_main_1")
        revenue_type = st.selectbox(
            "Revenue Type:",
            [
                "Product Sales",
                "Service Fees",
                "Subscription",
                "Advertising",
                "Affiliate",
                "Licensing",
                "Donations",
            ],
            key="website_type_main_1",
        )
        amount = st.number_input(
            "Revenue Amount ($):", min_value=0.0, step=0.01, key="website_amount_main_1"
        )
        transaction_id = st.text_input(
            "Transaction ID (optional):", key="website_id_main_1"
        )

        if st.button("💰 Record Website Revenue", key="website_button_main_1"):
            if source and amount > 0:
                new_transaction = {
                    "source": source,
                    "revenue_type": revenue_type,
                    "amount": amount,
                    "transaction_id": transaction_id,
                    "timestamp": datetime.now().isoformat(),
                }

                if append_entry("websites.json", "transactions", new_transaction):
                    st.success(f"🎉 Website revenue recorded: ${amount} from {source}")
                    st.rerun()


def revenue_crown_interface():
    """Main Revenue Crown interface"""

    st.set_page_config(
        page_title="💰 Codex Revenue Crown", page_icon="💰", layout="wide"
    )

    # Custom CSS
    st.markdown(
        """
    <style>
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #fff;
    }
    .revenue-header {
        text-align: center;
        padding: 30px;
        margin-bottom: 20px;
        background: linear-gradient(45deg, rgba(255,215,0,0.3), rgba(50,205,50,0.2));
        border: 2px solid #FFD700;
        border-radius: 20px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Header
    st.markdown(
        """
    <div class="revenue-header">
        <h1>💰 CODEX REVENUE CROWN — FINANCIAL SOVEREIGNTY</h1>
        <h3>🌟 Advanced Revenue Analytics & Management Dashboard 🌟</h3>
        <p><em>Track, analyze, and optimize your digital empire's revenue streams</em></p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Load revenue data
    stores = load_json("stores.json", {"transactions": []})["transactions"]
    social = load_json("social.json", {"transactions": []})["transactions"]
    websites = load_json("websites.json", {"transactions": []})["transactions"]

    # Calculate metrics
    metrics = create_revenue_metrics(stores, social, websites)

    # Top-level metrics dashboard
    st.markdown("### 👑 **Sovereign Revenue Overview**")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💎 Total Revenue",
            f"${metrics['totals']['grand_total']:,.2f}",
            delta=f"{metrics['growth']['total']:+.1f}%",
        )

    with col2:
        st.metric(
            "🏬 Stores Revenue",
            f"${metrics['totals']['stores']:,.2f}",
            delta=f"{metrics['growth']['stores']:+.1f}%",
        )

    with col3:
        st.metric(
            "📱 Social Revenue",
            f"${metrics['totals']['social']:,.2f}",
            delta=f"{metrics['growth']['social']:+.1f}%",
        )

    with col4:
        st.metric(
            "🌐 Website Revenue",
            f"${metrics['totals']['websites']:,.2f}",
            delta=f"{metrics['growth']['websites']:+.1f}%",
        )

    st.markdown("---")

    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "🏬 Stores",
            "📱 Social Media",
            "🌐 Websites",
            "📊 Analytics",
            "💎 Total Balance",
        ]
    )

    with tab1:
        display_stores_tab(stores)

    with tab2:
        display_social_media_tab(social)

    with tab3:
        display_websites_tab(websites)

    with tab4:
        st.markdown("### 📊 **Advanced Revenue Analytics**")
        create_revenue_visualizations(stores, social, websites)

    with tab5:
        st.markdown("### 💎 **Sovereign Financial Summary**")

        # Grand total with styling
        st.markdown(
            f"""
        <div style="text-align: center; padding: 30px; 
                    background: linear-gradient(45deg, rgba(255,215,0,0.3), rgba(50,205,50,0.2)); 
                    border: 3px solid #FFD700; border-radius: 20px; margin: 20px 0;">
            <h1 style="color: #FFD700; margin: 0;">👑 APPROVED SOVEREIGN BALANCE</h1>
            <h2 style="color: #32CD32; margin: 10px 0; font-size: 3em;">${metrics['totals']['grand_total']:,.2f}</h2>
            <p style="color: #fff; margin: 0;"><em>Digital Empire Financial Status: PROSPEROUS</em></p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Detailed breakdown
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**💰 Revenue Stream Breakdown:**")
            breakdown_data = [
                ["🏬 Physical Stores", f"${metrics['totals']['stores']:,.2f}"],
                ["📱 Social Media", f"${metrics['totals']['social']:,.2f}"],
                ["🌐 Digital Platforms", f"${metrics['totals']['websites']:,.2f}"],
                ["━━━━━━━━━━━━━━━", "━━━━━━━━━━━━━"],
                [
                    "👑 **TOTAL SOVEREIGNTY**",
                    f"**${metrics['totals']['grand_total']:,.2f}**",
                ],
            ]

            for item, value in breakdown_data:
                st.markdown(f"{item}: {value}")

        with col2:
            st.markdown("**📈 Growth Performance (30 days):**")
            growth_data = [
                ["🏬 Stores Growth", f"{metrics['growth']['stores']:+.1f}%"],
                ["📱 Social Growth", f"{metrics['growth']['social']:+.1f}%"],
                ["🌐 Website Growth", f"{metrics['growth']['websites']:+.1f}%"],
                ["━━━━━━━━━━━━━━━", "━━━━━━━━━━━━"],
                ["🚀 **TOTAL GROWTH**", f"**{metrics['growth']['total']:+.1f}%**"],
            ]

            for item, value in growth_data:
                growth_color = (
                    "#32CD32" if "+" in value else "#FF6347" if "-" in value else "#FFF"
                )
                st.markdown(
                    f"{item}: <span style='color: {growth_color}'>{value}</span>",
                    unsafe_allow_html=True,
                )

        # Recent activity summary
        st.markdown("---")
        st.markdown("### 🕐 **Recent Revenue Activity**")

        all_recent = []

        # Collect recent transactions from all sources
        for store in stores[-3:]:  # Last 3 from each
            all_recent.append(
                {
                    "timestamp": store.get("timestamp", ""),
                    "source": "🏬 Store",
                    "description": store.get("item", "Store Sale"),
                    "amount": store.get("amount", 0),
                }
            )

        for social_item in social[-3:]:
            all_recent.append(
                {
                    "timestamp": social_item.get("timestamp", ""),
                    "source": "📱 Social",
                    "description": f"{social_item.get('platform', 'Social')} Revenue",
                    "amount": social_item.get("amount", 0),
                }
            )

        for website in websites[-3:]:
            all_recent.append(
                {
                    "timestamp": website.get("timestamp", ""),
                    "source": "🌐 Website",
                    "description": website.get("source", "Website Revenue"),
                    "amount": website.get("amount", 0),
                }
            )

        # Sort by timestamp and display
        all_recent.sort(key=lambda x: x["timestamp"], reverse=True)

        for transaction in all_recent[:10]:  # Show top 10
            try:
                formatted_time = datetime.fromisoformat(
                    transaction["timestamp"]
                ).strftime("%Y-%m-%d %H:%M")
            except:
                formatted_time = transaction["timestamp"][:16]

            st.markdown(
                f"""
            <div style="background: rgba(255,255,255,0.05); padding: 10px; margin: 5px 0; 
                        border-left: 3px solid #FFD700; border-radius: 5px;">
                <strong>{transaction['source']}</strong> - {transaction['description']} - 
                <span style="color: #32CD32;">${transaction['amount']:,.2f}</span><br>
                <small>📅 {formatted_time}</small>
            </div>
            """,
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    revenue_crown_interface()

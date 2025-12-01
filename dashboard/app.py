# dashboard/app.py
import json
import os
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

# Configuration
API_BASE = os.getenv("API_BASE", "http://localhost:8000")
st.set_page_config(
    page_title="Codex Market Dominion",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #007bff;
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
</style>
""",
    unsafe_allow_html=True,
)


# Helper Functions
def make_request(method, endpoint, data=None, timeout=10):
    """Make API request with error handling"""
    try:
        url = f"{API_BASE}{endpoint}"
        if method.upper() == "GET":
            response = requests.get(url, timeout=timeout)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=timeout)
        else:
            raise ValueError(f"Unsupported method: {method}")

        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"API Error: {response.status_code} - {response.text}"

    except requests.exceptions.ConnectionError:
        return (
            None,
            "Connection Error: API server not available. Please ensure the API is running on port 8000.",
        )
    except requests.exceptions.Timeout:
        return None, "Timeout Error: API request took too long."
    except Exception as e:
        return None, f"Unexpected Error: {str(e)}"


# Resource Compliance & Health Loader
@st.cache_data(ttl=60)
def load_ledger_status():
    ledger_path = Path("codex_ledger.json")
    if ledger_path.exists():
        try:
            with open(ledger_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            st.error(f"Error loading ledger: {e}")
            return None
    return None


def display_error(message):
    """Display error message"""
    st.markdown(
        f'<div class="error-message">❌ {message}</div>', unsafe_allow_html=True
    )


def display_success(message):
    """Display success message"""
    st.markdown(
        f'<div class="success-message">✅ {message}</div>', unsafe_allow_html=True
    )


# Main App
def main():
    # Header
    st.markdown(
        """
    <div class="main-header">
        <h1>📊 Codex Market Dominion</h1>
        <p>Advanced Trading & Portfolio Management Platform</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # API Status & Resource Compliance Sidebar
    with st.sidebar:
        st.header("🔧 System Status")
        # Check API health
        health_data, health_error = make_request("GET", "/health")
        if health_data:
            st.success(f"✅ API Status: {health_data.get('status', 'Unknown')}")
            st.info(f"📊 Database: {health_data.get('database', 'Unknown')}")
            st.info(f"💾 Cache: {health_data.get('cache', 'Unknown')}")
        else:
            st.error("❌ API Unavailable")
            if health_error:
                st.error(health_error)
        st.text_input("API Base URL", value=API_BASE, disabled=True)

        # Resource Compliance & Health
        st.header("🛡️ Resource Compliance & Health")
        ledger = load_ledger_status()
        if ledger:
            meta = ledger.get("meta", {})
            metrics = ledger.get("system_metrics", {})
            st.metric(
                "System Completeness", metrics.get("system_completeness", "Unknown")
            )
            st.metric("Sovereignty Score", metrics.get("digital_sovereignty_score", 0))
            st.metric("Flame Power", metrics.get("flame_power_level", 0))
            st.metric("Omega Seal", "Active" if meta.get("omega_seal") else "Inactive")
            st.metric("Completed Cycles", len(ledger.get("cycles", [])))
            st.metric("Proclamations", len(ledger.get("proclamations", [])))
            st.metric("Archives", len(ledger.get("completed_archives", [])))
            st.caption(f"Last Updated: {meta.get('last_updated', 'N/A')}")
        else:
            st.warning("No ledger data found.")

    # Main Tabs
    tab_portfolio, tab_picks, tab_ai, tab_affiliate, tab_amm, tab_compliance = st.tabs(
        [
            "📊 Portfolio",
            "📈 Daily Picks",
            "🤖 AI Builder",
            "🤝 Affiliate Marketing",
            "🔄 AMM Trading",
            "🛡️ Compliance & Lineage",
        ]
    )
    with tab_compliance:
        st.header("🛡️ Resource Compliance & Lineage Dashboard")
        ledger = load_ledger_status()
        if ledger:
            meta = ledger.get("meta", {})
            metrics = ledger.get("system_metrics", {})
            st.subheader("System Metrics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Completeness", metrics.get("system_completeness", "Unknown"))
            with col2:
                st.metric(
                    "Sovereignty Score", metrics.get("digital_sovereignty_score", 0)
                )
            with col3:
                st.metric("Flame Power", metrics.get("flame_power_level", 0))
            with col4:
                st.metric(
                    "Omega Seal", "Active" if meta.get("omega_seal") else "Inactive"
                )

            st.subheader("Cycles & Proclamations")
            st.write(f"**Completed Cycles:** {len(ledger.get('cycles', []))}")
            st.write(f"**Proclamations:** {len(ledger.get('proclamations', []))}")
            st.write(f"**Archives:** {len(ledger.get('completed_archives', []))}")
            st.caption(f"Last Updated: {meta.get('last_updated', 'N/A')}")

            # Timeline chart for cycles
            cycles = ledger.get("cycles", [])
            if cycles:
                df_cycles = pd.DataFrame(cycles)
                if "name" in df_cycles and "completed_at" in df_cycles:
                    df_cycles["completed_at"] = pd.to_datetime(
                        df_cycles["completed_at"], errors="coerce"
                    )
                    fig = px.timeline(
                        df_cycles,
                        x_start=(
                            "initiated_date"
                            if "initiated_date" in df_cycles
                            else "started_at"
                        ),
                        x_end="completed_at",
                        y="name",
                        title="Cycle Completion Timeline",
                    )
                    st.plotly_chart(fig, use_container_width=True)

            # List proclamations
            st.subheader("Proclamations")
            for proc in ledger.get("proclamations", []):
                st.write(f"- {proc.get('title', 'N/A')} ({proc.get('status', 'N/A')})")

            # List archives
            st.subheader("Completed Archives")
            for arch in ledger.get("completed_archives", []):
                st.write(
                    f"- {arch.get('name', 'N/A')} (Sealed: {arch.get('custodian_seal', 'N/A')}, Date: {arch.get('completed_at', 'N/A')})"
                )

        else:
            st.warning("No ledger data found for compliance dashboard.")

        # Display ceremonial summary scroll for heirs and councils
        scroll_path = Path("scrolls/ceremonial_summary_scroll.md")
        if scroll_path.exists():
            st.subheader("Ceremonial Summary Scroll")
            with open(scroll_path, "r", encoding="utf-8") as f:
                ceremonial_text = f.read()
            st.markdown(ceremonial_text)
        else:
            st.info("No ceremonial summary scroll found.")

    with tab_portfolio:
        st.header("📊 Portfolio Management")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Load Portfolio Positions")
            pid = st.text_input(
                "Portfolio ID", placeholder="Enter portfolio ID (e.g., portfolio-123)"
            )

            if st.button("🔍 Load Positions", type="primary"):
                if pid:
                    data, error = make_request("GET", f"/portfolio/{pid}/positions")

                    if data and "positions" in data:
                        positions = data["positions"]
                        summary = data.get("summary", {})

                        # Display summary metrics
                        st.subheader("📋 Portfolio Summary")
                        col_a, col_b, col_c, col_d = st.columns(4)

                        with col_a:
                            st.metric(
                                "Total Positions", summary.get("total_positions", 0)
                            )
                        with col_b:
                            market_value = summary.get("total_market_value", 0)
                            st.metric("Market Value", f"${market_value:,.2f}")
                        with col_c:
                            cost_basis = summary.get("total_cost_basis", 0)
                            st.metric("Cost Basis", f"${cost_basis:,.2f}")
                        with col_d:
                            pnl = summary.get("total_unrealized_pnl", 0)
                            pnl_color = "normal" if pnl >= 0 else "inverse"
                            st.metric(
                                "Unrealized P&L",
                                f"${pnl:,.2f}",
                                delta=f"{summary.get('portfolio_return_percent', 0):.1f}%",
                            )

                        # Display positions
                        if positions:
                            st.subheader("📈 Position Details")
                            for p in positions:
                                with st.container():
                                    col_sym, col_qty, col_price, col_value, col_pnl = (
                                        st.columns([2, 2, 2, 2, 2])
                                    )

                                    with col_sym:
                                        st.write(f"**{p['symbol']}**")

                                    with col_qty:
                                        st.metric("Quantity", f"{p['quantity']:,.0f}")

                                    with col_price:
                                        last_price = p.get("last_price", 0)
                                        avg_cost = p.get("avg_cost", 0)
                                        price_change = (
                                            last_price - avg_cost
                                            if last_price and avg_cost
                                            else 0
                                        )
                                        st.metric(
                                            "Last Price",
                                            (
                                                f"${last_price:.2f}"
                                                if last_price
                                                else "N/A"
                                            ),
                                            delta=(
                                                f"${price_change:.2f}"
                                                if price_change != 0
                                                else None
                                            ),
                                        )

                                    with col_value:
                                        market_val = p.get("market_value", 0)
                                        st.metric("Market Value", f"${market_val:,.2f}")

                                    with col_pnl:
                                        unrealized_pnl = p.get("unrealized_pnl", 0)
                                        return_pct = p.get("return_percent", 0)
                                        st.metric(
                                            "P&L",
                                            f"${unrealized_pnl:,.2f}",
                                            delta=f"{return_pct:.1f}%",
                                        )

                                st.divider()

                        else:
                            st.info("📝 No positions found in this portfolio.")

                    elif error:
                        display_error(error)
                    else:
                        display_error("Failed to load portfolio data.")
                else:
                    st.warning("⚠️ Please enter a Portfolio ID.")

        with col2:
            st.subheader("📊 Portfolio Performance")
            if pid:
                perf_data, perf_error = make_request(
                    "GET", f"/portfolio/{pid}/performance?days=30"
                )

                if perf_data and "performance" in perf_data:
                    performance = perf_data["performance"]
                    summary = perf_data.get("summary", {})

                    # Create performance chart
                    df = pd.DataFrame(performance)
                    if not df.empty:
                        df["date"] = pd.to_datetime(df["date"])

                        fig = px.line(
                            df,
                            x="date",
                            y="portfolio_value",
                            title="Portfolio Performance (30 Days)",
                            labels={
                                "portfolio_value": "Portfolio Value ($)",
                                "date": "Date",
                            },
                        )

                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)

                        # Performance summary
                        st.subheader("📈 Performance Summary")
                        col_start, col_end, col_return = st.columns(3)

                        with col_start:
                            st.metric(
                                "Starting Value",
                                f"${summary.get('starting_value', 0):,.2f}",
                            )
                        with col_end:
                            st.metric(
                                "Current Value",
                                f"${summary.get('ending_value', 0):,.2f}",
                            )
                        with col_return:
                            total_return = summary.get("total_return", 0)
                            st.metric("Total Return", f"{total_return:.2f}%")

    with tab_picks:
        st.header("📈 Daily Trading Picks")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("🎯 Create Trading Picks")
            uid = st.text_input("User ID", placeholder="Enter user ID")
            trade_date = st.date_input("Trade Date", value=date.today())

            # Symbol input with validation
            symbols_input = st.text_input(
                "Symbols (comma-separated)",
                placeholder="e.g., AAPL, MSFT, GOOGL",
                help="Enter stock symbols separated by commas",
            )

            if st.button("🧠 Score Picks", type="primary"):
                if uid and symbols_input:
                    # Parse symbols
                    symbols = [
                        s.strip().upper() for s in symbols_input.split(",") if s.strip()
                    ]

                    if symbols:
                        payload = {
                            "user_id": uid,
                            "trade_date": str(trade_date),
                            "symbols": symbols,
                        }

                        with st.spinner("🔄 Analyzing picks..."):
                            result, error = make_request("POST", "/picks", data=payload)

                        if result:
                            display_success("Trading picks analyzed successfully!")

                            # Display results
                            st.subheader("📊 Analysis Results")

                            # Overall scores
                            scores = result.get("scores", {})
                            composite_score = result.get("composite_score", 0)

                            col_a, col_b, col_c = st.columns(3)
                            with col_a:
                                st.metric(
                                    "Composite Score", f"{composite_score:.1f}/100"
                                )
                            with col_b:
                                st.metric(
                                    "Symbols Analyzed",
                                    result.get("symbols_analyzed", 0),
                                )
                            with col_c:
                                expected_return = result.get("performance", {}).get(
                                    "expected_return", 0
                                )
                                st.metric("Expected Return", f"{expected_return:.1f}%")

                            # Score breakdown
                            if scores:
                                st.subheader("🔍 Score Breakdown")
                                score_df = pd.DataFrame(
                                    list(scores.items()), columns=["Category", "Score"]
                                )

                                fig = px.bar(
                                    score_df,
                                    x="Category",
                                    y="Score",
                                    title="Trading Signal Scores",
                                )
                                fig.update_layout(height=300)
                                st.plotly_chart(fig, use_container_width=True)

                            # Detailed JSON for advanced users
                            with st.expander("🔧 Advanced: Full Analysis Data"):
                                st.json(result)

                        elif error:
                            display_error(error)
                    else:
                        st.warning("⚠️ Please enter valid stock symbols.")
                else:
                    st.warning("⚠️ Please fill in all required fields.")

        with col2:
            st.subheader("📊 Market Trending")

            if st.button("🔥 Load Trending Symbols"):
                trending_data, trending_error = make_request("GET", "/market/trending")

                if trending_data and "trending_symbols" in trending_data:
                    symbols = trending_data["trending_symbols"]

                    st.subheader("🌟 Top Trending")
                    for symbol_data in symbols:
                        col_sym, col_price, col_change = st.columns([2, 2, 2])

                        with col_sym:
                            st.write(f"**{symbol_data.get('symbol', 'N/A')}**")
                        with col_price:
                            price = symbol_data.get("price", 0)
                            st.metric("Price", f"${price:.2f}" if price else "N/A")
                        with col_change:
                            change_pct = symbol_data.get("change_percent", 0)
                            st.metric("Change", f"{change_pct:.2f}%")

                elif trending_error:
                    display_error(trending_error)

    with tab_ai:
        st.header("🤖 AI Portfolio Builder")

        st.info(
            "🎯 AI Builder proposes allocations by risk tier and detects missing exposures."
        )

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("🎚️ Risk Tier Selection")
            tier = st.selectbox(
                "Select Risk Tier", ["conservative", "moderate", "aggressive"]
            )

            # Portfolio templates
            templates = {
                "conservative": {
                    "Bonds/Defensive": 0.5,
                    "Large-cap Dividend": 0.3,
                    "Core Equity ETF": 0.2,
                },
                "moderate": {
                    "Core Equity ETF": 0.5,
                    "Sector ETFs": 0.3,
                    "Growth Sleeve": 0.2,
                },
                "aggressive": {
                    "Growth/Small-cap": 0.5,
                    "Thematic/Momentum": 0.3,
                    "Core ETF": 0.2,
                },
            }

            st.subheader(f"📊 {tier.title()} Allocation")
            allocation = templates[tier]

            # Display as chart
            df_allocation = pd.DataFrame(
                list(allocation.items()), columns=["Asset Class", "Weight"]
            )
            df_allocation["Weight_Percent"] = df_allocation["Weight"] * 100

            fig = px.pie(
                df_allocation,
                values="Weight",
                names="Asset Class",
                title=f"{tier.title()} Portfolio Allocation",
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("📋 Recommended Weights")

            for asset_class, weight in allocation.items():
                col_asset, col_weight = st.columns([3, 1])

                with col_asset:
                    st.write(f"**{asset_class}**")
                with col_weight:
                    st.write(f"{weight:.0%}")

            st.divider()

            # Risk metrics
            st.subheader("⚖️ Risk Characteristics")

            risk_profiles = {
                "conservative": {
                    "volatility": "Low",
                    "expected_return": "4-6%",
                    "drawdown_risk": "Minimal",
                },
                "moderate": {
                    "volatility": "Medium",
                    "expected_return": "6-10%",
                    "drawdown_risk": "Moderate",
                },
                "aggressive": {
                    "volatility": "High",
                    "expected_return": "10-15%",
                    "drawdown_risk": "Significant",
                },
            }

            profile = risk_profiles[tier]

            st.metric("Expected Volatility", profile["volatility"])
            st.metric("Expected Annual Return", profile["expected_return"])
            st.metric("Drawdown Risk", profile["drawdown_risk"])

        st.caption(
            "⚠️ **Disclaimer**: Educational guidance only; consult a professional for personal investment advice."
        )

    with tab_affiliate:
        st.header("🤝 Affiliate Marketing Dashboard")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("📊 Current Stats")

            if st.button("📈 Fetch Affiliate Stats", type="primary"):
                data, error = make_request("GET", "/affiliate/stats")

                if data:
                    display_success("Affiliate stats loaded successfully!")

                    # Main metrics
                    col_a, col_b, col_c = st.columns(3)

                    with col_a:
                        clicks = data.get("clicks", 0)
                        st.metric("Total Clicks", f"{clicks:,}")

                    with col_b:
                        conversions = data.get("conversions", 0)
                        st.metric("Conversions", conversions)

                    with col_c:
                        commission = data.get("commission_usd", 0)
                        st.metric("Commission (USD)", f"${commission:,.2f}")

                    # Additional metrics
                    st.subheader("🎯 Performance Metrics")

                    conversion_rate = data.get("conversion_rate", 0)
                    st.metric("Conversion Rate", f"{conversion_rate:.2f}%")

                    program = data.get("program", "N/A")
                    st.info(f"**Program**: {program}")

                    # Top referrers
                    top_referrers = data.get("top_referrers", [])
                    if top_referrers:
                        st.subheader("🌟 Top Traffic Sources")
                        for i, source in enumerate(top_referrers, 1):
                            st.write(f"{i}. {source}")

                elif error:
                    display_error(error)

        with col2:
            st.subheader("📈 Performance Analysis")

            # Mock performance chart
            st.info(
                "📊 Performance trends will be displayed here when historical data is available."
            )

            # Commission calculator
            st.subheader("💰 Commission Calculator")

            estimated_clicks = st.number_input(
                "Estimated Monthly Clicks", min_value=0, value=1000, step=100
            )
            conversion_rate_input = st.number_input(
                "Conversion Rate (%)",
                min_value=0.0,
                max_value=100.0,
                value=3.5,
                step=0.1,
            )
            commission_per_conversion = st.number_input(
                "Commission per Conversion ($)", min_value=0.0, value=50.0, step=5.0
            )

            if estimated_clicks > 0:
                estimated_conversions = estimated_clicks * conversion_rate_input / 100
                estimated_commission = estimated_conversions * commission_per_conversion

                st.metric("Estimated Conversions", f"{estimated_conversions:.1f}")
                st.metric(
                    "Estimated Monthly Commission", f"${estimated_commission:,.2f}"
                )

    with tab_amm:
        st.header("🔄 AMM Trading Dashboard")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("💰 DeFi Pools")

            if st.button("🔍 Load Top Pools", type="primary"):
                pools_data, pools_error = make_request("GET", "/amm/pools")

                if pools_data and "pools" in pools_data:
                    pools = pools_data["pools"]
                    summary = pools_data

                    # Summary metrics
                    st.subheader("📊 Pool Summary")
                    col_a, col_b, col_c = st.columns(3)

                    with col_a:
                        st.metric("Total Pools", summary.get("total_pools", 0))
                    with col_b:
                        total_tvl = summary.get("total_tvl", 0)
                        st.metric(
                            "Total TVL",
                            (
                                f"${total_tvl/1e6:.1f}M"
                                if total_tvl > 1e6
                                else f"${total_tvl:,.0f}"
                            ),
                        )
                    with col_c:
                        avg_apr = summary.get("avg_apr", 0)
                        st.metric("Average APR", f"{avg_apr:.1f}%")

                    # Pool details
                    st.subheader("🏊 Pool Rankings")
                    for pool in pools[:5]:  # Show top 5
                        with st.container():
                            col_pool, col_tvl, col_apr, col_risk = st.columns(
                                [3, 2, 2, 2]
                            )

                            with col_pool:
                                st.write(f"**{pool.get('pool', 'N/A')}**")

                            with col_tvl:
                                tvl = pool.get("tvl_usd", 0)
                                st.metric(
                                    "TVL",
                                    f"${tvl/1e6:.1f}M" if tvl > 1e6 else f"${tvl:,.0f}",
                                )

                            with col_apr:
                                apr = pool.get("apr", 0)
                                st.metric("APR", f"{apr:.1f}%")

                            with col_risk:
                                risk = pool.get("risk_tier", "unknown")
                                risk_color = {
                                    "low": "🟢",
                                    "medium": "🟡",
                                    "high": "🔴",
                                }.get(risk, "⚪")
                                st.write(f"{risk_color} {risk.title()}")

                        st.divider()

                elif pools_error:
                    display_error(pools_error)

        with col2:
            st.subheader("💱 Execute Swap")

            pool_id = st.text_input("Pool ID", placeholder="e.g., pool-001")

            col_from, col_to = st.columns(2)
            with col_from:
                from_asset = st.text_input("From Asset", placeholder="e.g., USDC")
            with col_to:
                to_asset = st.text_input("To Asset", placeholder="e.g., ETH")

            amount = st.number_input(
                "Amount",
                min_value=0.0,
                step=0.1,
                help="Amount of the 'From Asset' to swap",
            )

            if st.button("🔄 Execute Swap", type="primary"):
                if pool_id and from_asset and to_asset and amount > 0:
                    payload = {
                        "pool_id": pool_id,
                        "from_asset": from_asset.upper(),
                        "to_asset": to_asset.upper(),
                        "amount": amount,
                    }

                    with st.spinner("⚡ Processing swap..."):
                        result, error = make_request("POST", "/amm/swap", data=payload)

                    if result:
                        display_success("Swap executed successfully!")

                        # Swap details
                        st.subheader("📋 Swap Details")

                        tx = result.get("tx", {})
                        swap_details = result.get("swap_details", {})

                        if tx:
                            st.code(f"Transaction Hash: {tx.get('hash', 'N/A')}")
                            st.info(f"Status: {tx.get('status', 'Unknown')}")
                            st.info(
                                f"Confirmation: {tx.get('estimated_confirmation', 'Unknown')}"
                            )

                        if swap_details:
                            col_input, col_output = st.columns(2)

                            with col_input:
                                st.metric(
                                    "Input",
                                    f"{swap_details.get('input_amount', 0)} {swap_details.get('from_asset', '')}",
                                )

                            with col_output:
                                estimated_output = swap_details.get(
                                    "estimated_output", 0
                                )
                                st.metric(
                                    "Estimated Output",
                                    f"{estimated_output:.6f} {swap_details.get('to_asset', '')}",
                                )

                            st.caption(
                                f"Fee: {swap_details.get('fee_percent', 0)}% | Slippage: {swap_details.get('slippage_tolerance', 0)}%"
                            )

                        # Full response for advanced users
                        with st.expander("🔧 Advanced: Full Response"):
                            st.json(result)

                    elif error:
                        display_error(error)

                else:
                    st.warning("⚠️ Please fill in all swap parameters.")

            # Swap calculator
            st.subheader("🧮 Swap Calculator")
            st.info("💡 Enter swap parameters above to see estimated fees and output.")


if __name__ == "__main__":
    main()

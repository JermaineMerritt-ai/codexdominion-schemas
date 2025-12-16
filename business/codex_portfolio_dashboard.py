"""
Codex Portfolio Management Dashboard
Advanced Streamlit interface for trading and portfolio management
"""

import asyncio
import json
import uuid
from datetime import date, datetime, timedelta
from decimal import Decimal

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

# Import our database module
try:
    from codex_database import (db, get_affiliate_performance,
                                get_portfolio_summary, get_top_pools)

    DATABASE_AVAILABLE = True
except ImportError as e:
    DATABASE_AVAILABLE = False

# Import error handler if available
try:
    from codex_error_handler import CodexErrorHandler, safe_execute

    ERROR_HANDLER_AVAILABLE = True
except ImportError:
    ERROR_HANDLER_AVAILABLE = False

    # Simple fallback decorator
    def safe_execute(func=None):
        def decorator(f):
            def wrapper(*args, **kwargs):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    st.error(f"Error in {f.__name__}: {e}")
                    return None

            return wrapper

        if func is None:
            # Called as @safe_execute()
            return decorator
        else:
            # Called as @safe_execute
            return decorator(func)


# Configure Streamlit page
st.set_page_config(
    page_title="Codex Portfolio Manager",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for enhanced styling
st.markdown(
    """
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }

    .metric-card {
        background: linear-gradient(145deg, #f0f2f6, #ffffff);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #2a5298;
        margin-bottom: 1rem;
    }

    .performance-positive {
        color: #00C851;
        font-weight: bold;
    }

    .performance-negative {
        color: #ff4444;
        font-weight: bold;
    }

    .risk-low {
        color: #00C851;
        background-color: #e8f5e8;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
    }

    .risk-medium {
        color: #ffbb33;
        background-color: #fff8e1;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
    }

    .risk-high {
        color: #ff4444;
        background-color: #ffebee;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
    }

    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Error handler
if ERROR_HANDLER_AVAILABLE:
    error_handler = CodexErrorHandler()
else:
    error_handler = None


# Helper functions
def format_currency(amount):
    """Format currency with proper styling"""
    if amount >= 0:
        return f'<span class="performance-positive">${amount:,.2f}</span>'
    else:
        return f'<span class="performance-negative">-${abs(amount):,.2f}</span>'


def format_percentage(percentage):
    """Format percentage with proper styling"""
    if percentage >= 0:
        return f'<span class="performance-positive">+{percentage:.2f}%</span>'
    else:
        return f'<span class="performance-negative">{percentage:.2f}%</span>'


def get_risk_badge(risk_tier):
    """Get styled risk tier badge"""
    risk_classes = {
        "conservative": "risk-low",
        "low": "risk-low",
        "moderate": "risk-medium",
        "medium": "risk-medium",
        "aggressive": "risk-high",
        "high": "risk-high",
    }

    class_name = risk_classes.get(risk_tier, "risk-medium")
    return f'<span class="{class_name}">{risk_tier.upper()}</span>'


@safe_execute
def load_sample_data():
    """Load sample data when database is not available"""
    return {
        "portfolios": [
            {
                "id": str(uuid.uuid4()),
                "name": "Growth Portfolio",
                "risk_tier": "aggressive",
                "total_value": 125000.00,
                "total_cost": 100000.00,
                "unrealized_pnl": 25000.00,
                "return_percentage": 25.0,
                "positions": [
                    {
                        "symbol": "AAPL",
                        "quantity": 100,
                        "avg_cost": 150.00,
                        "last_price": 155.25,
                        "market_value": 15525.00,
                    },
                    {
                        "symbol": "MSFT",
                        "quantity": 50,
                        "avg_cost": 300.00,
                        "last_price": 310.50,
                        "market_value": 15525.00,
                    },
                    {
                        "symbol": "GOOGL",
                        "quantity": 25,
                        "avg_cost": 2500.00,
                        "last_price": 2475.00,
                        "market_value": 61875.00,
                    },
                ],
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Conservative Portfolio",
                "risk_tier": "conservative",
                "total_value": 85000.00,
                "total_cost": 80000.00,
                "unrealized_pnl": 5000.00,
                "return_percentage": 6.25,
                "positions": [
                    {
                        "symbol": "SPY",
                        "quantity": 200,
                        "avg_cost": 400.00,
                        "last_price": 405.00,
                        "market_value": 81000.00,
                    },
                    {
                        "symbol": "BND",
                        "quantity": 40,
                        "avg_cost": 100.00,
                        "last_price": 100.00,
                        "market_value": 4000.00,
                    },
                ],
            },
        ],
        "affiliate_performance": {
            "total_commission": 4850.00,
            "total_clicks": 2941,
            "total_conversions": 99,
            "overall_conversion_rate": 3.37,
            "programs": [
                {
                    "program": "TradingView",
                    "clicks": 1250,
                    "conversions": 45,
                    "commission": 2250.00,
                    "conversion_rate": 3.6,
                },
                {
                    "program": "Interactive Brokers",
                    "clicks": 890,
                    "conversions": 32,
                    "commission": 1600.00,
                    "conversion_rate": 3.6,
                },
                {
                    "program": "Webull",
                    "clicks": 567,
                    "conversions": 18,
                    "commission": 800.00,
                    "conversion_rate": 3.2,
                },
                {
                    "program": "TD Ameritrade",
                    "clicks": 234,
                    "conversions": 4,
                    "commission": 200.00,
                    "conversion_rate": 1.7,
                },
            ],
        },
        "amm_pools": [
            {
                "pool_symbol": "USDC/ETH",
                "tvl_usd": 125000000.00,
                "apr": 8.5,
                "risk_tier": "low",
            },
            {
                "pool_symbol": "DAI/USDC",
                "tvl_usd": 85000000.00,
                "apr": 4.2,
                "risk_tier": "low",
            },
            {
                "pool_symbol": "WBTC/ETH",
                "tvl_usd": 45000000.00,
                "apr": 12.8,
                "risk_tier": "medium",
            },
            {
                "pool_symbol": "LINK/ETH",
                "tvl_usd": 25000000.00,
                "apr": 18.5,
                "risk_tier": "medium",
            },
            {
                "pool_symbol": "UNI/ETH",
                "tvl_usd": 15000000.00,
                "apr": 35.2,
                "risk_tier": "high",
            },
        ],
    }


# Main application
def main():
    """Main dashboard application"""

    # Header
    st.markdown(
        """
    <div class="main-header">
        <h1>📈 Codex Portfolio Manager</h1>
        <p>Advanced Trading & Portfolio Management Dashboard</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.image(
            "https://via.placeholder.com/200x60/2a5298/ffffff?text=CODEX", width=200
        )

        st.markdown("### 🎯 Navigation")
        page = st.selectbox(
            "Select Dashboard",
            [
                "Portfolio Overview",
                "Position Management",
                "Trading Analytics",
                "Affiliate Performance",
                "DeFi Pools",
                "Risk Analysis",
            ],
        )

        st.markdown("### ⚙️ Settings")

        # Mock user selection (in real app, this would be from auth)
        user_id = st.selectbox(
            "User Portfolio",
            ["demo_user_001", "demo_user_002", "demo_user_003"],
            key="user_selector",
        )

        # Time range selector
        time_range = st.selectbox(
            "Time Range", ["1D", "1W", "1M", "3M", "6M", "1Y", "ALL"], index=3
        )

        # Refresh data button
        if st.button("🔄 Refresh Data", type="primary"):
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # Load data
    if DATABASE_AVAILABLE:
        try:
            # In real app, load from database
            data = load_sample_data()
        except Exception as e:
            st.error(f"Error loading data: {e}")
            data = load_sample_data()
    else:
        data = load_sample_data()

    # Page routing
    if page == "Portfolio Overview":
        show_portfolio_overview(data)
    elif page == "Position Management":
        show_position_management(data)
    elif page == "Trading Analytics":
        show_trading_analytics(data)
    elif page == "Affiliate Performance":
        show_affiliate_performance(data)
    elif page == "DeFi Pools":
        show_defi_pools(data)
    elif page == "Risk Analysis":
        show_risk_analysis(data)


def show_portfolio_overview(data):
    """Portfolio overview dashboard"""
    st.markdown("## 📊 Portfolio Overview")

    # Key metrics
    total_value = sum(p["total_value"] for p in data["portfolios"])
    total_cost = sum(p["total_cost"] for p in data["portfolios"])
    total_pnl = sum(p["unrealized_pnl"] for p in data["portfolios"])
    overall_return = (total_pnl / total_cost * 100) if total_cost > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
        <div class="metric-card">
            <h4>💼 Total Portfolio Value</h4>
            <h2>{format_currency(total_value)}</h2>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="metric-card">
            <h4>💰 Total Cost Basis</h4>
            <h2>${total_cost:,.2f}</h2>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div class="metric-card">
            <h4>📈 Unrealized P&L</h4>
            <h2>{format_currency(total_pnl)}</h2>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
        <div class="metric-card">
            <h4>🎯 Total Return</h4>
            <h2>{format_percentage(overall_return)}</h2>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Portfolio breakdown
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📈 Portfolio Performance")

        # Create performance chart
        portfolio_df = pd.DataFrame(
            [
                {
                    "Portfolio": p["name"],
                    "Value": p["total_value"],
                    "Cost": p["total_cost"],
                    "P&L": p["unrealized_pnl"],
                    "Return %": p["return_percentage"],
                    "Risk Tier": p["risk_tier"],
                }
                for p in data["portfolios"]
            ]
        )

        fig = px.bar(
            portfolio_df,
            x="Portfolio",
            y=["Value", "Cost"],
            title="Portfolio Value vs Cost Basis",
            barmode="group",
            color_discrete_map={"Value": "#2a5298", "Cost": "#64b5f6"},
        )

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(size=12),
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🎯 Asset Allocation")

        # Aggregate all positions
        all_positions = []
        for portfolio in data["portfolios"]:
            all_positions.extend(portfolio["positions"])

        # Calculate allocation
        symbol_values = {}
        for pos in all_positions:
            symbol = pos["symbol"]
            if symbol in symbol_values:
                symbol_values[symbol] += pos["market_value"]
            else:
                symbol_values[symbol] = pos["market_value"]

        allocation_df = pd.DataFrame(
            [
                {"Symbol": symbol, "Value": value}
                for symbol, value in symbol_values.items()
            ]
        )

        fig = px.pie(
            allocation_df, values="Value", names="Symbol", title="Asset Allocation"
        )

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(size=10),
        )

        st.plotly_chart(fig, use_container_width=True)

    # Portfolio details table
    st.markdown("### 📋 Portfolio Details")

    portfolio_details = []
    for portfolio in data["portfolios"]:
        portfolio_details.append(
            {
                "Portfolio Name": portfolio["name"],
                "Risk Tier": portfolio["risk_tier"],
                "Positions": len(portfolio["positions"]),
                "Total Value": f"${portfolio['total_value']:,.2f}",
                "Cost Basis": f"${portfolio['total_cost']:,.2f}",
                "Unrealized P&L": f"${portfolio['unrealized_pnl']:,.2f}",
                "Return %": f"{portfolio['return_percentage']:.2f}%",
            }
        )

    details_df = pd.DataFrame(portfolio_details)
    st.dataframe(details_df, use_container_width=True)


def show_position_management(data):
    """Position management interface"""
    st.markdown("## 📋 Position Management")

    # Add new position form
    with st.expander("➕ Add New Position", expanded=False):
        col1, col2, col3 = st.columns(3)

        with col1:
            portfolio_options = [p["name"] for p in data["portfolios"]]
            selected_portfolio = st.selectbox("Portfolio", portfolio_options)
            symbol = st.text_input("Symbol", placeholder="e.g., AAPL").upper()

        with col2:
            quantity = st.number_input("Quantity", min_value=0.001, step=1.0)
            avg_cost = st.number_input("Average Cost", min_value=0.01, step=0.01)

        with col3:
            st.markdown("<br>", unsafe_allow_html=True)  # Spacing
            if st.button("Add Position", type="primary"):
                st.success(f"Added {quantity} shares of {symbol} at ${avg_cost:.2f}")
                st.rerun()

    # Current positions
    st.markdown("### 📊 Current Positions")

    # Flatten all positions with portfolio info
    all_positions = []
    for portfolio in data["portfolios"]:
        for pos in portfolio["positions"]:
            all_positions.append(
                {
                    "Portfolio": portfolio["name"],
                    "Symbol": pos["symbol"],
                    "Quantity": pos["quantity"],
                    "Avg Cost": pos["avg_cost"],
                    "Last Price": pos["last_price"],
                    "Market Value": pos["market_value"],
                    "Unrealized P&L": (pos["last_price"] - pos["avg_cost"])
                    * pos["quantity"],
                    "Return %": (
                        (pos["last_price"] - pos["avg_cost"]) / pos["avg_cost"] * 100
                    ),
                }
            )

    positions_df = pd.DataFrame(all_positions)

    # Format the dataframe for display
    formatted_positions = positions_df.copy()
    for col in ["Avg Cost", "Last Price", "Market Value", "Unrealized P&L"]:
        formatted_positions[col] = formatted_positions[col].apply(
            lambda x: f"${x:,.2f}"
        )
    formatted_positions["Return %"] = formatted_positions["Return %"].apply(
        lambda x: f"{x:.2f}%"
    )

    st.dataframe(
        formatted_positions,
        use_container_width=True,
        column_config={
            "Return %": st.column_config.NumberColumn(
                "Return %", help="Percentage return on position"
            )
        },
    )

    # Position performance chart
    fig = px.scatter(
        positions_df,
        x="Market Value",
        y="Return %",
        size="Quantity",
        color="Portfolio",
        hover_name="Symbol",
        title="Position Performance Analysis",
        labels={
            "Return %": "Return Percentage (%)",
            "Market Value": "Market Value ($)",
        },
    )

    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")

    st.plotly_chart(fig, use_container_width=True)


def show_trading_analytics(data):
    """Trading analytics and insights"""
    st.markdown("## 📈 Trading Analytics")

    # Mock trading data
    dates = pd.date_range(
        start=datetime.now() - timedelta(days=30), end=datetime.now(), freq="D"
    )

    # Generate mock price data
    import random

    symbols = list(
        set(
            [
                pos["symbol"]
                for portfolio in data["portfolios"]
                for pos in portfolio["positions"]
            ]
        )
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Price Performance")

        # Mock price data
        price_data = []
        for symbol in symbols[:3]:  # Limit to 3 symbols for clarity
            base_price = random.uniform(100, 400)
            for date in dates:
                price = base_price * (1 + random.gauss(0, 0.02))  # 2% daily volatility
                price_data.append({"Date": date, "Symbol": symbol, "Price": price})
                base_price = price

        price_df = pd.DataFrame(price_data)

        fig = px.line(
            price_df, x="Date", y="Price", color="Symbol", title="30-Day Price Movement"
        )

        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🎯 Performance Metrics")

        # Calculate performance metrics
        metrics = []
        for portfolio in data["portfolios"]:
            for pos in portfolio["positions"]:
                volatility = random.uniform(0.15, 0.45)  # Mock volatility
                sharpe_ratio = random.uniform(0.5, 2.0)  # Mock Sharpe ratio

                metrics.append(
                    {
                        "Symbol": pos["symbol"],
                        "Return %": (
                            (pos["last_price"] - pos["avg_cost"])
                            / pos["avg_cost"]
                            * 100
                        ),
                        "Volatility": volatility,
                        "Sharpe Ratio": sharpe_ratio,
                        "Market Value": pos["market_value"],
                    }
                )

        metrics_df = pd.DataFrame(metrics)

        # Risk-Return scatter plot
        fig = px.scatter(
            metrics_df,
            x="Volatility",
            y="Return %",
            size="Market Value",
            color="Sharpe Ratio",
            hover_name="Symbol",
            title="Risk-Return Analysis",
            color_continuous_scale="viridis",
        )

        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")

        st.plotly_chart(fig, use_container_width=True)

    # Trading insights
    st.markdown("### 💡 Trading Insights")

    insights_col1, insights_col2 = st.columns(2)

    with insights_col1:
        st.info("**Top Performer**: AAPL with +3.5% return")
        st.success("**Best Sharpe Ratio**: MSFT at 1.85")

    with insights_col2:
        st.warning("**High Volatility**: GOOGL showing 35% volatility")
        st.error("**Underperformer**: Consider reviewing position sizing")


def show_affiliate_performance(data):
    """Affiliate marketing performance dashboard"""
    st.markdown("## 🤝 Affiliate Performance")

    affiliate_data = data["affiliate_performance"]

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💰 Total Commission",
            f"${affiliate_data['total_commission']:,.2f}",
            delta="+12.5%",
        )

    with col2:
        st.metric(
            "👆 Total Clicks", f"{affiliate_data['total_clicks']:,}", delta="+8.2%"
        )

    with col3:
        st.metric(
            "✅ Conversions", f"{affiliate_data['total_conversions']:,}", delta="+15.3%"
        )

    with col4:
        st.metric(
            "📊 Conversion Rate",
            f"{affiliate_data['overall_conversion_rate']:.2f}%",
            delta="+0.7%",
        )

    # Program performance
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Commission by Program")

        programs_df = pd.DataFrame(affiliate_data["programs"])

        fig = px.bar(
            programs_df,
            x="program",
            y="commission",
            title="Commission by Affiliate Program",
            color="conversion_rate",
            color_continuous_scale="viridis",
        )

        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🎯 Conversion Performance")

        fig = px.scatter(
            programs_df,
            x="clicks",
            y="conversions",
            size="commission",
            color="conversion_rate",
            hover_name="program",
            title="Clicks vs Conversions",
            color_continuous_scale="plasma",
        )

        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")

        st.plotly_chart(fig, use_container_width=True)

    # Detailed program table
    st.markdown("### 📋 Program Details")

    formatted_programs = programs_df.copy()
    formatted_programs["commission"] = formatted_programs["commission"].apply(
        lambda x: f"${x:,.2f}"
    )
    formatted_programs["conversion_rate"] = formatted_programs["conversion_rate"].apply(
        lambda x: f"{x:.2f}%"
    )

    st.dataframe(formatted_programs, use_container_width=True)


def show_defi_pools(data):
    """DeFi liquidity pools dashboard"""
    st.markdown("## 🏦 DeFi Liquidity Pools")

    pools_data = data["amm_pools"]

    # Pool metrics
    total_tvl = sum(pool["tvl_usd"] for pool in pools_data)
    avg_apr = sum(pool["apr"] for pool in pools_data) / len(pools_data)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("💧 Total TVL", f"${total_tvl/1000000:,.1f}M", delta="+5.2%")

    with col2:
        st.metric("📈 Average APR", f"{avg_apr:.2f}%", delta="+1.8%")

    with col3:
        st.metric("🏊 Active Pools", f"{len(pools_data)}", delta="+2")

    # Pool analysis
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💧 TVL Distribution")

        pools_df = pd.DataFrame(pools_data)

        fig = px.treemap(
            pools_df,
            path=["risk_tier", "pool_symbol"],
            values="tvl_usd",
            title="TVL by Risk Tier and Pool",
            color="apr",
            color_continuous_scale="viridis",
        )

        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### ⚖️ Risk vs Reward")

        fig = px.scatter(
            pools_df,
            x="apr",
            y="tvl_usd",
            size="tvl_usd",
            color="risk_tier",
            hover_name="pool_symbol",
            title="APR vs TVL by Risk Tier",
            log_y=True,
            color_discrete_map={
                "low": "#00C851",
                "medium": "#ffbb33",
                "high": "#ff4444",
            },
        )

        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")

        st.plotly_chart(fig, use_container_width=True)

    # Pool details table
    st.markdown("### 📊 Pool Details")

    formatted_pools = pools_df.copy()
    formatted_pools["tvl_usd"] = formatted_pools["tvl_usd"].apply(
        lambda x: f"${x/1000000:,.1f}M"
    )
    formatted_pools["apr"] = formatted_pools["apr"].apply(lambda x: f"{x:.2f}%")
    formatted_pools["risk_tier"] = formatted_pools["risk_tier"].apply(get_risk_badge)

    st.markdown(
        formatted_pools.to_html(escape=False, index=False), unsafe_allow_html=True
    )


def show_risk_analysis(data):
    """Risk analysis dashboard"""
    st.markdown("## ⚠️ Risk Analysis")

    # Portfolio risk breakdown
    risk_summary = {}
    total_value = 0

    for portfolio in data["portfolios"]:
        risk_tier = portfolio["risk_tier"]
        value = portfolio["total_value"]

        if risk_tier in risk_summary:
            risk_summary[risk_tier] += value
        else:
            risk_summary[risk_tier] = value

        total_value += value

    # Risk allocation
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎯 Risk Allocation")

        risk_df = pd.DataFrame(
            [
                {
                    "Risk Tier": tier.title(),
                    "Value": value,
                    "Percentage": value / total_value * 100,
                }
                for tier, value in risk_summary.items()
            ]
        )

        fig = px.pie(
            risk_df,
            values="Value",
            names="Risk Tier",
            title="Portfolio Risk Distribution",
            color_discrete_map={
                "Conservative": "#00C851",
                "Moderate": "#ffbb33",
                "Aggressive": "#ff4444",
            },
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 📊 Risk Metrics")

        # Mock risk metrics
        risk_metrics = [
            {"Metric": "Portfolio Beta", "Value": "1.25", "Status": "Medium Risk"},
            {
                "Metric": "Value at Risk (95%)",
                "Value": "$8,750",
                "Status": "Acceptable",
            },
            {"Metric": "Max Drawdown", "Value": "12.5%", "Status": "Low Risk"},
            {"Metric": "Sharpe Ratio", "Value": "1.65", "Status": "Good"},
            {"Metric": "Correlation Risk", "Value": "0.73", "Status": "Medium"},
        ]

        for metric in risk_metrics:
            st.markdown(
                f"""
            <div class="metric-card">
                <strong>{metric['Metric']}</strong><br>
                <span style="font-size: 1.2em; color: #2a5298;">{metric['Value']}</span><br>
                <small>{metric['Status']}</small>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # Risk recommendations
    st.markdown("### 💡 Risk Management Recommendations")

    recommendations = [
        "🎯 Consider rebalancing towards more conservative assets if risk tolerance has decreased",
        "📊 Current portfolio shows good diversification across risk tiers",
        "⚠️ Monitor correlation risk - some positions may be highly correlated",
        "💰 Value at Risk is within acceptable limits for current risk profile",
        "📈 Consider adding more defensive positions to reduce overall portfolio beta",
    ]

    for rec in recommendations:
        st.info(rec)


if __name__ == "__main__":
    main()

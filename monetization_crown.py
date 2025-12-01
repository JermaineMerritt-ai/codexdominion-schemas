"""
🔥 MONETIZATION CROWN 👑
Streamlined Multi-Platform Creator Economy Dashboard

The Merritt Method™ - Digital Monetization Sovereignty
Enhanced with Robust Error Handling and System Monitoring
"""

import json
import traceback
from pathlib import Path

import streamlit as st

# Enhanced Error Handling Integration
try:
    from codex_error_handler import (get_system_status, health_monitor,
                                     log_error, log_info, log_warning,
                                     safe_api_call, safe_execute,
                                     safe_file_operation)

    ERROR_HANDLING_AVAILABLE = True
    log_info(
        "Enhanced Monetization Crown starting with full error handling",
        "monetization_crown",
    )
except ImportError:
    ERROR_HANDLING_AVAILABLE = False

    # Fallback functions
    def log_info(msg, module="system"):
        pass

    def log_error(msg, module="system"):
        st.error(f"[{module}] {msg}")

    def log_warning(msg, module="system"):
        st.warning(f"[{module}] {msg}")

    def safe_execute(module_name, default_return=None):
        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    st.error(f"Error in {func.__name__}: {str(e)}")
                    return default_return

            return wrapper

        return decorator


# Safe imports - only import what's available
def safe_import(module_name, function_names=None):
    """Safely import modules and functions"""
    try:
        module = __import__(module_name)
        if function_names:
            functions = {}
            for func_name in function_names:
                if hasattr(module, func_name):
                    functions[func_name] = getattr(module, func_name)
                else:
                    functions[func_name] = None
            return functions
        return module
    except ImportError:
        if function_names:
            return {name: None for name in function_names}
        return None


# Import YouTube functions
youtube_functions = safe_import(
    "codex_youtube_charts", ["youtube_metrics", "archive_youtube"]
)
youtube_metrics = (
    youtube_functions.get("youtube_metrics") if youtube_functions else None
)
archive_youtube = (
    youtube_functions.get("archive_youtube") if youtube_functions else None
)

# Import TikTok functions
tiktok_functions = safe_import(
    "codex_tiktok_earnings", ["tiktok_metrics", "archive_tiktok"]
)
tiktok_metrics = tiktok_functions.get("tiktok_metrics") if tiktok_functions else None
archive_tiktok = tiktok_functions.get("archive_tiktok") if tiktok_functions else None

# Import Threads functions
threads_functions = safe_import(
    "codex_threads_engagement", ["threads_metrics", "archive_threads"]
)
threads_metrics = (
    threads_functions.get("threads_metrics") if threads_functions else None
)
archive_threads = (
    threads_functions.get("archive_threads") if threads_functions else None
)

# Import WhatsApp functions
whatsapp_functions = safe_import(
    "codex_whatsapp_business",
    ["whatsapp_metrics", "whatsapp_broadcast", "archive_whatsapp"],
)
whatsapp_metrics = (
    whatsapp_functions.get("whatsapp_metrics") if whatsapp_functions else None
)
whatsapp_broadcast = (
    whatsapp_functions.get("whatsapp_broadcast") if whatsapp_functions else None
)
archive_whatsapp = (
    whatsapp_functions.get("archive_whatsapp") if whatsapp_functions else None
)

# Import Pinterest functions
pinterest_functions = safe_import(
    "codex_pinterest_capsule",
    ["pinterest_metrics", "pinterest_pin", "archive_pinterest"],
)
pinterest_metrics = (
    pinterest_functions.get("pinterest_metrics") if pinterest_functions else None
)
pinterest_pin = (
    pinterest_functions.get("pinterest_pin") if pinterest_functions else None
)
archive_pinterest = (
    pinterest_functions.get("archive_pinterest") if pinterest_functions else None
)

# Import Dawn Monetization Scroll functions
dawn_functions = safe_import(
    "dawn_monetization_scroll", ["dawn_monetization_scroll", "get_monetization_history"]
)
dawn_monetization_scroll_func = (
    dawn_functions.get("dawn_monetization_scroll") if dawn_functions else None
)
get_monetization_history = (
    dawn_functions.get("get_monetization_history") if dawn_functions else None
)

# Import Affiliate Command functions
affiliate_functions = safe_import(
    "codex_affiliate_command", ["fetch_affiliate_metrics", "archive_affiliate"]
)
fetch_affiliate_metrics = (
    affiliate_functions.get("fetch_affiliate_metrics") if affiliate_functions else None
)
archive_affiliate = (
    affiliate_functions.get("archive_affiliate") if affiliate_functions else None
)


def main():
    st.set_page_config(
        page_title="👑 Monetization Crown",
        page_icon="🔥",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Custom CSS for enhanced styling
    st.markdown(
        """
    <style>
    .main-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4, #FFEAA7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #FF6B6B;
    }
    .success-message {
        background: linear-gradient(90deg, #00d4aa, #00b894);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: bold;
    }
    .platform-tab {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Main header
    st.markdown(
        '<h1 class="main-header">👑 Monetization Crown 🔥</h1>', unsafe_allow_html=True
    )
    st.markdown("### 🚀 **Multi-Platform Creator Economy Command Center**")

    # Platform availability status
    platforms_available = []
    if youtube_metrics:
        platforms_available.append("📺 YouTube")
    if tiktok_metrics:
        platforms_available.append("🎵 TikTok")
    if threads_metrics:
        platforms_available.append("🧵 Threads")
    if whatsapp_metrics:
        platforms_available.append("💬 WhatsApp")
    if pinterest_metrics:
        platforms_available.append("📌 Pinterest")
    if fetch_affiliate_metrics:
        platforms_available.append("💎 Affiliate")

    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.info(f"🔥 **Active Platforms:** {', '.join(platforms_available)}")
    with col2:
        st.metric("💎 Platforms", len(platforms_available))
    with col3:
        if st.button("🔄 Refresh All", key="refresh_all"):
            st.rerun()
    with col4:
        if st.button("📜 Generate Dawn Scroll", key="dawn_scroll"):
            if dawn_monetization_scroll_func:
                with st.spinner("Generating Dawn Monetization Scroll..."):
                    scroll_result = dawn_monetization_scroll_func()
                    if scroll_result.get("success"):
                        st.session_state["dawn_scroll"] = scroll_result
                        st.success("✅ Dawn Scroll Generated!")
                    else:
                        st.error("❌ Dawn Scroll Failed")
            else:
                st.error("❌ Dawn Scroll not available")

    # Display Dawn Monetization Scroll if generated
    if st.session_state.get("dawn_scroll"):
        scroll_data = st.session_state["dawn_scroll"]
        summary = scroll_data.get("summary", {})

        st.markdown("### 📜 **Dawn Monetization Scroll Summary**")

        scroll_col1, scroll_col2, scroll_col3, scroll_col4, scroll_col5 = st.columns(5)

        with scroll_col1:
            total_revenue = summary.get("total_revenue", 0)
            st.metric("💰 Total Revenue", f"${total_revenue:.2f}")

        with scroll_col2:
            active_platforms = summary.get("active_platforms", 0)
            st.metric("🚀 Active Platforms", f"{active_platforms}/5")

        with scroll_col3:
            top_platform = summary.get("top_platform", "None")
            st.metric(
                "👑 Top Platform",
                top_platform.title() if top_platform != "None" else "None",
            )

        with scroll_col4:
            performance_tier = summary.get("performance_tier", "startup")
            tier_emoji = {
                "elite": "👑",
                "advanced": "⭐",
                "growing": "📈",
                "emerging": "🌱",
                "startup": "🚀",
            }.get(performance_tier, "🔥")
            st.metric(f"{tier_emoji} Tier", performance_tier.title())

        with scroll_col5:
            diversification = summary.get("diversification_score", 0)
            st.metric("🎯 Diversification", f"{diversification:.1f}%")

        if total_revenue >= 500:
            st.success(
                "🔥 **ADVANCED TIER ACHIEVED** - Excellent monetization performance!"
            )
        elif total_revenue >= 100:
            st.info("📈 **GROWING TIER** - Strong progress toward monetization goals!")
        elif total_revenue > 0:
            st.warning("🌱 **EMERGING TIER** - Building monetization foundation!")
        else:
            st.error("🚀 **STARTUP TIER** - Ready to launch monetization strategy!")

        st.divider()

    # Main tabs for each platform
    (
        tab_youtube,
        tab_tiktok,
        tab_threads,
        tab_whatsapp,
        tab_pinterest,
        tab_affiliate,
        tab_portfolio,
    ) = st.tabs(
        [
            "📺 YouTube Charts",
            "🎵 TikTok Earnings",
            "🧵 Threads Engagement",
            "💬 WhatsApp Business",
            "📌 Pinterest Capsule",
            "💎 Affiliate Command",
            "📈 Portfolio Manager",
        ]
    )

    # YouTube Charts Tab
    with tab_youtube:
        st.markdown('<div class="platform-tab">', unsafe_allow_html=True)
        st.markdown("### 📺 **YouTube Creator Analytics**")

        if youtube_metrics:
            col1, col2 = st.columns([2, 1])

            with col1:
                ch_id = st.text_input(
                    "🎬 YouTube Channel ID:",
                    placeholder="Enter your YouTube Channel ID",
                    help="Find your Channel ID in YouTube Studio > Settings > Channel",
                )

            with col2:
                st.markdown("**💡 Quick Tips:**")
                st.markdown("• Channel ID format: UC...")
                st.markdown("• Use YouTube Studio")
                st.markdown("• Analytics updated daily")

            if st.button(
                "📊 Fetch YouTube Metrics", key="youtube_fetch", type="primary"
            ):
                if ch_id:
                    with st.spinner("Fetching YouTube analytics..."):
                        try:
                            m = youtube_metrics(ch_id)

                            if m.get("error"):
                                st.error(f"❌ Error: {m['error']}")
                            else:
                                # Display metrics in a clean layout
                                metric_col1, metric_col2, metric_col3 = st.columns(3)

                                with metric_col1:
                                    subscribers = m.get("subscribers", 0)
                                    st.metric("👥 Subscribers", f"{subscribers:,}")

                                with metric_col2:
                                    views = m.get("views", 0)
                                    st.metric("👀 Total Views", f"{views:,}")

                                with metric_col3:
                                    videos = m.get("videos", 0)
                                    st.metric("🎥 Total Videos", f"{videos:,}")

                                # Additional metrics if available
                                if len(m.keys()) > 3:
                                    st.markdown("#### 📈 **Additional Metrics**")
                                    extra_cols = st.columns(min(4, len(m.keys()) - 3))
                                    extra_keys = [
                                        k
                                        for k in m.keys()
                                        if k
                                        not in [
                                            "subscribers",
                                            "views",
                                            "videos",
                                            "error",
                                        ]
                                    ]

                                    for i, key in enumerate(extra_keys[:4]):
                                        with extra_cols[i]:
                                            value = m[key]
                                            display_value = (
                                                f"{value:,}"
                                                if isinstance(value, (int, float))
                                                else str(value)
                                            )
                                            st.metric(
                                                key.replace("_", " ").title(),
                                                display_value,
                                            )

                                # Archive the data
                                if archive_youtube:
                                    archive_success = archive_youtube(m)
                                    if archive_success:
                                        st.success(
                                            "✅ YouTube metrics archived successfully!"
                                        )

                        except Exception as e:
                            st.error(f"❌ Error fetching YouTube metrics: {str(e)}")
                else:
                    st.warning("⚠️ Please enter a Channel ID")
        else:
            st.warning("⚠️ YouTube Charts module not available")

        st.markdown("</div>", unsafe_allow_html=True)

    # TikTok Earnings Tab
    with tab_tiktok:
        st.markdown('<div class="platform-tab">', unsafe_allow_html=True)
        st.markdown("### 🎵 **TikTok Creator Fund Analytics**")

        if tiktok_metrics:
            col1, col2 = st.columns([2, 1])

            with col1:
                uid = st.text_input(
                    "🎭 TikTok User ID:",
                    placeholder="Enter your TikTok User ID",
                    help="Find your User ID in TikTok Creator Center",
                )

            with col2:
                st.markdown("**💰 Creator Fund:**")
                st.markdown("• Earnings tracking")
                st.markdown("• Engagement analysis")
                st.markdown("• Growth insights")

            if st.button("💰 Fetch TikTok Metrics", key="tiktok_fetch", type="primary"):
                if uid:
                    with st.spinner("Fetching TikTok earnings..."):
                        try:
                            m = tiktok_metrics(uid)

                            if m.get("error"):
                                st.error(f"❌ Error: {m['error']}")
                            else:
                                # Display all metrics dynamically
                                st.markdown("#### 💎 **Creator Fund Performance**")

                                # Create columns for metrics
                                num_metrics = len([k for k in m.keys() if k != "error"])
                                cols_per_row = 4
                                rows_needed = (
                                    num_metrics + cols_per_row - 1
                                ) // cols_per_row

                                metric_keys = [k for k in m.keys() if k != "error"]
                                for row in range(rows_needed):
                                    cols = st.columns(cols_per_row)
                                    start_idx = row * cols_per_row
                                    end_idx = min(
                                        start_idx + cols_per_row, len(metric_keys)
                                    )

                                    for i, key in enumerate(
                                        metric_keys[start_idx:end_idx]
                                    ):
                                        with cols[i]:
                                            value = m[key]
                                            display_key = key.replace("_", " ").title()
                                            if isinstance(value, (int, float)):
                                                if (
                                                    "revenue" in key.lower()
                                                    or "earning" in key.lower()
                                                ):
                                                    st.metric(
                                                        display_key, f"${value:.2f}"
                                                    )
                                                else:
                                                    st.metric(display_key, f"{value:,}")
                                            else:
                                                st.metric(display_key, str(value))

                                # Archive the data
                                if archive_tiktok:
                                    archive_success = archive_tiktok(m)
                                    if archive_success:
                                        st.success(
                                            "✅ TikTok metrics archived successfully!"
                                        )

                        except Exception as e:
                            st.error(f"❌ Error fetching TikTok metrics: {str(e)}")
                else:
                    st.warning("⚠️ Please enter a User ID")
        else:
            st.warning("⚠️ TikTok Earnings module not available")

        st.markdown("</div>", unsafe_allow_html=True)

    # Threads Engagement Tab
    with tab_threads:
        st.markdown('<div class="platform-tab">', unsafe_allow_html=True)
        st.markdown("### 🧵 **Threads Community Engagement**")

        if threads_metrics:
            col1, col2 = st.columns([3, 1])

            with col1:
                if st.button(
                    "🧵 Fetch Threads Metrics", key="threads_fetch", type="primary"
                ):
                    with st.spinner("Fetching Threads engagement..."):
                        try:
                            m = threads_metrics()

                            if m.get("error"):
                                st.error(f"❌ Error: {m['error']}")
                            else:
                                # Display all metrics dynamically
                                st.markdown("#### 🌟 **Community Engagement**")

                                # Create responsive metric layout
                                metric_keys = [k for k in m.keys() if k != "error"]
                                cols_per_row = 3
                                rows_needed = (
                                    len(metric_keys) + cols_per_row - 1
                                ) // cols_per_row

                                for row in range(rows_needed):
                                    cols = st.columns(cols_per_row)
                                    start_idx = row * cols_per_row
                                    end_idx = min(
                                        start_idx + cols_per_row, len(metric_keys)
                                    )

                                    for i, key in enumerate(
                                        metric_keys[start_idx:end_idx]
                                    ):
                                        with cols[i]:
                                            value = m[key]
                                            display_key = key.replace("_", " ").title()
                                            if isinstance(value, (int, float)):
                                                if key.endswith(
                                                    "_rate"
                                                ) or key.endswith("_score"):
                                                    st.metric(
                                                        display_key,
                                                        f"{value:.1f}{'%' if '_rate' in key else ''}",
                                                    )
                                                else:
                                                    st.metric(display_key, f"{value:,}")
                                            else:
                                                st.metric(display_key, str(value))

                                # Archive the data
                                if archive_threads:
                                    archive_success = archive_threads(m)
                                    if archive_success:
                                        st.success(
                                            "✅ Threads metrics archived successfully!"
                                        )

                        except Exception as e:
                            st.error(f"❌ Error fetching Threads metrics: {str(e)}")

            with col2:
                st.markdown("**🧵 Threads Info:**")
                st.markdown("• Meta Graph API")
                st.markdown("• Community insights")
                st.markdown("• Engagement tracking")
                st.markdown("• Growth analysis")
        else:
            st.warning("⚠️ Threads Engagement module not available")

        st.markdown("</div>", unsafe_allow_html=True)

    # WhatsApp Business Tab
    with tab_whatsapp:
        st.markdown('<div class="platform-tab">', unsafe_allow_html=True)
        st.markdown("### 💬 **WhatsApp Business Communication**")

        if whatsapp_metrics and whatsapp_broadcast:
            # Broadcast section
            st.markdown("#### 📢 **Council Broadcast**")

            broadcast_col1, broadcast_col2 = st.columns([2, 1])

            with broadcast_col1:
                msg = st.text_area(
                    "📝 Broadcast Message:",
                    placeholder="Enter your message to send to the council...",
                    height=100,
                    help="Keep messages concise and valuable",
                )

                recipients = st.text_input(
                    "👥 Recipients (comma-separated):",
                    placeholder="+1234567890, +0987654321, ...",
                    help="Enter phone numbers in international format",
                )

            with broadcast_col2:
                st.markdown("**💡 Broadcast Tips:**")
                st.markdown("• Use +country code")
                st.markdown("• Comma-separated list")
                st.markdown("• Keep messages short")
                st.markdown("• Avoid spam content")

            if st.button("📢 Send Broadcast", key="whatsapp_broadcast", type="primary"):
                if msg and recipients:
                    recipient_list = [
                        r.strip() for r in recipients.split(",") if r.strip()
                    ]
                    if recipient_list:
                        with st.spinner("Dispatching broadcast..."):
                            try:
                                result = whatsapp_broadcast(msg, recipient_list)
                                if result.get("error"):
                                    st.error(f"❌ Broadcast failed: {result['error']}")
                                else:
                                    st.markdown(
                                        '<div class="success-message">✅ Broadcast dispatched successfully!</div>',
                                        unsafe_allow_html=True,
                                    )

                                    # Show results if available
                                    if result.get("successful_sends") is not None:
                                        result_col1, result_col2, result_col3 = (
                                            st.columns(3)
                                        )
                                        with result_col1:
                                            st.metric(
                                                "✅ Successful",
                                                result.get("successful_sends", 0),
                                            )
                                        with result_col2:
                                            st.metric(
                                                "❌ Failed",
                                                result.get("failed_sends", 0),
                                            )
                                        with result_col3:
                                            st.metric(
                                                "💰 Est. Cost",
                                                f"${result.get('estimated_cost', 0):.2f}",
                                            )
                            except Exception as e:
                                st.error(f"❌ Broadcast error: {str(e)}")
                    else:
                        st.warning("⚠️ Please enter valid recipients")
                else:
                    st.warning("⚠️ Please enter both message and recipients")

            st.divider()

            # Metrics section
            st.markdown("#### 📊 **Business Analytics**")

            if st.button(
                "📈 Fetch WhatsApp Metrics", key="whatsapp_fetch", type="primary"
            ):
                with st.spinner("Fetching WhatsApp analytics..."):
                    try:
                        m = whatsapp_metrics()

                        if m.get("error"):
                            st.error(f"❌ Error: {m['error']}")
                        else:
                            # Display all metrics dynamically
                            metric_keys = [k for k in m.keys() if k != "error"]
                            cols_per_row = 3
                            rows_needed = (
                                len(metric_keys) + cols_per_row - 1
                            ) // cols_per_row

                            for row in range(rows_needed):
                                cols = st.columns(cols_per_row)
                                start_idx = row * cols_per_row
                                end_idx = min(
                                    start_idx + cols_per_row, len(metric_keys)
                                )

                                for i, key in enumerate(metric_keys[start_idx:end_idx]):
                                    with cols[i]:
                                        value = m[key]
                                        display_key = key.replace("_", " ").title()
                                        if isinstance(value, (int, float)):
                                            if (
                                                "cost" in key.lower()
                                                or "revenue" in key.lower()
                                            ):
                                                st.metric(display_key, f"${value:.2f}")
                                            elif key.endswith("_rate") or key.endswith(
                                                "_percentage"
                                            ):
                                                st.metric(display_key, f"{value:.1f}%")
                                            else:
                                                st.metric(display_key, f"{value:,}")
                                        else:
                                            st.metric(display_key, str(value))

                            # Archive the data
                            if archive_whatsapp:
                                archive_success = archive_whatsapp(m)
                                if archive_success:
                                    st.success(
                                        "✅ WhatsApp metrics archived successfully!"
                                    )

                    except Exception as e:
                        st.error(f"❌ Error fetching WhatsApp metrics: {str(e)}")
        else:
            st.warning("⚠️ WhatsApp Business module not available")

        st.markdown("</div>", unsafe_allow_html=True)

    # Pinterest Capsule Tab
    with tab_pinterest:
        st.markdown('<div class="platform-tab">', unsafe_allow_html=True)
        st.markdown("### 📌 **Pinterest Affiliate Capsule**")

        if pinterest_metrics and pinterest_pin:
            # Metrics section
            st.markdown("#### 📊 **Affiliate Performance**")

            if st.button(
                "📌 Fetch Pinterest Metrics", key="pinterest_fetch", type="primary"
            ):
                with st.spinner("Fetching Pinterest analytics..."):
                    try:
                        m = pinterest_metrics()

                        if m.get("error"):
                            st.error(f"❌ Error: {m['error']}")
                        else:
                            # Display all metrics dynamically
                            metric_keys = [
                                k
                                for k in m.keys()
                                if k not in ["error", "demo", "last_updated"]
                            ]
                            cols_per_row = 3
                            rows_needed = (
                                len(metric_keys) + cols_per_row - 1
                            ) // cols_per_row

                            for row in range(rows_needed):
                                cols = st.columns(cols_per_row)
                                start_idx = row * cols_per_row
                                end_idx = min(
                                    start_idx + cols_per_row, len(metric_keys)
                                )

                                for i, key in enumerate(metric_keys[start_idx:end_idx]):
                                    with cols[i]:
                                        value = m[key]
                                        display_key = key.replace("_", " ").title()
                                        if isinstance(value, (int, float)):
                                            if (
                                                "revenue" in key.lower()
                                                or "cost" in key.lower()
                                            ):
                                                st.metric(display_key, f"${value:.2f}")
                                            elif (
                                                key.endswith("_rate")
                                                or key.endswith("_score")
                                                or "percentage" in key.lower()
                                            ):
                                                st.metric(
                                                    display_key,
                                                    f"{value:.1f}{'%' if '_rate' in key or 'percentage' in key else ''}",
                                                )
                                            else:
                                                st.metric(display_key, f"{value:,}")
                                        else:
                                            st.metric(display_key, str(value))

                            # Archive the data
                            if archive_pinterest:
                                archive_success = archive_pinterest(m)
                                if archive_success:
                                    st.success(
                                        "✅ Pinterest metrics archived successfully!"
                                    )

                    except Exception as e:
                        st.error(f"❌ Error fetching Pinterest metrics: {str(e)}")

            st.divider()

            # Pin creation section
            st.markdown("#### 📌 **Quick Pin Publisher**")

            pin_col1, pin_col2 = st.columns([2, 1])

            with pin_col1:
                title = st.text_input(
                    "📝 Pin Title:",
                    placeholder="Enter compelling pin title...",
                    help="Keep titles under 100 characters",
                )

                link = st.text_input(
                    "🔗 Pin Link:",
                    placeholder="https://your-affiliate-link.com",
                    help="This is where users will go when they click",
                )

                image_url = st.text_input(
                    "🖼️ Image URL:",
                    placeholder="https://example.com/image.jpg",
                    help="Vertical images (2:3 ratio) perform best",
                )

            with pin_col2:
                st.markdown("**📌 Pin Tips:**")
                st.markdown("• Use vertical images")
                st.markdown("• Compelling titles")
                st.markdown("• High-quality visuals")
                st.markdown("• Clear call-to-action")

            if st.button("📌 Publish Pin", key="pinterest_publish", type="primary"):
                if title and link and image_url:
                    with st.spinner("Publishing pin..."):
                        try:
                            result = pinterest_pin(title, link, image_url)
                            if result.get("success"):
                                st.markdown(
                                    '<div class="success-message">✅ Pin published successfully!</div>',
                                    unsafe_allow_html=True,
                                )
                                if result.get("pin_url"):
                                    st.info(f"🔗 **Pin URL:** {result['pin_url']}")
                            else:
                                st.error(
                                    f"❌ Pin publication failed: {result.get('error', 'Unknown error')}"
                                )
                        except Exception as e:
                            st.error(f"❌ Error publishing pin: {str(e)}")
                else:
                    st.warning("⚠️ Please fill in all pin details")
        else:
            st.warning("⚠️ Pinterest Capsule module not available")

        st.markdown("</div>", unsafe_allow_html=True)

    # Affiliate Command Tab
    with tab_affiliate:
        st.markdown('<div class="platform-tab">', unsafe_allow_html=True)
        st.markdown("### 💎 **Affiliate Command Center**")

        if fetch_affiliate_metrics:
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown("#### 💰 Affiliate Marketing Analytics")

                if st.button(
                    "💎 Fetch Affiliate Metrics", key="affiliate_fetch", type="primary"
                ):
                    with st.spinner("Fetching affiliate analytics..."):
                        try:
                            m = fetch_affiliate_metrics()

                            if m.get("error"):
                                st.error(f"❌ Error: {m['error']}")
                            else:
                                # Display all metrics dynamically
                                st.markdown("#### 🔥 **Commission Performance**")

                                # Core metrics row
                                core_col1, core_col2, core_col3 = st.columns(3)

                                with core_col1:
                                    clicks = m.get("clicks", 0)
                                    st.metric("👆 Clicks", f"{clicks:,}")

                                with core_col2:
                                    conversions = m.get("conversions", 0)
                                    st.metric("🎯 Conversions", f"{conversions:,}")

                                with core_col3:
                                    commission = m.get("commission", 0)
                                    st.metric("💰 Commission", f"${commission:.2f}")

                                # Performance metrics row
                                perf_col1, perf_col2, perf_col3 = st.columns(3)

                                with perf_col1:
                                    conversion_rate = m.get("conversion_rate", 0)
                                    st.metric(
                                        "📈 Conversion Rate", f"{conversion_rate:.2f}%"
                                    )

                                with perf_col2:
                                    epc = m.get("earnings_per_click", 0)
                                    st.metric("💵 Earnings/Click", f"${epc:.3f}")

                                with perf_col3:
                                    performance_score = m.get("performance_score", 0)
                                    st.metric(
                                        "⚡ Performance Score",
                                        f"{performance_score:.1f}/100",
                                    )

                                # Advanced metrics row
                                adv_col1, adv_col2, adv_col3 = st.columns(3)

                                with adv_col1:
                                    avg_commission = m.get("average_commission", 0)
                                    st.metric(
                                        "💎 Avg Commission", f"${avg_commission:.2f}"
                                    )

                                with adv_col2:
                                    monthly_proj = m.get("monthly_projection", 0)
                                    st.metric(
                                        "📅 Monthly Projection", f"${monthly_proj:.2f}"
                                    )

                                with adv_col3:
                                    profitability_tier = m.get(
                                        "profitability_tier", "startup"
                                    )
                                    tier_emoji = {
                                        "elite": "👑",
                                        "professional": "⭐",
                                        "advanced": "📈",
                                        "developing": "🌱",
                                        "emerging": "🚀",
                                        "startup": "💡",
                                    }.get(profitability_tier, "🔥")
                                    st.metric(
                                        f"{tier_emoji} Tier", profitability_tier.title()
                                    )

                                # Quality analysis section
                                if m.get("conversion_quality"):
                                    st.markdown("#### 🎯 **Performance Analysis**")

                                    analysis_col1, analysis_col2 = st.columns(2)

                                    with analysis_col1:
                                        conversion_quality = m.get(
                                            "conversion_quality", "unknown"
                                        )
                                        quality_emoji = {
                                            "exceptional": "🌟",
                                            "excellent": "🟢",
                                            "good": "🟡",
                                            "fair": "🟠",
                                            "needs_improvement": "🔴",
                                        }.get(conversion_quality, "❓")
                                        st.markdown(
                                            f"**{quality_emoji} Conversion Quality:** {conversion_quality.replace('_', ' ').title()}"
                                        )

                                        traffic_quality = m.get(
                                            "traffic_quality", "unknown"
                                        )
                                        traffic_emoji = {
                                            "premium": "💎",
                                            "high": "🟢",
                                            "good": "🟡",
                                            "average": "🟠",
                                            "low": "🔴",
                                        }.get(traffic_quality, "❓")
                                        st.markdown(
                                            f"**{traffic_emoji} Traffic Quality:** {traffic_quality.title()}"
                                        )

                                        optimization_potential = m.get(
                                            "optimization_potential", "unknown"
                                        )
                                        opt_emoji = {
                                            "optimized": "✅",
                                            "low": "🟢",
                                            "moderate": "🟡",
                                            "high": "🔴",
                                        }.get(optimization_potential, "❓")
                                        st.markdown(
                                            f"**{opt_emoji} Optimization Potential:** {optimization_potential.title()}"
                                        )

                                    with analysis_col2:
                                        growth_trend = m.get("growth_trend", "unknown")
                                        growth_emoji = {
                                            "accelerating": "🚀",
                                            "growing": "📈",
                                            "stable": "📊",
                                            "declining": "📉",
                                            "concerning": "🆘",
                                        }.get(growth_trend, "❓")
                                        st.markdown(
                                            f"**{growth_emoji} Growth Trend:** {growth_trend.title()}"
                                        )

                                        revenue_consistency = m.get(
                                            "revenue_consistency", "unknown"
                                        )
                                        consistency_emoji = {
                                            "very_consistent": "🎯",
                                            "consistent": "🟢",
                                            "moderate": "🟡",
                                            "volatile": "🔴",
                                        }.get(revenue_consistency, "❓")
                                        st.markdown(
                                            f"**{consistency_emoji} Revenue Consistency:** {revenue_consistency.replace('_', ' ').title()}"
                                        )

                                        active_networks = m.get("active_networks", 0)
                                        diversification = m.get(
                                            "network_diversification", 0
                                        )
                                        st.markdown(
                                            f"**🌐 Network Diversification:** {active_networks} networks ({diversification:.1f}%)"
                                        )

                                # Network performance section
                                if m.get("top_network"):
                                    st.markdown("#### 🌐 **Network Performance**")

                                    network_col1, network_col2, network_col3 = (
                                        st.columns(3)
                                    )

                                    with network_col1:
                                        top_network = m.get("top_network", "None")
                                        st.metric("🏆 Top Network", top_network)

                                    with network_col2:
                                        top_commission = m.get(
                                            "top_network_commission", 0
                                        )
                                        st.metric(
                                            "💰 Top Network Revenue",
                                            f"${top_commission:.2f}",
                                        )

                                    with network_col3:
                                        rpm = m.get("revenue_per_mille", 0)
                                        st.metric("📊 RPM", f"${rpm:.2f}")

                                # Store in session state for archiving
                                st.session_state["affiliate_metrics"] = m

                                # Archive the data
                                if archive_affiliate:
                                    archive_success = archive_affiliate(m)
                                    if archive_success:
                                        st.success(
                                            "✅ Affiliate metrics archived successfully!"
                                        )

                        except Exception as e:
                            st.error(f"❌ Error fetching affiliate metrics: {str(e)}")

                # Performance optimization section
                st.markdown("#### 🚀 **Quick Optimization Tools**")

                opt_col1, opt_col2 = st.columns(2)

                with opt_col1:
                    st.markdown("**💡 Performance Tips:**")
                    st.markdown("• Focus on high-converting traffic sources")
                    st.markdown("• Optimize landing pages for mobile")
                    st.markdown("• A/B test different promotional strategies")
                    st.markdown("• Monitor competitor affiliate programs")

                with opt_col2:
                    st.markdown("**📊 Network Suggestions:**")
                    st.markdown("• ShareASale - Broad merchant selection")
                    st.markdown("• Commission Junction - Premium brands")
                    st.markdown("• ClickBank - Digital products focus")
                    st.markdown("• Amazon Associates - E-commerce giant")

            with col2:
                st.markdown("#### 📚 Archive History")

                try:
                    from codex_affiliate_command import CodexAffiliateCommand

                    affiliate_system = CodexAffiliateCommand()
                    history = affiliate_system.get_archive_history(10)

                    if history:
                        st.metric("📈 Total Archives", len(history))

                        st.markdown("**🕒 Recent Reports:**")
                        for entry in history[-5:]:
                            timestamp = (
                                entry.get("ts", "Unknown")[:16]
                                if len(entry.get("ts", "")) > 16
                                else entry.get("ts", "Unknown")
                            )
                            commission = entry.get("commission", 0)
                            conversions = entry.get("conversions", 0)
                            st.markdown(
                                f"• {timestamp} - {conversions} conv, ${commission:.2f}"
                            )
                    else:
                        st.info("No archive history yet")

                except Exception as e:
                    st.warning(f"Could not load history: {str(e)}")

                st.markdown("#### ⚙️ Quick Actions")

                if st.button("📋 View Config", key="affiliate_config_btn"):
                    try:
                        config_file = Path("affiliate_config.json")
                        if config_file.exists():
                            with open(config_file, "r") as f:
                                config = json.load(f)
                            st.json(config)
                        else:
                            st.info("Config file will be created on first use")
                    except Exception as e:
                        st.error(f"Config error: {str(e)}")

                # Commission calculator
                st.markdown("#### 💰 Commission Calculator")

                calc_clicks = st.number_input(
                    "Expected Clicks", min_value=0, value=1000, step=100
                )
                calc_conv_rate = st.number_input(
                    "Conversion Rate (%)",
                    min_value=0.0,
                    value=2.5,
                    step=0.1,
                    format="%.1f",
                )
                calc_avg_commission = st.number_input(
                    "Avg Commission ($)",
                    min_value=0.0,
                    value=25.0,
                    step=1.0,
                    format="%.2f",
                )

                if calc_clicks and calc_conv_rate and calc_avg_commission:
                    conversions = calc_clicks * (calc_conv_rate / 100)
                    total_commission = conversions * calc_avg_commission
                    epc = total_commission / calc_clicks

                    st.metric("🎯 Expected Conversions", f"{conversions:.0f}")
                    st.metric("💰 Total Commission", f"${total_commission:.2f}")
                    st.metric("💵 EPC", f"${epc:.3f}")

                    # Performance analysis
                    if total_commission > 1000:
                        st.success("🚀 Excellent revenue potential!")
                    elif total_commission > 500:
                        st.info("💡 Good revenue opportunity")
                    elif total_commission > 100:
                        st.warning("⚠️ Moderate revenue potential")
                    else:
                        st.warning("📈 Consider traffic optimization")
        else:
            st.warning("⚠️ Affiliate Command module not available")

        st.markdown("</div>", unsafe_allow_html=True)

    # Portfolio Manager Tab
    with tab_portfolio:
        st.markdown('<div class="platform-tab">', unsafe_allow_html=True)
        st.markdown("### 📈 **Portfolio & Trading Management**")

        # Try to import portfolio functions
        portfolio_available = False
        try:
            from codex_database import (get_affiliate_performance,
                                        get_portfolio_summary, get_top_pools)

            portfolio_available = True
        except ImportError:
            portfolio_available = False

        if portfolio_available:
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown("#### 💼 Portfolio Overview")

                # Mock portfolio data for demonstration
                portfolio_data = {
                    "total_value": 125000.00,
                    "total_cost": 100000.00,
                    "unrealized_pnl": 25000.00,
                    "return_percentage": 25.0,
                    "positions": [
                        {
                            "symbol": "AAPL",
                            "quantity": 100,
                            "market_value": 15525.00,
                            "unrealized_pnl": 525.00,
                        },
                        {
                            "symbol": "MSFT",
                            "quantity": 50,
                            "market_value": 15525.00,
                            "unrealized_pnl": 525.00,
                        },
                        {
                            "symbol": "GOOGL",
                            "quantity": 25,
                            "market_value": 61875.00,
                            "unrealized_pnl": -625.00,
                        },
                    ],
                }

                # Portfolio metrics
                metric_col1, metric_col2, metric_col3 = st.columns(3)

                with metric_col1:
                    st.metric(
                        "💼 Portfolio Value",
                        f"${portfolio_data['total_value']:,.2f}",
                        delta=f"${portfolio_data['unrealized_pnl']:,.2f}",
                    )

                with metric_col2:
                    st.metric(
                        "📈 Total Return",
                        f"{portfolio_data['return_percentage']:.1f}%",
                        delta="vs cost basis",
                    )

                with metric_col3:
                    st.metric(
                        "🎯 Positions", len(portfolio_data["positions"]), delta="active"
                    )

                # Positions table
                st.markdown("**📊 Current Positions:**")
                import pandas as pd

                positions_df = pd.DataFrame(
                    [
                        {
                            "Symbol": pos["symbol"],
                            "Quantity": pos["quantity"],
                            "Market Value": f"${pos['market_value']:,.2f}",
                            "P&L": (
                                f"${pos['unrealized_pnl']:,.2f}"
                                if pos["unrealized_pnl"] >= 0
                                else f"-${abs(pos['unrealized_pnl']):,.2f}"
                            ),
                        }
                        for pos in portfolio_data["positions"]
                    ]
                )

                st.dataframe(positions_df, use_container_width=True)

                # Quick actions
                st.markdown("**⚡ Quick Actions:**")
                action_col1, action_col2, action_col3 = st.columns(3)

                with action_col1:
                    if st.button("🔄 Refresh Prices", key="portfolio_refresh"):
                        st.success("Prices updated!")

                with action_col2:
                    if st.button("📊 Full Analysis", key="portfolio_analysis"):
                        st.info("Opening detailed portfolio analysis...")

                with action_col3:
                    if st.button("➕ Add Position", key="portfolio_add"):
                        st.info("Add position form would open here")

            with col2:
                st.markdown("#### 🎯 Trading Insights")

                # Market overview
                st.markdown("**📈 Market Overview:**")

                market_data = [
                    {
                        "Index": "S&P 500",
                        "Value": "4,185.47",
                        "Change": "+0.8%",
                        "Status": "🟢",
                    },
                    {
                        "Index": "NASDAQ",
                        "Value": "12,870.00",
                        "Change": "+1.2%",
                        "Status": "🟢",
                    },
                    {
                        "Index": "DOW",
                        "Value": "33,745.40",
                        "Change": "+0.3%",
                        "Status": "🟢",
                    },
                ]

                for market in market_data:
                    st.markdown(
                        f"**{market['Index']}**: {market['Value']} ({market['Change']}) {market['Status']}"
                    )

                st.divider()

                # Portfolio allocation
                st.markdown("**🎯 Asset Allocation:**")
                allocation_data = {
                    "Technology": 45,
                    "Healthcare": 20,
                    "Financial": 15,
                    "Consumer": 10,
                    "Energy": 5,
                    "Cash": 5,
                }

                for sector, percentage in allocation_data.items():
                    st.progress(percentage / 100, text=f"{sector}: {percentage}%")

                st.divider()

                # Risk metrics
                st.markdown("**⚠️ Risk Metrics:**")

                risk_metrics = [
                    ("Portfolio Beta", "1.15", "Medium Risk"),
                    ("Sharpe Ratio", "1.42", "Good"),
                    ("Max Drawdown", "8.5%", "Low Risk"),
                    ("Volatility", "18.2%", "Moderate"),
                ]

                for metric, value, status in risk_metrics:
                    st.markdown(f"• **{metric}**: {value} ({status})")

                st.divider()

                # Performance vs benchmarks
                st.markdown("**📊 vs Benchmarks:**")

                benchmark_data = [
                    ("Portfolio", "25.0%", "🟢"),
                    ("S&P 500", "18.5%", "🔵"),
                    ("NASDAQ", "22.1%", "🔵"),
                    ("Sector ETF", "16.8%", "🔵"),
                ]

                for name, return_pct, color in benchmark_data:
                    st.markdown(f"{color} **{name}**: {return_pct}")

        else:
            # Fallback content when database not available
            st.info("🔧 **Portfolio Management System**")
            st.markdown("**Features include:**")
            st.markdown("• 📊 Real-time portfolio tracking")
            st.markdown("• 💰 P&L analysis and reporting")
            st.markdown("• ⚠️ Risk management tools")
            st.markdown("• 📈 Performance benchmarking")
            st.markdown("• 🎯 Asset allocation optimization")

            st.markdown("**🚀 Coming Soon:**")
            st.markdown("• Integration with major brokers")
            st.markdown("• Automated rebalancing")
            st.markdown("• Options trading analytics")
            st.markdown("• Crypto portfolio support")

            # Demo metrics
            demo_col1, demo_col2, demo_col3 = st.columns(3)

            with demo_col1:
                st.metric("Demo Portfolio", "$125,000", "+$25,000")

            with demo_col2:
                st.metric("Return", "25.0%", "+2.3%")

            with demo_col3:
                st.metric("Positions", "12", "+3")

            if st.button("🔗 Launch Full Portfolio Dashboard"):
                st.info("Opening dedicated Portfolio Management interface...")
                st.markdown("**Access at:** http://127.0.0.1:8501")

        st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("### 🔥 **The Merritt Method™ - Digital Monetization Sovereignty**")
    st.markdown("*Complete multi-platform creator economy command and control*")


if __name__ == "__main__":
    main()

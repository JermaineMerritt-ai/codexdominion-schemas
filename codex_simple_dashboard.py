"""
🔥 CODEX DOMINION SIMPLE LAUNCHER 👑
Bulletproof dashboard that works with available dependencies

The Merritt Method™ - Guaranteed Digital Sovereignty
"""

import streamlit as st
import json
import requests
from datetime import datetime
from pathlib import Path
import traceback

# Safe imports - only import what's available
def safe_import(module_name, class_name=None):
    """Safely import modules and return None if not available"""
    try:
        module = __import__(module_name)
        if class_name:
            return getattr(module, class_name)
        return module
    except ImportError:
        return None

# Try to import integrations
try:
    from codex_dawn_dispatch import CodexDawnDispatch, dawn_dispatch
    DAWN_AVAILABLE = True
except ImportError:
    DAWN_AVAILABLE = False

# Check for other integrations
WOOCOMMERCE_AVAILABLE = False
TWITTER_AVAILABLE = False
BUFFER_AVAILABLE = False
YOUTUBE_AVAILABLE = False

try:
    from codex_woocommerce_sync import CodexWooCommerceSync
    WOOCOMMERCE_AVAILABLE = True
except ImportError:
    pass

try:
    from codex_twitter_proclamation import CodexTwitterProclaimer
    TWITTER_AVAILABLE = True
except ImportError:
    pass

try:
    from codex_buffer_proclamation import CodexBufferProclaimer
    BUFFER_AVAILABLE = True
except ImportError:
    pass

try:
    from codex_youtube_charts import CodexYouTubeCharts, youtube_metrics, archive_youtube, get_youtube_analytics
    YOUTUBE_AVAILABLE = True
except ImportError:
    pass

try:
    from codex_tiktok_earnings import CodexTikTokEarnings, tiktok_metrics, archive_tiktok, get_tiktok_earnings
    TIKTOK_AVAILABLE = True
except ImportError:
    TIKTOK_AVAILABLE = False

try:
    from codex_threads_engagement import CodexThreadsEngagement, threads_metrics, archive_threads, get_threads_engagement
    THREADS_AVAILABLE = True
except ImportError:
    THREADS_AVAILABLE = False

try:
    from codex_whatsapp_business import CodexWhatsAppBusiness, whatsapp_metrics, whatsapp_broadcast, archive_whatsapp, get_whatsapp_business_summary
    WHATSAPP_AVAILABLE = True
except ImportError:
    WHATSAPP_AVAILABLE = False

try:
    from codex_pinterest_capsule import CodexPinterestCapsule, pinterest_metrics, pinterest_pin, pinterest_batch_pin, archive_pinterest, get_pinterest_capsule_summary
    PINTEREST_AVAILABLE = True
except ImportError:
    PINTEREST_AVAILABLE = False

def load_ledger():
    """Load codex ledger with error handling"""
    try:
        ledger_file = Path("codex_ledger.json")
        if ledger_file.exists() and ledger_file.stat().st_size > 0:
            with open(ledger_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {}
    except Exception as e:
        st.warning(f"Could not load ledger: {str(e)}")
        return {}

def main():
    st.set_page_config(
        page_title="🔥 Codex Dominion - Simple Dashboard",
        page_icon="👑",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Apply cosmic styling
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0c1445 0%, #1a237e 50%, #000051 100%);
        color: #ffffff;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #ffd700 !important;
        font-weight: bold;
        background: rgba(255, 215, 0, 0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #1a237e, #3949ab);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #ffd700;
        margin: 10px 0;
    }
    .success-box {
        background: rgba(76, 175, 80, 0.2);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #4caf50;
    }
    .error-box {
        background: rgba(244, 67, 54, 0.2);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #f44336;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sacred Header
    st.markdown("""
    <div style='text-align: center; background: linear-gradient(90deg, #ffd700, #ffeb3b); padding: 20px; border-radius: 15px; margin-bottom: 30px;'>
        <h1 style='color: #000051; font-size: 2.5em; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
            🔥 CODEX DOMINION 👑
        </h1>
        <p style='color: #1a237e; font-size: 1.2em; margin: 10px 0 0 0; font-weight: bold;'>
            Simple Digital Sovereignty Dashboard
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Service status sidebar
    st.sidebar.markdown("### 🔧 Service Status")
    st.sidebar.success("🏛️ Core Dashboard: Active")
    
    if DAWN_AVAILABLE:
        st.sidebar.success("🌅 Dawn Dispatch: Ready")
    else:
        st.sidebar.error("🌅 Dawn Dispatch: Not Available")
    
    if WOOCOMMERCE_AVAILABLE:
        st.sidebar.success("🛒 WooCommerce: Available")
    else:
        st.sidebar.warning("🛒 WooCommerce: Not Configured")
    
    if TWITTER_AVAILABLE:
        st.sidebar.success("🐦 Twitter: Available")
    else:
        st.sidebar.warning("🐦 Twitter: Not Configured")
    
    if BUFFER_AVAILABLE:
        st.sidebar.success("📱 Buffer: Available")
    else:
        st.sidebar.warning("📱 Buffer: Not Configured")
    
    if YOUTUBE_AVAILABLE:
        st.sidebar.success("📺 YouTube: Available")
    else:
        st.sidebar.warning("📺 YouTube: Not Configured")
    
    if TIKTOK_AVAILABLE:
        st.sidebar.success("🎵 TikTok: Available")
    else:
        st.sidebar.warning("🎵 TikTok: Not Configured")
    
    if THREADS_AVAILABLE:
        st.sidebar.success("🧵 Threads: Available")
    else:
        st.sidebar.warning("🧵 Threads: Not Configured")
    
    if WHATSAPP_AVAILABLE:
        st.sidebar.success("💬 WhatsApp: Available")
    else:
        st.sidebar.warning("💬 WhatsApp: Not Configured")
    
    if PINTEREST_AVAILABLE:
        st.sidebar.success("📌 Pinterest: Available")
    else:
        st.sidebar.warning("📌 Pinterest: Not Configured")

    # Main tabs - only show available features
    available_tabs = ["🏛️ Dominion Central", "📊 System Status"]
    
    if DAWN_AVAILABLE:
        available_tabs.insert(1, "🌅 Dawn Dispatch")
    
    if YOUTUBE_AVAILABLE:
        available_tabs.insert(-1, "📺 YouTube Charts")
    
    if TIKTOK_AVAILABLE:
        available_tabs.insert(-1, "🎵 TikTok Earnings")
    
    if THREADS_AVAILABLE:
        available_tabs.insert(-1, "🧵 Threads Engagement")
    
    if WHATSAPP_AVAILABLE:
        available_tabs.insert(-1, "💬 WhatsApp Business")
    
    if PINTEREST_AVAILABLE:
        available_tabs.insert(-1, "📌 Pinterest Capsule")
    
    tabs = st.tabs(available_tabs)

    with tabs[0]:  # Dominion Central
        st.markdown("### 🏛️ **DOMINION CENTRAL COMMAND**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("🔥 Active Systems", len([x for x in [DAWN_AVAILABLE, WOOCOMMERCE_AVAILABLE, TWITTER_AVAILABLE, BUFFER_AVAILABLE, YOUTUBE_AVAILABLE, TIKTOK_AVAILABLE, THREADS_AVAILABLE, WHATSAPP_AVAILABLE, PINTEREST_AVAILABLE] if x]))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("👑 Dashboard Status", "OPERATIONAL")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            ledger = load_ledger()
            st.metric("📜 Ledger Entries", len(ledger) if isinstance(ledger, dict) else 0)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("#### 📜 Recent System Activity")
        
        # Try to load recent archives
        try:
            archive_file = Path("completed_archives.json")
            if archive_file.exists():
                with open(archive_file, 'r', encoding='utf-8') as f:
                    archives = json.load(f)
                
                if archives:
                    st.markdown("**🌅 Recent Dawn Dispatches:**")
                    for archive in archives[-3:]:
                        timestamp = archive.get('timestamp', 'Unknown')[:19]
                        st.markdown(f"• {timestamp} - Dawn Dispatch completed")
                else:
                    st.info("No recent activity found")
            else:
                st.info("No archive file found - run a Dawn Dispatch to create activity history")
        except Exception as e:
            st.warning(f"Could not load activity: {str(e)}")

    # Dawn Dispatch tab (only if available)
    if DAWN_AVAILABLE:
        tab_index = 1
        with tabs[tab_index]:
            st.markdown("### 🌅 **DAWN DISPATCH SYSTEM**")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("#### 🚀 Generate Dawn Report")
                
                if st.button("🌅 Execute Dawn Dispatch", key="dawn_execute_btn", type="primary"):
                    with st.spinner("Generating comprehensive system report..."):
                        try:
                            result = dawn_dispatch()
                            
                            if result.get("success"):
                                st.markdown('<div class="success-box">✅ Dawn Dispatch completed successfully!</div>', unsafe_allow_html=True)
                                
                                # Show the report
                                if result.get("report"):
                                    st.markdown("#### 📜 Dawn Report")
                                    st.code(result["report"], language="text")
                                
                            else:
                                st.markdown(f'<div class="error-box">❌ Dawn Dispatch failed: {result.get("error")}</div>', unsafe_allow_html=True)
                        except Exception as e:
                            st.markdown(f'<div class="error-box">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
                
                # Quick metrics if Dawn Dispatch is available
                if st.button("📊 Quick System Check", key="dawn_quick_check_btn"):
                    try:
                        dawn_system = CodexDawnDispatch()
                        
                        col_a, col_b, col_c = st.columns(3)
                        
                        with col_a:
                            system_status = dawn_system.get_system_status()
                            health_score = system_status.get('health_score', 0)
                            st.metric("⚡ System Health", f"{health_score:.1f}%")
                        
                        with col_b:
                            ledger_data = dawn_system.get_ledger_updates()
                            st.metric("📜 Ledger Status", ledger_data.get('status', 'Unknown'))
                        
                        with col_c:
                            services = system_status.get('services', {})
                            online_count = sum(1 for v in services.values() if v)
                            st.metric("🔧 Services Online", f"{online_count}/{len(services)}")
                        
                    except Exception as e:
                        st.error(f"Quick check failed: {str(e)}")
            
            with col2:
                st.markdown("#### 📚 Recent Archives")
                
                try:
                    archive_file = Path("completed_archives.json")
                    if archive_file.exists():
                        with open(archive_file, 'r', encoding='utf-8') as f:
                            archives = json.load(f)
                        
                        if archives:
                            st.metric("📈 Total Archives", len(archives))
                            
                            st.markdown("**🕒 Recent Reports:**")
                            for archive in archives[-5:]:
                                timestamp = archive.get('timestamp', 'Unknown')[:16]
                                st.markdown(f"• {timestamp}")
                        else:
                            st.info("No archives yet")
                    else:
                        st.info("No archive file found")
                        
                except Exception as e:
                    st.warning(f"Could not load archives: {str(e)}")

    # YouTube Charts tab (only if available)
    if YOUTUBE_AVAILABLE:
        youtube_tab_index = -2 if len(available_tabs) > 2 else 2  # Before System Status
        with tabs[youtube_tab_index]:
            st.markdown("### 📺 **YOUTUBE CHARTS SYSTEM**")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("#### 🎥 Channel Analytics")
                
                # Channel ID input
                channel_id = st.text_input(
                    "🔗 YouTube Channel ID:",
                    placeholder="Enter your YouTube Channel ID",
                    help="Find your Channel ID in YouTube Studio under Settings > Channel"
                )
                
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button("📊 Get Analytics", key="youtube_get_btn", type="primary", disabled=not channel_id):
                        if channel_id:
                            with st.spinner("Fetching YouTube analytics..."):
                                try:
                                    analytics = get_youtube_analytics(channel_id)
                                    
                                    if analytics.get("error"):
                                        st.error(f"❌ Error: {analytics['error']}")
                                    else:
                                        st.success("✅ Analytics retrieved successfully!")
                                        
                                        # Store in session state for display
                                        st.session_state['youtube_analytics'] = analytics
                                        
                                except Exception as e:
                                    st.error(f"❌ Error fetching analytics: {str(e)}")
                
                with col_b:
                    if st.button("💾 Archive Current", key="youtube_archive_btn", disabled=not st.session_state.get('youtube_analytics')):
                        try:
                            if st.session_state.get('youtube_analytics'):
                                success = archive_youtube(st.session_state['youtube_analytics'])
                                if success:
                                    st.success("✅ Archived successfully!")
                                else:
                                    st.error("❌ Archive failed")
                        except Exception as e:
                            st.error(f"❌ Archive error: {str(e)}")
                
                with col_c:
                    if st.button("🔄 Test Connection", key="youtube_test_btn"):
                        try:
                            youtube_system = CodexYouTubeCharts()
                            if youtube_system.test_connection():
                                st.success("✅ API Connected!")
                            else:
                                st.error("❌ Connection Failed")
                        except Exception as e:
                            st.error(f"❌ Test failed: {str(e)}")
                
                # Display analytics if available
                if st.session_state.get('youtube_analytics'):
                    analytics = st.session_state['youtube_analytics']
                    
                    st.markdown("#### 📈 **Channel Metrics**")
                    
                    # Main metrics row
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    
                    with metric_col1:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        subscribers = analytics.get('subscribers', 0)
                        growth = analytics.get('subscriber_growth', 0)
                        st.metric("👥 Subscribers", f"{subscribers:,}", delta=growth if growth != 0 else None)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with metric_col2:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        views = analytics.get('views', 0)
                        view_growth = analytics.get('view_growth', 0)
                        st.metric("👀 Total Views", f"{views:,}", delta=view_growth if view_growth != 0 else None)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with metric_col3:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        videos = analytics.get('videos', 0)
                        video_growth = analytics.get('video_growth', 0)
                        st.metric("🎬 Total Videos", f"{videos:,}", delta=video_growth if video_growth != 0 else None)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with metric_col4:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        score = analytics.get('channel_score', 0)
                        st.metric("⭐ Channel Score", f"{score}/100")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Additional metrics row
                    metric_col5, metric_col6, metric_col7, metric_col8 = st.columns(4)
                    
                    with metric_col5:
                        avg_views = analytics.get('avg_views_per_video', 0)
                        st.metric("📊 Avg Views/Video", f"{avg_views:,}")
                    
                    with metric_col6:
                        engagement = analytics.get('engagement_rate', 0)
                        st.metric("💬 Engagement Rate", f"{engagement}%")
                    
                    with metric_col7:
                        views_per_sub = analytics.get('views_per_subscriber', 0)
                        st.metric("🔄 Views/Subscriber", f"{views_per_sub:.1f}")
                    
                    with metric_col8:
                        trend = analytics.get('trend_direction', 'Unknown')
                        trend_emoji = {"growing": "📈", "declining": "📉", "stable": "📊"}.get(trend, "❓")
                        st.metric("📈 Trend", f"{trend_emoji} {trend.title()}")
                    
                    # Channel info
                    if analytics.get('channel_title'):
                        st.markdown("#### 📺 **Channel Information**")
                        
                        info_col1, info_col2 = st.columns(2)
                        
                        with info_col1:
                            st.markdown(f"**🎯 Channel:** {analytics.get('channel_title', 'Unknown')}")
                            st.markdown(f"**🌍 Country:** {analytics.get('country', 'Not specified')}")
                            st.markdown(f"**🔗 Custom URL:** {analytics.get('custom_url', 'Not set')}")
                        
                        with info_col2:
                            created = analytics.get('created_date', '')
                            if created:
                                created_date = created[:10] if len(created) > 10 else created
                                st.markdown(f"**📅 Created:** {created_date}")
                            
                            growth_rate = analytics.get('growth_rate', 0)
                            st.markdown(f"**📈 Growth Rate:** {growth_rate}%")
                            
                            last_updated = analytics.get('last_updated', '')
                            if last_updated:
                                updated_time = last_updated[11:19] if len(last_updated) > 19 else 'Unknown'
                                st.markdown(f"**⏰ Last Updated:** {updated_time}")
                    
                    # Recent videos
                    if analytics.get('recent_videos'):
                        st.markdown("#### 🎬 **Recent Videos Performance**")
                        
                        recent_videos = analytics.get('recent_videos', [])[:5]  # Show top 5
                        
                        for i, video in enumerate(recent_videos):
                            with st.expander(f"🎥 {video.get('title', 'Unknown Title')[:60]}..."):
                                video_col1, video_col2, video_col3 = st.columns(3)
                                
                                with video_col1:
                                    st.metric("👀 Views", f"{video.get('views', 0):,}")
                                
                                with video_col2:
                                    st.metric("👍 Likes", f"{video.get('likes', 0):,}")
                                
                                with video_col3:
                                    st.metric("💬 Comments", f"{video.get('comments', 0):,}")
                                
                                published = video.get('published_at', '')
                                if published:
                                    pub_date = published[:10] if len(published) > 10 else published
                                    st.markdown(f"**📅 Published:** {pub_date}")
            
            with col2:
                st.markdown("#### 📚 Archive History")
                
                try:
                    youtube_system = CodexYouTubeCharts()
                    history = youtube_system.get_archive_history(10)
                    
                    if history:
                        st.metric("📈 Total Archives", len(history))
                        
                        st.markdown("**🕒 Recent Reports:**")
                        for entry in history[-5:]:
                            timestamp = entry.get('ts', 'Unknown')[:16] if len(entry.get('ts', '')) > 16 else entry.get('ts', 'Unknown')
                            subscribers = entry.get('subscribers', 0)
                            st.markdown(f"• {timestamp} - {subscribers:,} subs")
                    else:
                        st.info("No archive history yet")
                        
                except Exception as e:
                    st.warning(f"Could not load history: {str(e)}")
                
                st.markdown("#### ⚙️ Quick Actions")
                
                if st.button("📋 View Config", key="youtube_config_btn"):
                    try:
                        config_file = Path("youtube_config.json")
                        if config_file.exists():
                            with open(config_file, 'r') as f:
                                config = json.load(f)
                            st.json(config)
                        else:
                            st.info("Config file will be created on first use")
                    except Exception as e:
                        st.error(f"Config error: {str(e)}")

    # TikTok Earnings tab (only if available)
    if TIKTOK_AVAILABLE:
        tiktok_tab_index = -2 if len(available_tabs) > 2 else 2  # Before System Status
        with tabs[tiktok_tab_index]:
            st.markdown("### 🎵 **TIKTOK EARNINGS SYSTEM**")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("#### 💰 Creator Program Analytics")
                
                # User ID input
                user_id = st.text_input(
                    "👤 TikTok User ID:",
                    placeholder="Enter your TikTok User ID",
                    help="Find your User ID in TikTok Creator Studio or third-party analytics tools"
                )
                
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button("💰 Get Earnings", key="tiktok_get_btn", type="primary", disabled=not user_id):
                        if user_id:
                            with st.spinner("Fetching TikTok earnings analytics..."):
                                try:
                                    earnings = get_tiktok_earnings(user_id)
                                    
                                    if earnings.get("error"):
                                        st.error(f"❌ Error: {earnings['error']}")
                                    else:
                                        st.success("✅ Earnings data retrieved successfully!")
                                        
                                        # Store in session state for display
                                        st.session_state['tiktok_earnings'] = earnings
                                        
                                except Exception as e:
                                    st.error(f"❌ Error fetching earnings: {str(e)}")
                
                with col_b:
                    if st.button("💾 Archive Current", key="tiktok_archive_btn", disabled=not st.session_state.get('tiktok_earnings')):
                        try:
                            if st.session_state.get('tiktok_earnings'):
                                success = archive_tiktok(st.session_state['tiktok_earnings'])
                                if success:
                                    st.success("✅ Archived successfully!")
                                else:
                                    st.error("❌ Archive failed")
                        except Exception as e:
                            st.error(f"❌ Archive error: {str(e)}")
                
                with col_c:
                    if st.button("🔄 Test Connection", key="tiktok_test_btn"):
                        try:
                            tiktok_system = CodexTikTokEarnings()
                            if tiktok_system.test_connection():
                                st.success("✅ API Connected!")
                            else:
                                st.warning("⚠️ Using Demo Data")
                        except Exception as e:
                            st.warning(f"⚠️ Using Demo Mode: {str(e)}")
                
                # Display earnings if available
                if st.session_state.get('tiktok_earnings'):
                    earnings = st.session_state['tiktok_earnings']
                    
                    st.markdown("#### 💰 **Earnings Dashboard**")
                    
                    # Main earnings metrics row
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    
                    with metric_col1:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        total_earnings = earnings.get('payouts', 0)
                        earnings_growth = earnings.get('earnings_growth', 0)
                        st.metric("💰 Total Earnings", f"${total_earnings:.2f}", delta=f"${earnings_growth:.2f}" if earnings_growth != 0 else None)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with metric_col2:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        followers = earnings.get('followers', 0)
                        follower_growth = earnings.get('follower_growth', 0)
                        st.metric("👥 Followers", f"{followers:,}", delta=follower_growth if follower_growth != 0 else None)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with metric_col3:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        views = earnings.get('views', 0)
                        view_growth = earnings.get('view_growth', 0)
                        st.metric("👀 Total Views", f"{views:,}", delta=view_growth if view_growth != 0 else None)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with metric_col4:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        score = earnings.get('creator_score', 0)
                        st.metric("⭐ Creator Score", f"{score}/100")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Revenue breakdown row
                    metric_col5, metric_col6, metric_col7, metric_col8 = st.columns(4)
                    
                    with metric_col5:
                        creator_fund = earnings.get('creator_fund', 0)
                        st.metric("🏆 Creator Fund", f"${creator_fund:.2f}")
                    
                    with metric_col6:
                        live_gifts = earnings.get('live_gifts', 0)
                        st.metric("🎁 Live Gifts", f"${live_gifts:.2f}")
                    
                    with metric_col7:
                        partnerships = earnings.get('brand_partnerships', 0)
                        st.metric("🤝 Partnerships", f"${partnerships:.2f}")
                    
                    with metric_col8:
                        engagement = earnings.get('engagement_rate', 0)
                        st.metric("💬 Engagement", f"{engagement}%")
                    
                    # Performance metrics row
                    perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
                    
                    with perf_col1:
                        earnings_per_1k = earnings.get('earnings_per_1k_views', 0)
                        st.metric("💵 Per 1K Views", f"${earnings_per_1k:.4f}")
                    
                    with perf_col2:
                        avg_views = earnings.get('avg_views_per_video', 0)
                        st.metric("📊 Avg Views/Video", f"{avg_views:,}")
                    
                    with perf_col3:
                        monthly_proj = earnings.get('monthly_projection', 0)
                        st.metric("📈 Monthly Projection", f"${monthly_proj:.2f}")
                    
                    with perf_col4:
                        trend = earnings.get('trend_direction', 'Unknown')
                        trend_emoji = {"growing": "📈", "declining": "📉", "stable": "📊"}.get(trend, "❓")
                        st.metric("📈 Trend", f"{trend_emoji} {trend.title()}")
                    
                    # Revenue streams analysis
                    if earnings.get('revenue_streams'):
                        st.markdown("#### 💰 **Revenue Streams Analysis**")
                        
                        streams = earnings.get('revenue_streams', {})
                        primary_source = earnings.get('primary_revenue_source', 'Unknown')
                        diversification = earnings.get('revenue_diversification', 0)
                        
                        stream_col1, stream_col2 = st.columns(2)
                        
                        with stream_col1:
                            st.markdown(f"**🏆 Primary Source:** {primary_source}")
                            st.markdown(f"**🔄 Diversification:** {diversification} revenue streams")
                            
                            for stream_name, stream_data in streams.items():
                                amount = stream_data.get('amount', 0)
                                percentage = stream_data.get('percentage', 0)
                                st.markdown(f"• **{stream_name.title()}:** ${amount:.2f} ({percentage}%)")
                        
                        with stream_col2:
                            # Create a simple revenue breakdown chart
                            try:
                                import plotly.express as px
                                chart_data = {
                                    'Revenue Stream': [k.replace('_', ' ').title() for k in streams.keys()],
                                    'Amount': [v.get('amount', 0) for v in streams.values()]
                                }
                                
                                if any(chart_data['Amount']):
                                    fig = px.pie(
                                        values=chart_data['Amount'],
                                        names=chart_data['Revenue Stream'],
                                        title="Revenue Distribution"
                                    )
                                    fig.update_layout(height=300)
                                    st.plotly_chart(fig, use_container_width=True)
                                else:
                                    st.info("📊 No revenue data to chart")
                                
                            except ImportError:
                                st.info("📊 Install plotly for revenue charts: pip install plotly")
                            except Exception as e:
                                st.warning(f"Chart unavailable: {str(e)}")
                    
                    # Performance insights
                    if earnings.get('performance_insights'):
                        st.markdown("#### 🎯 **Performance Insights**")
                        
                        insights = earnings.get('performance_insights', [])
                        recommendations = earnings.get('recommendations', [])
                        priority = earnings.get('optimization_priority', 'general')
                        
                        insight_col1, insight_col2 = st.columns(2)
                        
                        with insight_col1:
                            st.markdown("**📊 Current Analysis:**")
                            for insight in insights:
                                st.markdown(f"• {insight}")
                        
                        with insight_col2:
                            st.markdown("**💡 Recommendations:**")
                            for rec in recommendations:
                                st.markdown(f"• {rec}")
                            
                            if priority:
                                priority_emoji = {"engagement": "💬", "monetization": "💰", "growth": "📈"}.get(priority, "🎯")
                                st.markdown(f"**{priority_emoji} Priority Focus:** {priority.title()}")
                    
                    # Demo data notice
                    if earnings.get('demo'):
                        st.info("📊 **Demo Data:** Configure TikTok API credentials for real analytics")
            
            with col2:
                st.markdown("#### 📚 Archive History")
                
                try:
                    tiktok_system = CodexTikTokEarnings()
                    history = tiktok_system.get_archive_history(10)
                    
                    if history:
                        st.metric("📈 Total Archives", len(history))
                        
                        st.markdown("**🕒 Recent Reports:**")
                        for entry in history[-5:]:
                            timestamp = entry.get('ts', 'Unknown')[:16] if len(entry.get('ts', '')) > 16 else entry.get('ts', 'Unknown')
                            earnings_val = entry.get('payouts', 0)
                            st.markdown(f"• {timestamp} - ${earnings_val:.2f}")
                    else:
                        st.info("No earnings history yet")
                        
                except Exception as e:
                    st.warning(f"Could not load history: {str(e)}")
                
                st.markdown("#### ⚙️ Quick Actions")
                
                if st.button("📋 View Config", key="tiktok_config_btn"):
                    try:
                        config_file = Path("tiktok_config.json")
                        if config_file.exists():
                            with open(config_file, 'r') as f:
                                config = json.load(f)
                            st.json(config)
                        else:
                            st.info("Config file will be created on first use")
                    except Exception as e:
                        st.error(f"Config error: {str(e)}")
                
                # Quick earnings calculator
                st.markdown("#### 💰 Earnings Calculator")
                
                calc_views = st.number_input("Views (in thousands)", min_value=0, value=100, step=10)
                calc_rate = st.number_input("Rate per 1K views ($)", min_value=0.0, value=0.02, step=0.01, format="%.4f")
                
                if calc_views and calc_rate:
                    estimated_earnings = calc_views * calc_rate
                    st.metric("💵 Estimated Earnings", f"${estimated_earnings:.2f}")

    # Threads Engagement tab (only if available)
    if THREADS_AVAILABLE:
        threads_tab_index = -2 if len(available_tabs) > 2 else 2  # Before System Status
        with tabs[threads_tab_index]:
            st.markdown("### 🧵 **THREADS ENGAGEMENT SYSTEM**")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("#### 💬 Community Engagement Analytics")
                
                # Profile ID input
                profile_id = st.text_input(
                    "👤 Threads Profile ID:",
                    placeholder="Enter your Threads Profile ID",
                    help="Find your Profile ID in Threads settings or use Meta Graph API tools"
                )
                
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button("📊 Get Engagement", key="threads_get_btn", type="primary", disabled=not profile_id):
                        if profile_id:
                            with st.spinner("Fetching Threads engagement analytics..."):
                                try:
                                    engagement = get_threads_engagement(profile_id)
                                    
                                    if engagement.get("error"):
                                        st.error(f"❌ Error: {engagement['error']}")
                                    else:
                                        st.success("✅ Engagement data retrieved successfully!")
                                        
                                        # Store in session state for display
                                        st.session_state['threads_engagement'] = engagement
                                        
                                except Exception as e:
                                    st.error(f"❌ Error fetching engagement: {str(e)}")
                
                with col_b:
                    if st.button("💾 Archive Current", key="threads_archive_btn", disabled=not st.session_state.get('threads_engagement')):
                        try:
                            if st.session_state.get('threads_engagement'):
                                success = archive_threads(st.session_state['threads_engagement'])
                                if success:
                                    st.success("✅ Archived successfully!")
                                else:
                                    st.error("❌ Archive failed")
                        except Exception as e:
                            st.error(f"❌ Archive error: {str(e)}")
                
                with col_c:
                    if st.button("🔄 Test Connection", key="threads_test_btn"):
                        try:
                            threads_system = CodexThreadsEngagement()
                            if threads_system.test_connection():
                                st.success("✅ Meta API Connected!")
                            else:
                                st.warning("⚠️ Using Demo Data")
                        except Exception as e:
                            st.warning(f"⚠️ Using Demo Mode: {str(e)}")
                
                # Display engagement if available
                if st.session_state.get('threads_engagement'):
                    engagement = st.session_state['threads_engagement']
                    
                    st.markdown("#### 💬 **Engagement Dashboard**")
                    
                    # Main engagement metrics row
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    
                    with metric_col1:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        likes = engagement.get('likes', 0)
                        likes_growth = engagement.get('likes_growth', 0)
                        st.metric("❤️ Total Likes", f"{likes:,}", delta=likes_growth if likes_growth != 0 else None)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with metric_col2:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        reposts = engagement.get('reposts', 0)
                        st.metric("🔄 Reposts", f"{reposts:,}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with metric_col3:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        replies = engagement.get('replies', 0)
                        st.metric("💬 Replies", f"{replies:,}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with metric_col4:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        total_engagement = engagement.get('total_engagement', 0)
                        st.metric("⚡ Total Engagement", f"{total_engagement:,}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Reach and performance metrics row
                    metric_col5, metric_col6, metric_col7, metric_col8 = st.columns(4)
                    
                    with metric_col5:
                        reach = engagement.get('reach', 0)
                        reach_growth = engagement.get('reach_growth', 0)
                        st.metric("👀 Reach", f"{reach:,}", delta=reach_growth if reach_growth != 0 else None)
                    
                    with metric_col6:
                        impressions = engagement.get('impressions', 0)
                        st.metric("📊 Impressions", f"{impressions:,}")
                    
                    with metric_col7:
                        engagement_rate = engagement.get('engagement_rate', 0)
                        st.metric("📈 Engagement Rate", f"{engagement_rate}%")
                    
                    with metric_col8:
                        performance_score = engagement.get('performance_score', 0)
                        st.metric("⭐ Performance Score", f"{performance_score}/100")
                    
                    # Community analysis row
                    perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
                    
                    with perf_col1:
                        followers = engagement.get('followers', 0)
                        st.metric("👥 Followers", f"{followers:,}")
                    
                    with perf_col2:
                        threads_count = engagement.get('threads_count', 0)
                        st.metric("🧵 Total Threads", f"{threads_count:,}")
                    
                    with perf_col3:
                        reply_ratio = engagement.get('reply_to_like_ratio', 0)
                        st.metric("💬 Reply/Like Ratio", f"{reply_ratio:.3f}")
                    
                    with perf_col4:
                        trend = engagement.get('trend_direction', 'Unknown')
                        trend_emoji = {"growing": "📈", "declining": "📉", "stable": "📊"}.get(trend, "❓")
                        st.metric("📈 Trend", f"{trend_emoji} {trend.title()}")
                    
                    # Community engagement analysis
                    if engagement.get('community_type'):
                        st.markdown("#### 🏘️ **Community Analysis**")
                        
                        community_col1, community_col2 = st.columns(2)
                        
                        with community_col1:
                            community_type = engagement.get('community_type', 'Unknown')
                            community_emoji = {
                                "conversational": "💬",
                                "sharing_focused": "🔄", 
                                "passive_consumers": "👀",
                                "balanced": "⚖️"
                            }.get(community_type, "❓")
                            
                            st.markdown(f"**{community_emoji} Community Type:** {community_type.replace('_', ' ').title()}")
                            
                            engagement_distribution = engagement.get('engagement_distribution', {})
                            if engagement_distribution:
                                st.markdown("**📊 Engagement Distribution:**")
                                st.markdown(f"• ❤️ Likes: {engagement_distribution.get('likes', 0)}%")
                                st.markdown(f"• 🔄 Reposts: {engagement_distribution.get('reposts', 0)}%")
                                st.markdown(f"• 💬 Replies: {engagement_distribution.get('replies', 0)}%")
                            
                            quality_score = engagement.get('engagement_quality_score', 0)
                            st.markdown(f"**⭐ Quality Score:** {quality_score}/3.0")
                        
                        with community_col2:
                            # Create engagement distribution chart
                            try:
                                import plotly.express as px
                                if engagement_distribution and any(engagement_distribution.values()):
                                    fig = px.pie(
                                        values=list(engagement_distribution.values()),
                                        names=['❤️ Likes', '🔄 Reposts', '💬 Replies'],
                                        title="Engagement Distribution"
                                    )
                                    fig.update_layout(height=300)
                                    st.plotly_chart(fig, use_container_width=True)
                                else:
                                    st.info("📊 No distribution data to chart")
                                
                            except ImportError:
                                st.info("📊 Install plotly for engagement charts: pip install plotly")
                            except Exception as e:
                                st.warning(f"Chart unavailable: {str(e)}")
                    
                    # Performance insights
                    if engagement.get('content_insights'):
                        st.markdown("#### 🎯 **Performance Insights**")
                        
                        insights = engagement.get('content_insights', [])
                        recommendations = engagement.get('recommendations', [])
                        priority = engagement.get('optimization_priority', 'general')
                        
                        insight_col1, insight_col2 = st.columns(2)
                        
                        with insight_col1:
                            st.markdown("**📊 Current Analysis:**")
                            for insight in insights:
                                st.markdown(f"• {insight}")
                        
                        with insight_col2:
                            st.markdown("**💡 Recommendations:**")
                            for rec in recommendations:
                                st.markdown(f"• {rec}")
                            
                            if priority:
                                priority_emoji = {"engagement": "💬", "reach": "👀", "conversation": "🗣️", "growth": "📈"}.get(priority, "🎯")
                                st.markdown(f"**{priority_emoji} Priority Focus:** {priority.title()}")
                    
                    # Engagement trends
                    if engagement.get('engagement_velocity'):
                        st.markdown("#### 📈 **Engagement Trends**")
                        
                        trend_col1, trend_col2, trend_col3 = st.columns(3)
                        
                        with trend_col1:
                            velocity = engagement.get('engagement_velocity', 'stable')
                            velocity_emoji = {
                                "accelerating": "🚀",
                                "decelerating": "⬇️",
                                "stable": "📊"
                            }.get(velocity, "❓")
                            st.markdown(f"**{velocity_emoji} Velocity:** {velocity.title()}")
                        
                        with trend_col2:
                            peak_hour = engagement.get('peak_engagement_hour', 'unknown')
                            if peak_hour != 'unknown':
                                st.markdown(f"**⏰ Peak Hour:** {peak_hour}")
                            else:
                                st.markdown("**⏰ Peak Hour:** Analyzing...")
                        
                        with trend_col3:
                            avg_daily = engagement.get('avg_daily_engagement', 0)
                            st.markdown(f"**📊 Daily Avg:** {avg_daily:,.0f}")
                    
                    # Demo data notice
                    if engagement.get('demo'):
                        st.info("📊 **Demo Data:** Configure Meta Graph API credentials for real analytics")
            
            with col2:
                st.markdown("#### 📚 Archive History")
                
                try:
                    threads_system = CodexThreadsEngagement()
                    history = threads_system.get_archive_history(10)
                    
                    if history:
                        st.metric("📈 Total Archives", len(history))
                        
                        st.markdown("**🕒 Recent Reports:**")
                        for entry in history[-5:]:
                            timestamp = entry.get('ts', 'Unknown')[:16] if len(entry.get('ts', '')) > 16 else entry.get('ts', 'Unknown')
                            likes = entry.get('likes', 0)
                            st.markdown(f"• {timestamp} - {likes:,} likes")
                    else:
                        st.info("No engagement history yet")
                        
                except Exception as e:
                    st.warning(f"Could not load history: {str(e)}")
                
                st.markdown("#### ⚙️ Quick Actions")
                
                if st.button("📋 View Config", key="threads_config_btn"):
                    try:
                        config_file = Path("threads_config.json")
                        if config_file.exists():
                            with open(config_file, 'r') as f:
                                config = json.load(f)
                            st.json(config)
                        else:
                            st.info("Config file will be created on first use")
                    except Exception as e:
                        st.error(f"Config error: {str(e)}")
                
                # Quick engagement calculator
                st.markdown("#### 💬 Engagement Rate Calculator")
                
                calc_likes = st.number_input("Likes", min_value=0, value=1000, step=50)
                calc_reposts = st.number_input("Reposts", min_value=0, value=50, step=5)
                calc_replies = st.number_input("Replies", min_value=0, value=100, step=10)
                calc_impressions = st.number_input("Impressions", min_value=1, value=10000, step=500)
                
                if calc_impressions > 0:
                    total_engagement_calc = calc_likes + calc_reposts + calc_replies
                    engagement_rate_calc = (total_engagement_calc / calc_impressions) * 100
                    st.metric("📊 Engagement Rate", f"{engagement_rate_calc:.2f}%")
                    
                    # Performance rating
                    if engagement_rate_calc > 5:
                        st.success("🔥 Excellent engagement!")
                    elif engagement_rate_calc > 2:
                        st.info("📈 Good engagement")
                    else:
                        st.warning("💡 Room for improvement")

    # WhatsApp Business tab (only if available)
    if WHATSAPP_AVAILABLE:
        # Find the correct tab index for WhatsApp
        whatsapp_tab_index = len(available_tabs) - 2  # Just before System Status
        with tabs[whatsapp_tab_index]:
            st.markdown("### 💬 **WHATSAPP BUSINESS SYSTEM**")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("#### 📱 Business Communication & Analytics")
                
                # Phone ID input
                phone_id = st.text_input(
                    "📞 WhatsApp Phone ID:",
                    placeholder="Enter your WhatsApp Business Phone ID",
                    help="Find your Phone ID in Meta Business Manager > WhatsApp > API Setup"
                )
                
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button("📊 Get Analytics", key="whatsapp_get_btn", type="primary", disabled=not phone_id):
                        if phone_id:
                            with st.spinner("Fetching WhatsApp Business analytics..."):
                                try:
                                    analytics = get_whatsapp_business_summary(phone_id)
                                    
                                    if analytics.get("error"):
                                        st.error(f"❌ Error: {analytics['error']}")
                                    else:
                                        st.success("✅ Analytics retrieved successfully!")
                                        
                                        # Store in session state for display
                                        st.session_state['whatsapp_analytics'] = analytics
                                        
                                except Exception as e:
                                    st.error(f"❌ Error fetching analytics: {str(e)}")
                
                with col_b:
                    if st.button("💾 Archive Current", key="whatsapp_archive_btn", disabled=not st.session_state.get('whatsapp_analytics')):
                        try:
                            if st.session_state.get('whatsapp_analytics'):
                                success = archive_whatsapp(st.session_state['whatsapp_analytics'])
                                if success:
                                    st.success("✅ Archived successfully!")
                                else:
                                    st.error("❌ Archive failed")
                        except Exception as e:
                            st.error(f"❌ Archive error: {str(e)}")
                
                with col_c:
                    if st.button("🔄 Test Connection", key="whatsapp_test_btn"):
                        try:
                            whatsapp_system = CodexWhatsAppBusiness()
                            if whatsapp_system.test_connection():
                                st.success("✅ WhatsApp API Connected!")
                            else:
                                st.warning("⚠️ Using Demo Data")
                        except Exception as e:
                            st.warning(f"⚠️ Using Demo Mode: {str(e)}")
                
                # Display analytics if available
                if st.session_state.get('whatsapp_analytics'):
                    analytics = st.session_state['whatsapp_analytics']
                    
                    st.markdown("#### 💬 **Business Communication Dashboard**")
                    
                    # Main business metrics row
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    
                    with metric_col1:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        conversations = analytics.get('conversations', 0)
                        conversation_growth = analytics.get('conversation_growth', 0)
                        st.metric("💬 Conversations", f"{conversations:,}", delta=conversation_growth if conversation_growth != 0 else None)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with metric_col2:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        leads = analytics.get('leads', 0)
                        lead_growth = analytics.get('lead_growth', 0)
                        st.metric("🎯 Leads", f"{leads:,}", delta=lead_growth if lead_growth != 0 else None)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with metric_col3:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        cost = analytics.get('messaging_cost_usd', 0)
                        cost_growth = analytics.get('cost_growth', 0)
                        st.metric("💰 Cost (USD)", f"${cost:.2f}", delta=f"${cost_growth:.2f}" if cost_growth != 0 else None)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with metric_col4:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        conversion_rate = analytics.get('lead_conversion_rate', 0)
                        st.metric("📈 Conversion Rate", f"{conversion_rate}%")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Message performance metrics row
                    metric_col5, metric_col6, metric_col7, metric_col8 = st.columns(4)
                    
                    with metric_col5:
                        messages_sent = analytics.get('messages_sent', 0)
                        st.metric("📤 Messages Sent", f"{messages_sent:,}")
                    
                    with metric_col6:
                        delivery_rate = analytics.get('delivery_rate', 0)
                        st.metric("✅ Delivery Rate", f"{delivery_rate*100:.1f}%")
                    
                    with metric_col7:
                        read_rate = analytics.get('read_rate', 0)
                        st.metric("👀 Read Rate", f"{read_rate*100:.1f}%")
                    
                    with metric_col8:
                        engagement_score = analytics.get('engagement_score', 0)
                        st.metric("⚡ Engagement Score", f"{engagement_score:.1f}/100")
                    
                    # Business efficiency metrics row
                    perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
                    
                    with perf_col1:
                        cost_per_conversation = analytics.get('cost_per_conversation', 0)
                        st.metric("💵 Cost/Conversation", f"${cost_per_conversation:.3f}")
                    
                    with perf_col2:
                        cost_per_lead = analytics.get('cost_per_lead', 0)
                        st.metric("🎯 Cost/Lead", f"${cost_per_lead:.2f}")
                    
                    with perf_col3:
                        roi_percentage = analytics.get('roi_percentage', 0)
                        roi_color = "normal" if roi_percentage > 0 else "inverse"
                        st.metric("📊 ROI", f"{roi_percentage:.1f}%", delta_color=roi_color)
                    
                    with perf_col4:
                        performance_score = analytics.get('business_performance_score', 0)
                        st.metric("⭐ Performance Score", f"{performance_score:.1f}/100")
                    
                    # Business analysis section
                    if analytics.get('cost_efficiency_rating'):
                        st.markdown("#### 💼 **Business Performance Analysis**")
                        
                        business_col1, business_col2 = st.columns(2)
                        
                        with business_col1:
                            cost_efficiency = analytics.get('cost_efficiency_rating', 'unknown')
                            cost_emoji = {"excellent": "🟢", "good": "🟡", "high": "🔴"}.get(cost_efficiency, "❓")
                            st.markdown(f"**{cost_emoji} Cost Efficiency:** {cost_efficiency.title()}")
                            
                            performance_trend = analytics.get('performance_trend', 'unknown')
                            trend_emoji = {"accelerating": "🚀", "stable": "📊", "declining": "📉"}.get(performance_trend, "❓")
                            st.markdown(f"**{trend_emoji} Trend:** {performance_trend.title()}")
                            
                            delivery_quality = analytics.get('delivery_quality', 'unknown')
                            delivery_emoji = {"excellent": "🟢", "good": "🟡", "needs_improvement": "🔴"}.get(delivery_quality, "❓")
                            st.markdown(f"**{delivery_emoji} Delivery Quality:** {delivery_quality.replace('_', ' ').title()}")
                            
                            engagement_quality = analytics.get('engagement_quality', 'unknown')
                            engagement_emoji = {"high": "🟢", "medium": "🟡", "low": "🔴"}.get(engagement_quality, "❓")
                            st.markdown(f"**{engagement_emoji} Engagement Quality:** {engagement_quality.title()}")
                        
                        with business_col2:
                            # ROI and cost analysis
                            roi_status = analytics.get('roi_status', 'unknown')
                            roi_emoji = {"profitable": "💰", "breaking_even": "⚖️", "loss": "📉"}.get(roi_status, "❓")
                            st.markdown(f"**{roi_emoji} ROI Status:** {roi_status.replace('_', ' ').title()}")
                            
                            monthly_projection = analytics.get('monthly_cost_projection', 0)
                            st.markdown(f"**📅 Monthly Cost Projection:** ${monthly_projection:.2f}")
                            
                            estimated_revenue = analytics.get('estimated_revenue', 0)
                            st.markdown(f"**💵 Estimated Revenue:** ${estimated_revenue:.2f}")
                            
                            messages_per_conversation = analytics.get('messages_per_conversation', 0)
                            st.markdown(f"**📱 Messages/Conversation:** {messages_per_conversation:.1f}")
                    
                    # Campaign performance section
                    if analytics.get('total_campaigns', 0) > 0:
                        st.markdown("#### 📢 **Campaign Performance**")
                        
                        campaign_col1, campaign_col2, campaign_col3 = st.columns(3)
                        
                        with campaign_col1:
                            total_campaigns = analytics.get('total_campaigns', 0)
                            st.metric("📊 Total Campaigns", total_campaigns)
                        
                        with campaign_col2:
                            avg_success_rate = analytics.get('avg_success_rate', 0)
                            st.metric("✅ Avg Success Rate", f"{avg_success_rate:.1f}%")
                        
                        with campaign_col3:
                            total_messages_sent = analytics.get('total_messages_sent', 0)
                            st.metric("📤 Total Sent", f"{total_messages_sent:,}")
                        
                        campaign_performance = analytics.get('campaign_performance', 'unknown')
                        perf_emoji = {"excellent": "🟢", "good": "🟡", "fair": "🟠", "needs_improvement": "🔴"}.get(campaign_performance, "❓")
                        st.markdown(f"**{perf_emoji} Campaign Rating:** {campaign_performance.replace('_', ' ').title()}")
                    
                    # Broadcast section
                    st.markdown("#### 📢 **Broadcast Message Tool**")
                    
                    broadcast_col1, broadcast_col2 = st.columns([2, 1])
                    
                    with broadcast_col1:
                        message_text = st.text_area(
                            "Message Content:",
                            placeholder="Enter your broadcast message...",
                            height=100,
                            help="Keep messages concise and valuable for best engagement"
                        )
                        
                        recipients_text = st.text_area(
                            "Recipients (one phone number per line):",
                            placeholder="+1234567890\n+0987654321\n...",
                            height=80,
                            help="Enter phone numbers in international format (e.g., +1234567890)"
                        )
                    
                    with broadcast_col2:
                        template_name = st.text_input(
                            "Template Name (optional):",
                            placeholder="e.g., welcome_message",
                            help="Use approved message templates for better delivery"
                        )
                        
                        if st.button("📢 Send Broadcast", key="whatsapp_broadcast_btn"):
                            if message_text and recipients_text:
                                recipients = [line.strip() for line in recipients_text.split('\n') if line.strip()]
                                
                                if recipients:
                                    with st.spinner("Sending broadcast..."):
                                        try:
                                            broadcast_result = whatsapp_broadcast(
                                                message_text,
                                                recipients,
                                                template_name if template_name else None
                                            )
                                            
                                            if broadcast_result.get("error"):
                                                st.error(f"❌ Broadcast failed: {broadcast_result['error']}")
                                            else:
                                                st.success("📢 Broadcast completed!")
                                                
                                                # Show results
                                                result_col1, result_col2, result_col3 = st.columns(3)
                                                
                                                with result_col1:
                                                    st.metric("✅ Successful", broadcast_result.get('successful_sends', 0))
                                                
                                                with result_col2:
                                                    st.metric("❌ Failed", broadcast_result.get('failed_sends', 0))
                                                
                                                with result_col3:
                                                    st.metric("💰 Est. Cost", f"${broadcast_result.get('estimated_cost', 0):.2f}")
                                        
                                        except Exception as e:
                                            st.error(f"❌ Broadcast error: {str(e)}")
                                else:
                                    st.error("❌ Please enter at least one recipient")
                            else:
                                st.error("❌ Please enter both message and recipients")
                    
                    # Demo data notice
                    if analytics.get('demo'):
                        st.info("📊 **Demo Data:** Configure WhatsApp Business API credentials for real analytics and broadcasting")
            
            with col2:
                st.markdown("#### 📚 Archive History")
                
                try:
                    whatsapp_system = CodexWhatsAppBusiness()
                    history = whatsapp_system.get_archive_history(10)
                    
                    if history:
                        st.metric("📈 Total Archives", len(history))
                        
                        st.markdown("**🕒 Recent Reports:**")
                        for entry in history[-5:]:
                            timestamp = entry.get('ts', 'Unknown')[:16] if len(entry.get('ts', '')) > 16 else entry.get('ts', 'Unknown')
                            conversations = entry.get('conversations', 0)
                            cost = entry.get('messaging_cost_usd', 0)
                            st.markdown(f"• {timestamp} - {conversations} conv, ${cost:.2f}")
                    else:
                        st.info("No message history yet")
                        
                except Exception as e:
                    st.warning(f"Could not load history: {str(e)}")
                
                st.markdown("#### ⚙️ Quick Actions")
                
                if st.button("📋 View Config", key="whatsapp_config_btn"):
                    try:
                        config_file = Path("whatsapp_config.json")
                        if config_file.exists():
                            with open(config_file, 'r') as f:
                                config = json.load(f)
                            st.json(config)
                        else:
                            st.info("Config file will be created on first use")
                    except Exception as e:
                        st.error(f"Config error: {str(e)}")
                
                # Cost calculator
                st.markdown("#### 💰 Cost Calculator")
                
                calc_conversations = st.number_input("Conversations", min_value=0, value=100, step=10)
                calc_cost_per_conv = st.number_input("Cost per conversation ($)", min_value=0.0, value=0.25, step=0.05, format="%.3f")
                
                if calc_conversations and calc_cost_per_conv:
                    estimated_cost = calc_conversations * calc_cost_per_conv
                    st.metric("💵 Estimated Cost", f"${estimated_cost:.2f}")
                    
                    # Budget analysis
                    if estimated_cost > 100:
                        st.warning("⚠️ High cost - consider optimization")
                    elif estimated_cost > 50:
                        st.info("💡 Moderate cost - monitor performance")
                    else:
                        st.success("✅ Cost-effective range")

    # Pinterest Capsule tab (only if available)
    if PINTEREST_AVAILABLE:
        # Find the correct tab index for Pinterest
        pinterest_tab_index = len(available_tabs) - 2  # Just before System Status
        with tabs[pinterest_tab_index]:
            st.markdown("### 📌 **PINTEREST CAPSULE SYSTEM**")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("#### 📌 Pinterest Affiliate & Analytics Dashboard")
                
                # User ID input
                user_id = st.text_input(
                    "👤 Pinterest User ID:",
                    placeholder="Enter your Pinterest User ID",
                    help="Find your User ID in Pinterest Business Hub > Account Settings"
                )
                
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button("📊 Get Analytics", key="pinterest_get_btn", type="primary"):
                        with st.spinner("Fetching Pinterest Capsule analytics..."):
                            try:
                                analytics = get_pinterest_capsule_summary(user_id)
                                
                                if analytics.get("error"):
                                    st.error(f"❌ Error: {analytics['error']}")
                                else:
                                    st.success("✅ Analytics retrieved successfully!")
                                    
                                    # Store in session state for display
                                    st.session_state['pinterest_analytics'] = analytics
                                    
                            except Exception as e:
                                st.error(f"❌ Error fetching analytics: {str(e)}")
                
                with col_b:
                    if st.button("💾 Archive Current", key="pinterest_archive_btn", disabled=not st.session_state.get('pinterest_analytics')):
                        try:
                            if st.session_state.get('pinterest_analytics'):
                                success = archive_pinterest(st.session_state['pinterest_analytics'])
                                if success:
                                    st.success("✅ Archived successfully!")
                                else:
                                    st.error("❌ Archive failed")
                        except Exception as e:
                            st.error(f"❌ Archive error: {str(e)}")
                
                with col_c:
                    if st.button("🔄 Test Connection", key="pinterest_test_btn"):
                        try:
                            pinterest_system = CodexPinterestCapsule()
                            if pinterest_system.test_connection():
                                st.success("✅ Pinterest API Connected!")
                            else:
                                st.warning("⚠️ Using Demo Data")
                        except Exception as e:
                            st.warning(f"⚠️ Using Demo Mode: {str(e)}")
                
                # Display analytics if available
                if st.session_state.get('pinterest_analytics'):
                    analytics = st.session_state['pinterest_analytics']
                    
                    st.markdown("#### 📌 **Pinterest Performance Dashboard**")
                    
                    # Main performance metrics row
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    
                    with metric_col1:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        impressions = analytics.get('impressions', 0)
                        growth_rate = analytics.get('growth_rate', 0)
                        st.metric("👀 Impressions", f"{impressions:,}", delta=f"{growth_rate:+.1f}%" if growth_rate != 0 else None)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with metric_col2:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        clicks = analytics.get('clicks', 0)
                        ctr = analytics.get('click_through_rate', 0)
                        st.metric("👆 Clicks", f"{clicks:,}", delta=f"{ctr:.2f}% CTR")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with metric_col3:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        saves = analytics.get('saves', 0)
                        save_rate = analytics.get('save_rate', 0)
                        st.metric("💾 Saves", f"{saves:,}", delta=f"{save_rate:.2f}% Rate")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with metric_col4:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        affiliate_revenue = analytics.get('affiliate_revenue', 0)
                        monthly_projection = analytics.get('estimated_monthly_revenue', 0)
                        st.metric("💰 Affiliate Revenue", f"${affiliate_revenue:.2f}", delta=f"${monthly_projection:.2f}/mo")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Engagement and performance metrics row
                    metric_col5, metric_col6, metric_col7, metric_col8 = st.columns(4)
                    
                    with metric_col5:
                        engagement_rate = analytics.get('engagement_rate', 0)
                        st.metric("⚡ Engagement Rate", f"{engagement_rate:.2f}%")
                    
                    with metric_col6:
                        performance_score = analytics.get('performance_score', 0)
                        st.metric("🏆 Performance Score", f"{performance_score:.1f}/100")
                    
                    with metric_col7:
                        revenue_per_click = analytics.get('revenue_per_click', 0)
                        st.metric("💵 Revenue/Click", f"${revenue_per_click:.2f}")
                    
                    with metric_col8:
                        rpm = analytics.get('revenue_per_impression', 0)
                        st.metric("📈 RPM", f"${rpm:.2f}")
                    
                    # Board and content metrics row
                    board_col1, board_col2, board_col3, board_col4 = st.columns(4)
                    
                    with board_col1:
                        total_boards = analytics.get('total_boards', 0)
                        st.metric("📋 Total Boards", total_boards)
                    
                    with board_col2:
                        active_boards = analytics.get('active_boards', 0)
                        st.metric("🔥 Active Boards", active_boards)
                    
                    with board_col3:
                        utilization = analytics.get('board_utilization_rate', 0)
                        st.metric("📊 Board Utilization", f"{utilization:.1f}%")
                    
                    with board_col4:
                        pin_clicks = analytics.get('pin_clicks', 0)
                        st.metric("📌 Pin Clicks", f"{pin_clicks:,}")
                    
                    # Quality and trend analysis section
                    if analytics.get('content_quality'):
                        st.markdown("#### 🎯 **Performance Analysis**")
                        
                        analysis_col1, analysis_col2 = st.columns(2)
                        
                        with analysis_col1:
                            content_quality = analytics.get('content_quality', 'unknown')
                            quality_emoji = {"exceptional": "🌟", "excellent": "🟢", "good": "🟡", "fair": "🟠", "needs_improvement": "🔴"}.get(content_quality, "❓")
                            st.markdown(f"**{quality_emoji} Content Quality:** {content_quality.replace('_', ' ').title()}")
                            
                            audience_engagement = analytics.get('audience_engagement', 'unknown')
                            engagement_emoji = {"very_high": "🔥", "high": "🟢", "moderate": "🟡", "low": "🟠", "very_low": "🔴"}.get(audience_engagement, "❓")
                            st.markdown(f"**{engagement_emoji} Audience Engagement:** {audience_engagement.replace('_', ' ').title()}")
                            
                            monetization_efficiency = analytics.get('monetization_efficiency', 'unknown')
                            monetization_emoji = {"excellent": "💰", "good": "🟢", "fair": "🟡", "low": "🟠", "very_low": "🔴"}.get(monetization_efficiency, "❓")
                            st.markdown(f"**{monetization_emoji} Monetization:** {monetization_efficiency.replace('_', ' ').title()}")
                        
                        with analysis_col2:
                            performance_trend = analytics.get('performance_trend', 'unknown')
                            trend_emoji = {"accelerating": "🚀", "growing": "📈", "stable": "📊", "declining": "📉", "critical": "🆘"}.get(performance_trend, "❓")
                            st.markdown(f"**{trend_emoji} Performance Trend:** {performance_trend.title()}")
                            
                            revenue_trend = analytics.get('revenue_trend', 'unknown')
                            revenue_emoji = {"excellent": "💎", "strong": "💰", "moderate": "💵", "weak": "📉", "poor": "🔴"}.get(revenue_trend, "❓")
                            st.markdown(f"**{revenue_emoji} Revenue Trend:** {revenue_trend.title()}")
                            
                            period_days = analytics.get('analytics_period_days', 30)
                            st.markdown(f"**📅 Analysis Period:** {period_days} days")
                    
                    # Pin creation section
                    st.markdown("#### 📌 **Quick Pin Creator**")
                    
                    pin_col1, pin_col2 = st.columns([2, 1])
                    
                    with pin_col1:
                        pin_title = st.text_input(
                            "Pin Title:",
                            placeholder="Enter compelling pin title...",
                            help="Keep titles under 100 characters for best performance"
                        )
                        
                        pin_description = st.text_area(
                            "Pin Description:",
                            placeholder="Add description with relevant hashtags...",
                            height=80,
                            help="Include relevant keywords and hashtags for better discoverability"
                        )
                        
                        pin_link = st.text_input(
                            "Affiliate/Destination Link:",
                            placeholder="https://example.com/affiliate-link",
                            help="This is where users will go when they click your pin"
                        )
                        
                        pin_image_url = st.text_input(
                            "Image URL:",
                            placeholder="https://example.com/image.jpg",
                            help="High-quality vertical images (2:3 ratio) perform best"
                        )
                    
                    with pin_col2:
                        board_id = st.text_input(
                            "Board ID (optional):",
                            placeholder="Use default board",
                            help="Leave blank to use your default board"
                        )
                        
                        if st.button("📌 Create Pin", key="pinterest_create_pin_btn"):
                            if pin_title and pin_link and pin_image_url:
                                with st.spinner("Creating Pinterest pin..."):
                                    try:
                                        pin_result = pinterest_pin(
                                            title=pin_title,
                                            link=pin_link,
                                            image_url=pin_image_url,
                                            board_id=board_id if board_id else None,
                                            description=pin_description
                                        )
                                        
                                        if pin_result.get("success"):
                                            st.success(f"✅ {pin_result.get('message', 'Pin created successfully!')}")
                                            
                                            if pin_result.get('pin_url'):
                                                st.markdown(f"🔗 **Pin URL:** {pin_result['pin_url']}")
                                        else:
                                            st.error(f"❌ Pin creation failed: {pin_result.get('error', 'Unknown error')}")
                                    
                                    except Exception as e:
                                        st.error(f"❌ Error creating pin: {str(e)}")
                            else:
                                st.error("❌ Please fill in title, link, and image URL")
                    
                    # Batch pin creation section
                    st.markdown("#### 📌 **Batch Pin Creator**")
                    
                    batch_pins_text = st.text_area(
                        "Batch Pins (JSON format):",
                        placeholder='[{"title": "Pin 1", "link": "https://...", "image_url": "https://...", "description": "..."}, {...}]',
                        height=100,
                        help="Create multiple pins at once using JSON format"
                    )
                    
                    batch_col1, batch_col2, batch_col3 = st.columns(3)
                    
                    with batch_col1:
                        if st.button("📌 Create Batch Pins", key="pinterest_batch_pins_btn"):
                            if batch_pins_text:
                                try:
                                    pins_data = json.loads(batch_pins_text)
                                    
                                    with st.spinner("Creating batch pins..."):
                                        batch_result = pinterest_batch_pin(pins_data)
                                        
                                        st.success("📌 Batch creation completed!")
                                        
                                        result_col1, result_col2, result_col3 = st.columns(3)
                                        
                                        with result_col1:
                                            st.metric("✅ Successful", batch_result.get('successful_pins', 0))
                                        
                                        with result_col2:
                                            st.metric("❌ Failed", batch_result.get('failed_pins', 0))
                                        
                                        with result_col3:
                                            st.metric("📊 Total Processed", batch_result.get('total_processed', 0))
                                
                                except json.JSONDecodeError:
                                    st.error("❌ Invalid JSON format")
                                except Exception as e:
                                    st.error(f"❌ Batch creation error: {str(e)}")
                            else:
                                st.error("❌ Please enter pin data")
                    
                    with batch_col2:
                        if st.button("📋 JSON Template", key="pinterest_json_template_btn"):
                            template = [
                                {
                                    "title": "Amazing Product Deal!",
                                    "description": "Check out this incredible affiliate opportunity! #affiliate #deals #pinterest",
                                    "link": "https://your-affiliate-link.com",
                                    "image_url": "https://your-image-url.com/image.jpg",
                                    "board_id": "optional-board-id"
                                }
                            ]
                            st.code(json.dumps(template, indent=2), language="json")
                    
                    with batch_col3:
                        st.markdown("**💡 Batch Tips:**")
                        st.markdown("• Max 25 pins per batch")
                        st.markdown("• 1 second delay between pins")
                        st.markdown("• Use high-quality images")
                        st.markdown("• Include relevant hashtags")
                    
                    # Demo data notice
                    if analytics.get('demo'):
                        st.info("📊 **Demo Data:** Configure Pinterest Business API credentials for real analytics and pin creation")
            
            with col2:
                st.markdown("#### 📚 Archive History")
                
                try:
                    pinterest_system = CodexPinterestCapsule()
                    history = pinterest_system.get_archive_history(10)
                    
                    if history:
                        st.metric("📈 Total Archives", len(history))
                        
                        st.markdown("**🕒 Recent Reports:**")
                        for entry in history[-5:]:
                            timestamp = entry.get('ts', 'Unknown')[:16] if len(entry.get('ts', '')) > 16 else entry.get('ts', 'Unknown')
                            impressions = entry.get('impressions', 0)
                            revenue = entry.get('affiliate_revenue', 0)
                            st.markdown(f"• {timestamp} - {impressions:,} imp, ${revenue:.2f}")
                    else:
                        st.info("No archive history yet")
                        
                except Exception as e:
                    st.warning(f"Could not load history: {str(e)}")
                
                st.markdown("#### ⚙️ Quick Actions")
                
                if st.button("📋 View Config", key="pinterest_config_btn"):
                    try:
                        config_file = Path("pinterest_config.json")
                        if config_file.exists():
                            with open(config_file, 'r') as f:
                                config = json.load(f)
                            st.json(config)
                        else:
                            st.info("Config file will be created on first use")
                    except Exception as e:
                        st.error(f"Config error: {str(e)}")
                
                # Revenue calculator
                st.markdown("#### 💰 Revenue Calculator")
                
                calc_impressions = st.number_input("Impressions", min_value=0, value=50000, step=1000)
                calc_ctr = st.number_input("CTR (%)", min_value=0.0, value=1.5, step=0.1, format="%.1f")
                calc_conversion = st.number_input("Conversion Rate (%)", min_value=0.0, value=5.0, step=0.5, format="%.1f")
                calc_commission = st.number_input("Avg Commission ($)", min_value=0.0, value=15.0, step=1.0, format="%.2f")
                
                if calc_impressions and calc_ctr and calc_conversion and calc_commission:
                    clicks = calc_impressions * (calc_ctr / 100)
                    conversions = clicks * (calc_conversion / 100)
                    estimated_revenue = conversions * calc_commission
                    
                    st.metric("👆 Estimated Clicks", f"{clicks:,.0f}")
                    st.metric("🎯 Estimated Conversions", f"{conversions:,.0f}")
                    st.metric("💰 Estimated Revenue", f"${estimated_revenue:.2f}")
                    
                    # Revenue analysis
                    if estimated_revenue > 500:
                        st.success("🚀 Excellent revenue potential!")
                    elif estimated_revenue > 200:
                        st.info("💡 Good revenue opportunity")
                    elif estimated_revenue > 50:
                        st.warning("⚠️ Moderate revenue potential")
                    else:
                        st.warning("📈 Consider optimizing for better results")

    # System Status tab (always available)
    status_tab_index = len(available_tabs) - 1
    with tabs[status_tab_index]:
        st.markdown("### ⚡ **SYSTEM STATUS**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔧 Service Health")
            
            services = [
                {"name": "Core Dashboard", "status": "🟢 OPERATIONAL", "available": True},
                {"name": "Dawn Dispatch", "status": "🟢 Ready" if DAWN_AVAILABLE else "🔴 Not Available", "available": DAWN_AVAILABLE},
                {"name": "WooCommerce", "status": "🟢 Available" if WOOCOMMERCE_AVAILABLE else "🔴 Not Configured", "available": WOOCOMMERCE_AVAILABLE},
                {"name": "Twitter", "status": "🟢 Available" if TWITTER_AVAILABLE else "🔴 Not Configured", "available": TWITTER_AVAILABLE},
                {"name": "Buffer", "status": "🟢 Available" if BUFFER_AVAILABLE else "🔴 Not Configured", "available": BUFFER_AVAILABLE},
                {"name": "YouTube Charts", "status": "🟢 Available" if YOUTUBE_AVAILABLE else "🔴 Not Configured", "available": YOUTUBE_AVAILABLE},
                {"name": "TikTok Earnings", "status": "🟢 Available" if TIKTOK_AVAILABLE else "🔴 Not Configured", "available": TIKTOK_AVAILABLE},
                {"name": "Threads Engagement", "status": "🟢 Available" if THREADS_AVAILABLE else "🔴 Not Configured", "available": THREADS_AVAILABLE}
            ]
            
            for service in services:
                st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
                st.markdown(f"**{service['name']}**")
                st.markdown(f"Status: {service['status']}")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 📊 System Metrics")
            
            total_services = len(services)
            available_services = sum(1 for s in services if s["available"])
            
            st.metric("🚀 Services Available", f"{available_services}/{total_services}")
            st.metric("📈 System Health", f"{(available_services/total_services)*100:.1f}%")
            
            # File system status
            try:
                files_present = 0
                files_total = 4
                
                if Path("codex_ledger.json").exists():
                    files_present += 1
                if Path("accounts.json").exists():
                    files_present += 1
                if Path("completed_archives.json").exists():
                    files_present += 1
                if Path("dawn_dispatch_config.json").exists():
                    files_present += 1
                
                st.metric("📁 Config Files", f"{files_present}/{files_total}")
                
            except Exception as e:
                st.error(f"File check error: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <p style='color: #ffd700; font-size: 0.9em;'>
            🔥 Codex Dominion Simple Dashboard 👑<br>
            <em>Powered by The Merritt Method™</em><br>
            <small>Bulletproof Digital Sovereignty Platform</small>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
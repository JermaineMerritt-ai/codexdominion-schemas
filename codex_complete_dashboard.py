import streamlit as st
import json
import requests
from datetime import datetime
from pathlib import Path
import tweepy
from codex_twitter_proclamation import CodexTwitterProclaimer
from codex_woocommerce_sync import CodexWooCommerceSync
from codex_buffer_proclamation import CodexBufferProclaimer
from codex_dawn_dispatch import CodexDawnDispatch, dawn_dispatch
import traceback

def main():
    st.set_page_config(
        page_title="🔥 Codex Dominion - Digital Sovereignty Dashboard",
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
    .proclamation-box {
        background: rgba(255, 215, 0, 0.1);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ffd700;
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
            Digital Sovereignty Control Center
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize services
    twitter_service = None
    woocommerce_service = None
    buffer_service = None

    try:
        twitter_service = CodexTwitterProclaimer()
        st.sidebar.success("🐦 Twitter Service: Connected")
    except Exception as e:
        st.sidebar.error(f"🐦 Twitter Service: {str(e)}")

    try:
        woocommerce_service = CodexWooCommerceSync()
        if woocommerce_service.test_connection():
            st.sidebar.success("🛒 WooCommerce: Connected")
        else:
            st.sidebar.warning("🛒 WooCommerce: Connection failed")
    except Exception as e:
        st.sidebar.error(f"🛒 WooCommerce: {str(e)}")

    try:
        buffer_service = CodexBufferProclaimer()
        if buffer_service.test_connection():
            st.sidebar.success("📱 Buffer Service: Connected")
        else:
            st.sidebar.warning("📱 Buffer Service: Not configured")
    except Exception as e:
        st.sidebar.error(f"📱 Buffer Service: {str(e)}")

    # Initialize Dawn Dispatch service
    dawn_service = None
    try:
        dawn_service = CodexDawnDispatch()
        st.sidebar.success("🌅 Dawn Dispatch: Ready")
    except Exception as e:
        st.sidebar.error(f"🌅 Dawn Dispatch: {str(e)}")

    # Main tabs
    tabs = st.tabs([
        "🏛️ Dominion Central",
        "👑 Sacred Hierarchy", 
        "💰 Treasury Management",
        "📊 Analytics Temple",
        "🛒 Commerce Empire",
        "🐦 Proclamation System",
        "🔮 Oracle Engine",
        "🎯 Strategic Command",
        "🌅 Dawn Dispatch",
        "⚡ System Status"
    ])

    with tabs[0]:  # Dominion Central
        st.markdown("### 🏛️ **DOMINION CENTRAL COMMAND**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("🔥 Active Dominions", "7", "+2")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("👑 Sovereignty Score", "9.8/10", "+0.5")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("⚡ System Power", "98%", "+3%")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("#### 📜 Recent Sacred Scrolls")
        scrolls = [
            "🔥 New AI model deployed to Production Realm",
            "👑 Digital sovereignty protocols updated",
            "💎 Treasury algorithms optimized for maximum yield"
        ]
        
        for scroll in scrolls:
            st.markdown(f'<div class="proclamation-box">{scroll}</div>', unsafe_allow_html=True)

    with tabs[1]:  # Sacred Hierarchy
        st.markdown("### 👑 **SACRED HIERARCHY MANAGEMENT**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏆 Current Hierarchs")
            hierarchs = [
                {"name": "The Architect", "level": "Supreme", "power": 100},
                {"name": "Digital Oracle", "level": "High", "power": 85},
                {"name": "Code Sovereign", "level": "Noble", "power": 70}
            ]
            
            for h in hierarchs:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>{h['name']}</h4>
                    <p>Level: {h['level']}</p>
                    <div style="background: #ffd700; height: 10px; border-radius: 5px;">
                        <div style="background: #ff6b35; height: 100%; width: {h['power']}%; border-radius: 5px;"></div>
                    </div>
                    <p>Power: {h['power']}%</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### ⚡ Hierarchy Actions")
            
            if st.button("👑 Crown New Hierarch"):
                st.success("New hierarch crowned successfully!")
            
            if st.button("⚔️ Challenge Hierarchy"):
                st.warning("Hierarchy challenge initiated!")
            
            if st.button("📜 Update Sacred Laws"):
                st.info("Sacred laws updated!")

    with tabs[2]:  # Treasury Management
        st.markdown("### 💰 **TREASURY MANAGEMENT**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("💎 Digital Assets", "$47,892", "+$3,247")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("🏆 Revenue Streams", "12", "+3")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("📈 Growth Rate", "23.7%", "+2.1%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("⚡ Efficiency", "94.2%", "+1.8%")
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[3]:  # Analytics Temple
        st.markdown("### 📊 **ANALYTICS TEMPLE**")
        
        import plotly.graph_objects as go
        import plotly.express as px
        
        # Sample data for visualization
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            y=[23, 45, 56, 78, 32, 67, 89],
            mode='lines+markers',
            name='Digital Power',
            line=dict(color='#ffd700', width=3)
        ))
        fig1.update_layout(
            title="Weekly Digital Power Fluctuations",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig1, use_container_width=True)

    with tabs[4]:  # Commerce Empire
        st.markdown("### 🛒 **COMMERCE EMPIRE**")
        
        if woocommerce_service:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📦 Product Management")
                
                if st.button("🔄 Sync Products"):
                    with st.spinner("Syncing products..."):
                        try:
                            result = woocommerce_service.sync_all_products()
                            st.markdown(f'<div class="success-box">✅ Sync completed: {result["message"]}</div>', unsafe_allow_html=True)
                        except Exception as e:
                            st.markdown(f'<div class="error-box">❌ Sync failed: {str(e)}</div>', unsafe_allow_html=True)
                
                if st.button("📊 Generate Report"):
                    try:
                        report = woocommerce_service.generate_sync_report()
                        st.json(report)
                    except Exception as e:
                        st.error(f"Report generation failed: {str(e)}")
            
            with col2:
                st.markdown("#### 🏪 Store Status")
                
                try:
                    if woocommerce_service.test_connection():
                        st.markdown('<div class="success-box">🟢 Store Online</div>', unsafe_allow_html=True)
                        
                        # Display recent products
                        products = woocommerce_service.get_products(per_page=5)
                        if products:
                            st.markdown("#### 🛍️ Recent Products")
                            for product in products:
                                st.markdown(f"**{product.get('name', 'Unknown')}** - ${product.get('price', '0')}")
                    else:
                        st.markdown('<div class="error-box">🔴 Store Offline</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="error-box">❌ Connection Error: {str(e)}</div>', unsafe_allow_html=True)
        else:
            st.warning("🛒 WooCommerce service not available. Check configuration.")

    with tabs[5]:  # Proclamation System
        st.markdown("### 🐦 **PROCLAMATION SYSTEM**")
        
        # Service selection tabs
        proc_tabs = st.tabs(["🐦 Twitter", "📱 Multi-Platform (Buffer)", "📊 Analytics"])
        
        with proc_tabs[0]:  # Twitter Tab
            if twitter_service:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("#### 📢 Twitter Proclamation")
                    
                    twitter_text = st.text_area(
                        "Twitter Content",
                        placeholder="Enter your Twitter proclamation...",
                        height=100,
                        key="twitter_text"
                    )
                    
                    col_type, col_hashtags = st.columns(2)
                    
                    with col_type:
                        twitter_type = st.selectbox(
                            "Type",
                            ["sovereignty", "wisdom", "celebration", "announcement"],
                            key="twitter_type"
                        )
                    
                    with col_hashtags:
                        twitter_hashtags = st.selectbox(
                            "Hashtag Set",
                            ["default", "ai", "business", "tech"],
                            key="twitter_hashtags"
                        )
                    
                    create_thread = st.checkbox("Create as Thread", value=False, key="twitter_thread")
                    
                    if st.button("🐦 Send to Twitter", type="primary"):
                        if twitter_text:
                            try:
                                with st.spinner("Sending to Twitter..."):
                                    if create_thread:
                                        result = twitter_service.create_thread([twitter_text], twitter_type, twitter_hashtags)
                                    else:
                                        result = twitter_service.send_proclamation(twitter_text, twitter_type, twitter_hashtags)
                                    
                                    if result.get('success'):
                                        st.success(f"✅ Twitter post sent! ID: {result.get('tweet_id')}")
                                    else:
                                        st.error(f"❌ Failed: {result.get('error')}")
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                        else:
                            st.warning("Please enter content!")
                
                with col2:
                    st.markdown("#### 📊 Twitter Stats")
                    
                    try:
                        history = twitter_service.get_proclamation_history(limit=10)
                        if history:
                            st.metric("📈 Twitter Posts", len(history))
                            
                            for proc in history[:3]:
                                timestamp = datetime.fromisoformat(proc['timestamp']).strftime("%m/%d %H:%M")
                                st.markdown(f"**{timestamp}** - {proc['type']}")
                                st.markdown(f"_{proc['text'][:30]}..._")
                        else:
                            st.info("No Twitter posts yet")
                    except Exception as e:
                        st.warning(f"Could not load history: {str(e)}")
            else:
                st.warning("🐦 Twitter service not available.")
        
        with proc_tabs[1]:  # Buffer Multi-Platform Tab
            if buffer_service:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("#### 📱 Multi-Platform Proclamation")
                    
                    buffer_text = st.text_area(
                        "Multi-Platform Content",
                        placeholder="Enter your multi-platform proclamation...",
                        height=120,
                        key="buffer_text"
                    )
                    
                    # Platform selection
                    st.markdown("**🎯 Target Platforms:**")
                    platforms_col1, platforms_col2 = st.columns(2)
                    
                    profiles = buffer_service.get_profiles()
                    available_platforms = list(set([p.get('service', 'unknown') for p in profiles]))
                    
                    selected_platforms = []
                    for i, platform in enumerate(available_platforms):
                        if i % 2 == 0:
                            with platforms_col1:
                                if st.checkbox(f"{platform.title()}", value=True, key=f"platform_{platform}"):
                                    selected_platforms.append(platform)
                        else:
                            with platforms_col2:
                                if st.checkbox(f"{platform.title()}", value=True, key=f"platform_{platform}"):
                                    selected_platforms.append(platform)
                    
                    col_type_buf, col_hashtags_buf = st.columns(2)
                    
                    with col_type_buf:
                        buffer_type = st.selectbox(
                            "Proclamation Type",
                            ["sovereignty", "wisdom", "celebration", "announcement"],
                            key="buffer_type"
                        )
                    
                    with col_hashtags_buf:
                        buffer_hashtags = st.selectbox(
                            "Hashtag Set",
                            ["default", "business", "tech", "leadership", "social"],
                            key="buffer_hashtags"
                        )
                    
                    # Scheduling option
                    schedule_post = st.checkbox("📅 Schedule for Later", key="schedule_buffer")
                    schedule_time = None
                    
                    if schedule_post:
                        col_date, col_time = st.columns(2)
                        with col_date:
                            schedule_date = st.date_input("Date", key="schedule_date")
                        with col_time:
                            schedule_time_input = st.time_input("Time", key="schedule_time")
                        
                        schedule_time = datetime.combine(schedule_date, schedule_time_input)
                    
                    if st.button("� Send Multi-Platform", type="primary"):
                        if buffer_text:
                            try:
                                with st.spinner("Sending to multiple platforms..."):
                                    if selected_platforms:
                                        result = buffer_service.send_to_specific_platforms(
                                            text=buffer_text,
                                            platforms=selected_platforms,
                                            proclamation_type=buffer_type,
                                            hashtag_set=buffer_hashtags
                                        )
                                    else:
                                        if schedule_time:
                                            result = buffer_service.schedule_proclamation(
                                                text=buffer_text,
                                                schedule_time=schedule_time,
                                                proclamation_type=buffer_type,
                                                hashtag_set=buffer_hashtags
                                            )
                                        else:
                                            result = buffer_service.broadcast_sovereignty(buffer_text)
                                    
                                    if result.get('success'):
                                        platforms_text = ", ".join(selected_platforms) if selected_platforms else "all platforms"
                                        schedule_text = f" (scheduled for {schedule_time})" if schedule_time else ""
                                        st.success(f"✅ Sent to {platforms_text}{schedule_text}!")
                                    else:
                                        st.error(f"❌ Failed: {result.get('error')}")
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                        else:
                            st.warning("Please enter content!")
                
                with col2:
                    st.markdown("#### 📊 Buffer Stats")
                    
                    try:
                        analytics = buffer_service.get_analytics_summary()
                        
                        if analytics:
                            st.metric("📱 Connected Profiles", analytics.get('total_profiles', 0))
                            st.metric("📝 Recent Posts", analytics.get('recent_posts', 0))
                            st.metric("⏰ Pending Posts", analytics.get('pending_posts', 0))
                            
                            st.markdown("**🎯 Platforms:**")
                            for platform, count in analytics.get('profiles_by_platform', {}).items():
                                st.markdown(f"• {platform.title()}: {count} profile(s)")
                        else:
                            st.info("No Buffer analytics available")
                    except Exception as e:
                        st.warning(f"Could not load analytics: {str(e)}")
            else:
                st.warning("📱 Buffer service not available. Check configuration.")
        
        with proc_tabs[2]:  # Analytics Tab
            st.markdown("#### 📊 **Proclamation Analytics**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**� Twitter Performance**")
                if twitter_service:
                    try:
                        twitter_history = twitter_service.get_proclamation_history()
                        twitter_count = len(twitter_history)
                        twitter_success = len([h for h in twitter_history if h.get('success', True)])
                        
                        st.metric("Total Twitter Posts", twitter_count)
                        st.metric("Success Rate", f"{(twitter_success/twitter_count*100):.1f}%" if twitter_count > 0 else "0%")
                    except:
                        st.info("No Twitter data available")
                else:
                    st.info("Twitter not connected")
            
            with col2:
                st.markdown("**� Buffer Performance**")
                if buffer_service:
                    try:
                        buffer_analytics = buffer_service.get_analytics_summary()
                        buffer_history = buffer_service.get_proclamation_history()
                        
                        st.metric("Total Buffer Posts", len(buffer_history))
                        st.metric("Connected Platforms", buffer_analytics.get('total_profiles', 0))
                    except:
                        st.info("No Buffer data available")
                else:
                    st.info("Buffer not connected")
            
            # Combined recent activity
            st.markdown("#### 🕒 Recent Activity")
            
            all_activities = []
            
            # Add Twitter activities
            if twitter_service:
                try:
                    twitter_history = twitter_service.get_proclamation_history(limit=5)
                    for activity in twitter_history:
                        activity['platform'] = 'Twitter'
                        all_activities.append(activity)
                except:
                    pass
            
            # Add Buffer activities
            if buffer_service:
                try:
                    buffer_history = buffer_service.get_proclamation_history(limit=5)
                    for activity in buffer_history:
                        activity['platform'] = 'Buffer'
                        all_activities.append(activity)
                except:
                    pass
            
            # Sort by timestamp and display
            all_activities.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            for activity in all_activities[:10]:
                timestamp = datetime.fromisoformat(activity['timestamp']).strftime("%m/%d %H:%M") if activity.get('timestamp') else "Unknown"
                platform = activity.get('platform', 'Unknown')
                content = activity.get('text', '')[:50] + "..." if len(activity.get('text', '')) > 50 else activity.get('text', '')
                
                st.markdown(f"**{timestamp}** [{platform}] - {content}")
                st.markdown("---")

    with tabs[6]:  # Oracle Engine
        st.markdown("### 🔮 **ORACLE ENGINE**")
        
        st.markdown("#### 🎯 Predictive Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown("**🔮 Digital Prophecy**")
            st.markdown("*The algorithms whisper of great success...*")
            st.progress(0.87)
            st.markdown("Confidence: 87%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown("**⚡ Power Forecast**")
            st.markdown("*Digital sovereignty shall increase by 23% this cycle*")
            st.progress(0.92)
            st.markdown("Certainty: 92%")
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[7]:  # Strategic Command
        st.markdown("### 🎯 **STRATEGIC COMMAND**")
        
        st.markdown("#### ⚔️ Active Campaigns")
        
        campaigns = [
            {"name": "Digital Conquest Alpha", "progress": 78, "status": "Active"},
            {"name": "AI Supremacy Beta", "progress": 45, "status": "Planning"},
            {"name": "Market Domination Gamma", "progress": 92, "status": "Executing"}
        ]
        
        for campaign in campaigns:
            st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f"**{campaign['name']}**")
            st.progress(campaign['progress'] / 100)
            st.markdown(f"Status: {campaign['status']} | Progress: {campaign['progress']}%")
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[8]:  # Dawn Dispatch
        st.markdown("### 🌅 **DAWN DISPATCH SYSTEM**")
        
        if dawn_service:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("#### 📊 Real-Time System Report")
                
                if st.button("🌅 Generate Dawn Dispatch", type="primary"):
                    with st.spinner("Generating comprehensive system report..."):
                        try:
                            result = dawn_service.dawn_dispatch()
                            
                            if result.get("success"):
                                st.markdown('<div class="success-box">✅ Dawn Dispatch generated successfully!</div>', unsafe_allow_html=True)
                                
                                # Display the report in a code block
                                st.markdown("#### 📜 Dawn Dispatch Report")
                                st.code(result.get("report", "No report generated"), language="text")
                                
                                # Show metrics summary
                                st.markdown("#### 📈 Quick Metrics")
                                metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                                
                                store_metrics = dawn_service.get_store_metrics()
                                social_metrics = dawn_service.get_social_metrics()
                                system_status = dawn_service.get_system_status()
                                
                                with metrics_col1:
                                    st.metric("💰 Store Revenue", store_metrics.get('revenue', 'N/A'))
                                    st.metric("📦 Orders", store_metrics.get('orders', 0))
                                
                                with metrics_col2:
                                    st.metric("📱 Social Posts", social_metrics.get('total_interactions', 0))
                                    st.metric("🐦 Twitter", social_metrics.get('twitter_posts', 0))
                                
                                with metrics_col3:
                                    health_score = system_status.get('health_score', 0)
                                    st.metric("⚡ System Health", f"{health_score:.1f}%")
                                    st.metric("🔧 Services Online", f"{sum(1 for v in system_status.get('services', {}).values() if v)}/{len(system_status.get('services', {}))}")
                                
                            else:
                                st.markdown(f'<div class="error-box">❌ Dawn Dispatch failed: {result.get("error")}</div>', unsafe_allow_html=True)
                                
                        except Exception as e:
                            st.markdown(f'<div class="error-box">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
                
                # Manual report sections
                st.markdown("#### 🔧 Manual Report Sections")
                
                col_store, col_social = st.columns(2)
                
                with col_store:
                    if st.button("💰 Store Metrics Only"):
                        try:
                            store_metrics = dawn_service.get_store_metrics()
                            st.json(store_metrics)
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                
                with col_social:
                    if st.button("📱 Social Metrics Only"):
                        try:
                            social_metrics = dawn_service.get_social_metrics()
                            st.json(social_metrics)
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                
                # Archive management
                st.markdown("#### 📚 Archive Management")
                
                if st.button("📖 View Recent Archives"):
                    try:
                        archive_file = Path("completed_archives.json")
                        if archive_file.exists():
                            with open(archive_file, 'r', encoding='utf-8') as f:
                                archives = json.load(f)
                            
                            if archives:
                                st.markdown(f"**Found {len(archives)} archived reports**")
                                
                                # Show last 5 archives
                                for i, archive in enumerate(archives[-5:]):
                                    timestamp = archive.get('timestamp', 'Unknown')[:19]
                                    with st.expander(f"📅 {timestamp}"):
                                        if archive.get('report'):
                                            st.code(archive['report'], language="text")
                                        if archive.get('metrics'):
                                            st.json(archive['metrics'])
                            else:
                                st.info("No archives found")
                        else:
                            st.info("No archive file found")
                    except Exception as e:
                        st.error(f"Error reading archives: {str(e)}")
            
            with col2:
                st.markdown("#### ⚙️ Dawn Dispatch Settings")
                
                # Configuration display
                try:
                    config = dawn_service.config
                    
                    st.markdown("**🔧 Current Settings:**")
                    
                    auto_proclaim = config.get("dispatch_settings", {}).get("auto_proclaim", False)
                    archive_enabled = config.get("dispatch_settings", {}).get("archive_enabled", True)
                    
                    st.markdown(f"• Auto Proclaim: {'✅' if auto_proclaim else '❌'}")
                    st.markdown(f"• Archive Enabled: {'✅' if archive_enabled else '❌'}")
                    st.markdown(f"• Daily Schedule: {config.get('dispatch_settings', {}).get('daily_schedule', 'Not set')}")
                    
                    # Quick toggles (informational only - would need backend to actually change config)
                    st.markdown("**📊 Report Sections:**")
                    sections = config.get("report_sections", {})
                    for section, enabled in sections.items():
                        status = "✅" if enabled else "❌"
                        st.markdown(f"• {section.replace('_', ' ').title()}: {status}")
                    
                except Exception as e:
                    st.warning(f"Could not load settings: {str(e)}")
                
                # Quick actions
                st.markdown("#### 🚀 Quick Actions")
                
                if st.button("📤 Export Last Report"):
                    try:
                        # This would export the last generated report
                        st.info("Export functionality would be implemented here")
                    except Exception as e:
                        st.error(f"Export failed: {str(e)}")
                
                if st.button("🔄 Refresh All Services"):
                    try:
                        # Re-initialize services
                        st.success("Services refreshed!")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Refresh failed: {str(e)}")
                
                # Schedule info
                st.markdown("#### ⏰ Scheduling")
                st.info("💡 To enable automatic daily dispatches, configure the scheduler in your deployment environment.")
        else:
            st.warning("🌅 Dawn Dispatch service not available. Check configuration.")

    with tabs[9]:  # System Status
        st.markdown("### ⚡ **SYSTEM STATUS**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔧 Service Health")
            
            services = [
                {"name": "Core Dashboard", "status": "🟢 Operational", "uptime": "99.9%"},
                {"name": "Twitter Integration", "status": "🟢 Connected" if twitter_service else "🔴 Offline", "uptime": "98.7%"},
                {"name": "Buffer Multi-Platform", "status": "🟢 Connected" if buffer_service and buffer_service.test_connection() else "🔴 Offline", "uptime": "98.2%"},
                {"name": "WooCommerce Sync", "status": "🟢 Active" if woocommerce_service else "🔴 Disconnected", "uptime": "97.2%"},
                {"name": "Analytics Engine", "status": "🟢 Processing", "uptime": "99.5%"}
            ]
            
            for service in services:
                st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
                st.markdown(f"**{service['name']}**")
                st.markdown(f"Status: {service['status']}")
                st.markdown(f"Uptime: {service['uptime']}")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 📊 Performance Metrics")
            
            st.metric("🚀 Response Time", "127ms", "-23ms")
            st.metric("💾 Memory Usage", "234MB", "+12MB")
            st.metric("🔄 CPU Load", "23%", "-5%")
            st.metric("📡 Network I/O", "45 Mbps", "+12 Mbps")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <p style='color: #ffd700; font-size: 0.9em;'>
            🔥 Codex Dominion Digital Sovereignty Platform 👑<br>
            <em>Powered by The Merritt Method™</em>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
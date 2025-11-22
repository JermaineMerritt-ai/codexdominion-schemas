"""
🔥 CODEX SIGNALS DASHBOARD 📊
Interactive portfolio signals and market analysis dashboard

The Merritt Method™ - Visual Financial Intelligence
"""

import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codex_signals.engine import SignalsEngine, MarketSnapshot, Position
from codex_signals.data_feeds import MockDataFeed, DataFeedManager

class SignalsDashboard:
    """
    Streamlit dashboard for Codex Signals Engine
    """
    
    def __init__(self):
        self.engine = SignalsEngine()
        self.data_feed = DataFeedManager()
        
        # Page configuration
        st.set_page_config(
            page_title="🔥 Codex Signals Dashboard",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def render_header(self):
        """Render dashboard header"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div style='text-align: center;'>
                <h1>🔥 CODEX SIGNALS DASHBOARD 📊</h1>
                <h3>Advanced Market Intelligence & Portfolio Signals</h3>
                <p><em>The Merritt Method™ - Quantitative Financial Sovereignty</em></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Real-time timestamp
        st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        st.markdown("---")
    
    def render_sidebar(self):
        """Render sidebar controls"""
        st.sidebar.header("🔧 Engine Configuration")
        
        # Engine parameters
        exposure_cap = st.sidebar.slider("Exposure Cap", 0.05, 0.20, 0.10, 0.01)
        vol_alpha = st.sidebar.slider("Vol Alpha Threshold", 0.15, 0.35, 0.25, 0.01)
        trend_alpha = st.sidebar.slider("Trend Alpha Threshold", 0.25, 0.50, 0.35, 0.01)
        
        # Update engine
        self.engine = SignalsEngine(exposure_cap, vol_alpha, trend_alpha)
        
        st.sidebar.markdown("---")
        st.sidebar.header("📊 Data Options")
        
        data_source = st.sidebar.selectbox(
            "Data Source",
            ["Mock Data", "Live Feed (Demo)"],
            index=0
        )
        
        refresh_data = st.sidebar.button("🔄 Refresh Data")
        
        return data_source, refresh_data
    
    def load_positions(self) -> Dict[str, Position]:
        """Load current portfolio positions"""
        # Mock positions for demo - in production would load from portfolio system
        return {
            "MSFT": Position(symbol="MSFT", weight=0.04, allowed_max=0.08),
            "AAPL": Position(symbol="AAPL", weight=0.03, allowed_max=0.06),
            "BTC-USD": Position(symbol="BTC-USD", weight=0.02, allowed_max=0.06),
            "ETH-USD": Position(symbol="ETH-USD", weight=0.015, allowed_max=0.05),
            "NVDA": Position(symbol="NVDA", weight=0.01, allowed_max=0.04),
        }
    
    def render_market_overview(self, snapshots: List[MarketSnapshot]):
        """Render market overview section"""
        st.header("📊 Market Overview")
        
        # Create DataFrame for easier manipulation
        df = pd.DataFrame([
            {
                'Symbol': s.symbol,
                'Price': s.price,
                '30d Vol': s.vol_30d,
                '20d Trend': s.trend_20d,
                'Liquidity Rank': s.liquidity_rank,
                'Tier': self.engine.classify_tier(s)
            }
            for s in snapshots
        ])
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Symbols", len(snapshots))
        
        with col2:
            avg_vol = df['30d Vol'].mean()
            st.metric("Avg 30d Vol", f"{avg_vol:.2f}")
        
        with col3:
            avg_trend = df['20d Trend'].mean()
            st.metric("Avg 20d Trend", f"{avg_trend:.2f}")
        
        with col4:
            high_liquid = len(df[df['Liquidity Rank'] <= 50])
            st.metric("High Liquidity", f"{high_liquid}/{len(snapshots)}")
        
        # Market snapshot table
        st.subheader("Market Snapshots")
        
        # Color-code tiers
        def color_tier(val):
            colors = {
                'Alpha': 'background-color: #90EE90',  # Light green
                'Beta': 'background-color: #87CEEB',   # Sky blue
                'Gamma': 'background-color: #FFE4B5',  # Moccasin
                'Delta': 'background-color: #FFB6C1'   # Light pink
            }
            return colors.get(val, '')
        
        styled_df = df.style.applymap(color_tier, subset=['Tier'])
        st.dataframe(styled_df, use_container_width=True)
        
        # Tier distribution chart
        col1, col2 = st.columns(2)
        
        with col1:
            tier_counts = df['Tier'].value_counts()
            fig_pie = px.pie(
                values=tier_counts.values,
                names=tier_counts.index,
                title="Tier Distribution",
                color_discrete_map={
                    'Alpha': '#90EE90',
                    'Beta': '#87CEEB', 
                    'Gamma': '#FFE4B5',
                    'Delta': '#FFB6C1'
                }
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Volatility vs Trend scatter
            fig_scatter = px.scatter(
                df, x='20d Trend', y='30d Vol',
                color='Tier', size='Price',
                hover_data=['Symbol', 'Liquidity Rank'],
                title="Risk-Return Profile",
                color_discrete_map={
                    'Alpha': '#90EE90',
                    'Beta': '#87CEEB',
                    'Gamma': '#FFE4B5', 
                    'Delta': '#FFB6C1'
                }
            )
            fig_scatter.add_hline(y=self.engine.vol_alpha, line_dash="dash", 
                                 annotation_text="Vol Alpha Threshold")
            fig_scatter.add_vline(x=self.engine.trend_alpha, line_dash="dash",
                                 annotation_text="Trend Alpha Threshold")
            st.plotly_chart(fig_scatter, use_container_width=True)
    
    def render_signals_analysis(self, snapshot: Dict):
        """Render signals analysis section"""
        st.header("🎯 Portfolio Signals Analysis")
        
        # Compliance banner
        banner = snapshot['banner']
        if "High-risk" in banner:
            st.error(f"⚠️ {banner}")
        elif "Elevated" in banner:
            st.warning(f"⚠️ {banner}")
        else:
            st.info(f"ℹ️ {banner}")
        
        # Tier counts
        tier_counts = snapshot['tier_counts']
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Alpha Tier", tier_counts['Alpha'], 
                     help="Strong trend + low vol + high liquidity")
        with col2:
            st.metric("Beta Tier", tier_counts['Beta'],
                     help="Neutral/stable conditions")
        with col3:
            st.metric("Gamma Tier", tier_counts['Gamma'],
                     help="Elevated risk, defensive sizing")
        with col4:
            st.metric("Delta Tier", tier_counts['Delta'],
                     help="High turbulence, capital preservation")
        
        # Picks table
        st.subheader("Portfolio Signals")
        
        picks_df = pd.DataFrame(snapshot['picks'])
        
        # Format for display
        picks_display = picks_df.copy()
        picks_display['Target Weight'] = picks_display['target_weight'].apply(lambda x: f"{x*100:.1f}%")
        picks_display['Risk Factors Count'] = picks_display['risk_factors'].apply(len)
        
        # Color-code tiers in picks
        styled_picks = picks_display[['symbol', 'tier', 'Target Weight', 'rationale', 'Risk Factors Count']].style.applymap(
            lambda val: 'background-color: #90EE90' if val == 'Alpha' 
            else 'background-color: #87CEEB' if val == 'Beta'
            else 'background-color: #FFE4B5' if val == 'Gamma'  
            else 'background-color: #FFB6C1' if val == 'Delta'
            else '', subset=['tier']
        )
        
        st.dataframe(styled_picks, use_container_width=True)
        
        # Target weights visualization
        fig_weights = go.Figure()
        
        symbols = picks_df['symbol'].tolist()
        weights = picks_df['target_weight'].tolist()
        tiers = picks_df['tier'].tolist()
        
        colors = {
            'Alpha': '#90EE90',
            'Beta': '#87CEEB',
            'Gamma': '#FFE4B5',
            'Delta': '#FFB6C1'
        }
        
        bar_colors = [colors[tier] for tier in tiers]
        
        fig_weights.add_trace(go.Bar(
            x=symbols,
            y=weights,
            marker_color=bar_colors,
            text=[f"{w*100:.1f}%" for w in weights],
            textposition='auto'
        ))
        
        fig_weights.update_layout(
            title="Target Portfolio Weights by Symbol",
            xaxis_title="Symbol",
            yaxis_title="Target Weight",
            yaxis_tickformat=".1%"
        )
        
        st.plotly_chart(fig_weights, use_container_width=True)
    
    def render_risk_analysis(self, snapshot: Dict):
        """Render risk analysis section"""
        st.header("⚠️ Risk Analysis")
        
        picks = snapshot['picks']
        
        # Risk factor analysis
        all_risks = []
        risk_counts = {}
        
        for pick in picks:
            for risk in pick['risk_factors']:
                all_risks.append({'symbol': pick['symbol'], 'risk': risk, 'tier': pick['tier']})
                risk_counts[risk] = risk_counts.get(risk, 0) + 1
        
        if all_risks:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Risk Factor Frequency")
                risk_df = pd.DataFrame(list(risk_counts.items()), columns=['Risk Factor', 'Count'])
                fig_risk = px.bar(risk_df, x='Count', y='Risk Factor', orientation='h',
                                 title="Most Common Risk Factors")
                st.plotly_chart(fig_risk, use_container_width=True)
            
            with col2:
                st.subheader("Symbols with Risk Factors")
                risk_symbols_df = pd.DataFrame(all_risks)
                if not risk_symbols_df.empty:
                    risk_summary = risk_symbols_df.groupby('symbol').agg({
                        'risk': 'count',
                        'tier': 'first'
                    }).reset_index()
                    risk_summary.columns = ['Symbol', 'Risk Count', 'Tier']
                    
                    st.dataframe(risk_summary, use_container_width=True)
        else:
            st.success("✅ No significant risk factors detected across portfolio signals")
        
        # Concentration analysis
        st.subheader("Portfolio Concentration Analysis")
        
        total_weight = sum(pick['target_weight'] for pick in picks)
        concentration_metrics = {
            'Total Allocated Weight': f"{total_weight*100:.1f}%",
            'Unallocated Weight': f"{(1-total_weight)*100:.1f}%",
            'Largest Position': f"{max(pick['target_weight'] for pick in picks)*100:.1f}%",
            'Average Position Size': f"{(total_weight/len(picks))*100:.1f}%"
        }
        
        col1, col2, col3, col4 = st.columns(4)
        cols = [col1, col2, col3, col4]
        
        for i, (metric, value) in enumerate(concentration_metrics.items()):
            with cols[i]:
                st.metric(metric, value)
    
    def export_signals(self, snapshot: Dict):
        """Export signals to JSON"""
        st.subheader("📤 Export Signals")
        
        if st.button("Export to JSON"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"codex_signals_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(snapshot, f, indent=2)
            
            st.success(f"✅ Signals exported to {filename}")
            
            # Show download link (in production would use st.download_button)
            st.json(snapshot)
    
    def run(self):
        """Run the dashboard"""
        self.render_header()
        
        # Sidebar controls
        data_source, refresh_data = self.render_sidebar()
        
        # Load data
        if data_source == "Mock Data":
            snapshots = MockDataFeed.get_mock_snapshots()
        else:
            snapshots = self.data_feed.get_market_snapshots()
        
        # Load positions
        positions = self.load_positions()
        
        # Generate signals
        snapshot = self.engine.generate(snapshots, positions)
        
        # Render sections
        self.render_market_overview(snapshots)
        st.markdown("---")
        
        self.render_signals_analysis(snapshot)
        st.markdown("---")
        
        self.render_risk_analysis(snapshot)
        st.markdown("---")
        
        self.export_signals(snapshot)
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>🔥 Codex Signals Dashboard v1.0 | The Merritt Method™ | 
            Educational and informational use only. Past performance does not guarantee future results.</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main dashboard entry point"""
    dashboard = SignalsDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
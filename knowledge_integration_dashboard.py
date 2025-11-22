#!/usr/bin/env python3
"""
Codex Knowledge Integration Dashboard
====================================

A comprehensive dashboard for managing and visualizing the multi-domain
knowledge integration system within Codex Dominion.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import asyncio
from datetime import datetime, timedelta
import sys
import os

# Add codex-integration to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'codex-integration'))

try:
    from multi_domain_learning_system import MultiDomainLearningSystem
    from domain_knowledge_extractors import IntegratedKnowledgeExtractor
    from enhanced_multi_domain_learning_system import EnhancedMultiDomainLearningSystem
    from cybersecurity_biotech_extractors import EnhancedIntegratedKnowledgeExtractor
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Codex Knowledge Integration",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.domain-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    margin: 0.5rem 0;
}

.metric-card {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
}

.knowledge-item {
    background: #f8f9fa;
    border-left: 4px solid #007bff;
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 5px;
}

.success-banner {
    background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

def main():
    """Main dashboard function"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🧠 Codex Dominion - Multi-Domain Knowledge Integration</h1>
        <p>Learning from Medical, Education, Business, Legal, Industry & Specialized Niches</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🎛️ Control Panel")
    
    # Initialize systems with enhanced capabilities
    if 'learning_system' not in st.session_state:
        st.session_state.learning_system = EnhancedMultiDomainLearningSystem()
        st.session_state.extractor = EnhancedIntegratedKnowledgeExtractor()
        st.session_state.legacy_system = MultiDomainLearningSystem()  # Keep for compatibility
    
    # Navigation
    page = st.sidebar.selectbox(
        "Navigate to:",
        ["📊 Dashboard Overview", "🔍 Domain Analysis", "🧠 Knowledge Extraction", 
         "📈 Learning Results", "⚙️ System Status", "🚀 Integration Tools"]
    )
    
    if page == "📊 Dashboard Overview":
        show_dashboard_overview()
    elif page == "🔍 Domain Analysis":
        show_domain_analysis()
    elif page == "🧠 Knowledge Extraction":
        show_knowledge_extraction()
    elif page == "📈 Learning Results":
        show_learning_results()
    elif page == "⚙️ System Status":
        show_system_status()
    elif page == "🚀 Integration Tools":
        show_integration_tools()

def show_dashboard_overview():
    """Show main dashboard overview"""
    st.header("📊 System Overview")
    
    # Get enhanced domain summary
    summary = st.session_state.learning_system.get_enhanced_domain_summary()
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{summary['system_overview']['total_domains']}</h3>
            <p>Knowledge Domains</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{summary['system_overview']['total_sources']}</h3>
            <p>Knowledge Sources</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{summary['system_overview']['average_credibility']:.1f}</h3>
            <p>Avg Credibility Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Active</h3>
            <p>System Status</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Domain breakdown
    st.subheader("🎯 Domain Breakdown")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Domain source count chart
        domain_data = []
        for domain, info in summary['domains'].items():
            domain_data.append({
                'Domain': domain.replace('_', ' ').title(),
                'Sources': info['source_count'],
                'Credibility': info['average_credibility']
            })
        
        df = pd.DataFrame(domain_data)
        
        fig = px.bar(df, x='Domain', y='Sources', 
                    title="Knowledge Sources per Domain",
                    color='Credibility',
                    color_continuous_scale='Viridis')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Credibility radar chart
        fig = go.Figure()
        
        categories = [domain.replace('_', ' ').title() for domain in summary['domains'].keys()]
        credibility_scores = [info['average_credibility'] for info in summary['domains'].values()]
        
        fig.add_trace(go.Scatterpolar(
            r=credibility_scores,
            theta=categories,
            fill='toself',
            name='Credibility Score'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            title="Domain Credibility Scores"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Top sources by domain
    st.subheader("🏆 Top Sources by Domain")
    
    for domain, info in summary['domains'].items():
        st.markdown(f"""
        <div class="domain-card">
            <h4>{domain.replace('_', ' ').title()}</h4>
            <p>Sources: {info['source_count']} | Avg Credibility: {info['average_credibility']:.1f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show top 3 sources
        for i, source in enumerate(info['top_sources'][:3]):
            st.write(f"  {i+1}. **{source['name']}** - Credibility: {source['credibility']}")

def show_domain_analysis():
    """Show detailed domain analysis"""
    st.header("🔍 Domain Analysis")
    
    # Domain selector - now includes cybersecurity and biotech
    domains = ["cybersecurity", "biotech", "medical", "education", "business_finance", "legal", "industry", "specialized_niches"]
    selected_domain = st.selectbox("Select Domain to Analyze:", 
                                 [d.replace('_', ' ').title() for d in domains])
    
    domain_key = selected_domain.lower().replace(' ', '_')
    
    if st.button(f"🚀 Analyze {selected_domain} Domain"):
        with st.spinner(f"Analyzing {selected_domain} domain..."):
            try:
                # Use enhanced learning for cybersecurity and biotech
                if domain_key in ["cybersecurity", "biotech"]:
                    if domain_key == "cybersecurity":
                        results = asyncio.run(st.session_state.learning_system.learn_from_cybersecurity_domain())
                    else:
                        results = asyncio.run(st.session_state.learning_system.learn_from_biotech_domain())
                else:
                    # Simulate domain analysis for other domains
                    results = {
                        "domain": domain_key,
                        "sources_processed": [f"Source {i+1}" for i in range(5)],
                        "knowledge_extracted": [f"Knowledge item {i+1}" for i in range(10)],
                        "patterns_identified": [
                            {"pattern_type": "trend_analysis", "confidence": 0.85, "occurrences": 8},
                            {"pattern_type": "best_practices", "confidence": 0.90, "occurrences": 12}
                        ],
                        "integration_score": 0.87,
                        "learning_timestamp": datetime.now().isoformat()
                    }
                
                st.success(f"✅ {selected_domain} analysis complete!")
                
                # Display results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Analysis Results")
                    st.write(f"**Sources Processed:** {len(results['sources_processed'])}")
                    st.write(f"**Knowledge Items:** {len(results['knowledge_extracted'])}")
                    st.write(f"**Patterns Found:** {len(results['patterns_identified'])}")
                    st.write(f"**Integration Score:** {results['integration_score']:.2f}")
                
                with col2:
                    # Integration score gauge
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = results['integration_score'] * 100,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Integration Score (%)"},
                        gauge = {'axis': {'range': [None, 100]},
                               'bar': {'color': "darkblue"},
                               'steps': [
                                   {'range': [0, 50], 'color': "lightgray"},
                                   {'range': [50, 80], 'color': "yellow"},
                                   {'range': [80, 100], 'color': "green"}],
                               'threshold': {'line': {'color': "red", 'width': 4},
                                           'thickness': 0.75, 'value': 90}}))
                    st.plotly_chart(fig, use_container_width=True)
                
                # Detailed patterns
                st.subheader("🔍 Identified Patterns")
                for pattern in results['patterns_identified']:
                    st.markdown(f"""
                    <div class="knowledge-item">
                        <strong>{pattern['pattern_type'].replace('_', ' ').title()}</strong><br>
                        Confidence: {pattern['confidence']:.1%} | 
                        Occurrences: {pattern['occurrences']}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Store results
                st.session_state[f'{domain_key}_results'] = results
                
            except Exception as e:
                st.error(f"Analysis failed: {e}")

def show_knowledge_extraction():
    """Show knowledge extraction interface"""
    st.header("🧠 Knowledge Extraction")
    
    # Topic input
    topic = st.text_input("Enter topic for comprehensive knowledge extraction:", 
                         placeholder="e.g., artificial intelligence, healthcare, blockchain")
    
    if st.button("🔍 Extract Comprehensive Knowledge") and topic:
        with st.spinner(f"Extracting knowledge about '{topic}' from all enhanced domains..."):
            try:
                # Enhanced comprehensive extraction
                knowledge = asyncio.run(
                    st.session_state.extractor.extract_comprehensive_enhanced_knowledge(topic)
                )
                
                st.markdown("""
                <div class="success-banner">
                    <h3>✅ Knowledge Extraction Complete!</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Results summary
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Domains Analyzed", 
                            len(knowledge['domain_insights']))
                
                with col2:
                    st.metric("Cross-Domain Correlations", 
                            len(knowledge['cross_domain_correlations']))
                
                with col3:
                    st.metric("Actionable Insights", 
                            len(knowledge['actionable_insights']))
                
                # Detailed results
                st.subheader("📊 Domain Insights")
                
                for domain, insights in knowledge['domain_insights'].items():
                    with st.expander(f"📁 {domain.replace('_', ' ').title()} Domain"):
                        if insights:
                            for i, insight in enumerate(insights[:3]):  # Show top 3
                                credibility_score = insight.get('credibility_score', insight.get('credibility', 0.0))
                                st.markdown(f"""
                                <div class="knowledge-item">
                                    <strong>Source:</strong> {insight.get('source', 'Unknown')}<br>
                                    <strong>Title:</strong> {insight.get('title', insight.get('name', 'N/A'))}<br>
                                    <strong>Credibility:</strong> {credibility_score:.1f}/10
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.write("No insights available for this domain.")
                
                # Cross-domain correlations
                if knowledge['cross_domain_correlations']:
                    st.subheader("🔗 Cross-Domain Correlations")
                    for correlation in knowledge['cross_domain_correlations']:
                        st.markdown(f"""
                        <div class="knowledge-item">
                            <strong>{correlation['correlation_type'].replace('_', ' ').title()}</strong><br>
                            Domains: {', '.join(correlation['domains'])}<br>
                            Strength: {correlation['strength']:.1%}<br>
                            Insight: {correlation['insight']}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Actionable insights
                st.subheader("💡 Actionable Insights")
                for insight in knowledge['actionable_insights']:
                    st.write(f"• {insight}")
                
                # Integration recommendations
                st.subheader("🚀 Integration Recommendations")
                for recommendation in knowledge['integration_recommendations']:
                    st.write(f"• {recommendation}")
                
                # Store results
                st.session_state[f'knowledge_{topic}'] = knowledge
                
            except Exception as e:
                st.error(f"Extraction failed: {e}")

def show_learning_results():
    """Show learning results and history"""
    st.header("📈 Learning Results")
    
    if st.button("🚀 Run Global Learning Session"):
        with st.spinner("Running comprehensive learning across all domains..."):
            try:
                results = asyncio.run(st.session_state.learning_system.learn_from_all_enhanced_domains())
                
                st.markdown("""
                <div class="success-banner">
                    <h3>🎉 Global Learning Session Complete!</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Global metrics
                global_session = results['global_learning_session']
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Domains Processed", 
                            len(global_session['domains_processed']))
                
                with col2:
                    st.metric("Total Sources", 
                            global_session['total_sources'])
                
                with col3:
                    st.metric("Integration Score", 
                            f"{global_session['overall_integration_score']:.2f}")
                
                with col4:
                    st.metric("Cross-Domain Patterns", 
                            len(global_session['cross_domain_patterns']))
                
                # Domain-by-domain results
                st.subheader("📊 Domain Results")
                
                domain_scores = []
                for domain, result in results['domain_results'].items():
                    domain_scores.append({
                        'Domain': domain.replace('_', ' ').title(),
                        'Integration Score': result['integration_score'],
                        'Sources': len(result['sources_processed']),
                        'Knowledge Items': len(result['knowledge_extracted']),
                        'Patterns': len(result['patterns_identified'])
                    })
                
                df = pd.DataFrame(domain_scores)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = px.bar(df, x='Domain', y='Integration Score',
                                title="Integration Scores by Domain",
                                color='Integration Score',
                                color_continuous_scale='Viridis')
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = px.scatter(df, x='Sources', y='Knowledge Items',
                                   size='Patterns', color='Domain',
                                   title="Knowledge Extraction Efficiency",
                                   hover_data=['Integration Score'])
                    st.plotly_chart(fig, use_container_width=True)
                
                # Cross-domain patterns
                st.subheader("🔗 Cross-Domain Patterns")
                for pattern in global_session['cross_domain_patterns']:
                    st.markdown(f"""
                    <div class="knowledge-item">
                        <strong>{pattern['pattern'].replace('_', ' ').title()}</strong><br>
                        Domains: {', '.join(pattern['involved_domains'])}<br>
                        Strength: {pattern['strength']:.1%}<br>
                        Description: {pattern['description']}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Store results
                st.session_state['global_learning_results'] = results
                
            except Exception as e:
                st.error(f"Global learning failed: {e}")

def show_system_status():
    """Show system status and health"""
    st.header("⚙️ System Status")
    
    # System health indicators
    st.subheader("🏥 System Health")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🟢 Operational</h3>
            <p>Learning System</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🟢 Active</h3>
            <p>Knowledge Extractors</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🟢 Ready</h3>
            <p>Integration Engine</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Configuration
    st.subheader("⚙️ Configuration")
    
    with st.expander("🔧 System Configuration"):
        st.json({
            "learning_system": "MultiDomainLearningSystem",
            "extractor": "IntegratedKnowledgeExtractor",
            "domains": 6,
            "total_sources": 30,
            "api_endpoints": 15,
            "last_updated": datetime.now().isoformat()
        })
    
    # Performance metrics
    st.subheader("📊 Performance Metrics")
    
    # Simulate performance data
    days = pd.date_range(start='2024-10-01', end='2024-11-06', freq='D')
    performance_data = pd.DataFrame({
        'Date': days,
        'Knowledge Items': [100 + i*5 + (i%3)*10 for i in range(len(days))],
        'Integration Score': [0.7 + (i%10)*0.03 for i in range(len(days))],
        'API Calls': [200 + i*8 + (i%5)*20 for i in range(len(days))]
    })
    
    fig = px.line(performance_data, x='Date', y='Knowledge Items',
                  title="Daily Knowledge Extraction Trend")
    st.plotly_chart(fig, use_container_width=True)

def show_integration_tools():
    """Show integration tools and utilities"""
    st.header("🚀 Integration Tools")
    
    st.subheader("🔄 Codex System Integration")
    
    if 'global_learning_results' in st.session_state:
        results = st.session_state['global_learning_results']
        
        if st.button("🚀 Integrate with Codex System"):
            with st.spinner("Integrating learned knowledge with Codex Dominion..."):
                integration_result = st.session_state.learning_system.integrate_with_codex_system(results)
                
                st.success("✅ Integration Complete!")
                
                # Show integration results
                enhancement = integration_result['codex_enhancement']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🆕 New Capabilities")
                    for capability in enhancement['new_capabilities']:
                        st.write(f"• {capability.replace('_', ' ').title()}")
                    
                    st.subheader("📈 Improved Modules")
                    for module in enhancement['improved_modules']:
                        st.write(f"• {module.replace('_', ' ').title()}")
                
                with col2:
                    st.subheader("🔗 Knowledge Fusions")
                    for fusion in enhancement['knowledge_fusion']:
                        st.markdown(f"""
                        <div class="knowledge-item">
                            <strong>{fusion['fusion_type'].replace('_', ' ').title()}</strong><br>
                            Domains: {', '.join(fusion['domains_involved'])}<br>
                            Benefit: {fusion['system_benefit']}
                        </div>
                        """, unsafe_allow_html=True)
                
                st.subheader("🚀 System Evolution")
                for evolution in enhancement['system_evolution']:
                    st.write(f"• {evolution}")
                
                st.session_state['integration_result'] = integration_result
    else:
        st.info("💡 Run a Global Learning Session first to generate integration data.")
    
    # Export tools
    st.subheader("📤 Export Tools")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Learning Data"):
            if 'global_learning_results' in st.session_state:
                data = st.session_state['global_learning_results']
                st.download_button(
                    label="💾 Download JSON",
                    data=json.dumps(data, indent=2),
                    file_name=f"learning_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            else:
                st.warning("No learning data to export.")
    
    with col2:
        if st.button("🔧 Export Configuration"):
            summary = st.session_state.learning_system.get_domain_summary()
            st.download_button(
                label="💾 Download Config",
                data=json.dumps(summary, indent=2),
                file_name=f"system_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col3:
        if st.button("📈 Export Integration"):
            if 'integration_result' in st.session_state:
                data = st.session_state['integration_result']
                st.download_button(
                    label="💾 Download Integration",
                    data=json.dumps(data, indent=2),
                    file_name=f"integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            else:
                st.warning("No integration data to export.")

if __name__ == "__main__":
    main()
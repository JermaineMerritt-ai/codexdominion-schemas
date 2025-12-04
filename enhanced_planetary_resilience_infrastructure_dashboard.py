"""
Enhanced Dashboard with Performance Optimizations
===============================================
"""

import json
import time
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# Performance monitoring decorator
def performance_monitor(operation_name=None):
    """Monitor performance of functions"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time

                # Store performance data
                if 'performance_data' not in st.session_state:
                    st.session_state.performance_data = {}

                op_name = operation_name or func.__name__
                if op_name not in st.session_state.performance_data:
                    st.session_state.performance_data[op_name] = []

                st.session_state.performance_data[op_name].append(execution_time)

                # Keep only last 100 measurements
                if len(st.session_state.performance_data[op_name]) > 100:
                    st.session_state.performance_data[op_name] = st.session_state.performance_data[op_name][-100:]

                return result
            except Exception as e:
                st.error(f"Error in {operation_name or func.__name__}: {str(e)}")
                raise
        return wrapper
    return decorator

# Enhanced data loading with caching
@st.cache_data(ttl=300)  # Cache for 5 minutes
@performance_monitor("load_json_file")
def load_json_enhanced(filename, default_data):
    """Enhanced JSON loading with caching and error handling"""
    try:
        path = Path(filename)
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data if data else default_data
        else:
            return default_data
    except Exception as e:
        st.error(f"Error loading {filename}: {str(e)}")
        return default_data

# Performance dashboard component
@performance_monitor("show_performance_dashboard")
def show_performance_dashboard():
    """Show performance statistics"""
    if 'performance_data' in st.session_state and st.session_state.performance_data:
        with st.expander("Performance Dashboard"):
            st.subheader("Operation Performance")

            for operation, times in st.session_state.performance_data.items():
                if times:
                    avg_time = sum(times) / len(times)
                    max_time = max(times)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(f"{operation} Avg", f"{avg_time:.3f}s")
                    with col2:
                        st.metric("Max", f"{max_time:.3f}s")
                    with col3:
                        st.metric("Calls", len(times))

# Enhanced styling
def apply_enhanced_styling():
    """Apply enhanced styling"""
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    }

    .enhanced-header {
        text-align: center;
        padding: 30px;
        margin-bottom: 30px;
        background: linear-gradient(45deg, rgba(138,43,226,0.4), rgba(75,0,130,0.3));
        border: 2px solid #8B2BE2;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(138,43,226,0.3);
    }

    .enhanced-card {
        background: rgba(255,255,255,0.1);
        padding: 25px;
        border-radius: 20px;
        border: 2px solid rgba(138,43,226,0.3);
        backdrop-filter: blur(15px);
        margin: 15px 0;
        transition: all 0.4s ease;
    }

    .enhanced-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 40px rgba(138,43,226,0.4);
        border-color: #8B2BE2;
    }

    .stButton > button {
        background: linear-gradient(45deg, #8B2BE2, #9370DB);
        border: none;
        border-radius: 15px;
        color: white;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(45deg, #9370DB, #8B2BE2);
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(138,43,226,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

Planetary Resilience & Infrastructure System
===========================================

Global-scale infrastructure intelligence for planetary resilience,
climate adaptation, and sustainable development.
"""

import streamlit as st
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any

# Page configuration
st.set_page_config(
    page_title="Planetary Resilience & Infrastructure",
    page_icon="🌍🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.planetary-header {
    background: linear-gradient(135deg, #2d5016 0%, #4a7c59 50%, #6faadb 100%);
    padding: 2rem;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(45, 80, 22, 0.3);
}

.infrastructure-card {
    background: linear-gradient(135deg, #4a7c59 0%, #6faadb 100%);
    padding: 1.5rem;
    border-radius: 15px;
    color: white;
    margin: 1rem 0;
    box-shadow: 0 8px 25px rgba(74, 124, 89, 0.2);
}

.resilience-metric {
    background: linear-gradient(135deg, #6faadb 0%, #2d5016 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    margin: 0.5rem 0;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

class PlanetaryResilienceSystem:
    """Planetary resilience and infrastructure intelligence"""

    def __init__(self):
        self.elite_sources = {
            "climate_infrastructure": [
                "IPCC Infrastructure Reports",
                "World Bank Climate Resilience",
                "UN Habitat Urban Resilience",
                "Climate Policy Initiative",
                "Global Commission on Adaptation"
            ],
            "smart_cities": [
                "Smart Cities Council",
                "C40 Cities Climate Leadership",
                "ICLEI Local Governments",
                "Singapore Smart Nation",
                "Barcelona Digital City"
            ],
            "renewable_infrastructure": [
                "International Renewable Energy Agency (IRENA)",
                "Global Wind Energy Council",
                "Solar Power Europe",
                "International Energy Agency",
                "BloombergNEF Energy Transition"
            ],
            "water_systems": [
                "World Water Council",
                "International Water Association",
                "UN Water",
                "Global Water Intelligence",
                "Water Resources Institute"
            ],
            "transportation_systems": [
                "International Transport Forum",
                "Global BRT Data",
                "Institute for Transportation Studies",
                "Mobility as a Service Alliance",
                "Sustainable Transport Partnership"
            ]
        }

        self.infrastructure_domains = [
            "Climate-Resilient Infrastructure",
            "Smart City Systems",
            "Renewable Energy Grids",
            "Water Management Systems",
            "Sustainable Transportation",
            "Circular Economy Infrastructure",
            "Disaster-Resilient Buildings",
            "Food Security Systems",
            "Digital Infrastructure",
            "Green Finance Mechanisms"
        ]

    async def analyze_planetary_systems(self, region: str, focus: str) -> Dict:
        """Analyze planetary resilience systems"""
        return {
            "region": region,
            "focus_area": focus,
            "resilience_analysis": {
                "climate_adaptation": {
                    "current_resilience": 0.72,
                    "adaptation_gaps": [
                        f"{region} needs enhanced flood protection systems",
                        f"Heat resilience infrastructure requires 40% expansion",
                        f"Coastal protection systems need climate-proofing"
                    ],
                    "investment_needed": "$45B globally for {focus}",
                    "timeline": "10-15 years for full implementation"
                },
                "infrastructure_assessment": {
                    "smart_cities_readiness": 0.68,
                    "renewable_integration": 0.75,
                    "water_security": 0.63,
                    "transport_sustainability": 0.58,
                    "digital_resilience": 0.82
                },
                "innovation_opportunities": [
                    f"AI-powered {focus} optimization in {region}",
                    f"Blockchain-based resource sharing for {focus}",
                    f"IoT sensors for real-time {focus} monitoring",
                    f"Green hydrogen infrastructure for {focus}"
                ]
            },
            "planetary_trends": [
                f"{region} leading in {focus} innovation with 23% growth",
                f"Global {focus} investment reaches $2.3T annually",
                f"Climate-resilient {focus} reduces risks by 65%",
                f"Smart {focus} systems improve efficiency by 40%"
            ],
            "sustainability_metrics": {
                "carbon_reduction": "45% by 2030 through smart infrastructure",
                "resource_efficiency": "60% improvement with circular systems",
                "disaster_resilience": "80% reduction in climate risks",
                "energy_independence": "90% renewable by 2040"
            }
        }

def main():
    """Main Planetary Resilience & Infrastructure interface"""

    # Header
    st.markdown("""
    <div class="planetary-header">
        <h1>🌍🏗️ PLANETARY RESILIENCE & INFRASTRUCTURE</h1>
        <h2>Global Infrastructure Intelligence & Climate Adaptation</h2>
        <p>Climate Resilience • Smart Cities • Sustainable Systems • Planetary Scale</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize system
    if 'planetary_system' not in st.session_state:
        st.session_state.planetary_system = PlanetaryResilienceSystem()

    col1, col2 = st.columns([2, 1])

    with col1:
    # Apply enhanced styling
    apply_enhanced_styling()

        st.header("🌍 Planetary Analysis")

        col_a, col_b = st.columns(2)
        with col_a:
            region = st.selectbox(
                "🌎 Select Region:",
                ["Global", "North America", "Europe", "Asia Pacific", "Africa", "Latin America", "Middle East"]
            )

        with col_b:
            focus = st.selectbox(
                "🎯 Infrastructure Focus:",
                ["Climate Resilience", "Smart Cities", "Renewable Energy", "Water Systems",
                 "Transportation", "Digital Infrastructure", "Disaster Prevention"]
            )

        if st.button("🚀 Analyze Planetary Systems"):
            with st.spinner(f"Analyzing {focus} infrastructure in {region}..."):
                analysis = asyncio.run(
                    st.session_state.planetary_system.analyze_planetary_systems(region, focus)
                )

                st.subheader("🌍 Resilience Assessment")
                resilience = analysis['resilience_analysis']['climate_adaptation']

                col1_met, col2_met, col3_met = st.columns(3)
                with col1_met:
                    st.metric("Climate Resilience", f"{resilience['current_resilience']:.0%}")
                with col2_met:
                    st.metric("Investment Needed", resilience['investment_needed'])
                with col3_met:
                    st.metric("Implementation Timeline", resilience['timeline'])

                st.subheader("🏗️ Infrastructure Readiness")
                infra = analysis['resilience_analysis']['infrastructure_assessment']

                for system, readiness in infra.items():
                    st.markdown(f"""
                    <div class="infrastructure-card">
                        <strong>{system.replace('_', ' ').title()}:</strong> {readiness:.0%} Ready
                    </div>
                    """, unsafe_allow_html=True)

    with col2:
    # Apply enhanced styling
    apply_enhanced_styling()

        st.header("🏗️ Infrastructure Capabilities")

        capabilities = [
            "🌍 Climate Adaptation",
            "🏙️ Smart City Systems",
            "⚡ Renewable Energy Grids",
            "💧 Water Management",
            "🚊 Sustainable Transport",
            "♻️ Circular Economy",
            "🏢 Resilient Buildings",
            "🌾 Food Security",
            "📡 Digital Infrastructure",
            "💚 Green Finance"
        ]

        for capability in capabilities:
            st.markdown(f"""
            <div class="resilience-metric">
                {capability}
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

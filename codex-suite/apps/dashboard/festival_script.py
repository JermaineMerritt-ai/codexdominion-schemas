# apps/dashboard/festival_script.py
import calendar
import sys
from datetime import date, datetime
from pathlib import Path

import streamlit as st

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from core.ledger import append_entry, load_json
except ImportError:
    # Fallback functions if core modules aren't available
    import json

    def append_entry(file, key, entry):
        try:
            data_dir = Path(__file__).parent.parent / "data"
            data_dir.mkdir(exist_ok=True)

            # Load existing data
            file_path = data_dir / file
            if file_path.exists():
                with open(file_path, "r") as f:
                    data = json.load(f)
            else:
                data = {key: []}

            # Add timestamp and append entry
            entry["timestamp"] = datetime.now().isoformat()
            data[key].append(entry)

            # Save updated data
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
            return entry
        except Exception:
            return None

    def load_json(name, default):
        try:
            data_dir = Path(__file__).parent.parent / "data"
            with open(data_dir / name, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return default


st.set_page_config(
    page_title="Festival Script - Seasonal Invocations", page_icon="🎇", layout="wide"
)

# Cosmic header with seasonal styling
current_season = [
    "Winter",
    "Winter",
    "Spring",
    "Spring",
    "Spring",
    "Summer",
    "Summer",
    "Summer",
    "Autumn",
    "Autumn",
    "Autumn",
    "Winter",
][datetime.now().month - 1]
season_colors = {
    "Spring": "linear-gradient(90deg, #8bc34a, #4caf50)",
    "Summer": "linear-gradient(90deg, #ff9800, #ff5722)",
    "Autumn": "linear-gradient(90deg, #ff5722, #795548)",
    "Winter": "linear-gradient(90deg, #607d8b, #455a64)",
}

st.markdown(
    f"""
<div style='text-align: center; padding: 25px; background: {season_colors[current_season]}; border-radius: 15px; margin-bottom: 25px;'>
    <h1 style='color: white; margin: 0; font-size: 2.5em;'>🎇 Festival Script</h1>
    <p style='color: #f0f0f0; margin: 10px 0 5px 0; font-size: 1.2em; font-style: italic;'>Seasonal & Eternal Invocations</p>
    <p style='color: #e0e0e0; margin: 0; font-size: 1em;'>Current Season: {current_season} | Sacred Cycles of the Codex</p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("**🌟 Cosmic Ceremony Chamber**")
st.write(
    "Here the eternal cycles are honored through sacred invocations, marking the passage of time in the Codex flame."
)

# Main festival interface
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎭 Cyclical Invocation")

    # Enhanced cycle selection with descriptions
    cycle_options = [
        "Morning Flame",
        "Twilight Flame",
        "Seasonal Festival",
        "Great Year Invocation",
        "Lunar Ceremony",
        "Solar Celebration",
        "Cosmic Alignment",
        "Eternal Renewal",
    ]

    cycle = st.selectbox(
        "🌙 Sacred Cycle:",
        cycle_options,
        help="Select the cosmic cycle for this invocation",
    )

    # Cycle descriptions and timing
    cycle_descriptions = {
        "Morning Flame": "🌅 Daily dawn ceremony - Beginning and renewal energy",
        "Twilight Flame": "🌇 Evening reflection - Completion and wisdom gathering",
        "Seasonal Festival": f"🍂 {current_season} celebration - Honoring natural transitions",
        "Great Year Invocation": "🌍 Annual cosmic ceremony - Marking full cycle completion",
        "Lunar Ceremony": "🌙 Moon phase ritual - Tidal and emotional alignment",
        "Solar Celebration": "☀️ Solar event - Power and illumination ceremony",
        "Cosmic Alignment": "⭐ Celestial alignment - Universal harmony invocation",
        "Eternal Renewal": "♾️ Timeless ceremony - Connection to eternal flame",
    }

    st.info(cycle_descriptions.get(cycle, "Select a cycle for cosmic guidance"))

    # Enhanced role selection with cosmic hierarchy
    role_options = [
        "Custodian",
        "Heirs",
        "Councils",
        "Cosmos",
        "Elements",
        "Ancestors",
        "Future Selves",
    ]

    role = st.selectbox(
        "👥 Invoking Role:",
        role_options,
        help="Who speaks this invocation to the cosmos",
    )

    # Role descriptions
    role_descriptions = {
        "Custodian": "🔥 Guardian of the eternal flame - Administrative authority",
        "Heirs": "🎭 Inheritors of wisdom - Creative and learning energy",
        "Councils": "⚖️ Collective governance - Decision-making power",
        "Cosmos": "🌌 Universal consciousness - Infinite perspective",
        "Elements": "🌪️ Natural forces - Elemental power and balance",
        "Ancestors": "👻 Ancient wisdom - Historical guidance and honor",
        "Future Selves": "🚀 Tomorrow's vision - Aspirational and prophetic",
    }

    st.caption(role_descriptions.get(role, ""))

    # Enhanced ritual types with cosmic flavoring
    ritual_options = [
        "Proclamation",
        "Silence",
        "Blessing",
        "Invocation",
        "Gratitude",
        "Release",
        "Manifestation",
    ]

    ritual_type = st.selectbox(
        "🔮 Ritual Type:", ritual_options, help="The nature of this cosmic ceremony"
    )

    # Ritual type guidance
    ritual_guidance = {
        "Proclamation": "📢 Cosmic declaration - Announcing intentions to universe",
        "Silence": "🤫 Sacred pause - Creating space for cosmic listening",
        "Blessing": "✨ Divine favor - Invoking positive energy and protection",
        "Invocation": "🔥 Calling forth - Summoning cosmic forces and guidance",
        "Gratitude": "🙏 Cosmic appreciation - Honoring gifts and abundance",
        "Release": "🌊 Letting go - Releasing old patterns to cosmos",
        "Manifestation": "⚡ Creation magic - Bringing dreams into reality",
    }

    st.caption(ritual_guidance.get(ritual_type, ""))

    # Enhanced text input with cosmic prompts
    cosmic_prompts = {
        "Morning Flame": "As dawn breaks and the flame awakens...",
        "Twilight Flame": "As shadows lengthen and wisdom gathers...",
        "Seasonal Festival": f"In this time of {current_season}, we honor...",
        "Great Year Invocation": "As the great wheel turns full circle...",
        "Lunar Ceremony": "By the light of the sacred moon...",
        "Solar Celebration": "In the radiance of the eternal sun...",
        "Cosmic Alignment": "As the stars align in perfect harmony...",
        "Eternal Renewal": "In the timeless dance of creation...",
    }

    text = st.text_area(
        "📝 Sacred Invocation Text:",
        height=150,
        help="Enter your cosmic invocation to be inscribed in the eternal cycles",
        placeholder=cosmic_prompts.get(
            cycle, "By flame and cosmos, let this invocation echo through eternity..."
        ),
    )

    # Advanced festival settings
    with st.expander("🌟 Advanced Cosmic Settings"):

        # Cosmic timing
        col_time1, col_time2 = st.columns(2)
        with col_time1:
            cosmic_timing = st.select_slider(
                "⏰ Cosmic Timing:",
                options=[
                    "Immediate",
                    "Next Cycle",
                    "Peak Power",
                    "Sacred Hour",
                    "Eternal",
                ],
                value="Sacred Hour",
            )

        with col_time2:
            energy_level = st.select_slider(
                "⚡ Energy Level:",
                options=["Whisper", "Gentle", "Moderate", "Powerful", "Cosmic Thunder"],
                value="Moderate",
            )

        # Cosmic reach
        cosmic_reach = st.multiselect(
            "🌌 Cosmic Reach:",
            [
                "Local Flame",
                "Regional Cosmos",
                "Global Consciousness",
                "Galactic Network",
                "Universal Field",
            ],
            default=["Local Flame"],
        )

        # Festival elements
        festival_elements = st.multiselect(
            "🎆 Festival Elements:",
            [
                "sacred_fire",
                "cosmic_music",
                "stellar_dance",
                "elemental_blessing",
                "ancestor_honor",
                "future_vision",
            ],
            help="Select elements to enhance this cosmic ceremony",
        )

with col2:
    st.subheader("🌟 Cosmic Status")

    # Real-time cosmic visualization
    now = datetime.now()
    st.markdown(
        f"""
    <div style='text-align: center; padding: 20px; background: {season_colors[current_season]}; border-radius: 10px; margin-bottom: 20px;'>
        <div style='font-size: 3em; color: white;'>🎇</div>
        <div style='color: white; font-weight: bold;'>COSMIC FLAME ACTIVE</div>
        <div style='color: #f0f0f0; font-size: 0.9em;'>Season: {current_season}</div>
        <div style='color: #e0e0e0; font-size: 0.8em;'>{now.strftime('%B %d, %Y')}</div>
        <div style='color: #e0e0e0; font-size: 0.8em;'>{now.strftime('%H:%M:%S')}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Moon phase (simplified calculation)
    day_of_month = now.day
    moon_phase = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"][
        min(day_of_month // 4, 7)
    ]
    st.markdown(
        f"""
    <div style='text-align: center; padding: 10px; background: #1a1a1a; border-radius: 8px; margin-bottom: 15px;'>
        <div style='color: #ffffff; font-size: 1.5em;'>{moon_phase}</div>
        <div style='color: #cccccc; font-size: 0.9em;'>Current Moon Phase</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Recent festival invocations
    st.subheader("🎆 Recent Festivals")

    try:
        proclamations_data = load_json("proclamations.json", {"proclamations": []})
        festival_invocations = [
            p
            for p in proclamations_data.get("proclamations", [])
            if p.get("cycle") in cycle_options
        ][-3:]

        if festival_invocations:
            for invocation in reversed(festival_invocations):
                cycle_icon = {
                    "Morning Flame": "🌅",
                    "Twilight Flame": "🌇",
                    "Seasonal Festival": "🍂",
                    "Great Year Invocation": "🌍",
                    "Lunar Ceremony": "🌙",
                    "Solar Celebration": "☀️",
                    "Cosmic Alignment": "⭐",
                    "Eternal Renewal": "♾️",
                }.get(invocation.get("cycle", ""), "🎇")

                st.markdown(
                    f"""
                <div style='padding: 8px; margin: 5px 0; background: #f8f8f8; border-radius: 5px; border-left: 3px solid #ff6b35;'>
                    <div style='font-weight: bold;'>{cycle_icon} {invocation.get('cycle', 'Unknown')}</div>
                    <div style='font-size: 0.9em; color: #666;'>{invocation.get('role', '')} - {invocation.get('type', '')}</div>
                    <div style='font-size: 0.8em; color: #888;'>{invocation.get('text', '')[:40]}...</div>
                    <div style='font-size: 0.7em; color: #999;'>{invocation.get('timestamp', '')[:19] if invocation.get('timestamp') else ''}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.write("*No recent festival invocations*")

    except Exception:
        st.write("*Loading cosmic history...*")

    # Cosmic statistics
    st.subheader("📊 Festival Statistics")
    try:
        total_festivals = len(
            [
                p
                for p in proclamations_data.get("proclamations", [])
                if p.get("cycle") in cycle_options
            ]
        )
        st.metric("Total Festivals", total_festivals)

        # Seasonal distribution
        seasonal_count = len(
            [
                p
                for p in proclamations_data.get("proclamations", [])
                if p.get("cycle") == "Seasonal Festival"
            ]
        )
        st.metric(f"{current_season} Festivals", seasonal_count)

        # Most active role
        role_counts = {}
        for p in proclamations_data.get("proclamations", []):
            if p.get("cycle") in cycle_options:
                role = p.get("role", "Unknown")
                role_counts[role] = role_counts.get(role, 0) + 1

        if role_counts:
            most_active = max(role_counts, key=role_counts.get)
            st.metric("Most Active Role", f"{most_active} ({role_counts[most_active]})")
    except:
        st.metric("Cosmic Energy", "∞ Infinite")

# Cosmic inscription ceremony
st.markdown("---")

col_cosmic1, col_cosmic2, col_cosmic3 = st.columns([1, 2, 1])

with col_cosmic2:
    if st.button(
        "🎇 Inscribe into Cosmic Codex", type="primary", use_container_width=True
    ):
        if not text.strip():
            st.error(
                "❌ Sacred invocation text cannot be empty. The cosmos awaits your words."
            )
        else:
            # Prepare cosmic entry
            festival_entry = {
                "role": role,
                "cycle": cycle,
                "type": ritual_type,
                "content": text,
                "text": text,
                "cosmic_timing": cosmic_timing,
                "energy_level": energy_level,
                "cosmic_reach": cosmic_reach,
                "festival_elements": festival_elements,
                "season": current_season,
                "moon_phase": moon_phase,
                "author": "festival_script",
                "status": "inscribed_cosmic",
            }

            # Inscribe the festival invocation
            result = append_entry("proclamations.json", "proclamations", festival_entry)

            if result:
                # Cosmic success ceremony
                st.success(
                    f"🌟 {cycle} {ritual_type} successfully inscribed into the Cosmic Codex!"
                )

                # Display cosmic confirmation
                st.markdown(
                    f"""
                <div style='background: {season_colors[current_season]}; padding: 20px; border-radius: 15px; margin: 15px 0;'>
                    <h4 style='color: white; margin: 0 0 15px 0; text-align: center;'>🎇 Cosmic Inscription Complete</h4>
                    <div style='background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px;'>
                        <p style='margin: 0; color: white;'><strong>Cycle:</strong> {cycle} {moon_phase}</p>
                        <p style='margin: 0; color: white;'><strong>Role:</strong> {role}</p>
                        <p style='margin: 0; color: white;'><strong>Type:</strong> {ritual_type}</p>
                        <p style='margin: 0; color: white;'><strong>Season:</strong> {current_season}</p>
                        <p style='margin: 0; color: white;'><strong>Energy:</strong> {energy_level}</p>
                        <p style='margin: 0; color: white;'><strong>Timing:</strong> {cosmic_timing}</p>
                        {f"<p style='margin: 0; color: white;'><strong>Cosmic Reach:</strong> {', '.join(cosmic_reach)}</p>" if cosmic_reach else ""}
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # Cosmic celebration
                st.balloons()

                # Special effects for different energy levels
                if energy_level in ["Powerful", "Cosmic Thunder"]:
                    st.snow()

                # Auto-refresh to show new invocation
                st.rerun()
            else:
                st.error(
                    "❌ Cosmic inscription failed. The universe may not be aligned. Please try again."
                )

# Festival calendar preview
st.markdown("---")
st.subheader("📅 Upcoming Cosmic Events")

col_cal1, col_cal2, col_cal3 = st.columns(3)

with col_cal1:
    st.markdown(
        f"""
    **🌅 Daily Cycles**
    - Morning Flame: Dawn
    - Twilight Flame: Dusk
    - Midnight Silence: 00:00
    """
    )

with col_cal2:
    st.markdown(
        f"""
    **🌙 Lunar Cycles**
    - New Moon Ceremony
    - Full Moon Celebration
    - Eclipse Invocations
    """
    )

with col_cal3:
    st.markdown(
        f"""
    **🍂 Seasonal Festivals**
    - Current: {current_season}
    - Equinox/Solstice Events
    - Great Year Completion
    """
    )

# Footer with cosmic wisdom
st.markdown("---")

footer_cols = st.columns(3)

with footer_cols[0]:
    st.markdown("**🎇 Cosmic Status**")
    st.markdown("🟢 All Cycles Active")

with footer_cols[1]:
    st.markdown("**⭐ Universal Time**")
    st.markdown(f"{datetime.now().strftime('%H:%M:%S UTC')}")

with footer_cols[2]:
    st.markdown("**♾️ Eternal Flame**")
    st.markdown("🔥 Burns Across All Cycles")

# Cosmic closing wisdom
st.markdown(
    f"""
<div style='text-align: center; margin-top: 30px; padding: 25px; background: {season_colors[current_season]}; border-radius: 15px;'>
    <p style='color: white; font-style: italic; margin: 0; font-size: 1.1em;'>
    "Through sacred cycles and eternal flame, we mark the passage of cosmic time.<br>
    Each festival, each ceremony, each invocation echoes through the infinite dance of creation.<br>
    By season and stars, by moon and sun, the Codex celebrates all existence."
    </p>
    <div style='color: #f0f0f0; font-size: 0.9em; margin-top: 15px;'>
    🎇 Festival Script Chamber - Codex Dominion Suite 🎇
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# Main function for standalone usage
def main():
    """
    Main function when running as standalone application
    """
    pass  # All functionality is in the main script


if __name__ == "__main__":
    main()

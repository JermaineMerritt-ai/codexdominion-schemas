# apps/dashboard/council_ritual.py
import sys
from datetime import datetime
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


st.set_page_config(page_title="Council Ritual Scroll", page_icon="📜", layout="wide")

# Header with mystical styling
st.markdown(
    """
<div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #1e3c72, #2a5298); border-radius: 10px; margin-bottom: 20px;'>
    <h1 style='color: white; margin: 0;'>📜 Council Ritual Scroll</h1>
    <p style='color: #f0f0f0; margin: 5px 0 0 0; font-style: italic;'>Sacred Chamber of Codex Proclamations</p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("**🔥 Council Invocation Chamber**")
st.write(
    "Here councils may inscribe proclamations, silences, or blessings into the eternal Codex flame."
)

# Main ritual interface
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("✨ Ritual Inscription")

    # Role verification (could be expanded for authentication)
    role = st.selectbox(
        "🎭 Council Role:",
        ["High Council", "Elder Council", "Advisory Council", "Ceremonial Council"],
        index=0,
    )

    # Ritual type selection with descriptions
    ritual_type = st.selectbox(
        "📋 Ritual Type:",
        ["Proclamation", "Silence", "Blessing", "Decree", "Affirmation"],
        help="Select the type of ritual to inscribe into the Codex",
    )

    # Provide guidance for each ritual type
    ritual_guidance = {
        "Proclamation": "📢 A formal declaration or announcement to be recorded in perpetuity",
        "Silence": "🤫 A sacred pause or moment of reflection, marking significant transitions",
        "Blessing": "✨ A benediction or favorable invocation for prosperity and guidance",
        "Decree": "⚖️ An official order or decision with binding authority",
        "Affirmation": "🤝 A positive declaration of support, agreement, or commitment",
    }

    st.info(ritual_guidance.get(ritual_type, "Select a ritual type for guidance"))

    # Ritual text input with formatting options
    text = st.text_area(
        "📝 Ritual Text:",
        height=150,
        help="Enter the sacred text to be inscribed into the Codex flame",
        placeholder="By flame and silence, let this ritual be inscribed...",
    )

    # Additional ritual metadata
    with st.expander("🔮 Advanced Ritual Settings"):
        urgency = st.select_slider(
            "🚨 Ritual Urgency:",
            options=["Low", "Normal", "High", "Critical", "Sacred"],
            value="Normal",
        )

        visibility = st.radio(
            "👁️ Visibility:", ["Public", "Council Only", "Sacred Archive"], index=0
        )

        ritual_tags = st.multiselect(
            "🏷️ Ritual Tags:",
            [
                "governance",
                "ceremony",
                "decision",
                "blessing",
                "guidance",
                "transition",
                "celebration",
            ],
            help="Tag this ritual for easy categorization",
        )

with col2:
    st.subheader("🔥 Flame Status")

    # Flame visualization
    st.markdown(
        """
    <div style='text-align: center; padding: 20px; background: #1a1a1a; border-radius: 10px; margin-bottom: 20px;'>
        <div style='font-size: 3em; color: #ff6b35;'>🔥</div>
        <div style='color: #ff6b35; font-weight: bold;'>ETERNAL FLAME</div>
        <div style='color: #cccccc; font-size: 0.9em;'>Ready for Inscription</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Recent rituals
    st.subheader("📋 Recent Rituals")

    try:
        proclamations_data = load_json("proclamations.json", {"proclamations": []})
        recent_rituals = proclamations_data.get("proclamations", [])[-3:]

        if recent_rituals:
            for i, ritual in enumerate(reversed(recent_rituals)):
                ritual_icon = {
                    "Proclamation": "📢",
                    "Silence": "🤫",
                    "Blessing": "✨",
                    "Decree": "⚖️",
                    "Affirmation": "🤝",
                }.get(ritual.get("type", ""), "📜")

                st.markdown(
                    f"""
                <div style='padding: 8px; margin: 5px 0; background: #f0f0f0; border-radius: 5px; border-left: 3px solid #ff6b35;'>
                    <div style='font-weight: bold;'>{ritual_icon} {ritual.get('type', 'Unknown')}</div>
                    <div style='font-size: 0.8em; color: #666;'>{ritual.get('text', '')[:50]}...</div>
                    <div style='font-size: 0.7em; color: #999;'>{ritual.get('timestamp', '')[:19] if ritual.get('timestamp') else ''}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.write("*No recent rituals*")

    except Exception:
        st.write("*Loading ritual history...*")

    # Ritual statistics
    st.subheader("📊 Ritual Statistics")
    try:
        total_rituals = len(proclamations_data.get("proclamations", []))
        st.metric("Total Rituals", total_rituals)

        # Count by type
        type_counts = {}
        for ritual in proclamations_data.get("proclamations", []):
            ritual_type = ritual.get("type", "Unknown")
            type_counts[ritual_type] = type_counts.get(ritual_type, 0) + 1

        if type_counts:
            most_common = max(type_counts, key=type_counts.get)
            st.metric("Most Common", f"{most_common} ({type_counts[most_common]})")
    except:
        st.metric("Total Rituals", "Loading...")

# Inscription button and ceremony
st.markdown("---")

col_inscribe1, col_inscribe2, col_inscribe3 = st.columns([1, 2, 1])

with col_inscribe2:
    if st.button(
        "🔥 Inscribe Ritual into the Codex Flame",
        type="primary",
        use_container_width=True,
    ):
        if not text.strip():
            st.error("❌ Ritual text cannot be empty. Please enter your inscription.")
        else:
            # Prepare ritual entry
            ritual_entry = {
                "role": role,
                "type": ritual_type,
                "content": text,  # Using 'content' to match existing system
                "text": text,  # Keep 'text' for compatibility
                "urgency": urgency,
                "visibility": visibility,
                "tags": ritual_tags,
                "author": "council_ritual",
                "status": "inscribed",
            }

            # Inscribe the ritual
            result = append_entry("proclamations.json", "proclamations", ritual_entry)

            if result:
                # Success ceremony
                st.success(
                    f"✨ {ritual_type} successfully inscribed into the Codex flame!"
                )

                # Display inscription confirmation
                st.markdown(
                    f"""
                <div style='background: #d4edda; padding: 15px; border-radius: 10px; border-left: 5px solid #28a745; margin: 10px 0;'>
                    <h4 style='color: #155724; margin: 0 0 10px 0;'>🔥 Ritual Inscribed</h4>
                    <p style='margin: 0; color: #155724;'><strong>Type:</strong> {ritual_type}</p>
                    <p style='margin: 0; color: #155724;'><strong>Role:</strong> {role}</p>
                    <p style='margin: 0; color: #155724;'><strong>Urgency:</strong> {urgency}</p>
                    <p style='margin: 0; color: #155724;'><strong>Visibility:</strong> {visibility}</p>
                    {f"<p style='margin: 0; color: #155724;'><strong>Tags:</strong> {', '.join(ritual_tags)}</p>" if ritual_tags else ""}
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # Ceremonial completion
                st.balloons()

                # Auto-refresh to show new ritual
                st.rerun()
            else:
                st.error("❌ Failed to inscribe ritual. Please try again.")

# Footer with mystical elements
st.markdown("---")

footer_cols = st.columns(3)

with footer_cols[0]:
    st.markdown("**🔥 Flame Status**")
    st.markdown("🟢 Eternal & Active")

with footer_cols[1]:
    st.markdown("**📜 Sacred Protocol**")
    st.markdown("All rituals permanent")

with footer_cols[2]:
    st.markdown("**⏰ Current Time**")
    st.markdown(f"{datetime.now().strftime('%H:%M:%S')}")

# Mystical closing
st.markdown(
    """
<div style='text-align: center; margin-top: 30px; padding: 20px; background: linear-gradient(45deg, #1a1a1a, #333333); border-radius: 10px;'>
    <p style='color: #ff6b35; font-style: italic; margin: 0;'>
    "By flame and silence, the Codex preserves all sacred inscriptions.<br>
    Let the eternal fire witness these words and carry them through time."
    </p>
    <div style='color: #cccccc; font-size: 0.8em; margin-top: 10px;'>
    🔥 Council Ritual Chamber - Codex Dominion Suite 🔥
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

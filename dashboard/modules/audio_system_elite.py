"""
🔊 TOP-TIER AUDIO SYSTEM - ELITE EDITION
High-fidelity audio generation, playback, and ceremonial voice synthesis
"""

import streamlit as st
import requests
import base64
import os
from typing import Optional


class AudioSystemElite:
    """Elite audio generation and playback system"""

    def __init__(self, backend_url: Optional[str] = None):
        self.backend_url = backend_url or os.environ.get(
            "BACKEND_URL",
            "https://codex-backend.azurewebsites.net"
        )
        self.voice_profiles = ["sovereign", "custodian", "oracle", "heir", "narrator"]

    def generate_audio(self, text: str, voice: str = "sovereign") -> Optional[str]:
        """
        Generate audio from text using backend API

        Args:
            text: Text to convert to audio
            voice: Voice profile to use

        Returns:
            Base64 encoded audio data or None on failure
        """
        payload = {"text": text, "voice": voice}

        try:
            response = requests.post(
                f"{self.backend_url}/audio/generate",
                json=payload,
                timeout=30
            )

            if response.status_code != 200:
                st.error(f"Audio generation failed with status {response.status_code}")
                return None

            audio_data = response.json().get("audio_base64")
            return audio_data

        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. Please try again.")
            return None
        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot connect to backend. Check your connection.")
            return None
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            return None

    def render_generation_ui(self):
        """Render the audio generation interface"""

        st.subheader("🎤 Generate Ceremonial Audio")

        user_text = st.text_area(
            "Enter text to convert into high‑fidelity audio",
            height=150,
            placeholder="Enter your ceremonial text here..."
        )

        col1, col2 = st.columns([3, 1])

        with col1:
            voice_choice = st.selectbox(
                "Choose Voice Profile",
                self.voice_profiles,
                index=0
            )

        with col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            generate_button = st.button("🎵 Generate Audio", use_container_width=True)

        if generate_button:
            if not user_text.strip():
                st.warning("⚠️ Please enter text to generate audio.")
            else:
                with st.spinner(f"🎨 Generating {voice_choice} voice..."):
                    audio_base64 = self.generate_audio(user_text, voice_choice)

                if audio_base64:
                    st.success("✅ Audio generated successfully!")

                    # Decode base64 to bytes
                    audio_bytes = base64.b64decode(audio_base64)

                    # Audio player
                    st.audio(audio_bytes, format="audio/mp3")

                    # Download button
                    st.download_button(
                        label="⬇️ Download Audio",
                        data=audio_bytes,
                        file_name=f"codex_{voice_choice}_audio.mp3",
                        mime="audio/mp3",
                        use_container_width=True
                    )

    def render_playback_ui(self):
        """Render the audio playback interface"""

        st.subheader("🎧 Audio Playback Module")

        uploaded_audio = st.file_uploader(
            "Upload an audio file",
            type=["mp3", "wav", "ogg", "m4a"],
            help="Supported formats: MP3, WAV, OGG, M4A"
        )

        if uploaded_audio:
            st.success(f"✅ Loaded: {uploaded_audio.name}")
            st.audio(uploaded_audio, format="audio/mp3")

            # Show file info
            file_size = len(uploaded_audio.getvalue()) / 1024  # KB
            st.info(f"📊 File size: {file_size:.2f} KB")

    def render_voice_profiles(self):
        """Render voice profile descriptions"""

        st.subheader("👥 Voice Profiles")

        profiles = {
            "sovereign": {
                "icon": "👑",
                "description": "Commanding, authoritative voice for royal proclamations"
            },
            "custodian": {
                "icon": "🛡️",
                "description": "Protective, wise voice for system guardianship"
            },
            "oracle": {
                "icon": "🔮",
                "description": "Mystical, prophetic voice for insights and predictions"
            },
            "heir": {
                "icon": "⚔️",
                "description": "Noble, earnest voice for successor communications"
            },
            "narrator": {
                "icon": "📖",
                "description": "Clear, professional voice for documentation and reports"
            }
        }

        cols = st.columns(len(profiles))

        for idx, (voice, info) in enumerate(profiles.items()):
            with cols[idx]:
                st.markdown(f"### {info['icon']} {voice.title()}")
                st.caption(info['description'])


def render_audio_system_elite():
    """Main render function for the audio system"""

    st.title("🔊 Top‑Tier Audio System — Elite Edition")
    st.write("High‑fidelity audio generation, playback, and ceremonial voice synthesis.")

    # Initialize audio system
    audio_system = AudioSystemElite()

    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["🎤 Generate", "🎧 Playback", "👥 Voice Profiles"])

    with tab1:
        audio_system.render_generation_ui()

    with tab2:
        audio_system.render_playback_ui()

    with tab3:
        audio_system.render_voice_profiles()

    # System info
    st.divider()
    with st.expander("ℹ️ System Information"):
        st.write(f"**Backend URL:** `{audio_system.backend_url}`")
        st.write(f"**Available Voices:** {len(audio_system.voice_profiles)}")
        st.write(f"**Supported Formats:** MP3, WAV, OGG, M4A")


if __name__ == "__main__":
    # For standalone testing
    st.set_page_config(
        page_title="Audio System Elite",
        page_icon="🔊",
        layout="wide"
    )
    render_audio_system_elite()

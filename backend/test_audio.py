"""
Test script for audio generation API
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.audio_engine import AudioEngine

def test_audio_generation():
    """Test audio generation with all voice profiles"""
    engine = AudioEngine()

    print("🎵 Testing Audio Engine")
    print("=" * 50)

    # Test text
    test_text = "The Council Seal has been established. Your sovereignty is recognized."

    # Test all voices
    for voice_info in engine.get_available_voices():
        voice_name = voice_info["name"]
        print(f"\n🎙️  Testing voice: {voice_name}")
        print(f"   Description: {voice_info['description']}")

        try:
            audio_base64 = engine.generate(test_text, voice_name)
            print(f"   ✅ Generated {len(audio_base64)} bytes of base64 audio")
        except Exception as e:
            print(f"   ❌ Error: {e}")

    print("\n" + "=" * 50)
    print("✅ Audio generation tests complete!")

if __name__ == "__main__":
    test_audio_generation()

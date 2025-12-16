"""
Audio Engine Service
Hybrid text-to-speech generation with free (gTTS) and premium voice profiles
"""

import base64
import io
import os
from typing import Dict, List, Optional
from gtts import gTTS
import logging

logger = logging.getLogger(__name__)

class AudioEngine:
    """
    Hybrid audio generation engine supporting both free and premium voices
    - Free voices: gTTS with multiple accents
    - Premium voices: High-quality AI voices (ElevenLabs, Azure TTS, etc.)
    """

    def __init__(self):
        """Initialize audio engine with free and premium voice profile mappings"""
        # Free voice profiles (gTTS)
        self.voice_profiles = {
            "sovereign": {
                "lang": "en",
                "tld": "com",
                "slow": False,
                "tier": "free",
                "description": "👑 Authoritative, warm, resonant — For proclamations, declarations, system-wide messages"
            },
            "custodian": {
                "lang": "en",
                "tld": "co.uk",
                "slow": False,
                "tier": "free",
                "description": "🛡️ Gentle, steady, reflective — For guidance, devotionals, meditations"
            },
            "oracle": {
                "lang": "en",
                "tld": "com.au",
                "slow": True,
                "tier": "free",
                "description": "🔮 Mystic, layered, ethereal — For ceremonial cycles, deep system messages"
            },
            "heir": {
                "lang": "en",
                "tld": "ca",
                "slow": False,
                "tier": "free",
                "description": "⚔️ Youthful, bright, hopeful — For capsules, onboarding, encouragement"
            },
            "narrator": {
                "lang": "en",
                "tld": "co.in",
                "slow": False,
                "tier": "free",
                "description": "📖 Neutral, clear, documentary — For analytics, logs, system summaries"
            },
            # Premium voice profiles
            "sovereign-premium": {
                "model_id": "premium_sovereign",
                "tier": "premium",
                "stability": 0.75,
                "similarity_boost": 0.85,
                "description": "🔥 Elite commanding voice with cinematic quality (Premium)"
            },
            "custodian-pro": {
                "model_id": "premium_custodian",
                "tier": "premium",
                "stability": 0.70,
                "similarity_boost": 0.80,
                "description": "🛡️ Professional guardian voice with warmth (Premium)"
            },
            "oracle-elite": {
                "model_id": "premium_oracle",
                "tier": "premium",
                "stability": 0.65,
                "similarity_boost": 0.90,
                "description": "🔮 Mystical wisdom voice with ethereal quality (Premium)"
            },
            "heir-ultimate": {
                "model_id": "premium_heir",
                "tier": "premium",
                "stability": 0.80,
                "similarity_boost": 0.75,
                "description": "⚔️ Dynamic youthful voice with energy (Premium)"
            },
            "narrator-master": {
                "model_id": "premium_narrator",
                "tier": "premium",
                "stability": 0.85,
                "similarity_boost": 0.70,
                "description": "📖 Professional narrator voice with clarity (Premium)"
            }
        }

        # Premium API configuration (set via environment variables)
        self.premium_api_key = os.getenv("PREMIUM_VOICE_API_KEY")
        self.premium_api_url = os.getenv("PREMIUM_VOICE_API_URL")
        self.premium_enabled = bool(self.premium_api_key)

    def generate(self, text: str, voice: str = "sovereign") -> str:
        """
        Generate audio from text using specified voice profile (free or premium)

        Args:
            text (str): Text to convert to speech
            voice (str): Voice profile name (default: "sovereign")

        Returns:
            str: Base64-encoded MP3 audio data

        Raises:
            ValueError: If voice profile is invalid or text is empty
            RuntimeError: If audio generation fails
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        if voice not in self.voice_profiles:
            available_voices = ", ".join(self.voice_profiles.keys())
            raise ValueError(
                f"Invalid voice '{voice}'. Available voices: {available_voices}"
            )

        profile = self.voice_profiles[voice]
        tier = profile.get("tier", "free")

        try:
            if tier == "premium":
                return self._generate_premium_audio(text, voice, profile)
            else:
                return self._generate_free_audio(text, voice, profile)
        except Exception as e:
            logger.error(f"Audio generation failed for voice '{voice}': {str(e)}")
            raise RuntimeError(f"Failed to generate audio: {str(e)}")

    def _generate_free_audio(self, text: str, voice: str, profile: Dict) -> str:
        """Generate audio using free gTTS service"""
        logger.info(f"Generating FREE audio with voice '{voice}' for {len(text)} characters")

        # Generate speech using gTTS
        tts = gTTS(
            text=text,
            lang=profile["lang"],
            tld=profile["tld"],
            slow=profile["slow"]
        )

        # Save to in-memory buffer
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        # Encode to base64
        audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')

        logger.info(f"Successfully generated {len(audio_base64)} bytes of FREE audio data")
        return audio_base64

    def _generate_premium_audio(self, text: str, voice: str, profile: Dict) -> str:
        """
        Generate audio using premium voice service (ElevenLabs, Azure TTS, etc.)

        This method integrates with premium voice APIs when PREMIUM_VOICE_API_KEY is set.
        Falls back to free gTTS if premium is unavailable.
        """
        if not self.premium_enabled:
            logger.warning(f"Premium voice '{voice}' requested but API key not configured. Falling back to free voice.")
            # Fallback to base voice (remove -premium, -pro, -elite, -ultimate, -master suffixes)
            base_voice = voice.split('-')[0]
            if base_voice in self.voice_profiles:
                return self._generate_free_audio(text, base_voice, self.voice_profiles[base_voice])
            else:
                return self._generate_free_audio(text, "sovereign", self.voice_profiles["sovereign"])

        logger.info(f"Generating PREMIUM audio with voice '{voice}' for {len(text)} characters")

        try:
            # Call premium voice synthesis method
            audio_bytes = self._synthesize_premium_audio(text, voice, profile)

            # Encode to base64
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

            logger.info(f"Successfully generated {len(audio_base64)} bytes of PREMIUM audio data")
            return audio_base64

        except Exception as e:
            logger.error(f"Premium audio generation failed: {str(e)}. Falling back to free voice.")
            base_voice = voice.split('-')[0]
            return self._generate_free_audio(text, base_voice, self.voice_profiles[base_voice])

    def _synthesize_premium_audio(self, text: str, voice: str, profile: Dict) -> bytes:
        """
        Synthesize audio using premium voice API - REPLACE THIS METHOD WITH YOUR API

        This is the single method you need to customize for your premium voice service.
        It should return raw audio bytes (MP3, WAV, etc.) - the calling method handles base64 encoding.

        Integration Examples:

        # ElevenLabs:
        # import requests
        # response = requests.post(
        #     f"https://api.elevenlabs.io/v1/text-to-speech/{profile['model_id']}",
        #     headers={"xi-api-key": self.premium_api_key},
        #     json={
        #         "text": text,
        #         "model_id": "eleven_monolingual_v1",
        #         "voice_settings": {
        #             "stability": profile["stability"],
        #             "similarity_boost": profile["similarity_boost"]
        #         }
        #     }
        # )
        # return response.content

        # Azure Cognitive Services:
        # import azure.cognitiveservices.speech as speechsdk
        # speech_config = speechsdk.SpeechConfig(subscription=self.premium_api_key, region="eastus")
        # speech_config.speech_synthesis_voice_name = profile["model_id"]
        # synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        # result = synthesizer.speak_text_async(text).get()
        # return result.audio_data

        # AWS Polly:
        # import boto3
        # polly = boto3.client('polly', aws_access_key_id=self.premium_api_key)
        # response = polly.synthesize_speech(
        #     Text=text,
        #     OutputFormat='mp3',
        #     VoiceId=profile["model_id"]
        # )
        # return response['AudioStream'].read()

        # Google Cloud TTS:
        # from google.cloud import texttospeech
        # client = texttospeech.TextToSpeechClient()
        # synthesis_input = texttospeech.SynthesisInput(text=text)
        # voice = texttospeech.VoiceSelectionParams(
        #     name=profile["model_id"],
        #     language_code="en-US"
        # )
        # audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        # response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        # return response.audio_content

        Args:
            text (str): Text to synthesize
            voice (str): Voice profile name (e.g., "sovereign-premium")
            profile (Dict): Voice configuration with model_id, stability, etc.

        Returns:
            bytes: Raw audio bytes (MP3 format recommended)
        """
        # PLACEHOLDER - Replace with your premium voice API call
        logger.warning(f"Premium API not implemented. Falling back to enhanced gTTS for '{voice}'")

        # Fallback to free voice for now
        base_voice = voice.split('-')[0]
        base_profile = self.voice_profiles.get(base_voice, self.voice_profiles["sovereign"])

        # Generate with gTTS and return raw bytes
        tts = gTTS(
            text=text,
            lang=base_profile["lang"],
            tld=base_profile["tld"],
            slow=False  # Premium voices should be natural speed
        )
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        return audio_buffer.read()  # Return raw bytes

    def get_available_voices(self) -> List[Dict[str, str]]:
        """
        Get list of available voice profiles with descriptions and tiers

        Returns:
            List[Dict]: List of voice profile information including tier status
        """
        voices = []
        for name, profile in self.voice_profiles.items():
            tier = profile.get("tier", "free")
            voice_info = {
                "name": name,
                "description": profile["description"],
                "tier": tier,
                "available": True if tier == "free" else self.premium_enabled
            }

            # Add tier-specific metadata
            if tier == "premium":
                voice_info["requires_api_key"] = not self.premium_enabled
                voice_info["fallback_voice"] = name.split('-')[0]
            else:
                voice_info["language"] = profile["lang"]
                voice_info["accent"] = profile["tld"]
                voice_info["slow_speech"] = profile["slow"]

            voices.append(voice_info)

        return voices

    def get_premium_status(self) -> Dict[str, any]:
        """Get premium voice service status"""
        return {
            "premium_enabled": self.premium_enabled,
            "api_configured": bool(self.premium_api_key),
            "total_voices": len(self.voice_profiles),
            "free_voices": sum(1 for p in self.voice_profiles.values() if p.get("tier") == "free"),
            "premium_voices": sum(1 for p in self.voice_profiles.values() if p.get("tier") == "premium"),
            "message": "Premium voices available" if self.premium_enabled else "Set PREMIUM_VOICE_API_KEY to enable premium voices"
        }

    def validate_voice(self, voice: str) -> bool:
        """Check if a voice profile exists"""
        return voice in self.voice_profiles

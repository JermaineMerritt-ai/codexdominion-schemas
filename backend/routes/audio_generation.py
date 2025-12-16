"""
Audio Generation API Router
Provides text-to-speech generation with multiple voice profiles
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
import sys
import os

# Add backend directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.audio_engine import AudioEngine

router = APIRouter(prefix="/audio", tags=["audio"])
engine = AudioEngine()

class AudioRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Text to convert to speech")
    voice: Literal[
        # Free voices
        "sovereign", "custodian", "oracle", "heir", "narrator",
        # Premium voices
        "sovereign-premium", "custodian-pro", "oracle-elite", "heir-ultimate", "narrator-master"
    ] = Field(
        default="sovereign",
        description="Voice profile to use for generation (free or premium)"
    )

class AudioResponse(BaseModel):
    audio_base64: str = Field(..., description="Base64-encoded audio data")
    voice: str = Field(..., description="Voice profile used")
    text_length: int = Field(..., description="Length of input text")
    format: str = Field(default="mp3", description="Audio format")
    tier: str = Field(default="free", description="Voice tier (free or premium)")

@router.post("/generate", response_model=AudioResponse)
async def generate_audio(req: AudioRequest):
    """
    Generate audio from text using specified voice profile

    **Free Voice Profiles:**
    - **sovereign**: Commanding, authoritative tone (US English)
    - **custodian**: Protective, reassuring tone (UK English)
    - **oracle**: Mystical, wise tone (Australian English, slower pace)
    - **heir**: Young, energetic tone (Canadian English)
    - **narrator**: Neutral, clear storytelling voice (Indian English)

    **Premium Voice Profiles** (requires PREMIUM_VOICE_API_KEY):
    - **sovereign-premium**: 🔥 Elite commanding voice with cinematic quality
    - **custodian-pro**: 🛡️ Professional guardian voice with warmth
    - **oracle-elite**: 🔮 Mystical wisdom voice with ethereal quality
    - **heir-ultimate**: ⚔️ Dynamic youthful voice with energy
    - **narrator-master**: 📖 Professional narrator voice with clarity

    **Returns:** Base64-encoded MP3 audio data

    **Note:** Premium voices automatically fall back to free versions if API key is not configured.
    """
    try:
        audio_base64 = engine.generate(req.text, req.voice)
        profile = engine.voice_profiles.get(req.voice, {})
        tier = profile.get("tier", "free")

        return AudioResponse(
            audio_base64=audio_base64,
            voice=req.voice,
            text_length=len(req.text),
            format="mp3",
            tier=tier
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Audio generation failed: {str(e)}"
        )

@router.get("/voices")
async def list_voices():
    """
    List all available voice profiles with descriptions and tier status

    Returns both free (gTTS) and premium voice options.
    Premium voices require PREMIUM_VOICE_API_KEY environment variable.
    """
    return {
        "voices": engine.get_available_voices(),
        "default": "sovereign",
        "total_voices": len(engine.voice_profiles),
        "premium_status": engine.get_premium_status()
    }

@router.get("/premium-status")
async def premium_status():
    """Check premium voice service availability"""
    return engine.get_premium_status()

@router.get("/health")
async def audio_health_check():
    """Health check for audio generation service"""
    status = engine.get_premium_status()
    return {
        "status": "healthy",
        "service": "audio-generation-hybrid",
        "voices_available": len(engine.get_available_voices()),
        "free_voices": status["free_voices"],
        "premium_voices": status["premium_voices"],
        "premium_enabled": status["premium_enabled"],
        "engine": "AudioEngine (gTTS + Premium)"
    }

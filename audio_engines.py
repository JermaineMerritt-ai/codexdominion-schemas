# ============================================================================================
# AUDIO GENERATION ENGINES - Modular Integration Layer
# ============================================================================================
"""
Audio generation engine integrations for the Audio Studio.

Supported engines:
- ElevenLabs: Voiceover and TTS (text-to-speech)
- Suno: Music generation
- Stability Audio: Sound effects and ambient audio
- AudioCraft: General audio generation (Meta)

Each engine implements the same interface:
    generate(prompt, **kwargs) -> Dict

Returns:
    {
        "success": bool,
        "audio_url": str,
        "duration": float,
        "sample_rate": int,
        "error": str (if success=False)
    }
"""

import os
import time
import requests
from typing import Dict, Any, Optional


# ============================================================================================
# ELEVENLABS - Voiceover & TTS
# ============================================================================================

class ElevenLabsAPIError(Exception):
    """Custom exception for ElevenLabs API errors."""
    pass


def generate_elevenlabs(
    text: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",  # Default voice (Rachel)
    model_id: str = "eleven_monolingual_v1",
    stability: float = 0.5,
    similarity_boost: float = 0.75,
    style: float = 0.0,
    **kwargs
) -> Dict[str, Any]:
    """Generate voiceover using ElevenLabs API.
    
    Args:
        text: Text to convert to speech
        voice_id: ElevenLabs voice ID
        model_id: Model to use (eleven_monolingual_v1, eleven_multilingual_v2, etc.)
        stability: Voice stability (0.0 to 1.0)
        similarity_boost: Voice similarity (0.0 to 1.0)
        style: Voice style/emotion (0.0 to 1.0)
    
    Returns:
        Dict with audio_url, duration, sample_rate
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("⚠️ ELEVENLABS_API_KEY not set - using placeholder")
        return generate_placeholder_audio("voiceover")
    
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        
        data = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost,
                "style": style,
                "use_speaker_boost": True
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            # Save audio file (would need storage integration)
            audio_url = f"https://storage.example.com/audio/{voice_id}_{int(time.time())}.mp3"
            
            return {
                "success": True,
                "audio_url": audio_url,
                "duration": estimate_duration_from_text(text),
                "sample_rate": 44100,
                "voice_id": voice_id,
                "engine": "elevenlabs"
            }
        else:
            raise ElevenLabsAPIError(f"ElevenLabs API error: {response.status_code} - {response.text}")
    
    except Exception as e:
        print(f"❌ ElevenLabs generation error: {e}")
        return generate_placeholder_audio("voiceover")


# ============================================================================================
# SUNO - Music Generation
# ============================================================================================

class SunoAPIError(Exception):
    """Custom exception for Suno API errors."""
    pass


def generate_suno(
    prompt: str,
    duration: int = 30,
    genre: Optional[str] = None,
    mood: Optional[str] = None,
    bpm: Optional[int] = None,
    key: Optional[str] = None,
    instrumental: bool = False,
    **kwargs
) -> Dict[str, Any]:
    """Generate music using Suno API.
    
    Args:
        prompt: Music description
        duration: Target duration in seconds
        genre: Musical genre
        mood: Emotional mood
        bpm: Beats per minute
        key: Musical key (C, D, Em, etc.)
        instrumental: Generate without vocals
    
    Returns:
        Dict with audio_url, duration, sample_rate
    """
    api_key = os.getenv("SUNO_API_KEY")
    if not api_key:
        print("⚠️ SUNO_API_KEY not set - using placeholder")
        return generate_placeholder_audio("music")
    
    try:
        # Build enhanced prompt
        enhanced_prompt = prompt
        if genre:
            enhanced_prompt += f", {genre} genre"
        if mood:
            enhanced_prompt += f", {mood} mood"
        if bpm:
            enhanced_prompt += f", {bpm} BPM"
        if key:
            enhanced_prompt += f", in {key}"
        if instrumental:
            enhanced_prompt += ", instrumental"
        
        url = "https://api.suno.ai/v1/generate"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "prompt": enhanced_prompt,
            "duration": duration,
            "make_instrumental": instrumental,
            "wait_audio": True  # Wait for generation to complete
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            
            return {
                "success": True,
                "audio_url": result.get("audio_url"),
                "duration": result.get("duration", duration),
                "sample_rate": 44100,
                "genre": genre,
                "mood": mood,
                "bpm": bpm,
                "key": key,
                "engine": "suno"
            }
        else:
            raise SunoAPIError(f"Suno API error: {response.status_code} - {response.text}")
    
    except Exception as e:
        print(f"❌ Suno generation error: {e}")
        return generate_placeholder_audio("music")


# ============================================================================================
# STABILITY AUDIO - Sound Effects & Ambient
# ============================================================================================

class StabilityAudioAPIError(Exception):
    """Custom exception for Stability Audio API errors."""
    pass


def generate_stability_audio(
    prompt: str,
    duration: int = 10,
    audio_type: str = "sfx",  # sfx, ambient
    negative_prompt: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """Generate sound effects or ambient audio using Stability Audio API.
    
    Args:
        prompt: Audio description
        duration: Duration in seconds (max 47)
        audio_type: Type of audio (sfx, ambient)
        negative_prompt: What to avoid
    
    Returns:
        Dict with audio_url, duration, sample_rate
    """
    api_key = os.getenv("STABILITY_API_KEY")
    if not api_key:
        print("⚠️ STABILITY_API_KEY not set - using placeholder")
        return generate_placeholder_audio(audio_type)
    
    try:
        url = "https://api.stability.ai/v2alpha/generation/audio"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "prompt": prompt,
            "duration": min(duration, 47),  # Max 47 seconds
            "output_format": "mp3"
        }
        
        if negative_prompt:
            data["negative_prompt"] = negative_prompt
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            
            return {
                "success": True,
                "audio_url": result.get("audio_url"),
                "duration": duration,
                "sample_rate": 44100,
                "audio_type": audio_type,
                "engine": "stability_audio"
            }
        else:
            raise StabilityAudioAPIError(f"Stability Audio API error: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Stability Audio generation error: {e}")
        return generate_placeholder_audio(audio_type)


# ============================================================================================
# AUDIOCRAFT - General Audio Generation (Meta)
# ============================================================================================

def generate_audiocraft(
    prompt: str,
    duration: int = 10,
    model: str = "musicgen-medium",  # musicgen-small, musicgen-medium, musicgen-large
    temperature: float = 1.0,
    top_k: int = 250,
    top_p: float = 0.0,
    **kwargs
) -> Dict[str, Any]:
    """Generate audio using AudioCraft (Meta) API.
    
    Args:
        prompt: Audio description
        duration: Duration in seconds
        model: AudioCraft model size
        temperature: Sampling temperature
        top_k: Top-k sampling
        top_p: Top-p sampling
    
    Returns:
        Dict with audio_url, duration, sample_rate
    """
    api_key = os.getenv("AUDIOCRAFT_API_KEY")
    if not api_key:
        print("⚠️ AUDIOCRAFT_API_KEY not set - using placeholder")
        return generate_placeholder_audio("music")
    
    try:
        url = "https://api.audiocraft.ai/v1/generate"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "prompt": prompt,
            "duration": duration,
            "model": model,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            
            return {
                "success": True,
                "audio_url": result.get("audio_url"),
                "duration": duration,
                "sample_rate": 32000,  # AudioCraft typically uses 32kHz
                "model": model,
                "engine": "audiocraft"
            }
        else:
            return generate_placeholder_audio("music")
    
    except Exception as e:
        print(f"❌ AudioCraft generation error: {e}")
        return generate_placeholder_audio("music")


# ============================================================================================
# HELPER FUNCTIONS
# ============================================================================================

def estimate_duration_from_text(text: str, words_per_minute: int = 150) -> float:
    """Estimate audio duration from text length."""
    word_count = len(text.split())
    duration_minutes = word_count / words_per_minute
    return duration_minutes * 60  # Convert to seconds


def generate_placeholder_audio(audio_type: str = "music") -> Dict[str, Any]:
    """Generate placeholder audio result for development."""
    placeholder_urls = {
        "music": "https://example.com/placeholder-music.mp3",
        "voiceover": "https://example.com/placeholder-voice.mp3",
        "sfx": "https://example.com/placeholder-sfx.mp3",
        "ambient": "https://example.com/placeholder-ambient.mp3"
    }
    
    return {
        "success": True,
        "audio_url": placeholder_urls.get(audio_type, placeholder_urls["music"]),
        "duration": 10.0,
        "sample_rate": 44100,
        "engine": "placeholder",
        "note": "Placeholder audio - configure API keys for real generation"
    }


# ============================================================================================
# PHASE 8 EXPANSION: NEW ENGINE INTEGRATIONS
# ============================================================================================

# ========== PLAY.HT - Advanced Voice Generation ==========

class PlayHTAPIError(Exception):
    """Custom exception for Play.ht API errors."""
    pass


def generate_playht(
    text: str,
    voice: str = "larry",  # Default voice
    voice_engine: str = "PlayHT2.0",
    speed: float = 1.0,
    temperature: float = 1.0,
    quality: str = "medium",  # draft, low, medium, high, premium
    output_format: str = "mp3",
    sample_rate: int = 44100,
    **kwargs
) -> Dict[str, Any]:
    """Generate voiceover using Play.ht API.
    
    Args:
        text: Text to convert to speech
        voice: Voice name or ID
        voice_engine: Voice engine (PlayHT2.0, PlayHT1.0)
        speed: Playback speed (0.5 to 2.0)
        temperature: Voice variation (0.0 to 2.0)
        quality: Audio quality level
        output_format: mp3, wav, flac, ogg
        sample_rate: 8000, 16000, 24000, 44100, 48000
    
    Returns:
        Dict with audio_url, duration, sample_rate
    """
    api_key = os.getenv("PLAYHT_API_KEY")
    user_id = os.getenv("PLAYHT_USER_ID")
    
    if not api_key or not user_id:
        print("⚠️ PLAYHT_API_KEY or PLAYHT_USER_ID not set - using placeholder")
        return generate_placeholder_audio("voiceover")
    
    try:
        url = "https://api.play.ht/api/v2/tts/stream"
        
        headers = {
            "Authorization": api_key,
            "X-User-Id": user_id,
            "Content-Type": "application/json"
        }
        
        data = {
            "text": text,
            "voice": voice,
            "voice_engine": voice_engine,
            "speed": speed,
            "temperature": temperature,
            "quality": quality,
            "output_format": output_format,
            "sample_rate": sample_rate
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            
            return {
                "success": True,
                "audio_url": result.get("url"),
                "duration": estimate_duration_from_text(text),
                "sample_rate": sample_rate,
                "voice": voice,
                "voice_engine": voice_engine,
                "engine": "playht"
            }
        else:
            raise PlayHTAPIError(f"Play.ht API error: {response.status_code} - {response.text}")
    
    except Exception as e:
        print(f"❌ Play.ht generation error: {e}")
        return generate_placeholder_audio("voiceover")


# ========== AZURE NEURAL VOICES - Enterprise TTS ==========

def generate_azure_voice(
    text: str,
    voice_name: str = "en-US-JennyNeural",
    style: Optional[str] = None,  # angry, cheerful, excited, friendly, hopeful, sad, etc.
    style_degree: float = 1.0,
    rate: str = "0%",  # -50% to +50%
    pitch: str = "0%",  # -50% to +50%
    output_format: str = "audio-24khz-48kbitrate-mono-mp3",
    **kwargs
) -> Dict[str, Any]:
    """Generate voiceover using Azure Neural Voices API.
    
    Args:
        text: Text to convert to speech
        voice_name: Azure voice name (e.g., en-US-JennyNeural)
        style: Voice style/emotion (if supported by voice)
        style_degree: Style intensity (0.01 to 2.0)
        rate: Speaking rate adjustment
        pitch: Pitch adjustment
        output_format: Azure audio format string
    
    Returns:
        Dict with audio_url, duration, sample_rate
    """
    api_key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_SPEECH_REGION", "eastus")
    
    if not api_key:
        print("⚠️ AZURE_SPEECH_KEY not set - using placeholder")
        return generate_placeholder_audio("voiceover")
    
    try:
        url = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
        
        headers = {
            "Ocp-Apim-Subscription-Key": api_key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": output_format
        }
        
        # Build SSML
        ssml = f"""<speak version='1.0' xml:lang='en-US'>
            <voice name='{voice_name}'>"""
        
        if style:
            ssml += f"""
                <mstts:express-as style='{style}' styledegree='{style_degree}'>
                    <prosody rate='{rate}' pitch='{pitch}'>
                        {text}
                    </prosody>
                </mstts:express-as>"""
        else:
            ssml += f"""
                <prosody rate='{rate}' pitch='{pitch}'>
                    {text}
                </prosody>"""
        
        ssml += """
            </voice>
        </speak>"""
        
        response = requests.post(url, headers=headers, data=ssml.encode('utf-8'))
        
        if response.status_code == 200:
            # Would save audio file
            audio_url = f"https://storage.example.com/azure_voice_{int(time.time())}.mp3"
            
            return {
                "success": True,
                "audio_url": audio_url,
                "duration": estimate_duration_from_text(text),
                "sample_rate": 24000,
                "voice_name": voice_name,
                "style": style,
                "engine": "azure_voice"
            }
        else:
            print(f"❌ Azure Voice error: {response.status_code}")
            return generate_placeholder_audio("voiceover")
    
    except Exception as e:
        print(f"❌ Azure Voice generation error: {e}")
        return generate_placeholder_audio("voiceover")


# ========== OPENVOICE - Open-Source Voice Cloning ==========

def generate_openvoice(
    text: str,
    reference_audio: Optional[str] = None,
    tone_color: Optional[str] = None,
    speed: float = 1.0,
    language: str = "en",
    **kwargs
) -> Dict[str, Any]:
    """Generate voiceover using OpenVoice (voice cloning).
    
    Args:
        text: Text to convert to speech
        reference_audio: URL or path to reference voice audio
        tone_color: Pre-defined tone color ID
        speed: Speech speed (0.5 to 2.0)
        language: Language code (en, zh, es, fr, etc.)
    
    Returns:
        Dict with audio_url, duration, sample_rate
    """
    api_endpoint = os.getenv("OPENVOICE_API_URL", "http://localhost:8000")
    
    try:
        url = f"{api_endpoint}/v1/generate"
        
        data = {
            "text": text,
            "language": language,
            "speed": speed
        }
        
        if reference_audio:
            data["reference_audio"] = reference_audio
        if tone_color:
            data["tone_color"] = tone_color
        
        response = requests.post(url, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            
            return {
                "success": True,
                "audio_url": result.get("audio_url"),
                "duration": estimate_duration_from_text(text),
                "sample_rate": 24000,
                "language": language,
                "engine": "openvoice"
            }
        else:
            print(f"❌ OpenVoice error: {response.status_code}")
            return generate_placeholder_audio("voiceover")
    
    except Exception as e:
        print(f"❌ OpenVoice generation error: {e}")
        return generate_placeholder_audio("voiceover")


# ========== UDIO - Advanced Music Generation ==========

class UdioAPIError(Exception):
    """Custom exception for Udio API errors."""
    pass


def generate_udio(
    prompt: str,
    duration: int = 30,
    genre: Optional[str] = None,
    mood: Optional[str] = None,
    tempo: Optional[str] = None,  # slow, medium, fast
    energy: Optional[str] = None,  # low, medium, high
    vocals: bool = True,
    **kwargs
) -> Dict[str, Any]:
    """Generate music using Udio API.
    
    Args:
        prompt: Music description
        duration: Target duration in seconds
        genre: Musical genre
        mood: Emotional mood
        tempo: Tempo description
        energy: Energy level
        vocals: Include vocals
    
    Returns:
        Dict with audio_url, duration, sample_rate
    """
    api_key = os.getenv("UDIO_API_KEY")
    
    if not api_key:
        print("⚠️ UDIO_API_KEY not set - using placeholder")
        return generate_placeholder_audio("music")
    
    try:
        # Build enhanced prompt
        enhanced_prompt = prompt
        if genre:
            enhanced_prompt += f", {genre}"
        if mood:
            enhanced_prompt += f", {mood} mood"
        if tempo:
            enhanced_prompt += f", {tempo} tempo"
        if energy:
            enhanced_prompt += f", {energy} energy"
        if not vocals:
            enhanced_prompt += ", instrumental"
        
        url = "https://api.udio.com/v1/generate"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "prompt": enhanced_prompt,
            "duration": duration,
            "include_vocals": vocals
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            
            # Poll for completion if needed
            generation_id = result.get("id")
            audio_url = result.get("audio_url")
            
            if not audio_url and generation_id:
                audio_url = poll_udio_generation(api_key, generation_id)
            
            return {
                "success": True,
                "audio_url": audio_url,
                "duration": duration,
                "sample_rate": 44100,
                "genre": genre,
                "mood": mood,
                "engine": "udio"
            }
        else:
            raise UdioAPIError(f"Udio API error: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Udio generation error: {e}")
        return generate_placeholder_audio("music")


def poll_udio_generation(api_key: str, generation_id: str, max_wait: int = 120) -> Optional[str]:
    """Poll Udio API for generation completion."""
    url = f"https://api.udio.com/v1/generations/{generation_id}"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    for _ in range(max_wait // 5):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "completed":
                return result.get("audio_url")
        time.sleep(5)
    
    return None


# ========== RIFFUSION - Real-Time Music Generation ==========

def generate_riffusion(
    prompt: str,
    negative_prompt: Optional[str] = None,
    duration: int = 5,  # Riffusion generates short clips
    seed: Optional[int] = None,
    num_inference_steps: int = 50,
    guidance_scale: float = 7.0,
    **kwargs
) -> Dict[str, Any]:
    """Generate music using Riffusion (Stable Diffusion for audio).
    
    Args:
        prompt: Music description
        negative_prompt: What to avoid
        duration: Duration in seconds (typically 5-10)
        seed: Random seed for reproducibility
        num_inference_steps: Number of diffusion steps
        guidance_scale: Prompt adherence strength
    
    Returns:
        Dict with audio_url, duration, sample_rate
    """
    api_endpoint = os.getenv("RIFFUSION_API_URL", "http://localhost:3000")
    
    try:
        url = f"{api_endpoint}/api/generate"
        
        data = {
            "prompt": prompt,
            "duration": duration,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale
        }
        
        if negative_prompt:
            data["negative_prompt"] = negative_prompt
        if seed is not None:
            data["seed"] = seed
        
        response = requests.post(url, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            
            return {
                "success": True,
                "audio_url": result.get("audio_url") or result.get("url"),
                "duration": duration,
                "sample_rate": 44100,
                "seed": seed,
                "engine": "riffusion"
            }
        else:
            print(f"❌ Riffusion error: {response.status_code}")
            return generate_placeholder_audio("music")
    
    except Exception as e:
        print(f"❌ Riffusion generation error: {e}")
        return generate_placeholder_audio("music")


# ========== FOLEY GENERATOR - Realistic Sound Effects ==========

def generate_foley(
    action: str,
    surface: Optional[str] = None,
    intensity: str = "medium",  # soft, medium, hard
    duration: float = 1.0,
    variation: int = 1,  # Number of variations to generate
    **kwargs
) -> Dict[str, Any]:
    """Generate Foley sound effects (procedural or ML-based).
    
    Args:
        action: Action type (footstep, door, impact, etc.)
        surface: Surface material (wood, concrete, metal, grass, etc.)
        intensity: Impact intensity
        duration: Duration in seconds
        variation: Variation number (for multiple takes)
    
    Returns:
        Dict with audio_url, duration, sample_rate
    """
    # Build descriptive prompt for Foley generation
    prompt = f"{action} sound"
    if surface:
        prompt += f" on {surface}"
    prompt += f", {intensity} intensity"
    
    # Use Stability Audio as Foley engine
    return generate_stability_audio(
        prompt=prompt,
        duration=duration,
        audio_type="sfx",
        **kwargs
    )

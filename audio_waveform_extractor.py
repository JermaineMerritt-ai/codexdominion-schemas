# ============================================================================================
# AUDIO WAVEFORM EXTRACTOR - Automatic Waveform + Metadata Extraction
# ============================================================================================
"""
Automatic waveform and metadata extraction for generated audio.

Features:
- Waveform data extraction
- Duration calculation
- Loudness analysis (RMS, peak, LUFS)
- Tag generation
- Category detection
- Visual waveform generation (PNG)

Uses:
- librosa: Audio analysis
- pydub: Audio loading
- matplotlib: Waveform visualization
- numpy: Data processing
"""

import os
import io
import base64
from typing import Dict, Any, List, Optional, Tuple
import numpy as np


class AudioWaveformExtractor:
    """Extract waveform data and metadata from audio files."""
    
    def __init__(self):
        """Initialize extractor with optional librosa import."""
        self.has_librosa = False
        self.has_pydub = False
        
        try:
            import librosa
            self.librosa = librosa
            self.has_librosa = True
        except ImportError:
            print("⚠️ librosa not installed - using fallback waveform generation")
        
        try:
            from pydub import AudioSegment
            self.AudioSegment = AudioSegment
            self.has_pydub = True
        except ImportError:
            print("⚠️ pydub not installed - limited audio loading")
    
    def extract_complete(
        self,
        audio_url: str,
        audio_type: str = "music",
        prompt: Optional[str] = None,
        engine: Optional[str] = None
    ) -> Dict[str, Any]:
        """Complete extraction pipeline.
        
        Returns:
            {
                "waveform_data": List[float],
                "waveform_url": str (PNG image URL),
                "duration": float,
                "sample_rate": int,
                "channels": int,
                "loudness": {
                    "rms_db": float,
                    "peak_db": float,
                    "lufs": float
                },
                "tags": List[str],
                "category": str,
                "metadata": Dict
            }
        """
        # Download audio (if URL)
        audio_path = self._download_audio(audio_url)
        
        # Extract waveform
        waveform_data, sample_rate = self._extract_waveform(audio_path)
        
        # Calculate duration
        duration = len(waveform_data) / sample_rate
        
        # Analyze loudness
        loudness = self._analyze_loudness(waveform_data, sample_rate)
        
        # Generate tags
        tags = self._generate_tags(audio_type, prompt, engine)
        
        # Detect category
        category = self._detect_category(audio_type, prompt)
        
        # Generate waveform image
        waveform_url = self._generate_waveform_image(waveform_data, sample_rate)
        
        # Extract additional metadata
        metadata = self._extract_metadata(audio_path, prompt)
        
        return {
            "waveform_data": waveform_data.tolist() if isinstance(waveform_data, np.ndarray) else waveform_data,
            "waveform_url": waveform_url,
            "duration": duration,
            "sample_rate": sample_rate,
            "channels": 1 if waveform_data.ndim == 1 else waveform_data.shape[0],
            "loudness": loudness,
            "tags": tags,
            "category": category,
            "metadata": metadata
        }
    
    def _download_audio(self, audio_url: str) -> str:
        """Download audio file from URL to temp location."""
        import tempfile
        import requests
        
        if audio_url.startswith("http"):
            response = requests.get(audio_url, stream=True)
            
            suffix = ".mp3"
            if "wav" in audio_url:
                suffix = ".wav"
            elif "flac" in audio_url:
                suffix = ".flac"
            
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            temp_file.write(response.content)
            temp_file.close()
            
            return temp_file.name
        else:
            return audio_url  # Local file
    
    def _extract_waveform(self, audio_path: str) -> Tuple[np.ndarray, int]:
        """Extract waveform data from audio file.
        
        Returns:
            (waveform_data, sample_rate)
        """
        if self.has_librosa:
            try:
                y, sr = self.librosa.load(audio_path, sr=None, mono=True)
                return y, sr
            except Exception as e:
                print(f"❌ Librosa loading error: {e}")
        
        if self.has_pydub:
            try:
                audio = self.AudioSegment.from_file(audio_path)
                sample_rate = audio.frame_rate
                
                # Convert to mono
                if audio.channels > 1:
                    audio = audio.set_channels(1)
                
                # Get raw audio data
                samples = np.array(audio.get_array_of_samples())
                
                # Normalize to -1.0 to 1.0
                waveform = samples / (2 ** (audio.sample_width * 8 - 1))
                
                return waveform, sample_rate
            except Exception as e:
                print(f"❌ Pydub loading error: {e}")
        
        # Fallback: Generate placeholder waveform
        print("⚠️ Using placeholder waveform - install librosa or pydub for real extraction")
        return self._generate_placeholder_waveform(), 44100
    
    def _generate_placeholder_waveform(self, duration: float = 10.0, sample_rate: int = 44100) -> np.ndarray:
        """Generate placeholder waveform for development."""
        num_samples = int(duration * sample_rate)
        
        # Generate sine wave with random modulation
        t = np.linspace(0, duration, num_samples)
        frequency = 440.0  # A440
        waveform = 0.3 * np.sin(2 * np.pi * frequency * t)
        
        # Add some variation
        waveform += 0.1 * np.random.randn(num_samples)
        
        return waveform
    
    def _analyze_loudness(self, waveform: np.ndarray, sample_rate: int) -> Dict[str, float]:
        """Analyze audio loudness (RMS, peak, LUFS).
        
        Returns:
            {
                "rms_db": float,
                "peak_db": float,
                "lufs": float (integrated loudness)
            }
        """
        # RMS (Root Mean Square) in dB
        rms = np.sqrt(np.mean(waveform ** 2))
        rms_db = 20 * np.log10(rms) if rms > 0 else -96.0
        
        # Peak level in dB
        peak = np.max(np.abs(waveform))
        peak_db = 20 * np.log10(peak) if peak > 0 else -96.0
        
        # LUFS (approximate - proper LUFS requires K-weighting)
        # For now, use RMS as approximation
        lufs = rms_db + 3.0  # Rough approximation
        
        return {
            "rms_db": float(rms_db),
            "peak_db": float(peak_db),
            "lufs": float(lufs)
        }
    
    def _generate_tags(
        self,
        audio_type: str,
        prompt: Optional[str],
        engine: Optional[str]
    ) -> List[str]:
        """Generate tags from audio type, prompt, and engine."""
        tags = [audio_type]
        
        if engine:
            tags.append(engine)
        
        if prompt:
            # Extract keywords from prompt
            keywords = ["music", "voice", "ambient", "sfx", "orchestral", "electronic",
                       "calm", "energetic", "dark", "bright", "epic", "cinematic"]
            
            prompt_lower = prompt.lower()
            for keyword in keywords:
                if keyword in prompt_lower:
                    tags.append(keyword)
        
        return list(set(tags))  # Remove duplicates
    
    def _detect_category(self, audio_type: str, prompt: Optional[str]) -> str:
        """Detect audio category from type and prompt."""
        if audio_type in ["voiceover", "voice", "speech", "tts"]:
            return "voice"
        elif audio_type in ["music", "song", "melody"]:
            if prompt and any(word in prompt.lower() for word in ["orchestral", "classical", "symphony"]):
                return "orchestral_music"
            elif prompt and any(word in prompt.lower() for word in ["electronic", "edm", "techno"]):
                return "electronic_music"
            else:
                return "music"
        elif audio_type in ["sfx", "sound_effect"]:
            return "sound_effects"
        elif audio_type in ["ambient", "atmosphere"]:
            return "ambience"
        else:
            return "audio"
    
    def _generate_waveform_image(
        self,
        waveform: np.ndarray,
        sample_rate: int,
        width: int = 800,
        height: int = 200
    ) -> str:
        """Generate waveform visualization as PNG image.
        
        Returns:
            Data URL (base64 encoded PNG)
        """
        try:
            import matplotlib
            matplotlib.use('Agg')  # Non-interactive backend
            import matplotlib.pyplot as plt
            
            # Create figure
            fig, ax = plt.subplots(figsize=(width / 100, height / 100), dpi=100)
            
            # Plot waveform
            time_axis = np.arange(len(waveform)) / sample_rate
            ax.plot(time_axis, waveform, color='#FFD700', linewidth=0.5)  # Gold color
            ax.fill_between(time_axis, waveform, alpha=0.3, color='#FFD700')
            
            # Style
            ax.set_xlim(0, len(waveform) / sample_rate)
            ax.set_ylim(-1.0, 1.0)
            ax.set_facecolor('#0F172A')  # Dark background
            fig.patch.set_facecolor('#0F172A')
            ax.tick_params(colors='#CBD5E1')
            ax.spines['bottom'].set_color('#CBD5E1')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#CBD5E1')
            
            # Save to bytes
            buf = io.BytesIO()
            plt.savefig(buf, format='png', facecolor='#0F172A', edgecolor='none')
            buf.seek(0)
            
            # Encode as base64
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            data_url = f"data:image/png;base64,{img_base64}"
            
            plt.close(fig)
            
            return data_url
        
        except ImportError:
            print("⚠️ matplotlib not installed - returning placeholder waveform URL")
            return "https://via.placeholder.com/800x200/0F172A/FFD700?text=Waveform"
        except Exception as e:
            print(f"❌ Waveform generation error: {e}")
            return "https://via.placeholder.com/800x200/0F172A/FFD700?text=Waveform+Error"
    
    def _extract_metadata(self, audio_path: str, prompt: Optional[str]) -> Dict[str, Any]:
        """Extract additional metadata from audio file."""
        metadata = {
            "file_size_bytes": 0,
            "format": "unknown",
            "bitrate": 0,
            "codec": "unknown"
        }
        
        try:
            # Get file size
            metadata["file_size_bytes"] = os.path.getsize(audio_path)
            
            # Detect format from extension
            ext = os.path.splitext(audio_path)[1].lower()
            metadata["format"] = ext[1:] if ext else "unknown"
            
            # Try to extract more with pydub
            if self.has_pydub:
                audio = self.AudioSegment.from_file(audio_path)
                metadata["bitrate"] = audio.frame_rate * audio.frame_width * 8 * audio.channels
                metadata["codec"] = "pcm" if ext == ".wav" else ext[1:]
        
        except Exception as e:
            print(f"⚠️ Metadata extraction warning: {e}")
        
        if prompt:
            metadata["prompt"] = prompt
        
        return metadata
    
    def downsample_waveform(
        self,
        waveform: np.ndarray,
        target_points: int = 1000
    ) -> List[float]:
        """Downsample waveform to target number of points for visualization.
        
        Useful for reducing data size for frontend display.
        """
        if len(waveform) <= target_points:
            return waveform.tolist() if isinstance(waveform, np.ndarray) else waveform
        
        # Calculate window size
        window_size = len(waveform) // target_points
        
        # Downsample by taking max absolute value in each window
        downsampled = []
        for i in range(0, len(waveform), window_size):
            window = waveform[i:i + window_size]
            if len(window) > 0:
                max_val = np.max(np.abs(window))
                downsampled.append(float(max_val * np.sign(np.mean(window))))
        
        return downsampled[:target_points]

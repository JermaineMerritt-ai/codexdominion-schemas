"""
🎨 Graphics Engines - Multi-AI Image Generation Interface
===========================================================

Unified interface for 3 major AI image generation engines:
- DALL-E 3 (OpenAI) - High quality, precise prompt following
- Midjourney v6 (via unofficial API) - Artistic, creative generation
- Stable Diffusion XL (Stability AI) - Fast, flexible, customizable

Usage:
------
from graphics_engines import DallEEngine, MidjourneyEngine, StableDiffusionEngine

# DALL-E 3
dalle = DallEEngine(api_key="sk-...")
result = dalle.generate("A serene mountain landscape at sunset", size="1024x1024", quality="hd")

# Midjourney
midjourney = MidjourneyEngine(api_key="mj-...")
result = midjourney.generate("Epic fantasy castle, dramatic lighting --v 6 --ar 16:9")

# Stable Diffusion XL
sd = StableDiffusionEngine(api_key="sk-...")
result = sd.generate("Cyberpunk cityscape with neon lights", style_preset="neon-punk")
"""

import os
import time
import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


# ============================================================================
# ENUMS & CONSTANTS
# ============================================================================

class ImageSize(Enum):
    """Standard image sizes"""
    SQUARE_1024 = "1024x1024"
    SQUARE_512 = "512x512"
    LANDSCAPE_1792_1024 = "1792x1024"
    PORTRAIT_1024_1792 = "1024x1792"
    WIDESCREEN_16_9 = "1920x1080"
    VERTICAL_9_16 = "1080x1920"


class ImageQuality(Enum):
    """Image quality presets"""
    STANDARD = "standard"
    HD = "hd"
    ULTRA = "ultra"


class StylePreset(Enum):
    """Stable Diffusion style presets"""
    ENHANCE = "enhance"
    ANIME = "anime"
    PHOTOGRAPHIC = "photographic"
    DIGITAL_ART = "digital-art"
    COMIC_BOOK = "comic-book"
    FANTASY_ART = "fantasy-art"
    LINE_ART = "line-art"
    ANALOG_FILM = "analog-film"
    NEON_PUNK = "neon-punk"
    ISOMETRIC = "isometric"
    LOW_POLY = "low-poly"
    ORIGAMI = "origami"
    MODELING_COMPOUND = "modeling-compound"
    CINEMATIC = "cinematic"
    THREE_D_MODEL = "3d-model"
    PIXEL_ART = "pixel-art"


# ============================================================================
# DALL-E 3 ENGINE
# ============================================================================

class DallEEngine:
    """
    OpenAI DALL-E 3 - High quality, precise prompt following
    
    Features:
    - Best-in-class prompt understanding
    - HD quality option
    - Multiple sizes (1024x1024, 1792x1024, 1024x1792)
    - Built-in content policy
    
    Limitations:
    - Max 1 image per request (no batch)
    - No style presets (uses natural language)
    - Higher cost than alternatives
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1/images/generations"
        self.model = "dall-e-3"
        
        if not self.api_key:
            raise ValueError("DALL-E API key required (OPENAI_API_KEY)")
    
    def generate(
        self,
        prompt: str,
        size: str = "1024x1024",
        quality: str = "standard",
        style: str = "vivid",
        n: int = 1
    ) -> Dict[str, Any]:
        """
        Generate image with DALL-E 3
        
        Args:
            prompt: Image description (max 4000 chars)
            size: Image size ("1024x1024", "1792x1024", "1024x1792")
            quality: Image quality ("standard" or "hd")
            style: Image style ("vivid" or "natural")
            n: Number of images (always 1 for DALL-E 3)
        
        Returns:
            {
                "image_url": "https://...",
                "revised_prompt": "Enhanced prompt used by DALL-E",
                "engine": "dall-e-3",
                "size": "1024x1024",
                "quality": "hd",
                "generated_at": "2025-12-22T10:30:00Z"
            }
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "n": 1,  # DALL-E 3 only supports 1 image
            "size": size,
            "quality": quality,
            "style": style,
            "response_format": "url"
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            
            result = data["data"][0]
            
            return {
                "image_url": result["url"],
                "revised_prompt": result.get("revised_prompt", prompt),
                "engine": "dall-e-3",
                "size": size,
                "quality": quality,
                "style": style,
                "generated_at": datetime.utcnow().isoformat() + "Z"
            }
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️ DALL-E generation failed: {e}")
            # Return placeholder
            return {
                "image_url": f"https://via.placeholder.com/{size.replace('x', 'x')}/FF6B6B/FFFFFF?text=DALL-E+Error",
                "revised_prompt": prompt,
                "engine": "dall-e-3",
                "error": str(e),
                "generated_at": datetime.utcnow().isoformat() + "Z"
            }
    
    def edit(
        self,
        image_path: str,
        mask_path: str,
        prompt: str,
        size: str = "1024x1024",
        n: int = 1
    ) -> Dict[str, Any]:
        """
        Edit image with DALL-E (inpainting)
        
        Args:
            image_path: Path to original image (PNG, max 4MB)
            mask_path: Path to mask image (transparent areas will be edited)
            prompt: Description of edit
            size: Output size
            n: Number of variations
        
        Returns:
            Same format as generate()
        """
        # DALL-E 2 only for edits (DALL-E 3 doesn't support editing yet)
        edit_url = "https://api.openai.com/v1/images/edits"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        with open(image_path, 'rb') as img_file, open(mask_path, 'rb') as mask_file:
            files = {
                'image': img_file,
                'mask': mask_file
            }
            data = {
                'prompt': prompt,
                'n': n,
                'size': size
            }
            
            try:
                response = requests.post(edit_url, headers=headers, files=files, data=data, timeout=120)
                response.raise_for_status()
                result_data = response.json()
                
                return {
                    "image_url": result_data["data"][0]["url"],
                    "revised_prompt": prompt,
                    "engine": "dall-e-2-edit",
                    "size": size,
                    "generated_at": datetime.utcnow().isoformat() + "Z"
                }
                
            except requests.exceptions.RequestException as e:
                print(f"⚠️ DALL-E edit failed: {e}")
                return {
                    "image_url": f"https://via.placeholder.com/{size}/FF6B6B/FFFFFF?text=Edit+Error",
                    "error": str(e),
                    "generated_at": datetime.utcnow().isoformat() + "Z"
                }
    
    def create_variation(
        self,
        image_path: str,
        n: int = 1,
        size: str = "1024x1024"
    ) -> Dict[str, Any]:
        """
        Create variations of existing image
        
        Args:
            image_path: Path to source image
            n: Number of variations
            size: Output size
        
        Returns:
            List of generated variations
        """
        variation_url = "https://api.openai.com/v1/images/variations"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        with open(image_path, 'rb') as img_file:
            files = {'image': img_file}
            data = {'n': n, 'size': size}
            
            try:
                response = requests.post(variation_url, headers=headers, files=files, data=data, timeout=120)
                response.raise_for_status()
                result_data = response.json()
                
                return {
                    "variations": [item["url"] for item in result_data["data"]],
                    "engine": "dall-e-2-variation",
                    "size": size,
                    "count": n,
                    "generated_at": datetime.utcnow().isoformat() + "Z"
                }
                
            except requests.exceptions.RequestException as e:
                print(f"⚠️ DALL-E variation failed: {e}")
                return {
                    "variations": [],
                    "error": str(e),
                    "generated_at": datetime.utcnow().isoformat() + "Z"
                }


# ============================================================================
# MIDJOURNEY ENGINE (Unofficial API)
# ============================================================================

class MidjourneyEngine:
    """
    Midjourney v6 - Artistic, creative generation via unofficial API
    
    Features:
    - Exceptional artistic quality
    - Advanced prompt syntax (--v 6, --ar, --style, etc.)
    - Style consistency
    - Community-driven aesthetics
    
    Limitations:
    - Requires unofficial API service (e.g., useapi.net, midjourney-api.xyz)
    - Longer generation times (60-90 seconds)
    - Rate limits vary by service
    
    Note: This uses a third-party API wrapper since Midjourney has no official API.
    You'll need to sign up for a service like useapi.net or host your own Discord bot.
    """
    
    def __init__(self, api_key: Optional[str] = None, api_base: Optional[str] = None):
        self.api_key = api_key or os.getenv("MIDJOURNEY_API_KEY")
        self.api_base = api_base or os.getenv("MIDJOURNEY_API_BASE", "https://api.useapi.net/v2/midjourney")
        
        if not self.api_key:
            raise ValueError("Midjourney API key required (MIDJOURNEY_API_KEY)")
    
    def generate(
        self,
        prompt: str,
        version: str = "6",
        aspect_ratio: str = "1:1",
        quality: int = 1,
        stylize: int = 100,
        chaos: int = 0,
        wait: bool = True,
        timeout: int = 180
    ) -> Dict[str, Any]:
        """
        Generate image with Midjourney
        
        Args:
            prompt: Image description with optional parameters
                    Example: "Epic fantasy castle --v 6 --ar 16:9 --style raw"
            version: Midjourney version ("5.2", "6", "niji-6")
            aspect_ratio: Aspect ratio ("1:1", "16:9", "9:16", "4:3", etc.)
            quality: Quality setting (0.25, 0.5, 1, 2)
            stylize: Stylization strength (0-1000, default 100)
            chaos: Variation strength (0-100)
            wait: Wait for generation to complete
            timeout: Max wait time in seconds
        
        Returns:
            {
                "image_url": "https://...",
                "job_id": "12345-abcde",
                "prompt": "Original prompt with parameters",
                "engine": "midjourney-v6",
                "status": "completed",
                "generated_at": "2025-12-22T10:30:00Z"
            }
        """
        # Build full prompt with parameters
        full_prompt = prompt
        if "--v" not in prompt:
            full_prompt += f" --v {version}"
        if "--ar" not in prompt:
            full_prompt += f" --ar {aspect_ratio}"
        if "--q" not in prompt:
            full_prompt += f" --q {quality}"
        if "--s" not in prompt and stylize != 100:
            full_prompt += f" --s {stylize}"
        if "--c" not in prompt and chaos > 0:
            full_prompt += f" --c {chaos}"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": full_prompt,
            "webhook_url": None,  # Optional: receive callback when done
            "webhook_type": "result"
        }
        
        try:
            # Step 1: Submit generation request
            response = requests.post(f"{self.api_base}/imagine", headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            job_id = data.get("job_id") or data.get("task_id") or data.get("id")
            
            if not wait:
                return {
                    "job_id": job_id,
                    "prompt": full_prompt,
                    "engine": f"midjourney-v{version}",
                    "status": "queued",
                    "generated_at": datetime.utcnow().isoformat() + "Z"
                }
            
            # Step 2: Poll for completion
            start_time = time.time()
            while time.time() - start_time < timeout:
                status_response = requests.get(
                    f"{self.api_base}/status/{job_id}",
                    headers=headers,
                    timeout=30
                )
                status_response.raise_for_status()
                status_data = status_response.json()
                
                status = status_data.get("status")
                
                if status == "completed" or status == "success":
                    return {
                        "image_url": status_data.get("image_url") or status_data.get("result"),
                        "job_id": job_id,
                        "prompt": full_prompt,
                        "engine": f"midjourney-v{version}",
                        "status": "completed",
                        "generated_at": datetime.utcnow().isoformat() + "Z"
                    }
                elif status == "failed" or status == "error":
                    raise Exception(f"Generation failed: {status_data.get('error', 'Unknown error')}")
                
                # Still processing, wait before next poll
                time.sleep(10)
            
            # Timeout reached
            return {
                "job_id": job_id,
                "prompt": full_prompt,
                "engine": f"midjourney-v{version}",
                "status": "timeout",
                "error": f"Generation exceeded {timeout}s timeout",
                "generated_at": datetime.utcnow().isoformat() + "Z"
            }
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Midjourney generation failed: {e}")
            return {
                "image_url": "https://via.placeholder.com/1024x1024/9333EA/FFFFFF?text=Midjourney+Error",
                "prompt": full_prompt,
                "engine": "midjourney",
                "error": str(e),
                "generated_at": datetime.utcnow().isoformat() + "Z"
            }
    
    def upscale(
        self,
        job_id: str,
        index: int = 1,
        wait: bool = True,
        timeout: int = 120
    ) -> Dict[str, Any]:
        """
        Upscale one of the 4 generated images
        
        Args:
            job_id: Original generation job ID
            index: Which image to upscale (1-4)
            wait: Wait for upscaling to complete
            timeout: Max wait time
        
        Returns:
            Upscaled image data
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "job_id": job_id,
            "index": index
        }
        
        try:
            response = requests.post(f"{self.api_base}/upscale", headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            upscale_job_id = data.get("job_id") or data.get("task_id")
            
            if not wait:
                return {
                    "job_id": upscale_job_id,
                    "status": "queued",
                    "engine": "midjourney-upscale"
                }
            
            # Poll for completion
            start_time = time.time()
            while time.time() - start_time < timeout:
                status_response = requests.get(
                    f"{self.api_base}/status/{upscale_job_id}",
                    headers=headers,
                    timeout=30
                )
                status_data = status_response.json()
                
                if status_data.get("status") == "completed":
                    return {
                        "image_url": status_data.get("image_url"),
                        "job_id": upscale_job_id,
                        "engine": "midjourney-upscale",
                        "status": "completed",
                        "generated_at": datetime.utcnow().isoformat() + "Z"
                    }
                
                time.sleep(5)
            
            return {"error": "Upscale timeout", "status": "timeout"}
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Midjourney upscale failed: {e}")
            return {"error": str(e), "status": "failed"}


# ============================================================================
# STABLE DIFFUSION XL ENGINE
# ============================================================================

class StableDiffusionEngine:
    """
    Stability AI Stable Diffusion XL - Fast, flexible, customizable
    
    Features:
    - Fast generation (3-10 seconds)
    - Multiple style presets (anime, photographic, digital-art, etc.)
    - Fine-grained control (steps, cfg_scale, seed)
    - High resolution (1536x1536 max)
    - Most cost-effective option
    
    Limitations:
    - Less artistic than Midjourney
    - Requires more prompt engineering
    - Lower default quality than DALL-E 3
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("STABILITY_API_KEY")
        self.base_url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0"
        
        if not self.api_key:
            raise ValueError("Stability AI API key required (STABILITY_API_KEY)")
    
    def generate(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: int = 1024,
        height: int = 1024,
        steps: int = 30,
        cfg_scale: float = 7.0,
        style_preset: Optional[str] = None,
        seed: Optional[int] = None,
        samples: int = 1
    ) -> Dict[str, Any]:
        """
        Generate image with Stable Diffusion XL
        
        Args:
            prompt: Image description
            negative_prompt: What to avoid in the image
            width: Image width (must be multiple of 64, max 1536)
            height: Image height (must be multiple of 64, max 1536)
            steps: Generation steps (10-50, higher = better quality but slower)
            cfg_scale: Prompt strength (1-20, higher = more literal)
            style_preset: Style preset (see StylePreset enum)
            seed: Random seed for reproducibility
            samples: Number of images to generate
        
        Returns:
            {
                "image_url": "data:image/png;base64,...",
                "image_base64": "...",
                "prompt": "Original prompt",
                "engine": "stable-diffusion-xl",
                "width": 1024,
                "height": 1024,
                "seed": 12345,
                "generated_at": "2025-12-22T10:30:00Z"
            }
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "text_prompts": [
                {"text": prompt, "weight": 1}
            ],
            "cfg_scale": cfg_scale,
            "height": height,
            "width": width,
            "samples": samples,
            "steps": steps
        }
        
        if negative_prompt:
            payload["text_prompts"].append({"text": negative_prompt, "weight": -1})
        
        if style_preset:
            payload["style_preset"] = style_preset
        
        if seed is not None:
            payload["seed"] = seed
        
        try:
            response = requests.post(
                f"{self.base_url}/text-to-image",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            
            # Stable Diffusion returns base64 images
            image_base64 = data["artifacts"][0]["base64"]
            actual_seed = data["artifacts"][0].get("seed", seed)
            
            return {
                "image_url": f"data:image/png;base64,{image_base64}",
                "image_base64": image_base64,
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "engine": "stable-diffusion-xl",
                "width": width,
                "height": height,
                "steps": steps,
                "cfg_scale": cfg_scale,
                "style_preset": style_preset,
                "seed": actual_seed,
                "generated_at": datetime.utcnow().isoformat() + "Z"
            }
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Stable Diffusion generation failed: {e}")
            return {
                "image_url": f"https://via.placeholder.com/{width}x{height}/22C55E/FFFFFF?text=SD+Error",
                "prompt": prompt,
                "engine": "stable-diffusion-xl",
                "error": str(e),
                "generated_at": datetime.utcnow().isoformat() + "Z"
            }
    
    def image_to_image(
        self,
        init_image_path: str,
        prompt: str,
        strength: float = 0.5,
        steps: int = 30,
        cfg_scale: float = 7.0,
        style_preset: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Transform existing image using prompt
        
        Args:
            init_image_path: Path to source image
            prompt: Transformation description
            strength: How much to change (0.0-1.0, higher = more change)
            steps: Generation steps
            cfg_scale: Prompt strength
            style_preset: Style preset
        
        Returns:
            Same format as generate()
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }
        
        with open(init_image_path, 'rb') as img_file:
            files = {
                'init_image': img_file
            }
            
            data = {
                'text_prompts[0][text]': prompt,
                'text_prompts[0][weight]': 1,
                'image_strength': strength,
                'init_image_mode': 'IMAGE_STRENGTH',
                'steps': steps,
                'cfg_scale': cfg_scale
            }
            
            if style_preset:
                data['style_preset'] = style_preset
            
            try:
                response = requests.post(
                    f"{self.base_url}/image-to-image",
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=60
                )
                response.raise_for_status()
                result_data = response.json()
                
                image_base64 = result_data["artifacts"][0]["base64"]
                
                return {
                    "image_url": f"data:image/png;base64,{image_base64}",
                    "image_base64": image_base64,
                    "prompt": prompt,
                    "engine": "stable-diffusion-xl-img2img",
                    "strength": strength,
                    "generated_at": datetime.utcnow().isoformat() + "Z"
                }
                
            except requests.exceptions.RequestException as e:
                print(f"⚠️ Stable Diffusion img2img failed: {e}")
                return {
                    "error": str(e),
                    "engine": "stable-diffusion-xl-img2img",
                    "generated_at": datetime.utcnow().isoformat() + "Z"
                }
    
    def upscale(
        self,
        image_path: str,
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Upscale image using Stability AI upscaler
        
        Args:
            image_path: Path to image to upscale
            width: Target width (optional, auto-calculated if not provided)
            height: Target height (optional, auto-calculated if not provided)
        
        Returns:
            Upscaled image data
        """
        upscale_url = "https://api.stability.ai/v1/generation/esrgan-v1-x2plus/image-to-image/upscale"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }
        
        with open(image_path, 'rb') as img_file:
            files = {'image': img_file}
            data = {}
            
            if width:
                data['width'] = width
            if height:
                data['height'] = height
            
            try:
                response = requests.post(upscale_url, headers=headers, files=files, data=data, timeout=60)
                response.raise_for_status()
                result_data = response.json()
                
                image_base64 = result_data["artifacts"][0]["base64"]
                
                return {
                    "image_url": f"data:image/png;base64,{image_base64}",
                    "image_base64": image_base64,
                    "engine": "stable-diffusion-upscale",
                    "generated_at": datetime.utcnow().isoformat() + "Z"
                }
                
            except requests.exceptions.RequestException as e:
                print(f"⚠️ Stable Diffusion upscale failed: {e}")
                return {
                    "error": str(e),
                    "engine": "stable-diffusion-upscale",
                    "generated_at": datetime.utcnow().isoformat() + "Z"
                }


# ============================================================================
# UNIVERSAL GRAPHICS INTERFACE
# ============================================================================

class UniversalGraphicsInterface:
    """
    Unified interface for all graphics engines
    
    Automatically selects best engine based on requirements:
    - DALL-E 3: Best for precise, photorealistic images
    - Midjourney: Best for artistic, creative images
    - Stable Diffusion: Best for fast generation and customization
    """
    
    def __init__(self):
        self.dalle = None
        self.midjourney = None
        self.stable_diffusion = None
        
        # Lazy load engines
        if os.getenv("OPENAI_API_KEY"):
            try:
                self.dalle = DallEEngine()
            except:
                pass
        
        if os.getenv("MIDJOURNEY_API_KEY"):
            try:
                self.midjourney = MidjourneyEngine()
            except:
                pass
        
        if os.getenv("STABILITY_API_KEY"):
            try:
                self.stable_diffusion = StableDiffusionEngine()
            except:
                pass
    
    def generate(
        self,
        prompt: str,
        engine: str = "auto",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate image using specified or auto-selected engine
        
        Args:
            prompt: Image description
            engine: Engine name ("dall-e", "midjourney", "stable-diffusion", or "auto")
            **kwargs: Engine-specific parameters
        
        Returns:
            Generated image data
        """
        # Auto-select engine
        if engine == "auto":
            # Heuristic: Choose based on prompt content
            prompt_lower = prompt.lower()
            
            if any(word in prompt_lower for word in ["artistic", "fantasy", "epic", "dramatic", "cinematic"]):
                engine = "midjourney"
            elif any(word in prompt_lower for word in ["photorealistic", "portrait", "precise", "detailed"]):
                engine = "dall-e"
            else:
                engine = "stable-diffusion"  # Default for speed
        
        # Route to appropriate engine
        if engine == "dall-e" and self.dalle:
            return self.dalle.generate(prompt, **kwargs)
        elif engine == "midjourney" and self.midjourney:
            return self.midjourney.generate(prompt, **kwargs)
        elif engine == "stable-diffusion" and self.stable_diffusion:
            return self.stable_diffusion.generate(prompt, **kwargs)
        else:
            # Fallback to any available engine
            if self.dalle:
                return self.dalle.generate(prompt, **kwargs)
            elif self.stable_diffusion:
                return self.stable_diffusion.generate(prompt, **kwargs)
            elif self.midjourney:
                return self.midjourney.generate(prompt, **kwargs)
            else:
                raise ValueError("No graphics engines available. Please configure API keys.")
    
    def get_available_engines(self) -> List[str]:
        """Get list of available engines"""
        engines = []
        if self.dalle:
            engines.append("dall-e-3")
        if self.midjourney:
            engines.append("midjourney-v6")
        if self.stable_diffusion:
            engines.append("stable-diffusion-xl")
        return engines


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Initialize universal interface
    graphics = UniversalGraphicsInterface()
    
    print("🎨 Available engines:", graphics.get_available_engines())
    
    # Generate with auto-selection
    result = graphics.generate(
        "A majestic lion in a savanna at golden hour, photorealistic, 4K quality",
        engine="auto"
    )
    
    print("\n✅ Generated image:")
    print(f"   Engine: {result.get('engine')}")
    print(f"   URL: {result.get('image_url')[:100]}...")
    print(f"   Generated at: {result.get('generated_at')}")

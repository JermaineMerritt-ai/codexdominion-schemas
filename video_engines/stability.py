"""
Stability AI Video Generation Engine

API Documentation: https://platform.stability.ai/docs
Model: Stable Video Diffusion (image-to-video)
"""

import os
import requests
import time
from typing import Dict, Any, Optional


class StabilityAPIError(Exception):
    """Stability API error"""
    pass


def generate(prompt: str, **kwargs) -> Dict[str, Any]:
    """
    Generate video using Stability AI Video.
    
    Note: Stability Video primarily uses image-to-video.
    For text-to-video, first generate image with SDXL, then video from image.
    
    Args:
        prompt: Text description (used to generate seed image if no image_url)
        **kwargs: Optional parameters:
            - duration: Video length (seconds, default: 4)
            - cfg_scale: Prompt strength 0-10 (default: 2.5)
            - motion_bucket_id: Motion amount 1-255 (default: 127)
            - seed: Random seed (optional)
            - image_url: Starting image (required for video generation)
            - fps: Frames per second 6-30 (default: 24)
    
    Returns:
        dict: {
            "video_url": "https://api.stability.ai/v1/...",
            "thumbnail_url": "https://api.stability.ai/v1/...",
            "duration": 4.0,
            "status": "complete",
            "engine": "stability",
            "generation_id": "xyz123..."
        }
    
    Raises:
        StabilityAPIError: If API call fails
    """
    api_key = os.getenv('STABILITY_API_KEY')
    if not api_key:
        raise StabilityAPIError("STABILITY_API_KEY not set in environment")
    
    # Extract parameters with defaults
    duration = kwargs.get('duration', 4)
    cfg_scale = kwargs.get('cfg_scale', 2.5)
    motion_bucket_id = kwargs.get('motion_bucket_id', 127)
    seed = kwargs.get('seed', 0)
    image_url = kwargs.get('image_url')
    fps = kwargs.get('fps', 24)
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    
    # If no image provided, generate one first using SDXL
    if not image_url:
        image_url = _generate_seed_image(prompt, api_key, seed)
    
    # Stability Video API endpoint
    api_url = "https://api.stability.ai/v2alpha/generation/image-to-video"
    
    # Download image to send as multipart (Stability requires this)
    try:
        image_response = requests.get(image_url, timeout=30)
        image_response.raise_for_status()
        image_data = image_response.content
    except requests.RequestException as e:
        raise StabilityAPIError(f"Failed to download seed image: {str(e)}")
    
    # Prepare multipart form data
    files = {
        "image": ("image.png", image_data, "image/png")
    }
    
    data = {
        "cfg_scale": cfg_scale,
        "motion_bucket_id": motion_bucket_id,
        "seed": seed
    }
    
    try:
        # Submit generation request
        response = requests.post(
            api_url,
            headers={"Authorization": headers["Authorization"]},
            files=files,
            data=data,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        generation_id = result.get('id')
        
        if not generation_id:
            # Some Stability endpoints return video directly
            if result.get('video'):
                video_base64 = result['video']
                # In production, save this to storage and get URL
                video_url = _save_video_to_storage(video_base64, generation_id or "direct")
                
                return {
                    "video_url": video_url,
                    "thumbnail_url": image_url,  # Use seed image as thumbnail
                    "duration": duration,
                    "status": "complete",
                    "engine": "stability",
                    "generation_id": generation_id or "direct"
                }
            else:
                raise StabilityAPIError(f"No generation ID or video in response: {result}")
        
        # Poll for completion
        status_url = f"https://api.stability.ai/v2alpha/generation/image-to-video/result/{generation_id}"
        max_attempts = 60  # ~5 minutes max (5s intervals)
        
        for attempt in range(max_attempts):
            status_response = requests.get(status_url, headers=headers, timeout=30)
            
            if status_response.status_code == 202:
                # Still processing
                time.sleep(5)
                continue
            
            status_response.raise_for_status()
            
            # Check content type
            if 'application/json' in status_response.headers.get('Content-Type', ''):
                status_data = status_response.json()
                if status_data.get('status') == 'failed':
                    raise StabilityAPIError(f"Generation failed: {status_data.get('error')}")
            else:
                # Video returned directly
                video_data = status_response.content
                video_url = _save_video_to_storage(video_data, generation_id)
                
                return {
                    "video_url": video_url,
                    "thumbnail_url": image_url,
                    "duration": duration,
                    "status": "complete",
                    "engine": "stability",
                    "generation_id": generation_id
                }
        
        raise StabilityAPIError(f"Generation timeout after {max_attempts * 5} seconds")
    
    except requests.RequestException as e:
        raise StabilityAPIError(f"API request failed: {str(e)}")


def _generate_seed_image(prompt: str, api_key: str, seed: int = 0) -> str:
    """Generate seed image using SDXL for text-to-video workflow"""
    # Simplified - in production, implement full SDXL generation
    # For now, return placeholder
    return "https://example.com/seed_image.png"


def _save_video_to_storage(video_data: bytes, generation_id: str) -> str:
    """Save video to storage and return URL"""
    # In production, upload to S3/GCS/Azure Storage
    # For now, return placeholder
    return f"https://storage.example.com/stability_{generation_id}.mp4"


# Fallback for development/testing
def generate_placeholder(prompt: str, **kwargs) -> Dict[str, Any]:
    """Placeholder response for testing without API key"""
    return {
        "video_url": "https://example.com/stability_video.mp4",
        "thumbnail_url": "https://example.com/stability_thumb.jpg",
        "duration": kwargs.get('duration', 4.0),
        "status": "complete",
        "engine": "stability",
        "generation_id": "placeholder_gen",
        "note": "Placeholder - Set STABILITY_API_KEY to use real API"
    }

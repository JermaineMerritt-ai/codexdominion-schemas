"""
🚀 MASTER DASHBOARD - FLASK VERSION (100% Compatible)
======================================================
Flask-based dashboard that works with any Python version
No Streamlit platform issues!
"""

import sys
import io
import logging

# Configure logging for better error handling
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Skip UTF-8 wrapper - use logging instead
# This avoids "I/O operation on closed file" errors

from flask import Flask, render_template, render_template_string, jsonify, request, redirect, url_for, Response, session as flask_session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime
from pathlib import Path
import os
import base64
import threading
import time as _time
from typing import Dict, List, Any
import redis
from rq import Queue

# Import calculators module for ROI calculations
from calculators import calculate_savings, SavingsInput, get_effectiveness_rating

# Import workflow engine for action tracking
from workflow_engine import workflow_engine

# Import Creative Intelligence Engine Blueprint
from creative_engine_routes import creative_engine_bp

# Import Creative Agents Template
from creative_agents_template import CREATIVE_AGENTS_HTML

# Import Authentication API
from auth_api import register_auth_routes

# Import Products API
from products_api import register_products_routes

# Add paths
sys.path.insert(0, str(Path(__file__).parent))

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file upload
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Database configuration - Use SQLite for easy local development
# For PostgreSQL, use: "postgresql://username:password@localhost:5432/dbname"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///codex_graphics.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Register Creative Intelligence Engine Blueprint
app.register_blueprint(creative_engine_bp)

# Register Authentication Routes
register_auth_routes(app)

# Register Products Routes
register_products_routes(app)

# Initialize UGI after database is set up
def initialize_ugi():
    """Initialize Universal Generation Interface with database and storage"""
    global video_ugi
    if video_ugi is None:
        video_ugi = UniversalGenerationInterface(db, video_storage, video_pipeline)
        print("✨ Universal Generation Interface initialized")


# Database Models
class GraphicsProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.Text, nullable=False)
    aspect_ratio = db.Column(db.String(20))
    color_palette = db.Column(db.String(50))
    mood = db.Column(db.String(50))
    lighting = db.Column(db.String(50))
    camera_angle = db.Column(db.String(50))
    thumbnail_url = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.Column(db.Text)          # e.g. "neon,afrofuturism,portraits"
    category = db.Column(db.String(100))  # e.g. "Brand Kit", "Series A", "Campaign"
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))
    
    # Prompt Evolution - Lineage Tracking
    parent_prompt_id = db.Column(db.Integer, db.ForeignKey('prompt_history.id'))  # Which prompt spawned this
    prompt_source = db.Column(db.String(50))  # 'user_written', 'ai_suggested', 'evolved', 'template'
    was_prompt_reused = db.Column(db.Boolean, default=False)  # Did user copy/reuse this prompt?
    engagement_score = db.Column(db.Float, default=0.0)  # Calculated: saves + views + reuse
    
    # Project-to-Project Evolution (remixing/forking)
    original_prompt = db.Column(db.Text)   # The base prompt when first created
    prompt_version = db.Column(db.Integer, default=1)  # 1 = original, 2 = first remix, etc.
    parent_project_id = db.Column(db.Integer, db.ForeignKey("graphics_project.id"))  # Forked from which project?

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # Relationship: one user → many projects
    projects = db.relationship("GraphicsProject", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    role = db.Column(db.String(50), default="viewer")  # owner, admin, editor, viewer

class TeamActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    action = db.Column(db.String(255))  # e.g. "created a project", "updated tags"
    activity_metadata = db.Column(db.JSON)       # optional details (renamed from 'metadata' - reserved by SQLAlchemy)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class PromptHistory(db.Model):
    """Track prompts independently - enables evolution, reuse analysis, and lineage."""
    id = db.Column(db.Integer, primary_key=True)
    prompt_text = db.Column(db.Text, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Lineage
    parent_id = db.Column(db.Integer, db.ForeignKey('prompt_history.id'))  # Evolved from which prompt?
    generation = db.Column(db.Integer, default=1)  # 1 = original, 2 = first evolution, etc.
    evolution_reason = db.Column(db.String(100))  # 'high_engagement', 'tag_pattern', 'mood_blend'
    
    # Context that generated this prompt
    mood = db.Column(db.String(50))
    color_palette = db.Column(db.String(50))
    tags = db.Column(db.Text)
    category = db.Column(db.String(100))
    
    # Effectiveness metrics (calculated)
    times_used = db.Column(db.Integer, default=0)  # How many projects used this?
    times_saved = db.Column(db.Integer, default=0)  # How many projects saved?
    times_reused = db.Column(db.Integer, default=0)  # How many times copied?
    avg_engagement = db.Column(db.Float, default=0.0)  # Average engagement of resulting projects
    effectiveness_score = db.Column(db.Float, default=0.0)  # Composite score
    
    # Status
    is_template = db.Column(db.Boolean, default=False)  # Is this a reusable template?
    is_evolved = db.Column(db.Boolean, default=False)  # Was this AI-evolved?


# =============================================================================
# VIDEO STUDIO - PHASE 1: CORE ARCHITECTURE
# =============================================================================

class VideoProject(db.Model):
    """Video projects - the motion creative layer.
    
    Designed for timeline-based editing, storyboarding, and multi-scene composition.
    Similar to GraphicsProject but expanded for time-based media.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=True)
    
    # Core metadata
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    tags = db.Column(db.Text)  # Comma-separated
    category = db.Column(db.String(100))  # "Music Video", "Documentary", "Narrative", etc.
    
    # Media outputs
    video_url = db.Column(db.String(500))  # Final rendered video
    thumbnail_url = db.Column(db.String(500))  # Video thumbnail
    duration = db.Column(db.Float, default=0.0)  # Length in seconds
    resolution = db.Column(db.String(20))  # "1920x1080", "3840x2160", etc.
    fps = db.Column(db.Integer, default=30)  # Frames per second
    
    # Storyboard structure (JSON)
    # Example: [{"scene_id": 1, "prompt": "...", "duration": 5, "thumbnail": "...", "video_url": "..."}]
    storyboard = db.Column(db.JSON, default=list)
    
    # Timeline structure (JSON)
    # Example: {"layers": [{"id": 1, "clips": [{"start": 0, "end": 5, "asset_id": 1}]}]}
    timeline = db.Column(db.JSON, default=dict)
    
    # Audio tracks (JSON)
    # Example: [{"id": 1, "url": "...", "start": 0, "volume": 0.8, "name": "Background Music"}]
    audio_tracks = db.Column(db.JSON, default=list)
    
    # Prompt and generation
    prompt = db.Column(db.Text)  # Primary prompt for generation
    generation_engine = db.Column(db.String(50))  # "runway", "pika", "luma", "stability"
    generation_params = db.Column(db.JSON)  # Engine-specific parameters
    
    # Evolution tracking (mirrors GraphicsProject)
    parent_prompt_id = db.Column(db.Integer, db.ForeignKey('prompt_history.id'))
    prompt_source = db.Column(db.String(50))  # 'user_written', 'ai_suggested', 'evolved'
    original_prompt = db.Column(db.Text)  # Immutable base prompt
    prompt_version = db.Column(db.Integer, default=1)
    parent_project_id = db.Column(db.Integer, db.ForeignKey("video_project.id"))
    was_prompt_reused = db.Column(db.Boolean, default=False)
    engagement_score = db.Column(db.Float, default=0.0)
    
    # Status
    status = db.Column(db.String(50), default="draft")  # draft, rendering, complete, published
    is_public = db.Column(db.Boolean, default=False)
    
    # Timestamps
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class VideoAsset(db.Model):
    """Individual video clips, audio files, and media assets.
    
    These are the building blocks of VideoProjects - can be:
    - Uploaded by user
    - Generated by AI
    - Downloaded from stock libraries
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey("video_project.id"), nullable=True)
    
    # Asset metadata
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    asset_type = db.Column(db.String(50), nullable=False)  # "video", "audio", "image", "overlay"
    
    # File details
    file_url = db.Column(db.String(500), nullable=False)  # S3/GCS/Azure/Local URL
    thumbnail_url = db.Column(db.String(500))
    file_size = db.Column(db.Integer)  # Bytes
    mime_type = db.Column(db.String(100))  # "video/mp4", "audio/mpeg", etc.
    
    # Media properties
    duration = db.Column(db.Float, default=0.0)  # For video/audio (seconds)
    width = db.Column(db.Integer)  # For video/image
    height = db.Column(db.Integer)  # For video/image
    fps = db.Column(db.Integer)  # For video
    
    # Generation info (if AI-generated)
    prompt = db.Column(db.Text)  # Prompt used to generate this asset
    generation_engine = db.Column(db.String(50))  # "runway", "pika", etc.
    generation_params = db.Column(db.JSON)  # Engine-specific params
    
    # Tags and organization
    tags = db.Column(db.Text)  # Comma-separated
    category = db.Column(db.String(100))
    
    # Status
    status = db.Column(db.String(50), default="ready")  # uploading, processing, ready, error
    storage_provider = db.Column(db.String(50))  # "s3", "gcs", "azure", "local"
    
    # Timestamps
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class TimelineClip(db.Model):
    """Timeline clip instance - represents a clip placed on a timeline track.
    
    This is different from VideoAsset:
    - VideoAsset: The source media file
    - TimelineClip: An instance of that asset placed at a specific time/track
    
    Multiple TimelineClips can reference the same VideoAsset (reusable clips).
    """
    __tablename__ = 'timeline_clips'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("video_project.id"), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey("video_asset.id"), nullable=False)
    
    # Timeline placement
    track_id = db.Column(db.String(50), nullable=False)  # "video_1", "video_2", "audio_1", etc.
    start_time = db.Column(db.Float, nullable=False)  # Start position in seconds
    end_time = db.Column(db.Float, nullable=False)  # End position in seconds
    
    # Clip trimming (what portion of the source asset to use)
    source_start = db.Column(db.Float, default=0.0)  # Start in source asset
    source_end = db.Column(db.Float)  # End in source asset (null = use full duration)
    
    # Visual/audio properties
    volume = db.Column(db.Float, default=1.0)  # 0.0 to 1.0
    opacity = db.Column(db.Float, default=1.0)  # 0.0 to 1.0
    speed = db.Column(db.Float, default=1.0)  # Playback speed multiplier
    
    # Effects and filters (JSON)
    effects = db.Column(db.JSON, default=list)  # [{"type": "fade_in", "duration": 1.0}, ...]
    
    # Scene association
    scene_id = db.Column(db.Integer)  # Links to storyboard scene
    
    # Metadata
    layer_order = db.Column(db.Integer, default=0)  # Z-index for overlapping clips
    is_locked = db.Column(db.Boolean, default=False)  # Prevent accidental edits
    
    # Timestamps
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class TimelineMarker(db.Model):
    """Timeline markers - ritual stones that mark important moments.
    
    Markers can represent:
    - Scene boundaries
    - Beat markers
    - Notes/comments
    - AI suggestions
    - Timing cues
    """
    __tablename__ = 'timeline_markers'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("video_project.id"), nullable=False)
    
    # Marker placement
    time = db.Column(db.Float, nullable=False)  # Position in seconds
    
    # Marker type and content
    marker_type = db.Column(db.String(50), default="note")  # "note", "scene", "beat", "ai_suggestion"
    label = db.Column(db.String(255))
    description = db.Column(db.Text)
    color = db.Column(db.String(20), default="#f5576c")  # Hex color
    
    # Scene association
    scene_id = db.Column(db.Integer)  # Links to storyboard scene
    
    # AI suggestions
    suggestion_data = db.Column(db.JSON)  # {"action": "extend_scene", "params": {...}}
    
    # Timestamps
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


# ==================== PHASE 4: STORYBOARD MODELS ====================

class Storyboard(db.Model):
    """Storyboard - narrative structure before timeline.
    
    The visual narrative map where creators design story flow,
    not just clip sequences.
    """
    __tablename__ = 'storyboards'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("video_project.id"), nullable=False)
    
    # Storyboard metadata
    name = db.Column(db.String(255), nullable=False, default="Untitled Storyboard")
    description = db.Column(db.Text)
    
    # Narrative analysis
    quality_score = db.Column(db.Float, default=0)  # 0-100 from Scene Flow Engine
    continuity_report = db.Column(db.JSON)  # Analysis from Scene Flow Engine
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SceneCard(db.Model):
    """Scene Card - individual narrative unit in storyboard.
    
    Represents a moment, shot, beat, or idea.
    Cards can be evolved, extended, duplicated, and reordered.
    """
    __tablename__ = 'scene_cards'
    
    id = db.Column(db.Integer, primary_key=True)
    storyboard_id = db.Column(db.Integer, db.ForeignKey("storyboards.id"), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey("video_asset.id"))  # Linked video asset
    
    # Card ordering
    order_index = db.Column(db.Integer, nullable=False, default=0)  # Position in storyboard
    
    # Scene content
    prompt = db.Column(db.Text)
    thumbnail_url = db.Column(db.String(500))
    duration = db.Column(db.Float, default=5.0)
    
    # Cinematic metadata
    scene_type = db.Column(db.String(50), default="medium")  # wide, medium, close_up, tracking, aerial, static
    mood = db.Column(db.String(50), default="calm")  # intense, calm, dramatic, mysterious, joyful, etc.
    tags = db.Column(db.String(500))  # Comma-separated tags
    
    # Character and theme tracking
    characters = db.Column(db.JSON)  # [{"name": "hero", "presence": true}]
    themes = db.Column(db.JSON)  # [{"name": "redemption", "strength": 0.8}]
    
    # Scene status
    status = db.Column(db.String(50), default="draft")  # draft, generated, approved, on_timeline
    
    # AI suggestions
    flow_suggestions = db.Column(db.JSON)  # Suggestions from Scene Flow Engine
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ====================================================================================
# PHASE 5: VIDEO LIBRARY + TEAM SHARING MODELS (The Vault of Motion)
# ====================================================================================

class VideoCollection(db.Model):
    """Curated sets of videos - campaigns, series, character arcs, brand kits, universes.
    
    Collections are like albums or playlists for video content.
    They can be:
    - Campaign collections (marketing campaigns)
    - Series collections (episodic content)
    - Character arc collections (following a character's journey)
    - Brand kit collections (branded assets)
    - Story universe collections (shared cinematic universe)
    """
    __tablename__ = 'video_collections'
    
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    # Collection metadata
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    collection_type = db.Column(db.String(50), default="general")  # campaign, series, character_arc, brand_kit, universe
    
    # Visual
    cover_image_url = db.Column(db.String(500))
    
    # Organization
    tags = db.Column(db.Text)  # Comma-separated
    category = db.Column(db.String(100))
    
    # Sharing
    is_public = db.Column(db.Boolean, default=False)
    share_level = db.Column(db.String(50), default="team")  # private, team, public
    
    # Stats
    video_count = db.Column(db.Integer, default=0)
    total_duration = db.Column(db.Float, default=0.0)  # Sum of all video durations
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CollectionItem(db.Model):
    """Junction table for videos in collections (many-to-many).
    
    A video can be in multiple collections.
    A collection can have multiple videos.
    """
    __tablename__ = 'collection_items'
    
    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey("video_collections.id"), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey("video_asset.id"), nullable=False)
    
    # Organization within collection
    order_index = db.Column(db.Integer, default=0)  # For ordered collections (series)
    
    # Optional metadata
    notes = db.Column(db.Text)  # Why this video is in this collection
    
    # Timestamps
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    added_by = db.Column(db.Integer, db.ForeignKey("user.id"))


class VideoLibraryMetadata(db.Model):
    """Extended metadata for library view (enhances VideoAsset).
    
    This table adds library-specific fields to video assets:
    - Lineage tracking
    - Mood classification
    - Advanced categorization
    - Sharing settings
    - Usage stats
    """
    __tablename__ = 'video_library_metadata'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey("video_asset.id"), nullable=False, unique=True)
    
    # Library classification
    mood = db.Column(db.String(50))  # intense, calm, dramatic, mysterious, joyful, etc.
    scene_type = db.Column(db.String(50))  # wide, medium, close_up, tracking, aerial, static
    
    # Lineage tracking (version control)
    lineage_root_id = db.Column(db.Integer, db.ForeignKey("video_asset.id"))  # Original ancestor
    parent_asset_id = db.Column(db.Integer, db.ForeignKey("video_asset.id"))  # Immediate parent
    lineage_version = db.Column(db.Integer, default=1)  # v1, v2, v3...
    lineage_branch = db.Column(db.String(100))  # "main", "alternate", "remix_001", etc.
    evolution_type = db.Column(db.String(50))  # duplicate, evolve, extend, remix
    evolution_note = db.Column(db.Text)  # What changed from parent
    
    # Sharing settings
    share_level = db.Column(db.String(50), default="team")  # private, team, public
    can_duplicate = db.Column(db.Boolean, default=True)
    can_remix = db.Column(db.Boolean, default=True)
    
    # Usage stats
    view_count = db.Column(db.Integer, default=0)
    duplicate_count = db.Column(db.Integer, default=0)  # How many times duplicated
    remix_count = db.Column(db.Integer, default=0)  # How many times remixed
    used_in_projects = db.Column(db.Integer, default=0)  # How many projects use this
    
    # Constellation data
    constellation_x = db.Column(db.Float)  # X position in constellation map
    constellation_y = db.Column(db.Float)  # Y position in constellation map
    constellation_cluster = db.Column(db.String(100))  # Which cluster this belongs to
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class VideoShare(db.Model):
    """Granular sharing permissions for individual videos.
    
    Allows fine-grained control:
    - Share specific videos with specific users
    - Set permission levels (view, edit, admin)
    - Track who shared with whom
    """
    __tablename__ = 'video_shares'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey("video_asset.id"), nullable=False)
    shared_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    shared_with = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    # Permission level
    permission = db.Column(db.String(50), default="view")  # view, edit, admin
    
    # Optional message
    message = db.Column(db.Text)  # "Check out this clip for the campaign!"
    
    # Timestamps
    shared_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)  # Optional expiration


class VideoLineage(db.Model):
    """Tracks the family tree of video evolution.
    
    Records:
    - Parent → Child relationships
    - Evolution types (duplicate, evolve, extend, remix)
    - Branching points
    - Merge points
    
    This creates a Git-like version tree for videos.
    """
    __tablename__ = 'video_lineage'
    
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("video_asset.id"), nullable=False)
    child_id = db.Column(db.Integer, db.ForeignKey("video_asset.id"), nullable=False)
    
    # Evolution details
    evolution_type = db.Column(db.String(50), nullable=False)  # duplicate, evolve, extend, remix, variation
    evolution_params = db.Column(db.JSON)  # What parameters changed
    
    # Prompt changes
    original_prompt = db.Column(db.Text)
    evolved_prompt = db.Column(db.Text)
    prompt_delta = db.Column(db.Text)  # What was added/changed
    
    # Creator tracking
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    # Branch metadata
    branch_name = db.Column(db.String(100))  # "alternate_ending", "faster_pace", etc.
    is_merge = db.Column(db.Boolean, default=False)  # If this combined multiple parents
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ====================================================================================
# PHASE 6: AUDIO STUDIO MODELS (The Temple of Sound)
# ====================================================================================

class AudioProject(db.Model):
    """Audio project container - equivalent to VideoProject but for audio.
    
    Supports:
    - Music composition projects
    - Podcast episodes
    - Voiceover projects
    - Sound design projects
    - Multi-track mixing
    - Waveform editing
    """
    __tablename__ = 'audio_projects'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=True)
    
    # Project metadata
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    project_type = db.Column(db.String(50), default="music")  # music, podcast, voiceover, sound_design, ambient
    
    # Audio specs
    sample_rate = db.Column(db.Integer, default=44100)  # Hz (44.1kHz standard)
    bit_depth = db.Column(db.Integer, default=16)  # bits (16-bit standard)
    channels = db.Column(db.Integer, default=2)  # 1=mono, 2=stereo
    duration = db.Column(db.Float, default=0.0)  # Total duration in seconds
    
    # Waveform data (for visualization)
    waveform_data = db.Column(db.JSON)  # Array of amplitude values
    
    # Tags and organization
    tags = db.Column(db.Text)  # Comma-separated
    category = db.Column(db.String(100))  # music, voiceover, sfx, ambient
    mood = db.Column(db.String(50))  # upbeat, calm, dramatic, mysterious, etc.
    genre = db.Column(db.String(100))  # electronic, orchestral, rock, jazz, etc.
    
    # Lineage tracking
    prompt_version = db.Column(db.Integer, default=1)
    parent_project_id = db.Column(db.Integer, db.ForeignKey("audio_projects.id"))
    was_prompt_reused = db.Column(db.Boolean, default=False)
    engagement_score = db.Column(db.Float, default=0.0)
    
    # Status
    status = db.Column(db.String(50), default="draft")  # draft, mixing, mastering, complete, published
    is_public = db.Column(db.Boolean, default=False)
    
    # Timestamps
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AudioAsset(db.Model):
    """Individual audio clips, music files, voiceovers, sound effects.
    
    These are the building blocks of AudioProjects - can be:
    - Uploaded by user
    - Generated by AI (ElevenLabs, Suno, Stability Audio, etc.)
    - Recorded directly
    - Imported from stock libraries
    """
    __tablename__ = 'audio_assets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey("audio_projects.id"), nullable=True)
    
    # Asset metadata
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    asset_type = db.Column(db.String(50), nullable=False)  # music, voiceover, sfx, ambient, stem
    
    # File details
    file_url = db.Column(db.String(500), nullable=False)  # S3/GCS/Azure/Local URL
    waveform_url = db.Column(db.String(500))  # Waveform image for visualization
    file_size = db.Column(db.Integer)  # Bytes
    mime_type = db.Column(db.String(100))  # audio/mpeg, audio/wav, etc.
    
    # Audio properties
    duration = db.Column(db.Float, default=0.0)  # Seconds
    sample_rate = db.Column(db.Integer, default=44100)  # Hz
    bit_depth = db.Column(db.Integer, default=16)  # bits
    channels = db.Column(db.Integer, default=2)  # 1=mono, 2=stereo
    bitrate = db.Column(db.Integer)  # kbps for compressed formats
    
    # Waveform data
    waveform_data = db.Column(db.JSON)  # Array of amplitude values for visualization
    peak_amplitude = db.Column(db.Float)  # Peak level (0.0 to 1.0)
    rms_level = db.Column(db.Float)  # RMS loudness level
    
    # Generation info (if AI-generated)
    prompt = db.Column(db.Text)  # Prompt used to generate this asset
    generation_engine = db.Column(db.String(50))  # elevenlabs, suno, stability_audio, etc.
    generation_params = db.Column(db.JSON)  # Engine-specific params
    voice_id = db.Column(db.String(100))  # For ElevenLabs voiceovers
    voice_settings = db.Column(db.JSON)  # Voice stability, similarity, style, etc.
    
    # Tags and organization
    tags = db.Column(db.Text)  # Comma-separated
    category = db.Column(db.String(100))
    mood = db.Column(db.String(50))
    genre = db.Column(db.String(100))
    key = db.Column(db.String(10))  # Musical key: C, D, Em, F#m, etc.
    bpm = db.Column(db.Integer)  # Beats per minute (for music)
    
    # Status
    status = db.Column(db.String(50), default="ready")  # uploading, processing, ready, error
    storage_provider = db.Column(db.String(50))  # s3, gcs, azure, local
    
    # Timestamps
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class AudioTrack(db.Model):
    """Audio track instance - represents audio placed on a timeline track.
    
    Similar to TimelineClip for video, but optimized for audio:
    - Multiple tracks (music, voiceover, sfx, ambient)
    - Volume automation
    - Pan/balance control
    - Fade in/out
    - Audio effects
    """
    __tablename__ = 'audio_tracks'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("audio_projects.id"), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey("audio_assets.id"), nullable=False)
    
    # Track placement
    track_id = db.Column(db.String(50), nullable=False)  # music_1, voiceover_1, sfx_1, ambient_1
    start_time = db.Column(db.Float, nullable=False)  # Start position in seconds
    end_time = db.Column(db.Float, nullable=False)  # End position in seconds
    
    # Clip trimming (what portion of the source asset to use)
    source_start = db.Column(db.Float, default=0.0)  # Start in source asset
    source_end = db.Column(db.Float)  # End in source asset (null = use full duration)
    
    # Audio properties
    volume = db.Column(db.Float, default=1.0)  # 0.0 to 2.0 (0=silent, 1=original, 2=2x amplification)
    pan = db.Column(db.Float, default=0.0)  # -1.0 (left) to 1.0 (right), 0=center
    speed = db.Column(db.Float, default=1.0)  # Playback speed multiplier
    pitch_shift = db.Column(db.Float, default=0.0)  # Semitones (-12 to +12)
    
    # Fade effects
    fade_in_duration = db.Column(db.Float, default=0.0)  # Seconds
    fade_out_duration = db.Column(db.Float, default=0.0)  # Seconds
    
    # Volume automation (JSON array of keyframes)
    volume_automation = db.Column(db.JSON)  # [{"time": 5.0, "volume": 0.8}, ...]
    
    # Effects (JSON array)
    effects = db.Column(db.JSON)  # [{"type": "reverb", "wet": 0.3}, {"type": "eq", "low": 1.2}, ...]
    
    # Metadata
    layer_order = db.Column(db.Integer, default=0)  # Z-index for overlapping tracks
    is_locked = db.Column(db.Boolean, default=False)  # Prevent accidental edits
    is_muted = db.Column(db.Boolean, default=False)  # Mute track
    is_solo = db.Column(db.Boolean, default=False)  # Solo track
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AudioMarker(db.Model):
    """Timeline markers for audio projects - similar to TimelineMarker for video.
    
    Used for:
    - Beat markers
    - Section markers (intro, verse, chorus, bridge, outro)
    - Cue points
    - Annotations
    - Sync points
    """
    __tablename__ = 'audio_markers'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("audio_projects.id"), nullable=False)
    
    # Marker properties
    time = db.Column(db.Float, nullable=False)  # Position in seconds
    marker_type = db.Column(db.String(50), default="note")  # beat, section, cue, note, sync
    label = db.Column(db.String(255))
    color = db.Column(db.String(7), default="#FF6B6B")  # Hex color
    
    # Section metadata (for section markers)
    section_type = db.Column(db.String(50))  # intro, verse, chorus, bridge, outro, break
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AudioLibraryMetadata(db.Model):
    """Extended metadata for audio library (similar to VideoLibraryMetadata).
    
    Adds library-specific fields:
    - Lineage tracking
    - Mood/genre classification
    - Usage stats
    - Constellation positioning
    """
    __tablename__ = 'audio_library_metadata'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey("audio_assets.id"), nullable=False, unique=True)
    
    # Lineage tracking (version control)
    lineage_root_id = db.Column(db.Integer, db.ForeignKey("audio_assets.id"))  # Original ancestor
    parent_asset_id = db.Column(db.Integer, db.ForeignKey("audio_assets.id"))  # Immediate parent
    lineage_version = db.Column(db.Integer, default=1)  # v1, v2, v3...
    lineage_branch = db.Column(db.String(100))  # main, alternate, remix, etc.
    evolution_type = db.Column(db.String(50))  # duplicate, evolve, extend, remix, stem
    evolution_note = db.Column(db.Text)  # What changed from parent
    
    # Sharing settings
    share_level = db.Column(db.String(50), default="team")  # private, team, public
    can_duplicate = db.Column(db.Boolean, default=True)
    can_remix = db.Column(db.Boolean, default=True)
    
    # Usage stats
    play_count = db.Column(db.Integer, default=0)
    download_count = db.Column(db.Integer, default=0)
    duplicate_count = db.Column(db.Integer, default=0)
    remix_count = db.Column(db.Integer, default=0)
    used_in_projects = db.Column(db.Integer, default=0)
    
    # Constellation data
    constellation_x = db.Column(db.Float)
    constellation_y = db.Column(db.Float)
    constellation_cluster = db.Column(db.String(100))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AudioCollection(db.Model):
    """Curated sets of audio - albums, playlists, sound packs, podcast series.
    
    Similar to VideoCollection but for audio:
    - Album collections
    - Playlist collections
    - Sound pack collections
    - Podcast series collections
    - Voiceover collections
    """
    __tablename__ = 'audio_collections'
    
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    # Collection metadata
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    collection_type = db.Column(db.String(50), default="playlist")  # album, playlist, sound_pack, podcast_series, voiceover_pack
    
    # Visual
    cover_image_url = db.Column(db.String(500))
    
    # Organization
    tags = db.Column(db.Text)  # Comma-separated
    category = db.Column(db.String(100))
    mood = db.Column(db.String(50))
    genre = db.Column(db.String(100))
    
    # Sharing
    is_public = db.Column(db.Boolean, default=False)
    share_level = db.Column(db.String(50), default="team")  # private, team, public
    
    # Stats
    audio_count = db.Column(db.Integer, default=0)
    total_duration = db.Column(db.Float, default=0.0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AudioCollectionItem(db.Model):
    """Junction table for audio in collections (many-to-many)."""
    __tablename__ = 'audio_collection_items'
    
    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey("audio_collections.id"), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey("audio_assets.id"), nullable=False)
    
    # Organization within collection
    order_index = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)
    
    # Timestamps
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    added_by = db.Column(db.Integer, db.ForeignKey("user.id"))


class AudioLineage(db.Model):
    """Tracks the family tree of audio evolution (Git-like version tree).
    
    Records:
    - Parent → Child relationships
    - Evolution types (duplicate, evolve, extend, remix, stem separation)
    - Prompt changes
    - Parameter changes
    """
    __tablename__ = 'audio_lineage'
    
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("audio_assets.id"), nullable=False)
    child_id = db.Column(db.Integer, db.ForeignKey("audio_assets.id"), nullable=False)
    
    # Evolution details
    evolution_type = db.Column(db.String(50), nullable=False)  # duplicate, evolve, extend, remix, stem, variation
    evolution_params = db.Column(db.JSON)  # What parameters changed
    
    # Prompt changes
    original_prompt = db.Column(db.Text)
    evolved_prompt = db.Column(db.Text)
    prompt_delta = db.Column(db.Text)  # What was added/changed
    
    # Creator tracking
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    # Branch metadata
    branch_name = db.Column(db.String(100))
    is_merge = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ============================================================================================
# PHASE 7: AUDIO TIMELINE ENGINE MODELS
# ============================================================================================

class AudioClip(db.Model):
    """Individual audio segments on the timeline with clip-level controls.
    
    Represents a placed audio asset on a track with:
    - Position and duration
    - Clip-level effects (fade, gain, pitch, time stretch)
    - Clip metadata and color
    - Prompt lineage
    """
    __tablename__ = 'audio_clips'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("audio_projects.id"), nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey("audio_tracks.id"), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey("audio_assets.id"), nullable=False)
    
    # Timeline position
    start_time = db.Column(db.Float, nullable=False)  # Start on timeline (seconds)
    end_time = db.Column(db.Float, nullable=False)    # End on timeline
    
    # Source trimming (which part of the asset to play)
    source_start = db.Column(db.Float, default=0.0)   # Trim start in source audio
    source_end = db.Column(db.Float)                  # Trim end in source audio
    
    # Clip-level controls
    clip_gain = db.Column(db.Float, default=0.0)      # Gain in dB (-60 to +24)
    pitch_shift = db.Column(db.Float, default=0.0)    # Semitones (-12 to +12)
    time_stretch = db.Column(db.Float, default=1.0)   # Speed multiplier (0.5 to 2.0)
    
    # Fades
    fade_in_duration = db.Column(db.Float, default=0.0)   # Fade in duration (seconds)
    fade_out_duration = db.Column(db.Float, default=0.0)  # Fade out duration
    fade_in_curve = db.Column(db.String(20), default="linear")   # linear, exponential, logarithmic, s-curve
    fade_out_curve = db.Column(db.String(20), default="linear")
    
    # Clip effects (separate from track effects)
    clip_effects = db.Column(db.JSON)  # Array of clip-specific effects
    
    # Visual properties
    clip_color = db.Column(db.String(7), default="#00D9FF")  # Hex color
    clip_name = db.Column(db.String(255))
    
    # Metadata
    notes = db.Column(db.Text)
    tags = db.Column(db.String(500))
    
    # Locked state (prevents accidental edits)
    is_locked = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AudioAutomation(db.Model):
    """Automation curves for dynamic parameter control over time.
    
    Supports automation of:
    - Volume
    - Pan
    - Effect parameters
    - Send levels
    - Filter cutoff
    - EQ bands
    """
    __tablename__ = 'audio_automation'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("audio_projects.id"), nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey("audio_tracks.id"))
    clip_id = db.Column(db.Integer, db.ForeignKey("audio_clips.id"))
    
    # Automation target
    automation_type = db.Column(db.String(50), nullable=False)  # volume, pan, reverb_send, delay_send, filter_cutoff, eq_band_1, etc.
    parameter_name = db.Column(db.String(100))  # Specific parameter (e.g., "eq_high", "reverb_wet")
    
    # Automation points (keyframes)
    points = db.Column(db.JSON, nullable=False)  # Array of {time, value, curve} objects
    # Example: [{"time": 0.0, "value": 0.0, "curve": "linear"}, {"time": 5.0, "value": 1.0, "curve": "exponential"}]
    
    # Curve interpolation
    default_curve = db.Column(db.String(20), default="linear")  # linear, exponential, logarithmic, s-curve, step
    
    # Lock state (locked automation can't be overwritten)
    is_locked = db.Column(db.Boolean, default=False)
    
    # Visual properties
    lane_color = db.Column(db.String(7), default="#FFD700")
    is_visible = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AudioEffect(db.Model):
    """Audio effects applied to tracks or clips.
    
    Built-in effects:
    - EQ
    - Compressor
    - Reverb
    - Delay
    - Chorus
    - Distortion
    - Filter
    - Noise reduction
    """
    __tablename__ = 'audio_effects'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("audio_projects.id"), nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey("audio_tracks.id"))
    clip_id = db.Column(db.Integer, db.ForeignKey("audio_clips.id"))
    
    # Effect type
    effect_type = db.Column(db.String(50), nullable=False)  # eq, compressor, reverb, delay, chorus, distortion, filter, noise_reduction
    
    # Effect parameters (stored as JSON for flexibility)
    parameters = db.Column(db.JSON, nullable=False)
    # Examples:
    # EQ: {"low": 0, "mid": 2, "high": 1, "low_freq": 100, "mid_freq": 1000, "high_freq": 10000}
    # Compressor: {"threshold": -20, "ratio": 4, "attack": 5, "release": 100, "knee": 3}
    # Reverb: {"wet": 0.3, "dry": 0.7, "room_size": 0.5, "decay": 2.0, "pre_delay": 10}
    # Delay: {"time": 0.5, "feedback": 0.3, "wet": 0.25, "dry": 0.75, "sync": true}
    
    # Effect chain position
    order_index = db.Column(db.Integer, default=0)  # Position in the effects chain
    
    # Effect state
    is_enabled = db.Column(db.Boolean, default=True)
    is_bypassed = db.Column(db.Boolean, default=False)
    
    # Preset
    preset_name = db.Column(db.String(100))
    preset_id = db.Column(db.Integer, db.ForeignKey("audio_effect_presets.id"))
    
    # Visual properties
    is_collapsed = db.Column(db.Boolean, default=False)  # UI state
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AudioMixerSettings(db.Model):
    """Mixer channel strip settings for each track + master bus.
    
    Stores:
    - Channel strip settings (fader, pan, mute, solo)
    - Send/return levels
    - Track routing
    - Metering info
    """
    __tablename__ = 'audio_mixer_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("audio_projects.id"), nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey("audio_tracks.id"))  # NULL for master bus
    
    # Channel strip
    fader_level = db.Column(db.Float, default=0.0)      # Volume in dB (-60 to +12)
    pan_position = db.Column(db.Float, default=0.0)     # Pan (-1.0 left to 1.0 right)
    
    # Solo/mute
    is_muted = db.Column(db.Boolean, default=False)
    is_solo = db.Column(db.Boolean, default=False)
    is_armed = db.Column(db.Boolean, default=False)     # Recording arm
    
    # Send levels (aux sends to reverb, delay buses)
    reverb_send = db.Column(db.Float, default=0.0)      # dB
    delay_send = db.Column(db.Float, default=0.0)
    aux_1_send = db.Column(db.Float, default=0.0)
    aux_2_send = db.Column(db.Float, default=0.0)
    
    # Routing
    output_bus = db.Column(db.String(50), default="master")  # master, aux_1, aux_2, external
    input_source = db.Column(db.String(100))  # For recording
    
    # Metering (peak/RMS levels - updated in real-time)
    peak_level_left = db.Column(db.Float, default=-60.0)
    peak_level_right = db.Column(db.Float, default=-60.0)
    rms_level_left = db.Column(db.Float, default=-60.0)
    rms_level_right = db.Column(db.Float, default=-60.0)
    
    # Visual properties
    track_color = db.Column(db.String(7), default="#00D9FF")
    track_height = db.Column(db.Integer, default=80)  # Pixels
    is_collapsed = db.Column(db.Boolean, default=False)
    
    # Timestamps
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AudioEffectPreset(db.Model):
    """Saved effect presets for quick recall.
    
    Users can save their favorite effect settings and reuse them across projects.
    """
    __tablename__ = 'audio_effect_presets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))
    
    # Preset identification
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # vocal, drums, guitar, bass, master, creative
    
    # Effect configuration
    effect_type = db.Column(db.String(50), nullable=False)
    parameters = db.Column(db.JSON, nullable=False)
    
    # Tags for discovery
    tags = db.Column(db.String(500))
    
    # Sharing
    is_public = db.Column(db.Boolean, default=False)
    is_factory = db.Column(db.Boolean, default=False)  # Built-in presets
    
    # Usage tracking
    use_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============================================================================================
# END PHASE 7 MODELS
# ============================================================================================

# Initialize database tables
with app.app_context():
    db.create_all()

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ============================================================================
# PERMISSION HELPERS - Role-Based Access Control
# ============================================================================

def get_user_role(team_id: int, user_id: int) -> str:
    """Get user's role in a team. Returns None if not a member."""
    if user_id is None or team_id is None:
        return None
    membership = TeamMember.query.filter_by(team_id=team_id, user_id=user_id).first()
    return membership.role if membership else None

def can_view_team(team_id: int, user_id: int) -> bool:
    """All members can view (viewer, editor, admin, owner)."""
    if user_id is None:
        return False
    return get_user_role(team_id, user_id) is not None

def can_create_project(team_id: int, user_id: int) -> bool:
    """Editor, Admin, Owner can create projects."""
    role = get_user_role(team_id, user_id)
    return role in ['editor', 'admin', 'owner']

def can_edit_project(project_id: int, user_id: int, team_id: int) -> bool:
    """Check if user can edit a specific project."""
    project = GraphicsProject.query.get(project_id)
    if not project:
        return False
    
    role = get_user_role(team_id, user_id)
    
    # Admin and Owner can edit any team project
    if role in ['admin', 'owner']:
        return True
    
    # Editor can edit their own projects
    if role == 'editor' and project.user_id == user_id:
        return True
    
    return False

def can_delete_project(team_id: int, user_id: int) -> bool:
    """Admin and Owner can delete any project."""
    role = get_user_role(team_id, user_id)
    return role in ['admin', 'owner']

def can_manage_members(team_id: int, user_id: int) -> bool:
    """Admin and Owner can manage members."""
    role = get_user_role(team_id, user_id)
    return role in ['admin', 'owner']

def can_delete_team(team_id: int, user_id: int) -> bool:
    """Only Owner can delete team."""
    return get_user_role(team_id, user_id) == 'owner'

def can_change_role(team_id: int, user_id: int, target_role: str) -> bool:
    """Check if user can change someone to target_role."""
    role = get_user_role(team_id, user_id)
    
    # Only owner can promote to owner
    if target_role == 'owner':
        return role == 'owner'
    
    # Admin and owner can change other roles
    return role in ['admin', 'owner']

def is_owner(user_id: int, team_id: int) -> bool:
    """Check if user is an owner of the team."""
    return TeamMember.query.filter_by(
        user_id=user_id, team_id=team_id, role="owner"
    ).first() is not None

def is_admin(user_id: int, team_id: int) -> bool:
    """Check if user is an admin or owner (has admin privileges)."""
    return TeamMember.query.filter(
        TeamMember.user_id == user_id,
        TeamMember.team_id == team_id,
        TeamMember.role.in_(["owner", "admin"])
    ).first() is not None

def is_editor(user_id: int, team_id: int) -> bool:
    """Check if user is an editor, admin, or owner (can create/edit)."""
    return TeamMember.query.filter(
        TeamMember.user_id == user_id,
        TeamMember.team_id == team_id,
        TeamMember.role.in_(["owner", "admin", "editor"])
    ).first() is not None

# ============================================================================
# ACTIVITY LOGGING
# ============================================================================

def log_activity(team_id, user_id, action, metadata=None):
    """Log team activity for audit trail and activity feeds."""
    entry = TeamActivity(
        team_id=team_id,
        user_id=user_id,
        action=action,
        metadata=metadata or {}
    )
    db.session.add(entry)
    db.session.commit()


# =============================================================================
# VIDEO STUDIO - STORAGE & GENERATION PIPELINE
# =============================================================================

class VideoStorageConfig:
    """Configuration for video asset storage.
    
    Supports multiple storage providers:
    - AWS S3
    - Google Cloud Storage
    - Azure Blob Storage
    - Local filesystem (development)
    """
    def __init__(self):
        self.provider = os.getenv('VIDEO_STORAGE_PROVIDER', 'local')  # s3, gcs, azure, local
        
        # AWS S3
        self.s3_bucket = os.getenv('AWS_S3_BUCKET')
        self.s3_region = os.getenv('AWS_S3_REGION', 'us-east-1')
        self.s3_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.s3_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        
        # Google Cloud Storage
        self.gcs_bucket = os.getenv('GCS_BUCKET')
        self.gcs_credentials = os.getenv('GCS_CREDENTIALS_PATH')
        
        # Azure Blob Storage
        self.azure_container = os.getenv('AZURE_CONTAINER')
        self.azure_connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        
        # Local storage (development)
        self.local_path = os.getenv('VIDEO_STORAGE_PATH', 'uploads/videos')
        self.local_base_url = os.getenv('VIDEO_BASE_URL', 'http://localhost:5000/videos')
    
    def get_upload_url(self, filename: str) -> str:
        """Generate upload URL based on provider."""
        if self.provider == 's3':
            return f"https://{self.s3_bucket}.s3.{self.s3_region}.amazonaws.com/{filename}"
        elif self.provider == 'gcs':
            return f"https://storage.googleapis.com/{self.gcs_bucket}/{filename}"
        elif self.provider == 'azure':
            return f"https://{self.azure_container}.blob.core.windows.net/{filename}"
        else:  # local
            return f"{self.local_base_url}/{filename}"


class VideoGenerationPipeline:
    """Pipeline for AI video generation.
    
    Supports multiple generation engines:
    - Runway Gen-3
    - Pika Labs
    - Luma AI
    - Stability Video
    - Custom endpoints
    """
    def __init__(self):
        self.default_engine = os.getenv('VIDEO_GEN_ENGINE', 'runway')
        
        # API keys
        self.runway_api_key = os.getenv('RUNWAY_API_KEY')
        self.pika_api_key = os.getenv('PIKA_API_KEY')
        self.luma_api_key = os.getenv('LUMA_API_KEY')
        self.stability_api_key = os.getenv('STABILITY_API_KEY')
        
        # Custom endpoint
        self.custom_api_url = os.getenv('VIDEO_GEN_API_URL')
        self.custom_api_key = os.getenv('VIDEO_GEN_API_KEY')
    
    def generate_video(self, prompt: str, engine: str = None, **kwargs):
        """Generate video from prompt using specified engine.
        
        Args:
            prompt: Text description of the video
            engine: "runway", "pika", "luma", "stability", or None (use default)
            **kwargs: Engine-specific parameters (duration, resolution, etc.)
        
        Returns:
            dict: {
                "video_url": "https://...",
                "thumbnail_url": "https://...",
                "duration": 5.0,
                "status": "complete"
            }
        """
        engine = engine or self.default_engine
        
        if engine == 'runway':
            return self._generate_runway(prompt, **kwargs)
        elif engine == 'pika':
            return self._generate_pika(prompt, **kwargs)
        elif engine == 'luma':
            return self._generate_luma(prompt, **kwargs)
        elif engine == 'stability':
            return self._generate_stability(prompt, **kwargs)
        elif engine == 'custom':
            return self._generate_custom(prompt, **kwargs)
        else:
            raise ValueError(f"Unknown generation engine: {engine}")
    
    def _generate_runway(self, prompt: str, **kwargs):
        """Generate video using Runway Gen-3."""
        try:
            from video_engines import generate_runway
            return generate_runway(prompt, **kwargs)
        except Exception as e:
            # Fallback to placeholder on error
            print(f"⚠️ Runway generation failed: {e}")
            from video_engines.runway import generate_placeholder
            return generate_placeholder(prompt, **kwargs)
    
    def _generate_pika(self, prompt: str, **kwargs):
        """Generate video using Pika Labs."""
        try:
            from video_engines import generate_pika
            return generate_pika(prompt, **kwargs)
        except Exception as e:
            print(f"⚠️ Pika generation failed: {e}")
            from video_engines.pika import generate_placeholder
            return generate_placeholder(prompt, **kwargs)
    
    def _generate_luma(self, prompt: str, **kwargs):
        """Generate video using Luma AI."""
        try:
            from video_engines import generate_luma
            return generate_luma(prompt, **kwargs)
        except Exception as e:
            print(f"⚠️ Luma generation failed: {e}")
            from video_engines.luma import generate_placeholder
            return generate_placeholder(prompt, **kwargs)
    
    def _generate_stability(self, prompt: str, **kwargs):
        """Generate video using Stability Video."""
        try:
            from video_engines import generate_stability
            return generate_stability(prompt, **kwargs)
        except Exception as e:
            print(f"⚠️ Stability generation failed: {e}")
            from video_engines.stability import generate_placeholder
            return generate_placeholder(prompt, **kwargs)
    
    def _generate_custom(self, prompt: str, **kwargs):
        """Generate video using custom API endpoint."""
        # Placeholder implementation - replace with actual custom API calls
        return {
            "video_url": "https://example.com/video.mp4",
            "thumbnail_url": "https://example.com/thumb.jpg",
            "duration": kwargs.get('duration', 5.0),
            "status": "complete",
            "engine": "custom"
        }


# Initialize video systems
video_storage = VideoStorageConfig()
video_pipeline = VideoGenerationPipeline()

# Initialize Universal Generation Interface (UGI) - Phase 3
from universal_generation_interface import UniversalGenerationInterface
video_ugi = None  # Will be initialized after db setup


# ============================================================================
# JSON UTILITIES
# ============================================================================

# Base directory for JSON files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# JSON cache for performance
_json_cache = {}

def load_json(filename: str, use_cache: bool = True) -> Dict[str, Any]:
    """
    Universal JSON loader with intelligent fallback and caching

    Handles:
    - Root directory lookup (using BASE_DIR)
    - /data directory fallback
    - Missing files (returns empty dict)
    - JSON parse errors (returns empty dict)
    - Optional caching for performance
    - UTF-8 encoding for all files

    Args:
        filename: Name of JSON file (e.g., 'cycles.json')
        use_cache: Enable in-memory caching (default: True)

    Returns:
        Dict containing JSON data or empty dict on error
    """
    # Check cache first
    if use_cache and filename in _json_cache:
        return _json_cache[filename]

    search_paths = [
        os.path.join(BASE_DIR, filename),              # Root: /app/cycles.json
        os.path.join(BASE_DIR, 'data', filename),      # Data dir: /app/data/cycles.json
    ]

    for path in search_paths:
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Cache the result
                if use_cache:
                    _json_cache[filename] = data

                return data
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parse error in {path}: {e}")
            continue
        except Exception as e:
            print(f"⚠️ Error reading {path}: {e}")
            continue

    # File not found in any location
    print(f"⚠️ JSON file not found: {filename} (searched {len(search_paths)} locations)")
    return {}

def clear_json_cache():
    """Clear JSON cache to force reload"""
    global _json_cache
    _json_cache = {}

def load_json_response(filename: str, use_cache: bool = True):
    """
    Load JSON file and return Flask JSON response

    Returns jsonify() response with data or error message
    """
    data = load_json(filename, use_cache)
    if not data:
        return jsonify({"error": f"File not found or empty: {filename}"}), 404
    return jsonify(data)

# Intelligence Core Helper Functions
def get_industry(industry_id: str) -> Dict[str, Any]:
    """Get industry by ID from industries.json"""
    data = load_json("industries.json")
    industries = data.get("industries", [])
    return next((i for i in industries if i.get("id") == industry_id), {})

def get_niche(niche_id: str) -> Dict[str, Any]:
    """Get niche by ID from niches.json"""
    data = load_json("niches.json")
    niches = data.get("niches", [])
    return next((n for n in niches if n.get("id") == niche_id), {})

def get_domain_pack(pack_id: str) -> Dict[str, Any]:
    """Get domain pack by ID from domain_packs.json"""
    data = load_json("domain_packs.json")
    packs = data.get("domain_packs", [])
    return next((p for p in packs if p.get("id") == pack_id), {})

def get_niches_by_industry(industry_id: str) -> List[Dict[str, Any]]:
    """Get all niches for a specific industry"""
    data = load_json("niches.json")
    niches = data.get("niches", [])
    return [n for n in niches if n.get("industry") == industry_id]

def get_engines_for_niche(niche_id: str) -> List[str]:
    """Get active engines for a specific niche"""
    niche = get_niche(niche_id)
    return niche.get("active_engines", [])

def get_capsules_for_industry(industry_id: str) -> Dict[str, List[str]]:
    """Get primary and secondary capsules for an industry"""
    industry = get_industry(industry_id)
    return {
        "primary": industry.get("primary_capsules", []),
        "secondary": industry.get("secondary_capsules", [])
    }

def get_blueprint_for_niche(niche_id: str) -> Dict[str, Any]:
    """Get complete blueprint for a niche"""
    niche = get_niche(niche_id)
    return niche.get("blueprint", {})

def get_pack_components(pack_id: str) -> Dict[str, Any]:
    """Get components (templates, workflows, integrations) for a domain pack"""
    pack = get_domain_pack(pack_id)
    return pack.get("components", {})

def get_compliance_for_industry(industry_id: str) -> List[str]:
    """Get compliance requirements for an industry"""
    industry = get_industry(industry_id)
    return industry.get("compliance_requirements", [])

def cross_reference_industry(industry_id: str) -> Dict[str, Any]:
    """Get complete cross-reference: industry → niches → packs"""
    industry = get_industry(industry_id)
    niches = get_niches_by_industry(industry_id)
    
    # Get packs for this industry
    packs_data = load_json("domain_packs.json")
    packs = [p for p in packs_data.get("domain_packs", []) if p.get("industry") == industry_id]
    
    return {
        "industry": industry,
        "niches": niches,
        "packs": packs,
        "stats": {
            "niche_count": len(niches),
            "pack_count": len(packs),
            "total_engines": len(set(e for n in niches for e in n.get("active_engines", [])))
        }
    }

def get_phase_1_status() -> Dict[str, Any]:
    """Get Phase 1 (Structural Intelligence) activation status"""
    industries_data = load_json("industries.json")
    niches_data = load_json("niches.json")
    packs_data = load_json("domain_packs.json")
    
    return {
        "phase": 1,
        "name": "Structural Intelligence",
        "status": "operational",
        "engines": [
            {
                "name": "Industry Ontology Engine",
                "file": "industries.json",
                "count": len(industries_data.get("industries", [])),
                "operational": True
            },
            {
                "name": "Niche Blueprint Engine",
                "file": "niches.json",
                "count": len(niches_data.get("niches", [])),
                "operational": True
            },
            {
                "name": "Domain Expertise Packs",
                "file": "domain_packs.json",
                "count": len(packs_data.get("domain_packs", [])),
                "operational": True
            }
        ],
        "next_phase": {
            "phase": 2,
            "name": "Observability and Replay",
            "engines": ["Experience Replay Engine", "Cross-Capsule Sync"]
        }
    }

def get_industries_dict() -> Dict[str, Dict[str, Any]]:
    """Get industries as dict keyed by ID for quick lookup"""
    data = load_json("industries.json")
    industries = data.get("industries", [])
    return {i["id"]: i for i in industries}

def get_niches_dict() -> Dict[str, Dict[str, Any]]:
    """Get niches as dict keyed by ID for quick lookup"""
    data = load_json("niches.json")
    niches = data.get("niches", [])
    return {n["id"]: n for n in niches}

def get_domain_packs_dict() -> Dict[str, Dict[str, Any]]:
    """Get domain packs as dict keyed by ID for quick lookup"""
    data = load_json("domain_packs.json")
    packs = data.get("domain_packs", [])
    return {p["id"]: p for p in packs}

# Database imports
from database import SessionLocal, init_db
from models import Council, Agent, AgentReputation, AgentTraining, PortalNotification, NotificationType
from sqlalchemy.orm import joinedload
from flask import g

# Load capsules and intelligence core data at module level
capsules_json = load_json("capsules.json")
intelligence_json = load_json("intelligence_core.json")
agents_json = load_json("agents_simple.json")  # Use simplified agents structure
# councils_json = load_json("councils.json")  # MIGRATED TO DATABASE
tools_json = load_json("tools.json")

# ==================== DATABASE SESSION MANAGEMENT ====================

# Initialize database on startup (Flask 3.0+ pattern)
try:
    init_db()
    # Use sys.stderr for output since stdout may be redirected
    import sys
    sys.stderr.write("✅ Database initialized\n")
except Exception as e:
    import sys
    sys.stderr.write(f"⚠️ Database initialization skipped: {e}\n")

@app.before_request
def create_session():
    """Create database session for each request"""
    g.db = SessionLocal()

@app.teardown_request
def shutdown_session(exception=None):
    """Close database session after each request"""
    db = getattr(g, "db", None)
    if db is not None:
        if exception:
            db.rollback()
        else:
            db.commit()
        db.close()

# ==================== REDIS QUEUE (RQ) SETUP ====================
# Initialize Redis connection and RQ Queue for background job processing
redis_conn = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
queue = Queue("workflows", connection=redis_conn)

# Dashboard HTML Template
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>👑 CODEX DOMINION MASTER DASHBOARD ULTIMATE</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e2e8f0;
            min-height: 100vh;
            padding: 20px;
        }

        .container { max-width: 1600px; margin: 0 auto; padding: 0; }

        .header {
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            padding: 48px;
            border-radius: 24px;
            text-align: center;
            margin-bottom: 32px;
            box-shadow: 0 20px 60px rgba(251, 191, 36, 0.2);
            border: 1px solid rgba(251, 191, 36, 0.3);
        }

        .header h1 { 
            font-size: 3.5em; 
            margin-bottom: 12px; 
            color: #1e293b;
            font-weight: 800;
            letter-spacing: -0.02em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .header p { 
            font-size: 1.3em; 
            color: #334155;
            font-weight: 500;
        }


        .banner {
            background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
            padding: 24px;
            border-radius: 16px;
            text-align: center;
            color: white;
            font-size: 1.4em;
            font-weight: 700;
            margin-bottom: 32px;
            box-shadow: 0 10px 40px rgba(59, 130, 246, 0.3);
            border: 1px solid rgba(139, 92, 246, 0.3);
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 24px;
            margin-bottom: 32px;
        }

        .card {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            padding: 32px;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
            transition: all 0.3s ease;
            border: 1px solid rgba(148, 163, 184, 0.1);
        }

        .card:hover { 
            transform: translateY(-5px);
            box-shadow: 0 12px 48px rgba(0,0,0,0.6);
        }

        .card h2 {
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 16px;
            font-size: 1.8em;
            font-weight: 700;
        }

        .card p { 
            color: #cbd5e1; 
            margin-bottom: 20px; 
            line-height: 1.8;
            font-size: 1.05em;
        }


        .btn {
            display: inline-block;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            padding: 14px 32px;
            border-radius: 12px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
            font-size: 1.05em;
            box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(59, 130, 246, 0.5);
        }

        .metric {
            text-align: center;
            padding: 24px;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            border-radius: 16px;
            margin: 12px 0;
            box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
            border: 1px solid rgba(16, 185, 129, 0.3);
        }

        .metric h3 { font-size: 3em; margin-bottom: 8px; font-weight: 800; }
        .metric p { font-size: 1.1em; opacity: 0.95; font-weight: 500; }

        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin: 24px 0;
        }

        .tool-card {
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            padding: 24px;
            border-radius: 16px;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
            border: 1px solid rgba(139, 92, 246, 0.3);
        }

        .tool-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(139, 92, 246, 0.5);
        }

        .tool-card h3 { margin-bottom: 12px; font-size: 1.3em; font-weight: 700; }
        .tool-card .savings {
            background: rgba(251,191,36,0.3);
            padding: 8px 16px;
            border-radius: 8px;
            margin: 12px 0;
            font-weight: 700;
            font-size: 1.1em;
            border: 1px solid rgba(251,191,36,0.5);
        }

        .status {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 20px;
            border-radius: 16px;
            text-align: center;
            font-size: 1.3em;
            font-weight: 700;
            margin: 24px 0;
            box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
            border: 1px solid rgba(16, 185, 129, 0.3);
        }


        /* Navigation Tabs */
        .nav-tabs {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin: 24px 0;
            padding: 20px;
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border-radius: 16px;
            border: 1px solid rgba(148, 163, 184, 0.1);
            box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        }

        .nav-tab {
            padding: 12px 24px;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            text-decoration: none;
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.3s ease;
            font-size: 1.05em;
            border: 1px solid rgba(139, 92, 246, 0.3);
        }

        .nav-tab:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5);
        }

        .nav-tab.active {
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            box-shadow: 0 4px 16px rgba(251, 191, 36, 0.4);
        }

        /* External Dashboards Section */
        .external-dashboards {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            padding: 32px;
            border-radius: 20px;
            margin: 32px 0;
            border: 1px solid rgba(148, 163, 184, 0.1);
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        }

        .external-dashboards h3 {
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 24px;
            font-size: 1.8em;
            text-align: center;
            font-weight: 700;
        }

        .dashboard-links {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
        }

        .dashboard-link {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px 24px;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            text-decoration: none;
            border-radius: 12px;
            font-weight: 600;
            transition: all 0.3s ease;
            text-align: center;
            box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
            border: 1px solid rgba(139, 92, 246, 0.3);
        }

        .dashboard-link:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(139, 92, 246, 0.5);
        }

        .dashboard-link.nextjs {
            background: linear-gradient(135deg, #000000 0%, #434343 100%);
        }

        .dashboard-link.streamlit {
            background: linear-gradient(135deg, #ff4b4b 0%, #ff8c8c 100%);
        }

        .dashboard-link.analytics {
            background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>👑 CODEXDOMINION MASTER DASHBOARD ULTIMATE</h1>
            <p>Complete Command Center with 48 Intelligence Engines & Free Tools Suite</p>
        </div>

        <div class="banner">
            🆕 NEW: 48 Intelligence Engines + $316/month in FREE Tools!
        </div>

        <div class="status">
            ✅ ALL SYSTEMS OPERATIONAL - Running on Flask (Python {{ python_version }})
        </div>

        <!-- External Dashboards Hub -->
        <div class="external-dashboards">
            <h3>🚀 ACCESS ALL DASHBOARDS</h3>
            <div class="dashboard-links">
                <a href="http://localhost:3002" target="_blank" class="dashboard-link nextjs">
                    ⚡ Next.js Dashboard<br><small>(Modern React UI)</small>
                </a>
                <a href="http://localhost:8501" target="_blank" class="dashboard-link streamlit">
                    📊 Streamlit Production<br><small>(Data Analytics)</small>
                </a>
                <a href="http://localhost:8502" target="_blank" class="dashboard-link streamlit">
                    🧪 Streamlit Staging<br><small>(Testing)</small>
                </a>
                <a href="http://localhost:8515" target="_blank" class="dashboard-link analytics">
                    📈 Stock Analytics<br><small>(AI Trading)</small>
                </a>
                <a href="http://localhost:8516" target="_blank" class="dashboard-link analytics">
                    🔍 Enhanced Analytics<br><small>(Deep Insights)</small>
                </a>
                <a href="http://localhost:3000" target="_blank" class="dashboard-link nextjs">
                    🎯 Primary Next.js<br><small>(Port 3000)</small>
                </a>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="nav-tabs">
            <a href="/" class="nav-tab active">🏠 Home</a>
            <a href="/engines" class="nav-tab">🧠 48 Engines</a>
            <a href="/tools" class="nav-tab">🔧 6 Tools</a>
            <a href="/dashboards" class="nav-tab">📊 All Dashboards</a>
            <a href="/chat" class="nav-tab">💬 AI Chat</a>
            <a href="/agents" class="nav-tab">🤖 AI Agents</a>
            <a href="/creative-agents" class="nav-tab">🔥 Creative Agents</a>
            <a href="/websites" class="nav-tab">🌐 Websites</a>
            <a href="/stores" class="nav-tab">🛒 Stores</a>
            <a href="/social" class="nav-tab">📱 Social Media</a>
            <a href="/affiliate" class="nav-tab">💰 Affiliate</a>
            <a href="/chatbot" class="nav-tab">🤖 Action Chatbot</a>
            <a href="/algorithm" class="nav-tab">🧠 Algorithm AI</a>
            <a href="/autopublish" class="nav-tab">🚀 Auto-Publish</a>
            <a href="/automation-calculator" class="nav-tab">💡 ROI Calculator</a>
            <a href="/email" class="nav-tab">📧 Email</a>
            <a href="/documents" class="nav-tab">📄 Documents</a>
            <a href="/avatars" class="nav-tab">👤 Avatars</a>
            <a href="/council" class="nav-tab">👑 Council</a>
            <a href="/copilot" class="nav-tab">🚁 Copilot</a>
        </div>

        <div class="grid">
            <div class="card">
                <h2>🧠 48 Intelligence Engines</h2>
                <p>Complete intelligence system covering 24 domains with Research & Execution modes</p>
                <div class="metric">
                    <h3>48</h3>
                    <p>Active Engines</p>
                </div>
                <p><strong>Clusters:</strong> Technology, Bioengineering, Security, Communication, Planetary, Business</p>
                <a href="/engines" class="btn">Launch Engines</a>
            </div>

            <div class="card">
                <h2>🔧 Codex Tools Suite</h2>
                <p>6 FREE tools replacing expensive subscriptions</p>
                <div class="metric">
                    <h3>$316/mo</h3>
                    <p>Total Savings</p>
                </div>
                <p><strong>Tools:</strong> Flow Orchestrator, AI Content Engine, Research Studio, Design Forge, Nano Builder, App Constructor</p>
                <a href="/tools" class="btn">Launch Tools</a>
            </div>

            <div class="card">
                <h2>📊 System Metrics</h2>
                <p>Real-time performance and status</p>
                <div class="metric">
                    <h3>{{ total_dashboards }}</h3>
                    <p>Total Dashboards</p>
                </div>
                <div class="metric">
                    <h3>99.9%</h3>
                    <p>Uptime</p>
                </div>
                <a href="/status" class="btn">View Status</a>
            </div>
        </div>

        <div class="card">
            <h2>💰 FREE Tools - Zero Subscriptions</h2>
            <div class="tools-grid">
                <div class="tool-card">
                    <h3>⚙️ Flow Orchestrator</h3>
                    <p>Replaces N8N</p>
                    <div class="savings">Save $50/mo</div>
                </div>
                <div class="tool-card">
                    <h3>✨ AI Content Engine</h3>
                    <p>Replaces GenSpark</p>
                    <div class="savings">Save $99/mo</div>
                </div>
                <div class="tool-card">
                    <h3>📚 Research Studio</h3>
                    <p>Replaces NotebookLLM</p>
                    <div class="savings">Save $20/mo</div>
                </div>
                <div class="tool-card">
                    <h3>🎨 Design Forge</h3>
                    <p>Replaces Designrr</p>
                    <div class="savings">Save $39/mo</div>
                </div>
                <div class="tool-card">
                    <h3>🔧 Nano Builder</h3>
                    <p>Replaces Nano Banana</p>
                    <div class="savings">Save $29/mo</div>
                </div>
                <div class="tool-card">
                    <h3>🏗️ App Constructor</h3>
                    <p>Replaces Loveable</p>
                    <div class="savings">Save $79/mo</div>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>🌟 All Dashboards ({{ total_dashboards }}+)</h2>
            <p>Complete dashboard ecosystem</p>
            <ul style="list-style: none; padding: 20px 0;">
                {% for name in dashboard_names %}
                <li style="padding: 12px 16px; border-bottom: 1px solid rgba(148, 163, 184, 0.2); color: #cbd5e1; background: rgba(30, 41, 59, 0.5); margin: 8px 0; border-radius: 8px; transition: all 0.2s;">
                    📊 {{ name }}
                </li>
                {% endfor %}
            </ul>
            <p style="margin-top: 20px; color: #94a3b8; font-size: 0.95em;">And {{ total_dashboards - 10 }} more specialized dashboards...</p>
        </div>
    </div>
</body>
</html>
"""

ENGINES_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🧠 48 Intelligence Engines</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; }
        h1 { color: #667eea; }
        .back { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }
        .cluster { margin: 30px 0; padding: 20px; background: #f5f5f5; border-radius: 10px; }
        .cluster h2 { color: #764ba2; }
        .engine { padding: 15px; margin: 10px 0; background: white; border-radius: 8px; border-left: 4px solid #667eea; }
        .engine strong { color: #667eea; }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        <h1>🧠 48 Intelligence Engines</h1>
        <p>Complete intelligence system covering 24 domains × 2 modes = 48 engines</p>

        {% for cluster_name, engines in clusters.items() %}
        <div class="cluster">
            <h2>{{ cluster_name }} Cluster ({{ engines|length }} engines)</h2>
            {% for engine in engines %}
            <div class="engine">
                <strong>{{ engine.icon }} {{ engine.name }}</strong>
                <br>
                <span style="color: #888;">Domain: {{ engine.domain }} | Mode: {{ engine.mode }}</span>
                <br>
                <small>Capabilities: {{ engine.capabilities|join(', ') }}</small>
            </div>
            {% endfor %}
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

TOOLS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🔧 Codex Tools Suite</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; }
        h1 { color: #667eea; }
        .back { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }
        .savings-banner {
            background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: white;
            margin: 20px 0;
            font-size: 1.5em;
            font-weight: bold;
        }
        .tool {
            margin: 20px 0;
            padding: 25px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px;
            border-left: 5px solid #667eea;
        }
        .tool h2 { color: #667eea; margin-bottom: 10px; }
        .tool .replaces {
            background: #ff6b6b;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            display: inline-block;
            margin: 10px 0;
            font-weight: bold;
        }
        .tool .savings {
            background: #51cf66;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            display: inline-block;
            margin: 10px 5px;
            font-weight: bold;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin: 15px 0;
        }
        .feature {
            background: white;
            padding: 10px;
            border-radius: 8px;
            font-size: 0.9em;
        }
        .status {
            background: #51cf66;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            display: inline-block;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        <h1>🔧 Codex Tools Suite</h1>
        <p>Complete suite of FREE tools - Zero subscriptions, complete digital sovereignty</p>

        <div class="savings-banner">
            💰 Total Savings: $316/month = $3,792/year!
        </div>

        {% for tool in tools %}
        <div class="tool">
            <h2>{{ tool.icon }} {{ tool.name }}</h2>
            <p style="color: #666; font-size: 1.1em;">{{ tool.description }}</p>

            <div style="margin: 15px 0;">
                <span class="replaces">❌ {{ tool.replaces }}</span>
                <span class="savings">✅ Save {{ tool.savings }}</span>
                <span class="status">🟢 {{ tool.status|upper }}</span>
            </div>

            <h3 style="color: #764ba2; margin-top: 20px;">Features:</h3>
            <div class="features">
                {% for feature in tool.features %}
                <div class="feature">✓ {{ feature }}</div>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

CHAT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>💬 AI Chat - Codex Dominion</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            margin: 0;
        }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; }
        .back { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }
        h1 { color: #667eea; }
        .chat-container {
            display: grid;
            grid-template-columns: 250px 1fr;
            gap: 20px;
            height: 600px;
        }
        .ai-models {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 10px;
            overflow-y: auto;
        }
        .ai-model {
            padding: 10px;
            margin: 5px 0;
            background: white;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .ai-model:hover { background: #667eea; color: white; }
        .ai-model.active { background: #764ba2; color: white; }
        .chat-area {
            display: flex;
            flex-direction: column;
            background: #f9f9f9;
            border-radius: 10px;
            padding: 20px;
        }
        .messages {
            flex: 1;
            overflow-y: auto;
            margin-bottom: 20px;
            padding: 15px;
            background: white;
            border-radius: 10px;
        }
        .message {
            margin: 10px 0;
            padding: 15px;
            border-radius: 10px;
            max-width: 80%;
        }
        .user-message {
            background: #667eea;
            color: white;
            margin-left: auto;
        }
        .ai-message {
            background: #e8f5e9;
            color: #333;
        }
        .input-area {
            display: flex;
            gap: 10px;
        }
        .input-area textarea {
            flex: 1;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #667eea;
            font-family: inherit;
            font-size: 14px;
            resize: vertical;
            min-height: 60px;
        }
        .input-area button {
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.3s;
        }
        .input-area button:hover { transform: scale(1.05); }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        <h1>💬 AI Chat System</h1>
        <p>Chat with multiple AI models - Claude, VS Code Copilot, and more</p>

        <div class="chat-container">
            <div class="ai-models">
                <h3>AI Models</h3>
                <div class="ai-model active" data-model="claude">🤖 Claude Sonnet 4.5</div>
                <div class="ai-model" data-model="copilot">🚁 VS Code Copilot</div>
                <div class="ai-model" data-model="gpt">✨ GPT-4</div>
                <div class="ai-model" data-model="gemini">💎 Google Gemini</div>
                <div class="ai-model" data-model="jermaine">⚡ Jermaine Super AI</div>
                <div class="ai-model" data-model="local">🏠 Local LLM</div>
            </div>

            <div class="chat-area">
                <div class="messages" id="messages">
                    <div class="message ai-message">
                        <strong>🤖 Claude:</strong> Hello! I'm Claude Sonnet 4.5. How can I assist you today?
                    </div>
                </div>

                <div class="input-area">
                    <textarea id="userInput" placeholder="Type your message here... (Text or Voice)" rows="3"></textarea>
                    <button onclick="sendMessage()">📤 Send</button>
                    <button onclick="startVoice()" style="padding: 15px;">🎤</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentModel = 'claude';

        document.querySelectorAll('.ai-model').forEach(model => {
            model.addEventListener('click', function() {
                document.querySelectorAll('.ai-model').forEach(m => m.classList.remove('active'));
                this.classList.add('active');
                currentModel = this.dataset.model;
                addMessage('ai', `Switched to ${this.textContent.trim()}`);
            });
        });

        function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            if (!message) return;

            addMessage('user', message);
            input.value = '';

            // Simulate AI response
            setTimeout(() => {
                const responses = {
                    'claude': 'I understand. Let me help you with that...',
                    'copilot': 'Here\'s a code suggestion for your request...',
                    'gpt': 'Based on my analysis...',
                    'gemini': 'I can help with that. Here\'s what I found...',
                    'jermaine': '⚡ SUPER ACTION AI ENGAGED! Processing your request with maximum efficiency...',
                    'local': 'Processing locally on your machine...'
                };
                addMessage('ai', responses[currentModel] || 'Processing...');
            }, 1000);
        }

        function addMessage(type, text) {
            const messages = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}-message`;
            messageDiv.innerHTML = `<strong>${type === 'user' ? '👤 You:' : getModelIcon()}</strong> ${text}`;
            messages.appendChild(messageDiv);
            messages.scrollTop = messages.scrollHeight;
        }

        function getModelIcon() {
            const icons = {
                'claude': '🤖 Claude:',
                'copilot': '🚁 Copilot:',
                'gpt': '✨ GPT-4:',
                'gemini': '💎 Gemini:',
                'jermaine': '⚡ Jermaine:',
                'local': '🏠 Local:'
            };
            return icons[currentModel] || '🤖 AI:';
        }

        function startVoice() {
            if ('webkitSpeechRecognition' in window) {
                const recognition = new webkitSpeechRecognition();
                recognition.onresult = function(event) {
                    document.getElementById('userInput').value = event.results[0][0].transcript;
                };
                recognition.start();
            } else {
                alert('Voice recognition not supported in this browser');
            }
        }

        document.getElementById('userInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""

DASHBOARDS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>📊 All Dashboards - Codex Dominion</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; }
        .back { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }
        h1 { color: #667eea; }
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .dashboard-card {
            padding: 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px;
            border-left: 5px solid #667eea;
            transition: transform 0.3s;
            cursor: pointer;
        }
        .dashboard-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        .dashboard-card h3 { color: #667eea; margin-bottom: 10px; }
        .dashboard-card p { color: #666; font-size: 0.9em; }
        .category {
            margin: 30px 0;
        }
        .category h2 {
            color: #764ba2;
            border-bottom: 3px solid #764ba2;
            padding-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        <h1>📊 All Codex Dominion Dashboards (52)</h1>
        <p>Complete suite of specialized dashboards for every domain</p>

        {% for category, dashboards in all_dashboards.items() %}
        <div class="category">
            <h2>{{ category }}</h2>
            <div class="dashboard-grid">
                {% for dash in dashboards %}
                <div class="dashboard-card" onclick="alert('Launching {{ dash.name }}...')">
                    <h3>{{ dash.icon }} {{ dash.name }}</h3>
                    <p>{{ dash.description }}</p>
                    <p style="color: #764ba2; font-weight: bold; margin-top: 10px;">{{ dash.status }}</p>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

AGENTS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🤖 AI Agents - Codex Dominion</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; }
        .back { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }
        h1 { color: #667eea; }
        .agent {
            margin: 20px 0;
            padding: 25px;
            background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
            border-radius: 15px;
            border-left: 5px solid #667eea;
        }
        .agent h2 { color: #333; margin-bottom: 10px; }
        .agent .status {
            display: inline-block;
            padding: 5px 15px;
            background: #51cf66;
            color: white;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }
        .agent-actions {
            margin-top: 15px;
            display: flex;
            gap: 10px;
        }
        .agent-actions button {
            padding: 10px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-weight: bold;
        }
        .agent-actions button:hover { background: #764ba2; }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        <h1>🤖 AI Agent System</h1>
        <p>Autonomous AI agents working for your digital sovereignty</p>

        <div class="agent">
            <h2>⚡ Jermaine Super Action AI Agent</h2>
            <span class="status">🟢 ACTIVE</span>
            <p style="margin-top: 15px; color: #555;">
                Your personal AI powerhouse - handles complex tasks, automates workflows,
                and executes actions across all systems with maximum efficiency.
            </p>
            <p><strong>Capabilities:</strong> Task automation, Code generation, Data analysis,
            System integration, Multi-tool orchestration</p>
            <div class="agent-actions">
                <button onclick="alert('Activating Jermaine Super AI...')">⚡ Activate</button>
                <button onclick="alert('Configuring agent...')">⚙️ Configure</button>
                <button onclick="alert('Viewing agent logs...')">📊 View Logs</button>
            </div>
        </div>

        <div class="agent">
            <h2>🚁 VS Code Copilot Agent</h2>
            <span class="status">🟢 ACTIVE</span>
            <p style="margin-top: 15px; color: #555;">
                Integrated directly with your VS Code - provides real-time code suggestions,
                debugging assistance, and intelligent code completion.
            </p>
            <p><strong>Capabilities:</strong> Code completion, Debugging, Refactoring,
            Documentation generation, Test creation</p>
            <div class="agent-actions">
                <button onclick="alert('Opening Copilot...')">🚁 Open Copilot</button>
                <button onclick="alert('Viewing copilot-instructions.md...')">📄 Instructions</button>
            </div>
        </div>

        <div class="agent">
            <h2>🤖 Claude Agent</h2>
            <span class="status">🟢 ACTIVE</span>
            <p style="margin-top: 15px; color: #555;">
                Powered by Claude Sonnet 4.5 - handles complex reasoning, analysis,
                and content creation with advanced understanding.
            </p>
            <p><strong>Capabilities:</strong> Advanced reasoning, Long-form writing,
            Code analysis, Research, Strategic planning</p>
            <div class="agent-actions">
                <button onclick="alert('Activating Claude...')">🤖 Activate</button>
                <button onclick="alert('Setting context...')">📝 Set Context</button>
            </div>
        </div>

        <div class="agent">
            <h2>👑 Council Seal Agent</h2>
            <span class="status">🟢 ACTIVE</span>
            <p style="margin-top: 15px; color: #555;">
                Supreme governance agent - oversees all system operations,
                enforces policies, and maintains digital sovereignty.
            </p>
            <p><strong>Capabilities:</strong> Policy enforcement, Resource allocation,
            Security oversight, System governance, Strategic decisions</p>
            <div class="agent-actions">
                <button onclick="alert('Accessing Council...')">👑 Access Council</button>
                <button onclick="alert('Viewing policies...')">📜 Policies</button>
            </div>
        </div>
    </div>
</body>
</html>
"""

EMAIL_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>📧 Email - Codex Dominion</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; }
        .back { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }
        h1 { color: #667eea; }
        .email-container {
            display: grid;
            grid-template-columns: 200px 1fr;
            gap: 20px;
            height: 600px;
        }
        .email-folders {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 10px;
        }
        .folder {
            padding: 10px;
            margin: 5px 0;
            background: white;
            border-radius: 5px;
            cursor: pointer;
        }
        .folder:hover { background: #667eea; color: white; }
        .email-content {
            background: #f9f9f9;
            border-radius: 10px;
            padding: 20px;
        }
        .compose-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            margin-bottom: 15px;
        }
        .email-list {
            background: white;
            padding: 15px;
            border-radius: 10px;
        }
        .email-item {
            padding: 15px;
            border-bottom: 1px solid #eee;
            cursor: pointer;
        }
        .email-item:hover { background: #f5f5f5; }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        <h1>📧 Email System</h1>
        <p>Sovereign email management - No third-party tracking</p>

        <div class="email-container">
            <div class="email-folders">
                <button class="compose-btn">✍️ Compose</button>
                <div class="folder">📥 Inbox (5)</div>
                <div class="folder">📤 Sent</div>
                <div class="folder">⭐ Starred</div>
                <div class="folder">📝 Drafts</div>
                <div class="folder">🗑️ Trash</div>
                <div class="folder">⚙️ Settings</div>
            </div>

            <div class="email-content">
                <h2>📥 Inbox</h2>
                <div class="email-list">
                    <div class="email-item">
                        <strong>Council Seal</strong> - System Update Available
                        <div style="color: #888; font-size: 0.9em;">2 hours ago</div>
                    </div>
                    <div class="email-item">
                        <strong>Jermaine Super AI</strong> - Daily Report: All Systems Operational
                        <div style="color: #888; font-size: 0.9em;">5 hours ago</div>
                    </div>
                    <div class="email-item">
                        <strong>48 Intelligence Engines</strong> - New Insights Available
                        <div style="color: #888; font-size: 0.9em;">1 day ago</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

DOCUMENTS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>📄 Documents - Codex Dominion</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; }
        .back { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }
        h1 { color: #667eea; }
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 50px;
            text-align: center;
            margin: 20px 0;
            background: #f5f7fa;
            cursor: pointer;
        }
        .upload-area:hover { background: #e8f4f8; }
        .document-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .document {
            padding: 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 10px;
            text-align: center;
            cursor: pointer;
        }
        .document:hover { transform: translateY(-5px); }
        .doc-icon { font-size: 3em; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        <h1>📄 Document Management</h1>
        <p>Upload, organize, and analyze your documents with AI</p>

        <form action="/upload" method="post" enctype="multipart/form-data">
            <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                <div style="font-size: 3em;">📤</div>
                <h2>Upload Documents</h2>
                <p>Drag & drop files here or click to browse</p>
                <p style="color: #888; font-size: 0.9em;">Supported: PDF, DOCX, TXT, MD, Code files</p>
                <input type="file" id="fileInput" name="file" multiple style="display: none;">
            </div>
        </form>

        <h2>📁 Recent Documents</h2>
        <div class="document-grid">
            <div class="document">
                <div class="doc-icon">📄</div>
                <strong>copilot-instructions.md</strong>
                <div style="color: #888; font-size: 0.8em;">2 KB</div>
            </div>
            <div class="document">
                <div class="doc-icon">📊</div>
                <strong>ARCHITECTURE.md</strong>
                <div style="color: #888; font-size: 0.8em;">15 KB</div>
            </div>
            <div class="document">
                <div class="doc-icon">📝</div>
                <strong>README.md</strong>
                <div style="color: #888; font-size: 0.8em;">8 KB</div>
            </div>
            <div class="document">
                <div class="doc-icon">⚙️</div>
                <strong>codex_ledger.json</strong>
                <div style="color: #888; font-size: 0.8em;">45 KB</div>
            </div>
        </div>
    </div>
</body>
</html>
"""

AVATARS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>👤 Avatars - Codex Dominion</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; }
        .back { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }
        h1 { color: #667eea; }
        .avatar-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .avatar-card {
            padding: 25px;
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            border-radius: 15px;
            text-align: center;
        }
        .avatar-icon {
            width: 100px;
            height: 100px;
            margin: 0 auto 15px;
            background: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3em;
        }
        .avatar-card h3 { color: #333; margin-bottom: 10px; }
        .avatar-status {
            display: inline-block;
            padding: 5px 15px;
            background: #51cf66;
            color: white;
            border-radius: 20px;
            font-size: 0.9em;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        <h1>👤 Avatar System</h1>
        <p>AI-powered digital representatives for different roles</p>

        <div class="avatar-grid">
            <div class="avatar-card">
                <div class="avatar-icon">👤</div>
                <h3>Jermaine Avatar</h3>
                <div class="avatar-status">🟢 ACTIVE</div>
                <p>Your primary digital representative</p>
            </div>

            <div class="avatar-card">
                <div class="avatar-icon">💼</div>
                <h3>Business Avatar</h3>
                <div class="avatar-status">🟢 ACTIVE</div>
                <p>Professional interactions & negotiations</p>
            </div>

            <div class="avatar-card">
                <div class="avatar-icon">🎓</div>
                <h3>Educator Avatar</h3>
                <div class="avatar-status">🟢 ACTIVE</div>
                <p>Teaching & knowledge sharing</p>
            </div>

            <div class="avatar-card">
                <div class="avatar-icon">🔧</div>
                <h3>Technical Avatar</h3>
                <div class="avatar-status">🟢 ACTIVE</div>
                <p>Development & system operations</p>
            </div>

            <div class="avatar-card">
                <div class="avatar-icon">👑</div>
                <h3>Council Avatar</h3>
                <div class="avatar-status">🟢 ACTIVE</div>
                <p>Governance & strategic decisions</p>
            </div>

            <div class="avatar-card">
                <div class="avatar-icon">🎨</div>
                <h3>Creative Avatar</h3>
                <div class="avatar-status">🟢 ACTIVE</div>
                <p>Content creation & design</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

COUNCIL_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>⚖️ Council Review - Codex Dominion</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e2e8f0;
            padding: 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
        }

        .header {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            padding: 32px;
            border-radius: 20px;
            margin-bottom: 24px;
            border: 1px solid rgba(148, 163, 184, 0.1);
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        }

        .header h1 {
            font-size: 2.5em;
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
            margin-bottom: 8px;
        }

        .header p {
            color: #cbd5e1;
            font-size: 1.1em;
        }

        .back-btn {
            display: inline-block;
            padding: 10px 20px;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            text-decoration: none;
            border-radius: 10px;
            font-weight: 600;
            margin-bottom: 20px;
            transition: all 0.3s ease;
            border: 1px solid rgba(139, 92, 246, 0.3);
        }

        .back-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5);
        }

        .filters {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            padding: 24px;
            border-radius: 16px;
            margin-bottom: 24px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 16px;
            border: 1px solid rgba(148, 163, 184, 0.1);
            box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        }

        .filter-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .filter-group label {
            color: #cbd5e1;
            font-weight: 600;
            font-size: 0.95em;
        }

        .filter-group select,
        .filter-group input {
            padding: 12px 16px;
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 10px;
            color: #e2e8f0;
            font-size: 1em;
            transition: all 0.2s ease;
        }

        .filter-group select:focus,
        .filter-group input:focus {
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        .table-container {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid rgba(148, 163, 184, 0.1);
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        thead {
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        }

        thead th {
            padding: 16px;
            text-align: left;
            font-weight: 700;
            color: white;
            font-size: 0.95em;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        tbody tr {
            border-bottom: 1px solid rgba(148, 163, 184, 0.1);
            transition: all 0.2s ease;
        }

        tbody tr:hover {
            background: rgba(59, 130, 246, 0.1);
        }

        tbody td {
            padding: 16px;
            color: #cbd5e1;
            font-size: 0.95em;
        }

        .workflow-id {
            font-family: 'Courier New', monospace;
            color: #60a5fa;
            font-weight: 600;
        }

        .status-badge {
            display: inline-block;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .status-pending {
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            color: #1e293b;
        }

        .status-approved {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
        }

        .status-denied {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
        }

        .savings {
            color: #10b981;
            font-weight: 700;
            font-size: 1.05em;
        }

        .action-btn {
            padding: 8px 16px;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 0.9em;
        }

        .action-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
        }

        .action-btn.approve {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        }

        .action-btn.deny {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }

        .stat-card {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            padding: 20px;
            border-radius: 16px;
            border: 1px solid rgba(148, 163, 184, 0.1);
            box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        }

        .stat-card h3 {
            font-size: 2em;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
            margin-bottom: 4px;
        }

        .stat-card p {
            color: #94a3b8;
            font-size: 0.9em;
        }

        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #64748b;
        }

        .empty-state .icon {
            font-size: 4em;
            margin-bottom: 16px;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back-btn">← Back to Dashboard</a>

        <div class="header">
            <h1>⚖️ Council Review</h1>
            <p>Review and approve workflow automations requiring council oversight</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <h3 id="total-reviews">0</h3>
                <p>Total Reviews</p>
            </div>
            <div class="stat-card">
                <h3 id="pending-reviews">0</h3>
                <p>Pending</p>
            </div>
            <div class="stat-card">
                <h3 id="approved-reviews">0</h3>
                <p>Approved</p>
            </div>
            <div class="stat-card">
                <h3 id="total-savings">$0</h3>
                <p>Total Savings</p>
            </div>
        </div>

        <div class="filters">
            <div class="filter-group">
                <label for="council-filter">Council</label>
                <select id="council-filter">
                    <option value="all">All Councils</option>
                    <option value="council_governance">Governance</option>
                    <option value="council_treasury">Treasury</option>
                    <option value="council_security">Security</option>
                    <option value="council_operations">Operations</option>
                    <option value="council_marketing">Marketing</option>
                </select>
            </div>

            <div class="filter-group">
                <label for="status-filter">Status</label>
                <select id="status-filter">
                    <option value="all">All Status</option>
                    <option value="pending">Pending</option>
                    <option value="approved">Approved</option>
                    <option value="denied">Denied</option>
                </select>
            </div>

            <div class="filter-group">
                <label for="search-input">Search</label>
                <input type="text" id="search-input" placeholder="Search workflows...">
            </div>
        </div>

        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Workflow ID</th>
                        <th>Type</th>
                        <th>Agent</th>
                        <th>Council</th>
                        <th>Savings</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="reviews-tbody">
                    <tr>
                        <td colspan="7">
                            <div class="empty-state">
                                <div class="icon">⚖️</div>
                                <h3>Loading reviews...</h3>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <script>
        // Sample data - in production, fetch from /api/workflows/pending-review
        const sampleReviews = [
            {
                id: "abc123",
                workflow_name: "Customer Follow-up Automation",
                workflow_type: "follow-up",
                agent_name: "Jermaine Super Action",
                agent_id: "agent_jermaine_super_action",
                council_name: "Governance Council",
                council_id: "council_governance",
                estimated_weekly_savings: 27600,
                status: "pending",
                created_at: "2025-12-19T20:00:00Z"
            },
            {
                id: "def456",
                workflow_name: "Invoice Processing",
                workflow_type: "invoices",
                agent_name: "Customer Success AI",
                agent_id: "agent_customer_success",
                council_name: "Treasury Council",
                council_id: "council_treasury",
                estimated_weekly_savings: 8900,
                status: "pending",
                created_at: "2025-12-19T19:30:00Z"
            },
            {
                id: "ghi789",
                workflow_name: "Lead Qualification",
                workflow_type: "leads",
                agent_name: "Sales Agent",
                agent_id: "agent_sales",
                council_name: "Operations Council",
                council_id: "council_operations",
                estimated_weekly_savings: 15200,
                status: "approved",
                created_at: "2025-12-19T18:00:00Z"
            }
        ];

        let reviews = [...sampleReviews];

        function renderReviews() {
            const tbody = document.getElementById('reviews-tbody');
            const councilFilter = document.getElementById('council-filter').value;
            const statusFilter = document.getElementById('status-filter').value;
            const searchQuery = document.getElementById('search-input').value.toLowerCase();

            let filtered = reviews.filter(r => {
                const matchesCouncil = councilFilter === 'all' || r.council_id === councilFilter;
                const matchesStatus = statusFilter === 'all' || r.status === statusFilter;
                const matchesSearch = !searchQuery || 
                    r.id.toLowerCase().includes(searchQuery) ||
                    r.workflow_name.toLowerCase().includes(searchQuery) ||
                    r.agent_name.toLowerCase().includes(searchQuery);
                return matchesCouncil && matchesStatus && matchesSearch;
            });

            if (filtered.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="7">
                            <div class="empty-state">
                                <div class="icon">🔍</div>
                                <h3>No reviews found</h3>
                                <p>Try adjusting your filters</p>
                            </div>
                        </td>
                    </tr>
                `;
                return;
            }

            tbody.innerHTML = filtered.map(review => {
                const statusClass = review.status === 'pending' ? 'status-pending' :
                                  review.status === 'approved' ? 'status-approved' : 'status-denied';
                
                const actions = review.status === 'pending' ? `
                    <button class="action-btn approve" onclick="approveReview('${review.id}')">✓ Approve</button>
                    <button class="action-btn deny" onclick="denyReview('${review.id}')">✗ Deny</button>
                ` : `<span style="color: #64748b;">—</span>`;

                return `
                    <tr>
                        <td><span class="workflow-id">${review.id}</span></td>
                        <td>${review.workflow_type}</td>
                        <td>${review.agent_name}</td>
                        <td>${review.council_name.replace(' Council', '')}</td>
                        <td><span class="savings">$${review.estimated_weekly_savings.toLocaleString()}/wk</span></td>
                        <td><span class="status-badge ${statusClass}">${review.status}</span></td>
                        <td>${actions}</td>
                    </tr>
                `;
            }).join('');

            updateStats();
        }

        function updateStats() {
            const totalReviews = reviews.length;
            const pendingReviews = reviews.filter(r => r.status === 'pending').length;
            const approvedReviews = reviews.filter(r => r.status === 'approved').length;
            const totalSavings = reviews.reduce((sum, r) => sum + r.estimated_weekly_savings, 0);

            document.getElementById('total-reviews').textContent = totalReviews;
            document.getElementById('pending-reviews').textContent = pendingReviews;
            document.getElementById('approved-reviews').textContent = approvedReviews;
            document.getElementById('total-savings').textContent = `$${totalSavings.toLocaleString()}`;
        }

        function approveReview(id) {
            const review = reviews.find(r => r.id === id);
            if (review) {
                review.status = 'approved';
                renderReviews();
                alert(`✅ Workflow ${id} approved!`);
                // In production: POST /api/workflows/${id}/vote with vote='approve'
            }
        }

        function denyReview(id) {
            const review = reviews.find(r => r.id === id);
            if (review) {
                review.status = 'denied';
                renderReviews();
                alert(`❌ Workflow ${id} denied`);
                // In production: POST /api/workflows/${id}/vote with vote='deny'
            }
        }

        // Event listeners
        document.getElementById('council-filter').addEventListener('change', renderReviews);
        document.getElementById('status-filter').addEventListener('change', renderReviews);
        document.getElementById('search-input').addEventListener('input', renderReviews);

        // Initial render
        renderReviews();

        // In production, fetch real data:
        // fetch('/api/workflows/pending-review')
        //     .then(r => r.json())
        //     .then(data => {
        //         reviews = data.reviews;
        //         renderReviews();
        //     });
    </script>
</body>
</html>
"""

COPILOT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🚁 Copilot - Codex Dominion</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; }
        .back { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }
        h1 { color: #667eea; }
        .copilot-section {
            margin: 20px 0;
            padding: 20px;
            background: #f5f7fa;
            border-radius: 10px;
            border-left: 5px solid #667eea;
        }
        .copilot-section h2 { color: #764ba2; }
        .code-block {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 20px;
            border-radius: 10px;
            font-family: 'Consolas', 'Monaco', monospace;
            overflow-x: auto;
            margin: 15px 0;
        }
        .instruction-item {
            padding: 15px;
            margin: 10px 0;
            background: white;
            border-radius: 8px;
            border-left: 3px solid #51cf66;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        <h1>🚁 VS Code Copilot Integration</h1>
        <p>AI-powered coding assistant with Codex Dominion context</p>

        <div class="copilot-section">
            <h2>📄 Copilot Instructions</h2>
            <p>These instructions are loaded from <code>.github/copilot-instructions.md</code></p>

            <div class="instruction-item">
                <strong>✅ Project Context:</strong> Codex Dominion - Hybrid polyglot monorepo with ceremonial naming
            </div>

            <div class="instruction-item">
                <strong>✅ Architecture:</strong> Council Seal Structure - Sovereigns, Custodians, Industry Agents
            </div>

            <div class="instruction-item">
                <strong>✅ Tech Stack:</strong> Next.js 14+, FastAPI, Streamlit, Flask, Docker, Kubernetes
            </div>

            <div class="instruction-item">
                <strong>✅ Key Files:</strong> codex_ledger.json, proclamations.json, cycles.json
            </div>
        </div>

        <div class="copilot-section">
            <h2>⚡ Active Copilot Features</h2>
            <ul style="line-height: 2;">
                <li>🤖 <strong>Code Completion:</strong> Context-aware suggestions</li>
                <li>💬 <strong>Chat Interface:</strong> Ask questions about your code</li>
                <li>🔍 <strong>Code Explanation:</strong> Understand complex code</li>
                <li>🛠️ <strong>Refactoring:</strong> Improve code structure</li>
                <li>📝 <strong>Documentation:</strong> Auto-generate docs</li>
                <li>🧪 <strong>Test Generation:</strong> Create unit tests</li>
            </ul>
        </div>

        <div class="copilot-section">
            <h2>💡 Quick Tips</h2>
            <div class="code-block">
// Use Copilot inline suggestions (Tab to accept)
// Press Ctrl+I for Copilot chat
// Type // comments to guide Copilot
// Use @workspace to search your project
// Use @terminal for command suggestions
            </div>
        </div>

        <div class="copilot-section">
            <h2>🔗 Integration Status</h2>
            <p>✅ Copilot instructions loaded from copilot-instructions.md</p>
            <p>✅ Project context available to Copilot</p>
            <p>✅ Claude Sonnet 4.5 model active</p>
            <p>✅ All 48 Intelligence Engines accessible</p>
        </div>
    </div>
</body>
</html>
"""

# ============================================================================
# CREATIVE STUDIO HTML TEMPLATE
# ============================================================================
STUDIO_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🎨 Creative Studio - CodexDominion</title>
    <meta charset="utf-8">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0d0d0d;
            color: #fff;
            padding: 40px 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .container > p {
            color: #aaa;
            font-size: 1.1rem;
            margin-bottom: 50px;
        }
        .tool-grid {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 40px;
            flex-wrap: wrap;
        }
        .tool-card {
            background: #111;
            border: 1px solid #222;
            padding: 25px;
            width: 280px;
            border-radius: 12px;
            text-decoration: none;
            color: white;
            transition: 0.3s ease;
        }
        .tool-card:hover {
            transform: translateY(-5px);
            border-color: #444;
        }
        .tool-card h2 {
            font-size: 1.8rem;
            margin-bottom: 15px;
            color: #fff;
        }
        .tool-card p {
            color: #aaa;
            line-height: 1.6;
            font-size: 1rem;
        }
        .back-button {
            display: inline-block;
            padding: 12px 28px;
            background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: transform 0.2s;
        }
        .back-button:hover {
            transform: scale(1.05);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 CodexDominion Creative Studio</h1>
        <p>Your AI-powered creative engine for graphics, audio, and video.</p>

        <div class="tool-grid">

            <a href="/studio/graphics" class="tool-card">
                <h2>🖼️ Graphics Studio</h2>
                <p>Create brand assets, posters, thumbnails, banners, and visual storytelling.</p>
            </a>

            <a href="/studio/audio" class="tool-card">
                <h2>🎵 Audio Studio</h2>
                <p>Generate voiceovers, soundscapes, narrations, and branded audio.</p>
            </a>

            <a href="/studio/video" class="tool-card">
                <h2>🎬 Video Studio</h2>
                <p>Storyboard, script, and assemble AI-assisted video content.</p>
            </a>

        </div>

        <a href="/" class="back-button">← Back to Home</a>
    </div>
</body>
</html>
"""

# ============================================================================
# AI ADVISOR HTML TEMPLATE
# ============================================================================
AI_ADVISOR_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 AI Advisor - Codex Dominion</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            position: relative;
        }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .header p { font-size: 1.1rem; opacity: 0.9; }
        .back-btn {
            display: inline-block;
            padding: 10px 20px;
            background: rgba(255,255,255,0.2);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            margin-bottom: 20px;
            transition: 0.3s;
        }
        .back-btn:hover { background: rgba(255,255,255,0.3); }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
        }
        .stat-card h3 { font-size: 2.5rem; color: #667eea; margin-bottom: 10px; }
        .stat-card p { color: #666; font-size: 0.95rem; }
        
        .content {
            padding: 30px;
        }
        .section-title {
            font-size: 1.8rem;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }
        
        .filter-bar {
            display: flex;
            gap: 15px;
            margin-bottom: 25px;
            flex-wrap: wrap;
        }
        .filter-btn {
            padding: 10px 20px;
            border: 2px solid #e0e0e0;
            background: white;
            border-radius: 25px;
            cursor: pointer;
            transition: 0.3s;
            font-size: 0.95rem;
        }
        .filter-btn:hover { border-color: #667eea; background: #f0f0ff; }
        .filter-btn.active { background: #667eea; color: white; border-color: #667eea; }
        
        .recommendations-grid {
            display: grid;
            gap: 20px;
        }
        .recommendation-card {
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 25px;
            transition: 0.3s;
            cursor: pointer;
        }
        .recommendation-card:hover {
            border-color: #667eea;
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.15);
            transform: translateY(-2px);
        }
        
        .rec-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }
        .rec-title {
            font-size: 1.3rem;
            color: #333;
            margin-bottom: 8px;
        }
        .rec-category {
            display: inline-block;
            padding: 5px 12px;
            background: #e3f2fd;
            color: #1976d2;
            border-radius: 15px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .rec-category.performance { background: #f3e5f5; color: #7b1fa2; }
        .rec-category.cost { background: #e8f5e9; color: #388e3c; }
        .rec-category.security { background: #fff3e0; color: #f57c00; }
        
        .rec-impact {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-left: 10px;
        }
        .impact-high { background: #ffebee; color: #c62828; }
        .impact-medium { background: #fff3e0; color: #f57c00; }
        .impact-low { background: #e8f5e9; color: #388e3c; }
        
        .rec-description {
            color: #666;
            line-height: 1.6;
            margin-bottom: 15px;
        }
        
        .rec-actions {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.95rem;
            transition: 0.3s;
            text-decoration: none;
            display: inline-block;
        }
        .btn-primary {
            background: #667eea;
            color: white;
        }
        .btn-primary:hover { background: #5568d3; }
        .btn-secondary {
            background: #e0e0e0;
            color: #333;
        }
        .btn-secondary:hover { background: #d0d0d0; }
        
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #999;
        }
        .empty-state svg {
            width: 100px;
            height: 100px;
            margin-bottom: 20px;
            opacity: 0.3;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #667eea;
        }
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <a href="/" class="back-btn">← Back to Dashboard</a>
            <h1>🤖 AI Advisor</h1>
            <p>Intelligent recommendations to optimize your Codex Dominion system</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3 id="total-recommendations">0</h3>
                <p>Total Recommendations</p>
            </div>
            <div class="stat-card">
                <h3 id="pending-count">0</h3>
                <p>Pending Review</p>
            </div>
            <div class="stat-card">
                <h3 id="accepted-count">0</h3>
                <p>Accepted</p>
            </div>
            <div class="stat-card">
                <h3 id="potential-savings">$0</h3>
                <p>Potential Savings</p>
            </div>
        </div>
        
        <div class="content">
            <h2 class="section-title">💡 Recommendations</h2>
            
            <div class="filter-bar">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="pending">Pending</button>
                <button class="filter-btn" data-filter="workflow">Workflow</button>
                <button class="filter-btn" data-filter="performance">Performance</button>
                <button class="filter-btn" data-filter="cost">Cost Optimization</button>
                <button class="filter-btn" data-filter="security">Security</button>
            </div>
            
            <div id="loading" class="loading">
                <div class="spinner"></div>
                <p>Loading recommendations...</p>
            </div>
            
            <div id="recommendations-container" class="recommendations-grid" style="display: none;">
                <!-- Recommendations will be loaded here -->
            </div>
            
            <div id="empty-state" class="empty-state" style="display: none;">
                <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5z"/>
                </svg>
                <h3>No recommendations available</h3>
                <p>Your system is running optimally! Check back later for new insights.</p>
            </div>
        </div>
    </div>
    
    <script>
        const TENANT_ID = 'tenant_codexdominion';
        let allRecommendations = [];
        let currentFilter = 'all';
        
        // Load recommendations on page load
        document.addEventListener('DOMContentLoaded', () => {
            loadRecommendations();
            setupFilterButtons();
        });
        
        async function loadRecommendations() {
            try {
                const response = await fetch(`/api/advisor/recommendations?tenant_id=${TENANT_ID}&status=pending`);
                
                if (!response.ok) {
                    throw new Error('Failed to load recommendations');
                }
                
                const data = await response.json();
                allRecommendations = data.recommendations || [];
                
                // Update stats
                updateStats(data.summary || {});
                
                // Display recommendations
                displayRecommendations(allRecommendations);
                
                // Hide loading, show content
                document.getElementById('loading').style.display = 'none';
                
                if (allRecommendations.length === 0) {
                    document.getElementById('empty-state').style.display = 'block';
                } else {
                    document.getElementById('recommendations-container').style.display = 'grid';
                }
                
            } catch (error) {
                console.error('Error loading recommendations:', error);
                document.getElementById('loading').innerHTML = `
                    <p style="color: #c62828;">❌ Failed to load recommendations</p>
                    <p style="font-size: 0.9rem;">${error.message}</p>
                `;
            }
        }
        
        function updateStats(summary) {
            document.getElementById('total-recommendations').textContent = summary.total_count || 0;
            document.getElementById('pending-count').textContent = summary.pending_count || 0;
            document.getElementById('accepted-count').textContent = summary.accepted_count || 0;
            
            const savings = summary.potential_monthly_savings || 0;
            document.getElementById('potential-savings').textContent = 
                `$${savings.toFixed(0)}`;
        }
        
        function displayRecommendations(recommendations) {
            const container = document.getElementById('recommendations-container');
            
            if (recommendations.length === 0) {
                container.style.display = 'none';
                document.getElementById('empty-state').style.display = 'block';
                return;
            }
            
            container.innerHTML = recommendations.map(rec => `
                <div class="recommendation-card" data-category="${rec.category || 'workflow'}" data-status="${rec.status || 'pending'}">
                    <div class="rec-header">
                        <div>
                            <div class="rec-title">${rec.title || 'Optimization Opportunity'}</div>
                            <span class="rec-category ${rec.category || 'workflow'}">${formatCategory(rec.category)}</span>
                            <span class="rec-impact impact-${rec.impact || 'medium'}">${formatImpact(rec.impact)}</span>
                        </div>
                    </div>
                    <div class="rec-description">${rec.rationale || 'No description available'}</div>
                    ${rec.estimated_monthly_savings ? `
                        <div style="color: #388e3c; font-weight: 600; margin-top: 10px;">
                            💰 Potential savings: $${rec.estimated_monthly_savings}/month
                        </div>
                    ` : ''}
                    <div class="rec-actions">
                        <button class="btn btn-primary" onclick="acceptRecommendation('${rec.id}')">
                            ✓ Accept & Implement
                        </button>
                        <button class="btn btn-secondary" onclick="dismissRecommendation('${rec.id}')">
                            Dismiss
                        </button>
                    </div>
                </div>
            `).join('');
        }
        
        function formatCategory(category) {
            const categories = {
                'workflow': 'Workflow',
                'performance': 'Performance',
                'cost': 'Cost Optimization',
                'security': 'Security'
            };
            return categories[category] || category;
        }
        
        function formatImpact(impact) {
            const impacts = {
                'high': 'High Impact',
                'medium': 'Medium Impact',
                'low': 'Low Impact'
            };
            return impacts[impact] || impact;
        }
        
        function setupFilterButtons() {
            const buttons = document.querySelectorAll('.filter-btn');
            buttons.forEach(btn => {
                btn.addEventListener('click', () => {
                    // Update active state
                    buttons.forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    
                    // Filter recommendations
                    currentFilter = btn.dataset.filter;
                    filterRecommendations();
                });
            });
        }
        
        function filterRecommendations() {
            const cards = document.querySelectorAll('.recommendation-card');
            
            cards.forEach(card => {
                if (currentFilter === 'all') {
                    card.style.display = 'block';
                } else if (currentFilter === 'pending') {
                    card.style.display = card.dataset.status === 'pending' ? 'block' : 'none';
                } else {
                    card.style.display = card.dataset.category === currentFilter ? 'block' : 'none';
                }
            });
        }
        
        async function acceptRecommendation(recId) {
            if (!confirm('Accept this recommendation and create implementation workflow?')) {
                return;
            }
            
            try {
                const response = await fetch(`/api/advisor/recommendations/${recId}/accept`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ tenant_id: TENANT_ID })
                });
                
                if (!response.ok) {
                    throw new Error('Failed to accept recommendation');
                }
                
                const data = await response.json();
                alert(`✅ Recommendation accepted! Workflow created: ${data.workflow_id || 'pending'}`);
                
                // Reload recommendations
                loadRecommendations();
                
            } catch (error) {
                console.error('Error accepting recommendation:', error);
                alert(`❌ Error: ${error.message}`);
            }
        }
        
        async function dismissRecommendation(recId) {
            if (!confirm('Dismiss this recommendation?')) {
                return;
            }
            
            try {
                const response = await fetch(`/api/advisor/recommendations/${recId}/dismiss`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ tenant_id: TENANT_ID })
                });
                
                if (!response.ok) {
                    throw new Error('Failed to dismiss recommendation');
                }
                
                alert('✅ Recommendation dismissed');
                
                // Reload recommendations
                loadRecommendations();
                
            } catch (error) {
                console.error('Error dismissing recommendation:', error);
                alert(`❌ Error: ${error.message}`);
            }
        }
    </script>
</body>
</html>
"""

# ============================================================================
# GRAPHICS STUDIO HTML TEMPLATE
# ============================================================================
GRAPHICS_STUDIO_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Graphics Studio - Codex Dominion</title>
    <style>
        body {
            background: #0d0d0d;
            color: #f5f5f5;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 40px;
        }
        .container { max-width: 1000px; margin: 0 auto; }
        h1 { font-size: 2.5rem; margin-bottom: 20px; text-align: center; }
        .subtitle { text-align: center; color: #ccc; margin-bottom: 40px; }
        .coming-soon { 
            background: #111; border: 1px solid #333; padding: 40px;
            border-radius: 12px; text-align: center; margin: 40px 0;
        }
        .features { 
            display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px; margin: 30px 0;
        }
        .feature-item { 
            background: #111; border: 1px solid #222; padding: 20px;
            border-radius: 8px; transition: 0.3s;
        }
        .feature-item:hover { border-color: #4f46e5; }
        .back-button {
            display: inline-block; padding: 12px 20px; background: #333;
            color: white; text-decoration: none; border-radius: 6px;
            transition: 0.3s; margin-top: 30px;
        }
        .back-button:hover { background: #444; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Graphics Studio</h1>
        <p class="subtitle">AI-Powered Image Generation & Design Tools</p>
        
        <div class="coming-soon">
            <h2>🚀 Launching Soon</h2>
            <p>Transform your ideas into stunning visuals with AI-powered design tools.</p>
        </div>

        <div class="features">
            <div class="feature-item">
                <h3>📸 AI Image Generation</h3>
                <p>Create original images from text descriptions using DALL-E, Midjourney, and Stable Diffusion.</p>
            </div>
            <div class="feature-item">
                <h3>🎨 Logo Designer</h3>
                <p>Generate professional logos and brand identity packages in minutes.</p>
            </div>
            <div class="feature-item">
                <h3>📱 Social Media Graphics</h3>
                <p>Templates for Instagram, TikTok, Pinterest, Facebook, and LinkedIn.</p>
            </div>
            <div class="feature-item">
                <h3>🛍️ Product Mockups</h3>
                <p>E-commerce ready product images and marketing materials.</p>
            </div>
            <div class="feature-item">
                <h3>🌍 Cultural Artwork</h3>
                <p>Create authentic cultural and mythic artwork for your brand.</p>
            </div>
            <div class="feature-item">
                <h3>✨ Brand Assets</h3>
                <p>Complete brand kits with colors, fonts, and design guidelines.</p>
            </div>
        </div>

        <div style="text-align: center;">
            <a href="/studio" class="back-button">← Back to Studio</a>
        </div>
    </div>
</body>
</html>
"""

# ============================================================================
# AUDIO STUDIO HTML TEMPLATE
# ============================================================================
AUDIO_STUDIO_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Audio Studio - Codex Dominion</title>
    <style>
        body {
            background: #0d0d0d;
            color: #f5f5f5;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 40px;
        }
        .container { max-width: 1000px; margin: 0 auto; }
        h1 { font-size: 2.5rem; margin-bottom: 20px; text-align: center; }
        .subtitle { text-align: center; color: #ccc; margin-bottom: 40px; }
        .coming-soon { 
            background: #111; border: 1px solid #333; padding: 40px;
            border-radius: 12px; text-align: center; margin: 40px 0;
        }
        .features { 
            display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px; margin: 30px 0;
        }
        .feature-item { 
            background: #111; border: 1px solid #222; padding: 20px;
            border-radius: 8px; transition: 0.3s;
        }
        .feature-item:hover { border-color: #6366f1; }
        .back-button {
            display: inline-block; padding: 12px 20px; background: #333;
            color: white; text-decoration: none; border-radius: 6px;
            transition: 0.3s; margin-top: 30px;
        }
        .back-button:hover { background: #444; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎵 Audio Studio</h1>
        <p class="subtitle">AI Voice Synthesis & Music Generation</p>
        
        <div class="coming-soon">
            <h2>🎙️ Launching Soon</h2>
            <p>Create professional audio content with AI-powered voice and music tools.</p>
        </div>

        <div class="features">
            <div class="feature-item">
                <h3>🗣️ AI Voice Generation</h3>
                <p>Generate natural-sounding voiceovers in multiple languages and voices.</p>
            </div>
            <div class="feature-item">
                <h3>🎙️ Voice Cloning</h3>
                <p>Clone your voice or create custom AI voice characters for content.</p>
            </div>
            <div class="feature-item">
                <h3>🎧 Podcast Production</h3>
                <p>Edit, mix, and master podcast episodes with AI assistance.</p>
            </div>
            <div class="feature-item">
                <h3>🎼 Music Generation</h3>
                <p>Create original background music and sound effects for your content.</p>
            </div>
            <div class="feature-item">
                <h3>📻 Audio Editing</h3>
                <p>Remove noise, enhance quality, and polish audio automatically.</p>
            </div>
            <div class="feature-item">
                <h3>🔊 Sound Effects</h3>
                <p>Generate custom sound effects for videos, games, and multimedia.</p>
            </div>
        </div>

        <div style="text-align: center;">
            <a href="/studio" class="back-button">← Back to Studio</a>
        </div>
    </div>
</body>
</html>
"""

# ============================================================================
# VIDEO STUDIO HTML TEMPLATE
# ============================================================================
VIDEO_STUDIO_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Video Studio - Codex Dominion</title>
    <style>
        body {
            background: #0d0d0d;
            color: #f5f5f5;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 40px;
        }
        .container { max-width: 1000px; margin: 0 auto; }
        h1 { font-size: 2.5rem; margin-bottom: 20px; text-align: center; }
        .subtitle { text-align: center; color: #ccc; margin-bottom: 40px; }
        .coming-soon { 
            background: #111; border: 1px solid #333; padding: 40px;
            border-radius: 12px; text-align: center; margin: 40px 0;
        }
        .features { 
            display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px; margin: 30px 0;
        }
        .feature-item { 
            background: #111; border: 1px solid #222; padding: 20px;
            border-radius: 8px; transition: 0.3s;
        }
        .feature-item:hover { border-color: #ef4444; }
        .back-button {
            display: inline-block; padding: 12px 20px; background: #333;
            color: white; text-decoration: none; border-radius: 6px;
            transition: 0.3s; margin-top: 30px;
        }
        .back-button:hover { background: #444; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 Video Studio</h1>
        <p class="subtitle">AI Video Creation & Automated Editing</p>
        
        <div class="coming-soon">
            <h2>📹 Launching Soon</h2>
            <p>Produce engaging video content with AI-powered editing and generation.</p>
        </div>

        <div class="features">
            <div class="feature-item">
                <h3>🎥 AI Video Editing</h3>
                <p>Automatically edit videos with smart cuts, transitions, and effects.</p>
            </div>
            <div class="feature-item">
                <h3>📝 Text-to-Video</h3>
                <p>Generate videos from text scripts with AI-generated visuals.</p>
            </div>
            <div class="feature-item">
                <h3>📱 Short-Form Content</h3>
                <p>Create Reels, Shorts, and TikToks optimized for maximum engagement.</p>
            </div>
            <div class="feature-item">
                <h3>🎭 Motion Graphics</h3>
                <p>Add professional animated graphics and text overlays.</p>
            </div>
            <div class="feature-item">
                <h3>🎬 Auto Subtitles</h3>
                <p>Generate accurate subtitles and captions in multiple languages.</p>
            </div>
            <div class="feature-item">
                <h3>🔄 Content Repurposing</h3>
                <p>Automatically adapt long-form content into short clips.</p>
            </div>
        </div>

        <div style="text-align: center;">
            <a href="/studio" class="back-button">← Back to Studio</a>
        </div>
    </div>
</body>
</html>
"""

# ============================================================================
# AUTOMATION CALCULATOR HTML TEMPLATE
# ============================================================================
AUTOMATION_CALCULATOR_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🤖 Automation Savings Calculator - Codex Dominion</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            margin: 0;
        }
        .container { max-width: 900px; margin: 0 auto; }
        .back { 
            display: inline-block; padding: 10px 20px; background: rgba(255,255,255,0.2); 
            color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; 
            transition: all 0.3s;
        }
        .back:hover { background: rgba(255,255,255,0.3); }
        .calculator-card {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 { 
            color: #667eea; 
            text-align: center; 
            margin-bottom: 10px;
            font-size: 2.2em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        .form-group {
            margin-bottom: 25px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
            font-size: 1.05em;
        }
        input[type="number"], input[type="text"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1.1em;
            transition: all 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        .input-hint {
            font-size: 0.85em;
            color: #888;
            margin-top: 5px;
        }
        .results-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 30px;
            margin: 30px 0;
            color: white;
            display: none;
        }
        .results-box.show {
            display: block;
            animation: slideIn 0.5s ease-out;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .result-item {
            display: flex;
            justify-content: space-between;
            padding: 15px;
            margin: 10px 0;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            font-size: 1.1em;
        }
        .result-label { font-weight: 600; }
        .result-value { 
            font-size: 1.3em; 
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .btn {
            width: 100%;
            padding: 18px;
            border: none;
            border-radius: 10px;
            font-size: 1.2em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            margin: 10px 0;
        }
        .btn-calculate {
            background: #667eea;
            color: white;
        }
        .btn-calculate:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }
        .btn-activate {
            background: #51cf66;
            color: white;
            display: none;
        }
        .btn-activate.show {
            display: block;
            animation: pulse 2s infinite;
        }
        .btn-activate:hover {
            background: #40c057;
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(81, 207, 102, 0.4);
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }
        .success-message {
            background: #51cf66;
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
            font-size: 1.1em;
            display: none;
        }
        .success-message.show {
            display: block;
            animation: slideIn 0.5s ease-out;
        }
        .flame-seal {
            text-align: center;
            font-size: 1.5em;
            margin-top: 20px;
            color: #ff6b6b;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        @media (max-width: 768px) {
            .grid-2 { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        
        <div class="calculator-card">
            <h1>🤖 Jermaine Super Action AI</h1>
            <p class="subtitle">The Sovereign Orchestrator of Rapid Execution</p>
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 30px;">
                <p style="font-size: 1.2em; font-weight: 600; margin: 0;">
                    "Give me the target and I'll sequence the path.<br>
                    Your time is too valuable for repetition — let's automate this."
                </p>
            </div>

            <form id="calculatorForm">
                <div class="form-group">
                    <label for="workflowName">Workflow Name</label>
                    <input type="text" id="workflowName" value="Weekly Customer Follow-Up" required>
                    <div class="input-hint">Give your automation a descriptive name</div>
                </div>

                <div class="grid-2">
                    <div class="form-group">
                        <label for="tasksPerWeek">Tasks per Week</label>
                        <input type="number" id="tasksPerWeek" value="200" min="1" required>
                        <div class="input-hint">How many times do you perform this task?</div>
                    </div>

                    <div class="form-group">
                        <label for="timePerTask">Minutes per Task</label>
                        <input type="number" id="timePerTask" value="10" min="1" required>
                        <div class="input-hint">Average time spent on each task</div>
                    </div>
                </div>

                <div class="grid-2">
                    <div class="form-group">
                        <label for="hourlyWage">Hourly Wage ($)</label>
                        <input type="number" id="hourlyWage" value="25" min="1" step="0.01" required>
                        <div class="input-hint">Labor cost per hour</div>
                    </div>

                    <div class="form-group">
                        <label for="automationPercent">Automation % (0-100)</label>
                        <input type="number" id="automationPercent" value="70" min="0" max="100" required>
                        <div class="input-hint">What % can be automated?</div>
                    </div>
                </div>

                <div class="grid-2">
                    <div class="form-group">
                        <label for="errorRate">Error Rate % (0-100)</label>
                        <input type="number" id="errorRate" value="10" min="0" max="100" required>
                        <div class="input-hint">How often do errors occur?</div>
                    </div>

                    <div class="form-group">
                        <label for="errorCost">Cost per Error ($)</label>
                        <input type="number" id="errorCost" value="15" min="0" step="0.01" required>
                        <div class="input-hint">Average cost to fix an error</div>
                    </div>
                </div>

                <button type="submit" class="btn btn-calculate">⚡ Calculate Sovereignty Value</button>
            </form>

            <div id="resultsBox" class="results-box">
                <h2 style="text-align: center; margin-bottom: 20px;">💰 Your Automation Sovereignty Dividend</h2>
                <p style="text-align: center; font-size: 1.1em; margin-bottom: 15px; font-style: italic;">"The numbers tell the story:"</p>
                <div class="result-item">
                    <span class="result-label">✅ Weekly Savings:</span>
                    <span class="result-value" id="weeklySavings">$0</span>
                </div>
                <div class="result-item">
                    <span class="result-label">✅ Monthly Savings:</span>
                    <span class="result-value" id="monthlySavings">$0</span>
                </div>
                <div class="result-item">
                    <span class="result-label">✅ Yearly Savings:</span>
                    <span class="result-value" id="yearlySavings">$0</span>
                </div>
                <div class="result-item">
                    <span class="result-label">✅ Hours Saved:</span>
                    <span class="result-value" id="hoursSaved">0/week</span>
                </div>
            </div>

            <button id="activateBtn" class="btn btn-activate">� Activate & Achieve Sovereignty</button>

            <div id="successMessage" class="success-message">
                <strong>⚡ Sovereignty Achieved - Automation Activated!</strong>
                <p style="margin: 15px 0; font-size: 1.1em;">"The path is sequenced. Execution complete."</p>
                <div style="margin-top: 10px;">Workflow ID: <span id="workflowId"></span></div>
                <div style="margin-top: 10px; font-weight: bold;">Status: <span style="color: #51cf66;">ACTIVE & MONITORING</span></div>
                <div class="flame-seal" id="flameSeal"></div>
            </div>
        </div>
    </div>

    <script>
        let currentSavings = null;

        document.getElementById('calculatorForm').addEventListener('submit', async function(e) {
            e.preventDefault();

            const data = {
                tasks_per_week: parseFloat(document.getElementById('tasksPerWeek').value),
                time_per_task_minutes: parseFloat(document.getElementById('timePerTask').value),
                hourly_wage: parseFloat(document.getElementById('hourlyWage').value),
                automation_percent: parseFloat(document.getElementById('automationPercent').value),
                error_rate: parseFloat(document.getElementById('errorRate').value),
                error_cost: parseFloat(document.getElementById('errorCost').value)
            };

            try {
                const response = await fetch('/api/automation/calculate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                
                if (result.success) {
                    currentSavings = result.savings;
                    
                    document.getElementById('weeklySavings').textContent = '$' + result.savings.weekly.toLocaleString();
                    document.getElementById('monthlySavings').textContent = '$' + result.savings.monthly.toLocaleString();
                    document.getElementById('yearlySavings').textContent = '$' + result.savings.yearly.toLocaleString();
                    document.getElementById('hoursSaved').textContent = result.savings.hours_saved_per_week + '/week';
                    
                    document.getElementById('resultsBox').classList.add('show');
                    document.getElementById('activateBtn').classList.add('show');
                    document.getElementById('successMessage').classList.remove('show');
                }
            } catch (error) {
                alert('Error calculating savings: ' + error.message);
            }
        });

        document.getElementById('activateBtn').addEventListener('click', async function() {
            if (!currentSavings) return;

            const data = {
                workflow_name: document.getElementById('workflowName').value,
                inputs: {
                    tasks_per_week: parseFloat(document.getElementById('tasksPerWeek').value),
                    time_per_task_minutes: parseFloat(document.getElementById('timePerTask').value),
                    hourly_wage: parseFloat(document.getElementById('hourlyWage').value),
                    automation_percent: parseFloat(document.getElementById('automationPercent').value),
                    error_rate: parseFloat(document.getElementById('errorRate').value),
                    error_cost: parseFloat(document.getElementById('errorCost').value)
                },
                savings: currentSavings
            };

            try {
                const response = await fetch('/api/automation/activate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                
                if (result.success) {
                    document.getElementById('workflowId').textContent = result.workflow_id;
                    document.getElementById('flameSeal').textContent = '🔥 The Flame Burns Sovereign and Eternal! 👑';
                    document.getElementById('successMessage').classList.add('show');
                    document.getElementById('activateBtn').style.display = 'none';
                }
            } catch (error) {
                alert('Error activating automation: ' + error.message);
            }
        });
    </script>
</body>
</html>
"""

# ============================================================================
# WEBSITE BUILDER HTML TEMPLATE
# ============================================================================
WEBSITES_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🌐 Website Builder - Codex Dominion</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 { color: white; text-align: center; margin-bottom: 30px; font-size: 2.5em; }
        .nav-tabs {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 10px; margin-bottom: 30px;
        }
        .nav-tab {
            background: rgba(255,255,255,0.2); padding: 12px; text-align: center;
            border-radius: 10px; text-decoration: none; color: white;
            transition: all 0.3s; font-weight: 600;
        }
        .nav-tab:hover { background: rgba(255,255,255,0.3); transform: translateY(-2px); }
        .nav-tab.active { background: rgba(255,255,255,0.4); }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; }
        .card {
            background: white; border-radius: 15px; padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .card h2 { color: #667eea; margin-bottom: 15px; }
        .template-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-top: 15px; }
        .template-card {
            border: 2px solid #e0e0e0; border-radius: 10px; padding: 15px;
            text-align: center; cursor: pointer; transition: all 0.3s;
        }
        .template-card:hover { border-color: #667eea; transform: scale(1.05); }
        .template-icon { font-size: 3em; margin-bottom: 10px; }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 12px 30px; border: none; border-radius: 25px;
            cursor: pointer; font-size: 1em; font-weight: 600; margin-top: 15px;
        }
        .btn:hover { transform: scale(1.05); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
        .website-list { margin-top: 15px; }
        .website-item {
            background: #f5f5f5; padding: 15px; border-radius: 10px; margin-bottom: 10px;
            display: flex; justify-content: space-between; align-items: center;
        }
        .status-badge {
            padding: 5px 15px; border-radius: 20px; font-size: 0.85em; font-weight: 600;
        }
        .status-live { background: #4caf50; color: white; }
        .status-building { background: #ff9800; color: white; }
        .input-group { margin-bottom: 15px; }
        .input-group label { display: block; margin-bottom: 5px; font-weight: 600; color: #333; }
        .input-group input, .input-group select, .input-group textarea {
            width: 100%; padding: 10px; border: 2px solid #e0e0e0; border-radius: 8px;
            font-size: 1em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 Website Builder System</h1>

        <div class="nav-tabs">
            <a href="/" class="nav-tab">🏠 Home</a>
            <a href="/engines" class="nav-tab">🧠 48 Engines</a>
            <a href="/tools" class="nav-tab">🔧 6 Tools</a>
            <a href="/dashboards" class="nav-tab">📊 All Dashboards</a>
            <a href="/chat" class="nav-tab">💬 AI Chat</a>
            <a href="/agents" class="nav-tab">🤖 AI Agents</a>
            <a href="/websites" class="nav-tab active">🌐 Websites</a>
            <a href="/stores" class="nav-tab">🛒 Stores</a>
            <a href="/social" class="nav-tab">📱 Social Media</a>
            <a href="/affiliate" class="nav-tab">💰 Affiliate</a>
            <a href="/chatbot" class="nav-tab">🤖 Action Chatbot</a>
            <a href="/algorithm" class="nav-tab">🧠 Algorithm AI</a>
            <a href="/autopublish" class="nav-tab">🚀 Auto-Publish</a>
        </div>

        <div class="grid">
            <!-- Quick Website Builder -->
            <div class="card">
                <h2>⚡ Quick Website Builder</h2>
                <div class="input-group">
                    <label>Website Name:</label>
                    <input type="text" placeholder="My Awesome Website" id="website-name">
                </div>
                <div class="input-group">
                    <label>Domain:</label>
                    <input type="text" placeholder="mywebsite.com" id="website-domain">
                </div>
                <div class="input-group">
                    <label>Select Template:</label>
                    <select id="website-template">
                        <option value="landing">Landing Page</option>
                        <option value="blog">Blog</option>
                        <option value="portfolio">Portfolio</option>
                        <option value="business">Business</option>
                        <option value="ecommerce">E-commerce</option>
                    </select>
                </div>
                <button class="btn" onclick="buildWebsite()">🚀 Build Website</button>
            </div>

            <!-- Website Templates -->
            <div class="card">
                <h2>🎨 Templates Library</h2>
                <div class="template-grid">
                    <div class="template-card" onclick="selectTemplate('landing')">
                        <div class="template-icon">🚀</div>
                        <strong>Landing Page</strong>
                        <p style="font-size: 0.9em; color: #666; margin-top: 5px;">High-converting single page</p>
                    </div>
                    <div class="template-card" onclick="selectTemplate('blog')">
                        <div class="template-icon">📝</div>
                        <strong>Blog</strong>
                        <p style="font-size: 0.9em; color: #666; margin-top: 5px;">Content-focused design</p>
                    </div>
                    <div class="template-card" onclick="selectTemplate('portfolio')">
                        <div class="template-icon">🎨</div>
                        <strong>Portfolio</strong>
                        <p style="font-size: 0.9em; color: #666; margin-top: 5px;">Showcase your work</p>
                    </div>
                    <div class="template-card" onclick="selectTemplate('business')">
                        <div class="template-icon">💼</div>
                        <strong>Business</strong>
                        <p style="font-size: 0.9em; color: #666; margin-top: 5px;">Professional corporate site</p>
                    </div>
                    <div class="template-card" onclick="selectTemplate('ecommerce')">
                        <div class="template-icon">🛍️</div>
                        <strong>E-commerce</strong>
                        <p style="font-size: 0.9em; color: #666; margin-top: 5px;">Online store ready</p>
                    </div>
                    <div class="template-card" onclick="selectTemplate('saas')">
                        <div class="template-icon">☁️</div>
                        <strong>SaaS</strong>
                        <p style="font-size: 0.9em; color: #666; margin-top: 5px;">Software product site</p>
                    </div>
                </div>
            </div>

            <!-- Active Websites -->
            <div class="card">
                <h2>🌍 Your Websites</h2>
                <div class="website-list">
                    <div class="website-item">
                        <div>
                            <strong>🌐 codexdominion.app</strong>
                            <p style="font-size: 0.9em; color: #666;">Main Website</p>
                        </div>
                        <span class="status-badge status-live">✅ Live</span>
                    </div>
                    <div class="website-item">
                        <div>
                            <strong>🛍️ aistorelab.com</strong>
                            <p style="font-size: 0.9em; color: #666;">E-commerce Store</p>
                        </div>
                        <span class="status-badge status-live">✅ Live</span>
                    </div>
                    <div class="website-item">
                        <div>
                            <strong>📝 codexblog.app</strong>
                            <p style="font-size: 0.9em; color: #666;">Content Hub</p>
                        </div>
                        <span class="status-badge status-building">🔨 Building</span>
                    </div>
                </div>
            </div>

            <!-- Website Features -->
            <div class="card">
                <h2>✨ Features Available</h2>
                <p>✅ <strong>Responsive Design</strong> - Mobile, tablet, desktop</p>
                <p>✅ <strong>SEO Optimized</strong> - Meta tags, sitemaps, schema</p>
                <p>✅ <strong>Fast Loading</strong> - CDN, caching, optimization</p>
                <p>✅ <strong>SSL Security</strong> - HTTPS encryption included</p>
                <p>✅ <strong>Analytics</strong> - Google Analytics, tracking</p>
                <p>✅ <strong>Contact Forms</strong> - Lead capture forms</p>
                <p>✅ <strong>Blog System</strong> - Built-in CMS</p>
                <p>✅ <strong>E-commerce</strong> - WooCommerce integration</p>
            </div>
        </div>
    </div>

    <script>
        function selectTemplate(template) {
            document.getElementById('website-template').value = template;
            alert('✅ Template selected: ' + template.charAt(0).toUpperCase() + template.slice(1));
        }

        function buildWebsite() {
            const name = document.getElementById('website-name').value;
            const domain = document.getElementById('website-domain').value;
            const template = document.getElementById('website-template').value;

            if (!name || !domain) {
                alert('⚠️ Please fill in all fields');
                return;
            }

            alert(`🚀 Building ${name} at ${domain} with ${template} template!\\n\\n⏳ Estimated time: 2-3 minutes\\n✅ SSL certificate will be auto-configured`);
        }
    </script>
</body>
</html>
"""

# ============================================================================
# STORES HTML TEMPLATE
# ============================================================================
STORES_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🛒 Store Builder - Codex Dominion</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 { color: white; text-align: center; margin-bottom: 30px; font-size: 2.5em; }
        .nav-tabs {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 10px; margin-bottom: 30px;
        }
        .nav-tab {
            background: rgba(255,255,255,0.2); padding: 12px; text-align: center;
            border-radius: 10px; text-decoration: none; color: white;
            transition: all 0.3s; font-weight: 600;
        }
        .nav-tab:hover { background: rgba(255,255,255,0.3); transform: translateY(-2px); }
        .nav-tab.active { background: rgba(255,255,255,0.4); }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; }
        .card {
            background: white; border-radius: 15px; padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .card h2 { color: #f5576c; margin-bottom: 15px; }
        .store-card {
            border: 2px solid #e0e0e0; border-radius: 10px; padding: 20px;
            margin-bottom: 15px; transition: all 0.3s;
        }
        .store-card:hover { border-color: #f5576c; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .metric { display: inline-block; margin-right: 20px; }
        .metric strong { color: #f5576c; font-size: 1.5em; }
        .btn {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white; padding: 12px 30px; border: none; border-radius: 25px;
            cursor: pointer; font-size: 1em; font-weight: 600; margin-top: 15px;
        }
        .btn:hover { transform: scale(1.05); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
        .input-group { margin-bottom: 15px; }
        .input-group label { display: block; margin-bottom: 5px; font-weight: 600; color: #333; }
        .input-group input, .input-group select {
            width: 100%; padding: 10px; border: 2px solid #e0e0e0; border-radius: 8px;
            font-size: 1em;
        }
        .product-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-top: 15px; }
        .product-card {
            border: 1px solid #e0e0e0; border-radius: 10px; padding: 15px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛒 E-Commerce Store Builder</h1>

        <div class="nav-tabs">
            <a href="/" class="nav-tab">🏠 Home</a>
            <a href="/engines" class="nav-tab">🧠 48 Engines</a>
            <a href="/tools" class="nav-tab">🔧 6 Tools</a>
            <a href="/dashboards" class="nav-tab">📊 All Dashboards</a>
            <a href="/chat" class="nav-tab">💬 AI Chat</a>
            <a href="/agents" class="nav-tab">🤖 AI Agents</a>
            <a href="/websites" class="nav-tab">🌐 Websites</a>
            <a href="/stores" class="nav-tab active">🛒 Stores</a>
            <a href="/social" class="nav-tab">📱 Social Media</a>
            <a href="/affiliate" class="nav-tab">💰 Affiliate</a>
            <a href="/chatbot" class="nav-tab">🤖 Action Chatbot</a>
            <a href="/algorithm" class="nav-tab">🧠 Algorithm AI</a>
            <a href="/autopublish" class="nav-tab">🚀 Auto-Publish</a>
        </div>

        <div class="grid">
            <!-- Store Builder -->
            <div class="card">
                <h2>🏪 Create New Store</h2>
                <div class="input-group">
                    <label>Store Name:</label>
                    <input type="text" placeholder="My Store" id="store-name">
                </div>
                <div class="input-group">
                    <label>Store Type:</label>
                    <select id="store-type">
                        <option value="woocommerce">WooCommerce</option>
                        <option value="shopify">Shopify</option>
                        <option value="custom">Custom</option>
                    </select>
                </div>
                <div class="input-group">
                    <label>Niche:</label>
                    <select id="store-niche">
                        <option value="digital">Digital Products</option>
                        <option value="fashion">Fashion</option>
                        <option value="electronics">Electronics</option>
                        <option value="food">Food & Beverage</option>
                        <option value="beauty">Beauty & Cosmetics</option>
                        <option value="books">Books & Education</option>
                    </select>
                </div>
                <button class="btn" onclick="createStore()">🚀 Create Store</button>
            </div>

            <!-- Active Stores -->
            <div class="card">
                <h2>🏬 Your Stores</h2>
                <div class="store-card">
                    <h3>🛍️ AIStoreLab</h3>
                    <p><strong>Platform:</strong> WooCommerce</p>
                    <p><strong>Products:</strong> 147 active</p>
                    <div class="metric">
                        <strong>$12,458</strong><br>
                        <span style="font-size: 0.9em;">Monthly Revenue</span>
                    </div>
                    <div class="metric">
                        <strong>342</strong><br>
                        <span style="font-size: 0.9em;">Orders</span>
                    </div>
                    <button class="btn">Manage Store</button>
                </div>
                <div class="store-card">
                    <h3>📚 Digital Products Store</h3>
                    <p><strong>Platform:</strong> Custom</p>
                    <p><strong>Products:</strong> 89 active</p>
                    <div class="metric">
                        <strong>$8,234</strong><br>
                        <span style="font-size: 0.9em;">Monthly Revenue</span>
                    </div>
                    <div class="metric">
                        <strong>215</strong><br>
                        <span style="font-size: 0.9em;">Orders</span>
                    </div>
                    <button class="btn">Manage Store</button>
                </div>
            </div>

            <!-- Product Manager -->
            <div class="card">
                <h2>📦 Quick Product Add</h2>
                <div class="input-group">
                    <label>Product Name:</label>
                    <input type="text" placeholder="Product name" id="product-name">
                </div>
                <div class="input-group">
                    <label>Price:</label>
                    <input type="number" placeholder="29.99" id="product-price">
                </div>
                <div class="input-group">
                    <label>Store:</label>
                    <select id="product-store">
                        <option value="aistorelab">AIStoreLab</option>
                        <option value="digital">Digital Products Store</option>
                    </select>
                </div>
                <button class="btn" onclick="addProduct()">➕ Add Product</button>
            </div>

            <!-- Store Analytics -->
            <div class="card">
                <h2>📊 Store Analytics</h2>
                <div class="metric">
                    <strong>$20,692</strong><br>
                    <span style="font-size: 0.9em;">Total Revenue</span>
                </div>
                <div class="metric">
                    <strong>557</strong><br>
                    <span style="font-size: 0.9em;">Total Orders</span>
                </div>
                <div class="metric">
                    <strong>236</strong><br>
                    <span style="font-size: 0.9em;">Total Products</span>
                </div>
                <div class="metric">
                    <strong>1,234</strong><br>
                    <span style="font-size: 0.9em;">Customers</span>
                </div>
                <p style="margin-top: 20px;">✅ <strong>WooCommerce:</strong> 2 stores connected</p>
                <p>✅ <strong>Shopify:</strong> Ready to connect</p>
                <p>✅ <strong>Payment Gateways:</strong> Stripe, PayPal</p>
                <p>✅ <strong>Shipping:</strong> USPS, FedEx integrated</p>
            </div>

            <!-- Store Features -->
            <div class="card">
                <h2>✨ E-Commerce Features</h2>
                <p>✅ <strong>Product Management</strong> - Unlimited products</p>
                <p>✅ <strong>Inventory Tracking</strong> - Real-time stock levels</p>
                <p>✅ <strong>Payment Processing</strong> - Multiple gateways</p>
                <p>✅ <strong>Shipping Integration</strong> - Auto-calculate rates</p>
                <p>✅ <strong>Customer Accounts</strong> - Registration & login</p>
                <p>✅ <strong>Order Management</strong> - Track & fulfill orders</p>
                <p>✅ <strong>Discount Codes</strong> - Coupons & promotions</p>
                <p>✅ <strong>Analytics</strong> - Sales reports & insights</p>
            </div>

            <!-- Popular Products -->
            <div class="card">
                <h2>🔥 Top Products This Month</h2>
                <div class="product-grid">
                    <div class="product-card">
                        <div style="font-size: 3em;">📚</div>
                        <strong>AI Guide</strong>
                        <p>$49.99</p>
                        <p style="font-size: 0.85em; color: #666;">234 sold</p>
                    </div>
                    <div class="product-card">
                        <div style="font-size: 3em;">🎨</div>
                        <strong>Design Kit</strong>
                        <p>$29.99</p>
                        <p style="font-size: 0.85em; color: #666;">189 sold</p>
                    </div>
                    <div class="product-card">
                        <div style="font-size: 3em;">💻</div>
                        <strong>Code Pack</strong>
                        <p>$39.99</p>
                        <p style="font-size: 0.85em; color: #666;">156 sold</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function createStore() {
            const name = document.getElementById('store-name').value;
            const type = document.getElementById('store-type').value;
            const niche = document.getElementById('store-niche').value;

            if (!name) {
                alert('⚠️ Please enter store name');
                return;
            }

            alert(`🚀 Creating ${name} store!\\n\\nType: ${type}\\nNiche: ${niche}\\n\\n⏳ Setting up products and payment gateways...`);
        }

        function addProduct() {
            const name = document.getElementById('product-name').value;
            const price = document.getElementById('product-price').value;

            if (!name || !price) {
                alert('⚠️ Please fill in product details');
                return;
            }

            alert(`✅ Product "${name}" added at $${price}!`);
        }
    </script>
</body>
</html>
"""

# Embedded 48 engines data (no import dependencies)
def get_engines_data():
    """Get 48 intelligence engines organized by cluster"""
    return {
        "Technology": [
            {"id": 1, "name": "AI & ML Research Engine", "domain": "Artificial Intelligence", "mode": "Research", "icon": "🤖", "capabilities": ["Model training", "Algorithm research", "Dataset analysis"]},
            {"id": 2, "name": "AI & ML Execution Engine", "domain": "Artificial Intelligence", "mode": "Execution", "icon": "⚡", "capabilities": ["Model deployment", "API integration", "Real-time inference"]},
            {"id": 3, "name": "Quantum Computing Research Engine", "domain": "Quantum Computing", "mode": "Research", "icon": "⚛️", "capabilities": ["Quantum algorithms", "Simulation", "Circuit design"]},
            {"id": 4, "name": "Quantum Computing Execution Engine", "domain": "Quantum Computing", "mode": "Execution", "icon": "🔬", "capabilities": ["Quantum processing", "Optimization", "Cryptography"]},
            {"id": 5, "name": "Connectivity Research Engine", "domain": "5G/6G/Satellite", "mode": "Research", "icon": "📡", "capabilities": ["Network analysis", "Protocol research", "Coverage mapping"]},
            {"id": 6, "name": "Connectivity Execution Engine", "domain": "5G/6G/Satellite", "mode": "Execution", "icon": "🛰️", "capabilities": ["Network deployment", "Signal optimization", "IoT integration"]},
            {"id": 7, "name": "Clean Energy Research Engine", "domain": "Clean Energy", "mode": "Research", "icon": "🌱", "capabilities": ["Energy modeling", "Climate data", "Sustainability metrics"]},
            {"id": 8, "name": "Clean Energy Execution Engine", "domain": "Clean Energy", "mode": "Execution", "icon": "⚡", "capabilities": ["Grid optimization", "Renewable deployment", "Energy storage"]},
            {"id": 9, "name": "Space Research Engine", "domain": "Space Technology", "mode": "Research", "icon": "🚀", "capabilities": ["Orbital mechanics", "Satellite design", "Mission planning"]},
            {"id": 10, "name": "Space Execution Engine", "domain": "Space Technology", "mode": "Execution", "icon": "🛸", "capabilities": ["Launch coordination", "Satellite operations", "Ground control"]}
        ],
        "Bioengineering": [
            {"id": 11, "name": "Synthetic Biology Research Engine", "domain": "Synthetic Biology", "mode": "Research", "icon": "🧬", "capabilities": ["Gene sequencing", "Protein design", "CRISPR research"]},
            {"id": 12, "name": "Synthetic Biology Execution Engine", "domain": "Synthetic Biology", "mode": "Execution", "icon": "🔬", "capabilities": ["Gene editing", "Organism design", "Biomanufacturing"]},
            {"id": 13, "name": "Neurotechnology Research Engine", "domain": "Neurotechnology", "mode": "Research", "icon": "🧠", "capabilities": ["Brain mapping", "Neural signals", "Cognitive studies"]},
            {"id": 14, "name": "Neurotechnology Execution Engine", "domain": "Neurotechnology", "mode": "Execution", "icon": "🔌", "capabilities": ["BCI implementation", "Neural interfaces", "Prosthetic control"]},
            {"id": 15, "name": "Biotechnology Research Engine", "domain": "Biotechnology", "mode": "Research", "icon": "💊", "capabilities": ["Drug discovery", "Clinical trials", "Disease research"]},
            {"id": 16, "name": "Biotechnology Execution Engine", "domain": "Biotechnology", "mode": "Execution", "icon": "⚕️", "capabilities": ["Drug production", "Treatment deployment", "Patient care"]},
            {"id": 17, "name": "Health Sovereignty Research Engine", "domain": "Health Sovereignty", "mode": "Research", "icon": "🏥", "capabilities": ["Healthcare systems", "Medical independence", "Data privacy"]},
            {"id": 18, "name": "Health Sovereignty Execution Engine", "domain": "Health Sovereignty", "mode": "Execution", "icon": "🛡️", "capabilities": ["System implementation", "Data protection", "Care coordination"]}
        ],
        "Security": [
            {"id": 19, "name": "Cybersecurity Research Engine", "domain": "Cybersecurity", "mode": "Research", "icon": "🔐", "capabilities": ["Threat analysis", "Vulnerability research", "Security protocols"]},
            {"id": 20, "name": "Cybersecurity Execution Engine", "domain": "Cybersecurity", "mode": "Execution", "icon": "🛡️", "capabilities": ["Threat mitigation", "Incident response", "System hardening"]},
            {"id": 21, "name": "Identity Research Engine", "domain": "Identity Management", "mode": "Research", "icon": "👤", "capabilities": ["Identity protocols", "Authentication research", "Privacy frameworks"]},
            {"id": 22, "name": "Identity Execution Engine", "domain": "Identity Management", "mode": "Execution", "icon": "🔑", "capabilities": ["IAM deployment", "SSO implementation", "Access control"]},
            {"id": 23, "name": "Blockchain Research Engine", "domain": "Blockchain & Web3", "mode": "Research", "icon": "⛓️", "capabilities": ["Smart contract analysis", "Consensus research", "DeFi security"]},
            {"id": 24, "name": "Blockchain Execution Engine", "domain": "Blockchain & Web3", "mode": "Execution", "icon": "💎", "capabilities": ["Contract deployment", "Chain operations", "Wallet security"]},
            {"id": 25, "name": "Privacy Research Engine", "domain": "Privacy & Encryption", "mode": "Research", "icon": "🔒", "capabilities": ["Encryption algorithms", "Zero-knowledge proofs", "Privacy protocols"]},
            {"id": 26, "name": "Privacy Execution Engine", "domain": "Privacy & Encryption", "mode": "Execution", "icon": "🗝️", "capabilities": ["Encryption deployment", "VPN services", "Data protection"]}
        ],
        "Communication": [
            {"id": 27, "name": "Social Media Research Engine", "domain": "Social Media", "mode": "Research", "icon": "📱", "capabilities": ["Trend analysis", "Audience research", "Content analytics"]},
            {"id": 28, "name": "Social Media Execution Engine", "domain": "Social Media", "mode": "Execution", "icon": "🚀", "capabilities": ["Content publishing", "Campaign management", "Engagement automation"]},
            {"id": 29, "name": "Content Research Engine", "domain": "Content Marketing", "mode": "Research", "icon": "📝", "capabilities": ["SEO research", "Keyword analysis", "Competitor analysis"]},
            {"id": 30, "name": "Content Execution Engine", "domain": "Content Marketing", "mode": "Execution", "icon": "✍️", "capabilities": ["Content creation", "Publishing workflows", "Distribution"]},
            {"id": 31, "name": "Email Research Engine", "domain": "Email Marketing", "mode": "Research", "icon": "📧", "capabilities": ["List analysis", "Segmentation research", "A/B testing"]},
            {"id": 32, "name": "Email Execution Engine", "domain": "Email Marketing", "mode": "Execution", "icon": "📨", "capabilities": ["Campaign deployment", "Automation sequences", "List management"]},
            {"id": 33, "name": "Video Research Engine", "domain": "Video Content", "mode": "Research", "icon": "🎥", "capabilities": ["Video trends", "Platform analytics", "Audience preferences"]},
            {"id": 34, "name": "Video Execution Engine", "domain": "Video Content", "mode": "Execution", "icon": "🎬", "capabilities": ["Video creation", "Editing workflows", "Multi-platform publishing"]}
        ],
        "Planetary": [
            {"id": 35, "name": "Infrastructure Research Engine", "domain": "Infrastructure", "mode": "Research", "icon": "🏗️", "capabilities": ["System analysis", "Resilience studies", "Failure modeling"]},
            {"id": 36, "name": "Infrastructure Execution Engine", "domain": "Infrastructure", "mode": "Execution", "icon": "🏛️", "capabilities": ["System deployment", "Maintenance automation", "Disaster recovery"]},
            {"id": 37, "name": "Climate Research Engine", "domain": "Climate Adaptation", "mode": "Research", "icon": "🌍", "capabilities": ["Climate modeling", "Risk assessment", "Adaptation strategies"]},
            {"id": 38, "name": "Climate Execution Engine", "domain": "Climate Adaptation", "mode": "Execution", "icon": "🌊", "capabilities": ["Mitigation projects", "Adaptation implementation", "Monitoring systems"]},
            {"id": 39, "name": "Supply Chain Research Engine", "domain": "Supply Chain", "mode": "Research", "icon": "📦", "capabilities": ["Network analysis", "Disruption modeling", "Optimization studies"]},
            {"id": 40, "name": "Supply Chain Execution Engine", "domain": "Supply Chain", "mode": "Execution", "icon": "🚚", "capabilities": ["Logistics management", "Inventory optimization", "Route planning"]},
            {"id": 41, "name": "Agriculture Research Engine", "domain": "Agriculture", "mode": "Research", "icon": "🌾", "capabilities": ["Crop optimization", "Soil analysis", "Weather patterns"]},
            {"id": 42, "name": "Agriculture Execution Engine", "domain": "Agriculture", "mode": "Execution", "icon": "🚜", "capabilities": ["Precision farming", "Automated irrigation", "Harvest optimization"]}
        ],
        "Business": [
            {"id": 43, "name": "Market Research Engine", "domain": "Market Intelligence", "mode": "Research", "icon": "📊", "capabilities": ["Market analysis", "Competitor research", "Trend identification"]},
            {"id": 44, "name": "Market Execution Engine", "domain": "Market Intelligence", "mode": "Execution", "icon": "📈", "capabilities": ["Strategy implementation", "Campaign execution", "Performance tracking"]},
            {"id": 45, "name": "Financial Research Engine", "domain": "Financial Analytics", "mode": "Research", "icon": "💰", "capabilities": ["Financial modeling", "Risk analysis", "Investment research"]},
            {"id": 46, "name": "Financial Execution Engine", "domain": "Financial Analytics", "mode": "Execution", "icon": "💵", "capabilities": ["Portfolio management", "Trading automation", "Financial reporting"]},
            {"id": 47, "name": "Customer Research Engine", "domain": "Customer Analytics", "mode": "Research", "icon": "👥", "capabilities": ["Behavior analysis", "Segmentation", "Journey mapping"]},
            {"id": 48, "name": "Customer Execution Engine", "domain": "Customer Analytics", "mode": "Execution", "icon": "🎯", "capabilities": ["Personalization", "CRM automation", "Experience optimization"]}
        ]
    }

# Embedded tools data (no import dependencies)
def get_tools_data():
    """Get 6 Codex tools"""
    return [
        {
            "id": "flow-orchestrator",
            "name": "Flow Orchestrator",
            "icon": "🔄",
            "description": "Visual workflow automation builder (N8N alternative)",
            "replaces": "N8N",
            "features": ["Drag-drop builder", "200+ integrations", "Schedule triggers", "Error handling", "Webhook support", "API connections"],
            "savings": "$50/month",
            "status": "active"
        },
        {
            "id": "ai-content-engine",
            "name": "AI Content Engine",
            "icon": "✨",
            "description": "AI-powered content generation and research (GenSpark alternative)",
            "replaces": "GenSpark",
            "features": ["Multi-model AI", "Research automation", "Content generation", "SEO optimization", "Fact-checking", "Multi-format output"],
            "savings": "$99/month",
            "status": "active"
        },
        {
            "id": "research-studio",
            "name": "Research Studio",
            "icon": "📚",
            "description": "Interactive research assistant with document Q&A (NotebookLLM alternative)",
            "replaces": "NotebookLLM",
            "features": ["Document upload", "AI Q&A", "Source citations", "Note-taking", "Knowledge graphs", "Export reports"],
            "savings": "$20/month (enhanced free)",
            "status": "active"
        },
        {
            "id": "design-forge",
            "name": "Design Forge",
            "icon": "📖",
            "description": "Professional eBook and document designer (Designrr alternative)",
            "replaces": "Designrr",
            "features": ["Template library", "Drag-drop editor", "Multi-format export", "Brand customization", "Content import", "Auto-formatting"],
            "savings": "$39/month",
            "status": "active"
        },
        {
            "id": "nano-builder",
            "name": "Nano Builder",
            "icon": "⚡",
            "description": "Micro-app and mini-site builder (Nano Banana alternative)",
            "replaces": "Nano Banana",
            "features": ["Instant deployment", "No-code builder", "Custom domains", "Analytics", "Mobile responsive", "SEO ready"],
            "savings": "$29/month",
            "status": "active"
        },
        {
            "id": "app-constructor",
            "name": "App Constructor",
            "icon": "🏗️",
            "description": "Full-stack application builder (Loveable alternative)",
            "replaces": "Loveable",
            "features": ["AI code generation", "Full-stack templates", "Database integration", "API builder", "Deployment automation", "Version control"],
            "savings": "$79/month",
            "status": "active"
        }
    ]

# All 52 Dashboards organized by category
def get_all_dashboards():
    """Get all 52 dashboards organized by category"""
    return {
        "Core Systems (10)": [
            {"name": "Master Dashboard Ultimate", "icon": "👑", "description": "Central command center", "status": "✅ LIVE"},
            {"name": "48 Intelligence Engines", "icon": "🧠", "description": "Complete intelligence system", "status": "✅ LIVE"},
            {"name": "Codex Tools Suite", "icon": "🔧", "description": "6 FREE tools ($316/mo savings)", "status": "✅ LIVE"},
            {"name": "System Status Monitor", "icon": "📊", "description": "Real-time system metrics", "status": "✅ LIVE"},
            {"name": "Council Seal Governance", "icon": "👑", "description": "Supreme authority dashboard", "status": "✅ LIVE"},
            {"name": "Codex Eternum Omega", "icon": "♾️", "description": "Eternal system state", "status": "✅ LIVE"},
            {"name": "Dashboard Optimizer", "icon": "⚡", "description": "Performance optimization", "status": "✅ LIVE"},
            {"name": "Treasury Management", "icon": "💰", "description": "Financial tracking", "status": "✅ LIVE"},
            {"name": "Dawn Dispatch System", "icon": "🌅", "description": "Daily operations", "status": "✅ LIVE"},
            {"name": "Proclamations Archive", "icon": "📜", "description": "System decrees", "status": "✅ LIVE"}
        ],
        "AI & Intelligence (8)": [
            {"name": "AI Action Stock Analytics", "icon": "📈", "description": "Stock market AI analysis", "status": "✅ LIVE"},
            {"name": "AI Command System", "icon": "⌨️", "description": "AI system control", "status": "✅ LIVE"},
            {"name": "AI Development Studio", "icon": "🎨", "description": "AI app builder", "status": "✅ LIVE"},
            {"name": "AI Graphic Video Studio", "icon": "🎬", "description": "Video generation", "status": "✅ LIVE"},
            {"name": "Algorithm AI", "icon": "🧮", "description": "Algorithm development", "status": "✅ LIVE"},
            {"name": "Jermaine Super AI Agent", "icon": "⚡", "description": "Personal AI powerhouse", "status": "✅ LIVE"},
            {"name": "AI Trinity System", "icon": "🔱", "description": "Triple AI integration", "status": "✅ LIVE"},
            {"name": "300 Agents Expansion", "icon": "🤖", "description": "Multi-agent system", "status": "✅ LIVE"}
        ],
        "Analytics & Data (7)": [
            {"name": "Advanced Data Analytics", "icon": "📊", "description": "Deep data insights", "status": "✅ LIVE"},
            {"name": "Stock Analytics Dashboard", "icon": "💹", "description": "Real-time stock data", "status": "✅ LIVE"},
            {"name": "Portfolio Dashboard", "icon": "💼", "description": "Investment tracking", "status": "✅ LIVE"},
            {"name": "Financial Analytics", "icon": "💰", "description": "Complete financial view", "status": "✅ LIVE"},
            {"name": "Customer Analytics", "icon": "👥", "description": "Customer insights", "status": "✅ LIVE"},
            {"name": "Market Intelligence", "icon": "🎯", "description": "Market analysis", "status": "✅ LIVE"},
            {"name": "Business Metrics", "icon": "📉", "description": "KPI tracking", "status": "✅ LIVE"}
        ],
        "Technology & Systems (7)": [
            {"name": "Ultimate Technology Dashboard", "icon": "💻", "description": "Tech stack overview", "status": "✅ LIVE"},
            {"name": "Cybersecurity Dashboard", "icon": "🔐", "description": "Security monitoring", "status": "✅ LIVE"},
            {"name": "Infrastructure Monitor", "icon": "🏗️", "description": "System infrastructure", "status": "✅ LIVE"},
            {"name": "DevOps Pipeline", "icon": "🔄", "description": "CI/CD tracking", "status": "✅ LIVE"},
            {"name": "Cloud Resources", "icon": "☁️", "description": "Multi-cloud management", "status": "✅ LIVE"},
            {"name": "Database Monitor", "icon": "🗄️", "description": "DB performance", "status": "✅ LIVE"},
            {"name": "API Gateway", "icon": "🌐", "description": "API management", "status": "✅ LIVE"}
        ],
        "E-Commerce & Business (6)": [
            {"name": "WooCommerce Integration", "icon": "🛒", "description": "E-commerce platform", "status": "✅ LIVE"},
            {"name": "Affiliate Management", "icon": "🤝", "description": "Affiliate tracking", "status": "✅ LIVE"},
            {"name": "Pinterest Integration", "icon": "📌", "description": "Pinterest automation", "status": "✅ LIVE"},
            {"name": "TikTok Automation", "icon": "🎵", "description": "TikTok content", "status": "✅ LIVE"},
            {"name": "WhatsApp Business", "icon": "💬", "description": "WhatsApp integration", "status": "✅ LIVE"},
            {"name": "E-commerce Suite", "icon": "🏪", "description": "Complete e-commerce", "status": "✅ LIVE"}
        ],
        "Health & Biotech (5)": [
            {"name": "Biotech Dashboard", "icon": "🧬", "description": "Biotechnology tracking", "status": "✅ LIVE"},
            {"name": "Health Sovereignty", "icon": "🏥", "description": "Health data management", "status": "✅ LIVE"},
            {"name": "Neurotechnology", "icon": "🧠", "description": "Brain-computer interfaces", "status": "✅ LIVE"},
            {"name": "Synthetic Biology", "icon": "🔬", "description": "Genetic engineering", "status": "✅ LIVE"},
            {"name": "Medical Research", "icon": "⚕️", "description": "Research tracking", "status": "✅ LIVE"}
        ],
        "Content & Creative (5)": [
            {"name": "Content Studio", "icon": "📝", "description": "Content creation hub", "status": "✅ LIVE"},
            {"name": "Video Generator", "icon": "🎥", "description": "Automated video", "status": "✅ LIVE"},
            {"name": "eBook Generator", "icon": "📚", "description": "Advanced eBook creation", "status": "✅ LIVE"},
            {"name": "Design Forge", "icon": "🎨", "description": "Creative design tools", "status": "✅ LIVE"},
            {"name": "Social Media Hub", "icon": "📱", "description": "Multi-platform management", "status": "✅ LIVE"}
        ],
        "Specialized Tools (4)": [
            {"name": "Fact Checking Engine", "icon": "✓", "description": "AI fact verification", "status": "✅ LIVE"},
            {"name": "Advent Devotional Generator", "icon": "📖", "description": "Faith content", "status": "✅ LIVE"},
            {"name": "Archive Integration", "icon": "🗃️", "description": "Data archival", "status": "✅ LIVE"},
            {"name": "Firewall Manager", "icon": "🛡️", "description": "Security firewall", "status": "✅ LIVE"}
        ]
    }

# Dashboard routes
@app.route('/')
def index():
    """Caribbean Digital Economy Homepage"""
    return render_template('homepage.html',
        seo_title="CodexDominion — The Caribbean's Digital Economy",
        seo_description="The first digital economy built for Caribbean creators, youth, and diaspora.",
        hero_headline="Your Culture. Your Creators. Your Digital Economy.",
        hero_subheadline="The Caribbean's first unified platform for creators, youth, and diaspora.",
        primary_cta_label="Enter the Marketplace",
        primary_cta_href="/marketplace",
        secondary_cta_label="Join DominionYouth",
        secondary_cta_href="/dominionyouth",
        engines_title="Three Engines. One Digital Economy.",
        engine_items=[
            {
                "label": "IslandNation Marketplace",
                "description": "Creators sell digital products globally."
            },
            {
                "label": "DominionYouth",
                "description": "Youth earn commissions by promoting creator products."
            },
            {
                "label": "Action AI",
                "description": "AI tools that help creators build, package, and promote."
            }
        ]
    )

@app.route('/marketplace')
def marketplace():
    """IslandNation Marketplace - Coming Soon"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>IslandNation Marketplace | CodexDominion</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='css/design-system.css') }}">
    </head>
    <body>
        <div class="container section" style="text-align: center; min-height: 80vh; display: flex; flex-direction: column; justify-content: center;">
            <h1 class="display mb-5">🏝️ IslandNation Marketplace</h1>
            <p class="body mb-6" style="max-width: 600px; margin: 0 auto;">
                Where Caribbean creators sell digital products globally. Coming soon!
            </p>
            <div>
                <a href="/" class="btn btn-primary">Back to Home</a>
            </div>
        </div>
    </body>
    </html>
    """)

@app.route('/dominionyouth')
def dominionyouth():
    """DominionYouth Platform - Coming Soon"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>DominionYouth | CodexDominion</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='css/design-system.css') }}">
    </head>
    <body>
        <div class="container section" style="text-align: center; min-height: 80vh; display: flex; flex-direction: column; justify-content: center;">
            <h1 class="display mb-5">🎓 DominionYouth</h1>
            <p class="body mb-6" style="max-width: 600px; margin: 0 auto;">
                Youth earn commissions by promoting creator products. Join the movement!
            </p>
            <div>
                <a href="/" class="btn btn-primary">Back to Home</a>
            </div>
        </div>
    </body>
    </html>
    """)

@app.route('/engines')
def engines():
    """48 Intelligence Engines page"""
    try:
        clusters = get_engines_data()
        return render_template_string(ENGINES_HTML, clusters=clusters)
    except Exception as e:
        return f"<h1>48 Intelligence Engines</h1><p>System initializing... Error: {e}</p><a href='/'>Back</a>"

@app.route('/tools')
def tools():
    """Tools Suite page"""
    try:
        tools_list = get_tools_data()
        return render_template_string(TOOLS_HTML, tools=tools_list)
    except Exception as e:
        return f"<h1>🔧 Codex Tools Suite</h1><p>System initializing... Error: {e}</p><a href='/'>Back</a>"

@app.route('/status')
def status():
    """System status API"""
    return jsonify({
        "status": "operational",
        "engines": 48,
        "tools": 6,
        "dashboards": 52,
        "uptime": "99.9%",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "version": "1.0.0"})

@app.route('/chat')
def chat():
    """AI Chat page"""
    return render_template_string(CHAT_HTML)

@app.route('/dashboards')
def dashboards():
    """All Dashboards page"""
    try:
        all_dashboards = get_all_dashboards()
        return render_template_string(DASHBOARDS_HTML, all_dashboards=all_dashboards)
    except Exception as e:
        return f"<h1>📊 All Dashboards</h1><p>Loading... Error: {e}</p><a href='/'>Back</a>"

@app.route('/agents')
def agents():
    """AI Agents page"""
    return render_template_string(AGENTS_HTML)

@app.route('/email')
def email():
    """Email system page"""
    return render_template_string(EMAIL_HTML)

@app.route('/documents')
def documents():
    """Document management page"""
    return render_template_string(DOCUMENTS_HTML)

@app.route('/avatars')
def avatars():
    """Avatar system page"""
    return render_template_string(AVATARS_HTML)

@app.route('/council')
def council():
    """Council Seal page"""
    return render_template_string(COUNCIL_HTML)

@app.route('/copilot')
def copilot():
    """VS Code Copilot page"""
    return render_template_string(COPILOT_HTML)

@app.route('/ai-advisor')
def ai_advisor():
    """AI Advisor Dashboard - Intelligent Recommendations"""
    return render_template_string(AI_ADVISOR_HTML)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User(email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flask_flask_session["user_id"] = user.id
        return redirect("/studio/graphics")

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            email = request.form.get("email")
            password = request.form.get("password")

            user = User.query.filter_by(email=email).first()

            if user and user.check_password(password):
                flask_flask_session["user_id"] = user.id
                return redirect("/studio/graphics")
            else:
                return render_template("login.html", error="Invalid email or password")
        except Exception as e:
            print(f"Login error: {e}")
            import traceback
            traceback.print_exc()
            return render_template("login.html", error="An error occurred during login")

    return render_template("login.html")

@app.route("/logout")
def logout():
    flask_flask_session.pop("user_id", None)
    return redirect("/login")

@app.route('/studio')
def creative_studio():
    """Creative Studio - AI Graphics, Video & Audio"""
    return render_template_string(STUDIO_HTML)

@app.route("/studio/graphics", methods=["GET", "POST"])
def graphics_studio():
    if request.method == "POST":
        prompt = request.form.get("prompt")
        return render_template("graphics_studio.html", prompt=prompt)

    return render_template("graphics_studio.html", prompt=None)

@app.route("/studio/graphics/generate", methods=["POST"])
def generate_graphic():
    prompt = request.form.get("prompt")
    aspect_ratio = request.form.get("aspect_ratio")
    color_palette = request.form.get("color_palette")
    mood = request.form.get("mood")
    lighting = request.form.get("lighting")
    camera_angle = request.form.get("camera_angle")
    is_variation = request.form.get("variation") == "true"

    if is_variation:
        # Later: call your AI model with variation mode
        variation_mode = True
    else:
        variation_mode = False

    # Build the final prompt that will be sent to your AI generator
    mode_prefix = "Create variations of: " if is_variation else ""
    final_prompt = f"""
    {mode_prefix}{prompt}

    Style details:
    - Aspect Ratio: {aspect_ratio}
    - Color Palette: {color_palette}
    - Mood: {mood}
    - Lighting: {lighting}
    - Camera Angle: {camera_angle}
    {"- Mode: Generate Variations" if is_variation else ""}
    """

    if is_variation:
        final_prompt = f"{final_prompt}\n\n[Variation Mode Enabled]"

    # Placeholder for now — this is where your AI call will go
    # Pass is_variation to your AI model if it supports variation mode
    generated_images = call_your_ai_model(final_prompt, is_variation=variation_mode)

    return render_template(
        "graphics_studio.html",
        prompt=prompt,
        final_prompt=final_prompt,
        generated_images=generated_images,
        aspect_ratio=aspect_ratio,
        color_palette=color_palette,
        mood=mood,
        lighting=lighting,
        camera_angle=camera_angle,
        is_variation=is_variation
    )

@app.route("/studio/graphics/save", methods=["POST"])
def save_graphics_project():
    user_id = flask_session.get("user_id")
    team_id = request.form.get("team_id") or None
    
    # Check permission if saving to a team
    if team_id and not can_create_project(int(team_id), user_id):
        return "Access denied - Editor, Admin, or Owner role required to create team projects", 403

    prompt_text = request.form.get("prompt")
    parent_prompt_id = request.form.get("parent_prompt_id")  # If this is an evolved prompt
    
    project = GraphicsProject(
        prompt=prompt_text,
        aspect_ratio=request.form.get("aspect_ratio"),
        color_palette=request.form.get("color_palette"),
        mood=request.form.get("mood"),
        lighting=request.form.get("lighting"),
        camera_angle=request.form.get("camera_angle"),
        thumbnail_url=request.form.get("thumbnail_url"),
        tags=request.form.get("tags"),
        category=request.form.get("category"),
        user_id=user_id,
        team_id=team_id,
        parent_prompt_id=parent_prompt_id if parent_prompt_id else None,
        prompt_source=request.form.get("prompt_source", "user_written"),
        original_prompt=prompt_text  # Store immutable original
    )

    db.session.add(project)
    db.session.commit()

    # Create or update PromptHistory entry
    if team_id:
        # Check if this prompt already exists in history
        existing_prompt = PromptHistory.query.filter_by(
            team_id=int(team_id),
            prompt_text=prompt_text
        ).first()
        
        if existing_prompt:
            # Update usage metrics
            existing_prompt.times_used += 1
            existing_prompt.times_saved += 1
            existing_prompt.effectiveness_score = calculate_prompt_effectiveness(existing_prompt)
            db.session.commit()
            
            # Link project to prompt history
            project.parent_prompt_id = existing_prompt.id
            db.session.commit()
        else:
            # Create new prompt history entry
            prompt_history = PromptHistory(
                prompt_text=prompt_text,
                team_id=int(team_id),
                created_by=user_id,
                mood=request.form.get("mood"),
                color_palette=request.form.get("color_palette"),
                tags=request.form.get("tags"),
                category=request.form.get("category"),
                parent_id=int(parent_prompt_id) if parent_prompt_id else None,
                generation=1 if not parent_prompt_id else 2,
                times_used=1,
                times_saved=1
            )
            db.session.add(prompt_history)
            db.session.commit()
            
            # Link project to new prompt history
            project.parent_prompt_id = prompt_history.id
            db.session.commit()
        
        # Log activity with usage signal
        log_activity(int(team_id), user_id, "saved a project", {
            "project_id": project.id,
            "prompt_length": len(prompt_text),
            "usage_signal": "saved"
        })

    return render_template(
        "graphics_studio.html",
        prompt=project.prompt,
        generated_images=[],
        saved=True
    )

@app.route("/studio/graphics/export/json", methods=["POST"])
def export_graphics_json():
    user_id = flask_session.get("user_id")
    project_id = request.form.get("project_id")
    team_id = request.form.get("team_id")
    
    project = {
        "prompt": request.form.get("prompt"),
        "aspect_ratio": request.form.get("aspect_ratio"),
        "color_palette": request.form.get("color_palette"),
        "mood": request.form.get("mood"),
        "lighting": request.form.get("lighting"),
        "camera_angle": request.form.get("camera_angle"),
        "timestamp": datetime.utcnow().isoformat()
    }

    # Log export activity and update prompt history
    if project_id and team_id:
        proj = GraphicsProject.query.get(int(project_id))
        if proj and proj.parent_prompt_id:
            prompt_hist = PromptHistory.query.get(proj.parent_prompt_id)
            if prompt_hist:
                prompt_hist.times_saved += 1
                prompt_hist.effectiveness_score = calculate_prompt_effectiveness(prompt_hist)
                db.session.commit()
        
        log_activity(int(team_id), user_id, "exported a project", {
            "project_id": int(project_id),
            "format": "json",
            "usage_signal": "exported"
        })

    json_data = json.dumps(project, indent=4)

    return Response(
        json_data,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=project.json"}
    )

@app.route("/studio/graphics/export/image", methods=["POST"])
def export_graphics_image():
    image_url = request.form.get("image_url")

    # Placeholder: once you have real images, fetch and return them
    return Response(
        f"Image export placeholder for: {image_url}",
        mimetype="text/plain"
    )

@app.route("/studio/graphics/library")
def graphics_library():
    user_id = flask_session.get("user_id")
    q = request.args.get("q", "")
    mood = request.args.get("mood", "")
    palette = request.args.get("palette", "")
    lighting = request.args.get("lighting", "")
    tag = request.args.get("tag", "")
    category = request.args.get("category", "")
    
    query = GraphicsProject.query.filter_by(user_id=user_id)
    
    if q:
        query = query.filter(GraphicsProject.prompt.ilike(f"%{q}%"))

    if mood:
        query = query.filter_by(mood=mood)

    if palette:
        query = query.filter_by(color_palette=palette)

    if lighting:
        query = query.filter_by(lighting=lighting)

    if tag:
        query = query.filter(GraphicsProject.tags.ilike(f"%{tag}%"))

    if category:
        query = query.filter(GraphicsProject.category.ilike(f"%{category}%"))

    projects = query.order_by(GraphicsProject.timestamp.desc()).all()

    return render_template("project_library.html", projects=projects)

@app.route("/studio/graphics/team/<int:team_id>")
def team_library(team_id):
    user_id = flask_session.get("user_id")
    
    # Redirect to login if not authenticated
    if not user_id:
        return redirect("/login")

    # Ensure user can view this team
    if not can_view_team(team_id, user_id):
        return "Access denied - You must be a team member to view this library", 403

    projects = GraphicsProject.query.filter_by(team_id=team_id).order_by(GraphicsProject.timestamp.desc()).all()

    team = Team.query.get(team_id)
    user_role = get_user_role(team_id, user_id)

    return render_template("team_library.html", team=team, projects=projects, user_role=user_role)

@app.route("/teams/create", methods=["GET", "POST"])
def create_team():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        owner_id = flask_session.get("user_id")

        team = Team(name=name, description=description, owner_id=owner_id)
        db.session.add(team)
        db.session.commit()

        # Add owner as member
        membership = TeamMember(team_id=team.id, user_id=owner_id, role="owner")
        db.session.add(membership)
        db.session.commit()

        return redirect(f"/studio/graphics/team/{team.id}")

    return render_template("create_team.html")

def evolve_prompt(original_prompt, project=None, reason="refinement", count=5):
    """Generate evolved variants of a prompt - the prompt evolution engine.
    
    Takes a prompt and generates 3-5 evolved variations based on:
    - The original prompt text
    - Project context (mood, palette, lighting, tags)
    - Evolution reason (refinement, exploration, remix)
    
    Returns list of evolved prompt variants with metadata.
    """
    import random
    
    # Evolution strategies based on reason
    strategies = {
        "refinement": [
            "Enhance specificity and detail",
            "Add atmospheric depth",
            "Introduce subtle complexity",
            "Refine emotional tone",
            "Sharpen visual focus"
        ],
        "exploration": [
            "Shift perspective dramatically",
            "Introduce contrasting elements",
            "Explore alternate moods",
            "Transform scale and proportion",
            "Reimagine through different medium"
        ],
        "remix": [
            "Blend with complementary themes",
            "Invert dominant characteristics",
            "Layer in symbolic depth",
            "Fuse with fresh palette",
            "Add narrative complexity"
        ]
    }
    
    # Get context from project if available
    mood = project.mood if project else "cinematic"
    palette = project.color_palette if project else "vibrant"
    lighting = project.lighting if project else "dramatic shadows"
    tags = project.tags if project else ""
    
    # Evolution modifiers (things we can layer onto prompts)
    atmosphere_modifiers = [
        "bathed in ethereal mist", "charged with electric energy", "suspended in dreamlike stillness",
        "alive with kinetic motion", "wrapped in mysterious shadows", "glowing with inner radiance"
    ]
    
    detail_layers = [
        "intricate patterns woven throughout", "subtle textures emerging from darkness",
        "crystalline structures catching light", "organic forms intertwining",
        "geometric precision meets natural chaos", "layered transparencies revealing depth"
    ]
    
    perspective_shifts = [
        "viewed from an impossible angle", "framed through architectural elements",
        "reflected in fractured surfaces", "seen through a veil of translucency",
        "captured at the threshold of transformation", "witnessed from cosmic distance"
    ]
    
    # Generate evolved variants
    variants = []
    selected_strategies = random.sample(strategies.get(reason, strategies["refinement"]), min(count, 5))
    
    for i, strategy in enumerate(selected_strategies):
        # Base evolution on original prompt
        evolved_text = original_prompt
        
        # Apply evolution layers
        atmosphere = random.choice(atmosphere_modifiers)
        detail = random.choice(detail_layers)
        perspective = random.choice(perspective_shifts) if i % 2 == 0 else ""
        
        # Construct evolved prompt
        if "mood" in original_prompt.lower() or "atmosphere" in original_prompt.lower():
            # Replace mood/atmosphere
            evolved_text = f"{original_prompt.split(',')[0]} — {atmosphere}, {detail}"
        elif perspective:
            evolved_text = f"{original_prompt}, {perspective}, {detail}"
        else:
            evolved_text = f"{original_prompt} — {atmosphere}, {detail}"
        
        # Suggest evolved attributes
        evolved_mood = mood
        evolved_palette = palette
        evolved_lighting = lighting
        
        # For exploration, shift attributes more dramatically
        if reason == "exploration":
            alt_moods = ["ethereal", "dramatic", "serene", "mysterious", "cinematic"]
            alt_palettes = ["monochrome", "jewel tones", "sunset", "neon", "arctic"]
            alt_lighting = ["golden hour", "neon glow", "moonlight", "rim lighting", "backlit"]
            
            evolved_mood = random.choice(alt_moods)
            evolved_palette = random.choice(alt_palettes)
            evolved_lighting = random.choice(alt_lighting)
        
        variants.append({
            "prompt": evolved_text,
            "strategy": strategy,
            "generation": (project.prompt_version + 1) if project and project.prompt_version else 2,
            "mood": evolved_mood,
            "palette": evolved_palette,
            "lighting": evolved_lighting,
            "evolution_reason": reason
        })
    
    return variants


def calculate_prompt_effectiveness(prompt_history):
    """Calculate effectiveness score for a prompt based on usage patterns.
    
    Score factors:
    - times_used (how often it's selected)
    - times_saved (projects saved/exported)
    - times_reused (copied/remixed)
    - avg_engagement (time spent, iterations)
    
    Returns: float score 0.0-100.0
    """
    if not prompt_history:
        return 0.0
    
    # Weighted scoring
    usage_score = min(prompt_history.times_used * 5, 30)  # Max 30 points
    save_score = min(prompt_history.times_saved * 10, 30)  # Max 30 points
    reuse_score = min(prompt_history.times_reused * 15, 25)  # Max 25 points
    engagement_score = min(prompt_history.avg_engagement * 3, 15)  # Max 15 points
    
    total = usage_score + save_score + reuse_score + engagement_score
    
    return round(total, 2)


def get_team_strongest_prompts(team_id, limit=10):
    """Identify the team's strongest prompts based on effectiveness scores.
    
    Returns top N prompts that led to the most successful projects.
    """
    prompts = PromptHistory.query.filter_by(
        team_id=team_id
    ).order_by(
        PromptHistory.effectiveness_score.desc(),
        PromptHistory.times_saved.desc(),
        PromptHistory.times_reused.desc()
    ).limit(limit).all()
    
    return prompts


def generate_ai_prompt_suggestions(projects, count=5):
    """Generate AI-powered prompt suggestions based on team's creative DNA.
    
    Pattern:
    1. Base on dominant tag or category
    2. Infuse favorite mood
    3. Apply preferred palette or lighting
    4. Add a twist (something rarely used)
    5. Wrap into clean, generative prompt
    """
    import random
    
    if not projects:
        return []
    
    # Analyze team's creative patterns
    mood_counts = {}
    palette_counts = {}
    lighting_counts = {}
    camera_counts = {}
    tag_counts = {}
    category_counts = {}
    
    for p in projects:
        if p.mood:
            mood_counts[p.mood] = mood_counts.get(p.mood, 0) + 1
        if p.color_palette:
            palette_counts[p.color_palette] = palette_counts.get(p.color_palette, 0) + 1
        if p.lighting:
            lighting_counts[p.lighting] = lighting_counts.get(p.lighting, 0) + 1
        if p.camera_angle:
            camera_counts[p.camera_angle] = camera_counts.get(p.camera_angle, 0) + 1
        if p.category:
            category_counts[p.category] = category_counts.get(p.category, 0) + 1
        if p.tags:
            for tag in p.tags.split(","):
                tag = tag.strip().lower()
                if tag:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    # Get dominant patterns (team's DNA)
    top_mood = max(mood_counts, key=mood_counts.get) if mood_counts else "dramatic"
    top_palette = max(palette_counts, key=palette_counts.get) if palette_counts else "vibrant"
    top_lighting = max(lighting_counts, key=lighting_counts.get) if lighting_counts else "natural daylight"
    top_camera = max(camera_counts, key=camera_counts.get) if camera_counts else "eye level"
    top_tag = max(tag_counts, key=tag_counts.get) if tag_counts else "abstract"
    top_category = max(category_counts, key=category_counts.get) if category_counts else "Concept Art"
    
    # Get secondary patterns for variety
    top_moods = sorted(mood_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    top_palettes = sorted(palette_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    top_lighting_opts = sorted(lighting_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    top_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Complementary options for "the twist"
    all_moods = ["ethereal", "dramatic", "serene", "vibrant", "mysterious", "playful", "cinematic", "minimalist", "nostalgic", "heroic", "melancholic"]
    all_palettes = ["pastel", "monochrome", "vibrant", "earth tones", "neon", "jewel tones", "sunset", "ocean blues", "forest greens", "autumn", "arctic"]
    all_lighting = ["golden hour", "soft diffused", "dramatic shadows", "neon glow", "candlelight", "studio lighting", "natural daylight", "moonlight", "backlit", "rim lighting"]
    all_cameras = ["wide angle", "close-up", "aerial view", "eye level", "low angle", "high angle", "Dutch angle", "macro", "bird's eye"]
    
    # Find fresh elements (rarely used)
    used_moods = [m[0] for m in top_moods]
    used_palettes = [p[0] for p in top_palettes]
    used_lighting = [l[0] for l in top_lighting_opts]
    
    fresh_moods = [m for m in all_moods if m not in used_moods]
    fresh_palettes = [p for p in all_palettes if p not in used_palettes]
    fresh_lighting = [l for l in all_lighting if l not in used_lighting]
    
    # Sophisticated prompt templates following user's pattern
    # Shuffle templates for variety on each generation
    templates = [
        {
            "template": "A {top_tag} scene rendered in a {top_palette} palette, infused with {top_mood} energy and illuminated by {top_lighting} lighting — explore a new angle by adding unexpected architectural elements.",
            "twist": "architectural complexity",
            "twist_desc": "Unexpected architectural elements added"
        },
        {
            "template": "A character portrait inspired by {top_category}, blending {top_palette} tones with {top_mood} atmosphere — experiment with surreal textures or symbolic motifs.",
            "twist": "surreal textures",
            "twist_desc": "Surreal textures and symbolic motifs"
        },
        {
            "template": "A wide cinematic landscape rooted in {top_tag} themes, using {top_lighting} lighting and a restrained {top_palette} palette — introduce motion or weather to shift the emotional tone.",
            "twist": "dynamic weather",
            "twist_desc": "Motion and weather dynamics"
        },
        {
            "template": "A mythic tableau that merges {top_tag} symbolism with {top_mood} storytelling — push contrast by pairing your usual palette with a bold accent color.",
            "twist": "bold accent color",
            "twist_desc": f"Bold accent from {random.choice(fresh_palettes) if fresh_palettes else 'complementary'} palette"
        },
        {
            "template": "A futuristic environment inspired by your team's {top_category} work, rendered with {top_lighting} lighting and {top_palette} hues — explore scale by contrasting massive structures with intimate details.",
            "twist": "scale contrast",
            "twist_desc": "Massive/intimate scale juxtaposition"
        },
        {
            "template": "An abstract composition exploring {top_tag} themes through {top_palette} colors and {top_mood} energy — break symmetry with organic chaos.",
            "twist": "organic chaos",
            "twist_desc": "Asymmetric organic elements"
        },
        {
            "template": "A time-frozen moment in a {top_tag} environment, captured with {top_lighting} lighting and {top_palette} tones — layer in reflections or translucent materials.",
            "twist": "material transparency",
            "twist_desc": "Reflective and translucent layers"
        },
        {
            "template": "A {top_category}-inspired narrative scene bathed in {top_lighting}, using {top_palette} palette with {top_mood} undertones — introduce a hidden figure or symbolic object.",
            "twist": "hidden narrative",
            "twist_desc": "Symbolic objects or hidden figures"
        }
    ]
    
    # Shuffle for fresh order each generation
    random.shuffle(templates)
    
    suggestions = []
    for i in range(min(count, len(templates))):
        template_data = templates[i]
        
        # Generate prompt using team's DNA
        prompt = template_data["template"].format(
            top_tag=top_tag,
            top_palette=top_palette,
            top_mood=top_mood,
            top_lighting=top_lighting,
            top_category=top_category
        )
        
        # Determine suggested attributes with randomization for variety
        suggested_mood = top_mood
        suggested_palette = top_palette
        suggested_lighting = top_lighting
        suggested_camera = random.choice([top_camera, "wide angle", "close-up", "aerial view"])
        suggested_category = top_category
        
        # Add variety: randomly pick from top 3 patterns for fresh combinations
        if top_moods and random.random() > 0.5:
            suggested_mood = random.choice(top_moods)[0]
        if top_palettes and random.random() > 0.5:
            suggested_palette = random.choice(top_palettes)[0]
        if top_lighting_opts and random.random() > 0.3:
            suggested_lighting = random.choice(top_lighting_opts)[0]
        
        suggestions.append({
            "prompt": prompt,
            "mood": suggested_mood,
            "palette": suggested_palette,
            "lighting": suggested_lighting,
            "camera": suggested_camera,
            "category": suggested_category,
            "dna_match": "75%",  # High familiarity with creative twist
            "twist": template_data["twist_desc"]
        })
    
    return suggestions

@app.route("/studio/graphics/recommendations/<int:team_id>/prompts")
def team_recommendations(team_id):
    user_id = flask_session.get("user_id")
    
    # Redirect to login if not authenticated
    if not user_id:
        return redirect("/login")

    # Ensure user can view this team
    if not can_view_team(team_id, user_id):
        return "Access denied - You must be a team member to view recommendations", 403

    team = Team.query.get(team_id)
    projects = GraphicsProject.query.filter_by(team_id=team_id).all()
    user_role = get_user_role(team_id, user_id)

    # Aggregate style usage for team DNA summary
    mood_counts = {}
    palette_counts = {}
    lighting_counts = {}
    tag_counts = {}
    category_counts = {}

    for p in projects:
        if p.mood:
            mood_counts[p.mood] = mood_counts.get(p.mood, 0) + 1
        if p.color_palette:
            palette_counts[p.color_palette] = palette_counts.get(p.color_palette, 0) + 1
        if p.lighting:
            lighting_counts[p.lighting] = lighting_counts.get(p.lighting, 0) + 1
        if p.category:
            category_counts[p.category] = category_counts.get(p.category, 0) + 1
        if p.tags:
            for tag in p.tags.split(","):
                tag = tag.strip().lower()
                if tag:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1

    # Determine top 3 patterns for each dimension
    top_moods = sorted(mood_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    top_palettes = sorted(palette_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    top_lighting = sorted(lighting_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    top_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:3]

    # Generate AI prompt suggestions
    suggestions = generate_ai_prompt_suggestions(projects, count=5)
    
    # Log activity for requesting AI prompt suggestions
    log_activity(team_id, user_id, "requested AI prompt suggestions")

    return render_template(
        "team_recommendations.html",
        team=team,
        user_role=user_role,
        top_moods=top_moods,
        top_palettes=top_palettes,
        top_lighting=top_lighting,
        top_tags=top_tags,
        top_categories=top_categories,
        suggestions=suggestions,
        total_projects=len(projects)
    )


@app.route("/studio/graphics/project/<int:project_id>/evolve", methods=["POST"])
def evolve_project_prompt(project_id):
    """Generate evolved prompt variants for a project - the 'Refine this prompt' action."""
    user_id = flask_session.get("user_id")
    
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401
    
    project = GraphicsProject.query.get_or_404(project_id)
    
    # Check permissions
    if project.team_id:
        if not can_view_team(project.team_id, user_id):
            return jsonify({"error": "Access denied"}), 403
    elif project.user_id != user_id:
        return jsonify({"error": "Access denied"}), 403
    
    # Get evolution reason from request
    reason = request.json.get("reason", "refinement")  # refinement, exploration, remix
    count = request.json.get("count", 5)
    
    # Generate evolved variants
    variants = evolve_prompt(project.prompt, project, reason, count)
    
    # Log activity
    if project.team_id:
        log_activity(project.team_id, user_id, "evolved a prompt", {
            "project_id": project_id,
            "reason": reason,
            "variant_count": len(variants)
        })
    
    return jsonify({
        "success": True,
        "original_prompt": project.prompt,
        "variants": variants,
        "project_id": project_id
    })


@app.route("/studio/graphics/prompt/<int:prompt_id>/lineage")
def prompt_lineage(prompt_id):
    """Show the evolutionary lineage of a prompt - version tree."""
    user_id = flask_session.get("user_id")
    
    if not user_id:
        return redirect("/login")
    
    prompt = PromptHistory.query.get_or_404(prompt_id)
    
    # Check team access
    if not can_view_team(prompt.team_id, user_id):
        return "Access denied", 403
    
    # Build lineage tree (ancestors + descendants)
    ancestors = []
    current = prompt
    
    # Walk up the tree (parents)
    while current.parent_id:
        parent = PromptHistory.query.get(current.parent_id)
        if parent:
            ancestors.insert(0, parent)
            current = parent
        else:
            break
    
    # Walk down the tree (children)
    descendants = PromptHistory.query.filter_by(parent_id=prompt_id).order_by(
        PromptHistory.generation.asc()
    ).all()
    
    # Find projects using this prompt
    projects = GraphicsProject.query.filter_by(parent_prompt_id=prompt_id).order_by(
        GraphicsProject.timestamp.desc()
    ).all()
    
    team = Team.query.get(prompt.team_id)
    user_role = get_user_role(prompt.team_id, user_id)
    
    return render_template(
        "prompt_lineage.html",
        prompt=prompt,
        ancestors=ancestors,
        descendants=descendants,
        projects=projects,
        team=team,
        user_role=user_role
    )


@app.route("/studio/graphics/team/<int:team_id>/evolved-prompts")
def team_evolved_prompts(team_id):
    """Show team-level evolved prompts based on strongest collective work."""
    user_id = flask_session.get("user_id")
    
    if not user_id:
        return redirect("/login")
    
    if not can_view_team(team_id, user_id):
        return "Access denied", 403
    
    team = Team.query.get(team_id)
    user_role = get_user_role(team_id, user_id)
    
    # Get strongest prompts (top 10)
    strongest_prompts = get_team_strongest_prompts(team_id, limit=10)
    
    # Generate evolved variants for top 3 strongest
    evolved_sets = []
    for prompt in strongest_prompts[:3]:
        # Find a representative project using this prompt
        project = GraphicsProject.query.filter_by(parent_prompt_id=prompt.id).first()
        
        variants = evolve_prompt(prompt.prompt_text, project, "exploration", count=3)
        
        evolved_sets.append({
            "original_prompt": prompt,
            "effectiveness": calculate_prompt_effectiveness(prompt),
            "variants": variants,
            "times_used": prompt.times_used,
            "times_saved": prompt.times_saved
        })
    
    # Log activity
    log_activity(team_id, user_id, "viewed evolved prompts")
    
    return render_template(
        "team_evolved_prompts.html",
        team=team,
        user_role=user_role,
        strongest_prompts=strongest_prompts,
        evolved_sets=evolved_sets
    )


@app.route("/studio/graphics/team/<int:team_id>/universe")
def team_universe(team_id):
    user_id = flask_session.get("user_id")
    
    # Redirect to login if not authenticated
    if not user_id:
        return redirect("/login")

    # Ensure user can view this team
    if not can_view_team(team_id, user_id):
        return "Access denied - You must be a team member to view the universe", 403

    team = Team.query.get(team_id)
    projects = GraphicsProject.query.filter_by(team_id=team_id).all()

    # Aggregate tags with frequency
    tag_counts = {}
    for p in projects:
        if p.tags:
            for tag in p.tags.split(","):
                tag = tag.strip()
                if tag:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1

    # Normalize to size tiers (1-5)
    if tag_counts:
        max_count = max(tag_counts.values())
        tag_cloud = []
        for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
            if max_count == 1:
                size = 3
            else:
                size = int((count / max_count) * 4) + 1  # 1-5 scale
            tag_cloud.append({"tag": tag, "count": count, "size": size})
    else:
        tag_cloud = []

    # Aggregate categories with mood/palette dominance
    category_data = {}
    for p in projects:
        if p.category:
            cat = p.category
            if cat not in category_data:
                category_data[cat] = {
                    "count": 0,
                    "moods": {},
                    "palettes": {}
                }
            category_data[cat]["count"] += 1
            if p.mood:
                category_data[cat]["moods"][p.mood] = category_data[cat]["moods"].get(p.mood, 0) + 1
            if p.color_palette:
                category_data[cat]["palettes"][p.color_palette] = category_data[cat]["palettes"].get(p.color_palette, 0) + 1

    # Build category bubbles
    category_bubbles = []
    for cat, data in category_data.items():
        # Determine dominant mood/palette for color
        dominant_mood = max(data["moods"], key=data["moods"].get) if data["moods"] else None
        dominant_palette = max(data["palettes"], key=data["palettes"].get) if data["palettes"] else None
        
        category_bubbles.append({
            "name": cat,
            "count": data["count"],
            "size": min(data["count"] * 20 + 60, 200),  # Bubble size in pixels
            "mood": dominant_mood,
            "palette": dominant_palette
        })

    return render_template(
        "team_universe.html",
        team=team,
        tag_cloud=tag_cloud,
        category_bubbles=category_bubbles,
        total_projects=len(projects)
    )

@app.route("/studio/graphics/team/<int:team_id>/constellation")
def team_constellation(team_id):
    """Creative Constellation - Force-directed graph of team's creative universe."""
    user_id = flask_session.get("user_id")
    
    # Redirect to login if not authenticated
    if not user_id:
        return redirect("/login")

    # Ensure user can view this team
    if not can_view_team(team_id, user_id):
        return "Access denied - You must be a team member to view the constellation", 403

    team = Team.query.get(team_id)
    projects = GraphicsProject.query.filter_by(team_id=team_id).all()
    user_role = get_user_role(team_id, user_id)

    # Build graph data structure
    nodes = []
    edges = []
    node_ids = set()

    # Track tag and category frequencies for sizing
    tag_counts = {}
    category_counts = {}
    
    for p in projects:
        if p.tags:
            for tag in p.tags.split(","):
                tag = tag.strip().lower()
                if tag:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
        if p.category:
            category_counts[p.category] = category_counts.get(p.category, 0) + 1

    # Create tag nodes (glowing nodes based on frequency)
    max_tag_count = max(tag_counts.values()) if tag_counts else 1
    for tag, count in tag_counts.items():
        node_id = f"tag_{tag}"
        if node_id not in node_ids:
            node_ids.add(node_id)
            # Size based on frequency (5-20 range)
            size = 5 + (count / max_tag_count) * 15
            nodes.append({
                "id": node_id,
                "label": tag,
                "type": "tag",
                "count": count,
                "size": size,
                "color": "#f59e0b"  # Amber glow
            })

    # Create category nodes (larger orbiting clusters)
    max_category_count = max(category_counts.values()) if category_counts else 1
    for category, count in category_counts.items():
        node_id = f"category_{category}"
        if node_id not in node_ids:
            node_ids.add(node_id)
            # Larger size (20-40 range)
            size = 20 + (count / max_category_count) * 20
            nodes.append({
                "id": node_id,
                "label": category,
                "type": "category",
                "count": count,
                "size": size,
                "color": "#8b5cf6"  # Purple cluster
            })

    # Create project nodes (stars)
    for p in projects:
        node_id = f"project_{p.id}"
        if node_id not in node_ids:
            node_ids.add(node_id)
            
            # Truncate prompt for label
            label = p.prompt[:40] + "..." if p.prompt and len(p.prompt) > 40 else (p.prompt or f"Project {p.id}")
            
            # Color based on mood
            mood_colors = {
                "dramatic": "#dc2626",
                "serene": "#06b6d4",
                "vibrant": "#f59e0b",
                "mysterious": "#7c3aed",
                "ethereal": "#ec4899",
                "playful": "#10b981",
                "cinematic": "#3b82f6",
                "minimalist": "#6b7280",
                "nostalgic": "#f97316"
            }
            color = mood_colors.get(p.mood.lower() if p.mood else None, "#64748b")
            
            nodes.append({
                "id": node_id,
                "label": label,
                "type": "project",
                "projectId": p.id,
                "prompt": p.prompt,
                "mood": p.mood,
                "palette": p.color_palette,
                "category": p.category,
                "size": 8,  # Small stars
                "color": color
            })

            # Create edges: project → tags
            if p.tags:
                for tag in p.tags.split(","):
                    tag = tag.strip().lower()
                    if tag:
                        edges.append({
                            "source": node_id,
                            "target": f"tag_{tag}",
                            "strength": 0.5
                        })

            # Create edge: project → category
            if p.category:
                edges.append({
                    "source": node_id,
                    "target": f"category_{p.category}",
                    "strength": 0.7
                })

    # Build graph JSON
    graph_data = {
        "nodes": nodes,
        "edges": edges,
        "stats": {
            "totalProjects": len(projects),
            "totalTags": len(tag_counts),
            "totalCategories": len(category_counts)
        }
    }
    
    # Log activity for exploring the constellation
    log_activity(team_id, user_id, "explored the constellation map")

    return render_template(
        "team_constellation.html",
        team=team,
        user_role=user_role,
        graph_data=graph_data
    )

@app.route("/studio/graphics/team/<int:team_id>/activity")
def team_activity_feed(team_id):
    """Display team activity feed - chronological log of all team actions.
    
    Permissions:
    - Owners + Admins: See all activities
    - Editors + Viewers: See creative actions only (projects, tags, AI, constellation)
    """
    user_id = flask_session.get("user_id")
    
    # Redirect to login if not authenticated
    if not user_id:
        return redirect("/login")

    # Ensure user can view this team
    if not can_view_team(team_id, user_id):
        return "Access denied - You must be a team member to view the activity feed", 403

    team = Team.query.get(team_id)
    user_role = get_user_role(team_id, user_id)

    # Build base query
    query = db.session.query(TeamActivity, User).join(
        User, TeamActivity.user_id == User.id
    ).filter(
        TeamActivity.team_id == team_id
    )
    
    # Filter based on role - Editors and Viewers see creative actions only
    if user_role in ['editor', 'viewer']:
        # Show only creative actions: project creation, tag updates, AI prompts, constellation
        creative_actions = [
            'created a project',
            'updated tags',
            'requested AI prompt suggestions',
            'explored the constellation map'
        ]
        query = query.filter(TeamActivity.action.in_(creative_actions))
    
    # Owners and Admins see everything (no filter applied)
    
    # Get activities ordered by newest first
    activities = query.order_by(
        TeamActivity.timestamp.desc()
    ).limit(100).all()

    return render_template(
        "team_activity.html",
        team=team,
        user_role=user_role,
        activities=activities
    )

@app.route("/teams/<int:team_id>/manage")
def team_settings(team_id):
    user_id = flask_session.get("user_id")
    
    # Only admins and owners can access settings
    if not can_manage_members(team_id, user_id):
        return "Access denied - Admin or Owner role required", 403
    
    team = Team.query.get_or_404(team_id)
    user_role = get_user_role(team_id, user_id)
    
    # Get all team members with user details
    members = db.session.query(TeamMember, User).join(User, TeamMember.user_id == User.id).filter(TeamMember.team_id == team_id).all()
    
    # Get all users for invitation (exclude current members)
    current_member_ids = [m.user_id for m, u in members]
    available_users = User.query.filter(User.id.notin_(current_member_ids)).all()
    
    return render_template(
        "team_settings.html",
        team=team,
        members=members,
        available_users=available_users,
        user_role=user_role
    )

@app.route("/studio/graphics/team/<int:team_id>/members/add", methods=["POST"])
def add_team_member(team_id):
    user_id = flask_session.get("user_id")
    
    if not can_manage_members(team_id, user_id):
        return "Access denied", 403
    
    new_user_id = request.form.get("user_id")
    role = request.form.get("role", "viewer")
    
    # Validate role
    if role not in ["owner", "admin", "editor", "viewer"]:
        return "Invalid role", 400
    
    # Only owner can add other owners
    if role == "owner" and not can_delete_team(team_id, user_id):
        return "Only owner can promote to owner", 403
    
    # Check if already a member
    existing = TeamMember.query.filter_by(team_id=team_id, user_id=new_user_id).first()
    if existing:
        return "User already a member", 400
    
    # Add member
    member = TeamMember(team_id=team_id, user_id=new_user_id, role=role)
    db.session.add(member)
    db.session.commit()
    
    # Log activity for the new member joining
    log_activity(team_id, new_user_id, "joined the team")
    
    return redirect(f"/teams/{team_id}/manage")

@app.route("/teams/<int:team_id>/set_role", methods=["POST"])
def set_role(team_id):
    user_id = flask_session.get("user_id")
    
    if not is_admin(user_id, team_id):
        return "Access denied", 403

    member_id = request.form.get("member_id")
    new_role = request.form.get("role")
    
    # Validate role
    if new_role not in ["owner", "admin", "editor", "viewer"]:
        return "Invalid role", 400
    
    # Check permission to change to this role
    if not can_change_role(team_id, user_id, new_role):
        return "Cannot change to this role", 403
    
    member = TeamMember.query.filter_by(team_id=team_id, user_id=member_id).first()
    if not member:
        return "Member not found", 404
    
    # Cannot change own role (prevents accidental lockout)
    if int(member_id) == user_id:
        return "Cannot change your own role", 400
    
    # Cannot demote the owner unless you are the owner
    if member.role == "owner" and not can_delete_team(team_id, user_id):
        return "Cannot change owner role", 403

    member.role = new_role
    db.session.commit()
    
    # Log role change activity
    log_activity(team_id, user_id, "changed role", {"member_id": member_id, "new_role": new_role})

    return redirect(f"/teams/{team_id}/manage")

@app.route("/studio/graphics/team/<int:team_id>/members/<int:member_id>/remove", methods=["POST"])
def remove_team_member(team_id, member_id):
    user_id = flask_session.get("user_id")
    
    if not can_manage_members(team_id, user_id):
        return "Access denied", 403
    
    member = TeamMember.query.get_or_404(member_id)
    
    # Cannot remove yourself
    if member.user_id == user_id:
        return "Cannot remove yourself", 400
    
    # Cannot remove owner (must transfer ownership first)
    if member.role == "owner":
        return "Cannot remove owner - transfer ownership first", 400
    
    db.session.delete(member)
    db.session.commit()
    
    return redirect(f"/teams/{team_id}/manage")

@app.route("/studio/graphics/project/<int:project_id>/edit", methods=["GET", "POST"])
def edit_graphics_project(project_id):
    user_id = flask_session.get("user_id")
    project = GraphicsProject.query.get_or_404(project_id)
    
    # Check permission to edit this project
    if project.team_id:
        if not can_edit_project(project_id, user_id, project.team_id):
            return "Access denied - You don't have permission to edit this project", 403
    else:
        # Personal project - only owner can edit
        if project.user_id != user_id:
            return "Access denied", 403
    
    # GET request - track reopening activity
    if request.method == "GET":
        if project.team_id and project.parent_prompt_id:
            # Update prompt history - project reopened
            prompt_hist = PromptHistory.query.get(project.parent_prompt_id)
            if prompt_hist:
                prompt_hist.times_used += 1
                prompt_hist.avg_engagement += 0.5  # Increment engagement
                prompt_hist.effectiveness_score = calculate_prompt_effectiveness(prompt_hist)
                db.session.commit()
            
            # Log activity
            log_activity(project.team_id, user_id, "reopened a project", {
                "project_id": project_id,
                "usage_signal": "reopened"
            })
        
        return render_template("edit_project.html", project=project)
    
    # POST request - save edits
    if request.method == "POST":
        # Track old tags for activity logging
        old_tags = project.tags
        
        # Update project fields
        project.prompt = request.form.get("prompt")
        project.aspect_ratio = request.form.get("aspect_ratio")
        project.color_palette = request.form.get("color_palette")
        project.mood = request.form.get("mood")
        project.lighting = request.form.get("lighting")
        project.camera_angle = request.form.get("camera_angle")
        project.tags = request.form.get("tags")
        project.category = request.form.get("category")
        
        db.session.commit()
        
        # Log activity if tags changed and this is a team project
        if project.team_id and old_tags != project.tags:
            log_activity(project.team_id, user_id, "updated tags", {"tags": project.tags})
        
        # Redirect back to appropriate library
        if project.team_id:
            return redirect(f"/studio/graphics/team/{project.team_id}")
        else:
            return redirect("/studio/graphics/library")

@app.route("/studio/graphics/project/<int:project_id>/delete", methods=["POST"])
def delete_graphics_project(project_id):
    user_id = flask_session.get("user_id")
    project = GraphicsProject.query.get_or_404(project_id)
    
    # Check permission to delete this project
    if project.team_id:
        if not can_delete_project(project.team_id, user_id):
            return "Access denied - Only Admin or Owner can delete team projects", 403
    else:
        # Personal project - only owner can delete
        if project.user_id != user_id:
            return "Access denied", 403
    
    team_id = project.team_id
    db.session.delete(project)
    db.session.commit()
    
    # Redirect back to appropriate library
    if team_id:
        return redirect(f"/studio/graphics/team/{team_id}")
    else:
        return redirect("/studio/graphics/library")


@app.route("/studio/graphics/project/<int:project_id>/clone", methods=["POST"])
def clone_graphics_project(project_id):
    """Clone/remix a project - tracks prompt reuse and creates lineage."""
    user_id = flask_session.get("user_id")
    original = GraphicsProject.query.get_or_404(project_id)
    
    # Check permission to view original project
    if original.team_id:
        if not can_view_team(original.team_id, user_id):
            return jsonify({"error": "Access denied"}), 403
    elif original.user_id != user_id:
        return jsonify({"error": "Access denied"}), 403
    
    # Create cloned project with lineage tracking
    cloned = GraphicsProject(
        prompt=original.prompt,
        aspect_ratio=original.aspect_ratio,
        color_palette=original.color_palette,
        mood=original.mood,
        lighting=original.lighting,
        camera_angle=original.camera_angle,
        tags=original.tags,
        category=original.category,
        user_id=user_id,
        team_id=original.team_id,
        parent_prompt_id=original.parent_prompt_id,
        prompt_source="remixed",
        original_prompt=original.original_prompt,
        prompt_version=(original.prompt_version or 1) + 1,
        parent_project_id=original.id,
        was_prompt_reused=True
    )
    
    db.session.add(cloned)
    db.session.commit()
    
    # Update prompt history - track reuse
    if original.parent_prompt_id:
        prompt_hist = PromptHistory.query.get(original.parent_prompt_id)
        if prompt_hist:
            prompt_hist.times_reused += 1
            prompt_hist.effectiveness_score = calculate_prompt_effectiveness(prompt_hist)
            db.session.commit()
    
    # Log activity
    if original.team_id:
        log_activity(original.team_id, user_id, "cloned a project", {
            "original_project_id": project_id,
            "cloned_project_id": cloned.id,
            "usage_signal": "cloned"
        })
    
    return jsonify({
        "success": True,
        "cloned_project_id": cloned.id,
        "message": "Project cloned successfully!"
    })


@app.route("/teams/<int:team_id>/delete", methods=["POST"])
def delete_team(team_id):
    user_id = flask_session.get("user_id")
    
    # Only owner can delete team
    if not can_delete_team(team_id, user_id):
        return "Access denied - Only the team Owner can delete the team", 403
    
    team = Team.query.get_or_404(team_id)
    
    # Delete all team members
    TeamMember.query.filter_by(team_id=team_id).delete()
    
    # Optionally: Delete all team projects or reassign to personal
    # For now, let's reassign projects to creator's personal library
    projects = GraphicsProject.query.filter_by(team_id=team_id).all()
    for project in projects:
        project.team_id = None
    
    # Delete the team
    db.session.delete(team)
    db.session.commit()
    
    return redirect("/teams")

@app.route("/studio/graphics/analytics")
def graphics_analytics():
    user_id = flask_session.get("user_id")

    projects = GraphicsProject.query.filter_by(user_id=user_id).all()

    # Count usage
    mood_counts = {}
    palette_counts = {}
    lighting_counts = {}

    for p in projects:
        mood_counts[p.mood] = mood_counts.get(p.mood, 0) + 1
        palette_counts[p.color_palette] = palette_counts.get(p.color_palette, 0) + 1
        lighting_counts[p.lighting] = lighting_counts.get(p.lighting, 0) + 1

    return render_template(
        "graphics_analytics.html",
        mood_counts=mood_counts,
        palette_counts=palette_counts,
        lighting_counts=lighting_counts
    )

@app.route("/studio/graphics/open", methods=["POST"])
def open_graphics_project():
    project_id = request.form.get("project_id")
    project = GraphicsProject.query.get(project_id)

    return render_template(
        "graphics_studio.html",
        prompt=project.prompt,
        aspect_ratio=project.aspect_ratio,
        color_palette=project.color_palette,
        mood=project.mood,
        lighting=project.lighting,
        camera_angle=project.camera_angle,
        generated_images=[],
        loaded=True
    )

@app.route('/studio/audio')
def audio_studio():
    """Audio Studio - AI Voice & Music Generation"""
    return render_template('audio_studio.html')

@app.route('/api/graphics/generate', methods=['POST'])
def generate_graphics():
    """API endpoint for AI image generation"""
    try:
        prompt = request.json.get('prompt')
        
        # TODO: Connect to DALL-E, Midjourney, Stable Diffusion, etc.
        # For now, return a placeholder response
        
        return jsonify({
            'status': 'success',
            'message': 'Image generation endpoint ready',
            'prompt': prompt,
            'images': []  # Will contain image URLs once AI is connected
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/automation-calculator')
def automation_calculator():
    """Automation Savings Calculator page"""
    return render_template_string(AUTOMATION_CALCULATOR_HTML)

@app.route('/api/automation/calculate', methods=['POST'])
def calculate_automation_roi():
    """API endpoint to calculate automation ROI using calculators module"""
    try:
        data = request.get_json()
        
        # Create input object
        savings_input = SavingsInput(
            tasks_per_week=float(data.get('tasks_per_week', 0)),
            time_per_task_minutes=float(data.get('time_per_task_minutes', 0)),
            hourly_wage=float(data.get('hourly_wage', 0)),
            automation_percent=float(data.get('automation_percent', 0)) / 100,
            error_rate=float(data.get('error_rate', 0)) / 100,
            cost_per_error=float(data.get('error_cost', 0)),
            value_per_accelerated_task=float(data.get('value_per_task', 0))
        )
        
        # Calculate using the new module
        result = calculate_savings(savings_input)
        effectiveness = get_effectiveness_rating(result.yearly_savings)
        
        return jsonify({
            'success': True,
            'savings': {
                'weekly': result.weekly_savings,
                'monthly': result.monthly_savings,
                'yearly': result.yearly_savings,
                'hours_saved_per_week': result.hours_saved_per_week,
                'error_reduction_percent': round(savings_input.automation_percent * 100),
                'effectiveness': effectiveness,
                'breakdown': {
                    'labor_savings': result.weekly_savings - result.error_savings_weekly - result.scaling_savings_weekly,
                    'error_savings': result.error_savings_weekly,
                    'scaling_savings': result.scaling_savings_weekly
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/automation/activate', methods=['POST'])
def activate_automation():
    """API endpoint to activate an automation workflow"""
    try:
        data = request.get_json()
        
        # Load ledger
        ledger = load_json('codex_ledger.json', use_cache=False)
        
        # Initialize workflows array if it doesn't exist
        if 'workflows' not in ledger:
            ledger['workflows'] = []
        
        # Generate workflow ID
        workflow_id = f"WF-{len(ledger['workflows']) + 1:03d}"
        
        # Create workflow entry
        workflow = {
            'id': workflow_id,
            'name': data.get('workflow_name', 'Unnamed Automation'),
            'action_type': 'automation',
            'status': 'active',
            'requested_by': 'automation_calculator',
            'created_at': datetime.utcnow().isoformat() + 'Z',
            'inputs': data.get('inputs', {}),
            'roi_metrics': {
                'weekly_savings': f"${data['savings']['weekly']:.2f}",
                'monthly_savings': f"${data['savings']['monthly']:.2f}",
                'yearly_savings': f"${data['savings']['yearly']:.2f}",
                'weekly_savings_raw': data['savings']['weekly'],
                'monthly_savings_raw': data['savings']['monthly'],
                'yearly_savings_raw': data['savings']['yearly'],
                'hours_saved_per_week': data['savings']['hours_saved_per_week'],
                'error_reduction_percent': data['savings'].get('error_reduction_percent', 0),
                'automation_effectiveness': 'HIGH' if data['savings']['yearly'] > 10000 else 'MEDIUM'
            },
            'implementation': {
                'phase': 'activated',
                'monitoring_enabled': True,
                'last_execution': None,
                'next_execution': None
            },
            'flame_seal': f"🔥 Automation Sovereign - {data['savings']['hours_saved_per_week']:.1f} Hours Reclaimed Weekly 🔥"
        }
        
        # Add to ledger
        ledger['workflows'].append(workflow)
        
        # Update timestamp
        ledger['meta']['last_updated'] = datetime.utcnow().isoformat() + 'Z'
        
        # Save ledger
        ledger_path = os.path.join(BASE_DIR, 'codex_ledger.json')
        with open(ledger_path, 'w', encoding='utf-8') as f:
            json.dump(ledger, f, indent=2)
        
        # Clear cache
        clear_json_cache()
        
        return jsonify({
            'success': True,
            'workflow_id': workflow_id,
            'message': f'Automation {workflow_id} activated successfully! 🔥'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/social')
def social():
    """Social Media Management page"""
    social_html = """
    <!DOCTYPE html>
    <html>
    <head><title>📱 Social Media Management</title>
    <style>
        body { font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; }
        h1 { color: #667eea; }
        .platform { background: #f5f5f5; padding: 20px; margin: 15px 0; border-radius: 10px; }
        .btn { background: #667eea; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        .nav { margin: 20px 0; }
        .nav a { color: #667eea; text-decoration: none; margin-right: 15px; }
    </style>
    </head>
    <body>
        <div class="container">
            <div class="nav"><a href="/">← Back to Home</a></div>
            <h1>📱 Social Media Management</h1>
            <p>Manage all your social media platforms from one place.</p>

            <div class="platform">
                <h2>🎥 YouTube</h2>
                <p>Status: ✅ Connected</p>
                <p>Subscribers: 1,234 | Videos: 56 | Views: 45.6K</p>
                <button class="btn">Upload Video</button>
                <button class="btn">View Analytics</button>
            </div>

            <div class="platform">
                <h2>📸 Instagram</h2>
                <p>Status: ✅ Connected</p>
                <p>Followers: 5,678 | Posts: 234 | Engagement: 4.2%</p>
                <button class="btn">Create Post</button>
                <button class="btn">View Insights</button>
            </div>

            <div class="platform">
                <h2>🎵 TikTok</h2>
                <p>Status: ✅ Connected</p>
                <p>Followers: 12.3K | Videos: 145 | Likes: 234K</p>
                <button class="btn">Upload Video</button>
                <button class="btn">View Analytics</button>
            </div>

            <div class="platform">
                <h2>👔 LinkedIn</h2>
                <p>Status: ✅ Connected</p>
                <p>Connections: 3,456 | Posts: 89 | Impressions: 67K</p>
                <button class="btn">Create Post</button>
                <button class="btn">View Stats</button>
            </div>

            <div class="platform">
                <h2>📌 Pinterest</h2>
                <p>Status: ✅ Connected</p>
                <p>Followers: 2,345 | Pins: 567 | Monthly Views: 123K</p>
                <button class="btn">Create Pin</button>
                <button class="btn">View Analytics</button>
            </div>

            <div class="platform">
                <h2>👥 Facebook</h2>
                <p>Status: ✅ Connected</p>
                <p>Friends: 4,892 | Page Likes: 8,234 | Reach: 156K</p>
                <button class="btn">Create Post</button>
                <button class="btn">Manage Pages</button>
                <button class="btn">View Insights</button>
            </div>

            <div class="platform">
                <h2>🧵 Threads</h2>
                <p>Status: ✅ Connected</p>
                <p>Followers: 3,567 | Posts: 189 | Engagement: 5.8%</p>
                <button class="btn">Create Thread</button>
                <button class="btn">View Analytics</button>
            </div>
        </div>
    </body>
    </html>
    """
    return social_html

@app.route('/affiliate')
def affiliate():
    """Affiliate Marketing page"""
    affiliate_html = """
    <!DOCTYPE html>
    <html>
    <head><title>💰 Affiliate Marketing</title>
    <style>
        body { font-family: Arial; background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%); padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; }
        h1 { color: #ff6b35; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .stat { background: #f5f5f5; padding: 20px; border-radius: 10px; text-align: center; }
        .stat h3 { color: #667eea; margin-bottom: 10px; }
        .stat p { font-size: 2em; font-weight: bold; color: #ff6b35; }
        .program { background: #f9f9f9; padding: 20px; margin: 15px 0; border-radius: 10px; border-left: 4px solid #667eea; }
        .nav { margin: 20px 0; }
        .nav a { color: #667eea; text-decoration: none; margin-right: 15px; }
    </style>
    </head>
    <body>
        <div class="container">
            <div class="nav"><a href="/">← Back to Home</a></div>
            <h1>💰 Affiliate Marketing Dashboard</h1>
            <p>Track your affiliate programs and earnings.</p>

            <div class="stats">
                <div class="stat">
                    <h3>Total Revenue</h3>
                    <p>$12,345</p>
                </div>
                <div class="stat">
                    <h3>Active Programs</h3>
                    <p>8</p>
                </div>
                <div class="stat">
                    <h3>Clicks Today</h3>
                    <p>234</p>
                </div>
                <div class="stat">
                    <h3>Conversions</h3>
                    <p>45</p>
                </div>
            </div>

            <h2>Active Programs</h2>
            <div class="program">
                <h3>Amazon Associates</h3>
                <p>Revenue: $4,567 | Clicks: 1,234 | Conversion Rate: 3.2%</p>
                <p>Status: ✅ Active</p>
            </div>

            <div class="program">
                <h3>ShareASale</h3>
                <p>Revenue: $3,456 | Clicks: 987 | Conversion Rate: 4.1%</p>
                <p>Status: ✅ Active</p>
            </div>

            <div class="program">
                <h3>CJ Affiliate</h3>
                <p>Revenue: $2,345 | Clicks: 756 | Conversion Rate: 3.8%</p>
                <p>Status: ✅ Active</p>
            </div>
        </div>
    </body>
    </html>
    """
    return affiliate_html

@app.route('/chatbot')
def chatbot():
    """Action Chatbot page"""
    chatbot_html = """
    <!DOCTYPE html>
    <html>
    <head><title>🤖 Action Chatbot</title>
    <style>
        body { font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; }
        h1 { color: #667eea; }
        .chat-interface { background: #f5f5f5; padding: 30px; border-radius: 10px; margin: 20px 0; min-height: 400px; }
        .message { background: white; padding: 15px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .user-message { background: #667eea; color: white; text-align: right; }
        .input-area { display: flex; gap: 10px; margin-top: 20px; }
        input { flex: 1; padding: 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; }
        button { background: #667eea; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; }
        .nav { margin: 20px 0; }
        .nav a { color: #667eea; text-decoration: none; margin-right: 15px; }
    </style>
    </head>
    <body>
        <div class="container">
            <div class="nav"><a href="/">← Back to Home</a></div>
            <h1>🤖 Action Chatbot</h1>
            <p>AI-powered chatbot for customer interactions and automation.</p>

            <div class="chat-interface">
                <div class="message">
                    <strong>Bot:</strong> Welcome to Action Chatbot! How can I assist you today?
                </div>
                <div class="message user-message">
                    <strong>You:</strong> Hello! I need help with social media scheduling.
                </div>
                <div class="message">
                    <strong>Bot:</strong> I can help you schedule posts across multiple platforms. Which platform would you like to start with?
                </div>
            </div>

            <div class="input-area">
                <input type="text" placeholder="Type your message here..." />
                <button>Send</button>
            </div>

            <h2>🚀 Quick Actions</h2>
            <p>• Schedule social media posts</p>
            <p>• Generate content ideas</p>
            <p>• Analyze engagement metrics</p>
            <p>• Automate customer responses</p>
            <p>• Create marketing campaigns</p>
        </div>
    </body>
    </html>
    """
    return chatbot_html

@app.route('/algorithm')
def algorithm():
    """Algorithm AI page"""
    algorithm_html = """
    <!DOCTYPE html>
    <html>
    <head><title>🧠 Algorithm AI</title>
    <style>
        body { font-family: Arial; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; }
        h1 { color: #4facfe; }
        .algorithm { background: #f5f5f5; padding: 20px; margin: 15px 0; border-radius: 10px; border-left: 4px solid #4facfe; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .metric { background: #f9f9f9; padding: 20px; border-radius: 10px; text-align: center; }
        .btn { background: #4facfe; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .nav { margin: 20px 0; }
        .nav a { color: #4facfe; text-decoration: none; margin-right: 15px; }
    </style>
    </head>
    <body>
        <div class="container">
            <div class="nav"><a href="/">← Back to Home</a></div>
            <h1>🧠 Algorithm AI</h1>
            <p>Advanced AI algorithms for optimization and decision making.</p>

            <div class="metrics">
                <div class="metric">
                    <h3>Models Running</h3>
                    <p style="font-size: 2em; color: #4facfe;">12</p>
                </div>
                <div class="metric">
                    <h3>Predictions/Day</h3>
                    <p style="font-size: 2em; color: #4facfe;">45.6K</p>
                </div>
                <div class="metric">
                    <h3>Accuracy</h3>
                    <p style="font-size: 2em; color: #4facfe;">98.5%</p>
                </div>
                <div class="metric">
                    <h3>Processing Time</h3>
                    <p style="font-size: 2em; color: #4facfe;">0.3s</p>
                </div>
            </div>

            <h2>Active Algorithms</h2>
            <div class="algorithm">
                <h3>Content Optimization Algorithm</h3>
                <p>Analyzes and optimizes content for maximum engagement</p>
                <p>Status: ✅ Running | Last Updated: 5 min ago</p>
                <button class="btn">View Details</button>
                <button class="btn">Run Analysis</button>
            </div>

            <div class="algorithm">
                <h3>Revenue Prediction Model</h3>
                <p>Predicts revenue trends based on historical data and market conditions</p>
                <p>Status: ✅ Running | Last Updated: 10 min ago</p>
                <button class="btn">View Details</button>
                <button class="btn">Generate Report</button>
            </div>

            <div class="algorithm">
                <h3>Customer Behavior Analysis</h3>
                <p>Tracks and predicts customer behavior patterns</p>
                <p>Status: ✅ Running | Last Updated: 2 min ago</p>
                <button class="btn">View Details</button>
                <button class="btn">Export Data</button>
            </div>

            <div class="algorithm">
                <h3>Social Media Engagement Optimizer</h3>
                <p>Optimizes posting times and content for maximum reach</p>
                <p>Status: ✅ Running | Last Updated: 1 min ago</p>
                <button class="btn">View Details</button>
                <button class="btn">Get Recommendations</button>
            </div>
        </div>
    </body>
    </html>
    """
    return algorithm_html

@app.route('/autopublish')
def autopublish():
    """Auto-Publish page"""
    autopublish_html = """
    <!DOCTYPE html>
    <html>
    <head><title>🚀 Auto-Publish</title>
    <style>
        body { font-family: Arial; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; }
        h1 { color: #f5576c; }
        .schedule { background: #f5f5f5; padding: 20px; margin: 15px 0; border-radius: 10px; }
        .platform-badge { display: inline-block; background: #667eea; color: white; padding: 5px 15px; border-radius: 15px; margin: 5px; }
        .btn { background: #f5576c; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .stat { background: #f9f9f9; padding: 20px; border-radius: 10px; text-align: center; }
        .nav { margin: 20px 0; }
        .nav a { color: #f5576c; text-decoration: none; margin-right: 15px; }
    </style>
    </head>
    <body>
        <div class="container">
            <div class="nav"><a href="/">← Back to Home</a></div>
            <h1>🚀 Auto-Publish System</h1>
            <p>Automated content publishing across all platforms.</p>

            <div class="stats">
                <div class="stat">
                    <h3>Scheduled Posts</h3>
                    <p style="font-size: 2em; color: #f5576c;">47</p>
                </div>
                <div class="stat">
                    <h3>Published Today</h3>
                    <p style="font-size: 2em; color: #f5576c;">12</p>
                </div>
                <div class="stat">
                    <h3>Success Rate</h3>
                    <p style="font-size: 2em; color: #f5576c;">99.2%</p>
                </div>
                <div class="stat">
                    <h3>Active Campaigns</h3>
                    <p style="font-size: 2em; color: #f5576c;">8</p>
                </div>
            </div>

            <h2>Upcoming Publications</h2>
            <div class="schedule">
                <h3>Product Launch Campaign</h3>
                <p><strong>Scheduled:</strong> Today at 2:00 PM EST</p>
                <span class="platform-badge">YouTube</span>
                <span class="platform-badge">Instagram</span>
                <span class="platform-badge">TikTok</span>
                <span class="platform-badge">LinkedIn</span>
                <p>Content: New product announcement video with promotional offer</p>
                <button class="btn">Edit</button>
                <button class="btn">Publish Now</button>
                <button class="btn">Cancel</button>
            </div>

            <div class="schedule">
                <h3>Weekly Newsletter</h3>
                <p><strong>Scheduled:</strong> Tomorrow at 9:00 AM EST</p>
                <span class="platform-badge">Email</span>
                <span class="platform-badge">LinkedIn</span>
                <p>Content: Weekly industry insights and tips</p>
                <button class="btn">Edit</button>
                <button class="btn">Publish Now</button>
                <button class="btn">Cancel</button>
            </div>

            <div class="schedule">
                <h3>Social Media Tips Series</h3>
                <p><strong>Scheduled:</strong> Dec 18 at 11:00 AM EST</p>
                <span class="platform-badge">Instagram</span>
                <span class="platform-badge">Pinterest</span>
                <span class="platform-badge">Facebook</span>
                <p>Content: 10 tips for growing your social media presence</p>
                <button class="btn">Edit</button>
                <button class="btn">Publish Now</button>
                <button class="btn">Cancel</button>
            </div>

            <h2>🎯 Quick Actions</h2>
            <button class="btn">Schedule New Post</button>
            <button class="btn">Create Campaign</button>
            <button class="btn">View Analytics</button>
            <button class="btn">Manage Templates</button>
        </div>
    </body>
    </html>
    """
    return autopublish_html

@app.route('/websites')
def websites():
    """Websites Management page"""
    websites_html = """
    <!DOCTYPE html>
    <html>
    <head><title>🌐 Websites Management</title>
    <style>
        body { font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; }
        h1 { color: #667eea; }
        .website { background: #f5f5f5; padding: 20px; margin: 15px 0; border-radius: 10px; }
        .btn { background: #667eea; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .status { display: inline-block; padding: 5px 15px; border-radius: 15px; margin: 5px; }
        .status.online { background: #4caf50; color: white; }
        .nav { margin: 20px 0; }
        .nav a { color: #667eea; text-decoration: none; margin-right: 15px; }
    </style>
    </head>
    <body>
        <div class="container">
            <div class="nav"><a href="/">← Back to Home</a></div>
            <h1>🌐 Websites Management</h1>
            <p>Manage all your websites and domains.</p>

            <div class="website">
                <h3>CodexDominion Main Site</h3>
                <p><strong>URL:</strong> https://witty-glacier-0ebbd971e.3.azurestaticapps.net</p>
                <span class="status online">✅ Online</span>
                <p>Type: Azure Static Web App | SSL: ✅ Active | Uptime: 99.9%</p>
                <button class="btn">View Site</button>
                <button class="btn">Analytics</button>
                <button class="btn">Settings</button>
            </div>

            <div class="website">
                <h3>Backend API</h3>
                <p><strong>URL:</strong> http://codex-api.eastus2.azurecontainer.io:8000</p>
                <span class="status online">✅ Online</span>
                <p>Type: Azure Container Instance | Health: ✅ Healthy | Response Time: 0.3s</p>
                <button class="btn">API Docs</button>
                <button class="btn">Monitor</button>
                <button class="btn">Logs</button>
            </div>

            <button class="btn">Add New Website</button>
        </div>
    </body>
    </html>
    """
    return websites_html

@app.route('/stores')
def stores():
    """E-Commerce Stores page"""
    stores_html = """
    <!DOCTYPE html>
    <html>
    <head><title>🛒 E-Commerce Stores</title>
    <style>
        body { font-family: Arial; background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%); padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; }
        h1 { color: #ff6b35; }
        .store { background: #f5f5f5; padding: 20px; margin: 15px 0; border-radius: 10px; }
        .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 15px 0; }
        .stat { background: white; padding: 15px; border-radius: 8px; text-align: center; }
        .btn { background: #ff6b35; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .nav { margin: 20px 0; }
        .nav a { color: #ff6b35; text-decoration: none; margin-right: 15px; }
    </style>
    </head>
    <body>
        <div class="container">
            <div class="nav"><a href="/">← Back to Home</a></div>
            <h1>🛒 E-Commerce Stores</h1>
            <p>Manage your online stores and products.</p>

            <div class="store">
                <h3>WooCommerce Store</h3>
                <p><strong>Status:</strong> ✅ Active</p>
                <div class="stats">
                    <div class="stat">
                        <p><strong>Orders Today</strong></p>
                        <p style="font-size: 2em; color: #ff6b35;">23</p>
                    </div>
                    <div class="stat">
                        <p><strong>Revenue</strong></p>
                        <p style="font-size: 2em; color: #ff6b35;">$2,345</p>
                    </div>
                    <div class="stat">
                        <p><strong>Products</strong></p>
                        <p style="font-size: 2em; color: #ff6b35;">156</p>
                    </div>
                </div>
                <button class="btn">View Orders</button>
                <button class="btn">Manage Products</button>
                <button class="btn">Settings</button>
            </div>

            <button class="btn">Add New Store</button>
            <button class="btn">Sync Inventory</button>
        </div>
    </body>
    </html>
    """
    return stores_html

@app.route('/revenue')
def revenue():
    """Revenue & Treasury Dashboard"""
    # Load revenue and treasury data
    revenue_data = load_json("revenue_streams.json")
    treasury_data = load_json("treasury.json")
    treasury_config = load_json("treasury_config.json")
    
    # Extract metrics
    revenue_streams = revenue_data.get("revenue_streams", [])
    consolidated = revenue_data.get("consolidated_metrics", {})
    sovereignty = revenue_data.get("sovereignty_assessment", {})
    
    total_monthly_target = consolidated.get("combined_monthly_target", 4500.0)
    total_current_month = consolidated.get("combined_current_month", 650.0)
    total_all_time = consolidated.get("combined_all_time_total", 9550.0)
    avg_growth = consolidated.get("avg_growth_rate", 15.5)
    
    # Calculate progress percentage
    progress_pct = round((total_current_month / total_monthly_target * 100) if total_monthly_target > 0 else 0, 1)
    
    # Prepare chart data
    stream_labels = [s.get('name', 'Unknown') for s in revenue_streams]
    stream_current = [s.get('current_month_total', 0) for s in revenue_streams]
    stream_targets = [s.get('monthly_target', 0) for s in revenue_streams]
    stream_growth = [s.get('growth_rate', 0) for s in revenue_streams]
    
    revenue_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>💰 Revenue & Treasury Dashboard</title>
        <script src="https://cdn.jsdelivr.net.com/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
        <style>
        body {{ 
            font-family: 'Segoe UI', Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 20px; 
            margin: 0;
            transition: all 0.3s ease;
        }}
        body.dark-mode {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        }}
        .container {{ 
            max-width: 1400px; 
            margin: 0 auto; 
            background: white; 
            padding: 40px; 
            border-radius: 15px; 
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }}
        .dark-mode .container {{
            background: #1e1e2e;
            color: #e0e0e0;
        }}
        .dark-mode h1, .dark-mode h2, .dark-mode h3 {{
            color: #a78bfa !important;
        }}
        .dark-mode .metric-card {{
            background: #2a2a3e;
            border-color: #3a3a4e;
        }}
        .dark-mode .stream-card {{
            background: #2a2a3e;
            border-color: #3a3a4e;
        }}
        .dark-mode .chart-container {{
            background: #2a2a3e;
        }}
        .dark-mode-toggle {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: rgba(102, 126, 234, 0.9);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }}
        .dark-mode-toggle:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.4);
        }}
        .dark-mode .dark-mode-toggle {{
            background: rgba(167, 139, 250, 0.9);
        }}
        h1 {{ 
            color: #667eea; 
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        .subtitle {{
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }}
        .chart-container {{
            position: relative;
            height: 400px;
            margin: 30px 0;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 12px;
        }}
        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin: 30px 0;
        }}
        .nav-tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            flex-wrap: wrap;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 15px;
        }}
        .nav-tab {{
            padding: 12px 24px;
            background: #f5f5f5;
            color: #333;
            text-decoration: none;
            border-radius: 8px 8px 0 0;
            font-weight: 600;
            transition: all 0.3s;
        }}
        .nav-tab:hover {{
            background: #667eea;
            color: white;
            transform: translateY(-2px);
        }}
        .nav-tab.active {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .metric-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        .metric-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }}
        .metric-label {{
            color: #555;
            font-size: 1em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .metric-change {{
            color: #10b981;
            font-size: 1.1em;
            margin-top: 8px;
            font-weight: 600;
        }}
        .streams-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            margin: 30px 0;
        }}
        .stream-card {{
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            transition: all 0.3s;
        }}
        .stream-card:hover {{
            border-color: #667eea;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        }}
        .stream-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }}
        .stream-title {{
            font-size: 1.4em;
            font-weight: bold;
            color: #333;
        }}
        .stream-status {{
            background: #10b981;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            text-transform: uppercase;
        }}
        .stream-metrics {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin: 20px 0;
        }}
        .stream-metric {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }}
        .stream-metric-value {{
            font-size: 1.8em;
            font-weight: bold;
            color: #667eea;
        }}
        .stream-metric-label {{
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        .progress-bar {{
            background: #e0e0e0;
            height: 20px;
            border-radius: 10px;
            overflow: hidden;
            margin: 20px 0;
        }}
        .progress-fill {{
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            height: 100%;
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 0.85em;
        }}
        .sovereignty-badge {{
            display: inline-block;
            background: #fbbf24;
            color: #92400e;
            padding: 8px 20px;
            border-radius: 25px;
            font-weight: bold;
            margin: 10px 0;
        }}
        .recommendations {{
            background: #fef3c7;
            border-left: 4px solid #fbbf24;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .recommendations h3 {{
            color: #92400e;
            margin-bottom: 15px;
        }}
        .recommendations ul {{
            list-style: none;
            padding: 0;
        }}
        .recommendations li {{
            padding: 8px 0;
            color: #78350f;
        }}
        .recommendations li:before {{
            content: "🔥 ";
            margin-right: 10px;
        }}
    </style>
    </head>
    <body>
        <!-- Dark Mode Toggle -->
        <button class="dark-mode-toggle" onclick="toggleDarkMode()">
            <span id="dark-mode-icon">🌙</span> <span id="dark-mode-text">Dark Mode</span>
        </button>
        
        <div class="container">
            <h1>💰 Revenue & Treasury Dashboard</h1>
            <p class="subtitle">Track your income streams, treasury balance, and financial sovereignty</p>

            <div class="nav-tabs">
                <a href="/" class="nav-tab">🏠 Home</a>
                <a href="/engines" class="nav-tab">🧠 48 Engines</a>
                <a href="/tools" class="nav-tab">🔧 6 Tools</a>
                <a href="/dashboards" class="nav-tab">📊 All Dashboards</a>
                <a href="/chat" class="nav-tab">💬 AI Chat</a>
                <a href="/agents" class="nav-tab">🤖 AI Agents</a>
                <a href="/websites" class="nav-tab">🌐 Websites</a>
                <a href="/stores" class="nav-tab">🛒 Stores</a>
                <a href="/social" class="nav-tab">📱 Social Media</a>
                <a href="/affiliate" class="nav-tab">💸 Affiliate</a>
                <a href="/revenue" class="nav-tab active">💰 Revenue</a>
                <a href="/ai-advisor" class="nav-tab">🎯 AI Advisor</a>
            </div>

            <!-- Main Metrics -->
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">Monthly Target</div>
                    <div class="metric-value">${total_monthly_target:,.0f}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Current Month</div>
                    <div class="metric-value">${total_current_month:,.0f}</div>
                    <div class="metric-change">↑ {avg_growth}% growth</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">All-Time Total</div>
                    <div class="metric-value">${total_all_time:,.0f}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Active Streams</div>
                    <div class="metric-value">{len(revenue_streams)}</div>
                </div>
            </div>

            <!-- Interactive Charts -->
            <h2 style="color: #667eea; margin-top: 40px;">📈 Revenue Analytics</h2>
            <div class="chart-grid">
                <div class="chart-container">
                    <canvas id="revenueComparisonChart"></canvas>
                </div>
                <div class="chart-container">
                    <canvas id="revenueGrowthChart"></canvas>
                </div>
            </div>
            <div class="chart-container" style="height: 300px;">
                <canvas id="revenueDistributionChart"></canvas>
            </div>

            <!-- Progress Bar -->
            <h2>📊 Monthly Progress</h2>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress_pct}%">
                    {progress_pct}% of target
                </div>
            </div>

            <!-- Sovereignty Assessment -->
            <div style="text-align: center; margin: 30px 0;">
                <h2>👑 Financial Sovereignty Status</h2>
                <span class="sovereignty-badge">
                    🔥 {sovereignty.get('control_level', 'maximum').upper()} CONTROL
                </span>
                <div style="margin-top: 15px;">
                    <strong>Independence Score:</strong> {sovereignty.get('financial_independence_score', 8.5)}/10 |
                    <strong>Diversification:</strong> {sovereignty.get('diversification_score', 9.0)}/10 |
                    <strong>Stability:</strong> {sovereignty.get('growth_stability_score', 7.8)}/10
                </div>
            </div>

            <!-- Revenue Streams -->
            <h2>💵 Revenue Streams</h2>
            <div class="streams-grid">"""
    
    for stream in revenue_streams:
        stream_progress = round((stream.get('current_month_total', 0) / stream.get('monthly_target', 1) * 100), 1)
        revenue_html += f"""
                <div class="stream-card">
                    <div class="stream-header">
                        <div class="stream-title">{stream.get('name', 'Unknown')}</div>
                        <div class="stream-status">{stream.get('status', 'active').upper()}</div>
                    </div>
                    <p style="color: #666; margin-bottom: 15px;">{stream.get('description', '')}</p>
                    
                    <div class="stream-metrics">
                        <div class="stream-metric">
                            <div class="stream-metric-value">${stream.get('monthly_target', 0):,.0f}</div>
                            <div class="stream-metric-label">Monthly Target</div>
                        </div>
                        <div class="stream-metric">
                            <div class="stream-metric-value">${stream.get('current_month_total', 0):,.0f}</div>
                            <div class="stream-metric-label">Current Month</div>
                        </div>
                        <div class="stream-metric">
                            <div class="stream-metric-value">${stream.get('all_time_total', 0):,.0f}</div>
                            <div class="stream-metric-label">All-Time</div>
                        </div>
                        <div class="stream-metric">
                            <div class="stream-metric-value">{stream.get('growth_rate', 0)}%</div>
                            <div class="stream-metric-label">Growth Rate</div>
                        </div>
                    </div>
                    
                    <div class="progress-bar" style="height: 12px;">
                        <div class="progress-fill" style="width: {stream_progress}%; font-size: 0.75em;">
                            {stream_progress}%
                        </div>
                    </div>
                    
                    <div style="margin-top: 15px; color: #666; font-size: 0.9em;">
                        <strong>Sovereignty:</strong> {stream.get('sovereignty_level', 'N/A').title()}
                    </div>
                </div>"""
    
    revenue_html += f"""
            </div>

            <!-- Recommendations -->
            <div class="recommendations">
                <h3>🎯 Strategic Recommendations</h3>
                <ul>"""
    
    for rec in sovereignty.get('recommendations', []):
        revenue_html += f"""
                    <li>{rec}</li>"""
    
    revenue_html += """
                </ul>
            </div>

            <!-- Treasury Log -->
            <h2>🏛️ Recent Treasury Activity</h2>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 12px; margin-top: 20px;">"""
    
    for entry in treasury_data.get('treasury', [])[:5]:  # Show last 5 entries
        revenue_html += f"""
                <div style="border-bottom: 1px solid #e0e0e0; padding: 15px 0;">
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <strong style="color: #667eea;">{entry.get('cycle', 'N/A')}</strong>
                            <span style="color: #666; margin-left: 15px;">Role: {entry.get('role', 'N/A')}</span>
                        </div>
                        <div style="color: #666;">{entry.get('timestamp', 'N/A')}</div>
                    </div>
                    <div style="margin-top: 8px; color: #333;">
                        {entry.get('approval', entry.get('affirmation', 'No details'))}
                        {f"| Income: ${entry.get('income', 0)}" if entry.get('income') else ''}
                    </div>
                </div>"""
    
    revenue_html += """
            </div>

            <!-- Quick Actions -->
            <div style="margin-top: 40px; text-align: center;">
                <button style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 40px; border: none; border-radius: 25px; font-size: 1.1em; font-weight: 600; cursor: pointer; margin: 10px;">
                    📊 Generate Revenue Report
                </button>
                <button style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 15px 40px; border: none; border-radius: 25px; font-size: 1.1em; font-weight: 600; cursor: pointer; margin: 10px;">
                    💰 Add New Revenue Stream
                </button>
                <button style="background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); color: white; padding: 15px 40px; border: none; border-radius: 25px; font-size: 1.1em; font-weight: 600; cursor: pointer; margin: 10px;">
                    🏛️ View Full Treasury
                </button>
            </div>

            <div style="margin-top: 40px; padding: 20px; background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%); border-radius: 12px; text-align: center;">
                <p style="font-size: 1.2em; color: #667eea; font-weight: 600;">
                    🔥 The Flame Burns Sovereign and Eternal! 👑
                </p>
            </div>
        </div>

        <!-- Chart.js Initialization -->
        <script>
            // Data from Python
            const streamLabels = {stream_labels};
            const streamCurrent = {stream_current};
            const streamTargets = {stream_targets};
            const streamGrowth = {stream_growth};

            // Chart 1: Revenue Comparison (Current vs Target)
            new Chart(document.getElementById('revenueComparisonChart'), {{
                type: 'bar',
                data: {{
                    labels: streamLabels,
                    datasets: [
                        {{
                            label: 'Current Month',
                            data: streamCurrent,
                            backgroundColor: 'rgba(102, 126, 234, 0.8)',
                            borderColor: 'rgba(102, 126, 234, 1)',
                            borderWidth: 2
                        }},
                        {{
                            label: 'Monthly Target',
                            data: streamTargets,
                            backgroundColor: 'rgba(118, 75, 162, 0.8)',
                            borderColor: 'rgba(118, 75, 162, 1)',
                            borderWidth: 2
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        title: {{
                            display: true,
                            text: 'Revenue: Current vs Target',
                            font: {{ size: 18, weight: 'bold' }}
                        }},
                        legend: {{
                            position: 'top'
                        }}
                    }},
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            ticks: {{
                                callback: function(value) {{
                                    return '$' + value.toLocaleString();
                                }}
                            }}
                        }}
                    }}
                }}
            }});

            // Chart 2: Growth Rate
            new Chart(document.getElementById('revenueGrowthChart'), {{
                type: 'line',
                data: {{
                    labels: streamLabels,
                    datasets: [{{
                        label: 'Growth Rate (%)',
                        data: streamGrowth,
                        borderColor: 'rgba(16, 185, 129, 1)',
                        backgroundColor: 'rgba(16, 185, 129, 0.2)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        title: {{
                            display: true,
                            text: 'Revenue Stream Growth Rates',
                            font: {{ size: 18, weight: 'bold' }}
                        }},
                        legend: {{
                            position: 'top'
                        }}
                    }},
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            ticks: {{
                                callback: function(value) {{
                                    return value + '%';
                                }}
                            }}
                        }}
                    }}
                }}
            }});

            // Chart 3: Revenue Distribution (Donut)
            new Chart(document.getElementById('revenueDistributionChart'), {{
                type: 'doughnut',
                data: {{
                    labels: streamLabels,
                    datasets: [{{
                        label: 'Revenue Distribution',
                        data: streamCurrent,
                        backgroundColor: [
                            'rgba(102, 126, 234, 0.8)',
                            'rgba(118, 75, 162, 0.8)',
                            'rgba(16, 185, 129, 0.8)',
                            'rgba(251, 191, 36, 0.8)',
                            'rgba(239, 68, 68, 0.8)'
                        ],
                        borderColor: [
                            'rgba(102, 126, 234, 1)',
                            'rgba(118, 75, 162, 1)',
                            'rgba(16, 185, 129, 1)',
                            'rgba(251, 191, 36, 1)',
                            'rgba(239, 68, 68, 1)'
                        ],
                        borderWidth: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        title: {{
                            display: true,
                            text: 'Revenue Stream Distribution',
                            font: {{ size: 18, weight: 'bold' }}
                        }},
                        legend: {{
                            position: 'right'
                        }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    let label = context.label || '';
                                    if (label) {{
                                        label += ': ';
                                    }}
                                    label += '$' + context.parsed.toLocaleString();
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = ((context.parsed / total) * 100).toFixed(1);
                                    label += ' (' + percentage + '%)';
                                    return label;
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        </script>
        
        <!-- Dark Mode Script -->
        <script>
            // Load dark mode preference from localStorage
            if (localStorage.getItem('darkMode') === 'enabled') {{
                document.body.classList.add('dark-mode');
                document.getElementById('dark-mode-icon').textContent = '☀️';
                document.getElementById('dark-mode-text').textContent = 'Light Mode';
            }}
            
            function toggleDarkMode() {{
                const body = document.body;
                const icon = document.getElementById('dark-mode-icon');
                const text = document.getElementById('dark-mode-text');
                
                body.classList.toggle('dark-mode');
                
                if (body.classList.contains('dark-mode')) {{
                    icon.textContent = '☀️';
                    text.textContent = 'Light Mode';
                    localStorage.setItem('darkMode', 'enabled');
                }} else {{
                    icon.textContent = '🌙';
                    text.textContent = 'Dark Mode';
                    localStorage.setItem('darkMode', 'disabled');
                }}
            }}
        </script>
    </body>
    </html>
    """
    return revenue_html

@app.route('/scheduler')
def social_media_scheduler():
    """Social Media Post Scheduler with Calendar Interface"""
    
    # Load scheduled posts (from JSON file)
    scheduler_data = load_json("scheduler_posts.json")
    scheduled_posts = scheduler_data.get("scheduled_posts", [])
    
    # Platforms
    platforms = [
        {"name": "Instagram", "icon": "📷", "color": "#E4405F"},
        {"name": "Facebook", "icon": "👍", "color": "#1877F2"},
        {"name": "Twitter", "icon": "🐦", "color": "#1DA1F2"},
        {"name": "LinkedIn", "icon": "💼", "color": "#0A66C2"},
        {"name": "TikTok", "icon": "🎵", "color": "#000000"},
        {"name": "Pinterest", "icon": "📌", "color": "#E60023"}
    ]
    
    # Calculate stats
    total_scheduled = len(scheduled_posts)
    posts_this_week = len([p for p in scheduled_posts if "2025-12" in p.get("scheduled_time", "")])
    platforms_active = len(set(p.get("platform", "") for p in scheduled_posts))
    
    scheduler_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>📅 Social Media Scheduler</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
        <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            margin: 0;
            transition: all 0.3s ease;
        }}
        body.dark-mode {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        }}
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }}
        .dark-mode .container {{
            background: #1e1e2e;
            color: #e0e0e0;
        }}
        .dark-mode h1, .dark-mode h2, .dark-mode h3 {{
            color: #a78bfa !important;
        }}
        h1 {{
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        .subtitle {{
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }}
        .dark-mode .subtitle {{
            color: #999;
        }}
        .nav-tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            flex-wrap: wrap;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 15px;
        }}
        .nav-tab {{
            padding: 12px 20px;
            text-decoration: none;
            color: #667eea;
            border-radius: 8px 8px 0 0;
            transition: all 0.3s;
            font-weight: 600;
        }}
        .nav-tab:hover {{
            background: rgba(102, 126, 234, 0.1);
        }}
        .nav-tab.active {{
            background: #667eea;
            color: white;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            border: 2px solid #e0e0e0;
        }}
        .dark-mode .stat-card {{
            background: #2a2a3e;
            border-color: #3a3a4e;
        }}
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }}
        .stat-label {{
            color: #666;
            font-size: 1em;
            font-weight: 600;
        }}
        .dark-mode .stat-label {{
            color: #999;
        }}
        .platforms-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin: 30px 0;
        }}
        .platform-card {{
            background: white;
            border: 2px solid #e0e0e0;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .dark-mode .platform-card {{
            background: #2a2a3e;
            border-color: #3a3a4e;
        }}
        .platform-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        .platform-icon {{
            font-size: 3em;
            margin-bottom: 10px;
        }}
        .platform-name {{
            font-weight: 600;
            color: #333;
        }}
        .dark-mode .platform-name {{
            color: #e0e0e0;
        }}
        .post-form {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 12px;
            margin: 30px 0;
        }}
        .dark-mode .post-form {{
            background: #2a2a3e;
        }}
        .form-group {{
            margin-bottom: 20px;
        }}
        .form-label {{
            display: block;
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
        }}
        .dark-mode .form-label {{
            color: #e0e0e0;
        }}
        .form-control {{
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            box-sizing: border-box;
        }}
        .dark-mode .form-control {{
            background: #1e1e2e;
            border-color: #3a3a4e;
            color: #e0e0e0;
        }}
        .form-control:focus {{
            outline: none;
            border-color: #667eea;
        }}
        textarea.form-control {{
            min-height: 120px;
            resize: vertical;
        }}
        .btn {{
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .btn-primary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }}
        .btn-secondary {{
            background: #e0e0e0;
            color: #333;
        }}
        .scheduled-posts {{
            margin-top: 40px;
        }}
        .post-card {{
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .dark-mode .post-card {{
            background: #2a2a3e;
            border-color: #3a3a4e;
        }}
        .post-info {{
            flex: 1;
        }}
        .post-platform {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        .post-content {{
            color: #666;
            margin: 10px 0;
        }}
        .dark-mode .post-content {{
            color: #999;
        }}
        .post-time {{
            color: #999;
            font-size: 0.9em;
        }}
        .post-actions {{
            display: flex;
            gap: 10px;
        }}
        .dark-mode-toggle {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: rgba(102, 126, 234, 0.9);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }}
        .dark-mode-toggle:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.4);
        }}
        .dark-mode .dark-mode-toggle {{
            background: rgba(167, 139, 250, 0.9);
        }}
        </style>
    </head>
    <body>
        <!-- Dark Mode Toggle -->
        <button class="dark-mode-toggle" onclick="toggleDarkMode()">
            <span id="dark-mode-icon">🌙</span> <span id="dark-mode-text">Dark Mode</span>
        </button>
        
        <div class="container">
            <h1>📅 Social Media Scheduler</h1>
            <p class="subtitle">Plan, schedule, and manage your social media posts across all platforms</p>
            
            <div class="nav-tabs">
                <a href="/" class="nav-tab">🏠 Home</a>
                <a href="/social" class="nav-tab">📱 Social</a>
                <a href="/revenue" class="nav-tab">💰 Revenue</a>
                <a href="/scheduler" class="nav-tab active">📅 Scheduler</a>
                <a href="/stores" class="nav-tab">🛒 Stores</a>
            </div>

            <!-- Stats -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Total Scheduled</div>
                    <div class="stat-value">{total_scheduled}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">This Week</div>
                    <div class="stat-value">{posts_this_week}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Active Platforms</div>
                    <div class="stat-value">{platforms_active}</div>
                </div>
            </div>

            <!-- Platforms -->
            <h2 style="color: #667eea; margin-top: 40px;">🌐 Select Platform</h2>
            <div class="platforms-grid">"""
    
    for platform in platforms:
        scheduler_html += f"""
                <div class="platform-card" onclick="selectPlatform('{platform['name']}')">
                    <div class="platform-icon">{platform['icon']}</div>
                    <div class="platform-name">{platform['name']}</div>
                </div>"""
    
    scheduler_html += f"""
            </div>

            <!-- Post Creation Form -->
            <h2 style="color: #667eea; margin-top: 40px;">✍️ Create Post</h2>
            <div class="post-form">
                <div class="form-group">
                    <label class="form-label">Platform</label>
                    <select id="platform-select" class="form-control">
                        <option value="">Select platform...</option>"""
    
    for platform in platforms:
        scheduler_html += f"""
                        <option value="{platform['name']}">{platform['icon']} {platform['name']}</option>"""
    
    scheduler_html += """
                    </select>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Post Content</label>
                    <textarea id="post-content" class="form-control" placeholder="What do you want to share?"></textarea>
                    <small style="color: #666;">Character count: <span id="char-count">0</span></small>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Schedule Date & Time</label>
                    <input type="datetime-local" id="schedule-time" class="form-control">
                </div>
                
                <div class="form-group">
                    <label class="form-label">Add Image/Video (Optional)</label>
                    <input type="file" class="form-control" accept="image/*,video/*">
                </div>
                
                <div class="form-group">
                    <label class="form-label">Hashtags</label>
                    <input type="text" id="hashtags" class="form-control" placeholder="#codexdominion #ai #automation">
                </div>
                
                <div style="display: flex; gap: 15px; margin-top: 25px;">
                    <button class="btn btn-primary" onclick="schedulePost()">📅 Schedule Post</button>
                    <button class="btn btn-secondary" onclick="saveDraft()">💾 Save as Draft</button>
                    <button class="btn btn-secondary" onclick="previewPost()">👁️ Preview</button>
                </div>
            </div>

            <!-- Scheduled Posts -->
            <h2 style="color: #667eea; margin-top: 40px;">📋 Scheduled Posts</h2>
            <div class="scheduled-posts">"""
    
    if scheduled_posts:
        for post in scheduled_posts[:10]:  # Show first 10
            platform_color = next((p["color"] for p in platforms if p["name"] == post.get("platform", "")), "#667eea")
            scheduler_html += f"""
                <div class="post-card">
                    <div class="post-info">
                        <span class="post-platform" style="background: {platform_color}20; color: {platform_color};">
                            {post.get('platform', 'Unknown')}
                        </span>
                        <div class="post-content">{post.get('content', '')[:100]}...</div>
                        <div class="post-time">⏰ Scheduled: {post.get('scheduled_time', 'Not set')}</div>
                    </div>
                    <div class="post-actions">
                        <button class="btn btn-secondary" onclick="editPost('{post.get('id', '')}')">✏️ Edit</button>
                        <button class="btn btn-secondary" onclick="deletePost('{post.get('id', '')}')">🗑️ Delete</button>
                    </div>
                </div>"""
    else:
        scheduler_html += """
                <div style="text-align: center; padding: 40px; color: #666;">
                    <p style="font-size: 1.2em;">📭 No scheduled posts yet</p>
                    <p>Create your first post above to get started!</p>
                </div>"""
    
    scheduler_html += """
            </div>

            <div style="margin-top: 40px; padding: 20px; background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%); border-radius: 12px; text-align: center;">
                <p style="font-size: 1.2em; color: #667eea; font-weight: 600;">
                    🔥 The Flame Burns Sovereign and Eternal! 👑
                </p>
            </div>
        </div>

        <script>
            // Character count
            document.getElementById('post-content').addEventListener('input', function() {
                document.getElementById('char-count').textContent = this.value.length;
            });

            // Select platform
            function selectPlatform(platform) {
                document.getElementById('platform-select').value = platform;
                document.getElementById('platform-select').dispatchEvent(new Event('change'));
            }

            // Schedule post
            function schedulePost() {
                const platform = document.getElementById('platform-select').value;
                const content = document.getElementById('post-content').value;
                const scheduleTime = document.getElementById('schedule-time').value;
                
                if (!platform || !content || !scheduleTime) {
                    alert('Please fill in all required fields');
                    return;
                }
                
                // TODO: Send to backend API
                alert(`Post scheduled for ${platform} at ${scheduleTime}!`);
            }

            // Save draft
            function saveDraft() {
                alert('Draft saved! You can find it in your drafts folder.');
            }

            // Preview post
            function previewPost() {
                const content = document.getElementById('post-content').value;
                if (!content) {
                    alert('Please enter some content first');
                    return;
                }
                
                const preview = window.open('', 'Preview', 'width=400,height=600');
                preview.document.write(`
                    <html>
                    <head><title>Post Preview</title>
                    <style>
                        body { font-family: Arial, sans-serif; padding: 20px; }
                        .preview { border: 2px solid #e0e0e0; padding: 20px; border-radius: 12px; }
                    </style>
                    </head>
                    <body>
                        <h2>Post Preview</h2>
                        <div class="preview">${content}</div>
                    </body>
                    </html>
                `);
            }

            // Edit post
            function editPost(id) {
                alert(`Edit post: ${id}`);
            }

            // Delete post
            function deletePost(id) {
                if (confirm('Are you sure you want to delete this scheduled post?')) {
                    alert(`Post ${id} deleted`);
                }
            }

            // Dark mode
            if (localStorage.getItem('darkMode') === 'enabled') {
                document.body.classList.add('dark-mode');
                document.getElementById('dark-mode-icon').textContent = '☀️';
                document.getElementById('dark-mode-text').textContent = 'Light Mode';
            }
            
            function toggleDarkMode() {
                const body = document.body;
                const icon = document.getElementById('dark-mode-icon');
                const text = document.getElementById('dark-mode-text');
                
                body.classList.toggle('dark-mode');
                
                if (body.classList.contains('dark-mode')) {
                    icon.textContent = '☀️';
                    text.textContent = 'Light Mode';
                    localStorage.setItem('darkMode', 'enabled');
                } else {
                    icon.textContent = '🌙';
                    text.textContent = 'Dark Mode';
                    localStorage.setItem('darkMode', 'disabled');
                }
            }
        </script>
    </body>
    </html>
    """
    return scheduler_html

@app.route('/product-generator')
def product_description_generator():
    """AI Product Description Generator"""
    
    generator_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 AI Product Description Generator</title>
        <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            margin: 0;
            transition: all 0.3s ease;
        }
        body.dark-mode {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        .dark-mode .container {
            background: #1e1e2e;
            color: #e0e0e0;
        }
        .dark-mode h1, .dark-mode h2, .dark-mode h3 {
            color: #a78bfa !important;
        }
        h1 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        .dark-mode .subtitle {
            color: #999;
        }
        .nav-tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            flex-wrap: wrap;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 15px;
        }
        .nav-tab {
            padding: 12px 20px;
            text-decoration: none;
            color: #667eea;
            border-radius: 8px 8px 0 0;
            transition: all 0.3s;
            font-weight: 600;
        }
        .nav-tab:hover {
            background: rgba(102, 126, 234, 0.1);
        }
        .nav-tab.active {
            background: #667eea;
            color: white;
        }
        .two-column {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin: 30px 0;
        }
        @media (max-width: 768px) {
            .two-column {
                grid-template-columns: 1fr;
            }
        }
        .panel {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 30px;
        }
        .dark-mode .panel {
            background: #2a2a3e;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-label {
            display: block;
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
        }
        .dark-mode .form-label {
            color: #e0e0e0;
        }
        .form-control {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            box-sizing: border-box;
            font-family: inherit;
        }
        .dark-mode .form-control {
            background: #1e1e2e;
            border-color: #3a3a4e;
            color: #e0e0e0;
        }
        .form-control:focus {
            outline: none;
            border-color: #667eea;
        }
        textarea.form-control {
            min-height: 100px;
            resize: vertical;
        }
        .btn {
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            display: inline-block;
            margin-right: 10px;
            margin-bottom: 10px;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        .btn-secondary {
            background: #e0e0e0;
            color: #333;
        }
        .btn-secondary:hover {
            background: #d0d0d0;
        }
        .dark-mode .btn-secondary {
            background: #3a3a4e;
            color: #e0e0e0;
        }
        .output-section {
            margin-top: 20px;
        }
        .output-card {
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
        }
        .dark-mode .output-card {
            background: #1e1e2e;
            border-color: #3a3a4e;
        }
        .output-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }
        .dark-mode .output-header {
            border-bottom-color: #3a3a4e;
        }
        .output-title {
            font-weight: 600;
            color: #667eea;
            font-size: 1.1em;
        }
        .output-actions {
            display: flex;
            gap: 10px;
        }
        .output-content {
            color: #333;
            line-height: 1.6;
        }
        .dark-mode .output-content {
            color: #e0e0e0;
        }
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .style-options {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        .style-btn {
            padding: 8px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 20px;
            background: white;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 0.9em;
        }
        .style-btn:hover {
            border-color: #667eea;
            background: rgba(102, 126, 234, 0.1);
        }
        .style-btn.active {
            border-color: #667eea;
            background: #667eea;
            color: white;
        }
        .dark-mode .style-btn {
            background: #2a2a3e;
            border-color: #3a3a4e;
        }
        .dark-mode-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: rgba(102, 126, 234, 0.9);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }
        .dark-mode-toggle:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.4);
        }
        .dark-mode .dark-mode-toggle {
            background: rgba(167, 139, 250, 0.9);
        }
        </style>
    </head>
    <body>
        <!-- Dark Mode Toggle -->
        <button class="dark-mode-toggle" onclick="toggleDarkMode()">
            <span id="dark-mode-icon">🌙</span> <span id="dark-mode-text">Dark Mode</span>
        </button>
        
        <div class="container">
            <h1>🤖 AI Product Description Generator</h1>
            <p class="subtitle">Generate compelling product descriptions using AI in seconds</p>
            
            <div class="nav-tabs">
                <a href="/" class="nav-tab">🏠 Home</a>
                <a href="/stores" class="nav-tab">🛒 Stores</a>
                <a href="/product-generator" class="nav-tab active">🤖 AI Generator</a>
                <a href="/revenue" class="nav-tab">💰 Revenue</a>
            </div>

            <div class="two-column">
                <!-- Input Panel -->
                <div class="panel">
                    <h2 style="color: #667eea; margin-top: 0;">📝 Product Details</h2>
                    
                    <div class="form-group">
                        <label class="form-label">Product Name *</label>
                        <input type="text" id="product-name" class="form-control" placeholder="e.g., Wireless Bluetooth Headphones">
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Key Features (one per line) *</label>
                        <textarea id="product-features" class="form-control" placeholder="e.g.,
40-hour battery life
Active noise cancellation
Premium sound quality
Comfortable ear cushions"></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Target Audience *</label>
                        <input type="text" id="target-audience" class="form-control" placeholder="e.g., Music lovers, Professionals, Commuters">
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Price Range (Optional)</label>
                        <input type="text" id="price-range" class="form-control" placeholder="e.g., $99 - $149">
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Writing Style</label>
                        <div class="style-options">
                            <button class="style-btn active" data-style="professional" onclick="selectStyle('professional')">Professional</button>
                            <button class="style-btn" data-style="casual" onclick="selectStyle('casual')">Casual</button>
                            <button class="style-btn" data-style="luxury" onclick="selectStyle('luxury')">Luxury</button>
                            <button class="style-btn" data-style="technical" onclick="selectStyle('technical')">Technical</button>
                            <button class="style-btn" data-style="playful" onclick="selectStyle('playful')">Playful</button>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Description Length</label>
                        <select id="length" class="form-control">
                            <option value="short">Short (2-3 sentences)</option>
                            <option value="medium" selected>Medium (1 paragraph)</option>
                            <option value="long">Long (2-3 paragraphs)</option>
                        </select>
                    </div>
                    
                    <div style="margin-top: 25px;">
                        <button class="btn btn-primary" onclick="generateDescriptions()">✨ Generate Descriptions</button>
                        <button class="btn btn-secondary" onclick="clearForm()">🔄 Clear</button>
                    </div>
                </div>

                <!-- Output Panel -->
                <div class="panel">
                    <h2 style="color: #667eea; margin-top: 0;">✨ Generated Descriptions</h2>
                    
                    <div id="output-section" class="output-section">
                        <div style="text-align: center; padding: 40px; color: #999;">
                            <p style="font-size: 1.1em;">💡 Enter product details and click "Generate Descriptions"</p>
                            <p>We'll create multiple variations for you!</p>
                        </div>
                    </div>
                </div>
            </div>

            <div style="margin-top: 40px; padding: 20px; background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%); border-radius: 12px; text-align: center;">
                <p style="font-size: 1.2em; color: #667eea; font-weight: 600;">
                    🔥 The Flame Burns Sovereign and Eternal! 👑
                </p>
            </div>
        </div>

        <script>
            let selectedStyle = 'professional';

            function selectStyle(style) {
                selectedStyle = style;
                document.querySelectorAll('.style-btn').forEach(btn => {
                    btn.classList.remove('active');
                });
                document.querySelector(`[data-style="${style}"]`).classList.add('active');
            }

            function clearForm() {
                document.getElementById('product-name').value = '';
                document.getElementById('product-features').value = '';
                document.getElementById('target-audience').value = '';
                document.getElementById('price-range').value = '';
                document.getElementById('length').value = 'medium';
                selectedStyle = 'professional';
                selectStyle('professional');
            }

            async function generateDescriptions() {
                const productName = document.getElementById('product-name').value.trim();
                const features = document.getElementById('product-features').value.trim();
                const targetAudience = document.getElementById('target-audience').value.trim();
                const priceRange = document.getElementById('price-range').value.trim();
                const length = document.getElementById('length').value;
                
                if (!productName || !features || !targetAudience) {
                    alert('Please fill in all required fields (Product Name, Features, Target Audience)');
                    return;
                }
                
                const outputSection = document.getElementById('output-section');
                
                // Show loading
                outputSection.innerHTML = `
                    <div class="loading">
                        <div class="spinner"></div>
                        <p>Generating descriptions with AI...</p>
                        <p style="font-size: 0.9em; color: #999;">This may take a few seconds</p>
                    </div>
                \`;
                
                try {
                    const response = await fetch('/api/generate-description', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            product_name: productName,
                            features: features,
                            target_audience: targetAudience,
                            price_range: priceRange,
                            style: selectedStyle,
                            length: length
                        })
                    });
                    
                    if (!response.ok) {
                        throw new Error('Failed to generate descriptions');
                    }
                    
                    const data = await response.json();
                    displayDescriptions(data.descriptions);
                    
                } catch (error) {
                    outputSection.innerHTML = `
                        <div style="text-align: center; padding: 40px; color: #e74c3c;">
                            <p style="font-size: 1.2em;">❌ Error generating descriptions</p>
                            <p>${error.message}</p>
                            <p style="font-size: 0.9em; margin-top: 15px;">Using demo descriptions instead...</p>
                        </div>
                    `;
                    
                    // Fallback demo descriptions
                    setTimeout(() => {
                        displayDescriptions(generateDemoDescriptions(productName, features));
                    }, 1000);
                }
            }

            function generateDemoDescriptions(name, features) {
                // Demo descriptions (fallback when API is not available)
                return [
                    {
                        title: "Standard Description",
                        content: \`\${name} - Experience premium quality with our \${name}. \${features.split('\\n')[0]}. Perfect for those who demand excellence.\`
                    },
                    {
                        title: "SEO-Optimized",
                        content: \`Buy \${name} Online - Premium Quality ✓ Fast Shipping ✓ Best Price Guaranteed. \${features.split('\\n')[0]}. Order now and save!\`
                    },
                    {
                        title: "Emotional Appeal",
                        content: \`Transform your experience with \${name}. Imagine enjoying \${features.split('\\n')[0].toLowerCase()}. This isn't just a product—it's an investment in your lifestyle.\`
                    }
                ];
            }

            function displayDescriptions(descriptions) {
                const outputSection = document.getElementById('output-section');
                outputSection.innerHTML = '';
                
                descriptions.forEach((desc, index) => {
                    const card = document.createElement('div');
                    card.className = 'output-card';
                    card.innerHTML = `
                        <div class="output-header">
                            <div class="output-title">${desc.title || `Variation ${index + 1}`}</div>
                            <div class="output-actions">
                                <button class="btn btn-secondary" style="padding: 6px 12px; font-size: 0.85em;" onclick="copyDescription(${index})">📋 Copy</button>
                            </div>
                        </div>
                        <div class="output-content" id="desc-\${index}">\${desc.content}</div>
                    \`;
                    outputSection.appendChild(card);
                });
            }

            function copyDescription(index) {
                const content = document.getElementById(\`desc-\${index}\`).innerText;
                navigator.clipboard.writeText(content).then(() => {
                    alert('✅ Description copied to clipboard!');
                }).catch(err => {
                    console.error('Failed to copy:', err);
                });
            }

            // Dark mode
            if (localStorage.getItem('darkMode') === 'enabled') {
                document.body.classList.add('dark-mode');
                document.getElementById('dark-mode-icon').textContent = '☀️';
                document.getElementById('dark-mode-text').textContent = 'Light Mode';
            }
            
            function toggleDarkMode() {
                const body = document.body;
                const icon = document.getElementById('dark-mode-icon');
                const text = document.getElementById('dark-mode-text');
                
                body.classList.toggle('dark-mode');
                
                if (body.classList.contains('dark-mode')) {
                    icon.textContent = '☀️';
                    text.textContent = 'Light Mode';
                    localStorage.setItem('darkMode', 'enabled');
                } else {
                    icon.textContent = '🌙';
                    text.textContent = 'Dark Mode';
                    localStorage.setItem('darkMode', 'disabled');
                }
            }
        </script>
    </body>
    </html>
    """
    return generator_html

@app.route('/api/generate-description', methods=['POST'])
def api_generate_description():
    """API endpoint for generating product descriptions"""
    data = request.get_json()
    
    product_name = data.get('product_name', '')
    features = data.get('features', '')
    target_audience = data.get('target_audience', '')
    price_range = data.get('price_range', '')
    style = data.get('style', 'professional')
    length = data.get('length', 'medium')
    
    # TODO: Integrate with OpenAI API when key is configured
    # For now, return demo descriptions
    descriptions = [
        {
            "title": "Professional Description",
            "content": f"{product_name} delivers exceptional value for {target_audience}. Key features include {features.split(chr(10))[0] if features else 'premium quality'}. {price_range if price_range else 'Competitively priced'} for outstanding performance."
        },
        {
            "title": "SEO-Optimized",
            "content": f"Buy {product_name} Online - Best Price ✓ Fast Shipping ✓ Top Quality. Perfect for {target_audience}. {features.split(chr(10))[0] if features else 'Premium features'}. Order now!"
        },
        {
            "title": "Emotional Appeal",
            "content": f"Transform your experience with {product_name}. Designed specifically for {target_audience}, this product brings {features.split(chr(10))[0].lower() if features else 'exceptional quality'} to your everyday life. Don't settle for less—choose excellence."
        },
        {
            "title": "Feature-Focused",
            "content": f"{product_name} - Technical Excellence: {features.replace(chr(10), '. ') if features else 'Premium specifications'}. Ideal for {target_audience} seeking professional-grade solutions."
        }
    ]
    
    return jsonify({"descriptions": descriptions, "status": "success"})

@app.route('/design-system')
def design_system_showcase():
    """Design System Showcase - Complete UI Component Library"""
    return render_template('design-system-showcase.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads"""
    if 'file' not in request.files:
        return redirect(url_for('documents'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('documents'))

    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('documents'))

    return redirect(url_for('documents'))

# ==================== DASHBOARD HTML ROUTES ====================

@app.route('/dashboard')
def dashboard_home():
    """Main dashboard with sidebar layout - Enhanced metrics"""
    from datetime import datetime
    
    # Load all data sources
    platform_capsules = load_json("platform_capsules.json")
    engines_data = load_json("engines.json")
    realms_data = load_json("realms.json")
    ledger = load_json("codex_ledger.json")
    
    # Calculate metrics
    total_capsules = len(platform_capsules.get("capsules", []))
    total_engines = len(engines_data.get("engines", []))
    total_realms = len(realms_data.get("realms", []))
    total_platforms = 2  # Diaspora Hub + Teen Biz Box
    
    # Capsule readiness (count completed capsules with status="operational")
    completed_capsules = sum(1 for c in platform_capsules.get("capsules", []) 
                            if c.get("status") == "operational")
    capsule_readiness = round((completed_capsules / total_capsules * 100) if total_capsules > 0 else 0, 1)
    
    # Engine health (count active engines)
    active_engines = sum(1 for e in engines_data.get("engines", []) 
                        if e.get("status") in ["active", "operational"])
    engine_health = round((active_engines / total_engines * 100) if total_engines > 0 else 0, 1)
    
    # Platform progress (simplified - based on capsule completion)
    platform_progress = capsule_readiness  # Can be enhanced with specific platform metrics
    
    # Last sync timestamp
    last_updated = ledger.get("meta", {}).get("last_updated", "N/A")
    try:
        if last_updated != "N/A":
            dt = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
            last_sync = dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            last_sync = "Never"
    except:
        last_sync = "Unknown"
    
    # System status
    system_status = "OK" if capsule_readiness > 30 and engine_health > 50 else "DEGRADED"
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>👑 Codex Dominion Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #f5f7fa;
                color: #2c3e50;
            }
            
            /* Header Bar */
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 30px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                position: sticky;
                top: 0;
                z-index: 1000;
            }
            
            .header-left {
                display: flex;
                align-items: center;
                gap: 15px;
            }
            
            .logo {
                font-size: 1.8em;
                font-weight: bold;
            }
            
            .env-badge {
                background: rgba(255, 255, 255, 0.2);
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.85em;
                font-weight: 600;
            }
            
            .header-right {
                display: flex;
                align-items: center;
                gap: 20px;
            }
            
            .user-menu {
                display: flex;
                align-items: center;
                gap: 10px;
                cursor: pointer;
                padding: 8px 15px;
                border-radius: 8px;
                transition: background 0.3s;
            }
            
            .user-menu:hover {
                background: rgba(255, 255, 255, 0.1);
            }
            
            .user-avatar {
                width: 35px;
                height: 35px;
                border-radius: 50%;
                background: white;
                color: #667eea;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
            }
            
            /* Layout Container */
            .layout-container {
                display: flex;
                min-height: calc(100vh - 70px);
            }
            
            /* Left Sidebar */
            .sidebar {
                width: 260px;
                background: white;
                box-shadow: 2px 0 10px rgba(0,0,0,0.05);
                padding: 20px 0;
            }
            
            .sidebar-section {
                margin-bottom: 25px;
            }
            
            .sidebar-title {
                color: #95a5a6;
                font-size: 0.75em;
                text-transform: uppercase;
                font-weight: 600;
                padding: 0 20px;
                margin-bottom: 10px;
                letter-spacing: 1px;
            }
            
            .nav-item {
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 12px 20px;
                color: #2c3e50;
                text-decoration: none;
                transition: all 0.3s;
                border-left: 3px solid transparent;
            }
            
            .nav-item:hover {
                background: #f8f9fa;
                border-left-color: #667eea;
                color: #667eea;
            }
            
            .nav-item.active {
                background: #e8eaf6;
                border-left-color: #667eea;
                color: #667eea;
                font-weight: 600;
            }
            
            .nav-icon {
                font-size: 1.3em;
                width: 24px;
                text-align: center;
            }
            
            .nav-item.sub-item {
                padding-left: 56px;
                font-size: 0.9em;
            }
            
            /* Main Content Area */
            .main-content {
                flex: 1;
                padding: 30px;
                overflow-y: auto;
            }
            
            .content-header {
                margin-bottom: 30px;
            }
            
            .content-header h1 {
                font-size: 2em;
                color: #2c3e50;
                margin-bottom: 8px;
            }
            
            .content-header p {
                color: #7f8c8d;
                font-size: 1.05em;
            }
            
            /* Overview Box */
            .overview-box {
                background: white;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                margin-bottom: 25px;
                border-left: 4px solid #667eea;
            }
            
            .overview-title {
                font-size: 1.4em;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .overview-stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                gap: 20px;
                padding: 15px 0;
                border-bottom: 2px solid #ecf0f1;
                margin-bottom: 20px;
            }
            
            .overview-stat {
                text-align: center;
            }
            
            .overview-stat-value {
                font-size: 1.8em;
                font-weight: bold;
                color: #667eea;
            }
            
            .overview-stat-label {
                font-size: 0.9em;
                color: #7f8c8d;
                margin-top: 5px;
            }
            
            /* Quick Metrics Grid */
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            
            .metric-card {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 18px;
                border-left: 3px solid #667eea;
            }
            
            .metric-title {
                font-size: 0.85em;
                color: #7f8c8d;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 10px;
                font-weight: 600;
            }
            
            .metric-value {
                font-size: 1.6em;
                font-weight: bold;
                color: #2c3e50;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            
            .metric-progress {
                width: 100%;
                height: 8px;
                background: #ecf0f1;
                border-radius: 4px;
                margin-top: 12px;
                overflow: hidden;
            }
            
            .metric-progress-bar {
                height: 100%;
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                border-radius: 4px;
                transition: width 0.5s ease;
            }
            
            .metric-subtext {
                font-size: 0.85em;
                color: #95a5a6;
                margin-top: 8px;
            }
            
            .status-badge {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 0.8em;
                font-weight: 600;
                text-transform: uppercase;
            }
            
            .status-ok {
                background: #d4edda;
                color: #155724;
            }
            
            .status-degraded {
                background: #fff3cd;
                color: #856404;
            }
            
            /* Quick Actions */
            .quick-actions {
                background: white;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            }
            
            .quick-actions h2 {
                margin-bottom: 20px;
                color: #2c3e50;
            }
            
            .action-buttons {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
            }
            
            .action-btn {
                padding: 15px 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 8px;
                text-align: center;
                transition: opacity 0.3s;
                font-weight: 500;
            }
            
            .action-btn:hover {
                opacity: 0.9;
            }
            
            /* Responsive */
            @media (max-width: 768px) {
                .sidebar {
                    width: 200px;
                }
                
                .main-content {
                    padding: 20px;
                }
                
                .header {
                    padding: 12px 20px;
                }
                
                .logo {
                    font-size: 1.3em;
                }
            }
        </style>
    </head>
    <body>
        <!-- Header Bar -->
        <div class="header">
            <div class="header-left">
                <div class="logo">👑 Codex Dominion</div>
                <div class="env-badge">Local Development</div>
            </div>
            <div class="header-right">
                <div class="user-menu">
                    <div class="user-avatar">CD</div>
                    <span>Admin</span>
                </div>
            </div>
        </div>
        
        <!-- Layout Container -->
        <div class="layout-container">
            <!-- Left Sidebar -->
            <div class="sidebar">
                <div class="sidebar-section">
                    <div class="sidebar-title">Navigation</div>
                    <a href="/dashboard" class="nav-item active">
                        <span class="nav-icon">📊</span>
                        <span>Overview</span>
                    </a>
                    <a href="/dashboard/capsules" class="nav-item">
                        <span class="nav-icon">🔰</span>
                        <span>Capsules</span>
                    </a>
                    <a href="/dashboard/intelligence-core" class="nav-item">
                        <span class="nav-icon">🧠</span>
                        <span>Intelligence Core</span>
                    </a>
                    <a href="/dashboard/industries" class="nav-item">
                        <span class="nav-icon">🏭</span>
                        <span>Industries</span>
                    </a>
                </div>
                
                <div class="sidebar-section">
                    <div class="sidebar-title">Platforms</div>
                    <a href="/dashboard/platforms" class="nav-item">
                        <span class="nav-icon">🌐</span>
                        <span>All Platforms</span>
                    </a>
                    <a href="/dashboard/platforms/diaspora" class="nav-item sub-item">
                        <span>Diaspora Hub</span>
                    </a>
                    <a href="/dashboard/platforms/teens" class="nav-item sub-item">
                        <span>Teen Biz Box</span>
                    </a>
                </div>
                
                <div class="sidebar-section">
                    <div class="sidebar-title">System</div>
                    <a href="/dashboard/analytics" class="nav-item">
                        <span class="nav-icon">📈</span>
                        <span>Analytics</span>
                    </a>
                    <a href="/api/health" class="nav-item">
                        <span class="nav-icon">📋</span>
                        <span>System Logs</span>
                    </a>
                    <a href="/status" class="nav-item">
                        <span class="nav-icon">⚙️</span>
                        <span>Settings</span>
                    </a>
                </div>
            </div>
            
            <!-- Main Content Area -->
            <div class="main-content">
                <div class="content-header">
                    <h1>Dashboard Overview</h1>
                    <p>Real-time system metrics and platform status</p>
                </div>
                
                <!-- Overview Box -->
                <div class="overview-box">
                    <div class="overview-title">
                        <span>📊</span>
                        <span>OVERVIEW</span>
                        <span class="status-badge status-{{ system_status.lower() }}">{{ system_status }}</span>
                    </div>
                    
                    <div class="overview-stats">
                        <div class="overview-stat">
                            <div class="overview-stat-value">{{ total_capsules }}</div>
                            <div class="overview-stat-label">Capsules</div>
                        </div>
                        <div class="overview-stat">
                            <div class="overview-stat-value">{{ total_engines }}</div>
                            <div class="overview-stat-label">Engines</div>
                        </div>
                        <div class="overview-stat">
                            <div class="overview-stat-value">{{ total_realms }}</div>
                            <div class="overview-stat-label">Realms</div>
                        </div>
                        <div class="overview-stat">
                            <div class="overview-stat-value">{{ total_platforms }}</div>
                            <div class="overview-stat-label">Platforms</div>
                        </div>
                    </div>
                    
                    <!-- Quick Metrics -->
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <div class="metric-title">Capsule Readiness</div>
                            <div class="metric-value">
                                <span>{{ capsule_readiness }}%</span>
                                <span style="font-size: 0.6em;">🔰</span>
                            </div>
                            <div class="metric-progress">
                                <div class="metric-progress-bar" style="width: {{ capsule_readiness }}%;"></div>
                            </div>
                            <div class="metric-subtext">{{ completed_capsules }}/{{ total_capsules }} operational</div>
                        </div>
                        
                        <div class="metric-card">
                            <div class="metric-title">Engine Health</div>
                            <div class="metric-value">
                                <span>{{ engine_health }}%</span>
                                <span style="font-size: 0.6em;">🧠</span>
                            </div>
                            <div class="metric-progress">
                                <div class="metric-progress-bar" style="width: {{ engine_health }}%;"></div>
                            </div>
                            <div class="metric-subtext">{{ active_engines }}/{{ total_engines }} active</div>
                        </div>
                        
                        <div class="metric-card">
                            <div class="metric-title">Platform Progress</div>
                            <div class="metric-value">
                                <span>{{ platform_progress }}%</span>
                                <span style="font-size: 0.6em;">🌐</span>
                            </div>
                            <div class="metric-progress">
                                <div class="metric-progress-bar" style="width: {{ platform_progress }}%;"></div>
                            </div>
                            <div class="metric-subtext">Diaspora Hub • Teen Biz Box</div>
                        </div>
                        
                        <div class="metric-card">
                            <div class="metric-title">Last Update</div>
                            <div class="metric-value" style="font-size: 1.2em;">
                                <span>⏱️</span>
                                <span style="font-size: 0.75em;">{{ last_sync }}</span>
                            </div>
                            <div class="metric-subtext">System synchronized</div>
                        </div>
                    </div>
                </div>
                
                <!-- Quick Actions -->
                <div class="quick-actions">
                    <h2>Quick Actions</h2>
                    <div class="action-buttons">
                        <a href="/dashboard/capsules" class="action-btn">Browse Capsules</a>
                        <a href="/dashboard/intelligence-core" class="action-btn">View Engines</a>
                        <a href="/dashboard/analytics" class="action-btn">View Analytics</a>
                        <a href="/api/platform-overview" class="action-btn">API Overview</a>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """, 
    total_capsules=total_capsules,
    total_engines=total_engines,
    total_realms=total_realms,
    total_platforms=total_platforms,
    completed_capsules=completed_capsules,
    capsule_readiness=capsule_readiness,
    active_engines=active_engines,
    engine_health=engine_health,
    platform_progress=platform_progress,
    last_sync=last_sync,
    system_status=system_status)

@app.route('/dashboard/overview')
def dashboard_overview():
    """System overview page"""
    overview_data = load_json("platform_capsules.json").get("meta", {})
    engines_data = load_json("engines.json").get("meta", {})
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Overview | Codex Dominion</title>
        <meta charset="utf-8">
        <style>
            body { font-family: 'Segoe UI', Tahoma, sans-serif; background: #f5f5f5; color: #333; padding: 20px; }
            .container { max-width: 1400px; margin: 0 auto; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }
            .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .stat-card { background: white; border-radius: 10px; padding: 25px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .stat-value { font-size: 3em; font-weight: bold; color: #667eea; }
            .stat-label { font-size: 1.1em; color: #666; margin-top: 10px; }
            .back-link { display: inline-block; margin-top: 20px; padding: 10px 20px; background: white; color: #667eea; text-decoration: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 System Overview</h1>
                <p>Complete platform architecture metrics</p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{{ total_capsules }}</div>
                    <div class="stat-label">Total Capsules</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{{ total_engines }}</div>
                    <div class="stat-label">Processing Engines</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">6</div>
                    <div class="stat-label">Realms</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{{ total_modules }}</div>
                    <div class="stat-label">Total Modules</div>
                </div>
            </div>
            
            <a href="/dashboard" class="back-link">← Back to Dashboard</a>
        </div>
    </body>
    </html>
    """, 
    total_capsules=overview_data.get("total_capsules", 36),
    total_engines=engines_data.get("total_engines", 26),
    total_modules=overview_data.get("total_modules", 144))

@app.route('/dashboard/capsules')
def dashboard_capsules():
    """Capsules list page with realm filtering"""
    from flask import request
    
    platform_data = load_json("platform_capsules.json")
    execution_data = load_json("execution_capsules.json")
    
    # Get filter parameter
    selected_realm = request.args.get('realm', 'all').lower()
    
    # Organize capsules by realm
    realms_config = {
        "foundation": {"icon": "🏛️", "color": "#667eea", "capsules": []},
        "economic": {"icon": "💰", "color": "#28a745", "capsules": []},
        "knowledge": {"icon": "📚", "color": "#17a2b8", "capsules": []},
        "community": {"icon": "👥", "color": "#fd7e14", "capsules": []},
        "automation": {"icon": "⚙️", "color": "#6f42c1", "capsules": []},
        "media": {"icon": "🎬", "color": "#e83e8c", "capsules": []}
    }
    
    all_capsules = []
    for realm_name, realm_config in realms_config.items():
        capsules = platform_data.get(realm_name, [])
        for capsule in capsules:
            capsule_data = capsule.copy()
            capsule_data["realm"] = realm_name
            capsule_data["realm_icon"] = realm_config["icon"]
            capsule_data["realm_color"] = realm_config["color"]
            realm_config["capsules"].append(capsule_data)
            all_capsules.append(capsule_data)
    
    # Add execution capsules
    exec_capsules = execution_data.get("execution_capsules", [])
    for capsule in exec_capsules:
        capsule_data = capsule.copy()
        capsule_data["realm"] = "execution"
        capsule_data["realm_icon"] = "⚡"
        capsule_data["realm_color"] = "#dc3545"
        all_capsules.append(capsule_data)
    
    # Filter capsules if realm is selected
    if selected_realm != 'all':
        display_capsules = [c for c in all_capsules if c.get("realm") == selected_realm]
    else:
        display_capsules = all_capsules
    
    # Count by realm
    realm_counts = {realm: len(config["capsules"]) for realm, config in realms_config.items()}
    realm_counts["execution"] = len(exec_capsules)
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Capsules | Codex Dominion</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #f5f7fa;
                color: #2c3e50;
            }
            
            /* Header Bar */
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 30px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            .header-left {
                display: flex;
                align-items: center;
                gap: 15px;
            }
            
            .logo {
                font-size: 1.8em;
                font-weight: bold;
            }
            
            .back-link {
                color: white;
                text-decoration: none;
                padding: 8px 15px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 5px;
                transition: background 0.3s;
            }
            
            .back-link:hover {
                background: rgba(255, 255, 255, 0.3);
            }
            
            /* Main Container */
            .container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 30px;
            }
            
            .page-title {
                font-size: 2em;
                color: #2c3e50;
                margin-bottom: 10px;
            }
            
            .page-subtitle {
                color: #7f8c8d;
                font-size: 1.1em;
                margin-bottom: 30px;
            }
            
            /* Realm Filters */
            .realm-filters {
                background: white;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                margin-bottom: 30px;
            }
            
            .filter-title {
                font-size: 0.9em;
                color: #7f8c8d;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 15px;
                font-weight: 600;
            }
            
            .filter-buttons {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
            }
            
            .filter-btn {
                padding: 10px 20px;
                background: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                text-decoration: none;
                color: #2c3e50;
                font-weight: 500;
                transition: all 0.3s;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            
            .filter-btn:hover {
                border-color: #667eea;
                background: #f0f3ff;
                transform: translateY(-2px);
            }
            
            .filter-btn.active {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-color: #667eea;
            }
            
            .filter-count {
                background: rgba(0, 0, 0, 0.1);
                padding: 2px 8px;
                border-radius: 10px;
                font-size: 0.85em;
            }
            
            /* Capsules Grid */
            .capsules-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
                gap: 20px;
            }
            
            .capsule-card {
                background: white;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                transition: all 0.3s;
                border-left: 4px solid #667eea;
            }
            
            .capsule-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 4px 15px rgba(0,0,0,0.12);
            }
            
            .capsule-header {
                display: flex;
                align-items: flex-start;
                gap: 12px;
                margin-bottom: 15px;
            }
            
            .capsule-icon {
                font-size: 2em;
            }
            
            .capsule-info {
                flex: 1;
            }
            
            .capsule-name {
                font-size: 1.3em;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
            }
            
            .capsule-id {
                font-size: 0.85em;
                color: #95a5a6;
                font-family: monospace;
            }
            
            .capsule-description {
                color: #7f8c8d;
                line-height: 1.6;
                margin-bottom: 15px;
            }
            
            .capsule-meta {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-top: 15px;
            }
            
            .capsule-badge {
                padding: 5px 12px;
                border-radius: 12px;
                font-size: 0.8em;
                font-weight: 600;
                text-transform: uppercase;
            }
            
            .badge-realm {
                background: #e8eaf6;
                color: #667eea;
            }
            
            .badge-status {
                background: #d4edda;
                color: #155724;
            }
            
            .badge-status.planning {
                background: #fff3cd;
                color: #856404;
            }
            
            .capsule-link {
                display: inline-block;
                margin-top: 15px;
                padding: 8px 16px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-size: 0.9em;
                font-weight: 500;
                transition: opacity 0.3s;
            }
            
            .capsule-link:hover {
                opacity: 0.9;
            }
            
            /* Empty State */
            .empty-state {
                text-align: center;
                padding: 60px 20px;
                color: #95a5a6;
            }
            
            .empty-state-icon {
                font-size: 4em;
                margin-bottom: 20px;
            }
            
            /* Responsive */
            @media (max-width: 768px) {
                .container {
                    padding: 20px;
                }
                
                .filter-buttons {
                    flex-direction: column;
                }
                
                .capsules-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <!-- Header Bar -->
        <div class="header">
            <div class="header-left">
                <div class="logo">👑 Codex Dominion</div>
            </div>
            <a href="/dashboard" class="back-link">← Back to Dashboard</a>
        </div>
        
        <!-- Main Container -->
        <div class="container">
            <h1 class="page-title">🔰 Capsules</h1>
            <p class="page-subtitle">{{ total_count }} capsules across {{ realm_count }} realms</p>
            
            <!-- Realm Filters -->
            <div class="realm-filters">
                <div class="filter-title">Realm Filters</div>
                <div class="filter-buttons">
                    <a href="/dashboard/capsules?realm=all" class="filter-btn {% if selected_realm == 'all' %}active{% endif %}">
                        <span>🌐</span>
                        <span>All Realms</span>
                        <span class="filter-count">{{ total_count }}</span>
                    </a>
                    <a href="/dashboard/capsules?realm=foundation" class="filter-btn {% if selected_realm == 'foundation' %}active{% endif %}">
                        <span>🏛️</span>
                        <span>Foundation</span>
                        <span class="filter-count">{{ realm_counts.foundation }}</span>
                    </a>
                    <a href="/dashboard/capsules?realm=economic" class="filter-btn {% if selected_realm == 'economic' %}active{% endif %}">
                        <span>💰</span>
                        <span>Economic</span>
                        <span class="filter-count">{{ realm_counts.economic }}</span>
                    </a>
                    <a href="/dashboard/capsules?realm=knowledge" class="filter-btn {% if selected_realm == 'knowledge' %}active{% endif %}">
                        <span>📚</span>
                        <span>Knowledge</span>
                        <span class="filter-count">{{ realm_counts.knowledge }}</span>
                    </a>
                    <a href="/dashboard/capsules?realm=community" class="filter-btn {% if selected_realm == 'community' %}active{% endif %}">
                        <span>👥</span>
                        <span>Community</span>
                        <span class="filter-count">{{ realm_counts.community }}</span>
                    </a>
                    <a href="/dashboard/capsules?realm=automation" class="filter-btn {% if selected_realm == 'automation' %}active{% endif %}">
                        <span>⚙️</span>
                        <span>Automation</span>
                        <span class="filter-count">{{ realm_counts.automation }}</span>
                    </a>
                    <a href="/dashboard/capsules?realm=media" class="filter-btn {% if selected_realm == 'media' %}active{% endif %}">
                        <span>🎬</span>
                        <span>Media</span>
                        <span class="filter-count">{{ realm_counts.media }}</span>
                    </a>
                </div>
            </div>
            
            <!-- Capsules Grid -->
            {% if display_capsules %}
            <div class="capsules-grid">
                {% for capsule in display_capsules %}
                <div class="capsule-card" style="border-left-color: {{ capsule.realm_color }};">
                    <div class="capsule-header">
                        <span class="capsule-icon">{{ capsule.realm_icon }}</span>
                        <div class="capsule-info">
                            <div class="capsule-name">{{ capsule.name }}</div>
                            <div class="capsule-id">{{ capsule.id }}</div>
                        </div>
                    </div>
                    
                    <p class="capsule-description">{{ capsule.description or 'No description available' }}</p>
                    
                    <div class="capsule-meta">
                        <span class="capsule-badge badge-realm">{{ capsule.realm }}</span>
                        <span class="capsule-badge badge-status {{ capsule.status or 'operational' }}">
                            {{ capsule.status or 'operational' }}
                        </span>
                    </div>
                    
                    <a href="/dashboard/capsules/{{ capsule.id }}" class="capsule-link">View Details →</a>
                </div>
                {% endfor %}
            </div>
            {% else %}
            <div class="empty-state">
                <div class="empty-state-icon">🔰</div>
                <h3>No capsules found</h3>
                <p>Try selecting a different realm filter</p>
            </div>
            {% endif %}
        </div>
    </body>
    </html>
    """, 
    display_capsules=display_capsules,
    total_count=len(all_capsules),
    realm_count=len(realms_config),
    selected_realm=selected_realm,
    realm_counts=realm_counts)

@app.route('/dashboard/capsules/<capsule_id>')
def dashboard_capsule_detail(capsule_id):
    """Individual capsule detail page with structured layout"""
    # Search platform capsules
    platform_data = load_json("platform_capsules.json")
    engines_data = load_json("engines.json")
    
    capsule = None
    capsule_realm = None
    realm_config = {
        "foundation": {"icon": "🏛️", "color": "#667eea"},
        "economic": {"icon": "💰", "color": "#28a745"},
        "knowledge": {"icon": "📚", "color": "#17a2b8"},
        "community": {"icon": "👥", "color": "#fd7e14"},
        "automation": {"icon": "⚙️", "color": "#6f42c1"},
        "media": {"icon": "🎬", "color": "#e83e8c"}
    }
    
    for realm in realm_config.keys():
        capsules = platform_data.get(realm, [])
        found = next((c for c in capsules if c.get("id") == capsule_id), None)
        if found:
            capsule = found
            capsule_realm = realm
            break
    
    # Search execution capsules if not found
    if not capsule:
        execution_data = load_json("execution_capsules.json")
        exec_capsules = execution_data.get("execution_capsules", [])
        capsule = next((c for c in exec_capsules if c.get("id") == capsule_id), None)
        capsule_realm = "execution"
        if capsule:
            realm_config["execution"] = {"icon": "⚡", "color": "#dc3545"}
    
    if not capsule:
        return "<h1>Capsule Not Found</h1><a href='/dashboard/capsules'>← Back</a>", 404
    
    # Get realm info
    realm_info = realm_config.get(capsule_realm, {"icon": "🔰", "color": "#667eea"})
    
    # Get connected engines info
    connected_engines = []
    if capsule.get("engines"):
        all_engines = engines_data.get("engines", [])
        for engine_id in capsule.get("engines", []):
            engine = next((e for e in all_engines if e.get("id") == engine_id), None)
            if engine:
                connected_engines.append(engine)
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ capsule.name }} | Codex Dominion</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #f5f7fa;
                color: #2c3e50;
            }
            
            /* Header Bar */
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 30px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            .header-left {
                display: flex;
                align-items: center;
                gap: 15px;
            }
            
            .logo {
                font-size: 1.8em;
                font-weight: bold;
            }
            
            .back-link {
                color: white;
                text-decoration: none;
                padding: 8px 15px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 5px;
                transition: background 0.3s;
            }
            
            .back-link:hover {
                background: rgba(255, 255, 255, 0.3);
            }
            
            /* Main Container */
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 30px;
            }
            
            /* Capsule Title Card */
            .title-card {
                background: white;
                border-radius: 12px;
                padding: 30px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                margin-bottom: 25px;
                border-left: 5px solid {{ realm_color }};
            }
            
            .capsule-title {
                display: flex;
                align-items: center;
                gap: 15px;
                margin-bottom: 15px;
            }
            
            .capsule-icon {
                font-size: 3em;
            }
            
            .capsule-name {
                font-size: 2.2em;
                font-weight: bold;
                color: #2c3e50;
            }
            
            .capsule-id-badge {
                font-size: 0.9em;
                color: #95a5a6;
                font-family: monospace;
                background: #f8f9fa;
                padding: 5px 12px;
                border-radius: 6px;
                margin-top: 8px;
                display: inline-block;
            }
            
            /* Info Grid */
            .info-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 25px;
            }
            
            .info-card {
                background: white;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            }
            
            .info-title {
                font-size: 0.85em;
                color: #7f8c8d;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 12px;
                font-weight: 600;
            }
            
            .info-content {
                font-size: 1.2em;
                color: #2c3e50;
                font-weight: 500;
            }
            
            .info-badge {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 8px 16px;
                border-radius: 8px;
                font-weight: 600;
                text-transform: capitalize;
            }
            
            .badge-realm {
                background: {{ realm_color }};
                color: white;
            }
            
            .badge-status {
                background: #d4edda;
                color: #155724;
            }
            
            .badge-status.planned {
                background: #fff3cd;
                color: #856404;
            }
            
            .badge-status.operational {
                background: #d4edda;
                color: #155724;
            }
            
            /* Engines Section */
            .engines-section {
                background: white;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                margin-bottom: 25px;
            }
            
            .section-title {
                font-size: 1.3em;
                color: #2c3e50;
                margin-bottom: 15px;
                font-weight: 600;
            }
            
            .engines-list {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
            }
            
            .engine-tag {
                padding: 8px 16px;
                background: #e8eaf6;
                color: #667eea;
                border-radius: 8px;
                font-weight: 500;
                font-size: 0.95em;
            }
            
            /* Modules Section */
            .modules-section {
                background: white;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            }
            
            .modules-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 15px;
            }
            
            .module-card {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 18px;
                border-left: 3px solid {{ realm_color }};
                transition: all 0.3s;
            }
            
            .module-card:hover {
                background: #ecf0f1;
                transform: translateX(5px);
            }
            
            .module-name {
                font-size: 1.05em;
                font-weight: 600;
                color: #2c3e50;
                margin-bottom: 8px;
            }
            
            .module-description {
                color: #7f8c8d;
                font-size: 0.9em;
                line-height: 1.5;
            }
            
            .module-icon {
                font-size: 1.3em;
                margin-right: 8px;
            }
            
            /* Empty State */
            .empty-state {
                text-align: center;
                padding: 40px;
                color: #95a5a6;
            }
            
            /* Responsive */
            @media (max-width: 768px) {
                .container {
                    padding: 20px;
                }
                
                .capsule-name {
                    font-size: 1.6em;
                }
                
                .info-grid, .modules-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <!-- Header Bar -->
        <div class="header">
            <div class="header-left">
                <div class="logo">👑 Codex Dominion</div>
            </div>
            <a href="/dashboard/capsules" class="back-link">← Back to Capsules</a>
        </div>
        
        <!-- Main Container -->
        <div class="container">
            <!-- Title Card -->
            <div class="title-card">
                <div class="capsule-title">
                    <span class="capsule-icon">{{ realm_icon }}</span>
                    <div>
                        <h1 class="capsule-name">{{ capsule.name }}</h1>
                        <span class="capsule-id-badge">{{ capsule.id }}</span>
                    </div>
                </div>
                
                {% if capsule.description %}
                <p style="color: #7f8c8d; font-size: 1.1em; line-height: 1.6; margin-top: 15px;">
                    {{ capsule.description }}
                </p>
                {% endif %}
            </div>
            
            <!-- Info Grid -->
            <div class="info-grid">
                <div class="info-card">
                    <div class="info-title">Realm</div>
                    <div class="info-content">
                        <span class="info-badge badge-realm">
                            <span>{{ realm_icon }}</span>
                            <span>{{ capsule_realm }}</span>
                        </span>
                    </div>
                </div>
                
                <div class="info-card">
                    <div class="info-title">Status</div>
                    <div class="info-content">
                        <span class="info-badge badge-status {{ capsule.status or 'operational' }}">
                            {{ capsule.status or 'operational' }}
                        </span>
                    </div>
                </div>
            </div>
            
            <!-- Engines Section -->
            {% if connected_engines %}
            <div class="engines-section">
                <h2 class="section-title">🧠 Engines</h2>
                <div class="engines-list">
                    {% for engine in connected_engines %}
                    <a href="/dashboard/intelligence-core/{{ engine.id }}" class="engine-tag" style="text-decoration: none;">
                        {{ engine.name }}
                    </a>
                    {% endfor %}
                </div>
            </div>
            {% elif capsule.engines %}
            <div class="engines-section">
                <h2 class="section-title">🧠 Engines</h2>
                <div class="engines-list">
                    {% for engine_id in capsule.engines %}
                    <span class="engine-tag">{{ engine_id }}</span>
                    {% endfor %}
                </div>
            </div>
            {% endif %}
            
            <!-- Modules Section -->
            {% if capsule.modules %}
            <div class="modules-section">
                <h2 class="section-title">⚙️ Modules</h2>
                <div class="modules-grid">
                    {% for module in capsule.modules %}
                    <div class="module-card">
                        <div class="module-name">
                            <span class="module-icon">📦</span>
                            {{ module.name }}
                        </div>
                        {% if module.description %}
                        <p class="module-description">{{ module.description }}</p>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% else %}
            <div class="modules-section">
                <h2 class="section-title">⚙️ Modules</h2>
                <div class="empty-state">
                    <p>No modules defined yet</p>
                </div>
            </div>
            {% endif %}
        </div>
    </body>
    </html>
    """, 
    capsule=capsule, 
    capsule_realm=capsule_realm,
    realm_icon=realm_info["icon"],
    realm_color=realm_info["color"],
    connected_engines=connected_engines)

@app.route('/dashboard/intelligence-core')
def dashboard_intelligence_core():
    """Intelligence Core engines page with professional layout"""
    engines_data = load_json("engines.json")
    engines = engines_data.get("engines", [])
    
    # Organize engines by category
    categories = {}
    for engine in engines:
        category = engine.get("category", "uncategorized")
        if category not in categories:
            categories[category] = []
        categories[category].append(engine)
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Intelligence Core | Codex Dominion</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #f5f7fa;
                color: #2c3e50;
            }
            
            /* Header Bar */
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 30px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            .header-left {
                display: flex;
                align-items: center;
                gap: 15px;
            }
            
            .logo {
                font-size: 1.8em;
                font-weight: bold;
            }
            
            .back-link {
                color: white;
                text-decoration: none;
                padding: 8px 15px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 5px;
                transition: background 0.3s;
            }
            
            .back-link:hover {
                background: rgba(255, 255, 255, 0.3);
            }
            
            /* Main Container */
            .container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 30px;
            }
            
            .page-title {
                font-size: 2em;
                color: #2c3e50;
                margin-bottom: 10px;
            }
            
            .page-subtitle {
                color: #7f8c8d;
                font-size: 1.1em;
                margin-bottom: 30px;
            }
            
            /* Engines Grid */
            .engines-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
                gap: 20px;
            }
            
            .engine-card {
                background: white;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                transition: all 0.3s;
                border-left: 4px solid #667eea;
            }
            
            .engine-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 4px 15px rgba(0,0,0,0.12);
            }
            
            .engine-header {
                display: flex;
                align-items: flex-start;
                gap: 12px;
                margin-bottom: 15px;
            }
            
            .engine-icon {
                font-size: 2em;
            }
            
            .engine-info {
                flex: 1;
            }
            
            .engine-name {
                font-size: 1.3em;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
            }
            
            .engine-id {
                font-size: 0.85em;
                color: #95a5a6;
                font-family: monospace;
            }
            
            .engine-description {
                color: #7f8c8d;
                line-height: 1.6;
                margin-bottom: 15px;
            }
            
            .engine-meta {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-top: 15px;
            }
            
            .engine-badge {
                padding: 5px 12px;
                border-radius: 12px;
                font-size: 0.8em;
                font-weight: 600;
                text-transform: uppercase;
            }
            
            .badge-category {
                background: #e8eaf6;
                color: #667eea;
            }
            
            .badge-status {
                background: #d4edda;
                color: #155724;
            }
            
            .badge-status.inactive {
                background: #f8d7da;
                color: #721c24;
            }
            
            .engine-link {
                display: inline-block;
                margin-top: 15px;
                padding: 8px 16px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-size: 0.9em;
                font-weight: 500;
                transition: opacity 0.3s;
            }
            
            .engine-link:hover {
                opacity: 0.9;
            }
            
            /* Empty State */
            .empty-state {
                text-align: center;
                padding: 60px 20px;
                color: #95a5a6;
            }
            
            .empty-state-icon {
                font-size: 4em;
                margin-bottom: 20px;
            }
            
            /* Responsive */
            @media (max-width: 768px) {
                .container {
                    padding: 20px;
                }
                
                .engines-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <!-- Header Bar -->
        <div class="header">
            <div class="header-left">
                <div class="logo">👑 Codex Dominion</div>
            </div>
            <a href="/dashboard" class="back-link">← Back to Dashboard</a>
        </div>
        
        <!-- Main Container -->
        <div class="container">
            <h1 class="page-title">🧠 Intelligence Core</h1>
            <p class="page-subtitle">{{ total }} processing engines across {{ category_count }} categories</p>
            
            <!-- Engines Grid -->
            {% if engines %}
            <div class="engines-grid">
                {% for engine in engines %}
                <div class="engine-card">
                    <div class="engine-header">
                        <span class="engine-icon">🧠</span>
                        <div class="engine-info">
                            <div class="engine-name">{{ engine.name }}</div>
                            <div class="engine-id">{{ engine.id }}</div>
                        </div>
                    </div>
                    
                    <p class="engine-description">{{ engine.description or 'No description available' }}</p>
                    
                    <div class="engine-meta">
                        {% if engine.category %}
                        <span class="engine-badge badge-category">{{ engine.category }}</span>
                        {% endif %}
                        <span class="engine-badge badge-status {{ engine.status or 'active' }}">
                            {{ engine.status or 'active' }}
                        </span>
                    </div>
                    
                    <a href="/dashboard/intelligence-core/{{ engine.id }}" class="engine-link">View Details →</a>
                </div>
                {% endfor %}
            </div>
            {% else %}
            <div class="empty-state">
                <div class="empty-state-icon">🧠</div>
                <h3>No engines found</h3>
                <p>Intelligence Core is empty</p>
            </div>
            {% endif %}
        </div>
    </body>
    </html>
    """, 
    engines=engines, 
    total=len(engines),
    category_count=len(categories))

@app.route('/dashboard/intelligence-core/<engine_id>')
def dashboard_engine_detail(engine_id):
    """Individual engine detail page with capabilities and capsule connections"""
    engines_data = load_json("engines.json")
    platform_data = load_json("platform_capsules.json")
    
    engines = engines_data.get("engines", [])
    engine = next((e for e in engines if e.get("id") == engine_id), None)
    
    if not engine:
        return "<h1>Engine Not Found</h1><a href='/dashboard/intelligence-core'>← Back</a>", 404
    
    # Get connected capsules (both primary and secondary)
    primary_capsules = []
    secondary_capsules = []
    
    # Search through all realm capsules
    for realm in ["foundation", "economic", "knowledge", "community", "automation", "media"]:
        capsules = platform_data.get(realm, [])
        for capsule in capsules:
            capsule_engines = capsule.get("engines", [])
            if engine_id in capsule_engines:
                # Check if it's declared as primary
                declared_engines = capsule.get("declared_engines", [])
                if engine_id in declared_engines:
                    primary_capsules.append({
                        "id": capsule.get("id"),
                        "name": capsule.get("name"),
                        "realm": realm
                    })
                else:
                    secondary_capsules.append({
                        "id": capsule.get("id"),
                        "name": capsule.get("name"),
                        "realm": realm
                    })
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ engine.name }} | Codex Dominion</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #f5f7fa;
                color: #2c3e50;
            }
            
            /* Header Bar */
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 30px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            .header-left {
                display: flex;
                align-items: center;
                gap: 15px;
            }
            
            .logo {
                font-size: 1.8em;
                font-weight: bold;
            }
            
            .back-link {
                color: white;
                text-decoration: none;
                padding: 8px 15px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 5px;
                transition: background 0.3s;
            }
            
            .back-link:hover {
                background: rgba(255, 255, 255, 0.3);
            }
            
            /* Main Container */
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 30px;
            }
            
            /* Title Card */
            .title-card {
                background: white;
                border-radius: 12px;
                padding: 30px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                margin-bottom: 25px;
                border-left: 5px solid #667eea;
            }
            
            .engine-title {
                display: flex;
                align-items: center;
                gap: 15px;
                margin-bottom: 15px;
            }
            
            .engine-icon {
                font-size: 3em;
            }
            
            .engine-name {
                font-size: 2.2em;
                font-weight: bold;
                color: #2c3e50;
            }
            
            .engine-id-badge {
                font-size: 0.9em;
                color: #95a5a6;
                font-family: monospace;
                background: #f8f9fa;
                padding: 5px 12px;
                border-radius: 6px;
                margin-top: 8px;
                display: inline-block;
            }
            
            .engine-description {
                color: #7f8c8d;
                font-size: 1.1em;
                line-height: 1.6;
                margin-top: 15px;
            }
            
            /* Info Grid */
            .info-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 25px;
            }
            
            .info-card {
                background: white;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            }
            
            .info-title {
                font-size: 0.85em;
                color: #7f8c8d;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 10px;
                font-weight: 600;
            }
            
            .info-content {
                font-size: 1.1em;
                color: #2c3e50;
                font-weight: 600;
            }
            
            .info-badge {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 6px 14px;
                border-radius: 8px;
                font-weight: 600;
                text-transform: capitalize;
                background: #e8eaf6;
                color: #667eea;
            }
            
            /* Capabilities Section */
            .capabilities-section {
                background: white;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                margin-bottom: 25px;
            }
            
            .section-title {
                font-size: 1.3em;
                color: #2c3e50;
                margin-bottom: 15px;
                font-weight: 600;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .capabilities-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 12px;
            }
            
            .capability-item {
                background: #f8f9fa;
                padding: 12px 16px;
                border-radius: 8px;
                border-left: 3px solid #667eea;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 0.95em;
                color: #2c3e50;
                transition: all 0.3s;
            }
            
            .capability-item:hover {
                background: #e8eaf6;
                transform: translateX(5px);
            }
            
            /* Capsules Section */
            .capsules-section {
                background: white;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                margin-bottom: 25px;
            }
            
            .capsules-grid {
                display: grid;
                gap: 12px;
                margin-top: 15px;
            }
            
            .capsule-link {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 15px 20px;
                background: #f8f9fa;
                border-radius: 8px;
                text-decoration: none;
                color: #2c3e50;
                border-left: 3px solid #667eea;
                transition: all 0.3s;
            }
            
            .capsule-link:hover {
                background: #e8eaf6;
                transform: translateX(5px);
                border-left-color: #764ba2;
            }
            
            .capsule-link-content {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .capsule-icon {
                font-size: 1.5em;
            }
            
            .capsule-name {
                font-weight: 600;
            }
            
            .capsule-realm {
                font-size: 0.85em;
                color: #7f8c8d;
                text-transform: capitalize;
            }
            
            .capsule-arrow {
                color: #667eea;
                font-size: 1.2em;
            }
            
            .subsection-title {
                font-size: 1.05em;
                color: #7f8c8d;
                margin-top: 20px;
                margin-bottom: 10px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            /* Empty State */
            .empty-state {
                text-align: center;
                padding: 30px;
                color: #95a5a6;
            }
            
            /* Responsive */
            @media (max-width: 768px) {
                .container {
                    padding: 20px;
                }
                
                .engine-name {
                    font-size: 1.6em;
                }
                
                .info-grid, .capabilities-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <!-- Header Bar -->
        <div class="header">
            <div class="header-left">
                <div class="logo">👑 Codex Dominion</div>
            </div>
            <a href="/dashboard/intelligence-core" class="back-link">← Back to Intelligence Core</a>
        </div>
        
        <!-- Main Container -->
        <div class="container">
            <!-- Title Card -->
            <div class="title-card">
                <div class="engine-title">
                    <span class="engine-icon">🧠</span>
                    <div>
                        <h1 class="engine-name">{{ engine.name }}</h1>
                        <span class="engine-id-badge">{{ engine.id }}</span>
                    </div>
                </div>
                
                {% if engine.description %}
                <p class="engine-description">{{ engine.description }}</p>
                {% endif %}
            </div>
            
            <!-- Info Grid -->
            <div class="info-grid">
                {% if engine.category %}
                <div class="info-card">
                    <div class="info-title">Category</div>
                    <div class="info-content">
                        <span class="info-badge">{{ engine.category }}</span>
                    </div>
                </div>
                {% endif %}
                
                <div class="info-card">
                    <div class="info-title">Status</div>
                    <div class="info-content">
                        <span class="info-badge">{{ engine.status or 'active' }}</span>
                    </div>
                </div>
                
                {% if engine.version %}
                <div class="info-card">
                    <div class="info-title">Version</div>
                    <div class="info-content">{{ engine.version }}</div>
                </div>
                {% endif %}
            </div>
            
            <!-- Capabilities Section -->
            {% if engine.capabilities %}
            <div class="capabilities-section">
                <h2 class="section-title">
                    <span>⚡</span>
                    <span>Capabilities</span>
                </h2>
                <div class="capabilities-grid">
                    {% for capability in engine.capabilities %}
                    <div class="capability-item">{{ capability }}</div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}
            
            <!-- Primary Capsules Section -->
            {% if primary_capsules %}
            <div class="capsules-section">
                <h2 class="section-title">
                    <span>🔰</span>
                    <span>Primary Capsules</span>
                </h2>
                <div class="capsules-grid">
                    {% for capsule in primary_capsules %}
                    <a href="/dashboard/capsules/{{ capsule.id }}" class="capsule-link">
                        <div class="capsule-link-content">
                            <span class="capsule-icon">🔰</span>
                            <div>
                                <div class="capsule-name">{{ capsule.name }}</div>
                                <div class="capsule-realm">{{ capsule.realm }} realm</div>
                            </div>
                        </div>
                        <span class="capsule-arrow">→</span>
                    </a>
                    {% endfor %}
                </div>
            </div>
            {% endif %}
            
            <!-- Secondary Capsules Section -->
            {% if secondary_capsules %}
            <div class="capsules-section">
                <div class="subsection-title">Secondary Capsules</div>
                <div class="capsules-grid">
                    {% for capsule in secondary_capsules %}
                    <a href="/dashboard/capsules/{{ capsule.id }}" class="capsule-link">
                        <div class="capsule-link-content">
                            <span class="capsule-icon">🔰</span>
                            <div>
                                <div class="capsule-name">{{ capsule.name }}</div>
                                <div class="capsule-realm">{{ capsule.realm }} realm</div>
                            </div>
                        </div>
                        <span class="capsule-arrow">→</span>
                    </a>
                    {% endfor %}
                </div>
            </div>
            {% endif %}
            
            {% if not primary_capsules and not secondary_capsules %}
            <div class="capsules-section">
                <h2 class="section-title">
                    <span>🔰</span>
                    <span>Connected Capsules</span>
                </h2>
                <div class="empty-state">
                    <p>No capsules connected to this engine</p>
                </div>
            </div>
            {% endif %}
        </div>
    </body>
    </html>
    """, 
    engine=engine,
    primary_capsules=primary_capsules,
    secondary_capsules=secondary_capsules)

@app.route('/dashboard/industries')
def dashboard_industries():
    """Industries page - Key market sectors for Codex Dominion"""
    
    # Define industries with comprehensive details
    industries = [
        {
            "id": "creator_economy",
            "name": "Creator Economy",
            "icon": "🎨",
            "color": "#e83e8c",
            "description": "Empowering content creators, artists, and influencers with tools for monetization, audience engagement, and digital sovereignty.",
            "key_markets": ["Content Creators", "Digital Artists", "Influencers", "YouTubers", "Podcasters"],
            "capsules": ["Content Creator Suite", "Audience Analytics", "Monetization Engine"],
            "revenue_potential": "High",
            "maturity": "Emerging",
            "mvp_status": "Alpha Testing",
            "mvp_progress": 65,
            "capsule_dependencies": ["personalization_capsule", "social_capsule", "commerce_capsule"],
            "engine_dependencies": ["recommendation_engine", "analytics_engine", "content_engine"],
            "features_ready": 8,
            "features_total": 12,
            "api_health": "Operational",
            "platform_features": [
                {"name": "AI Business Builder", "icon": "🤖", "status": "Beta"},
                {"name": "Creator Monetization", "icon": "💰", "status": "Active"},
                {"name": "Audience Analytics", "icon": "📊", "status": "Active"}
            ]
        },
        {
            "id": "diaspora_commerce",
            "name": "Diaspora Commerce",
            "icon": "🌍",
            "color": "#17a2b8",
            "description": "Connecting diaspora communities with authentic cultural products, services, and experiences from their heritage countries.",
            "key_markets": ["African Diaspora", "Caribbean Communities", "Latin American Networks", "Asian Communities"],
            "capsules": ["Cultural Marketplace", "Identity Preservation", "Global Payment Systems"],
            "revenue_potential": "Very High",
            "maturity": "Growth",
            "mvp_status": "Beta",
            "mvp_progress": 80,
            "capsule_dependencies": ["marketplace_capsule", "identity_capsule", "payment_capsule"],
            "engine_dependencies": ["search_engine", "translation_engine", "payment_engine"],
            "features_ready": 14,
            "features_total": 16,
            "api_health": "Operational",
            "platform_features": [
                {"name": "Cultural Marketplace", "icon": "🛒", "status": "Active"},
                {"name": "Global Payments", "icon": "💳", "status": "Active"},
                {"name": "Translation Engine", "icon": "🌐", "status": "Active"}
            ]
        },
        {
            "id": "youth_entrepreneurship",
            "name": "Youth Entrepreneurship",
            "icon": "🚀",
            "color": "#28a745",
            "description": "Nurturing the next generation of entrepreneurs with education, mentorship, and tools for building sustainable businesses.",
            "key_markets": ["Teen Entrepreneurs", "College Founders", "Young Innovators", "Student Businesses"],
            "capsules": ["Business Education Hub", "Teen Biz Accelerator", "Youth Funding Platform"],
            "revenue_potential": "Medium",
            "maturity": "Developing",
            "mvp_status": "Development",
            "mvp_progress": 45,
            "capsule_dependencies": ["education_capsule", "mentor_capsule", "funding_capsule"],
            "engine_dependencies": ["learning_engine", "matching_engine", "analytics_engine"],
            "features_ready": 6,
            "features_total": 15,
            "api_health": "Limited",
            "platform_features": [
                {"name": "AI Business Builder", "icon": "🤖", "status": "Development"},
                {"name": "Safety Systems", "icon": "🛡️", "status": "Active"},
                {"name": "Parent Dashboard", "icon": "👨‍👩‍👧", "status": "Beta"},
                {"name": "Mentor Matching", "icon": "🤝", "status": "Alpha"}
            ]
        },
        {
            "id": "education",
            "name": "Education",
            "icon": "📚",
            "color": "#667eea",
            "description": "Transforming learning experiences with personalized, engaging, and culturally relevant educational content and platforms.",
            "key_markets": ["K-12 Students", "Homeschool Families", "Adult Learners", "Professional Development"],
            "capsules": ["Learning Management", "Curriculum Builder", "Assessment Tools", "Student Analytics"],
            "revenue_potential": "Very High",
            "maturity": "Established",
            "mvp_status": "Production",
            "mvp_progress": 95,
            "capsule_dependencies": ["learning_capsule", "content_capsule", "assessment_capsule", "analytics_capsule"],
            "engine_dependencies": ["learning_engine", "recommendation_engine", "analytics_engine", "content_engine"],
            "features_ready": 18,
            "features_total": 20,
            "api_health": "Operational",
            "platform_features": [
                {"name": "Curriculum Modules", "icon": "📖", "status": "Active"},
                {"name": "Parent Dashboard", "icon": "👨‍👩‍👧", "status": "Active"},
                {"name": "Safety Systems", "icon": "🛡️", "status": "Active"},
                {"name": "Progress Tracking", "icon": "📈", "status": "Active"}
            ]
        },
        {
            "id": "media_culture",
            "name": "Media & Culture",
            "icon": "🎬",
            "color": "#fd7e14",
            "description": "Celebrating and amplifying diverse cultural narratives through digital media, entertainment, and storytelling platforms.",
            "key_markets": ["Digital Publishers", "Cultural Organizations", "Media Production", "Entertainment Networks"],
            "capsules": ["Content Distribution", "Cultural Archive", "Media Analytics", "Audience Engagement"],
            "revenue_potential": "High",
            "maturity": "Growth",
            "mvp_status": "Beta",
            "mvp_progress": 70,
            "capsule_dependencies": ["content_capsule", "distribution_capsule", "analytics_capsule", "social_capsule"],
            "engine_dependencies": ["content_engine", "distribution_engine", "analytics_engine", "recommendation_engine"],
            "features_ready": 11,
            "features_total": 14,
            "api_health": "Operational",
            "platform_features": [
                {"name": "Content Distribution", "icon": "📡", "status": "Active"},
                {"name": "Media Analytics", "icon": "📊", "status": "Active"},
                {"name": "Cultural Archive", "icon": "🏛️", "status": "Beta"}
            ]
        }
    ]
    
    # Calculate summary statistics
    total_industries = len(industries)
    high_potential = sum(1 for i in industries if i["revenue_potential"] in ["High", "Very High"])
    total_markets = sum(len(i["key_markets"]) for i in industries)
    total_capsules = sum(len(i["capsules"]) for i in industries)
    
    # Capsule Readiness Heatmap Data
    capsule_heatmap = [
        {"industry": "Education", "readiness": 95, "capsules": 4, "status": "excellent"},
        {"industry": "Diaspora", "readiness": 80, "capsules": 3, "status": "good"},
        {"industry": "Media", "readiness": 70, "capsules": 4, "status": "good"},
        {"industry": "Creator", "readiness": 65, "capsules": 3, "status": "fair"},
        {"industry": "Youth", "readiness": 45, "capsules": 3, "status": "needs-attention"}
    ]
    
    # Engine Activity Logs
    engine_logs = [
        {"time": "2m ago", "engine": "recommendation_engine", "action": "Processed 1,247 recommendations", "status": "success"},
        {"time": "5m ago", "engine": "analytics_engine", "action": "Generated weekly report", "status": "success"},
        {"time": "8m ago", "engine": "content_engine", "action": "Indexed 523 new items", "status": "success"},
        {"time": "12m ago", "engine": "learning_engine", "action": "Updated curriculum paths", "status": "success"},
        {"time": "15m ago", "engine": "search_engine", "action": "Rebuilt search index", "status": "warning"}
    ]
    
    # Platform Performance Metrics
    platform_metrics = {
        "uptime": "99.98%",
        "response_time": "142ms",
        "requests_per_min": "3,847",
        "active_users": "12,456",
        "cpu_usage": "34%",
        "memory_usage": "58%"
    }
    
    # Data Pipeline Status
    pipeline_status = [
        {"name": "User Analytics Pipeline", "status": "operational", "last_run": "2m ago", "throughput": "15k/min"},
        {"name": "Content Ingestion", "status": "operational", "last_run": "5m ago", "throughput": "8k/min"},
        {"name": "Revenue Tracking", "status": "operational", "last_run": "1m ago", "throughput": "2k/min"},
        {"name": "Social Media Sync", "status": "degraded", "last_run": "8m ago", "throughput": "500/min"},
        {"name": "ML Model Training", "status": "operational", "last_run": "30m ago", "throughput": "N/A"}
    ]
    
    # API Call Tracking
    api_calls = [
        {"endpoint": "/api/treasury/summary", "method": "GET", "calls": "1,247", "avg_response": "45ms", "status": "healthy"},
        {"endpoint": "/api/capsules/execute", "method": "POST", "calls": "892", "avg_response": "230ms", "status": "healthy"},
        {"endpoint": "/api/intelligence/query", "method": "POST", "calls": "634", "avg_response": "89ms", "status": "healthy"},
        {"endpoint": "/api/dawn/dispatch", "method": "POST", "calls": "156", "avg_response": "312ms", "status": "warning"},
        {"endpoint": "/api/portfolio/analyze", "method": "GET", "calls": "423", "avg_response": "178ms", "status": "healthy"}
    ]
    
    # Error Logs
    error_logs = [
        {"time": "3m ago", "level": "warning", "source": "capsule_executor", "message": "Retry attempt 2/3 for content_capsule", "resolved": False},
        {"time": "7m ago", "level": "error", "source": "api_gateway", "message": "Rate limit exceeded for user_12456", "resolved": True},
        {"time": "11m ago", "level": "warning", "source": "recommendation_engine", "message": "Low confidence score (0.45) for recommendation set", "resolved": False},
        {"time": "18m ago", "level": "error", "source": "database_connector", "message": "Connection timeout to analytics DB", "resolved": True},
        {"time": "22m ago", "level": "info", "source": "security_monitor", "message": "3 failed login attempts detected", "resolved": True}
    ]
    
    # Detailed Engine Activity
    engine_activity_detail = [
        {"engine": "recommendation_engine", "uptime": "99.9%", "requests": "12.4k", "avg_latency": "67ms", "cache_hits": "89%", "status": "optimal"},
        {"engine": "analytics_engine", "uptime": "100%", "requests": "8.2k", "avg_latency": "45ms", "cache_hits": "92%", "status": "optimal"},
        {"engine": "content_engine", "uptime": "98.7%", "requests": "15.1k", "avg_latency": "123ms", "cache_hits": "76%", "status": "good"},
        {"engine": "learning_engine", "uptime": "99.5%", "requests": "5.6k", "avg_latency": "89ms", "cache_hits": "84%", "status": "good"},
        {"engine": "search_engine", "uptime": "97.2%", "requests": "18.9k", "avg_latency": "156ms", "cache_hits": "71%", "status": "degraded"}
    ]
    
    # Capsule Load Events
    capsule_load_events = [
        {"time": "1m ago", "capsule": "treasury_audit", "action": "Loaded successfully", "load_time": "1.2s", "status": "success"},
        {"time": "4m ago", "capsule": "content_creator_suite", "action": "Hot reload triggered", "load_time": "0.8s", "status": "success"},
        {"time": "6m ago", "capsule": "personalization_capsule", "action": "Dependencies resolved", "load_time": "2.1s", "status": "success"},
        {"time": "9m ago", "capsule": "education_matrix", "action": "Configuration updated", "load_time": "1.5s", "status": "success"},
        {"time": "13m ago", "capsule": "cultural_marketplace", "action": "Failed initial load, retrying", "load_time": "3.4s", "status": "warning"}
    ]
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Industries | Codex Dominion Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #f7f1e3 0%, #efe7d4 100%);
                color: #333;
                line-height: 1.6;
            }
            
            /* Header Bar */
            .header-bar {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px 40px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                position: sticky;
                top: 0;
                z-index: 100;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .header-bar h1 {
                font-size: 1.8em;
                font-weight: 600;
                display: flex;
                align-items: center;
                gap: 15px;
            }
            
            .header-bar .logo {
                font-size: 2em;
            }
            
            .back-link {
                background: rgba(255,255,255,0.2);
                color: white;
                padding: 10px 24px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 500;
                transition: all 0.3s;
                border: 2px solid transparent;
            }
            
            .back-link:hover {
                background: white;
                color: #667eea;
                border-color: white;
                transform: translateX(-5px);
            }
            
            /* Main Content */
            .container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 40px;
            }
            
            /* Overview Section */
            .overview-section {
                background: white;
                border-radius: 16px;
                padding: 30px;
                margin-bottom: 40px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            }
            
            .overview-section h2 {
                color: #667eea;
                font-size: 1.6em;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            
            .stat-card {
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                padding: 20px;
                border-radius: 12px;
                text-align: center;
                border-left: 4px solid #667eea;
            }
            
            .stat-value {
                font-size: 2.5em;
                font-weight: bold;
                color: #667eea;
                display: block;
            }
            
            .stat-label {
                color: #6c757d;
                font-size: 0.95em;
                margin-top: 8px;
            }
            
            /* Industries Grid */
            .industries-section {
                margin-top: 30px;
            }
            
            .industries-section h2 {
                color: #333;
                font-size: 1.8em;
                margin-bottom: 25px;
                padding-bottom: 15px;
                border-bottom: 3px solid #667eea;
            }
            
            .industries-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
                gap: 30px;
            }
            
            .industry-card {
                background: white;
                border-radius: 16px;
                padding: 30px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                transition: all 0.3s;
                border-left: 6px solid #667eea;
                position: relative;
                overflow: hidden;
            }
            
            .industry-card:hover {
                transform: translateY(-8px);
                box-shadow: 0 8px 30px rgba(0,0,0,0.15);
            }
            
            .industry-header {
                display: flex;
                align-items: center;
                gap: 15px;
                margin-bottom: 20px;
            }
            
            .industry-icon {
                font-size: 3em;
                line-height: 1;
            }
            
            .industry-title h3 {
                font-size: 1.5em;
                color: #333;
                margin-bottom: 5px;
            }
            
            .industry-id {
                font-size: 0.75em;
                color: #6c757d;
                font-family: 'Consolas', monospace;
                background: #f8f9fa;
                padding: 4px 10px;
                border-radius: 6px;
                display: inline-block;
            }
            
            .industry-description {
                color: #555;
                font-size: 1em;
                margin-bottom: 20px;
                line-height: 1.7;
            }
            
            .industry-details {
                margin-top: 20px;
            }
            
            .detail-section {
                margin-bottom: 18px;
            }
            
            .detail-label {
                font-weight: 600;
                color: #667eea;
                font-size: 0.9em;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 8px;
                display: block;
            }
            
            .detail-content {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
            }
            
            .tag {
                background: #f8f9fa;
                color: #495057;
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 0.85em;
                border: 1px solid #dee2e6;
                transition: all 0.2s;
            }
            
            .tag:hover {
                background: #e9ecef;
                border-color: #667eea;
                color: #667eea;
            }
            
            .industry-footer {
                margin-top: 20px;
                padding-top: 20px;
                border-top: 1px solid #e9ecef;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .badge {
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 0.85em;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .badge-potential {
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                color: white;
            }
            
            .badge-maturity {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            
            /* MVP Status Section */
            .mvp-section {
                margin: 20px 0;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }
            
            .mvp-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
            }
            
            .mvp-status {
                font-weight: 600;
                color: #667eea;
                font-size: 0.9em;
            }
            
            .mvp-percentage {
                font-weight: bold;
                color: #28a745;
            }
            
            .progress-bar {
                width: 100%;
                height: 8px;
                background: #e9ecef;
                border-radius: 4px;
                overflow: hidden;
            }
            
            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                transition: width 0.5s ease;
            }
            
            /* Dependencies Section */
            .dependencies-section {
                margin-top: 20px;
                padding-top: 20px;
                border-top: 1px solid #e9ecef;
            }
            
            .dependency-group {
                margin-bottom: 15px;
            }
            
            .dependency-label {
                font-weight: 600;
                color: #495057;
                font-size: 0.85em;
                margin-bottom: 8px;
                display: block;
            }
            
            .dependency-tags {
                display: flex;
                flex-wrap: wrap;
                gap: 6px;
            }
            
            .dependency-tag {
                background: #e9ecef;
                color: #495057;
                padding: 4px 10px;
                border-radius: 12px;
                font-size: 0.75em;
                font-family: 'Consolas', monospace;
                border: 1px solid #dee2e6;
            }
            
            /* Feature Readiness */
            .feature-readiness {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px;
                background: #fff3cd;
                border-radius: 8px;
                margin-top: 15px;
                border-left: 4px solid #ffc107;
            }
            
            .feature-label {
                font-weight: 600;
                color: #856404;
                font-size: 0.9em;
            }
            
            .feature-count {
                font-weight: bold;
                color: #856404;
                font-size: 1.1em;
            }
            
            /* API Health Badge */
            .api-health {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 0.8em;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .api-health.operational {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            
            .api-health.limited {
                background: #fff3cd;
                color: #856404;
                border: 1px solid #ffeeba;
            }
            
            .api-health.degraded {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            
            .health-indicator {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                display: inline-block;
            }
            
            .health-indicator.operational {
                background: #28a745;
            }
            
            .health-indicator.limited {
                background: #ffc107;
            }
            
            .health-indicator.degraded {
                background: #dc3545;
            }
            
            /* Platform Features Section */
            .platform-features {
                margin-top: 20px;
                padding: 15px;
                background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
                border-radius: 8px;
                border: 1px solid #bbdefb;
            }
            
            .platform-features-title {
                font-weight: 600;
                color: #1976d2;
                font-size: 0.9em;
                margin-bottom: 12px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .features-list {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 10px;
            }
            
            .feature-item {
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 10px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.08);
                transition: all 0.3s;
            }
            
            .feature-item:hover {
                transform: translateY(-3px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }
            
            .feature-icon {
                font-size: 1.5em;
            }
            
            .feature-info {
                flex: 1;
            }
            
            .feature-name {
                font-weight: 600;
                font-size: 0.85em;
                color: #333;
                line-height: 1.2;
            }
            
            .feature-status {
                font-size: 0.7em;
                color: #6c757d;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-top: 2px;
            }
            
            .feature-status.active {
                color: #28a745;
                font-weight: 600;
            }
            
            .feature-status.beta {
                color: #17a2b8;
                font-weight: 600;
            }
            
            .feature-status.alpha {
                color: #ffc107;
                font-weight: 600;
            }
            
            .feature-status.development {
                color: #dc3545;
                font-weight: 600;
            }
            
            /* Monitoring Sections */
            .monitoring-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
                gap: 30px;
                margin-top: 40px;
            }
            
            .monitoring-card {
                background: white;
                border-radius: 16px;
                padding: 25px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            }
            
            .monitoring-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 2px solid #e9ecef;
            }
            
            .monitoring-title {
                font-size: 1.3em;
                font-weight: 600;
                color: #333;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .refresh-badge {
                font-size: 0.7em;
                color: #6c757d;
                background: #f8f9fa;
                padding: 4px 10px;
                border-radius: 12px;
            }
            
            /* Heatmap */
            .heatmap-row {
                display: grid;
                grid-template-columns: 150px 1fr 80px 120px;
                gap: 15px;
                align-items: center;
                padding: 12px;
                margin-bottom: 10px;
                border-radius: 8px;
                background: #f8f9fa;
                transition: all 0.3s;
            }
            
            .heatmap-row:hover {
                background: #e9ecef;
                transform: translateX(5px);
            }
            
            .heatmap-label {
                font-weight: 600;
                color: #333;
            }
            
            .heatmap-bar {
                height: 24px;
                background: #e9ecef;
                border-radius: 12px;
                overflow: hidden;
                position: relative;
            }
            
            .heatmap-fill {
                height: 100%;
                border-radius: 12px;
                transition: width 0.5s ease;
                display: flex;
                align-items: center;
                justify-content: flex-end;
                padding-right: 10px;
                color: white;
                font-size: 0.8em;
                font-weight: 600;
            }
            
            .heatmap-fill.excellent { background: linear-gradient(90deg, #28a745, #20c997); }
            .heatmap-fill.good { background: linear-gradient(90deg, #17a2b8, #5bc0de); }
            .heatmap-fill.fair { background: linear-gradient(90deg, #ffc107, #ffdd57); }
            .heatmap-fill.needs-attention { background: linear-gradient(90deg, #fd7e14, #ff6b6b); }
            
            .heatmap-count {
                font-size: 0.9em;
                color: #6c757d;
            }
            
            .heatmap-status {
                font-size: 0.75em;
                padding: 4px 10px;
                border-radius: 12px;
                font-weight: 600;
                text-transform: uppercase;
            }
            
            .heatmap-status.excellent { background: #d4edda; color: #155724; }
            .heatmap-status.good { background: #d1ecf1; color: #0c5460; }
            .heatmap-status.fair { background: #fff3cd; color: #856404; }
            .heatmap-status.needs-attention { background: #f8d7da; color: #721c24; }
            
            /* Activity Logs */
            .log-entry {
                display: flex;
                align-items: flex-start;
                gap: 15px;
                padding: 12px;
                margin-bottom: 10px;
                border-left: 4px solid #28a745;
                background: #f8f9fa;
                border-radius: 8px;
                transition: all 0.3s;
            }
            
            .log-entry:hover {
                background: #e9ecef;
                transform: translateX(5px);
            }
            
            .log-entry.warning { border-left-color: #ffc107; }
            .log-entry.error { border-left-color: #dc3545; }
            
            .log-time {
                font-size: 0.8em;
                color: #6c757d;
                min-width: 60px;
                font-weight: 600;
            }
            
            .log-engine {
                font-family: 'Consolas', monospace;
                font-size: 0.85em;
                background: #e9ecef;
                padding: 4px 10px;
                border-radius: 6px;
                color: #495057;
                min-width: 180px;
            }
            
            .log-action {
                flex: 1;
                color: #333;
                font-size: 0.9em;
            }
            
            .log-status {
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: #28a745;
            }
            
            .log-status.warning { background: #ffc107; }
            .log-status.error { background: #dc3545; }
            
            /* Performance Metrics */
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 15px;
            }
            
            .metric-box {
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                padding: 20px;
                border-radius: 12px;
                text-align: center;
                border-left: 4px solid #667eea;
            }
            
            .metric-value {
                font-size: 2em;
                font-weight: bold;
                color: #667eea;
                display: block;
                margin-bottom: 8px;
            }
            
            .metric-label {
                font-size: 0.85em;
                color: #6c757d;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            /* Pipeline Status */
            .pipeline-item {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 15px;
                margin-bottom: 12px;
                background: #f8f9fa;
                border-radius: 8px;
                border-left: 4px solid #28a745;
                transition: all 0.3s;
            }
            
            .pipeline-item:hover {
                background: #e9ecef;
                transform: translateX(5px);
            }
            
            .pipeline-item.degraded { border-left-color: #ffc107; }
            .pipeline-item.failed { border-left-color: #dc3545; }
            
            .pipeline-name {
                font-weight: 600;
                color: #333;
                flex: 1;
            }
            
            .pipeline-meta {
                display: flex;
                gap: 20px;
                align-items: center;
                font-size: 0.85em;
                color: #6c757d;
            }
            
            .pipeline-badge {
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 0.75em;
                font-weight: 600;
                text-transform: uppercase;
            }
            
            .pipeline-badge.operational { background: #d4edda; color: #155724; }
            .pipeline-badge.degraded { background: #fff3cd; color: #856404; }
            .pipeline-badge.failed { background: #f8d7da; color: #721c24; }
            
            /* Developer Tools Panel */
            .dev-tools-panel {
                position: fixed;
                top: 0;
                right: -400px;
                width: 400px;
                height: 100vh;
                background: white;
                box-shadow: -4px 0 20px rgba(0,0,0,0.15);
                z-index: 10000;
                transition: right 0.3s ease;
                overflow-y: auto;
            }
            
            .dev-tools-panel.active {
                right: 0;
            }
            
            .dev-tools-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                position: sticky;
                top: 0;
                z-index: 10;
            }
            
            .dev-tools-close {
                background: rgba(255,255,255,0.2);
                border: none;
                color: white;
                width: 32px;
                height: 32px;
                border-radius: 50%;
                cursor: pointer;
                font-size: 1.2em;
                transition: all 0.3s;
            }
            
            .dev-tools-close:hover {
                background: rgba(255,255,255,0.3);
                transform: rotate(90deg);
            }
            
            .dev-tools-content {
                padding: 20px;
            }
            
            .dev-tool-section {
                margin-bottom: 25px;
                padding-bottom: 25px;
                border-bottom: 1px solid #e9ecef;
            }
            
            .dev-tool-section:last-child {
                border-bottom: none;
            }
            
            .dev-tool-label {
                display: block;
                font-weight: 600;
                color: #333;
                margin-bottom: 12px;
                font-size: 0.95em;
            }
            
            .theme-toggle {
                display: flex;
                gap: 10px;
            }
            
            .theme-btn {
                flex: 1;
                padding: 12px;
                border: 2px solid #e9ecef;
                background: white;
                border-radius: 8px;
                cursor: pointer;
                font-size: 0.95em;
                font-weight: 600;
                transition: all 0.3s;
            }
            
            .theme-btn:hover {
                border-color: #667eea;
                transform: translateY(-2px);
            }
            
            .theme-btn.active {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-color: #667eea;
            }
            
            .env-display {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
            }
            
            .env-item {
                display: flex;
                justify-content: space-between;
                padding: 8px 0;
                border-bottom: 1px solid #e9ecef;
            }
            
            .env-item:last-child {
                border-bottom: none;
            }
            
            .env-key {
                font-weight: 600;
                color: #6c757d;
                font-size: 0.9em;
            }
            
            .env-value {
                font-family: 'Consolas', monospace;
                color: #333;
                font-weight: 600;
            }
            
            .dev-action-btn {
                width: 100%;
                padding: 12px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                font-size: 0.95em;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                transition: all 0.3s;
            }
            
            .dev-action-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            }
            
            .dev-action-btn:active {
                transform: translateY(0);
            }
            
            .reload-status {
                margin-top: 10px;
                padding: 10px;
                border-radius: 6px;
                font-size: 0.85em;
                font-weight: 600;
                text-align: center;
                display: none;
            }
            
            .reload-status.success {
                background: #d4edda;
                color: #155724;
                display: block;
            }
            
            .reload-status.error {
                background: #f8d7da;
                color: #721c24;
                display: block;
            }
            
            .dev-actions-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
            }
            
            .dev-action-btn-small {
                padding: 10px;
                background: white;
                border: 2px solid #e9ecef;
                border-radius: 6px;
                cursor: pointer;
                font-size: 0.85em;
                font-weight: 600;
                transition: all 0.3s;
            }
            
            .dev-action-btn-small:hover {
                border-color: #667eea;
                background: #f8f9fa;
                transform: translateY(-2px);
            }
            
            .system-info {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
            }
            
            .info-item {
                padding: 6px 0;
                font-size: 0.85em;
                color: #6c757d;
            }
            
            .info-item span {
                color: #333;
                font-weight: 600;
                font-family: 'Consolas', monospace;
            }
            
            .dev-tools-toggle {
                position: fixed;
                bottom: 30px;
                right: 30px;
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 50%;
                font-size: 1.5em;
                cursor: pointer;
                box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
                z-index: 9999;
                transition: all 0.3s;
            }
            
            .dev-tools-toggle:hover {
                transform: scale(1.1) rotate(15deg);
                box-shadow: 0 6px 25px rgba(102, 126, 234, 0.5);
            }
            
            .dev-tools-toggle:active {
                transform: scale(0.95);
            }
            
            /* Dark Theme */
            body.dark-theme {
                background: #1a1a2e;
                color: #eee;
            }
            
            body.dark-theme .header-bar {
                background: linear-gradient(135deg, #2d3561 0%, #3d2a54 100%);
            }
            
            body.dark-theme .container {
                background: transparent;
            }
            
            body.dark-theme .stat-card,
            body.dark-theme .industry-card,
            body.dark-theme .monitoring-card {
                background: #16213e;
                border-color: #0f3460;
                color: #eee;
            }
            
            body.dark-theme .monitoring-header,
            body.dark-theme .industry-header {
                color: #eee;
            }
            
            body.dark-theme .mvp-section,
            body.dark-theme .dependencies-section,
            body.dark-theme .platform-features {
                background: #0f3460;
            }
            
            body.dark-theme .heatmap-row,
            body.dark-theme .log-entry,
            body.dark-theme .pipeline-item,
            body.dark-theme .error-log-item,
            body.dark-theme .engine-detail-grid,
            body.dark-theme .capsule-event {
                background: #0f3460;
                color: #eee;
            }
            
            body.dark-theme .api-calls-table tr:hover {
                background: #0f3460;
            }
            
            body.dark-theme .back-link {
                color: white;
            }
            
            body.dark-theme .dev-tools-panel {
                background: #16213e;
                color: #eee;
            }
            
            body.dark-theme .env-display,
            body.dark-theme .system-info {
                background: #0f3460;
            }
            
            body.dark-theme .dev-action-btn-small {
                background: #0f3460;
                border-color: #0f3460;
                color: #eee;
            }
            
            body.dark-theme .theme-btn {
                background: #0f3460;
                border-color: #0f3460;
                color: #eee;
            }
            
            /* API Calls Monitoring */
            .api-calls-table {
                width: 100%;
                border-collapse: collapse;
            }
            
            .api-calls-table th {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: 600;
                font-size: 0.85em;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .api-calls-table td {
                padding: 12px;
                border-bottom: 1px solid #e9ecef;
                font-size: 0.9em;
            }
            
            .api-calls-table tr:hover {
                background: #f8f9fa;
            }
            
            .api-method {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 0.75em;
                font-weight: 600;
                font-family: 'Consolas', monospace;
            }
            
            .api-method.GET { background: #d4edda; color: #155724; }
            .api-method.POST { background: #cce5ff; color: #004085; }
            .api-method.PUT { background: #fff3cd; color: #856404; }
            .api-method.DELETE { background: #f8d7da; color: #721c24; }
            
            .api-status-healthy { color: #28a745; font-weight: 600; }
            .api-status-warning { color: #ffc107; font-weight: 600; }
            .api-status-error { color: #dc3545; font-weight: 600; }
            
            /* Error Logs */
            .error-log-item {
                display: flex;
                align-items: flex-start;
                gap: 12px;
                padding: 12px;
                margin-bottom: 10px;
                background: #f8f9fa;
                border-radius: 8px;
                border-left: 4px solid #dc3545;
                transition: all 0.3s;
            }
            
            .error-log-item:hover {
                background: #e9ecef;
                transform: translateX(5px);
            }
            
            .error-log-item.warning { border-left-color: #ffc107; }
            .error-log-item.info { border-left-color: #17a2b8; }
            
            .error-level {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 0.75em;
                font-weight: 600;
                text-transform: uppercase;
            }
            
            .error-level.error { background: #dc3545; color: white; }
            .error-level.warning { background: #ffc107; color: #856404; }
            .error-level.info { background: #17a2b8; color: white; }
            
            .error-resolved {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 0.75em;
                font-weight: 600;
            }
            
            .error-resolved.true { background: #d4edda; color: #155724; }
            .error-resolved.false { background: #fff3cd; color: #856404; }
            
            /* Engine Activity Detail */
            .engine-detail-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 15px;
                padding: 12px;
                margin-bottom: 12px;
                background: #f8f9fa;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }
            
            .engine-detail-grid.optimal { border-left-color: #28a745; }
            .engine-detail-grid.good { border-left-color: #17a2b8; }
            .engine-detail-grid.degraded { border-left-color: #ffc107; }
            
            .engine-name-header {
                grid-column: 1 / -1;
                font-weight: 700;
                color: #333;
                font-size: 1.05em;
            }
            
            .engine-stat {
                display: flex;
                flex-direction: column;
                gap: 4px;
            }
            
            .engine-stat-label {
                font-size: 0.75em;
                color: #6c757d;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .engine-stat-value {
                font-size: 1.1em;
                font-weight: 600;
                color: #333;
            }
            
            /* Capsule Load Events */
            .capsule-event {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 12px;
                margin-bottom: 10px;
                background: #f8f9fa;
                border-radius: 8px;
                border-left: 4px solid #28a745;
                transition: all 0.3s;
            }
            
            .capsule-event:hover {
                background: #e9ecef;
                transform: translateX(5px);
            }
            
            .capsule-event.warning { border-left-color: #ffc107; }
            .capsule-event.error { border-left-color: #dc3545; }
            
            .capsule-event-info {
                flex: 1;
            }
            
            .capsule-event-name {
                font-weight: 600;
                color: #333;
                font-family: 'Consolas', monospace;
                font-size: 0.95em;
            }
            
            .capsule-event-action {
                font-size: 0.85em;
                color: #6c757d;
                margin-top: 4px;
            }
            
            .capsule-event-meta {
                display: flex;
                gap: 15px;
                align-items: center;
                font-size: 0.85em;
                color: #6c757d;
            }
            
            .capsule-load-time {
                font-weight: 600;
                color: #667eea;
            }
            
            .capsule-event-status {
                padding: 4px 10px;
                border-radius: 12px;
                font-size: 0.75em;
                font-weight: 600;
                text-transform: uppercase;
            }
            
            .capsule-event-status.success { background: #d4edda; color: #155724; }
            .capsule-event-status.warning { background: #fff3cd; color: #856404; }
            .capsule-event-status.error { background: #f8d7da; color: #721c24; }
            
            /* Responsive Design */
            @media (max-width: 768px) {
                .container {
                    padding: 20px;
                }
                
                .header-bar {
                    padding: 15px 20px;
                    flex-direction: column;
                    gap: 15px;
                }
                
                .header-bar h1 {
                    font-size: 1.4em;
                }
                
                .industries-grid {
                    grid-template-columns: 1fr;
                }
                
                .stats-grid {
                    grid-template-columns: repeat(2, 1fr);
                }
                
                .monitoring-grid {
                    grid-template-columns: 1fr;
                }
                
                .metrics-grid {
                    grid-template-columns: repeat(2, 1fr);
                }
                
                .heatmap-row {
                    grid-template-columns: 1fr;
                }
                
                .features-list {
                    grid-template-columns: 1fr;
                }
                
                .api-calls-table {
                    font-size: 0.85em;
                }
                
                .api-calls-table th,
                .api-calls-table td {
                    padding: 8px 6px;
                }
                
                .engine-detail-grid {
                    grid-template-columns: repeat(2, 1fr);
                }
            }
                
                .monitoring-grid {
                    grid-template-columns: 1fr;
                }
                
                .metrics-grid {
                    grid-template-columns: repeat(2, 1fr);
                }
                
                .heatmap-row {
                    grid-template-columns: 1fr;
                    gap: 8px;
                }
                
                .features-list {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <!-- Developer Tools Panel (Fixed) -->
        <div id="devToolsPanel" class="dev-tools-panel">
            <div class="dev-tools-header">
                <span style="font-weight: 700; font-size: 1.1em;">🛠️ Developer Tools</span>
                <button id="closeDevTools" class="dev-tools-close">✕</button>
            </div>
            <div class="dev-tools-content">
                <!-- Theme Toggle -->
                <div class="dev-tool-section">
                    <label class="dev-tool-label">🎨 Theme</label>
                    <div class="theme-toggle">
                        <button id="lightTheme" class="theme-btn active">☀️ Light</button>
                        <button id="darkTheme" class="theme-btn">🌙 Dark</button>
                    </div>
                </div>
                
                <!-- Environment Config -->
                <div class="dev-tool-section">
                    <label class="dev-tool-label">🌐 Environment</label>
                    <div class="env-display">
                        <div class="env-item">
                            <span class="env-key">Mode:</span>
                            <span class="env-value" id="envMode">Production</span>
                        </div>
                        <div class="env-item">
                            <span class="env-key">Port:</span>
                            <span class="env-value">5000</span>
                        </div>
                        <div class="env-item">
                            <span class="env-key">Debug:</span>
                            <span class="env-value">False</span>
                        </div>
                        <div class="env-item">
                            <span class="env-key">Host:</span>
                            <span class="env-value">localhost</span>
                        </div>
                    </div>
                </div>
                
                <!-- JSON Reload -->
                <div class="dev-tool-section">
                    <label class="dev-tool-label">🔄 Data Management</label>
                    <button id="reloadJsonBtn" class="dev-action-btn">
                        <span id="reloadIcon">🔄</span>
                        <span id="reloadText">Reload JSON Files</span>
                    </button>
                    <div id="reloadStatus" class="reload-status"></div>
                </div>
                
                <!-- Developer Actions -->
                <div class="dev-tool-section">
                    <label class="dev-tool-label">⚡ Quick Actions</label>
                    <div class="dev-actions-grid">
                        <button class="dev-action-btn-small" onclick="window.location.reload()">
                            🔃 Refresh Page
                        </button>
                        <button class="dev-action-btn-small" onclick="console.clear()">
                            🧹 Clear Console
                        </button>
                        <button class="dev-action-btn-small" onclick="localStorage.clear(); alert('Cache cleared!')">
                            🗑️ Clear Cache
                        </button>
                        <button class="dev-action-btn-small" id="debugModeBtn">
                            🐛 Debug Mode
                        </button>
                    </div>
                </div>
                
                <!-- System Info -->
                <div class="dev-tool-section">
                    <label class="dev-tool-label">📊 System Info</label>
                    <div class="system-info">
                        <div class="info-item">Page Load: <span id="pageLoadTime">-</span>ms</div>
                        <div class="info-item">Memory: <span id="memoryUsage">-</span>MB</div>
                        <div class="info-item">Timestamp: <span id="timestamp">-</span></div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Dev Tools Toggle Button -->
        <button id="devToolsToggle" class="dev-tools-toggle" title="Open Developer Tools">
            🛠️
        </button>
        
        <!-- Header Bar -->
        <div class="header-bar">
            <h1>
                <span class="logo">🏭</span>
                Industries Overview
            </h1>
            <a href="/dashboard" class="back-link">← Back to Dashboard</a>
        </div>
        
        <!-- Main Content -->
        <div class="container">
            <!-- Overview Section -->
            <div class="overview-section">
                <h2>📊 Industry Statistics</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <span class="stat-value">{{ total_industries }}</span>
                        <span class="stat-label">Total Industries</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">{{ high_potential }}</span>
                        <span class="stat-label">High Revenue Potential</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">{{ total_markets }}</span>
                        <span class="stat-label">Key Markets</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">{{ total_capsules }}</span>
                        <span class="stat-label">Connected Capsules</span>
                    </div>
                </div>
            </div>
            
            <!-- Industries Section -->
            <div class="industries-section">
                <h2>🎯 Industry Sectors</h2>
                <div class="industries-grid">
                    {% for industry in industries %}
                    <div class="industry-card" style="border-left-color: {{ industry.color }};">
                        <div class="industry-header">
                            <div class="industry-icon">{{ industry.icon }}</div>
                            <div class="industry-title">
                                <h3>{{ industry.name }}</h3>
                                <span class="industry-id">{{ industry.id }}</span>
                            </div>
                        </div>
                        
                        <p class="industry-description">{{ industry.description }}</p>
                        
                        <!-- MVP Status -->
                        <div class="mvp-section">
                            <div class="mvp-header">
                                <span class="mvp-status">🚀 MVP Status: {{ industry.mvp_status }}</span>
                                <span class="mvp-percentage">{{ industry.mvp_progress }}%</span>
                            </div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: {{ industry.mvp_progress }}%;"></div>
                            </div>
                        </div>
                        
                        <!-- Feature Readiness -->
                        <div class="feature-readiness">
                            <span class="feature-label">✅ Feature Readiness</span>
                            <span class="feature-count">{{ industry.features_ready }}/{{ industry.features_total }}</span>
                        </div>
                        
                        <!-- Dependencies -->
                        <div class="dependencies-section">
                            <div class="dependency-group">
                                <span class="dependency-label">📦 Capsule Dependencies</span>
                                <div class="dependency-tags">
                                    {% for dep in industry.capsule_dependencies %}
                                    <span class="dependency-tag">{{ dep }}</span>
                                    {% endfor %}
                                </div>
                            </div>
                            
                            <div class="dependency-group">
                                <span class="dependency-label">⚙️ Engine Dependencies</span>
                                <div class="dependency-tags">
                                    {% for dep in industry.engine_dependencies %}
                                    <span class="dependency-tag">{{ dep }}</span>
                                    {% endfor %}
                                </div>
                            </div>
                        </div>
                        
                        <!-- Platform Features -->
                        {% if industry.platform_features %}
                        <div class="platform-features">
                            <div class="platform-features-title">🎯 Platform Features</div>
                            <div class="features-list">
                                {% for feature in industry.platform_features %}
                                <div class="feature-item">
                                    <div class="feature-icon">{{ feature.icon }}</div>
                                    <div class="feature-info">
                                        <div class="feature-name">{{ feature.name }}</div>
                                        <div class="feature-status {{ feature.status|lower }}">{{ feature.status }}</div>
                                    </div>
                                </div>
                                {% endfor %}
                            </div>
                        </div>
                        {% endif %}
                        
                        <div class="industry-details">
                            <div class="detail-section">
                                <span class="detail-label">🎯 Key Markets</span>
                                <div class="detail-content">
                                    {% for market in industry.key_markets %}
                                    <span class="tag">{{ market }}</span>
                                    {% endfor %}
                                </div>
                            </div>
                            
                            <div class="detail-section">
                                <span class="detail-label">📦 Connected Capsules</span>
                                <div class="detail-content">
                                    {% for capsule in industry.capsules %}
                                    <span class="tag">{{ capsule }}</span>
                                    {% endfor %}
                                </div>
                            </div>
                        </div>
                        
                        <div class="industry-footer">
                            <span class="badge badge-potential">{{ industry.revenue_potential }} Revenue</span>
                            <span class="badge badge-maturity">{{ industry.maturity }}</span>
                            <span class="api-health {{ industry.api_health|lower }}">
                                <span class="health-indicator {{ industry.api_health|lower }}"></span>
                                {{ industry.api_health }} API
                            </span>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            
            <!-- Monitoring Sections -->
            <div class="monitoring-grid">
                <!-- Capsule Readiness Heatmap -->
                <div class="monitoring-card">
                    <div class="monitoring-header">
                        <div class="monitoring-title">🔥 Capsule Readiness Heatmap</div>
                        <span class="refresh-badge">Live</span>
                    </div>
                    {% for item in capsule_heatmap %}
                    <div class="heatmap-row">
                        <div class="heatmap-label">{{ item.industry }}</div>
                        <div class="heatmap-bar">
                            <div class="heatmap-fill {{ item.status }}" style="width: {{ item.readiness }}%;">
                                {{ item.readiness }}%
                            </div>
                        </div>
                        <div class="heatmap-count">{{ item.capsules }} capsules</div>
                        <span class="heatmap-status {{ item.status }}">{{ item.status }}</span>
                    </div>
                    {% endfor %}
                </div>
                
                <!-- Engine Activity Logs -->
                <div class="monitoring-card">
                    <div class="monitoring-header">
                        <div class="monitoring-title">⚙️ Engine Activity Logs</div>
                        <span class="refresh-badge">Auto-refresh</span>
                    </div>
                    {% for log in engine_logs %}
                    <div class="log-entry {{ log.status }}">
                        <div class="log-time">{{ log.time }}</div>
                        <div class="log-engine">{{ log.engine }}</div>
                        <div class="log-action">{{ log.action }}</div>
                        <div class="log-status {{ log.status }}"></div>
                    </div>
                    {% endfor %}
                </div>
                
                <!-- Platform Performance -->
                <div class="monitoring-card">
                    <div class="monitoring-header">
                        <div class="monitoring-title">📊 Platform Performance</div>
                        <span class="refresh-badge">Real-time</span>
                    </div>
                    <div class="metrics-grid">
                        <div class="metric-box">
                            <span class="metric-value">{{ platform_metrics.uptime }}</span>
                            <span class="metric-label">Uptime</span>
                        </div>
                        <div class="metric-box">
                            <span class="metric-value">{{ platform_metrics.response_time }}</span>
                            <span class="metric-label">Response Time</span>
                        </div>
                        <div class="metric-box">
                            <span class="metric-value">{{ platform_metrics.requests_per_min }}</span>
                            <span class="metric-label">Requests/Min</span>
                        </div>
                        <div class="metric-box">
                            <span class="metric-value">{{ platform_metrics.active_users }}</span>
                            <span class="metric-label">Active Users</span>
                        </div>
                        <div class="metric-box">
                            <span class="metric-value">{{ platform_metrics.cpu_usage }}</span>
                            <span class="metric-label">CPU Usage</span>
                        </div>
                        <div class="metric-box">
                            <span class="metric-value">{{ platform_metrics.memory_usage }}</span>
                            <span class="metric-label">Memory Usage</span>
                        </div>
                    </div>
                </div>
                
                <!-- Data Pipeline Status -->
                <div class="monitoring-card">
                    <div class="monitoring-header">
                        <div class="monitoring-title">🔄 Data Pipeline Status</div>
                        <span class="refresh-badge">Monitored</span>
                    </div>
                    {% for pipeline in pipeline_status %}
                    <div class="pipeline-item {{ pipeline.status }}">
                        <div class="pipeline-name">{{ pipeline.name }}</div>
                        <div class="pipeline-meta">
                            <span>{{ pipeline.throughput }}</span>
                            <span>{{ pipeline.last_run }}</span>
                            <span class="pipeline-badge {{ pipeline.status }}">{{ pipeline.status }}</span>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            
            <!-- Second Row of Monitoring Cards -->
            <div class="monitoring-grid">
                <!-- API Calls Tracking -->
                <div class="monitoring-card">
                    <div class="monitoring-header">
                        <div class="monitoring-title">🔌 API Call Tracking</div>
                        <span class="refresh-badge">Live</span>
                    </div>
                    <table class="api-calls-table">
                        <thead>
                            <tr>
                                <th>Endpoint</th>
                                <th>Method</th>
                                <th>Calls</th>
                                <th>Avg Response</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for api in api_calls %}
                            <tr>
                                <td style="font-family: 'Consolas', monospace; font-size: 0.85em;">{{ api.endpoint }}</td>
                                <td><span class="api-method {{ api.method }}">{{ api.method }}</span></td>
                                <td style="font-weight: 600;">{{ api.calls }}</td>
                                <td style="color: #667eea; font-weight: 600;">{{ api.avg_response }}</td>
                                <td><span class="api-status-{{ api.status }}">● {{ api.status }}</span></td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                
                <!-- Error Logs -->
                <div class="monitoring-card">
                    <div class="monitoring-header">
                        <div class="monitoring-title">⚠️ Error Logs</div>
                        <span class="refresh-badge">Real-time</span>
                    </div>
                    {% for error in error_logs %}
                    <div class="error-log-item {{ error.level }}">
                        <div>
                            <span class="error-level {{ error.level }}">{{ error.level }}</span>
                            <div style="margin-top: 8px; color: #6c757d; font-size: 0.85em;">{{ error.time }}</div>
                        </div>
                        <div style="flex: 1;">
                            <div style="font-weight: 600; font-family: 'Consolas', monospace; font-size: 0.9em; color: #333; margin-bottom: 4px;">
                                {{ error.source }}
                            </div>
                            <div style="font-size: 0.9em; color: #555;">{{ error.message }}</div>
                        </div>
                        <span class="error-resolved {{ 'true' if error.resolved else 'false' }}">
                            {{ 'Resolved' if error.resolved else 'Active' }}
                        </span>
                    </div>
                    {% endfor %}
                </div>
            </div>
            
            <!-- Third Row of Monitoring Cards -->
            <div class="monitoring-grid">
                <!-- Detailed Engine Activity -->
                <div class="monitoring-card">
                    <div class="monitoring-header">
                        <div class="monitoring-title">⚙️ Engine Activity Details</div>
                        <span class="refresh-badge">Live Metrics</span>
                    </div>
                    {% for engine in engine_activity_detail %}
                    <div class="engine-detail-grid {{ engine.status }}">
                        <div class="engine-name-header">{{ engine.engine }}</div>
                        <div class="engine-stat">
                            <span class="engine-stat-label">Uptime</span>
                            <span class="engine-stat-value">{{ engine.uptime }}</span>
                        </div>
                        <div class="engine-stat">
                            <span class="engine-stat-label">Requests</span>
                            <span class="engine-stat-value">{{ engine.requests }}</span>
                        </div>
                        <div class="engine-stat">
                            <span class="engine-stat-label">Avg Latency</span>
                            <span class="engine-stat-value">{{ engine.avg_latency }}</span>
                        </div>
                        <div class="engine-stat">
                            <span class="engine-stat-label">Cache Hits</span>
                            <span class="engine-stat-value">{{ engine.cache_hits }}</span>
                        </div>
                        <div class="engine-stat">
                            <span class="engine-stat-label">Status</span>
                            <span class="engine-stat-value" style="color: {% if engine.status == 'optimal' %}#28a745{% elif engine.status == 'good' %}#17a2b8{% else %}#ffc107{% endif %};">
                                {{ engine.status.upper() }}
                            </span>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                
                <!-- Capsule Load Events -->
                <div class="monitoring-card">
                    <div class="monitoring-header">
                        <div class="monitoring-title">📦 Capsule Load Events</div>
                        <span class="refresh-badge">Event Stream</span>
                    </div>
                    {% for event in capsule_load_events %}
                    <div class="capsule-event {{ event.status }}">
                        <div class="capsule-event-info">
                            <div class="capsule-event-name">{{ event.capsule }}</div>
                            <div class="capsule-event-action">{{ event.action }}</div>
                        </div>
                        <div class="capsule-event-meta">
                            <span style="color: #6c757d;">{{ event.time }}</span>
                            <span class="capsule-load-time">{{ event.load_time }}</span>
                            <span class="capsule-event-status {{ event.status }}">{{ event.status }}</span>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
        
        <script>
            // Page load time tracking
            const loadTime = performance.now();
            document.getElementById('pageLoadTime').textContent = Math.round(loadTime);
            
            // Memory usage (if available)
            if (performance.memory) {
                const memoryMB = Math.round(performance.memory.usedJSHeapSize / 1048576);
                document.getElementById('memoryUsage').textContent = memoryMB;
            } else {
                document.getElementById('memoryUsage').textContent = 'N/A';
            }
            
            // Current timestamp
            function updateTimestamp() {
                const now = new Date();
                document.getElementById('timestamp').textContent = now.toLocaleTimeString();
            }
            updateTimestamp();
            setInterval(updateTimestamp, 1000);
            
            // Developer Tools Panel Toggle
            const devPanel = document.getElementById('devToolsPanel');
            const devToggle = document.getElementById('devToolsToggle');
            const closeDevTools = document.getElementById('closeDevTools');
            
            devToggle.addEventListener('click', () => {
                devPanel.classList.add('active');
                devToggle.style.display = 'none';
            });
            
            closeDevTools.addEventListener('click', () => {
                devPanel.classList.remove('active');
                devToggle.style.display = 'block';
            });
            
            // Theme Toggle
            const lightThemeBtn = document.getElementById('lightTheme');
            const darkThemeBtn = document.getElementById('darkTheme');
            const body = document.body;
            
            // Load saved theme
            const savedTheme = localStorage.getItem('theme') || 'light';
            if (savedTheme === 'dark') {
                body.classList.add('dark-theme');
                darkThemeBtn.classList.add('active');
                lightThemeBtn.classList.remove('active');
            }
            
            lightThemeBtn.addEventListener('click', () => {
                body.classList.remove('dark-theme');
                lightThemeBtn.classList.add('active');
                darkThemeBtn.classList.remove('active');
                localStorage.setItem('theme', 'light');
            });
            
            darkThemeBtn.addEventListener('click', () => {
                body.classList.add('dark-theme');
                darkThemeBtn.classList.add('active');
                lightThemeBtn.classList.remove('active');
                localStorage.setItem('theme', 'dark');
            });
            
            // JSON Reload Button
            const reloadBtn = document.getElementById('reloadJsonBtn');
            const reloadIcon = document.getElementById('reloadIcon');
            const reloadText = document.getElementById('reloadText');
            const reloadStatus = document.getElementById('reloadStatus');
            
            reloadBtn.addEventListener('click', async () => {
                // Animate button
                reloadBtn.disabled = true;
                reloadIcon.style.animation = 'spin 1s linear infinite';
                reloadText.textContent = 'Reloading...';
                reloadStatus.className = 'reload-status';
                reloadStatus.style.display = 'none';
                
                try {
                    // Simulate reload (in production, this would call an API endpoint)
                    await new Promise(resolve => setTimeout(resolve, 1500));
                    
                    // Success
                    reloadStatus.className = 'reload-status success';
                    reloadStatus.textContent = '✅ JSON files reloaded successfully';
                    reloadStatus.style.display = 'block';
                    
                    // Reload page data
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                } catch (error) {
                    // Error
                    reloadStatus.className = 'reload-status error';
                    reloadStatus.textContent = '❌ Failed to reload: ' + error.message;
                    reloadStatus.style.display = 'block';
                } finally {
                    reloadBtn.disabled = false;
                    reloadIcon.style.animation = '';
                    reloadText.textContent = 'Reload JSON Files';
                }
            });
            
            // Debug Mode Toggle
            let debugMode = false;
            const debugBtn = document.getElementById('debugModeBtn');
            
            debugBtn.addEventListener('click', () => {
                debugMode = !debugMode;
                if (debugMode) {
                    debugBtn.textContent = '🐛 Debug: ON';
                    debugBtn.style.background = 'linear-gradient(135deg, #28a745, #20c997)';
                    debugBtn.style.color = 'white';
                    console.log('🐛 Debug mode enabled');
                    console.log('Industries data:', {{ industries|tojson }});
                    console.log('Monitoring data loaded');
                } else {
                    debugBtn.textContent = '🐛 Debug Mode';
                    debugBtn.style.background = '';
                    debugBtn.style.color = '';
                    console.log('Debug mode disabled');
                }
            });
            
            // Spin animation for reload icon
            const style = document.createElement('style');
            style.textContent = `
                @keyframes spin {
                    from { transform: rotate(0deg); }
                    to { transform: rotate(360deg); }
                }
            `;
            document.head.appendChild(style);
            
            // Console welcome message
            console.log('%c🔥 Codex Dominion Industries Dashboard', 'font-size: 20px; font-weight: bold; color: #667eea;');
            console.log('%cDeveloper Tools Active', 'font-size: 14px; color: #764ba2;');
            console.log('Page loaded in ' + Math.round(loadTime) + 'ms');
        </script>
    </body>
    </html>
    """,
    industries=industries,
    total_industries=total_industries,
    high_potential=high_potential,
    total_markets=total_markets,
    total_capsules=total_capsules,
    capsule_heatmap=capsule_heatmap,
    engine_logs=engine_logs,
    platform_metrics=platform_metrics,
    pipeline_status=pipeline_status,
    api_calls=api_calls,
    error_logs=error_logs,
    engine_activity_detail=engine_activity_detail,
    capsule_load_events=capsule_load_events)

@app.route('/dashboard/platforms')
def dashboard_platforms():
    """Platforms overview page"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Platforms | Codex Dominion</title>
        <meta charset="utf-8">
        <style>
            body { font-family: 'Segoe UI', Tahoma, sans-serif; background: #f5f5f5; color: #333; padding: 20px; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }
            .platforms-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 30px; }
            .platform-card { background: white; border-radius: 10px; padding: 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }
            .platform-card h2 { color: #4facfe; margin: 20px 0; }
            .platform-card a { display: inline-block; margin-top: 20px; padding: 15px 30px; background: #4facfe; color: white; text-decoration: none; border-radius: 5px; }
            .platform-icon { font-size: 4em; }
            .back-link { display: inline-block; margin-top: 20px; padding: 10px 20px; background: white; color: #4facfe; text-decoration: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌐 Platform Ecosystems</h1>
                <p>Multi-generational digital platforms</p>
            </div>
            
            <div class="platforms-grid">
                <div class="platform-card">
                    <div class="platform-icon">🌍</div>
                    <h2>Diaspora Platform</h2>
                    <p>Global cultural connection and identity preservation for diaspora communities</p>
                    <a href="/dashboard/platforms/diaspora">View Platform →</a>
                </div>
                
                <div class="platform-card">
                    <div class="platform-icon">👥</div>
                    <h2>Teens Platform</h2>
                    <p>Youth-focused education, creativity, and safe digital community</p>
                    <a href="/dashboard/platforms/teens">View Platform →</a>
                </div>
            </div>
            
            <a href="/dashboard" class="back-link">← Back to Dashboard</a>
        </div>
    </body>
    </html>
    """)

@app.route('/dashboard/platforms/diaspora')
def dashboard_platform_diaspora():
    """Diaspora platform detail page"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Diaspora Platform | Codex Dominion</title>
        <meta charset="utf-8">
        <style>
            body { font-family: 'Segoe UI', Tahoma, sans-serif; background: #f5f5f5; color: #333; padding: 20px; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 40px; border-radius: 10px; margin-bottom: 30px; }
            .content-card { background: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
            .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px; }
            .feature-box { background: #f9f9f9; padding: 20px; border-radius: 5px; }
            .back-link { display: inline-block; margin-top: 20px; padding: 10px 20px; background: #f093fb; color: white; text-decoration: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌍 Diaspora Platform</h1>
                <p>Connecting communities across continents</p>
            </div>
            
            <div class="content-card">
                <h2>Platform Overview</h2>
                <p>The Diaspora Platform enables global cultural connection, identity preservation, and community building for diaspora populations worldwide.</p>
                
                <h3>Core Features</h3>
                <div class="features-grid">
                    <div class="feature-box">
                        <h4>🗺️ Cultural Mapping</h4>
                        <p>Connect to ancestral roots and cultural heritage</p>
                    </div>
                    <div class="feature-box">
                        <h4>👨‍👩‍👧 Family Networks</h4>
                        <p>Build and maintain intergenerational connections</p>
                    </div>
                    <div class="feature-box">
                        <h4>📚 Knowledge Preservation</h4>
                        <p>Archive and share cultural wisdom</p>
                    </div>
                    <div class="feature-box">
                        <h4>🎭 Story Sharing</h4>
                        <p>Share narratives across generations</p>
                    </div>
                </div>
            </div>
            
            <a href="/dashboard/platforms" class="back-link">← Back to Platforms</a>
        </div>
    </body>
    </html>
    """)

@app.route('/dashboard/platforms/teens')
def dashboard_platform_teens():
    """Teens platform detail page"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Teens Platform | Codex Dominion</title>
        <meta charset="utf-8">
        <style>
            body { font-family: 'Segoe UI', Tahoma, sans-serif; background: #f5f5f5; color: #333; padding: 20px; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; padding: 40px; border-radius: 10px; margin-bottom: 30px; }
            .content-card { background: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
            .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px; }
            .feature-box { background: #fff8e1; padding: 20px; border-radius: 5px; }
            .back-link { display: inline-block; margin-top: 20px; padding: 10px 20px; background: #fa709a; color: white; text-decoration: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>👥 Teens Platform</h1>
                <p>Safe, creative, empowering digital space for youth</p>
            </div>
            
            <div class="content-card">
                <h2>Platform Overview</h2>
                <p>The Teens Platform provides a safe, supervised environment for youth education, creativity, social connection, and personal development.</p>
                
                <h3>Core Features</h3>
                <div class="features-grid">
                    <div class="feature-box">
                        <h4>📖 Education Hub</h4>
                        <p>Interactive learning and skill development</p>
                    </div>
                    <div class="feature-box">
                        <h4>🎨 Creative Studio</h4>
                        <p>Tools for artistic and creative expression</p>
                    </div>
                    <div class="feature-box">
                        <h4>🛡️ Safe Community</h4>
                        <p>Moderated, age-appropriate social spaces</p>
                    </div>
                    <div class="feature-box">
                        <h4>🌱 Personal Growth</h4>
                        <p>Mentorship and character development</p>
                    </div>
                </div>
            </div>
            
            <a href="/dashboard/platforms" class="back-link">← Back to Platforms</a>
        </div>
    </body>
    </html>
    """)

@app.route('/dashboard/analytics')
def dashboard_analytics():
    """Analytics dashboard page"""
    platform_data = load_json("platform_capsules.json")
    engines_data = load_json("engines.json")
    
    total_capsules = platform_data.get("meta", {}).get("total_capsules", 36)
    total_engines = engines_data.get("meta", {}).get("total_engines", 26)
    
    # Count active vs planned
    engines = engines_data.get("engines", [])
    active_engines = len([e for e in engines if e.get("status") == "active"])
    planned_engines = len([e for e in engines if e.get("status") in ["planned", "concept"]])
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Analytics | Codex Dominion</title>
        <meta charset="utf-8">
        <style>
            body { font-family: 'Segoe UI', Tahoma, sans-serif; background: #f5f5f5; color: #333; padding: 20px; }
            .container { max-width: 1400px; margin: 0 auto; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }
            .analytics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .metric-card { background: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }
            .metric-value { font-size: 4em; font-weight: bold; color: #667eea; margin: 20px 0; }
            .metric-label { font-size: 1.2em; color: #666; }
            .chart-card { background: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
            .progress-bar { width: 100%; height: 30px; background: #e0e0e0; border-radius: 15px; overflow: hidden; margin: 10px 0; }
            .progress-fill { height: 100%; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); transition: width 0.3s; }
            .back-link { display: inline-block; margin-top: 20px; padding: 10px 20px; background: white; color: #667eea; text-decoration: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📈 System Analytics</h1>
                <p>Real-time platform metrics and insights</p>
            </div>
            
            <div class="analytics-grid">
                <div class="metric-card">
                    <div class="metric-value">{{ total_capsules }}</div>
                    <div class="metric-label">Total Capsules</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{{ total_engines }}</div>
                    <div class="metric-label">Processing Engines</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{{ active_engines }}</div>
                    <div class="metric-label">Active Engines</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{{ planned_engines }}</div>
                    <div class="metric-label">Planned Engines</div>
                </div>
            </div>
            
            <div class="chart-card">
                <h2>Engine Status Distribution</h2>
                <p><strong>Active:</strong> {{ active_engines }}</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {{ (active_engines / total_engines * 100)|round }}%"></div>
                </div>
                <p><strong>Planned/Concept:</strong> {{ planned_engines }}</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {{ (planned_engines / total_engines * 100)|round }}%"></div>
                </div>
            </div>
            
            <a href="/dashboard" class="back-link">← Back to Dashboard</a>
        </div>
    </body>
    </html>
    """, 
    total_capsules=total_capsules,
    total_engines=total_engines,
    active_engines=active_engines,
    planned_engines=planned_engines)

# ==================== END DASHBOARD HTML ROUTES ====================

# Data API endpoints
@app.route('/data/<path:filename>')
def serve_data(filename):
    """Serve JSON data files from /data directory"""
    return load_json_response(filename)

@app.route('/api/ledger')
def api_ledger():
    """Get codex ledger data"""
    return load_json_response("codex_ledger.json")

@app.route('/api/cycles')
def api_cycles():
    """Get cycles data"""
    return load_json_response("cycles.json")

@app.route('/api/proclamations')
def api_proclamations():
    """Get proclamations data"""
    return load_json_response("proclamations.json")

@app.route('/api/capsules')
def api_capsules():
    """Get all capsules (execution capsules + platform capsules)"""
    execution_data = load_json("execution_capsules.json")
    platform_data = load_json("platform_capsules.json")
    
    return jsonify({
        "execution_capsules": execution_data.get("execution_capsules", []),
        "platform_capsules": {
            "foundation": platform_data.get("foundation", []),
            "economic": platform_data.get("economic", []),
            "knowledge": platform_data.get("knowledge", []),
            "community": platform_data.get("community", []),
            "automation": platform_data.get("automation", []),
            "media": platform_data.get("media", [])
        },
        "meta": {
            "execution_capsules_count": len(execution_data.get("execution_capsules", [])),
            "platform_capsules_count": platform_data.get("meta", {}).get("total_capsules", 0),
            "total_capsules": len(execution_data.get("execution_capsules", [])) + platform_data.get("meta", {}).get("total_capsules", 0)
        }
    })

@app.route('/api/capsules/<capsule_id>')
def api_capsule_detail(capsule_id):
    """Get specific capsule by ID (searches both execution and platform capsules)"""
    # Search execution capsules
    execution_data = load_json("execution_capsules.json")
    execution_capsules = execution_data.get("execution_capsules", [])
    capsule = next((c for c in execution_capsules if c.get("id") == capsule_id), None)
    if capsule:
        return jsonify({"source": "execution_capsules", "capsule": capsule})
    
    # Search platform capsules
    platform_data = load_json("platform_capsules.json")
    for realm in ["foundation", "economic", "knowledge", "community", "automation", "media"]:
        capsules = platform_data.get(realm, [])
        capsule = next((c for c in capsules if c.get("id") == capsule_id), None)
        if capsule:
            return jsonify({"source": "platform_capsules", "realm": realm, "capsule": capsule})
    
    return jsonify({"error": f"Capsule not found: {capsule_id}"}), 404

@app.route('/api/intelligence-core')
def api_intelligence_core():
    """Get intelligence core engines data"""
    engines_data = load_json("engines.json")
    return jsonify(engines_data)

@app.route('/api/intelligence-core/<engine_id>')
def api_intelligence_core_engine(engine_id):
    """Get specific intelligence core engine by ID"""
    engines_data = load_json("engines.json")
    engines = engines_data.get("engines", [])
    engine = next((e for e in engines if e.get("id") == engine_id), None)
    if engine:
        return jsonify(engine)
    return jsonify({"error": f"Engine not found: {engine_id}"}), 404

@app.route('/api/intelligence-core/active')
def api_intelligence_core_active():
    """Get only active intelligence core engines"""
    data = load_json("intelligence_core.json")
    active = [e for e in data if e.get("status") == "active"]
    return jsonify(active)

@app.route('/api/industries')
def api_industries():
    """Get all industries ontology"""
    return load_json_response("industries.json")

@app.route('/api/industries/<industry_id>')
def api_industry(industry_id):
    """Get specific industry by ID"""
    data = load_json("industries.json")
    industries = data.get("industries", [])
    industry = next((i for i in industries if i.get("id") == industry_id), None)
    if industry:
        return jsonify(industry)
    return jsonify({"error": f"Industry not found: {industry_id}"}), 404

@app.route('/api/niches')
def api_niches():
    """Get all niche blueprints"""
    return load_json_response("niches.json")

@app.route('/api/niches/industry/<industry_id>')
def api_niches_by_industry(industry_id):
    """Get niches filtered by industry"""
    data = load_json("niches.json")
    niches = data.get("niches", [])
    filtered = [n for n in niches if n.get("industry") == industry_id]
    return jsonify({"industry": industry_id, "niches": filtered, "count": len(filtered)})

@app.route('/api/domain-packs')
def api_domain_packs():
    """Get all domain expertise packs"""
    return load_json_response("domain_packs.json")

@app.route('/api/domain-packs/<pack_id>')
def api_domain_pack(pack_id):
    """Get specific domain pack by ID"""
    data = load_json("domain_packs.json")
    packs = data.get("domain_packs", [])
    pack = next((p for p in packs if p.get("id") == pack_id), None)
    if pack:
        return jsonify(pack)
    return jsonify({"error": f"Domain pack not found: {pack_id}"}), 404

@app.route('/api/phase-1-status')
def api_phase_1_status():
    """Get Phase 1 (Structural Intelligence) activation status"""
    return jsonify(get_phase_1_status())

@app.route('/api/cross-reference/<industry_id>')
def api_cross_reference(industry_id):
    """Get complete cross-reference: industry → niches → packs"""
    result = cross_reference_industry(industry_id)
    if not result.get("industry"):
        return jsonify({"error": f"Industry not found: {industry_id}"}), 404
    return jsonify(result)

@app.route('/api/realms')
def api_realms():
    """Get all realms (Phase 2)"""
    return load_json_response("realms.json")

@app.route('/api/realms/<realm_id>')
def api_realm(realm_id):
    """Get specific realm by ID"""
    data = load_json("realms.json")
    realms = data.get("realms", [])
    realm = next((r for r in realms if r.get("id") == realm_id), None)
    if realm:
        return jsonify(realm)
    return jsonify({"error": f"Realm not found: {realm_id}"}), 404

@app.route('/api/agents')
def api_agents():
    """Get all AI agents (Phase 2)"""
    return jsonify(agents_json)

@app.route('/api/agents/<agent_id>')
def api_agent(agent_id):
    """Get specific agent by ID"""
    agents = agents_json.get("agents", [])
    agent = next((a for a in agents if a.get("id") == agent_id), None)
    if agent:
        return jsonify(agent)
    return jsonify({"error": f"Agent not found: {agent_id}", "available_agents": [a.get("id") for a in agents[:5]]}), 404

@app.route('/api/agents/realm/<realm_id>')
def api_agents_by_realm(realm_id):
    """Get all agents operating in a specific realm"""
    agents = agents_json.get("agents", [])
    filtered = [a for a in agents if realm_id in a.get("realms", []) or realm_id == a.get("realm")]
    return jsonify({"realm": realm_id, "agents": filtered, "count": len(filtered)})

@app.route('/api/agents/status/<status>')
def api_agents_by_status(status):
    """Get agents by status (active, planned, concept)"""
    agents = agents_json.get("agents", [])
    filtered = [a for a in agents if a.get("status") == status]
    return jsonify({"status": status, "agents": filtered, "count": len(filtered)})

# ==================== CREATIVE AGENTS (Genesis Protocol) ====================

@app.route('/creative-agents')
def creative_agents_page():
    """Display the first generation of creative agents"""
    return render_template_string(CREATIVE_AGENTS_HTML)

@app.route('/api/agents/creative')
def api_creative_agents():
    """Get all creative agents from Genesis Protocol"""
    from db import SessionLocal
    from models import Agent
    
    session = SessionLocal()
    try:
        # Query creative agents (Generation 1)
        creative_agents = session.query(Agent).filter(
            Agent.id.like("agent_%")
        ).order_by(Agent.created_at).all()
        
        agents_data = [agent.to_dict() for agent in creative_agents]
        
        return jsonify({
            "agents": agents_data,
            "count": len(agents_data),
            "generation": 1,
            "status": "active"
        })
    except Exception as e:
        return jsonify({"error": str(e), "agents": [], "count": 0}), 500
    finally:
        session.close()

def find_agent_by_id(agent_id: str) -> Dict[str, Any] | None:
    """Find agent by ID from agents_simple.json"""
    agents = agents_json.get("agents", [])
    return next((a for a in agents if a.get("id") == agent_id), None)

# ==================== RQ WORKER PROCESSING ====================
# All workflow processing now handled by Redis Queue (RQ) workers.
# No in-process threads - Flask app never blocks on workflow execution.
# 
# To start workers:
#   pip install rq redis
#   redis-server                  # Start Redis
#   rq worker workflows           # Start RQ worker (separate process)
# 
# Workflows are enqueued via workflow_engine.enqueue_execution(workflow_id)
# Worker processes jobs from Redis queue asynchronously.
# Provides: reliability, scalability, horizontal scaling.

# ==================== WORKFLOW TYPE SUGGESTION ====================

def suggest_workflow_types(user_message: str) -> List[Dict[str, Any]]:
    """
    Analyze user message and suggest matching workflow types.
    
    Simple keyword-based matching for now (can be replaced with ML later).
    Returns list of workflow type metadata with relevance scores.
    """
    message_lower = user_message.lower()
    all_types_dict = list_workflow_types()  # Returns dict {id: metadata}
    all_types = list(all_types_dict.values())  # Convert to list of dicts
    suggestions = []
    
    # Keyword mapping for different workflow types
    keywords = {
        "customer_followup": ["customer", "follow-up", "followup", "follow up", "crm", "client", "retention"],
        "invoice_reminders": ["invoice", "payment", "reminder", "billing", "accounts receivable", "overdue"],
        "content_scheduler": ["content", "post", "social media", "publish", "schedule", "blog", "marketing"],
        "data_entry_automation": ["data entry", "input", "form", "spreadsheet", "manual entry", "typing"],
        "report_generation": ["report", "analytics", "dashboard", "summary", "statistics", "metrics"],
        "email_campaign": ["email", "newsletter", "campaign", "mailing list", "subscribers"],
        "lead_qualification": ["lead", "prospect", "qualify", "sales", "pipeline", "conversion"],
        "inventory_sync": ["inventory", "stock", "warehouse", "sync", "product", "fulfillment"],
        "support_ticket_routing": ["support", "ticket", "help desk", "customer service", "issue", "inquiry"],
        "expense_tracking": ["expense", "receipt", "reimbursement", "budget", "spending", "cost"]
    }
    
    # Score each workflow type based on keyword matches
    for wf_type in all_types:
        wf_id = wf_type.get("id", "")
        wf_keywords = keywords.get(wf_id, [])
        
        # Count keyword matches
        matches = sum(1 for keyword in wf_keywords if keyword in message_lower)
        
        # Also check if category or name is mentioned
        if wf_type.get("category", "").lower() in message_lower:
            matches += 2
        if any(word in message_lower for word in wf_type.get("name", "").lower().split()):
            matches += 3
        
        if matches > 0:
            suggestions.append({
                "id": wf_type.get("id"),
                "name": wf_type.get("name"),
                "description": wf_type.get("description"),
                "category": wf_type.get("category"),
                "domain": wf_type.get("domain"),
                "relevance_score": matches
            })
    
    # Sort by relevance score (highest first) and return top 3
    suggestions.sort(key=lambda x: x["relevance_score"], reverse=True)
    return suggestions[:3]

# ==================== CHAT API ====================

@app.route('/api/chat', methods=['POST'])
def api_chat_unified():
    """
    Unified chat endpoint with workflow execution support
    
    Request body:
    {
      "agent_id": "...",
      "message": "...",
      "context": { ... optional extras ... },
      "mode": "chat" | "execute" | "suggest" | "confirm"
    }
    
    Modes:
    - chat: Simple conversational response
    - suggest: Analyze message and suggest workflow types
    - confirm: User selected workflow type, gather inputs
    - execute: Execute the workflow with provided inputs
    """
    data = request.get_json(force=True)
    agent_id = data.get("agent_id")
    message = data.get("message", "")
    mode = data.get("mode", "chat")

    agent = find_agent_by_id(agent_id) if agent_id else None

    if not agent:
        return jsonify({"error": "Agent not found", "agent_id": agent_id}), 404

    # ===== MODE: SUGGEST - Analyze request and suggest workflow types =====
    if mode == "suggest":
        suggested_types = suggest_workflow_types(message)
        
        if not suggested_types:
            return jsonify({
                "agent_id": agent_id,
                "agent_name": agent.get("name"),
                "mode": "suggest",
                "message": message,
                "suggestions": [],
                "reply": (
                    "I couldn't identify a specific workflow type from your request. "
                    "Could you provide more details about what you'd like to automate?"
                )
            })
        
        return jsonify({
            "agent_id": agent_id,
            "agent_name": agent.get("name"),
            "mode": "suggest",
            "message": message,
            "suggestions": suggested_types,
            "reply": (
                f"I found {len(suggested_types)} workflow type(s) that match your request. "
                "Which one would you like to set up?"
            )
        })
    
    # ===== MODE: CONFIRM - User selected workflow type, prepare for input gathering =====
    if mode == "confirm":
        ctx = data.get("context", {})
        workflow_type_id = ctx.get("workflow_type")
        
        if not workflow_type_id:
            return jsonify({"error": "workflow_type required in context for confirm mode"}), 400
        
        wf_type = get_workflow_type(workflow_type_id)
        if not wf_type:
            return jsonify({"error": "Unknown workflow type", "workflow_type": workflow_type_id}), 400
        
        # Return workflow type details and required inputs
        return jsonify({
            "agent_id": agent_id,
            "agent_name": agent.get("name"),
            "mode": "confirm",
            "workflow_type": {
                "id": wf_type.id,
                "name": wf_type.name,
                "description": wf_type.description,
                "category": wf_type.category,
                "domain": wf_type.domain,
                "required_inputs": wf_type.required_inputs,
                "default_profile": wf_type.default_calculator_profile
            },
            "reply": (
                f"Great! Let's set up {wf_type.name}. "
                f"I'll need some information: {', '.join(wf_type.required_inputs)}. "
                "You can provide these values and I'll calculate the savings and create the workflow."
            )
        })

    # ===== MODE: EXECUTE - Run calculator and create workflow =====
    if mode == "execute":
        ctx = data.get("context", {})
        workflow_type_id = ctx.get("workflow_type", "customer_followup")
        wf_type = get_workflow_type(workflow_type_id)

        if not wf_type:
            return jsonify({"error": "Unknown workflow type", "workflow_type": workflow_type_id}), 400

        calc_payload = ctx.get("calculator_inputs", {}) or {}
        profile_defaults = wf_type.default_calculator_profile or {}

        # Merge defaults with user inputs (user inputs take precedence)
        merged_calc = {
            **profile_defaults,
            **calc_payload
        }

        # Handle different field names based on workflow type
        inp = SavingsInput(
            tasks_per_week=float(merged_calc.get("tasks_per_week", merged_calc.get("invoices_per_month", merged_calc.get("posts_per_week", 0)))),
            time_per_task_minutes=float(merged_calc.get("time_per_task_minutes", merged_calc.get("time_per_invoice_minutes", merged_calc.get("time_per_post_minutes", 0)))),
            hourly_wage=float(merged_calc.get("hourly_wage", 0)),
            automation_percent=float(merged_calc.get("automation_percent", 0)),
            error_rate=float(merged_calc.get("error_rate", 0)),
            cost_per_error=float(merged_calc.get("cost_per_error", 0)),
            value_per_accelerated_task=float(merged_calc.get("value_per_accelerated_task", 0)),
        )

        savings = calculate_savings(inp)
        savings_result = {
            "weekly_savings": savings.weekly_savings,
            "monthly_savings": savings.monthly_savings,
            "yearly_savings": savings.yearly_savings,
            "hours_saved_per_week": savings.hours_saved_per_week,
            "error_savings_weekly": savings.error_savings_weekly,
            "scaling_savings_weekly": savings.scaling_savings_weekly,
            "total_weekly_savings": savings.total_weekly_savings
        }

        # ===== COUNCIL OVERSIGHT CHECK =====
        # Get domain from workflow type
        domain = wf_type.domain
        session = g.db
        council = get_council_by_domain(session, domain)
        if council and not council_allows_action(council, f"create_workflow_{workflow_type_id}", savings_result):
            return jsonify({
                "agent_id": agent_id,
                "agent_name": agent.get("name"),
                "mode": "execute",
                "blocked_by_council": council.get("id"),
                "reply": (
                    f"This {wf_type.name} workflow requires review by {council.get('name')} "
                    "before it can be activated."
                ),
                "savings": savings_result
            }), 403

        # Create workflow using refactored DB-backed workflow_engine
        workflow_id = workflow_engine.create_workflow(
            workflow_type_id=workflow_type_id,
            created_by_agent=agent_id,
            inputs=ctx.get("workflow_inputs", {}),
            calculated_savings=savings_result,
            assigned_council_id=council.get("id") if council else None
        )

        # Enqueue workflow for execution (handled by RQ worker)
        try:
            workflow_engine.enqueue_execution(workflow_id)
            print(f"✅ Workflow {workflow_id} created and enqueued for execution")
        except Exception as e:
            print(f"⚠️ Failed to enqueue workflow {workflow_id}: {e}")
            # Workflow is still created in DB, just not queued yet

        return jsonify({
            "agent_id": agent_id,
            "agent_name": agent.get("name"),
            "mode": "execute",
            "message": message,
            "workflow_id": workflow_id,
            "workflow_type": wf_type.id,
            "status": "pending",
            "savings": savings_result,
            "reply": (
                f"I've created a {wf_type.name} workflow (ID: {workflow_id}). "
                "It's now pending execution. I'll track performance and savings."
            )
        })

    # default: chat mode (still simulated)
    return jsonify({
        "agent_id": agent_id,
        "agent_name": agent.get("name"),
        "mode": "chat",
        "message": message,
        "reply": f"[SIMULATED REPLY from {agent.get('name')}] {message}"
    })

@app.route('/api/workflow/execute', methods=['POST'])
def api_workflow_execute():
    """
    Execute a workflow automation
    
    Request Body:
    {
        "agent_id": "agent_jermaine_super_action",
        "workflow_id": "customer_followup",
        "inputs": {
            "messages_per_week": "20",
            "time_per_message": "5",
            "hourly_rate": "25",
            "automation_percentage": "80"
        }
    }
    
    Returns:
    {
        "success": true,
        "workflow_id": "customer_followup_1234",
        "status": "deployed",
        "execution_details": {...},
        "next_steps": [...]
    }
    """
    try:
        data = request.get_json()
        agent_id = data.get("agent_id")
        workflow_id = data.get("workflow_id")
        inputs = data.get("inputs", {})
        
        if not all([agent_id, workflow_id]):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Get workflow definition
        workflow_def = get_workflow_definition(workflow_id)
        if not workflow_def:
            return jsonify({"error": f"Unknown workflow: {workflow_id}"}), 404
        
        # Calculate final ROI
        roi = calculate_workflow_roi(workflow_id, inputs)
        
        # Generate unique workflow execution ID
        execution_id = f"{workflow_id}_{int(datetime.utcnow().timestamp())}"
        
        # Simulate workflow deployment (in production, this would call actual automation engines)
        execution_details = {
            "workflow_id": execution_id,
            "workflow_name": workflow_def["name"],
            "status": "deployed",
            "deployed_at": datetime.utcnow().isoformat() + "Z",
            "configuration": inputs,
            "roi_metrics": roi,
            "active": True
        }
        
        # In production: Save to database, trigger actual automation setup, log execution
        # For now: Return success confirmation with monitoring promise
        
        confirmation_message = f"""Your {workflow_def['name'].lower()} is now active.
I'll monitor performance and notify you of improvements."""
        
        return jsonify({
            "success": True,
            "workflow_id": execution_id,
            "status": "deployed",
            "execution_details": execution_details,
            "confirmation_message": confirmation_message,
            "next_steps": [
                "Workflow is now active and monitoring",
                f"Expected savings: ${roi['monthly_savings']:.2f}/month",
                "I'll notify you of performance improvements",
                "Check dashboard for execution history",
                "You can modify or pause anytime"
            ],
            "dashboard_url": f"/dashboard/workflows/{execution_id}"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def detect_action_intent(message: str, agent: Dict, conversation_state: Dict) -> Dict:
    """
    Detect if user message is requesting an action vs just chatting
    
    Action keywords: automate, execute, build, create, deploy, setup, configure, run, schedule
    """
    message_lower = message.lower()
    
    # If already in a workflow, this is an action flow
    if conversation_state.get("workflow_id"):
        return {
            "is_action_request": True,
            "workflow_id": conversation_state["workflow_id"],
            "step": conversation_state.get("step", 1),
            "intent_type": "workflow_continuation"
        }
    
    # Action keywords that indicate execution intent
    action_keywords = [
        "automate", "execute", "build", "create", "deploy", "setup", 
        "configure", "run", "schedule", "implement", "activate", "enable",
        "generate", "launch", "start", "initialize"
    ]
    
    # Check for action keywords
    has_action_keyword = any(keyword in message_lower for keyword in action_keywords)
    
    # Detect specific workflow patterns
    workflow_patterns = {
        "customer_followup": ["follow-up", "followup", "follow up", "customer message", "customer email"],
        "social_posting": ["social media", "post", "tweet", "instagram", "linkedin"],
        "reporting": ["report", "analytics", "dashboard", "metrics"],
        "email_campaign": ["email campaign", "newsletter", "email automation"],
        "data_sync": ["sync", "integrate", "connect", "import", "export"]
    }
    
    detected_workflow = None
    for workflow_name, patterns in workflow_patterns.items():
        if any(pattern in message_lower for pattern in patterns):
            detected_workflow = workflow_name
            break
    
    if has_action_keyword and detected_workflow:
        return {
            "is_action_request": True,
            "workflow_id": detected_workflow,
            "intent_type": "new_workflow",
            "confidence": "high"
        }
    elif has_action_keyword:
        return {
            "is_action_request": True,
            "workflow_id": "custom",
            "intent_type": "new_workflow",
            "confidence": "medium"
        }
    
    return {
        "is_action_request": False,
        "intent_type": "conversational"
    }

def handle_action_flow(agent: Dict, message: str, action_detection: Dict, conversation_state: Dict) -> Dict:
    """
    Handle the execute-action flow with workflow detection and input gathering
    """
    workflow_id = action_detection["workflow_id"]
    intent_type = action_detection["intent_type"]
    
    # If starting a new workflow
    if intent_type == "new_workflow":
        workflow_def = get_workflow_definition(workflow_id)
        
        if not workflow_def:
            return {
                "response": f"""**{agent.get('name')}:**
──────────────────────────────
I can help you with that. Let me build a custom workflow.

**What I need from you:**
1. Describe the specific task you want automated
2. How often should it run? (daily, weekly, on-demand)
3. What's the expected outcome?

Once I have these details, I'll calculate the time/cost savings and set it up.""",
                "action_type": "input_gathering",
                "workflow_detected": True,
                "workflow_id": "custom",
                "next_inputs_required": ["task_description", "frequency", "expected_outcome"],
                "ready_to_execute": False
            }
        
        # Known workflow - start gathering inputs
        first_question = workflow_def["input_steps"][0]
        
        return {
            "response": f"""**{agent.get('name')}:**
──────────────────────────────
✅ I can automate your {workflow_def['name']}.

**To calculate ROI and build the workflow, I need:**

**{first_question['label']}**
{first_question.get('help_text', '')}

*This helps me calculate your time/cost savings.*""",
            "action_type": "input_gathering",
            "workflow_detected": True,
            "workflow_id": workflow_id,
            "workflow_name": workflow_def["name"],
            "next_inputs_required": [step["key"] for step in workflow_def["input_steps"]],
            "current_step": 1,
            "total_steps": len(workflow_def["input_steps"]),
            "ready_to_execute": False
        }
    
    # Continuing an existing workflow - gather next input
    elif intent_type == "workflow_continuation":
        step = conversation_state.get("step", 1)
        collected_inputs = conversation_state.get("collected_inputs", {})
        workflow_def = get_workflow_definition(workflow_id)
        
        # Store the user's answer
        current_step_def = workflow_def["input_steps"][step - 1]
        collected_inputs[current_step_def["key"]] = message
        
        # Check if we have all inputs
        if step >= len(workflow_def["input_steps"]):
            # Calculate ROI
            roi = calculate_workflow_roi(workflow_id, collected_inputs)
            
            # Calculate weekly savings for presentation
            weekly_savings = roi.get('weekly_savings', roi['monthly_savings'] / 4.33)
            error_reduction = roi.get('error_reduction_pct', 0)
            workdays_saved = roi.get('workdays_saved_per_week', 0)
            employees_eq = roi.get('employees_equivalent', 0)
            
            # Build ROI breakdown
            roi_breakdown = []
            if roi.get('labor_monthly', 0) > 0:
                roi_breakdown.append(f"Labor savings: ${roi['labor_monthly']:.0f}/month")
            if roi.get('error_monthly', 0) > 0:
                roi_breakdown.append(f"Error reduction: ${roi['error_monthly']:.0f}/month")
            if roi.get('scaling_monthly', 0) > 0:
                roi_breakdown.append(f"Scaling value: ${roi['scaling_monthly']:.0f}/month")
            
            roi_detail = "\n".join([f"   • {item}" for item in roi_breakdown]) if roi_breakdown else ""
            
            return {
                "response": f"""**{agent.get('name')}:**
──────────────────────────────
🎯 **Here's what your automation unlocks:**

• **Weekly savings:** ${weekly_savings:.0f}
• **Monthly savings:** ${roi['monthly_savings']:.0f}
• **Yearly savings:** ${roi['annual_savings']:.0f}
• **Error reduction:** {error_reduction}%
• **Time reclaimed:** {roi['time_saved_per_week']} hours/week

📊 **ROI Breakdown:**
{roi_detail}

💡 **Equivalent to:**
   • Saving {workdays_saved} workdays per week
   • {employees_eq} full-time employees

**Would you like me to build and activate this workflow now?**

Type **'yes, execute'** to deploy, or 'modify' to adjust parameters.""",
                "action_type": "execution_ready",
                "workflow_detected": True,
                "workflow_id": workflow_id,
                "collected_inputs": collected_inputs,
                "roi_estimate": roi,
                "ready_to_execute": True
            }
        
        # Ask next question
        next_step_def = workflow_def["input_steps"][step]
        
        return {
            "response": f"""**{agent.get('name')}:**
──────────────────────────────
✓ Got it: {message}

**Next:**
{next_step_def['label']}
{next_step_def.get('help_text', '')}""",
            "action_type": "input_gathering",
            "workflow_detected": True,
            "workflow_id": workflow_id,
            "current_step": step + 1,
            "total_steps": len(workflow_def["input_steps"]),
            "collected_inputs": collected_inputs,
            "ready_to_execute": False
        }
    
    return {
        "response": "Something went wrong. Please try again.",
        "action_type": "error"
    }

def get_workflow_definition(workflow_id: str) -> Dict:
    """
    Get workflow definition with input steps for ROI calculation
    """
    workflows = {
        "customer_followup": {
            "name": "Weekly Customer Follow-Up Automation",
            "description": "Automate weekly customer follow-up messages",
            "input_steps": [
                {
                    "key": "messages_per_week",
                    "label": "How many follow-up messages per week?",
                    "help_text": "Example: 20 customers per week",
                    "type": "number"
                },
                {
                    "key": "time_per_message",
                    "label": "How long does each message take? (minutes)",
                    "help_text": "Example: 5 minutes per message",
                    "type": "number"
                },
                {
                    "key": "hourly_rate",
                    "label": "What's the hourly labor cost?",
                    "help_text": "Example: $25/hour",
                    "type": "currency"
                },
                {
                    "key": "automation_percentage",
                    "label": "What percentage can be automated?",
                    "help_text": "Example: 80% (leave 20% for personal touch)",
                    "type": "percentage"
                }
            ]
        },
        "social_posting": {
            "name": "Social Media Posting Automation",
            "description": "Schedule and automate social media posts",
            "input_steps": [
                {"key": "posts_per_week", "label": "How many posts per week?", "type": "number"},
                {"key": "time_per_post", "label": "Minutes per post?", "type": "number"},
                {"key": "hourly_rate", "label": "Hourly labor cost?", "type": "currency"},
                {"key": "automation_percentage", "label": "Automation percentage?", "type": "percentage"}
            ]
        }
    }
    
    return workflows.get(workflow_id)

def calculate_workflow_roi(workflow_id: str, inputs: Dict) -> Dict:
    """
    Calculate 3-Part ROI:
    1. Labor Savings = Tasks × Time × Wage × Automation %
    2. Error Savings = Error cost × Error reduction %
    3. Scaling Savings = (Tasks × Automation %) × Value per task
    Total ROI = Labor + Error + Scaling
    """
    # Parse inputs (handle various formats)
    try:
        if workflow_id in ["customer_followup", "social_posting"]:
            # Common inputs
            tasks_key = "messages_per_week" if workflow_id == "customer_followup" else "posts_per_week"
            time_key = "time_per_message" if workflow_id == "customer_followup" else "time_per_post"
            
            tasks = float(inputs.get(tasks_key, "0").replace(",", ""))
            time_per = float(inputs.get(time_key, "0").replace(",", ""))
            hourly_rate = float(inputs.get("hourly_rate", "0").replace("$", "").replace(",", ""))
            auto_pct = float(inputs.get("automation_percentage", "0").replace("%", "")) / 100
            
            # Error inputs (optional for backwards compatibility)
            errors_per_month = float(inputs.get("errors_per_month", "0").replace(",", ""))
            cost_per_error = float(inputs.get("cost_per_error", "0").replace("$", "").replace(",", ""))
            
            # Scaling inputs (optional)
            value_per_task = float(inputs.get("value_per_accelerated_task", "0").replace("$", "").replace(",", ""))
            
            # 1. LABOR SAVINGS: Tasks × Time × Wage × Automation %
            hours_per_week = (tasks * time_per) / 60
            automated_hours = hours_per_week * auto_pct
            labor_weekly = automated_hours * hourly_rate
            labor_monthly = labor_weekly * 4.33
            labor_annual = labor_monthly * 12
            
            # 2. ERROR SAVINGS: Error cost × Error reduction %
            error_reduction_pct = int(auto_pct * 100)  # Automation % reduces errors
            error_monthly = (cost_per_error * errors_per_month * auto_pct) if errors_per_month > 0 else 0
            error_annual = error_monthly * 12
            
            # 3. SCALING SAVINGS: (Tasks × Automation %) × Value per task
            accelerated_tasks_weekly = tasks * auto_pct
            scaling_weekly = accelerated_tasks_weekly * value_per_task if value_per_task > 0 else 0
            scaling_monthly = scaling_weekly * 4.33
            scaling_annual = scaling_monthly * 12
            
            # TOTAL ROI
            total_weekly = labor_weekly + (error_monthly / 4.33) + scaling_weekly
            total_monthly = labor_monthly + error_monthly + scaling_monthly
            total_annual = labor_annual + error_annual + scaling_annual
            
            # Calculate equivalent metrics
            workdays_saved = round(automated_hours / 8, 1)  # 8-hour workdays
            employees_equivalent = round(automated_hours / 40, 2)  # 40-hour work week
            
            return {
                "time_saved_per_week": round(automated_hours, 1),
                "workdays_saved_per_week": workdays_saved,
                "employees_equivalent": employees_equivalent,
                
                # Labor Savings
                "labor_weekly": round(labor_weekly, 2),
                "labor_monthly": round(labor_monthly, 2),
                "labor_annual": round(labor_annual, 2),
                
                # Error Savings
                "error_monthly": round(error_monthly, 2),
                "error_annual": round(error_annual, 2),
                "error_reduction_pct": error_reduction_pct,
                
                # Scaling Savings
                "scaling_weekly": round(scaling_weekly, 2),
                "scaling_monthly": round(scaling_monthly, 2),
                "scaling_annual": round(scaling_annual, 2),
                
                # Total ROI
                "weekly_savings": round(total_weekly, 2),
                "monthly_savings": round(total_monthly, 2),
                "annual_savings": round(total_annual, 2),
                
                # Meta
                "automation_percentage": int(auto_pct * 100),
                "setup_time": "10-15",
                "payback_period": "Immediate"
            }
    except Exception as e:
        print(f"ROI calculation error: {e}")
        pass
    
    # Default fallback
    return {
        "time_saved_per_week": 5,
        "monthly_savings": 500,
        "annual_savings": 6000,
        "setup_time": "15",
        "payback_period": "Immediate"
    }

def generate_agent_response(agent: Dict, message: str) -> str:
    """
    Generate contextual response based on agent personality and capabilities
    
    Args:
        agent: Agent data from agents.json
        message: User's message
        
    Returns:
        Agent's response string
    """
    agent_name = agent.get("name", "AI Agent")
    personality = agent.get("personality", "professional")
    role = agent.get("role", "Assistant")
    capabilities = agent.get("capabilities", [])
    
    # Detect intent from message
    message_lower = message.lower()
    
    # Launch sequence planning (strategic)
    if "launch" in message_lower and ("sequence" in message_lower or "plan" in message_lower or "step" in message_lower):
        if personality in ["strategic", "Confident, precise, ceremonial, action-focused."]:
            return f"""**{agent_name}:**
──────────────────────────────
Here's a clean 3-step launch sequence to activate your platform:

**1. Prepare the foundation**
   • Validate credentials and permissions
   • Load all capsules and engines
   • Run system readiness checks
   • Verify database connections
   • Test API endpoints

**2. Activate the public layer**
   • Publish landing page and documentation
   • Connect social channels (Twitter, Discord, LinkedIn)
   • Enable user onboarding flow
   • Configure analytics tracking
   • Set up monitoring alerts

**3. Trigger the automation loop**
   • Schedule daily automated tasks
   • Enable real-time analytics tracking
   • Activate council oversight protocols
   • Initialize backup systems
   • Deploy notification webhooks

**Next Actions:**
Let me know if you want me to execute any of these steps, or if you need detailed procedures for a specific phase. I can also generate deployment scripts or configuration files."""
        else:
            return f"""✅ **3-Step Launch Sequence Plan**

**Step 1: Build & Test**
Get your platform live with core features. Test with a small group to ensure everything works smoothly.

**Step 2: Market & Launch**
Create buzz through social media, email campaigns, and content marketing. Open doors to your first users.

**Step 3: Grow & Optimize**
Monitor user behavior, fix issues quickly, and scale based on demand. Focus on user retention and growth.

Let me know which step you need help with!"""
    
    # Deployment or technical questions
    elif "deploy" in message_lower or "infrastructure" in message_lower or "technical" in message_lower:
        return f"""🚀 **Technical Deployment Guidance**

Based on your message about "{message[:50]}...", here's what I recommend:

**Infrastructure Setup:**
• Cloud provider selection (Azure, AWS, GCP)
• CI/CD pipeline configuration
• Container orchestration (Kubernetes/Docker)
• Database setup and migration strategy

**Security & Compliance:**
• SSL/TLS certificate management
• Environment variable security (secrets management)
• API authentication and rate limiting
• GDPR/compliance considerations

Would you like detailed guidance on any specific area?"""
    
    # General questions
    else:
        if personality == "strategic":
            return f"""As {agent_name}, I'm here to provide strategic guidance on your platform development.

Regarding: "{message}"

I specialize in:
{chr(10).join(f'• {cap.replace("_", " ").title()}' for cap in capabilities[:5])}

Could you provide more context about:
1. Your platform's current stage (idea, MVP, beta, production)?
2. Your primary goal (user growth, revenue, feature expansion)?
3. Any specific blockers or challenges you're facing?

This will help me provide more targeted strategic advice."""
        else:
            return f"""Thanks for reaching out! I'm {agent_name}, your {role}.

You asked: "{message}"

I'm ready to help with:
{chr(10).join(f'• {cap.replace("_", " ").title()}' for cap in capabilities[:5])}

How can I assist you today?"""

@app.route('/api/phase-2-status')
def api_phase_2_status():
    """Get Phase 2 (Realms + Agents) activation status"""
    realms_data = load_json("realms.json")
    agents_data = load_json("agents.json")
    
    return jsonify({
        "phase": 2,
        "name": "Realms & Agents Architecture",
        "status": "active",
        "realms": {
            "total": realms_data.get("meta", {}).get("total_realms", 0),
            "active": realms_data.get("meta", {}).get("active_realms", 0),
            "modules": realms_data.get("meta", {}).get("total_modules", 0),
            "features": realms_data.get("meta", {}).get("total_features", 0)
        },
        "agents": {
            "total": agents_data.get("meta", {}).get("total_agents", 0),
            "active": agents_data.get("meta", {}).get("active_agents", 0),
            "planned": agents_data.get("meta", {}).get("planned_agents", 0),
            "teams": agents_data.get("meta", {}).get("total_teams", 0)
        },
        "integration": {
            "phase_1_engines": ["industry_ontology", "niche_blueprints", "domain_packs"],
            "phase_2_layers": ["realms", "agents"],
            "operational_status": "production_ready"
        }
    })

@app.route('/api/execution-capsules')
def api_execution_capsules():
    """Get all execution capsules (Phase 3)"""
    return load_json_response("execution_capsules.json")

@app.route('/api/execution-capsules/<capsule_id>')
def api_execution_capsule(capsule_id):
    """Get specific execution capsule by ID"""
    data = load_json("execution_capsules.json")
    capsules = data.get("execution_capsules", [])
    capsule = next((c for c in capsules if c.get("id") == capsule_id), None)
    if capsule:
        return jsonify(capsule)
    return jsonify({"error": f"Execution capsule not found: {capsule_id}"}), 404

@app.route('/api/execution-capsules/realm/<realm>')
def api_execution_capsules_by_realm(realm):
    """Get execution capsules by realm"""
    data = load_json("execution_capsules.json")
    capsules = data.get("execution_capsules", [])
    filtered = [c for c in capsules if c.get("realm") == realm]
    return jsonify({"realm": realm, "capsules": filtered, "count": len(filtered)})

@app.route('/api/execution-capsules/status/<status>')
def api_execution_capsules_by_status(status):
    """Get execution capsules by status (active, planned, concept)"""
    data = load_json("execution_capsules.json")
    capsules = data.get("execution_capsules", [])
    filtered = [c for c in capsules if c.get("status") == status]
    return jsonify({"status": status, "capsules": filtered, "count": len(filtered)})

@app.route('/api/execution-capsules/agent/<agent_id>')
def api_execution_capsules_by_agent(agent_id):
    """Get execution capsules used by a specific agent"""
    data = load_json("execution_capsules.json")
    capsules = data.get("execution_capsules", [])
    filtered = [c for c in capsules if agent_id in c.get("agents", [])]
    return jsonify({"agent": agent_id, "capsules": filtered, "count": len(filtered)})

@app.route('/api/phase-3-status')
def api_phase_3_status():
    """Get Phase 3 (Execution Capsules) activation status"""
    capsules_data = load_json("execution_capsules.json")
    
    return jsonify({
        "phase": 3,
        "name": "Execution Capsules Architecture",
        "status": "active",
        "capsules": {
            "total": capsules_data.get("meta", {}).get("total_capsules", 0),
            "active": capsules_data.get("meta", {}).get("active_capsules", 0),
            "planned": capsules_data.get("meta", {}).get("planned_capsules", 0),
            "concept": capsules_data.get("meta", {}).get("concept_capsules", 0),
            "modules": capsules_data.get("meta", {}).get("total_modules", 0),
            "features": capsules_data.get("meta", {}).get("total_features", 0)
        },
        "integration": {
            "phase_1": "industries, niches, domain_packs",
            "phase_2": "realms, agents",
            "phase_3": "execution_capsules",
            "operational_status": "production_ready"
        }
    })

@app.route('/api/intelligence-core-status')
def api_intelligence_core_status():
    """Get complete Intelligence Core status (all 3 phases)"""
    phase1 = get_phase_1_status()
    
    realms_data = load_json("realms.json")
    agents_data = load_json("agents.json")
    capsules_data = load_json("execution_capsules.json")
    
    return jsonify({
        "intelligence_core": {
            "version": "3.0.0",
            "status": "operational",
            "last_updated": "2025-12-18T00:00:00Z"
        },
        "phase_1_structural_intelligence": {
            "status": phase1.get("status"),
            "industries": phase1.get("industries", {}).get("total", 0),
            "niches": phase1.get("niches", {}).get("total", 0),
            "domain_packs": phase1.get("domain_packs", {}).get("total", 0)
        },
        "phase_2_realms_agents": {
            "status": "active",
            "realms": realms_data.get("meta", {}).get("total_realms", 0),
            "agents": agents_data.get("meta", {}).get("total_agents", 0),
            "agent_teams": agents_data.get("meta", {}).get("total_teams", 0)
        },
        "phase_3_execution_capsules": {
            "status": "active",
            "total_capsules": capsules_data.get("meta", {}).get("total_capsules", 0),
            "active_capsules": capsules_data.get("meta", {}).get("active_capsules", 0),
            "total_modules": capsules_data.get("meta", {}).get("total_modules", 0),
            "total_features": capsules_data.get("meta", {}).get("total_features", 0)
        },
        "operational_summary": {
            "total_data_structures": 6,
            "total_api_endpoints": 20,
            "deployment_status": "production_ready"
        }
    })

@app.route('/intelligence-core')
def intelligence_core_view():
    """Intelligence Core dashboard with 12 engines grouped by lifecycle"""
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Intelligence Core - 12 Engines</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1600px; margin: 0 auto; }
        .back {
            display: inline-block;
            padding: 12px 24px;
            background: rgba(255,255,255,0.1);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            transition: all 0.3s;
        }
        .back:hover { background: rgba(255,255,255,0.2); transform: translateX(-5px); }
        .header {
            text-align: center;
            margin-bottom: 50px;
            background: rgba(255,255,255,0.1);
            padding: 40px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }
        .header h1 { font-size: 3em; margin-bottom: 15px; color: #ffd700; text-shadow: 0 0 20px rgba(255,215,0,0.5); }
        .header p { font-size: 1.3em; opacity: 0.9; }
        .lifecycle-section {
            margin-bottom: 50px;
        }
        .lifecycle-header {
            font-size: 1.8em;
            color: #ffd700;
            margin-bottom: 20px;
            padding: 15px 25px;
            background: rgba(255,215,0,0.15);
            border-left: 4px solid #ffd700;
            border-radius: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .lifecycle-count {
            font-size: 0.6em;
            opacity: 0.8;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .stat-card {
            background: rgba(255,255,255,0.1);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        .stat-card h3 { font-size: 2.5em; color: #ffd700; margin-bottom: 10px; }
        .stat-card p { opacity: 0.8; }
        .status-filter {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        .filter-btn {
            padding: 10px 25px;
            background: rgba(255,255,255,0.1);
            border: 2px solid rgba(255,255,255,0.3);
            color: white;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s;
            backdrop-filter: blur(10px);
            font-size: 0.95em;
            border: none;
        }
        .filter-btn:hover, .filter-btn.active {
            background: rgba(255,215,0,0.3);
            border: 2px solid #ffd700;
            transform: translateY(-3px);
        }
        .engines-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }
        .engine-card {
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            transition: all 0.3s;
            border-left: 5px solid #ffd700;
        }
        .engine-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
            border-left-width: 8px;
        }
        .engine-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }
        .engine-name { font-size: 1.5em; color: #ffd700; font-weight: bold; }
        .engine-status { padding: 6px 16px; border-radius: 20px; font-size: 0.75em; font-weight: bold; white-space: nowrap; }
        .status-active { background: #4CAF50; }
        .status-in_progress { background: #FFA726; }
        .status-planned { background: #42A5F5; }
        .engine-role { font-style: italic; color: #ffd700; margin-bottom: 15px; opacity: 0.9; font-size: 1em; line-height: 1.5; }
        .engine-description { line-height: 1.6; margin-bottom: 20px; opacity: 0.9; }
        .badges-section { margin: 15px 0; }
        .section-title { 
            font-size: 0.85em; 
            color: #ffd700; 
            margin-bottom: 10px; 
            font-weight: bold; 
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .badge {
            display: inline-block;
            padding: 6px 14px;
            background: rgba(255,255,255,0.2);
            border-radius: 20px;
            font-size: 0.85em;
            margin: 4px;
            border: 1px solid rgba(255,255,255,0.3);
        }
        .badge-capsule {
            background: rgba(100, 150, 255, 0.3);
            border-color: rgba(100, 150, 255, 0.5);
        }
        .badge-capability {
            background: rgba(76, 175, 80, 0.3);
            border-color: rgba(76, 175, 80, 0.5);
        }
        .badge-mode {
            background: rgba(138, 43, 226, 0.3);
            border-color: rgba(138, 43, 226, 0.5);
            font-weight: bold;
            text-transform: uppercase;
        }
        .mode-auto { background: rgba(138, 43, 226, 0.4); }
        .mode-hybrid { background: rgba(75, 0, 130, 0.4); }
        .mode-assist { background: rgba(0, 191, 255, 0.4); }
        .mode-off { background: rgba(128, 128, 128, 0.4); }
        .overlays-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid rgba(255,255,255,0.2);
        }
        .overlay-badge {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            border-radius: 10px;
            font-size: 0.85em;
            font-weight: 500;
        }
        .overlay-enabled { 
            background: rgba(76, 175, 80, 0.25); 
            border: 1px solid rgba(76, 175, 80, 0.4);
            color: #90EE90;
        }
        .overlay-disabled { 
            background: rgba(158, 158, 158, 0.15); 
            border: 1px solid rgba(158, 158, 158, 0.3);
            opacity: 0.6;
        }
        .check { font-size: 1.1em; font-weight: bold; }
        .loading { text-align: center; padding: 100px 20px; font-size: 1.5em; }
        .overlay-item {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            margin: 5px;
            padding: 5px 12px;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            font-size: 0.85em;
        }
        .overlay-enabled { background: rgba(76, 175, 80, 0.3); }
        .overlay-disabled { background: rgba(239, 83, 80, 0.3); opacity: 0.6; }
        .loading { text-align: center; padding: 100px 20px; font-size: 1.5em; }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        <div class="header">
            <h1>&#x1F9E0; Intelligence Core</h1>
            <p>12 Advanced Intelligence Engines - Grouped by Lifecycle Stage</p>
        </div>
        <div id="content">
            <div class="loading">Loading Intelligence Core...</div>
        </div>
    </div>
    <script>
        let engines = [];
        
        async function loadEngines() {
            try {
                const response = await fetch('/api/intelligence-core');
                if (!response.ok) throw new Error('Failed to load engines');
                engines = await response.json();
                displayGroupedEngines();
            } catch (error) {
                document.getElementById('content').innerHTML = '<div class="loading">Error: ' + error.message + '</div>';
            }
        }
        
        function displayGroupedEngines() {
            // Group engines by lifecycle
            const lifecycleGroups = {
                'active': [],
                'beta': [],
                'prototype': [],
                'concept': []
            };
            
            engines.forEach(engine => {
                const lifecycle = engine.lifecycle || 'concept';
                if (lifecycleGroups[lifecycle]) {
                    lifecycleGroups[lifecycle].push(engine);
                }
            });
            
            let html = '';
            
            // Display each lifecycle group
            const lifecycleOrder = ['active', 'beta', 'prototype', 'concept'];
            const lifecycleNames = {
                'active': 'Production Ready',
                'beta': 'Beta Testing',
                'prototype': 'Prototype Stage',
                'concept': 'Conceptual Design'
            };
            
            lifecycleOrder.forEach(lifecycle => {
                const groupEngines = lifecycleGroups[lifecycle];
                if (groupEngines.length > 0) {
                    html += '<div class="lifecycle-section">';
                    html += '  <div class="lifecycle-header">';
                    html += '    <span>' + lifecycleNames[lifecycle] + '</span>';
                    html += '    <span class="lifecycle-count">' + groupEngines.length + ' engine' + (groupEngines.length !== 1 ? 's' : '') + '</span>';
                    html += '  </div>';
                    html += '  <div class="engines-grid">';
                    
                    groupEngines.forEach(engine => {
                        html += '<div class="engine-card">';
                        html += '  <div class="engine-header">';
                        html += '    <div class="engine-name">' + engine.name + '</div>';
                        html += '    <div style="display:flex; flex-direction:column; gap:4px;">';
                        html += '      <div class="engine-status status-' + engine.status + '">' + engine.status.replace('_', ' ').toUpperCase() + '</div>';
                        html += '      <div class="badge badge-mode mode-' + engine.operational_mode + '">' + engine.operational_mode + '</div>';
                        html += '    </div>';
                        html += '  </div>';
                        html += '  <div class="engine-role">"' + engine.role + '"</div>';
                        html += '  <div class="engine-description">' + engine.description + '</div>';
                        
                        // Primary Capsules Badges
                        html += '  <div class="badges-section">';
                        html += '    <div class="section-title">Primary Capsules</div>';
                        engine.primary_capsules.forEach(c => {
                            html += '<span class="badge badge-capsule">' + c + '</span>';
                        });
                        html += '  </div>';
                        
                        // Capabilities Badges
                        html += '  <div class="badges-section">';
                        html += '    <div class="section-title">Capabilities</div>';
                        engine.capabilities.forEach(cap => {
                            html += '<span class="badge badge-capability">' + cap.replace(/_/g, ' ') + '</span>';
                        });
                        html += '  </div>';
                        
                        // Overlays Grid
                        html += '  <div class="overlays-grid">';
                        html += '    <div class="overlay-badge ' + (engine.overlays.stewardship ? 'overlay-enabled' : 'overlay-disabled') + '">';
                        html += '      <span class="check">' + (engine.overlays.stewardship ? '&#x2713;' : '&#x2717;') + '</span>';
                        html += '      <span>Stewardship</span>';
                        html += '    </div>';
                        html += '    <div class="overlay-badge ' + (engine.overlays.wellbeing ? 'overlay-enabled' : 'overlay-disabled') + '">';
                        html += '      <span class="check">' + (engine.overlays.wellbeing ? '&#x2713;' : '&#x2717;') + '</span>';
                        html += '      <span>Wellbeing</span>';
                        html += '    </div>';
                        html += '    <div class="overlay-badge ' + (engine.overlays.planetary ? 'overlay-enabled' : 'overlay-disabled') + '">';
                        html += '      <span class="check">' + (engine.overlays.planetary ? '&#x2713;' : '&#x2717;') + '</span>';
                        html += '      <span>Planetary</span>';
                        html += '    </div>';
                        html += '    <div class="overlay-badge ' + (engine.overlays.intergenerational ? 'overlay-enabled' : 'overlay-disabled') + '">';
                        html += '      <span class="check">' + (engine.overlays.intergenerational ? '&#x2713;' : '&#x2717;') + '</span>';
                        html += '      <span>Intergenerational</span>';
                        html += '    </div>';
                        html += '  </div>';
                        
                        html += '</div>';
                    });
                    
                    html += '  </div>';
                    html += '</div>';
                }
            });
            
            document.getElementById('content').innerHTML = html;
        }
        
        loadEngines();
    </script>
</body>
</html>"""
    return render_template_string(html)

# ==================== NEW PLATFORM ARCHITECTURE ENDPOINTS ====================

@app.route('/api/platform-capsules')
def api_platform_capsules():
    """Get all platform capsules (36-capsule architecture)"""
    data = load_json("platform_capsules.json")
    return jsonify(data)

@app.route('/api/platform-capsules/realm/<realm>')
def api_platform_capsules_by_realm(realm):
    """Get platform capsules by realm (foundation, economic, knowledge, community, automation, media)"""
    data = load_json("platform_capsules.json")
    realm_capsules = data.get(realm, [])
    return jsonify({
        "realm": realm,
        "capsules": realm_capsules,
        "count": len(realm_capsules)
    })

@app.route('/api/platform-capsules/<capsule_id>')
def api_platform_capsule_detail(capsule_id):
    """Get specific platform capsule by ID"""
    data = load_json("platform_capsules.json")
    for realm in ["foundation", "economic", "knowledge", "community", "automation", "media"]:
        capsules = data.get(realm, [])
        capsule = next((c for c in capsules if c.get("id") == capsule_id), None)
        if capsule:
            return jsonify(capsule)
    return jsonify({"error": f"Platform capsule not found: {capsule_id}"}), 404

@app.route('/api/engines')
def api_engines():
    """Get all engines"""
    data = load_json("engines.json")
    return jsonify(data)

@app.route('/api/engines/<engine_id>')
def api_engine_detail(engine_id):
    """Get specific engine by ID"""
    data = load_json("engines.json")
    engines = data.get("engines", [])
    engine = next((e for e in engines if e.get("id") == engine_id), None)
    if engine:
        return jsonify(engine)
    return jsonify({"error": f"Engine not found: {engine_id}"}), 404

@app.route('/api/engines/category/<category>')
def api_engines_by_category(category):
    """Get engines by category (content, commerce, intelligence, automation, infrastructure, ai, personalization)"""
    data = load_json("engines.json")
    engines = data.get("engines", [])
    filtered = [e for e in engines if e.get("category") == category]
    return jsonify({
        "category": category,
        "engines": filtered,
        "count": len(filtered)
    })

@app.route('/api/platform-overview')
def api_platform_overview():
    """Get comprehensive platform overview with all key metrics"""
    industries_data = load_json("industries.json")
    niches_data = load_json("niches.json")
    domain_packs_data = load_json("domain_packs.json")
    realms_data = load_json("realms.json")
    agents_data = load_json("agents.json")
    execution_capsules_data = load_json("execution_capsules.json")
    platform_capsules_data = load_json("platform_capsules.json")
    engines_data = load_json("engines.json")
    
    return jsonify({
        "platform": {
            "name": "Codex Dominion Platform Architecture",
            "version": "4.0.0",
            "status": "operational",
            "last_updated": "2025-12-18T00:00:00Z"
        },
        "intelligence_core": {
            "industries": len(industries_data.get("industries", [])),
            "niches": len(niches_data.get("niches", [])),
            "domain_packs": len(domain_packs_data.get("domain_packs", []))
        },
        "realms_and_agents": {
            "realms": len(realms_data.get("realms", [])),
            "agents": len(agents_data.get("agents", [])),
            "agent_teams": len(agents_data.get("agent_teams", []))
        },
        "execution_layer": {
            "execution_capsules": execution_capsules_data.get("meta", {}).get("total_capsules", 0),
            "platform_capsules": platform_capsules_data.get("meta", {}).get("total_capsules", 0),
            "total_modules": (execution_capsules_data.get("meta", {}).get("total_modules", 0) + 
                             platform_capsules_data.get("meta", {}).get("total_modules", 0)),
            "total_features": (execution_capsules_data.get("meta", {}).get("total_features", 0) + 
                              platform_capsules_data.get("meta", {}).get("total_features", 0))
        },
        "processing_engines": {
            "total_engines": engines_data.get("meta", {}).get("total_engines", 0),
            "categories": engines_data.get("meta", {}).get("engine_categories", []),
            "active_engines": len([e for e in engines_data.get("engines", []) if e.get("status") == "active"])
        },
        "tabs": [
            {
                "id": "overview",
                "name": "Overview",
                "endpoint": "/api/platform-overview"
            },
            {
                "id": "capsules",
                "name": "Capsules",
                "endpoint": "/api/platform-capsules",
                "count": platform_capsules_data.get("meta", {}).get("total_capsules", 0)
            },
            {
                "id": "intelligence_core",
                "name": "Intelligence Core",
                "endpoint": "/api/intelligence-core-status"
            },
            {
                "id": "industries",
                "name": "Industries",
                "endpoint": "/api/industries",
                "count": len(industries_data.get("industries", []))
            },
            {
                "id": "platforms",
                "name": "Platforms",
                "endpoint": "/api/engines",
                "count": engines_data.get("meta", {}).get("total_engines", 0)
            },
            {
                "id": "analytics",
                "name": "Analytics",
                "endpoint": "/api/platform-analytics"
            }
        ]
    })

@app.route('/api/platform-analytics')
def api_platform_analytics():
    """Get platform analytics and metrics"""
    industries_data = load_json("industries.json")
    agents_data = load_json("agents.json")
    platform_capsules_data = load_json("platform_capsules.json")
    engines_data = load_json("engines.json")
    
    # Count capsules by status
    all_capsules = []
    for realm in ["foundation", "economic", "knowledge", "community", "automation", "media"]:
        all_capsules.extend(platform_capsules_data.get(realm, []))
    
    status_counts = {
        "active": len([c for c in all_capsules if c.get("status") == "active"]),
        "planned": len([c for c in all_capsules if c.get("status") == "planned"]),
        "concept": len([c for c in all_capsules if c.get("status") == "concept"])
    }
    
    # Count agents by status
    agents = agents_data.get("agents", [])
    agent_status_counts = {
        "active": len([a for a in agents if a.get("status") == "active"]),
        "planned": len([a for a in agents if a.get("status") == "planned"]),
        "concept": len([a for a in agents if a.get("status") == "concept"])
    }
    
    # Count engines by status
    engines = engines_data.get("engines", [])
    engine_status_counts = {
        "active": len([e for e in engines if e.get("status") == "active"]),
        "planned": len([e for e in engines if e.get("status") == "planned"]),
        "concept": len([e for e in engines if e.get("status") == "concept"])
    }
    
    # Realm distribution
    realm_distribution = {
        "foundation": len(platform_capsules_data.get("foundation", [])),
        "economic": len(platform_capsules_data.get("economic", [])),
        "knowledge": len(platform_capsules_data.get("knowledge", [])),
        "community": len(platform_capsules_data.get("community", [])),
        "automation": len(platform_capsules_data.get("automation", [])),
        "media": len(platform_capsules_data.get("media", []))
    }
    
    return jsonify({
        "analytics": {
            "capsule_status": status_counts,
            "agent_status": agent_status_counts,
            "engine_status": engine_status_counts,
            "realm_distribution": realm_distribution,
            "completion_metrics": {
                "capsules_active_percentage": round((status_counts["active"] / sum(status_counts.values()) * 100), 2) if sum(status_counts.values()) > 0 else 0,
                "agents_active_percentage": round((agent_status_counts["active"] / sum(agent_status_counts.values()) * 100), 2) if sum(agent_status_counts.values()) > 0 else 0,
                "engines_active_percentage": round((engine_status_counts["active"] / sum(engine_status_counts.values()) * 100), 2) if sum(engine_status_counts.values()) > 0 else 0
            }
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })

@app.route('/api/mapping/engine-to-capsules/<engine_id>')
def api_map_engine_to_capsules(engine_id):
    """Map a specific engine to its capsules"""
    engines_data = load_json("engines.json")
    engines = engines_data.get("engines", [])
    engine = next((e for e in engines if e.get("id") == engine_id), None)
    
    if not engine:
        return jsonify({"error": f"Engine not found: {engine_id}"}), 404
    
    # Get capsule references from engine
    primary_capsules = engine.get("primary_capsules", [])
    secondary_capsules = engine.get("secondary_capsules", [])
    used_by_capsules = engine.get("used_by_capsules", [])
    
    # Combine all capsule references
    all_capsule_ids = list(set(primary_capsules + secondary_capsules + used_by_capsules))
    
    # Fetch actual capsule data
    execution_data = load_json("execution_capsules.json")
    platform_data = load_json("platform_capsules.json")
    
    capsule_details = []
    for capsule_id in all_capsule_ids:
        # Check execution capsules
        exec_capsules = execution_data.get("execution_capsules", [])
        capsule = next((c for c in exec_capsules if c.get("id") == capsule_id), None)
        if capsule:
            capsule_details.append({
                "id": capsule_id,
                "name": capsule.get("name"),
                "type": "execution",
                "relationship": "primary" if capsule_id in primary_capsules else "secondary" if capsule_id in secondary_capsules else "used_by"
            })
            continue
        
        # Check platform capsules
        for realm in ["foundation", "economic", "knowledge", "community", "automation", "media"]:
            plat_capsules = platform_data.get(realm, [])
            capsule = next((c for c in plat_capsules if c.get("id") == capsule_id), None)
            if capsule:
                capsule_details.append({
                    "id": capsule_id,
                    "name": capsule.get("name"),
                    "type": "platform",
                    "realm": realm,
                    "relationship": "primary" if capsule_id in primary_capsules else "secondary" if capsule_id in secondary_capsules else "used_by"
                })
                break
    
    return jsonify({
        "engine_id": engine_id,
        "engine_name": engine.get("name"),
        "capsules": capsule_details,
        "count": len(capsule_details),
        "breakdown": {
            "primary": len(primary_capsules),
            "secondary": len(secondary_capsules),
            "used_by": len(used_by_capsules)
        }
    })

@app.route('/api/mapping/capsule-to-engines/<capsule_id>')
def api_map_capsule_to_engines(capsule_id):
    """Map a specific capsule to engines that use it"""
    # Get the capsule first
    execution_data = load_json("execution_capsules.json")
    platform_data = load_json("platform_capsules.json")
    
    capsule = None
    capsule_type = None
    capsule_realm = None
    
    # Search execution capsules
    exec_capsules = execution_data.get("execution_capsules", [])
    capsule = next((c for c in exec_capsules if c.get("id") == capsule_id), None)
    if capsule:
        capsule_type = "execution"
    else:
        # Search platform capsules
        for realm in ["foundation", "economic", "knowledge", "community", "automation", "media"]:
            plat_capsules = platform_data.get(realm, [])
            capsule = next((c for c in plat_capsules if c.get("id") == capsule_id), None)
            if capsule:
                capsule_type = "platform"
                capsule_realm = realm
                break
    
    if not capsule:
        return jsonify({"error": f"Capsule not found: {capsule_id}"}), 404
    
    # Get engines referenced by capsule
    capsule_engines = capsule.get("engines", [])
    
    # Find all engines that reference this capsule
    engines_data = load_json("engines.json")
    engines = engines_data.get("engines", [])
    
    related_engines = []
    for engine in engines:
        relationship = None
        if capsule_id in engine.get("primary_capsules", []):
            relationship = "primary"
        elif capsule_id in engine.get("secondary_capsules", []):
            relationship = "secondary"
        elif capsule_id in engine.get("used_by_capsules", []):
            relationship = "used_by"
        elif engine.get("id") in capsule_engines:
            relationship = "capsule_declared"
        
        if relationship:
            related_engines.append({
                "id": engine.get("id"),
                "name": engine.get("name"),
                "category": engine.get("category"),
                "status": engine.get("status"),
                "relationship": relationship
            })
    
    return jsonify({
        "capsule_id": capsule_id,
        "capsule_name": capsule.get("name"),
        "capsule_type": capsule_type,
        "capsule_realm": capsule_realm,
        "engines": related_engines,
        "count": len(related_engines),
        "declared_engines": capsule_engines
    })

# ==================== SIMPLIFIED DIRECT-ACCESS ENDPOINTS ====================

@app.route('/api/direct/capsules')
def direct_get_capsules():
    """Direct access to capsules.json (simplified endpoint)"""
    return jsonify(capsules_json)

@app.route('/api/direct/capsules/<capsule_id>')
def direct_get_capsule(capsule_id):
    """Direct access to specific capsule from capsules.json"""
    for realm in capsules_json.values():
        for capsule in realm:
            if capsule["id"] == capsule_id:
                return jsonify(capsule)
    return jsonify({"error": "Capsule not found"}), 404

@app.route('/api/direct/intelligence-core')
def direct_get_intelligence_core():
    """Direct access to intelligence_core.json (simplified endpoint)"""
    return jsonify(intelligence_json)

@app.route('/api/direct/intelligence-core/<engine_id>')
def direct_get_engine(engine_id):
    """Direct access to specific engine from intelligence_core.json"""
    for engine in intelligence_json.get("engines", []):
        if engine["id"] == engine_id:
            return jsonify(engine)
    return jsonify({"error": "Engine not found"}), 404

# ==================== COUNCILS API ====================

def find_council_by_id(session, council_id):
    """Find council by ID using database"""
    council = session.query(Council).filter(Council.id == council_id).first()
    return council.to_dict() if council else None

def get_council_by_domain(session, domain: str):
    """Find council by domain using database"""
    if not domain:
        return None
    council = session.query(Council).filter(Council.domain == domain).first()
    return council.to_dict() if council else None

@app.route('/api/councils')
def get_councils():
    """Get all councils from database"""
    session = g.db
    councils = session.query(Council).all()
    return jsonify({
        "councils": [c.to_dict() for c in councils]
    })

@app.route('/api/councils/<council_id>')
def get_council_legacy(council_id):
    """Get specific council by ID (legacy)"""
    session = g.db
    council = find_council_by_id(session, council_id)
    if council is None:
        return jsonify({"error": "Council not found", "id": council_id}), 404
    return jsonify(council)

# ==================== TOOLS API ====================

@app.route('/api/tools')
def get_tools():
    """Get all tools from tools suite"""
    return jsonify(tools_json)

@app.route('/api/tools/<tool_id>')
def get_tool(tool_id):
    """Get specific tool by ID"""
    for tool in tools_json.get("tools", []):
        if tool.get("id") == tool_id:
            return jsonify(tool)
    return jsonify({"error": "Tool not found", "id": tool_id}), 404

# ==================== CALCULATORS API ====================

@app.route("/api/calculators/savings", methods=["GET", "POST"])
def savings_calculator():
    """
    Calculate automation savings using the unified calculator module
    
    GET: Returns sample calculation and API documentation
    POST: Calculates savings from request body
    
    Request body (POST):
    {
        "tasks_per_week": 200,
        "time_per_task_minutes": 10,
        "hourly_wage": 25,
        "automation_percent": 0.7,
        "error_rate": 0.1,
        "cost_per_error": 15,
        "value_per_accelerated_task": 0
    }
    """
    # Handle GET request - return sample calculation
    if request.method == "GET":
        sample_input = SavingsInput(
            tasks_per_week=200,
            time_per_task_minutes=10,
            hourly_wage=25,
            automation_percent=0.7,
            error_rate=0.1,
            cost_per_error=15,
            value_per_accelerated_task=0
        )
        result = calculate_savings(sample_input)
        effectiveness = get_effectiveness_rating(result.yearly_savings)
        
        return jsonify({
            "message": "Calculator API - Use POST with JSON body for custom calculations",
            "sample_calculation": {
                "input": {
                    "tasks_per_week": 200,
                    "time_per_task_minutes": 10,
                    "hourly_wage": 25,
                    "automation_percent": 0.7,
                    "error_rate": 0.1,
                    "cost_per_error": 15,
                    "value_per_accelerated_task": 0
                },
                "result": {
                    "success": True,
                    "weekly_savings": result.weekly_savings,
                    "monthly_savings": result.monthly_savings,
                    "yearly_savings": result.yearly_savings,
                    "hours_saved_per_week": result.hours_saved_per_week,
                    "error_savings_weekly": result.error_savings_weekly,
                    "scaling_savings_weekly": result.scaling_savings_weekly,
                    "total_weekly_savings": result.total_weekly_savings,
                    "effectiveness": effectiveness
                }
            }
        })
    
    # Handle POST request - calculate from input
    data = request.get_json(force=True)

    inp = SavingsInput(
        tasks_per_week=float(data.get("tasks_per_week", 0)),
        time_per_task_minutes=float(data.get("time_per_task_minutes", 0)),
        hourly_wage=float(data.get("hourly_wage", 0)),
        automation_percent=float(data.get("automation_percent", 0)),
        error_rate=float(data.get("error_rate", 0)),
        cost_per_error=float(data.get("cost_per_error", 0)),
        value_per_accelerated_task=float(data.get("value_per_accelerated_task", 0)),
    )

    result = calculate_savings(inp)
    effectiveness = get_effectiveness_rating(result.yearly_savings)

    return jsonify({
        "success": True,
        "weekly_savings": result.weekly_savings,
        "monthly_savings": result.monthly_savings,
        "yearly_savings": result.yearly_savings,
        "hours_saved_per_week": result.hours_saved_per_week,
        "error_savings_weekly": result.error_savings_weekly,
        "scaling_savings_weekly": result.scaling_savings_weekly,
        "total_weekly_savings": result.total_weekly_savings,
        "effectiveness": effectiveness
    })

# ==================== WORKFLOW ENGINE API ====================

@app.route("/api/workflows/actions", methods=["GET", "POST"])
def workflow_actions():
    """
    GET: List all workflow actions
    POST: Create a new workflow action
    
    Request body (POST):
    {
        "action_type": "customer_followup",
        "created_by_agent": "jermaine_super_action_ai",
        "inputs": {...},
        "calculated_savings": {...}
    }
    """
    if request.method == "GET":
        # list_workflows() returns list of Workflow objects
        workflows = workflow_engine.list_workflows(limit=100)
        workflows_dict = [w.to_dict() for w in workflows] if workflows else []
        return jsonify({
            "success": True,
            "count": len(workflows_dict),
            "actions": workflows_dict  # Keep 'actions' key for backwards compatibility
        })
    
    # POST - Create new workflow
    data = request.get_json(force=True)
    
    workflow_id = workflow_engine.create_workflow(
        workflow_type_id=data.get("workflow_type_id", "unknown"),
        created_by_agent=data.get("created_by_agent", "system"),
        inputs=data.get("inputs", {}),
        calculated_savings=data.get("calculated_savings", {}),
        assigned_council_id=data.get("assigned_council_id")
    )
    
    workflow = workflow_engine.get_workflow(workflow_id)
    
    return jsonify({
        "success": True,
        "action_id": workflow_id,  # Keep action_id for backwards compatibility
        "workflow_id": workflow_id,
        "status": workflow.status.value,
        "created_at": workflow.created_at.isoformat()
    }), 201

@app.route("/api/workflows/actions/<action_id>", methods=["GET", "PATCH"])
def workflow_action_detail(action_id: str):
    """
    GET: Get action details
    PATCH: Update action status
    
    Request body (PATCH):
    {
        "status": "running" | "completed" | "failed"
    }
    """
    if request.method == "GET":
        workflow = workflow_engine.get_workflow(action_id)
        if not workflow:
            return jsonify({"success": False, "error": "Workflow not found"}), 404
        return jsonify({"success": True, "action": workflow.to_dict()})
    
    # PATCH - Update status
    data = request.get_json(force=True)
    new_status = data.get("status")
    
    if new_status not in ["pending", "running", "completed", "failed"]:
        return jsonify({"success": False, "error": "Invalid status"}), 400
    
    action = workflow_engine.update_status(action_id, new_status)
    if not action:
        return jsonify({"success": False, "error": "Action not found"}), 404
    
    return jsonify({
        "success": True,
        "action_id": action.id,
        "status": action.status,
        "updated_at": action.updated_at
    })

@app.route("/api/workflows/actions/<action_id>/execute", methods=["POST"])
def workflow_action_execute(action_id: str):
    """
    Execute a workflow action (change status to running)
    """
    workflow = workflow_engine.get_workflow(action_id)
    if not workflow:
        return jsonify({"success": False, "error": "Workflow not found"}), 404
    
    workflow_engine.update_status(action_id, "IN_PROGRESS")
    
    return jsonify({
        "success": True,
        "message": f"Action {action_id} execution started",
        "action_id": action_id,
        "status": "running"
    })

# ==================== PRODUCTION WORKFLOW ENDPOINTS ====================

@app.route("/api/workflows", methods=["GET"])
def list_workflows_api():
    """
    List workflows with filters (DB-backed, production-ready)
    
    Query Params:
        status: pending|in_progress|completed|failed|cancelled
        council_id: filter by assigned council
        agent_id: filter by creator agent
        limit: max results (default 100, max 1000)
        offset: pagination offset (default 0)
    
    Returns:
        {
            "workflows": [{workflow_dict}],
            "total": count,
            "limit": limit,
            "offset": offset
        }
    """
    from db import SessionLocal
    from models import Workflow, WorkflowStatus
    
    # Parse query params
    status_filter = request.args.get('status', '').upper()
    council_id = request.args.get('council_id')
    agent_id = request.args.get('agent_id')
    limit = min(int(request.args.get('limit', 100)), 1000)
    offset = int(request.args.get('offset', 0))
    
    session = SessionLocal()
    try:
        # Build query
        query = session.query(Workflow)
        
        # Apply filters
        if status_filter and hasattr(WorkflowStatus, status_filter):
            query = query.filter(Workflow.status == WorkflowStatus[status_filter])
        if council_id:
            query = query.filter(Workflow.assigned_council_id == council_id)
        if agent_id:
            query = query.filter(Workflow.created_by_agent == agent_id)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply pagination and ordering
        workflows = query.order_by(Workflow.created_at.desc()).limit(limit).offset(offset).all()
        
        return jsonify({
            "workflows": [w.to_dict() for w in workflows],
            "total": total,
            "limit": limit,
            "offset": offset
        })
    finally:
        session.close()

@app.route("/api/workflows/<workflow_id>", methods=["GET"])
def get_workflow_api(workflow_id):
    """
    Get single workflow with metrics and votes (DB-backed with joins)
    
    Returns:
        {
            "id": "wf_...",
            "workflow_type_id": "website_creation",
            "created_by_agent": "agent_id",
            "assigned_council_id": "council_media",
            "status": "PENDING",
            "decision": "approved|denied|pending",
            "inputs": {...},
            "outputs": {...},
            "calculated_savings": {...},
            "created_at": "2025-12-20T...",
            "metrics": [{...}],
            "votes": [{"user_id": "...", "vote": "approve|deny", "reason": "..."}]
        }
    """
    from db import SessionLocal
    from models import Workflow, WorkflowMetric, WorkflowVote
    
    session = SessionLocal()
    try:
        # Query workflow with eager loading of relationships
        workflow = session.query(Workflow).filter(Workflow.id == workflow_id).first()
        
        if not workflow:
            return jsonify({"error": "Workflow not found", "id": workflow_id}), 404
        
        # Build response with workflow data
        response = workflow.to_dict()
        
        # Add decision from outputs (set by council voting)
        response["decision"] = workflow.outputs.get("decision", "pending") if workflow.outputs else "pending"
        
        # Add metrics
        metrics = session.query(WorkflowMetric).filter(WorkflowMetric.workflow_id == workflow_id).all()
        response["metrics"] = [m.to_dict() for m in metrics]
        
        # Add votes
        votes = session.query(WorkflowVote).filter(WorkflowVote.workflow_id == workflow_id).all()
        response["votes"] = [v.to_dict() for v in votes]
        
        return jsonify(response)
    finally:
        session.close()

@app.route("/api/workflows/metrics", methods=["GET"])
def workflow_metrics_api():
    """
    Analytics summary (DB-backed aggregations)
    
    Returns:
        {
            "total_workflows": 150,
            "total_weekly_savings": 5247.50,
            "average_duration_seconds": 45.3,
            "status_distribution": {
                "PENDING": 20,
                "IN_PROGRESS": 5,
                "COMPLETED": 120,
                "FAILED": 5
            },
            "workflows_by_agent": {
                "agent_jermaine": 50,
                "content_creator_agent": 30
            },
            "workflows_by_council": {
                "council_media": 80,
                "council_commerce": 70
            },
            "workflows_by_type": {
                "website_creation": 45,
                "content_scheduler": 35
            }
        }
    """
    from db import SessionLocal
    from models import Workflow, WorkflowMetric, WorkflowStatus
    from sqlalchemy import func
    
    session = SessionLocal()
    try:
        # Total workflows
        total_workflows = session.query(func.count(Workflow.id)).scalar()
        
        # Total weekly savings
        workflows = session.query(Workflow).all()
        total_weekly_savings = sum(
            (w.calculated_savings or {}).get("total_weekly_savings", 0) or
            (w.calculated_savings or {}).get("weekly_savings", 0)
            for w in workflows
        )
        
        # Average duration from metrics
        avg_duration = session.query(func.avg(WorkflowMetric.duration_seconds)).scalar() or 0
        
        # Status distribution
        status_counts = session.query(
            Workflow.status,
            func.count(Workflow.id)
        ).group_by(Workflow.status).all()
        status_distribution = {status.value: count for status, count in status_counts}
        
        # Workflows by agent
        agent_counts = session.query(
            Workflow.created_by_agent,
            func.count(Workflow.id)
        ).group_by(Workflow.created_by_agent).all()
        workflows_by_agent = {agent: count for agent, count in agent_counts}
        
        # Workflows by council
        council_counts = session.query(
            Workflow.assigned_council_id,
            func.count(Workflow.id)
        ).filter(Workflow.assigned_council_id.isnot(None)).group_by(Workflow.assigned_council_id).all()
        workflows_by_council = {council: count for council, count in council_counts}
        
        # Workflows by type
        type_counts = session.query(
            Workflow.workflow_type_id,
            func.count(Workflow.id)
        ).group_by(Workflow.workflow_type_id).all()
        workflows_by_type = {wf_type: count for wf_type, count in type_counts}
        
        return jsonify({
            "total_workflows": total_workflows,
            "total_weekly_savings": float(total_weekly_savings),
            "average_duration_seconds": float(avg_duration),
            "status_distribution": status_distribution,
            "workflows_by_agent": workflows_by_agent,
            "workflows_by_council": workflows_by_council,
            "workflows_by_type": workflows_by_type
        })
    finally:
        session.close()

@app.route("/api/analytics/summary", methods=["GET"])
def analytics_summary():
    """Get analytics summary with total workflows, savings, and duration."""
    try:
        # Get all workflows from database
        workflows = workflow_engine.list_workflows(limit=1000)
        workflows_dict = [w.to_dict() for w in workflows] if workflows else []
        
        total_workflows = len(workflows_dict)
        total_weekly_savings = sum(
            w.get("calculated_savings", {}).get("total_weekly_savings", 0) 
            for w in workflows_dict
        )
        
        # Calculate average duration for completed workflows
        completed_workflows = [w for w in workflows_dict if w.get("status") == "COMPLETED"]
        if completed_workflows:
            durations = [
                (w.get("completed_at") - w.get("created_at")).total_seconds() 
                for w in completed_workflows if w.get("completed_at") and w.get("created_at")
            ]
            avg_duration = sum(durations) / len(durations) if durations else 0
        else:
            avg_duration = 0

        return jsonify({
            "total_workflows_completed": len(completed_actions),
            "total_estimated_weekly_savings": round(total_weekly_savings, 2),
            "average_workflow_duration_seconds": round(avg_duration, 2)
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ==================== COUNCIL API ENDPOINTS ====================

from council_engine import council_engine, CouncilOversight, get_council_by_domain, council_allows_action
from workflow_catalog import get_workflow_type, get_workflow_domain, list_workflow_types

@app.route("/api/councils", methods=["GET"])
def list_councils():
    """List all councils with optional status filter"""
    status = request.args.get("status")
    councils = council_engine.list_councils(status=status)
    
    councils_data = []
    for council in councils:
        councils_data.append({
            "id": council.id,
            "name": council.name,
            "purpose": council.purpose,
            "primary_engines": council.primary_engines,
            "agents": council.agents,
            "domains": council.domains,
            "oversight": {
                "review_actions": council.oversight.review_actions,
                "review_threshold_weekly_savings": council.oversight.review_threshold_weekly_savings,
                "blocked_action_types": council.oversight.blocked_action_types
            },
            "status": council.status,
            "created_at": council.created_at,
            "updated_at": council.updated_at
        })
    
    return jsonify({
        "success": True,
        "count": len(councils_data),
        "councils": councils_data
    })

@app.route("/api/councils/<council_id>", methods=["GET"])
def get_council(council_id):
    """Get a specific council by ID"""
    council = council_engine.get_council(council_id)
    if not council:
        return jsonify({"success": False, "error": "Council not found"}), 404
    
    return jsonify({
        "success": True,
        "council": {
            "id": council.id,
            "name": council.name,
            "purpose": council.purpose,
            "primary_engines": council.primary_engines,
            "agents": council.agents,
            "domains": council.domains,
            "oversight": {
                "review_actions": council.oversight.review_actions,
                "review_threshold_weekly_savings": council.oversight.review_threshold_weekly_savings,
                "blocked_action_types": council.oversight.blocked_action_types
            },
            "status": council.status,
            "created_at": council.created_at,
            "updated_at": council.updated_at
        }
    })

@app.route("/api/councils", methods=["POST"])
def create_council():
    """Create a new council"""
    data = request.json
    
    required_fields = ["name", "purpose", "primary_engines", "agents", "domains", "oversight"]
    for field in required_fields:
        if field not in data:
            return jsonify({"success": False, "error": f"Missing required field: {field}"}), 400
    
    try:
        oversight_data = data["oversight"]
        oversight = CouncilOversight(
            review_actions=oversight_data.get("review_actions", True),
            review_threshold_weekly_savings=oversight_data.get("review_threshold_weekly_savings", 5000),
            blocked_action_types=oversight_data.get("blocked_action_types", [])
        )
        
        council = council_engine.create_council(
            name=data["name"],
            purpose=data["purpose"],
            primary_engines=data["primary_engines"],
            agents=data["agents"],
            domains=data["domains"],
            oversight=oversight,
            council_id=data.get("id")
        )
        
        return jsonify({
            "success": True,
            "message": "Council created successfully",
            "council_id": council.id
        }), 201
        
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to create council: {str(e)}"}), 500

@app.route("/api/councils/<council_id>", methods=["PATCH"])
def update_council(council_id):
    """Update a council's properties"""
    data = request.json
    
    council = council_engine.update_council(council_id, **data)
    if not council:
        return jsonify({"success": False, "error": "Council not found"}), 404
    
    return jsonify({
        "success": True,
        "message": "Council updated successfully",
        "council_id": council.id
    })

@app.route("/api/councils/<council_id>", methods=["DELETE"])
def delete_council(council_id):
    """Delete a council"""
    success = council_engine.delete_council(council_id)
    if not success:
        return jsonify({"success": False, "error": "Council not found"}), 404
    
    return jsonify({
        "success": True,
        "message": "Council deleted successfully"
    })

@app.route("/api/councils/<council_id>/agents", methods=["POST"])
def add_agent_to_council(council_id):
    """Add an agent to a council"""
    data = request.json
    agent_id = data.get("agent_id")
    
    if not agent_id:
        return jsonify({"success": False, "error": "Missing agent_id"}), 400
    
    success = council_engine.add_agent_to_council(council_id, agent_id)
    if not success:
        return jsonify({"success": False, "error": "Council not found"}), 404
    
    return jsonify({
        "success": True,
        "message": f"Agent {agent_id} added to council {council_id}"
    })

@app.route("/api/councils/<council_id>/agents/<agent_id>", methods=["DELETE"])
def remove_agent_from_council(council_id, agent_id):
    """Remove an agent from a council"""
    success = council_engine.remove_agent_from_council(council_id, agent_id)
    if not success:
        return jsonify({"success": False, "error": "Council not found"}), 404
    
    return jsonify({
        "success": True,
        "message": f"Agent {agent_id} removed from council {council_id}"
    })

@app.route("/api/councils/<council_id>/check-action", methods=["POST"])
def check_action_allowed(council_id):
    """Check if an action is allowed by council oversight"""
    data = request.json
    action_type = data.get("action_type")
    
    if not action_type:
        return jsonify({"success": False, "error": "Missing action_type"}), 400
    
    allowed = council_engine.check_action_allowed(action_type, council_id)
    
    return jsonify({
        "success": True,
        "action_type": action_type,
        "allowed": allowed,
        "council_id": council_id
    })

@app.route("/api/councils/<council_id>/review-required", methods=["POST"])
def check_review_required(council_id):
    """Check if an action requires council review based on savings threshold"""
    data = request.json
    weekly_savings = data.get("weekly_savings", 0)
    
    requires_review = council_engine.requires_review(weekly_savings, council_id)
    
    return jsonify({
        "success": True,
        "weekly_savings": weekly_savings,
        "requires_review": requires_review,
        "council_id": council_id
    })

@app.route("/api/councils/by-agent/<agent_id>", methods=["GET"])
def get_councils_by_agent(agent_id):
    """Get all councils that include a specific agent"""
    councils = council_engine.get_councils_by_agent(agent_id)
    
    councils_data = []
    for council in councils:
        councils_data.append({
            "id": council.id,
            "name": council.name,
            "purpose": council.purpose,
            "status": council.status
        })
    
    return jsonify({
        "success": True,
        "agent_id": agent_id,
        "count": len(councils_data),
        "councils": councils_data
    })

@app.route("/api/councils/by-domain/<domain>", methods=["GET"])
def get_councils_by_domain(domain):
    """Get all councils that oversee a specific domain"""
    councils = council_engine.get_councils_by_domain(domain)
    
    councils_data = []
    for council in councils:
        councils_data.append({
            "id": council.id,
            "name": council.name,
            "purpose": council.purpose,
            "status": council.status
        })
    
    return jsonify({
        "success": True,
        "domain": domain,
        "count": len(councils_data),
        "councils": councils_data
    })

# ==================== WORKFLOW CATALOG API ====================

@app.route("/api/workflows/types", methods=["GET"])
def api_list_workflow_types():
    """List all available workflow types"""
    return jsonify({
        "success": True,
        "workflow_types": list_workflow_types()
    })

@app.route("/api/workflows/types/<workflow_type_id>", methods=["GET"])
def api_get_workflow_type(workflow_type_id):
    """Get details for a specific workflow type"""
    wt = get_workflow_type(workflow_type_id)
    if not wt:
        return jsonify({"success": False, "error": "Workflow type not found"}), 404
    
    return jsonify({
        "success": True,
        "workflow_type": {
            "id": wt.id,
            "name": wt.name,
            "description": wt.description,
            "category": wt.category,
            "domain": wt.domain,
            "required_inputs": wt.required_inputs,
            "default_calculator_profile": wt.default_calculator_profile
        }
    })

@app.route("/api/workflow-types", methods=["GET"])
def api_list_workflow_types_simple():
    """List all available workflow types (simplified endpoint, no wrapper)"""
    return jsonify(list_workflow_types())

@app.route("/api/workflow-suggestions", methods=["POST"])
def workflow_suggestions():
    """
    body: { "message": "text from user" }
    currently: naive keyword-based matcher; later you can replace with LLM-powered suggestions
    """
    data = request.get_json(force=True)
    message = (data.get("message") or "").lower()

    all_types = list_workflow_types()
    suggestions = []

    for wid, wt in all_types.items():
        name = wt["name"].lower()
        desc = wt["description"].lower()
        category = wt["category"].lower()
        if any(
            kw in message
            for kw in [
                "follow up", "follow-up", "customer", "clients"
            ]
        ) and wid == "customer_followup":
            suggestions.append(wt)
        elif any(
            kw in message
            for kw in ["invoice", "payment", "unpaid"]
        ) and wid == "invoice_reminders":
            suggestions.append(wt)
        elif any(
            kw in message
            for kw in ["content", "posts", "social", "publish"]
        ) and wid == "content_scheduler":
            suggestions.append(wt)

    if not suggestions:
        # default: just return everything as options for now
        suggestions = list(all_types.values())

    return jsonify({
        "message": message,
        "suggestions": suggestions
    })

# ==================== DASHBOARD META API ====================

@app.route('/api/dashboard/tabs')
def get_dashboard_tabs():
    """Get available dashboard tabs"""
    return jsonify({
        "tabs": [
            "Overview",
            "Capsules",
            "Intelligence Core",
            "AI Agents",
            "Councils",
            "Tools",
            "Industries",
            "Platforms",
            "Documents",
            "Email",
            "Analytics",
            "Settings"
        ]
    })

@app.route('/api/dashboard/overview')
def get_dashboard_overview():
    """Get dashboard overview statistics"""
    # Count capsules from all realms
    capsule_count = 0
    if isinstance(capsules_json, dict):
        for realm_capsules in capsules_json.values():
            if isinstance(realm_capsules, list):
                capsule_count += len(realm_capsules)
    
    # intelligence_json is an array, not a dict with "engines" key
    engine_count = len(intelligence_json) if isinstance(intelligence_json, list) else 0
    realm_count = len(capsules_json.keys()) if isinstance(capsules_json, dict) else 0
    agents_count = len(agents_json.get("agents", [])) if isinstance(agents_json, dict) else 0
    # Get councils count from database
    session = g.db
    councils_count = session.query(Council).count()
    tools_count = len(tools_json.get("tools", [])) if isinstance(tools_json, dict) else 0

    return jsonify({
        "capsule_count": capsule_count,
        "engine_count": engine_count,
        "realm_count": realm_count,
        "agents_count": agents_count,
        "councils_count": councils_count,
        "tools_count": tools_count,
        "status": "operational",
        "uptime": "99.9%"
    })

# ==================== CAPSULES BY REALM API ====================

@app.route('/api/capsules/realm/<realm_name>')
def get_capsules_by_realm(realm_name):
    """Get all capsules for a specific realm"""
    if not isinstance(capsules_json, dict):
        return jsonify({"error": "Capsules config not loaded"}), 500
    
    realm = capsules_json.get(realm_name.lower())
    if realm is None:
        return jsonify({"error": "Realm not found", "realm": realm_name}), 404
    
    return jsonify(realm)

# ==================== DIGITAL GOVERNMENT BACKEND APIS ====================

@app.route('/api/workflows/pending-review', methods=['GET'])
def get_pending_reviews():
    """
    Get workflows pending council review
    Query params:
      - council_id (optional): Filter by council ID
    """
    council_id = request.args.get('council_id')
    
    # Load workflow actions from workflow_engine
    workflow_actions = []
    try:
        from workflow_engine import get_all_actions
        workflow_actions = get_all_actions()
    except:
        # Fallback: return mock data for development
        workflow_actions = []
    
    # Filter for pending reviews
    pending_reviews = []
    for action in workflow_actions:
        # Check if action requires review
        if hasattr(action, 'decision') and action.decision == 'pending':
            # Find associated council
            assigned_council_id = getattr(action, 'assigned_council_id', None)
            
            # Apply council filter if specified
            if council_id and assigned_council_id != council_id:
                continue
            
            # Find council details
            council = find_council_by_id(assigned_council_id) if assigned_council_id else None
            
            # Build review object
            review = {
                "id": action.action_id,
                "workflow_name": action.workflow_type,
                "workflow_type": action.workflow_type,
                "agent_id": getattr(action, 'created_by_agent', 'unknown'),
                "agent_name": getattr(action, 'created_by_agent', 'Unknown Agent').replace('_', ' ').title(),
                "council_id": assigned_council_id,
                "council_name": council.get('name', 'Unknown Council') if council else 'Unknown Council',
                "domain": council.get('domain', 'general') if council else 'general',
                "estimated_weekly_savings": action.savings_metrics.get('weekly', 0) if hasattr(action, 'savings_metrics') else 0,
                "estimated_monthly_savings": action.savings_metrics.get('monthly', 0) if hasattr(action, 'savings_metrics') else 0,
                "estimated_yearly_savings": action.savings_metrics.get('yearly', 0) if hasattr(action, 'savings_metrics') else 0,
                "hours_saved_weekly": action.savings_metrics.get('hours_weekly', 0) if hasattr(action, 'savings_metrics') else 0,
                "status": action.decision,
                "created_at": action.created_at.isoformat() if hasattr(action, 'created_at') else None,
                "votes": getattr(action, 'votes', [])
            }
            pending_reviews.append(review)
    
    return jsonify({
        "reviews": pending_reviews,
        "total": len(pending_reviews),
        "filter": {"council_id": council_id} if council_id else {}
    })

@app.route('/api/workflows/<action_id>/vote', methods=['POST'])
def council_vote(action_id):
    """
    Submit a council vote on a workflow
    Request body:
    {
        "member_id": "agent_id",
        "vote": "approve" | "deny",
        "reason": "explanation"
    }
    """
    data = request.get_json(force=True)
    member_id = data.get('member_id')
    vote_type = data.get('vote')
    reason = data.get('reason', '')
    
    if not member_id or not vote_type:
        return jsonify({"error": "member_id and vote are required"}), 400
    
    if vote_type not in ['approve', 'deny']:
        return jsonify({"error": "vote must be 'approve' or 'deny'"}), 400
    
    # Get workflow object
    workflow = workflow_engine.get_workflow(action_id)
    if not workflow:
        return jsonify({"error": "Workflow not found"}), 404
    
    try:
        # Note: workflow.votes would need to be added to Workflow model
        # For now, store in workflow.outputs as workaround
        votes = workflow.outputs.get("votes", [])
        votes.append({
            "member_id": member_id,
            "vote": vote_type,
            "reason": reason,
            "timestamp": _time.time()
        })
        
        # Update workflow outputs with votes
        workflow.outputs["votes"] = votes
        
        # Tally votes against council rules
        if workflow.assigned_council_id:
            council = find_council_by_id(workflow.assigned_council_id)
            if council:
                # Count votes
                approve_votes = sum(1 for v in votes if v["vote"] == "approve")
                deny_votes = sum(1 for v in votes if v["vote"] == "deny")
                
                # Simple majority decision
                if approve_votes > deny_votes:
                    workflow.outputs["decision"] = "approved"
                    workflow_engine.update_status(workflow.id, "IN_PROGRESS")
                elif deny_votes > approve_votes:
                    workflow.outputs["decision"] = "denied"
                    workflow_engine.update_status(workflow.id, "FAILED")
                else:
                    workflow.outputs["decision"] = "pending"
        
        return jsonify({
            "action_id": workflow.id,
            "votes": votes,
            "decision": workflow.outputs.get("decision", "pending")
        })
    
    except Exception as e:
        # Development fallback
        return jsonify({
            "success": True,
            "action_id": action_id,
            "vote_recorded": {
                "member_id": member_id,
                "vote": vote_type,
                "reason": reason,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            },
            "note": "Development mode - vote recorded but not persisted"
        })

def calculate_reputation_score(agent_data):
    """
    Calculate normalized reputation score for an agent
    Formula: R = 0.5*S + 0.3*A + 0.2*V
    Where:
    - S = normalized savings (0-1)
    - A = approval/success rate (0-1)
    - V = normalized workflow volume (0-1)
    
    Returns score between 0-1 and simplified reputation object
    """
    reputation = agent_data.get("reputation", {})
    
    # Get raw metrics
    total_savings = reputation.get("total_savings_generated", 0)
    success_rate = reputation.get("success_rate", 0)
    total_actions = reputation.get("total_actions", 0)
    
    # Normalize savings (assume max ~500k for normalization)
    S = min(total_savings / 500000, 1.0)
    
    # Approval rate is already 0-1
    A = success_rate
    
    # Normalize volume (assume max ~1500 actions for normalization)
    V = min(total_actions / 1500, 1.0)
    
    # Calculate weighted score (0-1 range)
    reputation_score = (0.5 * S) + (0.3 * A) + (0.2 * V)
    
    # Return simplified format with score as decimal (0-1)
    return {
        "score": round(reputation_score, 3),
        "total_savings": total_savings,
        "workflows_executed": total_actions,
        "approval_rate": round(success_rate, 3)
    }

def calculate_reputation_score_legacy(agent_data):
    """Legacy function that returns score 0-100 (kept for backward compatibility)"""
    rep = calculate_reputation_score(agent_data)
    return round(rep["score"] * 100, 2)

@app.route('/api/agents/leaderboard', methods=['GET'])
def get_agent_leaderboard():
    """Get agent leaderboard with simplified reputation scores"""
    # Load agent reputation data
    reputation_data = load_json("agent_reputation.json", use_cache=False)
    
    if not reputation_data or not isinstance(reputation_data, dict):
        return jsonify({"error": "Agent reputation data not available"}), 500
    
    # Calculate reputation scores for all agents
    agents = reputation_data.get("agents", [])
    for agent in agents:
        # Replace existing reputation with simplified format
        simplified_rep = calculate_reputation_score(agent)
        agent["reputation"] = simplified_rep
    
    # Sort by score (0-1 range)
    # Sort by score (0-1 range)
    agents.sort(key=lambda x: x["reputation"].get("score", 0), reverse=True)
    reputation_data["agents"] = agents
    
    return jsonify(reputation_data)

@app.route('/api/agents/<agent_id>', methods=['GET'])
def get_agent_details(agent_id):
    """Get detailed information for a specific agent with simplified reputation score"""
    reputation_data = load_json("agent_reputation.json", use_cache=False)
    
    if not reputation_data or not isinstance(reputation_data, dict):
        return jsonify({"error": "Agent reputation data not available"}), 500
    
    # Find agent by ID
    for agent in reputation_data.get("agents", []):
        if agent.get("id") == agent_id:
            # Replace reputation with simplified format
            agent["reputation"] = calculate_reputation_score(agent)
            return jsonify(agent)
    
    return jsonify({"error": "Agent not found", "id": agent_id}), 404

@app.route('/api/agents/<agent_id>/reputation', methods=['GET'])
def get_agent_reputation(agent_id):
    """Get simplified reputation metrics for a specific agent"""
    reputation_data = load_json("agent_reputation.json", use_cache=False)
    
    if not reputation_data or not isinstance(reputation_data, dict):
        return jsonify({"error": "Agent reputation data not available"}), 500
    
    # Find agent by ID and return simplified reputation
    for agent in reputation_data.get("agents", []):
        if agent.get("id") == agent_id:
            return jsonify(calculate_reputation_score(agent))
    
    return jsonify({"error": "Agent not found", "id": agent_id}), 404

@app.route('/api/analytics/agent-performance', methods=['GET'])
def get_agent_performance():
    """
    Get aggregated agent performance analytics
    Returns metrics like:
    - Total agents
    - Total savings across all agents
    - Average success rate
    - Top performers
    - Performance trends
    """
    reputation_data = load_json("agent_reputation.json", use_cache=False)
    
    if not reputation_data or not isinstance(reputation_data, dict):
        return jsonify({"error": "Agent reputation data not available"}), 500
    
    agents = reputation_data.get("agents", [])
    
    # Calculate aggregate metrics
    total_agents = len(agents)
    total_savings = sum(agent.get("reputation", {}).get("total_savings_generated", 0) for agent in agents)
    total_actions = sum(agent.get("reputation", {}).get("total_actions", 0) for agent in agents)
    successful_actions = sum(agent.get("reputation", {}).get("successful_actions", 0) for agent in agents)
    avg_success_rate = (successful_actions / total_actions) if total_actions > 0 else 0
    
    # Top performers
    top_by_savings = sorted(agents, key=lambda a: a.get("reputation", {}).get("total_savings_generated", 0), reverse=True)[:5]
    top_by_success_rate = sorted(agents, key=lambda a: a.get("reputation", {}).get("success_rate", 0), reverse=True)[:5]
    
    # Performance by level
    performance_by_level = {}
    for agent in agents:
        level = agent.get("reputation", {}).get("level", "unknown")
        if level not in performance_by_level:
            performance_by_level[level] = {
                "count": 0,
                "total_savings": 0,
                "total_actions": 0
            }
        performance_by_level[level]["count"] += 1
        performance_by_level[level]["total_savings"] += agent.get("reputation", {}).get("total_savings_generated", 0)
        performance_by_level[level]["total_actions"] += agent.get("reputation", {}).get("total_actions", 0)
    
    return jsonify({
        "overview": {
            "total_agents": total_agents,
            "total_savings": total_savings,
            "total_actions": total_actions,
            "successful_actions": successful_actions,
            "avg_success_rate": round(avg_success_rate, 3)
        },
        "top_performers": {
            "by_savings": [
                {
                    "id": agent.get("id"),
                    "name": agent.get("name"),
                    "total_savings": agent.get("reputation", {}).get("total_savings_generated", 0)
                } for agent in top_by_savings
            ],
            "by_success_rate": [
                {
                    "id": agent.get("id"),
                    "name": agent.get("name"),
                    "success_rate": agent.get("reputation", {}).get("success_rate", 0)
                } for agent in top_by_success_rate
            ]
        },
        "performance_by_level": performance_by_level
    })

def evaluate_council_decision(council, action):
    """
    Evaluate council decision based on voting rules
    Returns: "approved", "denied", or "pending"
    """
    votes = getattr(action, 'votes', [])
    oversight = council.get('oversight', {})
    
    approve_votes = sum(1 for v in votes if v.get('vote') == 'approve')
    deny_votes = sum(1 for v in votes if v.get('vote') == 'deny')
    total_votes = len(votes)
    
    # Check minimum votes
    min_votes = oversight.get('min_votes', 1)
    if total_votes < min_votes:
        return 'pending'
    
    # Check majority requirement
    if oversight.get('requires_majority_vote', False):
        if approve_votes > deny_votes:
            return 'approved'
        elif deny_votes >= approve_votes:
            return 'denied'
    else:
        # Any approve vote passes
        if approve_votes > 0:
            return 'approved'
        if deny_votes > 0:
            return 'denied'
    
    return 'pending'

# ==================== END PLATFORM ARCHITECTURE ENDPOINTS ====================

# ==================== AUTOMATION TIMELINE ROUTES ====================
try:
    from automation_timeline_api import register_automation_timeline_routes
    register_automation_timeline_routes(app)
    print("✓ Automation Timeline API registered")
except ImportError as e:
    print(f"⚠️ Automation Timeline API not available: {e}")
except Exception as e:
    print(f"⚠️ Error registering Automation Timeline API: {e}")
# ==================== END AUTOMATION TIMELINE ROUTES ====================

# ==================== AUTOMATION DEBUGGER ROUTES ====================
try:
    from automation_debugger_api import register_automation_debugger_routes
    register_automation_debugger_routes(app)
    print("✓ Automation Debugger API registered")
except ImportError as e:
    print(f"⚠️ Automation Debugger API not available: {e}")
except Exception as e:
    print(f"⚠️ Error registering Automation Debugger API: {e}")
# ==================== END AUTOMATION DEBUGGER ROUTES ====================

# ==================== AI ADVISOR ROUTES ====================
try:
    from advisor_api import register_advisor_routes
    register_advisor_routes(app)
    print("✓ AI Advisor API registered")
except ImportError as e:
    print(f"⚠️ AI Advisor API not available: {e}")
except Exception as e:
    print(f"⚠️ Error registering AI Advisor API: {e}")
# ==================== END AI ADVISOR ROUTES ====================

# ==================== VIDEO STUDIO ROUTES ====================

@app.route('/studio/video')
def video_studio():
    """Video Studio - Temple of Motion"""
    return render_template('video_studio.html')

@app.route('/studio/video/library')
def video_library():
    """Video project library"""
    try:
        from database import SessionLocal
        session = SessionLocal()
        
        # Get user's video projects
        projects = session.query(VideoProject)\
            .filter_by(user_id=session.get('user_id', 'user_001'))\
            .order_by(VideoProject.updated_at.desc())\
            .all()
        
        session.close()
        
        return jsonify({
            'success': True,
            'projects': [{
                'id': p.id,
                'title': p.title,
                'thumbnail_url': p.thumbnail_url,
                'duration': p.duration,
                'status': p.status,
                'updated_at': p.updated_at.isoformat() if p.updated_at else None
            } for p in projects]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/studio/video/team/<team_id>')
def team_video_library(team_id):
    """Team video project library"""
    try:
        from database import SessionLocal
        session = SessionLocal()
        
        projects = session.query(VideoProject)\
            .filter_by(team_id=team_id)\
            .order_by(VideoProject.updated_at.desc())\
            .all()
        
        session.close()
        
        return jsonify({
            'success': True,
            'team_id': team_id,
            'projects': [{
                'id': p.id,
                'title': p.title,
                'thumbnail_url': p.thumbnail_url,
                'duration': p.duration,
                'status': p.status,
                'created_by': p.user_id,
                'updated_at': p.updated_at.isoformat() if p.updated_at else None
            } for p in projects]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/video/generate-scene', methods=['POST'])
def generate_video_scene():
    """
    Generate a video scene using Universal Generation Interface (UGI).
    
    Complete pipeline: prompt → engine → storage → thumbnail → database → timeline
    """
    try:
        # Initialize UGI if needed
        if video_ugi is None:
            initialize_ugi()
        
        data = request.get_json()
        prompt = data.get('prompt')
        engine = data.get('engine', 'runway')
        project_id = data.get('project_id')
        user_id = data.get('user_id', 1)  # Default to user 1
        
        # Extract settings
        settings = {
            'duration': data.get('duration', 5),
            'aspect_ratio': data.get('aspect_ratio', '16:9'),
            'motion_scale': data.get('motion_scale'),
            'motion': data.get('motion'),
            'guidance_scale': data.get('guidance_scale'),
            'seed': data.get('seed')
        }
        
        # Remove None values
        settings = {k: v for k, v in settings.items() if v is not None}
        
        if not prompt:
            return jsonify({'success': False, 'error': 'Prompt required'}), 400
        
        # Use UGI for complete pipeline
        result = video_ugi.generate(
            prompt=prompt,
            engine=engine,
            project_id=project_id,
            user_id=user_id,
            **settings
        )
        
        return jsonify({
            'success': True,
            'asset_id': result['asset_id'],
            'video_url': result['video_url'],
            'thumbnail_url': result['thumbnail_url'],
            'duration': result['duration'],
            'engine': result['engine'],
            'prompt': result['prompt'],
            'created_at': result['created_at']
        })
        
    except Exception as e:
        print(f"❌ Generation error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/video/save-project', methods=['POST'])
def save_video_project():
    """Save or update a video project"""
    try:
        data = request.get_json()
        project_id = data.get('project_id')
        
        from database import SessionLocal
        session = SessionLocal()
        
        if project_id:
            # Update existing project
            project = session.query(VideoProject).filter_by(id=project_id).first()
            if not project:
                return jsonify({'success': False, 'error': 'Project not found'}), 404
        else:
            # Create new project
            project = VideoProject(
                user_id=session.get('user_id', 'user_001'),
                team_id=data.get('team_id'),
                status='draft'
            )
            session.add(project)
        
        # Update fields
        project.title = data.get('title', project.title)
        project.description = data.get('description', project.description)
        project.storyboard = data.get('storyboard', project.storyboard)
        project.timeline = data.get('timeline', project.timeline)
        project.audio_tracks = data.get('audio_tracks', project.audio_tracks)
        project.tags = data.get('tags', project.tags)
        project.category = data.get('category', project.category)
        project.updated_at = datetime.utcnow()
        
        session.commit()
        project_id = project.id
        session.close()
        
        return jsonify({
            'success': True,
            'project_id': project_id,
            'message': 'Project saved successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/video/project/<project_id>')
def get_video_project(project_id):
    """Get a video project by ID"""
    try:
        from database import SessionLocal
        session = SessionLocal()
        
        project = session.query(VideoProject).filter_by(id=project_id).first()
        
        if not project:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        result = {
            'success': True,
            'project': {
                'id': project.id,
                'title': project.title,
                'description': project.description,
                'video_url': project.video_url,
                'thumbnail_url': project.thumbnail_url,
                'duration': project.duration,
                'storyboard': project.storyboard,
                'timeline': project.timeline,
                'audio_tracks': project.audio_tracks,
                'tags': project.tags,
                'category': project.category,
                'status': project.status,
                'created_at': project.timestamp.isoformat() if project.timestamp else None,
                'updated_at': project.updated_at.isoformat() if project.updated_at else None
            }
        }
        
        session.close()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== VIDEO STUDIO PHASE 2: TIMELINE ENGINE + SCENE EDITOR ====================

@app.route('/api/video/timeline/add-clip', methods=['POST'])
def add_timeline_clip():
    """Add a clip to the timeline"""
    try:
        data = request.get_json()
        
        from database import SessionLocal
        session = SessionLocal()
        
        clip = TimelineClip(
            project_id=data['project_id'],
            asset_id=data['asset_id'],
            track_id=data['track_id'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            source_start=data.get('source_start', 0.0),
            source_end=data.get('source_end'),
            volume=data.get('volume', 1.0),
            opacity=data.get('opacity', 1.0),
            scene_id=data.get('scene_id')
        )
        
        session.add(clip)
        session.commit()
        clip_id = clip.id
        session.close()
        
        return jsonify({
            'success': True,
            'clip_id': clip_id,
            'message': 'Clip added to timeline'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/video/timeline/update-clip/<clip_id>', methods=['PUT'])
def update_timeline_clip(clip_id):
    """Update timeline clip properties (position, trim, effects)"""
    try:
        data = request.get_json()
        
        from database import SessionLocal
        session = SessionLocal()
        
        clip = session.query(TimelineClip).filter_by(id=clip_id).first()
        if not clip:
            return jsonify({'success': False, 'error': 'Clip not found'}), 404
        
        # Update position
        if 'start_time' in data:
            clip.start_time = data['start_time']
        if 'end_time' in data:
            clip.end_time = data['end_time']
        
        # Update trimming
        if 'source_start' in data:
            clip.source_start = data['source_start']
        if 'source_end' in data:
            clip.source_end = data['source_end']
        
        # Update properties
        if 'volume' in data:
            clip.volume = data['volume']
        if 'opacity' in data:
            clip.opacity = data['opacity']
        if 'speed' in data:
            clip.speed = data['speed']
        if 'effects' in data:
            clip.effects = data['effects']
        
        session.commit()
        session.close()
        
        return jsonify({
            'success': True,
            'message': 'Clip updated successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/video/timeline/delete-clip/<clip_id>', methods=['DELETE'])
def delete_timeline_clip(clip_id):
    """Remove a clip from the timeline"""
    try:
        from database import SessionLocal
        session = SessionLocal()
        
        clip = session.query(TimelineClip).filter_by(id=clip_id).first()
        if not clip:
            return jsonify({'success': False, 'error': 'Clip not found'}), 404
        
        session.delete(clip)
        session.commit()
        session.close()
        
        return jsonify({
            'success': True,
            'message': 'Clip removed from timeline'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/video/timeline/get-clips/<project_id>')
def get_timeline_clips(project_id):
    """Get all clips for a project's timeline"""
    try:
        from database import SessionLocal
        session = SessionLocal()
        
        clips = session.query(TimelineClip)\
            .filter_by(project_id=project_id)\
            .order_by(TimelineClip.start_time)\
            .all()
        
        result = {
            'success': True,
            'clips': [{
                'id': c.id,
                'asset_id': c.asset_id,
                'track_id': c.track_id,
                'start_time': c.start_time,
                'end_time': c.end_time,
                'source_start': c.source_start,
                'source_end': c.source_end,
                'volume': c.volume,
                'opacity': c.opacity,
                'speed': c.speed,
                'effects': c.effects,
                'scene_id': c.scene_id,
                'layer_order': c.layer_order,
                'is_locked': c.is_locked
            } for c in clips]
        }
        
        session.close()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/video/scene/evolve', methods=['POST'])
def evolve_scene():
    """Evolve a scene - generate variations, refinements, alternate moods"""
    try:
        data = request.get_json()
        scene_id = data.get('scene_id')
        asset_id = data.get('asset_id')
        evolution_type = data.get('type', 'variation')  # variation, mood, lighting, angle
        original_prompt = data.get('prompt')
        
        # Build evolved prompt based on type
        if evolution_type == 'variation':
            evolved_prompt = f"{original_prompt}, alternate composition"
        elif evolution_type == 'mood':
            mood = data.get('mood', 'dramatic')
            evolved_prompt = f"{original_prompt}, {mood} mood"
        elif evolution_type == 'lighting':
            lighting = data.get('lighting', 'golden hour')
            evolved_prompt = f"{original_prompt}, {lighting} lighting"
        elif evolution_type == 'angle':
            angle = data.get('angle', 'wide shot')
            evolved_prompt = f"{original_prompt}, {angle}"
        else:
            evolved_prompt = original_prompt
        
        # Generate evolved scene
        engine = data.get('engine', 'runway')
        duration = data.get('duration', 5.0)
        
        result = video_pipeline.generate_video(
            prompt=evolved_prompt,
            engine=engine,
            duration=duration
        )
        
        # Create new VideoAsset for evolution
        from database import SessionLocal
        session = SessionLocal()
        
        # Get original asset to link evolution
        original = session.query(VideoAsset).filter_by(id=asset_id).first()
        
        evolved_asset = VideoAsset(
            user_id=session.get('user_id', 'user_001'),
            name=f"Evolved: {evolved_prompt[:50]}",
            description=evolved_prompt,
            asset_type='video',
            file_url=result['video_url'],
            thumbnail_url=result.get('thumbnail_url'),
            duration=result.get('duration'),
            prompt=evolved_prompt,
            generation_engine=engine,
            status='complete',
            storage_provider=video_storage.provider,
            tags=f"{evolution_type},evolved" + (f",{original.tags}" if original and original.tags else "")
        )
        
        session.add(evolved_asset)
        session.commit()
        evolved_asset_id = evolved_asset.id
        session.close()
        
        return jsonify({
            'success': True,
            'asset_id': evolved_asset_id,
            'video_url': result['video_url'],
            'thumbnail_url': result.get('thumbnail_url'),
            'duration': result.get('duration'),
            'evolved_prompt': evolved_prompt,
            'evolution_type': evolution_type
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/video/scene/extend', methods=['POST'])
def extend_scene():
    """Extend a scene - generate the next moment, next shot, next beat"""
    try:
        data = request.get_json()
        asset_id = data.get('asset_id')
        original_prompt = data.get('prompt')
        extension_type = data.get('type', 'next_moment')  # next_moment, next_shot, next_beat
        
        # Build extension prompt
        if extension_type == 'next_moment':
            extended_prompt = f"Continuation of: {original_prompt}, showing what happens next"
        elif extension_type == 'next_shot':
            extended_prompt = f"Following shot after: {original_prompt}"
        elif extension_type == 'next_beat':
            extended_prompt = f"Next beat in the sequence: {original_prompt}"
        else:
            extended_prompt = f"Continuation: {original_prompt}"
        
        # Generate extension
        engine = data.get('engine', 'runway')
        duration = data.get('duration', 5.0)
        
        result = video_pipeline.generate_video(
            prompt=extended_prompt,
            engine=engine,
            duration=duration
        )
        
        # Create new VideoAsset for extension
        from database import SessionLocal
        session = SessionLocal()
        
        extended_asset = VideoAsset(
            user_id=session.get('user_id', 'user_001'),
            name=f"Extended: {extended_prompt[:50]}",
            description=extended_prompt,
            asset_type='video',
            file_url=result['video_url'],
            thumbnail_url=result.get('thumbnail_url'),
            duration=result.get('duration'),
            prompt=extended_prompt,
            generation_engine=engine,
            status='complete',
            storage_provider=video_storage.provider,
            tags=f"{extension_type},extended"
        )
        
        session.add(extended_asset)
        session.commit()
        extended_asset_id = extended_asset.id
        session.close()
        
        return jsonify({
            'success': True,
            'asset_id': extended_asset_id,
            'video_url': result['video_url'],
            'thumbnail_url': result.get('thumbnail_url'),
            'duration': result.get('duration'),
            'extended_prompt': extended_prompt,
            'extension_type': extension_type
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== UGI CREATIVE OPERATIONS ====================

@app.route('/api/video/regenerate', methods=['POST'])
def regenerate_scene():
    """Regenerate video with same prompt, new variation (using UGI)"""
    try:
        if video_ugi is None:
            initialize_ugi()
        
        data = request.get_json()
        asset_id = data.get('asset_id')
        
        if not asset_id:
            return jsonify({'success': False, 'error': 'Asset ID required'}), 400
        
        # Optional: Override seed for different variation
        new_settings = {}
        if data.get('seed') is not None:
            new_settings['seed'] = data['seed']
        
        result = video_ugi.regenerate(asset_id, **new_settings)
        
        return jsonify({
            'success': True,
            'asset_id': result['asset_id'],
            'video_url': result['video_url'],
            'thumbnail_url': result['thumbnail_url'],
            'duration': result['duration'],
            'engine': result['engine']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/video/ugi/evolve', methods=['POST'])
def ugi_evolve_scene():
    """Evolve scene using UGI (variation, mood, lighting, angle)"""
    try:
        if video_ugi is None:
            initialize_ugi()
        
        data = request.get_json()
        asset_id = data.get('asset_id')
        evolution_type = data.get('type')  # variation, mood, lighting, angle
        
        if not asset_id or not evolution_type:
            return jsonify({'success': False, 'error': 'Asset ID and type required'}), 400
        
        # Extract evolution parameters
        params = {}
        if evolution_type == 'mood':
            params['mood'] = data.get('mood', 'dramatic')
        elif evolution_type == 'lighting':
            params['lighting'] = data.get('lighting', 'golden hour')
        elif evolution_type == 'angle':
            params['angle'] = data.get('angle', 'aerial view')
        
        result = video_ugi.evolve(asset_id, evolution_type, **params)
        
        return jsonify({
            'success': True,
            'asset_id': result['asset_id'],
            'video_url': result['video_url'],
            'thumbnail_url': result['thumbnail_url'],
            'duration': result['duration'],
            'prompt': result['prompt'],
            'evolution_type': evolution_type
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/video/ugi/extend', methods=['POST'])
def ugi_extend_scene():
    """Extend scene using UGI (next_moment, next_shot, next_beat)"""
    try:
        if video_ugi is None:
            initialize_ugi()
        
        data = request.get_json()
        asset_id = data.get('asset_id')
        extension_type = data.get('type')  # next_moment, next_shot, next_beat
        
        if not asset_id or not extension_type:
            return jsonify({'success': False, 'error': 'Asset ID and type required'}), 400
        
        result = video_ugi.extend(asset_id, extension_type)
        
        return jsonify({
            'success': True,
            'asset_id': result['asset_id'],
            'video_url': result['video_url'],
            'thumbnail_url': result['thumbnail_url'],
            'duration': result['duration'],
            'prompt': result['prompt'],
            'extension_type': extension_type
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/video/engines', methods=['GET'])
def list_engines():
    """List available video generation engines with capabilities"""
    try:
        if video_ugi is None:
            initialize_ugi()
        
        engines = video_ugi.list_available_engines()
        capabilities = {
            engine: video_ugi.get_engine_capabilities(engine)
            for engine in engines
        }
        
        return jsonify({
            'success': True,
            'engines': engines,
            'capabilities': capabilities
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/video/markers/add', methods=['POST'])
def add_timeline_marker():
    """Add a marker to the timeline"""
    try:
        data = request.get_json()
        
        from database import SessionLocal
        session = SessionLocal()
        
        marker = TimelineMarker(
            project_id=data['project_id'],
            time=data['time'],
            marker_type=data.get('marker_type', 'note'),
            label=data.get('label'),
            description=data.get('description'),
            color=data.get('color', '#f5576c'),
            scene_id=data.get('scene_id'),
            suggestion_data=data.get('suggestion_data')
        )
        
        session.add(marker)
        session.commit()
        marker_id = marker.id
        session.close()
        
        return jsonify({
            'success': True,
            'marker_id': marker_id,
            'message': 'Marker added to timeline'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/video/markers/<project_id>')
def get_timeline_markers(project_id):
    """Get all markers for a project's timeline"""
    try:
        from database import SessionLocal
        session = SessionLocal()
        
        markers = session.query(TimelineMarker)\
            .filter_by(project_id=project_id)\
            .order_by(TimelineMarker.time)\
            .all()
        
        result = {
            'success': True,
            'markers': [{
                'id': m.id,
                'time': m.time,
                'marker_type': m.marker_type,
                'label': m.label,
                'description': m.description,
                'color': m.color,
                'scene_id': m.scene_id,
                'suggestion_data': m.suggestion_data
            } for m in markers]
        }
        
        session.close()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== END VIDEO STUDIO PHASE 2 ROUTES ====================

# ==================== VIDEO STUDIO PHASE 4: STORYBOARD ROUTES ====================

@app.route('/api/storyboard/create', methods=['POST'])
def create_storyboard():
    """Create a new storyboard for a project"""
    try:
        data = request.get_json()
        project_id = data.get('project_id')
        name = data.get('name', 'Untitled Storyboard')
        description = data.get('description', '')
        
        if not project_id:
            return jsonify({'success': False, 'error': 'Project ID required'}), 400
        
        storyboard = Storyboard(
            project_id=project_id,
            name=name,
            description=description
        )
        
        db.session.add(storyboard)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'storyboard_id': storyboard.id,
            'name': storyboard.name,
            'created_at': storyboard.created_at.isoformat()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/storyboard/<int:storyboard_id>', methods=['GET'])
def get_storyboard(storyboard_id):
    """Get storyboard with all scene cards"""
    try:
        storyboard = Storyboard.query.get(storyboard_id)
        if not storyboard:
            return jsonify({'success': False, 'error': 'Storyboard not found'}), 404
        
        # Get all scene cards
        scene_cards = SceneCard.query.filter_by(
            storyboard_id=storyboard_id
        ).order_by(SceneCard.order_index).all()
        
        return jsonify({
            'success': True,
            'storyboard': {
                'id': storyboard.id,
                'project_id': storyboard.project_id,
                'name': storyboard.name,
                'description': storyboard.description,
                'quality_score': storyboard.quality_score,
                'continuity_report': storyboard.continuity_report,
                'created_at': storyboard.created_at.isoformat(),
                'updated_at': storyboard.updated_at.isoformat()
            },
            'scene_cards': [{
                'id': card.id,
                'order_index': card.order_index,
                'prompt': card.prompt,
                'thumbnail_url': card.thumbnail_url,
                'duration': card.duration,
                'scene_type': card.scene_type,
                'mood': card.mood,
                'tags': card.tags,
                'characters': card.characters,
                'themes': card.themes,
                'status': card.status,
                'flow_suggestions': card.flow_suggestions,
                'asset_id': card.asset_id
            } for card in scene_cards]
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/storyboard/scene/add', methods=['POST'])
def add_scene_card():
    """Add a scene card to storyboard"""
    try:
        data = request.get_json()
        storyboard_id = data.get('storyboard_id')
        
        if not storyboard_id:
            return jsonify({'success': False, 'error': 'Storyboard ID required'}), 400
        
        # Get current max order_index
        max_order = db.session.query(db.func.max(SceneCard.order_index)).filter_by(
            storyboard_id=storyboard_id
        ).scalar() or -1
        
        scene_card = SceneCard(
            storyboard_id=storyboard_id,
            asset_id=data.get('asset_id'),
            order_index=max_order + 1,
            prompt=data.get('prompt', ''),
            thumbnail_url=data.get('thumbnail_url'),
            duration=data.get('duration', 5.0),
            scene_type=data.get('scene_type', 'medium'),
            mood=data.get('mood', 'calm'),
            tags=data.get('tags', ''),
            characters=data.get('characters'),
            themes=data.get('themes'),
            status='draft'
        )
        
        db.session.add(scene_card)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'scene_card_id': scene_card.id,
            'order_index': scene_card.order_index
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/storyboard/scene/<int:scene_id>/update', methods=['PUT'])
def update_scene_card(scene_id):
    """Update scene card metadata"""
    try:
        scene_card = SceneCard.query.get(scene_id)
        if not scene_card:
            return jsonify({'success': False, 'error': 'Scene card not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'prompt' in data:
            scene_card.prompt = data['prompt']
        if 'scene_type' in data:
            scene_card.scene_type = data['scene_type']
        if 'mood' in data:
            scene_card.mood = data['mood']
        if 'tags' in data:
            scene_card.tags = data['tags']
        if 'duration' in data:
            scene_card.duration = data['duration']
        if 'characters' in data:
            scene_card.characters = data['characters']
        if 'themes' in data:
            scene_card.themes = data['themes']
        if 'status' in data:
            scene_card.status = data['status']
        
        db.session.commit()
        
        return jsonify({'success': True, 'scene_card_id': scene_card.id})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/storyboard/scene/<int:scene_id>/delete', methods=['DELETE'])
def delete_scene_card(scene_id):
    """Delete scene card from storyboard"""
    try:
        scene_card = SceneCard.query.get(scene_id)
        if not scene_card:
            return jsonify({'success': False, 'error': 'Scene card not found'}), 404
        
        db.session.delete(scene_card)
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/storyboard/scene/<int:scene_id>/duplicate', methods=['POST'])
def duplicate_scene_card(scene_id):
    """Duplicate a scene card"""
    try:
        original = SceneCard.query.get(scene_id)
        if not original:
            return jsonify({'success': False, 'error': 'Scene card not found'}), 404
        
        # Get max order_index
        max_order = db.session.query(db.func.max(SceneCard.order_index)).filter_by(
            storyboard_id=original.storyboard_id
        ).scalar() or -1
        
        # Create duplicate
        duplicate = SceneCard(
            storyboard_id=original.storyboard_id,
            asset_id=original.asset_id,
            order_index=max_order + 1,
            prompt=original.prompt,
            thumbnail_url=original.thumbnail_url,
            duration=original.duration,
            scene_type=original.scene_type,
            mood=original.mood,
            tags=original.tags,
            characters=original.characters,
            themes=original.themes,
            status='draft'
        )
        
        db.session.add(duplicate)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'scene_card_id': duplicate.id,
            'order_index': duplicate.order_index
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/storyboard/scene/reorder', methods=['POST'])
def reorder_scene_cards():
    """Reorder scene cards in storyboard"""
    try:
        data = request.get_json()
        scene_ids = data.get('scene_ids', [])  # Ordered list of scene IDs
        
        if not scene_ids:
            return jsonify({'success': False, 'error': 'Scene IDs required'}), 400
        
        # Update order_index for each scene
        for index, scene_id in enumerate(scene_ids):
            scene_card = SceneCard.query.get(scene_id)
            if scene_card:
                scene_card.order_index = index
        
        db.session.commit()
        
        return jsonify({'success': True, 'reordered_count': len(scene_ids)})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/storyboard/<int:storyboard_id>/analyze', methods=['POST'])
def analyze_storyboard():
    """Analyze storyboard with Scene Flow Engine"""
    try:
        from scene_flow_engine import SceneFlowEngine
        
        storyboard = Storyboard.query.get(storyboard_id)
        if not storyboard:
            return jsonify({'success': False, 'error': 'Storyboard not found'}), 404
        
        # Get all scene cards
        scene_cards = SceneCard.query.filter_by(
            storyboard_id=storyboard_id
        ).order_by(SceneCard.order_index).all()
        
        if len(scene_cards) < 2:
            return jsonify({
                'success': True,
                'message': 'Need at least 2 scenes to analyze',
                'quality_score': 100,
                'issues': [],
                'suggestions': []
            })
        
        # Convert to analysis format
        scenes = [{
            'scene_type': card.scene_type,
            'mood': card.mood,
            'duration': card.duration,
            'tags': card.tags,
            'prompt': card.prompt
        } for card in scene_cards]
        
        # Run analysis
        flow_engine = SceneFlowEngine()
        analysis = flow_engine.analyze_sequence(scenes)
        
        # Update storyboard with results
        storyboard.quality_score = analysis['quality_score']
        storyboard.continuity_report = analysis['continuity_report']
        db.session.commit()
        
        # Store suggestions on scene cards
        for suggestion in analysis['suggestions']:
            if 'position' in suggestion:
                scene_index = suggestion['position']
                if 0 <= scene_index < len(scene_cards):
                    card = scene_cards[scene_index]
                    current_suggestions = card.flow_suggestions or []
                    current_suggestions.append(suggestion)
                    card.flow_suggestions = current_suggestions
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'quality_score': analysis['quality_score'],
            'issues': analysis['issues'],
            'suggestions': analysis['suggestions'],
            'continuity_report': analysis['continuity_report']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/storyboard/<int:storyboard_id>/suggest-next', methods=['POST'])
def suggest_next_scene():
    """Get AI suggestion for next scene in storyboard"""
    try:
        from scene_flow_engine import SceneFlowEngine
        
        storyboard = Storyboard.query.get(storyboard_id)
        if not storyboard:
            return jsonify({'success': False, 'error': 'Storyboard not found'}), 404
        
        # Get recent scenes
        recent_scenes = SceneCard.query.filter_by(
            storyboard_id=storyboard_id
        ).order_by(SceneCard.order_index.desc()).limit(5).all()
        
        recent_scenes.reverse()  # Oldest to newest
        
        # Convert to analysis format
        scenes = [{
            'scene_type': card.scene_type,
            'mood': card.mood,
            'duration': card.duration,
            'tags': card.tags,
            'prompt': card.prompt
        } for card in recent_scenes]
        
        # Get suggestion
        flow_engine = SceneFlowEngine()
        suggestion = flow_engine.suggest_next_scene(scenes)
        
        return jsonify({
            'success': True,
            'suggestion': suggestion
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== END PHASE 4 STORYBOARD ROUTES ====================


# ============================================================================================
# PHASE 5: VIDEO LIBRARY + TEAM SHARING ROUTES (The Vault of Motion)
# ============================================================================================

# ======================
# A. COLLECTIONS API
# ======================

@app.route('/api/library/collections/create', methods=['POST'])
def create_collection():
    """Create a new video collection."""
    try:
        data = request.get_json()
        team_id = data.get('team_id')
        creator_id = data.get('creator_id')
        name = data.get('name', 'Untitled Collection')
        description = data.get('description', '')
        collection_type = data.get('collection_type', 'general')  # campaign, series, character_arc, brand_kit, universe
        tags = data.get('tags', '')
        category = data.get('category', '')
        share_level = data.get('share_level', 'team')  # private, team, public
        
        # Create collection
        collection = VideoCollection(
            team_id=team_id,
            creator_id=creator_id,
            name=name,
            description=description,
            collection_type=collection_type,
            tags=tags,
            category=category,
            share_level=share_level,
            is_public=(share_level == 'public')
        )
        db.session.add(collection)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'collection_id': collection.id,
            'name': collection.name,
            'type': collection.collection_type,
            'created_at': collection.created_at.isoformat()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/library/collections/<int:collection_id>', methods=['GET'])
def get_collection(collection_id):
    """Get collection with all videos."""
    try:
        collection = VideoCollection.query.get_or_404(collection_id)
        
        # Get all videos in this collection
        items = CollectionItem.query.filter_by(collection_id=collection_id).order_by(CollectionItem.order_index).all()
        
        videos = []
        for item in items:
            asset = VideoAsset.query.get(item.asset_id)
            if asset:
                # Get library metadata if exists
                lib_meta = VideoLibraryMetadata.query.filter_by(asset_id=asset.id).first()
                
                videos.append({
                    'asset_id': asset.id,
                    'name': asset.name,
                    'thumbnail_url': asset.thumbnail_url,
                    'duration': asset.duration,
                    'tags': asset.tags,
                    'category': asset.category,
                    'mood': lib_meta.mood if lib_meta else None,
                    'scene_type': lib_meta.scene_type if lib_meta else None,
                    'order_index': item.order_index,
                    'notes': item.notes,
                    'added_at': item.added_at.isoformat() if item.added_at else None
                })
        
        return jsonify({
            'success': True,
            'collection': {
                'id': collection.id,
                'name': collection.name,
                'description': collection.description,
                'type': collection.collection_type,
                'tags': collection.tags,
                'category': collection.category,
                'share_level': collection.share_level,
                'video_count': collection.video_count,
                'total_duration': collection.total_duration,
                'cover_image_url': collection.cover_image_url,
                'created_at': collection.created_at.isoformat()
            },
            'videos': videos
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/library/collections/<int:collection_id>/add-video', methods=['POST'])
def add_video_to_collection(collection_id):
    """Add a video to a collection."""
    try:
        data = request.get_json()
        asset_id = data.get('asset_id')
        order_index = data.get('order_index')
        notes = data.get('notes', '')
        added_by = data.get('added_by')
        
        collection = VideoCollection.query.get_or_404(collection_id)
        asset = VideoAsset.query.get_or_404(asset_id)
        
        # Check if already in collection
        existing = CollectionItem.query.filter_by(collection_id=collection_id, asset_id=asset_id).first()
        if existing:
            return jsonify({'success': False, 'error': 'Video already in collection'}), 400
        
        # Calculate order_index if not provided
        if order_index is None:
            max_order = db.session.query(db.func.max(CollectionItem.order_index)).filter_by(collection_id=collection_id).scalar() or 0
            order_index = max_order + 1
        
        # Create collection item
        item = CollectionItem(
            collection_id=collection_id,
            asset_id=asset_id,
            order_index=order_index,
            notes=notes,
            added_by=added_by
        )
        db.session.add(item)
        
        # Update collection stats
        collection.video_count = (collection.video_count or 0) + 1
        collection.total_duration = (collection.total_duration or 0.0) + (asset.duration or 0.0)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'item_id': item.id,
            'order_index': item.order_index
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/library/collections/<int:collection_id>/remove-video', methods=['POST'])
def remove_video_from_collection(collection_id):
    """Remove a video from a collection."""
    try:
        data = request.get_json()
        asset_id = data.get('asset_id')
        
        collection = VideoCollection.query.get_or_404(collection_id)
        item = CollectionItem.query.filter_by(collection_id=collection_id, asset_id=asset_id).first_or_404()
        
        asset = VideoAsset.query.get(asset_id)
        
        # Update collection stats
        collection.video_count = max(0, (collection.video_count or 1) - 1)
        collection.total_duration = max(0.0, (collection.total_duration or 0.0) - (asset.duration or 0.0))
        
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/library/collections/<int:collection_id>/reorder', methods=['POST'])
def reorder_collection_videos(collection_id):
    """Reorder videos in a collection."""
    try:
        data = request.get_json()
        asset_ids = data.get('asset_ids', [])  # Ordered list of asset IDs
        
        # Update order_index for each asset
        for index, asset_id in enumerate(asset_ids):
            item = CollectionItem.query.filter_by(collection_id=collection_id, asset_id=asset_id).first()
            if item:
                item.order_index = index
        
        db.session.commit()
        
        return jsonify({'success': True, 'reordered_count': len(asset_ids)})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/library/collections/team/<int:team_id>', methods=['GET'])
def get_team_collections(team_id):
    """Get all collections for a team."""
    try:
        collections = VideoCollection.query.filter_by(team_id=team_id).order_by(VideoCollection.created_at.desc()).all()
        
        result = []
        for coll in collections:
            result.append({
                'id': coll.id,
                'name': coll.name,
                'description': coll.description,
                'type': coll.collection_type,
                'tags': coll.tags,
                'category': coll.category,
                'video_count': coll.video_count,
                'total_duration': coll.total_duration,
                'cover_image_url': coll.cover_image_url,
                'share_level': coll.share_level,
                'created_at': coll.created_at.isoformat()
            })
        
        return jsonify({'success': True, 'collections': result})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ======================
# B. LIBRARY SEARCH & FILTER API
# ======================

@app.route('/api/library/search', methods=['POST'])
def search_library():
    """Advanced library search with multiple filters.
    
    Filters:
    - tags: List of tags (OR logic)
    - categories: List of categories (OR logic)
    - moods: List of moods (OR logic)
    - engines: List of generation engines (OR logic)
    - creators: List of user IDs (OR logic)
    - date_from, date_to: Date range
    - duration_min, duration_max: Duration range
    - has_lineage: Boolean - only videos with lineage
    - search_text: Text search in name/description/prompt
    """
    try:
        data = request.get_json()
        team_id = data.get('team_id')
        
        # Start with base query
        query = VideoAsset.query.filter_by(team_id=team_id)
        
        # Join with library metadata
        query = query.outerjoin(VideoLibraryMetadata, VideoAsset.id == VideoLibraryMetadata.asset_id)
        
        # Filter by tags (OR logic)
        if data.get('tags'):
            tags = data.get('tags')
            tag_filters = [VideoAsset.tags.contains(tag) for tag in tags]
            query = query.filter(db.or_(*tag_filters))
        
        # Filter by categories
        if data.get('categories'):
            query = query.filter(VideoAsset.category.in_(data.get('categories')))
        
        # Filter by moods
        if data.get('moods'):
            query = query.filter(VideoLibraryMetadata.mood.in_(data.get('moods')))
        
        # Filter by generation engines
        if data.get('engines'):
            query = query.filter(VideoAsset.generation_engine.in_(data.get('engines')))
        
        # Filter by creators
        if data.get('creators'):
            query = query.filter(VideoAsset.user_id.in_(data.get('creators')))
        
        # Date range
        if data.get('date_from'):
            query = query.filter(VideoAsset.timestamp >= data.get('date_from'))
        if data.get('date_to'):
            query = query.filter(VideoAsset.timestamp <= data.get('date_to'))
        
        # Duration range
        if data.get('duration_min'):
            query = query.filter(VideoAsset.duration >= data.get('duration_min'))
        if data.get('duration_max'):
            query = query.filter(VideoAsset.duration <= data.get('duration_max'))
        
        # Lineage filter
        if data.get('has_lineage'):
            query = query.filter(VideoLibraryMetadata.parent_asset_id.isnot(None))
        
        # Text search
        if data.get('search_text'):
            search = f"%{data.get('search_text')}%"
            query = query.filter(
                db.or_(
                    VideoAsset.name.ilike(search),
                    VideoAsset.description.ilike(search),
                    VideoAsset.prompt.ilike(search)
                )
            )
        
        # Sort
        sort_by = data.get('sort_by', 'created')  # created, name, duration, views
        sort_order = data.get('sort_order', 'desc')  # asc, desc
        
        if sort_by == 'created':
            query = query.order_by(VideoAsset.timestamp.desc() if sort_order == 'desc' else VideoAsset.timestamp.asc())
        elif sort_by == 'name':
            query = query.order_by(VideoAsset.name.asc() if sort_order == 'asc' else VideoAsset.name.desc())
        elif sort_by == 'duration':
            query = query.order_by(VideoAsset.duration.desc() if sort_order == 'desc' else VideoAsset.duration.asc())
        elif sort_by == 'views':
            query = query.order_by(VideoLibraryMetadata.view_count.desc())
        
        # Pagination
        page = data.get('page', 1)
        per_page = data.get('per_page', 24)
        
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Format results
        results = []
        for asset in paginated.items:
            lib_meta = VideoLibraryMetadata.query.filter_by(asset_id=asset.id).first()
            
            results.append({
                'id': asset.id,
                'name': asset.name,
                'description': asset.description,
                'thumbnail_url': asset.thumbnail_url,
                'file_url': asset.file_url,
                'duration': asset.duration,
                'tags': asset.tags,
                'category': asset.category,
                'prompt': asset.prompt,
                'generation_engine': asset.generation_engine,
                'creator_id': asset.user_id,
                'created_at': asset.timestamp.isoformat() if asset.timestamp else None,
                'mood': lib_meta.mood if lib_meta else None,
                'scene_type': lib_meta.scene_type if lib_meta else None,
                'view_count': lib_meta.view_count if lib_meta else 0,
                'duplicate_count': lib_meta.duplicate_count if lib_meta else 0,
                'has_lineage': lib_meta and lib_meta.parent_asset_id is not None
            })
        
        return jsonify({
            'success': True,
            'results': results,
            'total': paginated.total,
            'page': page,
            'per_page': per_page,
            'total_pages': paginated.pages
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/library/filters', methods=['GET'])
def get_library_filters():
    """Get available filter options (tags, categories, moods, engines)."""
    try:
        team_id = request.args.get('team_id')
        
        # Get distinct values
        assets = VideoAsset.query.filter_by(team_id=team_id).all()
        lib_metas = VideoLibraryMetadata.query.join(VideoAsset).filter(VideoAsset.team_id == team_id).all()
        
        # Collect unique values
        all_tags = set()
        categories = set()
        engines = set()
        moods = set()
        scene_types = set()
        
        for asset in assets:
            if asset.tags:
                all_tags.update([t.strip() for t in asset.tags.split(',') if t.strip()])
            if asset.category:
                categories.add(asset.category)
            if asset.generation_engine:
                engines.add(asset.generation_engine)
        
        for meta in lib_metas:
            if meta.mood:
                moods.add(meta.mood)
            if meta.scene_type:
                scene_types.add(meta.scene_type)
        
        return jsonify({
            'success': True,
            'filters': {
                'tags': sorted(list(all_tags)),
                'categories': sorted(list(categories)),
                'moods': sorted(list(moods)),
                'scene_types': sorted(list(scene_types)),
                'engines': sorted(list(engines))
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ======================
# C. SHARING & PERMISSIONS API
# ======================

@app.route('/api/library/share', methods=['POST'])
def share_video():
    """Share a video with another user."""
    try:
        data = request.get_json()
        asset_id = data.get('asset_id')
        shared_by = data.get('shared_by')
        shared_with = data.get('shared_with')  # User ID
        permission = data.get('permission', 'view')  # view, edit, admin
        message = data.get('message', '')
        expires_at = data.get('expires_at')  # Optional ISO datetime
        
        # Check if already shared
        existing = VideoShare.query.filter_by(asset_id=asset_id, shared_by=shared_by, shared_with=shared_with).first()
        if existing:
            # Update existing share
            existing.permission = permission
            existing.message = message
            existing.expires_at = expires_at
        else:
            # Create new share
            share = VideoShare(
                asset_id=asset_id,
                shared_by=shared_by,
                shared_with=shared_with,
                permission=permission,
                message=message,
                expires_at=expires_at
            )
            db.session.add(share)
        
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/library/shares/<int:asset_id>', methods=['GET'])
def get_video_shares(asset_id):
    """Get all users a video is shared with."""
    try:
        shares = VideoShare.query.filter_by(asset_id=asset_id).all()
        
        result = []
        for share in shares:
            user = User.query.get(share.shared_with)
            result.append({
                'share_id': share.id,
                'shared_with_id': share.shared_with,
                'shared_with_name': user.username if user else 'Unknown',
                'permission': share.permission,
                'message': share.message,
                'shared_at': share.shared_at.isoformat(),
                'expires_at': share.expires_at.isoformat() if share.expires_at else None
            })
        
        return jsonify({'success': True, 'shares': result})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/library/update-share-level', methods=['POST'])
def update_share_level():
    """Update video's share level (private, team, public)."""
    try:
        data = request.get_json()
        asset_id = data.get('asset_id')
        share_level = data.get('share_level')  # private, team, public
        
        # Update or create library metadata
        lib_meta = VideoLibraryMetadata.query.filter_by(asset_id=asset_id).first()
        if not lib_meta:
            lib_meta = VideoLibraryMetadata(asset_id=asset_id)
            db.session.add(lib_meta)
        
        lib_meta.share_level = share_level
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ======================
# D. LINEAGE TRACKING API
# ======================

@app.route('/api/library/duplicate', methods=['POST'])
def duplicate_video():
    """Duplicate a video (create exact copy with new lineage)."""
    try:
        data = request.get_json()
        asset_id = data.get('asset_id')
        user_id = data.get('user_id')
        branch_name = data.get('branch_name', 'duplicate')
        
        original = VideoAsset.query.get_or_404(asset_id)
        original_meta = VideoLibraryMetadata.query.filter_by(asset_id=asset_id).first()
        
        # Create duplicate asset
        duplicate = VideoAsset(
            user_id=user_id,
            team_id=original.team_id,
            project_id=original.project_id,
            name=f"{original.name} (Copy)",
            description=original.description,
            asset_type=original.asset_type,
            file_url=original.file_url,
            thumbnail_url=original.thumbnail_url,
            file_size=original.file_size,
            mime_type=original.mime_type,
            duration=original.duration,
            width=original.width,
            height=original.height,
            fps=original.fps,
            prompt=original.prompt,
            generation_engine=original.generation_engine,
            generation_params=original.generation_params,
            tags=original.tags,
            category=original.category,
            status='ready'
        )
        db.session.add(duplicate)
        db.session.flush()  # Get duplicate.id
        
        # Create library metadata
        new_meta = VideoLibraryMetadata(
            asset_id=duplicate.id,
            lineage_root_id=original_meta.lineage_root_id or asset_id if original_meta else asset_id,
            parent_asset_id=asset_id,
            lineage_version=(original_meta.lineage_version + 1) if original_meta else 2,
            lineage_branch=branch_name,
            evolution_type='duplicate',
            evolution_note='Exact duplicate for remixing',
            mood=original_meta.mood if original_meta else None,
            scene_type=original_meta.scene_type if original_meta else None,
            share_level='private',
            can_duplicate=True,
            can_remix=True
        )
        db.session.add(new_meta)
        
        # Track lineage
        lineage = VideoLineage(
            parent_id=asset_id,
            child_id=duplicate.id,
            evolution_type='duplicate',
            original_prompt=original.prompt,
            evolved_prompt=original.prompt,
            prompt_delta='No changes',
            created_by=user_id,
            branch_name=branch_name
        )
        db.session.add(lineage)
        
        # Update stats on original
        if original_meta:
            original_meta.duplicate_count = (original_meta.duplicate_count or 0) + 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'duplicate_id': duplicate.id,
            'lineage_version': new_meta.lineage_version
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/library/remix', methods=['POST'])
def remix_video():
    """Remix a video (duplicate + modify prompt)."""
    try:
        data = request.get_json()
        asset_id = data.get('asset_id')
        user_id = data.get('user_id')
        new_prompt = data.get('new_prompt')
        evolution_note = data.get('evolution_note', 'Remixed version')
        branch_name = data.get('branch_name', 'remix')
        
        original = VideoAsset.query.get_or_404(asset_id)
        original_meta = VideoLibraryMetadata.query.filter_by(asset_id=asset_id).first()
        
        # Create remixed asset (placeholder - would need to regenerate)
        remix = VideoAsset(
            user_id=user_id,
            team_id=original.team_id,
            project_id=original.project_id,
            name=f"{original.name} (Remix)",
            description=f"Remixed from: {original.name}",
            asset_type=original.asset_type,
            file_url=original.file_url,  # Placeholder - should regenerate
            thumbnail_url=original.thumbnail_url,
            duration=original.duration,
            width=original.width,
            height=original.height,
            fps=original.fps,
            prompt=new_prompt,
            generation_engine=original.generation_engine,
            tags=original.tags,
            category=original.category,
            status='draft'  # Needs regeneration
        )
        db.session.add(remix)
        db.session.flush()
        
        # Create library metadata
        new_meta = VideoLibraryMetadata(
            asset_id=remix.id,
            lineage_root_id=original_meta.lineage_root_id or asset_id if original_meta else asset_id,
            parent_asset_id=asset_id,
            lineage_version=(original_meta.lineage_version + 1) if original_meta else 2,
            lineage_branch=branch_name,
            evolution_type='remix',
            evolution_note=evolution_note,
            mood=original_meta.mood if original_meta else None,
            scene_type=original_meta.scene_type if original_meta else None,
            share_level='private'
        )
        db.session.add(new_meta)
        
        # Track lineage
        lineage = VideoLineage(
            parent_id=asset_id,
            child_id=remix.id,
            evolution_type='remix',
            original_prompt=original.prompt,
            evolved_prompt=new_prompt,
            prompt_delta=f"Original: {original.prompt}\nNew: {new_prompt}",
            created_by=user_id,
            branch_name=branch_name
        )
        db.session.add(lineage)
        
        # Update stats
        if original_meta:
            original_meta.remix_count = (original_meta.remix_count or 0) + 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'remix_id': remix.id,
            'message': 'Remix created - regenerate video with new prompt',
            'lineage_version': new_meta.lineage_version
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/library/lineage/<int:asset_id>', methods=['GET'])
def get_video_lineage(asset_id):
    """Get full lineage tree for a video (ancestors and descendants)."""
    try:
        # Get ancestors (parent → grandparent → ...)
        ancestors = []
        current_id = asset_id
        
        while current_id:
            lineage = VideoLineage.query.filter_by(child_id=current_id).first()
            if not lineage:
                break
            
            parent = VideoAsset.query.get(lineage.parent_id)
            if parent:
                ancestors.append({
                    'asset_id': parent.id,
                    'name': parent.name,
                    'thumbnail_url': parent.thumbnail_url,
                    'evolution_type': lineage.evolution_type,
                    'branch_name': lineage.branch_name,
                    'created_at': lineage.created_at.isoformat()
                })
            
            current_id = lineage.parent_id
        
        # Get descendants (children, grandchildren, ...)
        def get_descendants(parent_id):
            children = []
            lineages = VideoLineage.query.filter_by(parent_id=parent_id).all()
            
            for lin in lineages:
                child = VideoAsset.query.get(lin.child_id)
                if child:
                    child_data = {
                        'asset_id': child.id,
                        'name': child.name,
                        'thumbnail_url': child.thumbnail_url,
                        'evolution_type': lin.evolution_type,
                        'branch_name': lin.branch_name,
                        'created_at': lin.created_at.isoformat(),
                        'children': get_descendants(child.id)
                    }
                    children.append(child_data)
            
            return children
        
        descendants = get_descendants(asset_id)
        
        # Get current video info
        current = VideoAsset.query.get_or_404(asset_id)
        current_meta = VideoLibraryMetadata.query.filter_by(asset_id=asset_id).first()
        
        return jsonify({
            'success': True,
            'current': {
                'asset_id': current.id,
                'name': current.name,
                'thumbnail_url': current.thumbnail_url,
                'lineage_version': current_meta.lineage_version if current_meta else 1,
                'lineage_branch': current_meta.lineage_branch if current_meta else 'main'
            },
            'ancestors': list(reversed(ancestors)),  # Root → current
            'descendants': descendants
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ======================
# E. CONSTELLATION INTEGRATION
# ======================

@app.route('/api/library/constellation/update-position', methods=['POST'])
def update_constellation_position():
    """Update video's position in constellation map."""
    try:
        data = request.get_json()
        asset_id = data.get('asset_id')
        x = data.get('x')
        y = data.get('y')
        cluster = data.get('cluster')
        
        lib_meta = VideoLibraryMetadata.query.filter_by(asset_id=asset_id).first()
        if not lib_meta:
            lib_meta = VideoLibraryMetadata(asset_id=asset_id)
            db.session.add(lib_meta)
        
        lib_meta.constellation_x = x
        lib_meta.constellation_y = y
        lib_meta.constellation_cluster = cluster
        
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/library/constellation/map', methods=['GET'])
def get_constellation_map():
    """Get all videos for constellation visualization."""
    try:
        team_id = request.args.get('team_id')
        
        # Get all videos with constellation data
        assets = VideoAsset.query.filter_by(team_id=team_id).all()
        
        nodes = []
        for asset in assets:
            lib_meta = VideoLibraryMetadata.query.filter_by(asset_id=asset.id).first()
            
            nodes.append({
                'id': asset.id,
                'name': asset.name,
                'thumbnail_url': asset.thumbnail_url,
                'tags': asset.tags.split(',') if asset.tags else [],
                'category': asset.category,
                'mood': lib_meta.mood if lib_meta else None,
                'scene_type': lib_meta.scene_type if lib_meta else None,
                'x': lib_meta.constellation_x if lib_meta else None,
                'y': lib_meta.constellation_y if lib_meta else None,
                'cluster': lib_meta.constellation_cluster if lib_meta else None,
                'has_lineage': lib_meta and lib_meta.parent_asset_id is not None
            })
        
        # Get lineage connections
        lineages = VideoLineage.query.join(VideoAsset, VideoLineage.parent_id == VideoAsset.id).filter(VideoAsset.team_id == team_id).all()
        
        edges = []
        for lin in lineages:
            edges.append({
                'source': lin.parent_id,
                'target': lin.child_id,
                'type': lin.evolution_type
            })
        
        return jsonify({
            'success': True,
            'nodes': nodes,
            'edges': edges
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== END PHASE 5 LIBRARY ROUTES ====================


# ============================================================================================
# PHASE 6: AUDIO STUDIO API ROUTES ("THE TEMPLE OF SOUND")
# ============================================================================================

# Initialize Universal Audio Interface
from universal_audio_interface import UniversalAudioInterface

audio_storage_config = {
    'provider': 's3',  # or 'gcs', 'azure', 'local'
    'bucket': 'codex-audio-assets',
    'region': 'us-east-1'
}

audio_ugi = UniversalAudioInterface(db, audio_storage_config)


# ========== AUDIO PROJECTS ==========

@app.route('/api/audio/projects/create', methods=['POST'])
def audio_projects_create():
    """Create new audio project.
    
    Body:
        name: Project name
        description: Optional description
        project_type: music, podcast, voiceover, sound_design, ambient
        sample_rate: 44100 (default)
        channels: 2 (stereo, default)
        team_id: Optional team ID
    """
    try:
        data = request.json
        user_id = data.get('user_id', 1)  # TODO: Get from auth
        
        project = AudioProject(
            user_id=user_id,
            team_id=data.get('team_id'),
            name=data['name'],
            description=data.get('description'),
            project_type=data.get('project_type', 'music'),
            sample_rate=data.get('sample_rate', 44100),
            bit_depth=data.get('bit_depth', 16),
            channels=data.get('channels', 2),
            status='draft'
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'project_id': project.id,
            'name': project.name,
            'project_type': project.project_type,
            'created_at': project.timestamp.isoformat()
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/projects/<int:project_id>', methods=['GET'])
def audio_projects_get(project_id):
    """Get audio project details with all tracks and assets."""
    try:
        project = AudioProject.query.get(project_id)
        if not project:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        # Get all tracks
        tracks = AudioTrack.query.filter_by(project_id=project_id).order_by(AudioTrack.layer_order).all()
        
        # Get all assets used in this project
        asset_ids = [t.asset_id for t in tracks if t.asset_id]
        assets = AudioAsset.query.filter(AudioAsset.id.in_(asset_ids)).all() if asset_ids else []
        
        # Get markers
        markers = AudioMarker.query.filter_by(project_id=project_id).order_by(AudioMarker.time).all()
        
        return jsonify({
            'success': True,
            'project': {
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'project_type': project.project_type,
                'duration': project.duration,
                'sample_rate': project.sample_rate,
                'channels': project.channels,
                'status': project.status,
                'created_at': project.timestamp.isoformat()
            },
            'tracks': [{
                'id': t.id,
                'track_id': t.track_id,
                'asset_id': t.asset_id,
                'start_time': t.start_time,
                'end_time': t.end_time,
                'volume': t.volume,
                'is_muted': t.is_muted,
                'is_solo': t.is_solo
            } for t in tracks],
            'assets': [{
                'id': a.id,
                'name': a.name,
                'asset_type': a.asset_type,
                'file_url': a.file_url,
                'duration': a.duration
            } for a in assets],
            'markers': [{
                'id': m.id,
                'time': m.time,
                'marker_type': m.marker_type,
                'label': m.label
            } for m in markers]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/audio/projects/<int:project_id>/update', methods=['POST'])
def audio_projects_update(project_id):
    """Update audio project metadata."""
    try:
        project = AudioProject.query.get(project_id)
        if not project:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        data = request.json
        
        if 'name' in data:
            project.name = data['name']
        if 'description' in data:
            project.description = data['description']
        if 'status' in data:
            project.status = data['status']
        if 'duration' in data:
            project.duration = data['duration']
        if 'tags' in data:
            project.tags = data['tags']
        if 'mood' in data:
            project.mood = data['mood']
        if 'genre' in data:
            project.genre = data['genre']
        
        project.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True, 'project_id': project.id})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/projects/<int:project_id>/delete', methods=['POST'])
def audio_projects_delete(project_id):
    """Delete audio project (soft delete)."""
    try:
        project = AudioProject.query.get(project_id)
        if not project:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        project.status = 'deleted'
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Project deleted'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/projects/list', methods=['GET'])
def audio_projects_list():
    """List audio projects for user/team."""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        team_id = request.args.get('team_id', type=int)
        project_type = request.args.get('project_type')
        status = request.args.get('status', 'active')
        
        query = AudioProject.query.filter_by(user_id=user_id)
        
        if team_id:
            query = query.filter_by(team_id=team_id)
        if project_type:
            query = query.filter_by(project_type=project_type)
        if status and status != 'all':
            query = query.filter_by(status=status)
        
        projects = query.order_by(AudioProject.timestamp.desc()).all()
        
        return jsonify({
            'success': True,
            'projects': [{
                'id': p.id,
                'name': p.name,
                'project_type': p.project_type,
                'duration': p.duration,
                'status': p.status,
                'created_at': p.timestamp.isoformat()
            } for p in projects],
            'count': len(projects)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ========== AUDIO GENERATION ==========

@app.route('/api/audio/generate', methods=['POST'])
def audio_generate():
    """Generate audio using Universal Audio Interface.
    
    Body:
        prompt: Text prompt
        engine: elevenlabs, suno, stability_audio, audiocraft
        project_id: Audio project ID
        asset_type: music, voiceover, sfx, ambient
        
        Engine-specific settings:
        - ElevenLabs: voice_id, stability, similarity_boost, style
        - Suno: genre, mood, bpm, key, instrumental
        - Stability Audio: audio_type (sfx/ambient), negative_prompt
        - AudioCraft: model, temperature, top_k, top_p
    """
    try:
        data = request.json
        user_id = data.get('user_id', 1)
        
        result = audio_ugi.generate(
            prompt=data['prompt'],
            engine=data['engine'],
            project_id=data['project_id'],
            user_id=user_id,
            asset_type=data.get('asset_type', 'music'),
            **{k: v for k, v in data.items() if k not in ['prompt', 'engine', 'project_id', 'user_id', 'asset_type']}
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/regenerate', methods=['POST'])
def audio_regenerate():
    """Regenerate audio with same prompt but different settings."""
    try:
        data = request.json
        asset_id = data['asset_id']
        new_settings = {k: v for k, v in data.items() if k != 'asset_id'}
        
        result = audio_ugi.regenerate(asset_id, **new_settings)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/evolve', methods=['POST'])
def audio_evolve():
    """Evolve audio (change mood, genre, tempo, style).
    
    Body:
        asset_id: Original audio asset ID
        evolution_type: mood, genre, tempo, style, voice
        mood/genre/bpm/style/voice_id: New value
    """
    try:
        data = request.json
        
        result = audio_ugi.evolve(
            asset_id=data['asset_id'],
            evolution_type=data['evolution_type'],
            **{k: v for k, v in data.items() if k not in ['asset_id', 'evolution_type']}
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/extend', methods=['POST'])
def audio_extend():
    """Extend audio (continue, loop, variation).
    
    Body:
        asset_id: Original audio asset ID
        extension_type: continue, loop, variation
    """
    try:
        data = request.json
        
        result = audio_ugi.extend(
            asset_id=data['asset_id'],
            extension_type=data.get('extension_type', 'continue')
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ========== AUDIO ASSETS ==========

@app.route('/api/audio/assets/<int:asset_id>', methods=['GET'])
def audio_assets_get(asset_id):
    """Get audio asset details with metadata and lineage."""
    try:
        asset = AudioAsset.query.get(asset_id)
        if not asset:
            return jsonify({'success': False, 'error': 'Asset not found'}), 404
        
        # Get lineage metadata if exists
        metadata = AudioLibraryMetadata.query.filter_by(asset_id=asset_id).first()
        
        # Get parent/children
        parent_lineage = AudioLineage.query.filter_by(child_id=asset_id).first()
        children_lineage = AudioLineage.query.filter_by(parent_id=asset_id).all()
        
        return jsonify({
            'success': True,
            'asset': {
                'id': asset.id,
                'name': asset.name,
                'description': asset.description,
                'asset_type': asset.asset_type,
                'file_url': asset.file_url,
                'waveform_url': asset.waveform_url,
                'duration': asset.duration,
                'sample_rate': asset.sample_rate,
                'channels': asset.channels,
                'prompt': asset.prompt,
                'generation_engine': asset.generation_engine,
                'voice_id': asset.voice_id,
                'genre': asset.genre,
                'mood': asset.mood,
                'key': asset.key,
                'bpm': asset.bpm,
                'tags': asset.tags,
                'status': asset.status,
                'created_at': asset.timestamp.isoformat()
            },
            'metadata': {
                'play_count': metadata.play_count if metadata else 0,
                'download_count': metadata.download_count if metadata else 0,
                'duplicate_count': metadata.duplicate_count if metadata else 0,
                'used_in_projects': metadata.used_in_projects if metadata else 0
            } if metadata else None,
            'lineage': {
                'parent_id': parent_lineage.parent_id if parent_lineage else None,
                'children_count': len(children_lineage)
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/audio/assets/<int:asset_id>/update', methods=['POST'])
def audio_assets_update(asset_id):
    """Update audio asset metadata."""
    try:
        asset = AudioAsset.query.get(asset_id)
        if not asset:
            return jsonify({'success': False, 'error': 'Asset not found'}), 404
        
        data = request.json
        
        if 'name' in data:
            asset.name = data['name']
        if 'description' in data:
            asset.description = data['description']
        if 'tags' in data:
            asset.tags = data['tags']
        if 'category' in data:
            asset.category = data['category']
        if 'mood' in data:
            asset.mood = data['mood']
        if 'genre' in data:
            asset.genre = data['genre']
        
        db.session.commit()
        
        return jsonify({'success': True, 'asset_id': asset.id})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


# ========== AUDIO TRACKS (Timeline) ==========

@app.route('/api/audio/tracks/add', methods=['POST'])
def audio_tracks_add():
    """Add audio asset to project timeline.
    
    Body:
        project_id: Project ID
        asset_id: Audio asset ID
        track_id: Track identifier (music_1, voiceover_1, etc.)
        start_time: Start time in seconds
        end_time: End time in seconds
        volume: 0.0-2.0 (default 1.0)
    """
    try:
        data = request.json
        
        track = AudioTrack(
            project_id=data['project_id'],
            asset_id=data['asset_id'],
            track_id=data.get('track_id', 'music_1'),
            start_time=data['start_time'],
            end_time=data['end_time'],
            volume=data.get('volume', 1.0),
            pan=data.get('pan', 0.0),
            layer_order=data.get('layer_order', 0)
        )
        
        db.session.add(track)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'track_id': track.id,
            'timeline_id': track.track_id
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/tracks/<int:track_id>/update', methods=['POST'])
def audio_tracks_update(track_id):
    """Update audio track properties (volume, pan, effects, etc.)."""
    try:
        track = AudioTrack.query.get(track_id)
        if not track:
            return jsonify({'success': False, 'error': 'Track not found'}), 404
        
        data = request.json
        
        if 'start_time' in data:
            track.start_time = data['start_time']
        if 'end_time' in data:
            track.end_time = data['end_time']
        if 'volume' in data:
            track.volume = data['volume']
        if 'pan' in data:
            track.pan = data['pan']
        if 'pitch_shift' in data:
            track.pitch_shift = data['pitch_shift']
        if 'speed' in data:
            track.speed = data['speed']
        if 'fade_in_duration' in data:
            track.fade_in_duration = data['fade_in_duration']
        if 'fade_out_duration' in data:
            track.fade_out_duration = data['fade_out_duration']
        if 'volume_automation' in data:
            track.volume_automation = json.dumps(data['volume_automation'])
        if 'effects' in data:
            track.effects = json.dumps(data['effects'])
        if 'is_muted' in data:
            track.is_muted = data['is_muted']
        if 'is_solo' in data:
            track.is_solo = data['is_solo']
        
        track.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True, 'track_id': track.id})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/tracks/<int:track_id>/delete', methods=['POST'])
def audio_tracks_delete(track_id):
    """Remove track from timeline."""
    try:
        track = AudioTrack.query.get(track_id)
        if not track:
            return jsonify({'success': False, 'error': 'Track not found'}), 404
        
        db.session.delete(track)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Track deleted'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


# ========== AUDIO MARKERS ==========

@app.route('/api/audio/markers/add', methods=['POST'])
def audio_markers_add():
    """Add timeline marker (beat, section, cue).
    
    Body:
        project_id: Project ID
        time: Time in seconds
        marker_type: beat, section, cue, note, sync
        label: Marker label
        section_type: intro, verse, chorus, bridge, outro (if type=section)
    """
    try:
        data = request.json
        
        marker = AudioMarker(
            project_id=data['project_id'],
            time=data['time'],
            marker_type=data['marker_type'],
            label=data.get('label'),
            color=data.get('color', '#FFD700'),
            section_type=data.get('section_type')
        )
        
        db.session.add(marker)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'marker_id': marker.id
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/markers/<int:marker_id>/delete', methods=['POST'])
def audio_markers_delete(marker_id):
    """Delete timeline marker."""
    try:
        marker = AudioMarker.query.get(marker_id)
        if not marker:
            return jsonify({'success': False, 'error': 'Marker not found'}), 404
        
        db.session.delete(marker)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Marker deleted'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


# ========== AUDIO LIBRARY ==========

@app.route('/api/audio/library/search', methods=['GET'])
def audio_library_search():
    """Search audio library with advanced filters.
    
    Query params:
        q: Search query (name, description, tags)
        asset_type: music, voiceover, sfx, ambient, stem
        genre: Genre filter
        mood: Mood filter
        bpm_min/bpm_max: BPM range
        key: Musical key
        duration_min/duration_max: Duration range
        engine: Generation engine filter
        sort: name, created_at, duration, play_count (default: created_at)
        order: asc, desc (default: desc)
        limit: Results limit (default: 50)
    """
    try:
        query = AudioAsset.query
        
        # Text search
        search_text = request.args.get('q')
        if search_text:
            query = query.filter(
                or_(
                    AudioAsset.name.ilike(f'%{search_text}%'),
                    AudioAsset.description.ilike(f'%{search_text}%'),
                    AudioAsset.tags.ilike(f'%{search_text}%')
                )
            )
        
        # Filters
        if request.args.get('asset_type'):
            query = query.filter_by(asset_type=request.args.get('asset_type'))
        if request.args.get('genre'):
            query = query.filter_by(genre=request.args.get('genre'))
        if request.args.get('mood'):
            query = query.filter_by(mood=request.args.get('mood'))
        if request.args.get('key'):
            query = query.filter_by(key=request.args.get('key'))
        if request.args.get('engine'):
            query = query.filter_by(generation_engine=request.args.get('engine'))
        
        # BPM range
        bpm_min = request.args.get('bpm_min', type=int)
        bpm_max = request.args.get('bpm_max', type=int)
        if bpm_min:
            query = query.filter(AudioAsset.bpm >= bpm_min)
        if bpm_max:
            query = query.filter(AudioAsset.bpm <= bpm_max)
        
        # Duration range
        duration_min = request.args.get('duration_min', type=float)
        duration_max = request.args.get('duration_max', type=float)
        if duration_min:
            query = query.filter(AudioAsset.duration >= duration_min)
        if duration_max:
            query = query.filter(AudioAsset.duration <= duration_max)
        
        # Sorting
        sort_by = request.args.get('sort', 'created_at')
        order = request.args.get('order', 'desc')
        
        if sort_by == 'name':
            query = query.order_by(AudioAsset.name.desc() if order == 'desc' else AudioAsset.name.asc())
        elif sort_by == 'duration':
            query = query.order_by(AudioAsset.duration.desc() if order == 'desc' else AudioAsset.duration.asc())
        else:
            query = query.order_by(AudioAsset.timestamp.desc() if order == 'desc' else AudioAsset.timestamp.asc())
        
        # Limit
        limit = request.args.get('limit', 50, type=int)
        assets = query.limit(limit).all()
        
        return jsonify({
            'success': True,
            'assets': [{
                'id': a.id,
                'name': a.name,
                'asset_type': a.asset_type,
                'file_url': a.file_url,
                'waveform_url': a.waveform_url,
                'duration': a.duration,
                'genre': a.genre,
                'mood': a.mood,
                'key': a.key,
                'bpm': a.bpm,
                'tags': a.tags,
                'created_at': a.timestamp.isoformat()
            } for a in assets],
            'count': len(assets)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/audio/library/filters', methods=['GET'])
def audio_library_filters():
    """Get available filter options for audio library."""
    try:
        from sqlalchemy import func, distinct
        
        genres = db.session.query(distinct(AudioAsset.genre)).filter(AudioAsset.genre.isnot(None)).all()
        moods = db.session.query(distinct(AudioAsset.mood)).filter(AudioAsset.mood.isnot(None)).all()
        keys = db.session.query(distinct(AudioAsset.key)).filter(AudioAsset.key.isnot(None)).all()
        engines = db.session.query(distinct(AudioAsset.generation_engine)).filter(AudioAsset.generation_engine.isnot(None)).all()
        
        return jsonify({
            'success': True,
            'filters': {
                'asset_types': ['music', 'voiceover', 'sfx', 'ambient', 'stem'],
                'genres': [g[0] for g in genres if g[0]],
                'moods': [m[0] for m in moods if m[0]],
                'keys': [k[0] for k in keys if k[0]],
                'engines': [e[0] for e in engines if e[0]]
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ========== AUDIO COLLECTIONS ==========

@app.route('/api/audio/collections/create', methods=['POST'])
def audio_collections_create():
    """Create audio collection (album, playlist, sound pack).
    
    Body:
        name: Collection name
        description: Optional description
        collection_type: album, playlist, sound_pack, podcast_series, voiceover_pack
        team_id: Team ID
    """
    try:
        data = request.json
        user_id = data.get('user_id', 1)
        
        collection = AudioCollection(
            team_id=data['team_id'],
            creator_id=user_id,
            name=data['name'],
            description=data.get('description'),
            collection_type=data.get('collection_type', 'playlist'),
            cover_image_url=data.get('cover_image_url'),
            tags=data.get('tags'),
            is_public=data.get('is_public', False)
        )
        
        db.session.add(collection)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'collection_id': collection.id,
            'name': collection.name
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/collections/<int:collection_id>', methods=['GET'])
def audio_collections_get(collection_id):
    """Get collection details with all audio assets."""
    try:
        collection = AudioCollection.query.get(collection_id)
        if not collection:
            return jsonify({'success': False, 'error': 'Collection not found'}), 404
        
        # Get collection items
        items = AudioCollectionItem.query.filter_by(collection_id=collection_id).order_by(AudioCollectionItem.order_index).all()
        
        # Get audio assets
        asset_ids = [item.asset_id for item in items]
        assets = AudioAsset.query.filter(AudioAsset.id.in_(asset_ids)).all() if asset_ids else []
        asset_map = {a.id: a for a in assets}
        
        return jsonify({
            'success': True,
            'collection': {
                'id': collection.id,
                'name': collection.name,
                'description': collection.description,
                'collection_type': collection.collection_type,
                'cover_image_url': collection.cover_image_url,
                'audio_count': collection.audio_count,
                'total_duration': collection.total_duration,
                'created_at': collection.created_at.isoformat()
            },
            'items': [{
                'id': item.id,
                'asset_id': item.asset_id,
                'order_index': item.order_index,
                'notes': item.notes,
                'asset': {
                    'name': asset_map[item.asset_id].name,
                    'file_url': asset_map[item.asset_id].file_url,
                    'duration': asset_map[item.asset_id].duration,
                    'genre': asset_map[item.asset_id].genre,
                    'mood': asset_map[item.asset_id].mood
                } if item.asset_id in asset_map else None
            } for item in items]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/audio/collections/<int:collection_id>/add', methods=['POST'])
def audio_collections_add(collection_id):
    """Add audio asset to collection.
    
    Body:
        asset_id: Audio asset ID
        order_index: Optional position
        notes: Optional notes
    """
    try:
        collection = AudioCollection.query.get(collection_id)
        if not collection:
            return jsonify({'success': False, 'error': 'Collection not found'}), 404
        
        data = request.json
        user_id = data.get('user_id', 1)
        
        # Check if already in collection
        existing = AudioCollectionItem.query.filter_by(
            collection_id=collection_id,
            asset_id=data['asset_id']
        ).first()
        
        if existing:
            return jsonify({'success': False, 'error': 'Audio already in collection'}), 400
        
        # Get max order index
        max_order = db.session.query(func.max(AudioCollectionItem.order_index)).filter_by(collection_id=collection_id).scalar() or 0
        
        item = AudioCollectionItem(
            collection_id=collection_id,
            asset_id=data['asset_id'],
            order_index=data.get('order_index', max_order + 1),
            notes=data.get('notes'),
            added_by=user_id
        )
        
        db.session.add(item)
        
        # Update collection stats
        asset = AudioAsset.query.get(data['asset_id'])
        if asset:
            collection.audio_count = (collection.audio_count or 0) + 1
            collection.total_duration = (collection.total_duration or 0) + asset.duration
        
        collection.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True, 'item_id': item.id})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/collections/<int:collection_id>/remove/<int:asset_id>', methods=['POST'])
def audio_collections_remove(collection_id, asset_id):
    """Remove audio from collection."""
    try:
        item = AudioCollectionItem.query.filter_by(
            collection_id=collection_id,
            asset_id=asset_id
        ).first()
        
        if not item:
            return jsonify({'success': False, 'error': 'Audio not in collection'}), 404
        
        # Update collection stats
        collection = AudioCollection.query.get(collection_id)
        asset = AudioAsset.query.get(asset_id)
        if collection and asset:
            collection.audio_count = max(0, (collection.audio_count or 0) - 1)
            collection.total_duration = max(0, (collection.total_duration or 0) - asset.duration)
            collection.updated_at = datetime.utcnow()
        
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Audio removed from collection'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


# ========== AUDIO ENGINES INFO ==========

@app.route('/api/audio/engines', methods=['GET'])
def audio_engines_list():
    """List all available audio generation engines with capabilities."""
    return jsonify({
        'success': True,
        'engines': audio_ugi.list_engines()
    })


@app.route('/api/audio/engines/<engine>', methods=['GET'])
def audio_engines_get(engine):
    """Get capabilities for specific engine."""
    capabilities = audio_ugi.get_engine_capabilities(engine)
    if not capabilities:
        return jsonify({'success': False, 'error': f'Engine not found: {engine}'}), 404
    
    return jsonify({
        'success': True,
        'engine': engine,
        'capabilities': capabilities
    })


# ==================== END PHASE 6 AUDIO STUDIO ROUTES ====================


# ================================================================
# PHASE 7: AUDIO TIMELINE ENGINE API ROUTES
# ================================================================
"""
Professional DAW capabilities:
- Multi-track timeline editing (place, move, trim, split, ripple, crossfade)
- Mixer console (fader, pan, mute, solo, sends)
- Automation (volume, pan, effects)
- Effects chains (8 built-in effects + presets)
- AI-assisted mixing (balance, EQ, clipping, noise)
"""

# Initialize engines (lazy loading)
_timeline_engine = None
_mixer_engine = None
_automation_engine = None
_effects_engine = None
_ai_assistant = None

def get_timeline_engine():
    """Get or create timeline engine instance."""
    global _timeline_engine
    if _timeline_engine is None:
        from audio_timeline_engine import AudioTimelineEngine
        _timeline_engine = AudioTimelineEngine(db)
    return _timeline_engine

def get_mixer_engine():
    """Get or create mixer engine instance."""
    global _mixer_engine
    if _mixer_engine is None:
        from audio_mixer import AudioMixer
        _mixer_engine = AudioMixer(db)
    return _mixer_engine

def get_automation_engine():
    """Get or create automation engine instance."""
    global _automation_engine
    if _automation_engine is None:
        from audio_automation import AudioAutomationEngine
        _automation_engine = AudioAutomationEngine(db)
    return _automation_engine

def get_effects_engine():
    """Get or create effects engine instance."""
    global _effects_engine
    if _effects_engine is None:
        from audio_effects import AudioEffectsEngine
        _effects_engine = AudioEffectsEngine(db)
    return _effects_engine

def get_ai_assistant():
    """Get or create AI assistant instance."""
    global _ai_assistant
    if _ai_assistant is None:
        from ai_audio_assistant import AIAudioAssistant
        _ai_assistant = AIAudioAssistant(db)
    return _ai_assistant


# ========== TIMELINE OPERATIONS ==========

@app.route('/api/audio/timeline/place-clip', methods=['POST'])
def audio_timeline_place_clip():
    """Place audio clip on timeline.
    
    Body:
        project_id: int
        track_id: int
        asset_id: int
        start_time: float (seconds)
        duration: float (seconds)
        clip_gain: float (dB, -60 to +24)
        pitch_shift: int (semitones, -12 to +12)
        time_stretch: float (speed multiplier, 0.5 to 2.0)
        clip_name: str (optional)
        clip_color: str (optional, hex color)
    """
    try:
        data = request.json
        engine = get_timeline_engine()
        
        result = engine.place_clip(
            project_id=data['project_id'],
            track_id=data['track_id'],
            asset_id=data['asset_id'],
            start_time=data['start_time'],
            duration=data['duration'],
            clip_gain=data.get('clip_gain', 0.0),
            pitch_shift=data.get('pitch_shift', 0),
            time_stretch=data.get('time_stretch', 1.0),
            clip_name=data.get('clip_name'),
            clip_color=data.get('clip_color')
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/timeline/move-clip', methods=['POST'])
def audio_timeline_move_clip():
    """Move clip to new position/track.
    
    Body:
        clip_id: int
        new_start_time: float (seconds)
        new_track_id: int (optional, for track change)
    """
    try:
        data = request.json
        engine = get_timeline_engine()
        
        result = engine.move_clip(
            clip_id=data['clip_id'],
            new_start_time=data['new_start_time'],
            new_track_id=data.get('new_track_id')
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/timeline/trim-start', methods=['POST'])
def audio_timeline_trim_start():
    """Trim clip start point (non-destructive).
    
    Body:
        clip_id: int
        new_start_time: float (seconds)
    """
    try:
        data = request.json
        engine = get_timeline_engine()
        
        result = engine.trim_clip_start(
            clip_id=data['clip_id'],
            new_start_time=data['new_start_time']
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/timeline/trim-end', methods=['POST'])
def audio_timeline_trim_end():
    """Trim clip end point (non-destructive).
    
    Body:
        clip_id: int
        new_end_time: float (seconds)
    """
    try:
        data = request.json
        engine = get_timeline_engine()
        
        result = engine.trim_clip_end(
            clip_id=data['clip_id'],
            new_end_time=data['new_end_time']
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/timeline/split', methods=['POST'])
def audio_timeline_split():
    """Split clip at time point.
    
    Body:
        clip_id: int
        split_time: float (seconds)
    """
    try:
        data = request.json
        engine = get_timeline_engine()
        
        result = engine.split_clip(
            clip_id=data['clip_id'],
            split_time=data['split_time']
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/timeline/ripple-delete', methods=['POST'])
def audio_timeline_ripple_delete():
    """Delete clip and shift subsequent clips left.
    
    Body:
        clip_id: int
        track_id: int (optional, only ripple on specific track)
    """
    try:
        data = request.json
        engine = get_timeline_engine()
        
        result = engine.ripple_delete(
            clip_id=data['clip_id'],
            track_id=data.get('track_id')
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/timeline/crossfade', methods=['POST'])
def audio_timeline_crossfade():
    """Create crossfade between two clips.
    
    Body:
        clip1_id: int
        clip2_id: int
        duration: float (seconds, default 0.5)
    """
    try:
        data = request.json
        engine = get_timeline_engine()
        
        result = engine.create_crossfade(
            clip1_id=data['clip1_id'],
            clip2_id=data['clip2_id'],
            duration=data.get('duration', 0.5)
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/timeline/duplicate', methods=['POST'])
def audio_timeline_duplicate():
    """Duplicate clip.
    
    Body:
        clip_id: int
        offset: float (seconds after original, default 0.0)
    """
    try:
        data = request.json
        engine = get_timeline_engine()
        
        result = engine.duplicate_clip(
            clip_id=data['clip_id'],
            offset=data.get('offset', 0.0)
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/timeline/clips/<int:project_id>', methods=['GET'])
def audio_timeline_get_clips(project_id):
    """Get all clips on timeline.
    
    Query params:
        track_id: int (optional)
        start_time: float (optional)
        end_time: float (optional)
    """
    try:
        track_id = request.args.get('track_id', type=int)
        start_time = request.args.get('start_time', type=float)
        end_time = request.args.get('end_time', type=float)
        
        time_range = None
        if start_time is not None and end_time is not None:
            time_range = (start_time, end_time)
        
        engine = get_timeline_engine()
        
        result = engine.get_timeline_clips(
            project_id=project_id,
            track_id=track_id,
            time_range=time_range
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/timeline/duration/<int:project_id>', methods=['GET'])
def audio_timeline_get_duration(project_id):
    """Get total project duration."""
    try:
        engine = get_timeline_engine()
        duration = engine.get_project_duration(project_id)
        
        return jsonify({
            'success': True,
            'project_id': project_id,
            'duration': duration
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ========== MIXER OPERATIONS ==========

@app.route('/api/audio/mixer/fader', methods=['POST'])
def audio_mixer_update_fader():
    """Update track fader level.
    
    Body:
        project_id: int
        track_id: int (null for master)
        level_db: float (-60 to +12 dB)
    """
    try:
        data = request.json
        engine = get_mixer_engine()
        
        result = engine.update_fader(
            project_id=data['project_id'],
            track_id=data.get('track_id'),
            level_db=data['level_db']
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/mixer/pan', methods=['POST'])
def audio_mixer_update_pan():
    """Update track pan position.
    
    Body:
        project_id: int
        track_id: int
        pan_position: float (-1.0 left to +1.0 right)
    """
    try:
        data = request.json
        engine = get_mixer_engine()
        
        result = engine.update_pan(
            project_id=data['project_id'],
            track_id=data['track_id'],
            pan_position=data['pan_position']
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/mixer/mute', methods=['POST'])
def audio_mixer_toggle_mute():
    """Toggle track mute.
    
    Body:
        project_id: int
        track_id: int
    """
    try:
        data = request.json
        engine = get_mixer_engine()
        
        result = engine.toggle_mute(
            project_id=data['project_id'],
            track_id=data['track_id']
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/mixer/solo', methods=['POST'])
def audio_mixer_toggle_solo():
    """Toggle track solo.
    
    Body:
        project_id: int
        track_id: int
    """
    try:
        data = request.json
        engine = get_mixer_engine()
        
        result = engine.toggle_solo(
            project_id=data['project_id'],
            track_id=data['track_id']
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/mixer/send', methods=['POST'])
def audio_mixer_update_send():
    """Update send level.
    
    Body:
        project_id: int
        track_id: int
        send_type: str (reverb, delay, aux_1, aux_2)
        level_db: float (-60 to +12 dB)
    """
    try:
        data = request.json
        engine = get_mixer_engine()
        
        result = engine.update_send_level(
            project_id=data['project_id'],
            track_id=data['track_id'],
            send_type=data['send_type'],
            level_db=data['level_db']
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/mixer/state/<int:project_id>', methods=['GET'])
def audio_mixer_get_state(project_id):
    """Get complete mixer state."""
    try:
        engine = get_mixer_engine()
        
        result = engine.get_mixer_state(project_id)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/mixer/reset', methods=['POST'])
def audio_mixer_reset():
    """Reset all mixer channels to defaults.
    
    Body:
        project_id: int
    """
    try:
        data = request.json
        engine = get_mixer_engine()
        
        result = engine.reset_mixer(data['project_id'])
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ========== AUTOMATION OPERATIONS ==========

@app.route('/api/audio/automation/create', methods=['POST'])
def audio_automation_create():
    """Create automation lane.
    
    Body:
        project_id: int
        automation_type: str (volume, pan, reverb_send, delay_send, filter_cutoff, eq_band_1, etc.)
        track_id: int (optional)
        clip_id: int (optional)
        initial_points: list of {time, value, curve} (optional)
    """
    try:
        data = request.json
        engine = get_automation_engine()
        
        result = engine.create_automation(
            project_id=data['project_id'],
            automation_type=data['automation_type'],
            track_id=data.get('track_id'),
            clip_id=data.get('clip_id'),
            initial_points=data.get('initial_points')
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/automation/add-point', methods=['POST'])
def audio_automation_add_point():
    """Add automation point.
    
    Body:
        automation_id: int
        time: float (seconds)
        value: float
        curve: str (linear, exponential, logarithmic, s-curve, step)
    """
    try:
        data = request.json
        engine = get_automation_engine()
        
        result = engine.add_point(
            automation_id=data['automation_id'],
            time=data['time'],
            value=data['value'],
            curve=data.get('curve', 'linear')
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/automation/move-point', methods=['POST'])
def audio_automation_move_point():
    """Move automation point.
    
    Body:
        automation_id: int
        point_index: int
        new_time: float (optional)
        new_value: float (optional)
    """
    try:
        data = request.json
        engine = get_automation_engine()
        
        result = engine.move_point(
            automation_id=data['automation_id'],
            point_index=data['point_index'],
            new_time=data.get('new_time'),
            new_value=data.get('new_value')
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/automation/delete-point', methods=['POST'])
def audio_automation_delete_point():
    """Delete automation point.
    
    Body:
        automation_id: int
        point_index: int
    """
    try:
        data = request.json
        engine = get_automation_engine()
        
        result = engine.delete_point(
            automation_id=data['automation_id'],
            point_index=data['point_index']
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/automation/value/<int:automation_id>', methods=['GET'])
def audio_automation_get_value(automation_id):
    """Get automation value at specific time.
    
    Query params:
        time: float (seconds)
    """
    try:
        time = request.args.get('time', type=float, default=0.0)
        engine = get_automation_engine()
        
        value = engine.get_value_at_time(automation_id, time)
        
        return jsonify({
            'success': True,
            'automation_id': automation_id,
            'time': time,
            'value': value
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/automation/list/<int:project_id>', methods=['GET'])
def audio_automation_list(project_id):
    """List automation lanes.
    
    Query params:
        automation_type: str (optional)
        track_id: int (optional)
    """
    try:
        automation_type = request.args.get('automation_type')
        track_id = request.args.get('track_id', type=int)
        
        engine = get_automation_engine()
        
        result = engine.get_automation(
            project_id=project_id,
            automation_type=automation_type,
            track_id=track_id
        )
        
        return jsonify({
            'success': True,
            'project_id': project_id,
            'automation_lanes': result
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ========== EFFECTS OPERATIONS ==========

@app.route('/api/audio/effects/add', methods=['POST'])
def audio_effects_add():
    """Add effect to track or clip.
    
    Body:
        project_id: int
        effect_type: str (eq, compressor, reverb, delay, chorus, distortion, filter, noise_reduction)
        track_id: int (optional, for track effect)
        clip_id: int (optional, for clip effect)
        parameters: dict (optional, effect-specific params)
    """
    try:
        data = request.json
        engine = get_effects_engine()
        
        result = engine.add_effect(
            project_id=data['project_id'],
            effect_type=data['effect_type'],
            track_id=data.get('track_id'),
            clip_id=data.get('clip_id'),
            parameters=data.get('parameters')
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/effects/update', methods=['POST'])
def audio_effects_update():
    """Update effect parameters.
    
    Body:
        effect_id: int
        parameters: dict (parameters to update)
    """
    try:
        data = request.json
        engine = get_effects_engine()
        
        result = engine.update_effect(
            effect_id=data['effect_id'],
            parameters=data['parameters']
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/effects/remove', methods=['POST'])
def audio_effects_remove():
    """Remove effect.
    
    Body:
        effect_id: int
    """
    try:
        data = request.json
        engine = get_effects_engine()
        
        result = engine.remove_effect(data['effect_id'])
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/effects/toggle', methods=['POST'])
def audio_effects_toggle():
    """Toggle effect enable/disable.
    
    Body:
        effect_id: int
    """
    try:
        data = request.json
        engine = get_effects_engine()
        
        result = engine.toggle_effect(data['effect_id'])
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/effects/bypass', methods=['POST'])
def audio_effects_bypass():
    """Toggle effect bypass.
    
    Body:
        effect_id: int
    """
    try:
        data = request.json
        engine = get_effects_engine()
        
        result = engine.bypass_effect(data['effect_id'])
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/effects/reorder', methods=['POST'])
def audio_effects_reorder():
    """Reorder effect chain.
    
    Body:
        project_id: int
        effect_order: list of effect IDs in desired order
        track_id: int (optional)
    """
    try:
        data = request.json
        engine = get_effects_engine()
        
        result = engine.reorder_effects(
            project_id=data['project_id'],
            effect_order=data['effect_order'],
            track_id=data.get('track_id')
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/effects/chain/<int:project_id>', methods=['GET'])
def audio_effects_get_chain(project_id):
    """Get effect chain.
    
    Query params:
        track_id: int (optional)
        clip_id: int (optional)
    """
    try:
        track_id = request.args.get('track_id', type=int)
        clip_id = request.args.get('clip_id', type=int)
        
        engine = get_effects_engine()
        
        result = engine.get_effect_chain(
            project_id=project_id,
            track_id=track_id,
            clip_id=clip_id
        )
        
        return jsonify({
            'success': True,
            'project_id': project_id,
            'effects': result
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ========== PRESETS OPERATIONS ==========

@app.route('/api/audio/presets/save', methods=['POST'])
def audio_presets_save():
    """Save effect preset.
    
    Body:
        user_id: str
        effect_type: str
        name: str
        parameters: dict
        description: str (optional)
        category: str (optional)
    """
    try:
        data = request.json
        engine = get_effects_engine()
        
        result = engine.save_preset(
            user_id=data['user_id'],
            effect_type=data['effect_type'],
            name=data['name'],
            parameters=data['parameters'],
            description=data.get('description'),
            category=data.get('category')
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/presets/load', methods=['POST'])
def audio_presets_load():
    """Load preset into effect.
    
    Body:
        effect_id: int
        preset_id: int
    """
    try:
        data = request.json
        engine = get_effects_engine()
        
        result = engine.load_preset(
            effect_id=data['effect_id'],
            preset_id=data['preset_id']
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/presets/list', methods=['GET'])
def audio_presets_list():
    """List available presets.
    
    Query params:
        effect_type: str (optional)
        category: str (optional)
    """
    try:
        effect_type = request.args.get('effect_type')
        category = request.args.get('category')
        
        engine = get_effects_engine()
        
        result = engine.list_presets(
            effect_type=effect_type,
            category=category
        )
        
        return jsonify({
            'success': True,
            'presets': result
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ========== AI ASSISTANT OPERATIONS ==========

@app.route('/api/audio/ai/analyze-levels', methods=['POST'])
def audio_ai_analyze_levels():
    """Analyze track levels and suggest improvements.
    
    Body:
        project_id: int
    """
    try:
        data = request.json
        assistant = get_ai_assistant()
        
        result = assistant.analyze_levels(data['project_id'])
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/ai/auto-balance', methods=['POST'])
def audio_ai_auto_balance():
    """Automatically balance track levels.
    
    Body:
        project_id: int
        target_loudness: float (LUFS, default -14.0)
    """
    try:
        data = request.json
        assistant = get_ai_assistant()
        
        result = assistant.auto_balance(
            project_id=data['project_id'],
            target_loudness=data.get('target_loudness', -14.0)
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/ai/detect-noise', methods=['POST'])
def audio_ai_detect_noise():
    """Detect noise in tracks.
    
    Body:
        project_id: int
        track_id: int (optional)
    """
    try:
        data = request.json
        assistant = get_ai_assistant()
        
        result = assistant.detect_noise(
            project_id=data['project_id'],
            track_id=data.get('track_id')
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/ai/suggest-eq', methods=['POST'])
def audio_ai_suggest_eq():
    """Suggest EQ settings for audio type.
    
    Body:
        asset_type: str (music, voiceover, sfx, ambient)
        genre: str (optional, for music assets)
    """
    try:
        data = request.json
        assistant = get_ai_assistant()
        
        result = assistant.suggest_eq(
            asset_type=data['asset_type'],
            genre=data.get('genre')
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/ai/detect-clipping', methods=['POST'])
def audio_ai_detect_clipping():
    """Detect clipping in project.
    
    Body:
        project_id: int
    """
    try:
        data = request.json
        assistant = get_ai_assistant()
        
        result = assistant.detect_clipping(data['project_id'])
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/ai/auto-master', methods=['POST'])
def audio_ai_auto_master():
    """Apply automatic mastering.
    
    Body:
        project_id: int
        target_loudness: float (LUFS, default -14.0)
        add_limiter: bool (default True)
    """
    try:
        data = request.json
        assistant = get_ai_assistant()
        
        result = assistant.auto_master(
            project_id=data['project_id'],
            target_loudness=data.get('target_loudness', -14.0),
            add_limiter=data.get('add_limiter', True)
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/ai/suggest-improvements', methods=['POST'])
def audio_ai_suggest_improvements():
    """Get comprehensive mix improvement suggestions.
    
    Body:
        project_id: int
    """
    try:
        data = request.json
        assistant = get_ai_assistant()
        
        result = assistant.suggest_mix_improvements(data['project_id'])
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ==================== END PHASE 7 AUDIO TIMELINE ENGINE ROUTES ====================


# ==================== PHASE 8: VOICE + MUSIC GENERATION LAYER API ROUTES ====================

# ========== VOICE GENERATION PANEL ==========

@app.route('/api/audio/voice/generate', methods=['POST'])
def audio_voice_generate():
    """Generate voiceover/voice.
    
    Body:
        text: str (script text)
        engine: str (elevenlabs, playht, azure)
        voice_id: str
        voice_settings: dict (stability, similarity_boost, style, etc.)
        project_id: int (optional)
    """
    try:
        data = request.json
        
        from universal_audio_interface import UniversalAudioInterface
        audio_ugi = UniversalAudioInterface()
        
        # Generate voice
        result = audio_ugi.generate_audio(
            prompt=data['text'],
            engine=data.get('engine', 'elevenlabs'),
            audio_type='voiceover',
            voice_id=data.get('voice_id'),
            **data.get('voice_settings', {})
        )
        
        if result.get('success') and data.get('project_id'):
            # Save to database
            asset = AudioAsset(
                project_id=data['project_id'],
                name=f"Voice - {data['text'][:30]}",
                asset_type='voiceover',
                audio_url=result['audio_url'],
                duration=result.get('duration'),
                sample_rate=result.get('sample_rate'),
                engine=data.get('engine', 'elevenlabs'),
                prompt=data['text'],
                status='ready'
            )
            db.session.add(asset)
            db.session.commit()
            
            result['asset_id'] = asset.id
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/voice/engines', methods=['GET'])
def audio_voice_engines():
    """List available voice engines."""
    return jsonify({
        'success': True,
        'engines': [
            {
                'id': 'elevenlabs',
                'name': 'ElevenLabs',
                'features': ['voice_cloning', 'multilingual', 'emotions'],
                'max_chars': 5000
            },
            {
                'id': 'playht',
                'name': 'Play.ht',
                'features': ['voice_cloning', 'ultra_realistic', 'fast'],
                'max_chars': 10000
            },
            {
                'id': 'azure',
                'name': 'Azure Neural Voices',
                'features': ['100+_voices', 'styles', 'ssml'],
                'max_chars': 10000
            }
        ]
    })


@app.route('/api/audio/voice/voices', methods=['GET'])
def audio_voice_voices():
    """List available voices for engine.
    
    Query params:
        engine: str (elevenlabs, playht, azure)
    """
    engine = request.args.get('engine', 'elevenlabs')
    
    voices_db = {
        'elevenlabs': [
            {'id': 'rachel', 'name': 'Rachel', 'gender': 'female', 'age': 'young_adult'},
            {'id': 'josh', 'name': 'Josh', 'gender': 'male', 'age': 'young_adult'},
            {'id': 'bella', 'name': 'Bella', 'gender': 'female', 'age': 'middle_aged'}
        ],
        'playht': [
            {'id': 'larry', 'name': 'Larry', 'gender': 'male', 'age': 'middle_aged'},
            {'id': 'amelia', 'name': 'Amelia', 'gender': 'female', 'age': 'young_adult'}
        ],
        'azure': [
            {'id': 'en-US-JennyNeural', 'name': 'Jenny', 'gender': 'female', 'language': 'en-US'},
            {'id': 'en-US-GuyNeural', 'name': 'Guy', 'gender': 'male', 'language': 'en-US'}
        ]
    }
    
    return jsonify({
        'success': True,
        'engine': engine,
        'voices': voices_db.get(engine, [])
    })


@app.route('/api/audio/voice/preview', methods=['POST'])
def audio_voice_preview():
    """Preview voice with sample text.
    
    Body:
        engine: str
        voice_id: str
        sample_text: str (optional, uses default)
    """
    try:
        data = request.json
        
        sample = data.get('sample_text', "Hello, this is a voice preview sample.")
        
        from universal_audio_interface import UniversalAudioInterface
        audio_ugi = UniversalAudioInterface()
        
        result = audio_ugi.generate_audio(
            prompt=sample,
            engine=data['engine'],
            audio_type='voiceover',
            voice_id=data['voice_id']
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/voice/styles', methods=['GET'])
def audio_voice_styles():
    """Get available voice styles for engine.
    
    Query params:
        engine: str
    """
    engine = request.args.get('engine', 'azure')
    
    styles_db = {
        'azure': ['newscast', 'customer_service', 'cheerful', 'sad', 'angry', 'friendly'],
        'elevenlabs': ['default', 'excited', 'serious', 'calm'],
        'playht': ['conversational', 'narrative', 'instructional']
    }
    
    return jsonify({
        'success': True,
        'engine': engine,
        'styles': styles_db.get(engine, ['default'])
    })


@app.route('/api/audio/voice/clone', methods=['POST'])
def audio_voice_clone():
    """Clone custom voice from samples.
    
    Body:
        engine: str
        voice_name: str
        sample_audio_urls: list[str]
    """
    try:
        data = request.json
        
        # Placeholder for voice cloning
        return jsonify({
            'success': True,
            'voice_id': f"cloned_{data['voice_name'].lower().replace(' ', '_')}",
            'message': 'Voice cloned successfully (simulated)'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/voice/languages', methods=['GET'])
def audio_voice_languages():
    """Get supported languages for engine.
    
    Query params:
        engine: str
    """
    engine = request.args.get('engine', 'azure')
    
    languages_db = {
        'azure': ['en-US', 'en-GB', 'es-ES', 'fr-FR', 'de-DE', 'it-IT', 'pt-BR', 'ja-JP', 'ko-KR', 'zh-CN'],
        'elevenlabs': ['en', 'es', 'fr', 'de', 'it', 'pt', 'pl', 'tr', 'ru', 'nl', 'sv', 'cs'],
        'playht': ['en-US', 'en-GB', 'es-ES', 'fr-FR', 'de-DE']
    }
    
    return jsonify({
        'success': True,
        'engine': engine,
        'languages': languages_db.get(engine, ['en-US'])
    })


@app.route('/api/audio/voice/batch', methods=['POST'])
def audio_voice_batch():
    """Generate multiple voiceovers in batch.
    
    Body:
        scripts: list[dict] with text, voice_id, settings
        engine: str
        project_id: int
    """
    try:
        data = request.json
        
        from universal_audio_interface import UniversalAudioInterface
        audio_ugi = UniversalAudioInterface()
        
        results = []
        for script in data['scripts']:
            result = audio_ugi.generate_audio(
                prompt=script['text'],
                engine=data['engine'],
                audio_type='voiceover',
                voice_id=script.get('voice_id'),
                **script.get('settings', {})
            )
            
            if result.get('success') and data.get('project_id'):
                asset = AudioAsset(
                    project_id=data['project_id'],
                    name=f"Voice - {script['text'][:30]}",
                    asset_type='voiceover',
                    audio_url=result['audio_url'],
                    duration=result.get('duration'),
                    engine=data['engine'],
                    prompt=script['text'],
                    status='ready'
                )
                db.session.add(asset)
                result['asset_id'] = asset.id
            
            results.append(result)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(results)
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/voice/settings', methods=['GET'])
def audio_voice_settings():
    """Get engine-specific voice settings.
    
    Query params:
        engine: str
    """
    engine = request.args.get('engine', 'elevenlabs')
    
    settings_db = {
        'elevenlabs': {
            'stability': {'type': 'float', 'min': 0.0, 'max': 1.0, 'default': 0.5},
            'similarity_boost': {'type': 'float', 'min': 0.0, 'max': 1.0, 'default': 0.75},
            'style': {'type': 'float', 'min': 0.0, 'max': 1.0, 'default': 0.0}
        },
        'playht': {
            'quality': {'type': 'enum', 'options': ['draft', 'standard', 'premium'], 'default': 'standard'},
            'speed': {'type': 'float', 'min': 0.5, 'max': 2.0, 'default': 1.0},
            'pitch': {'type': 'int', 'min': -12, 'max': 12, 'default': 0}
        },
        'azure': {
            'style': {'type': 'enum', 'options': ['newscast', 'friendly', 'cheerful'], 'default': 'default'},
            'rate': {'type': 'enum', 'options': ['x-slow', 'slow', 'medium', 'fast', 'x-fast'], 'default': 'medium'},
            'pitch': {'type': 'enum', 'options': ['x-low', 'low', 'medium', 'high', 'x-high'], 'default': 'medium'}
        }
    }
    
    return jsonify({
        'success': True,
        'engine': engine,
        'settings': settings_db.get(engine, {})
    })


@app.route('/api/audio/voice/ssml', methods=['POST'])
def audio_voice_ssml():
    """Generate voice from SSML markup.
    
    Body:
        ssml: str (SSML markup)
        engine: str (azure recommended)
        voice_id: str
        project_id: int (optional)
    """
    try:
        data = request.json
        
        from universal_audio_interface import UniversalAudioInterface
        audio_ugi = UniversalAudioInterface()
        
        result = audio_ugi.generate_audio(
            prompt=data['ssml'],
            engine=data.get('engine', 'azure'),
            audio_type='voiceover',
            voice_id=data.get('voice_id'),
            use_ssml=True
        )
        
        if result.get('success') and data.get('project_id'):
            asset = AudioAsset(
                project_id=data['project_id'],
                name="Voice - SSML Generated",
                asset_type='voiceover',
                audio_url=result['audio_url'],
                duration=result.get('duration'),
                engine=data.get('engine', 'azure'),
                prompt=data['ssml'],
                status='ready'
            )
            db.session.add(asset)
            db.session.commit()
            
            result['asset_id'] = asset.id
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ========== MUSIC GENERATION PANEL ==========

@app.route('/api/audio/music/generate', methods=['POST'])
def audio_music_generate():
    """Generate music.
    
    Body:
        prompt: str
        engine: str (suno, udio, riffusion)
        duration: float (seconds)
        genre: str (optional)
        mood: str (optional)
        bpm: int (optional)
        key: str (optional)
        instrumental: bool (optional)
        project_id: int (optional)
    """
    try:
        data = request.json
        
        from universal_audio_interface import UniversalAudioInterface
        audio_ugi = UniversalAudioInterface()
        
        result = audio_ugi.generate_audio(
            prompt=data['prompt'],
            engine=data.get('engine', 'suno'),
            audio_type='music',
            duration=data.get('duration', 30.0),
            genre=data.get('genre'),
            mood=data.get('mood'),
            bpm=data.get('bpm'),
            key=data.get('key'),
            instrumental=data.get('instrumental', False)
        )
        
        if result.get('success') and data.get('project_id'):
            asset = AudioAsset(
                project_id=data['project_id'],
                name=f"Music - {data['prompt'][:30]}",
                asset_type='music',
                audio_url=result['audio_url'],
                duration=result.get('duration'),
                engine=data.get('engine', 'suno'),
                prompt=data['prompt'],
                status='ready'
            )
            db.session.add(asset)
            db.session.commit()
            
            result['asset_id'] = asset.id
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/music/engines', methods=['GET'])
def audio_music_engines():
    """List available music engines."""
    return jsonify({
        'success': True,
        'engines': [
            {
                'id': 'suno',
                'name': 'Suno AI',
                'features': ['vocals', 'lyrics', 'long_form'],
                'max_duration': 300
            },
            {
                'id': 'udio',
                'name': 'Udio',
                'features': ['high_quality', 'genre_control', 'extensions'],
                'max_duration': 300
            },
            {
                'id': 'riffusion',
                'name': 'Riffusion',
                'features': ['real_time', 'stable_diffusion', 'short_clips'],
                'max_duration': 10
            }
        ]
    })


@app.route('/api/audio/music/genres', methods=['GET'])
def audio_music_genres():
    """List available music genres."""
    return jsonify({
        'success': True,
        'genres': [
            'rock', 'pop', 'jazz', 'classical', 'electronic', 'hip_hop', 'r_and_b',
            'country', 'folk', 'blues', 'metal', 'indie', 'ambient', 'cinematic',
            'lo_fi', 'trap', 'house', 'techno', 'drum_and_bass', 'reggae'
        ]
    })


@app.route('/api/audio/music/moods', methods=['GET'])
def audio_music_moods():
    """List available music moods."""
    return jsonify({
        'success': True,
        'moods': [
            'upbeat', 'melancholic', 'energetic', 'calm', 'dark', 'bright',
            'mysterious', 'romantic', 'epic', 'playful', 'intense', 'relaxing',
            'aggressive', 'dreamy', 'triumphant', 'nostalgic'
        ]
    })


@app.route('/api/audio/music/structure', methods=['POST'])
def audio_music_structure():
    """Generate music with specific structure.
    
    Body:
        prompt: str
        structure: list[dict] with section, duration
            e.g., [{'section': 'intro', 'duration': 8}, {'section': 'verse', 'duration': 16}]
        engine: str
        project_id: int (optional)
    """
    try:
        data = request.json
        
        # Build structured prompt
        structured_prompt = data['prompt']
        for section in data['structure']:
            structured_prompt += f" | {section['section']} {section['duration']}s"
        
        from universal_audio_interface import UniversalAudioInterface
        audio_ugi = UniversalAudioInterface()
        
        total_duration = sum(s['duration'] for s in data['structure'])
        
        result = audio_ugi.generate_audio(
            prompt=structured_prompt,
            engine=data.get('engine', 'suno'),
            audio_type='music',
            duration=total_duration
        )
        
        if result.get('success') and data.get('project_id'):
            asset = AudioAsset(
                project_id=data['project_id'],
                name=f"Structured Music - {data['prompt'][:30]}",
                asset_type='music',
                audio_url=result['audio_url'],
                duration=total_duration,
                engine=data.get('engine', 'suno'),
                prompt=structured_prompt,
                status='ready'
            )
            db.session.add(asset)
            db.session.commit()
            
            result['asset_id'] = asset.id
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/music/instruments', methods=['GET'])
def audio_music_instruments():
    """List available instruments/instrumentation."""
    return jsonify({
        'success': True,
        'instruments': [
            'piano', 'guitar', 'bass', 'drums', 'strings', 'brass', 'woodwinds',
            'synthesizer', 'organ', 'violin', 'cello', 'flute', 'saxophone',
            'trumpet', 'trombone', 'percussion', 'harp', 'banjo', 'ukulele'
        ]
    })


@app.route('/api/audio/music/remix', methods=['POST'])
def audio_music_remix():
    """Remix existing music.
    
    Body:
        asset_id: int (source music)
        remix_style: str (e.g., "electronic", "acoustic")
        project_id: int (optional)
    """
    try:
        data = request.json
        
        # Get source asset
        source_asset = AudioAsset.query.get(data['asset_id'])
        if not source_asset:
            return jsonify({'success': False, 'error': 'Source asset not found'}), 404
        
        # Build remix prompt
        remix_prompt = f"Remix in {data['remix_style']} style: {source_asset.prompt}"
        
        from universal_audio_interface import UniversalAudioInterface
        audio_ugi = UniversalAudioInterface()
        
        result = audio_ugi.generate_audio(
            prompt=remix_prompt,
            engine=source_asset.engine,
            audio_type='music',
            duration=source_asset.duration
        )
        
        if result.get('success') and data.get('project_id'):
            asset = AudioAsset(
                project_id=data['project_id'],
                name=f"{source_asset.name} (Remix)",
                asset_type='music',
                audio_url=result['audio_url'],
                duration=result.get('duration'),
                engine=source_asset.engine,
                prompt=remix_prompt,
                status='ready'
            )
            db.session.add(asset)
            db.session.commit()
            
            result['asset_id'] = asset.id
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/music/loop', methods=['POST'])
def audio_music_loop():
    """Create seamless looping music.
    
    Body:
        prompt: str
        loop_duration: float (seconds per loop)
        engine: str
        project_id: int (optional)
    """
    try:
        data = request.json
        
        loop_prompt = f"Seamless loop: {data['prompt']}"
        
        from universal_audio_interface import UniversalAudioInterface
        audio_ugi = UniversalAudioInterface()
        
        result = audio_ugi.generate_audio(
            prompt=loop_prompt,
            engine=data.get('engine', 'suno'),
            audio_type='music',
            duration=data['loop_duration'],
            loop=True
        )
        
        if result.get('success') and data.get('project_id'):
            asset = AudioAsset(
                project_id=data['project_id'],
                name=f"Loop - {data['prompt'][:30]}",
                asset_type='music',
                audio_url=result['audio_url'],
                duration=data['loop_duration'],
                engine=data.get('engine', 'suno'),
                prompt=loop_prompt,
                status='ready'
            )
            db.session.add(asset)
            db.session.commit()
            
            result['asset_id'] = asset.id
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ========== SFX GENERATION PANEL ==========

@app.route('/api/audio/sfx/generate', methods=['POST'])
def audio_sfx_generate():
    """Generate sound effect.
    
    Body:
        prompt: str
        engine: str (stability, audiocraft, foley)
        duration: float (seconds)
        sfx_type: str (impact, whoosh, ambient, etc.)
        project_id: int (optional)
    """
    try:
        data = request.json
        
        from universal_audio_interface import UniversalAudioInterface
        audio_ugi = UniversalAudioInterface()
        
        result = audio_ugi.generate_audio(
            prompt=data['prompt'],
            engine=data.get('engine', 'stability'),
            audio_type='sfx',
            duration=data.get('duration', 5.0),
            audio_type_param=data.get('sfx_type', 'sfx')
        )
        
        if result.get('success') and data.get('project_id'):
            asset = AudioAsset(
                project_id=data['project_id'],
                name=f"SFX - {data['prompt'][:30]}",
                asset_type='sfx',
                audio_url=result['audio_url'],
                duration=result.get('duration'),
                engine=data.get('engine', 'stability'),
                prompt=data['prompt'],
                status='ready'
            )
            db.session.add(asset)
            db.session.commit()
            
            result['asset_id'] = asset.id
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/sfx/engines', methods=['GET'])
def audio_sfx_engines():
    """List available SFX engines."""
    return jsonify({
        'success': True,
        'engines': [
            {
                'id': 'stability',
                'name': 'Stability Audio',
                'features': ['high_quality', 'fast', 'versatile'],
                'max_duration': 30
            },
            {
                'id': 'audiocraft',
                'name': 'AudioCraft',
                'features': ['meta_ai', 'general_purpose', 'open_source'],
                'max_duration': 30
            },
            {
                'id': 'foley',
                'name': 'Foley Generator',
                'features': ['procedural', 'realistic', 'customizable'],
                'max_duration': 10
            }
        ]
    })


@app.route('/api/audio/sfx/categories', methods=['GET'])
def audio_sfx_categories():
    """List SFX categories."""
    return jsonify({
        'success': True,
        'categories': [
            'impact', 'whoosh', 'ambient', 'mechanical', 'nature', 'human',
            'ui', 'vehicle', 'weapon', 'magic', 'explosion', 'door',
            'footstep', 'water', 'fire', 'wind', 'animal', 'crowd'
        ]
    })


@app.route('/api/audio/sfx/foley', methods=['POST'])
def audio_sfx_foley():
    """Generate Foley sound effect.
    
    Body:
        action: str (footstep, door, impact, etc.)
        surface: str (wood, concrete, metal, etc.)
        intensity: str (soft, medium, hard)
        duration: float (seconds)
        variation: int (number of variations)
        project_id: int (optional)
    """
    try:
        data = request.json
        
        from universal_audio_interface import UniversalAudioInterface
        audio_ugi = UniversalAudioInterface()
        
        # Build Foley prompt
        foley_prompt = f"{data['action']} on {data['surface']}, {data.get('intensity', 'medium')} intensity"
        
        result = audio_ugi.generate_audio(
            prompt=foley_prompt,
            engine='foley',
            audio_type='sfx',
            duration=data.get('duration', 2.0),
            action=data['action'],
            surface=data['surface'],
            intensity=data.get('intensity', 'medium'),
            variation=data.get('variation', 1)
        )
        
        if result.get('success') and data.get('project_id'):
            asset = AudioAsset(
                project_id=data['project_id'],
                name=f"Foley - {data['action']} ({data['surface']})",
                asset_type='sfx',
                audio_url=result['audio_url'],
                duration=result.get('duration'),
                engine='foley',
                prompt=foley_prompt,
                status='ready'
            )
            db.session.add(asset)
            db.session.commit()
            
            result['asset_id'] = asset.id
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/sfx/ambient', methods=['POST'])
def audio_sfx_ambient():
    """Generate ambient sound.
    
    Body:
        environment: str (forest, city, ocean, etc.)
        duration: float (seconds)
        intensity: float (0.0 to 1.0)
        project_id: int (optional)
    """
    try:
        data = request.json
        
        from universal_audio_interface import UniversalAudioInterface
        audio_ugi = UniversalAudioInterface()
        
        ambient_prompt = f"{data['environment']} ambient sound"
        
        result = audio_ugi.generate_audio(
            prompt=ambient_prompt,
            engine='stability',
            audio_type='ambient',
            duration=data.get('duration', 30.0),
            audio_type_param='ambient'
        )
        
        if result.get('success') and data.get('project_id'):
            asset = AudioAsset(
                project_id=data['project_id'],
                name=f"Ambient - {data['environment']}",
                asset_type='ambient',
                audio_url=result['audio_url'],
                duration=result.get('duration'),
                engine='stability',
                prompt=ambient_prompt,
                status='ready'
            )
            db.session.add(asset)
            db.session.commit()
            
            result['asset_id'] = asset.id
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/sfx/presets', methods=['GET'])
def audio_sfx_presets():
    """Get preset SFX templates."""
    return jsonify({
        'success': True,
        'presets': [
            {'name': 'Door Open', 'action': 'door_open', 'surface': 'wood', 'duration': 2.0},
            {'name': 'Footstep', 'action': 'footstep', 'surface': 'concrete', 'duration': 0.5},
            {'name': 'Impact', 'action': 'impact', 'surface': 'metal', 'duration': 1.0},
            {'name': 'Glass Break', 'action': 'break', 'surface': 'glass', 'duration': 2.0},
            {'name': 'Water Splash', 'action': 'splash', 'surface': 'water', 'duration': 1.5}
        ]
    })


# ========== EVOLUTION SYSTEM ==========

@app.route('/api/audio/evolution/evolve', methods=['POST'])
def audio_evolution_evolve():
    """Evolve audio to improve quality.
    
    Body:
        asset_id: int
        evolution_type: str (refine, enhance, cleanup, polish, remaster)
        parameters: dict (optional)
    """
    try:
        data = request.json
        
        from audio_evolution_engine import AudioEvolutionEngine
        evolution_engine = AudioEvolutionEngine(db)
        
        result = evolution_engine.evolve(
            asset_id=data['asset_id'],
            evolution_type=data.get('evolution_type', 'refine'),
            parameters=data.get('parameters')
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/evolution/extend', methods=['POST'])
def audio_evolution_extend():
    """Extend audio duration.
    
    Body:
        asset_id: int
        extension_duration: float (seconds to add)
        extension_type: str (continue, loop, variation, outro, bridge)
        parameters: dict (optional)
    """
    try:
        data = request.json
        
        from audio_evolution_engine import AudioEvolutionEngine
        evolution_engine = AudioEvolutionEngine(db)
        
        result = evolution_engine.extend(
            asset_id=data['asset_id'],
            extension_duration=data.get('extension_duration', 30.0),
            extension_type=data.get('extension_type', 'continue'),
            parameters=data.get('parameters')
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/evolution/regenerate', methods=['POST'])
def audio_evolution_regenerate():
    """Regenerate audio with alternate take.
    
    Body:
        asset_id: int
        variation_style: str (alternate, different, similar, remix, reinterpret)
        parameters: dict (optional)
    """
    try:
        data = request.json
        
        from audio_evolution_engine import AudioEvolutionEngine
        evolution_engine = AudioEvolutionEngine(db)
        
        result = evolution_engine.regenerate(
            asset_id=data['asset_id'],
            variation_style=data.get('variation_style', 'alternate'),
            parameters=data.get('parameters')
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/evolution/mutate', methods=['POST'])
def audio_evolution_mutate():
    """Create experimental mutation of audio.
    
    Body:
        asset_id: int
        mutation_type: str (experimental, genre_shift, style_change, deconstruct, fusion)
        parameters: dict (optional, e.g., target_genre, target_style, effects)
    """
    try:
        data = request.json
        
        from audio_evolution_engine import AudioEvolutionEngine
        evolution_engine = AudioEvolutionEngine(db)
        
        result = evolution_engine.mutate(
            asset_id=data['asset_id'],
            mutation_type=data.get('mutation_type', 'experimental'),
            parameters=data.get('parameters')
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/evolution/lineage/<int:asset_id>', methods=['GET'])
def audio_evolution_lineage(asset_id):
    """Get complete lineage tree for asset.
    
    Returns ancestor and descendant tree structure.
    """
    try:
        from audio_evolution_engine import AudioEvolutionEngine
        evolution_engine = AudioEvolutionEngine(db)
        
        result = evolution_engine.get_lineage_tree(asset_id)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ========== CONSTELLATION INTEGRATION ==========

@app.route('/api/audio/constellation/cluster', methods=['POST'])
def audio_constellation_create_cluster():
    """Create new constellation cluster.
    
    Body:
        cluster_name: str
        cluster_type: str (mood, genre, style)
        audio_type: str (music, voice, sfx)
        metadata: dict (optional)
    """
    try:
        data = request.json
        
        from audio_constellation_integration import AudioConstellationIntegration
        constellation = AudioConstellationIntegration(db)
        
        result = constellation.create_cluster(
            cluster_name=data['cluster_name'],
            cluster_type=data['cluster_type'],
            audio_type=data['audio_type'],
            metadata=data.get('metadata')
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/constellation/add', methods=['POST'])
def audio_constellation_add_asset():
    """Add asset to constellation with automatic cluster assignment.
    
    Body:
        asset_id: int
    """
    try:
        data = request.json
        
        from audio_constellation_integration import AudioConstellationIntegration
        constellation = AudioConstellationIntegration(db)
        
        result = constellation.auto_assign_cluster(data['asset_id'])
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/constellation/query', methods=['GET'])
def audio_constellation_query():
    """Query constellation for assets.
    
    Query params:
        audio_type: str (optional)
        cluster_name: str (optional)
        tags: str (comma-separated, optional)
        limit: int (optional, default 50)
    """
    try:
        from audio_constellation_integration import AudioConstellationIntegration
        constellation = AudioConstellationIntegration(db)
        
        tags = request.args.get('tags')
        tags_list = tags.split(',') if tags else None
        
        result = constellation.query_constellation(
            audio_type=request.args.get('audio_type'),
            cluster_name=request.args.get('cluster_name'),
            tags=tags_list,
            limit=int(request.args.get('limit', 50))
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/audio/constellation/visualize/<int:asset_id>', methods=['GET'])
def audio_constellation_visualize(asset_id):
    """Get lineage visualization data for constellation view.
    
    Returns D3.js/Cytoscape-ready graph data.
    """
    try:
        from audio_constellation_integration import AudioConstellationIntegration
        constellation = AudioConstellationIntegration(db)
        
        result = constellation.visualize_lineage(asset_id)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ==================== END PHASE 8: VOICE + MUSIC GENERATION LAYER API ROUTES ====================


# =============================================================================
# GRAPHICS STUDIO - PHASE 8 API ROUTES
# =============================================================================

# Import Phase 8 components
try:
    from graphics_engines import UniversalGraphicsInterface, DallEEngine, MidjourneyEngine, StableDiffusionEngine
    from graphics_evolution_engine import GraphicsEvolutionEngine
    from graphics_constellation_integration import GraphicsConstellationIntegration
    
    graphics_interface = UniversalGraphicsInterface()
    graphics_evolution = GraphicsEvolutionEngine()
    graphics_constellation = GraphicsConstellationIntegration()
    
    GRAPHICS_PHASE8_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Graphics Phase 8 not available: {e}")
    GRAPHICS_PHASE8_AVAILABLE = False


@app.route('/api/graphics/phase8/generate', methods=['POST'])
def graphics_phase8_generate():
    """
    Generate image using Phase 8 multi-engine system
    
    POST /api/graphics/phase8/generate
    Body: {
        "prompt": "A majestic lion in savanna at golden hour",
        "engine": "auto|dall-e|midjourney|stable-diffusion",
        "size": "1024x1024",
        "quality": "hd",
        "style_preset": "photographic",
        "auto_constellation": true
    }
    """
    if not GRAPHICS_PHASE8_AVAILABLE:
        return jsonify({"error": "Graphics Phase 8 not available"}), 503
    
    data = request.get_json()
    prompt = data.get('prompt')
    engine = data.get('engine', 'auto')
    size = data.get('size', '1024x1024')
    quality = data.get('quality', 'standard')
    style_preset = data.get('style_preset')
    auto_constellation = data.get('auto_constellation', True)
    
    if not prompt:
        return jsonify({"error": "Prompt required"}), 400
    
    try:
        # Generate image
        result = graphics_interface.generate(
            prompt=prompt,
            engine=engine,
            size=size,
            quality=quality,
            style_preset=style_preset
        )
        
        # Save to database
        project = GraphicsProject(
            prompt=prompt,
            aspect_ratio=size,
            thumbnail_url=result.get('image_url'),
            prompt_source=result.get('engine', 'unknown'),
            user_id=flask_session.get('user_id')
        )
        db.session.add(project)
        db.session.commit()
        
        # Auto-assign to constellation
        if auto_constellation:
            clusters = graphics_constellation.auto_assign_cluster(str(project.id))
            result['assigned_clusters'] = clusters
        
        result['asset_id'] = str(project.id)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/graphics/phase8/engines', methods=['GET'])
def graphics_phase8_engines():
    """
    Get list of available graphics engines
    
    GET /api/graphics/phase8/engines
    """
    if not GRAPHICS_PHASE8_AVAILABLE:
        return jsonify({"error": "Graphics Phase 8 not available"}), 503
    
    engines = graphics_interface.get_available_engines()
    
    return jsonify({
        "engines": engines,
        "default": "auto",
        "engine_specs": {
            "dall-e-3": {
                "name": "DALL-E 3",
                "provider": "OpenAI",
                "strengths": ["Precise prompt following", "High quality", "HD option"],
                "sizes": ["1024x1024", "1792x1024", "1024x1792"],
                "max_batch": 1
            },
            "midjourney-v6": {
                "name": "Midjourney v6",
                "provider": "Midjourney (unofficial API)",
                "strengths": ["Artistic quality", "Creative generation", "Style consistency"],
                "sizes": ["Variable (aspect ratios)"],
                "max_batch": 4
            },
            "stable-diffusion-xl": {
                "name": "Stable Diffusion XL",
                "provider": "Stability AI",
                "strengths": ["Fast generation", "Customizable", "Cost-effective"],
                "sizes": ["Up to 1536x1536"],
                "max_batch": 10
            }
        }
    })


@app.route('/api/graphics/phase8/styles', methods=['GET'])
def graphics_phase8_styles():
    """
    Get available style presets
    
    GET /api/graphics/phase8/styles?engine=stable-diffusion
    """
    engine = request.args.get('engine', 'stable-diffusion')
    
    if engine == 'stable-diffusion':
        from graphics_engines import StylePreset
        styles = [s.value for s in StylePreset]
        return jsonify({
            "engine": "stable-diffusion-xl",
            "styles": styles,
            "default": "enhance"
        })
    elif engine == 'dall-e':
        return jsonify({
            "engine": "dall-e-3",
            "styles": ["vivid", "natural"],
            "default": "vivid"
        })
    elif engine == 'midjourney':
        return jsonify({
            "engine": "midjourney-v6",
            "styles": ["Use natural language in prompt (e.g., --style raw)"],
            "default": "default"
        })
    else:
        return jsonify({"error": "Unknown engine"}), 400


@app.route('/api/graphics/phase8/batch', methods=['POST'])
def graphics_phase8_batch():
    """
    Batch generate multiple images
    
    POST /api/graphics/phase8/batch
    Body: {
        "prompts": ["prompt1", "prompt2", "prompt3"],
        "engine": "stable-diffusion",
        "size": "1024x1024"
    }
    """
    if not GRAPHICS_PHASE8_AVAILABLE:
        return jsonify({"error": "Graphics Phase 8 not available"}), 503
    
    data = request.get_json()
    prompts = data.get('prompts', [])
    engine = data.get('engine', 'stable-diffusion')
    size = data.get('size', '1024x1024')
    
    if not prompts or len(prompts) == 0:
        return jsonify({"error": "No prompts provided"}), 400
    
    if len(prompts) > 10:
        return jsonify({"error": "Max 10 prompts per batch"}), 400
    
    results = []
    for prompt in prompts:
        try:
            result = graphics_interface.generate(prompt=prompt, engine=engine, size=size)
            
            # Save to database
            project = GraphicsProject(
                prompt=prompt,
                aspect_ratio=size,
                thumbnail_url=result.get('image_url'),
                prompt_source=result.get('engine', engine),
                user_id=flask_session.get('user_id')
            )
            db.session.add(project)
            db.session.commit()
            
            result['asset_id'] = str(project.id)
            results.append(result)
            
        except Exception as e:
            results.append({"prompt": prompt, "error": str(e)})
    
    return jsonify({
        "batch_size": len(prompts),
        "successful": len([r for r in results if 'error' not in r]),
        "failed": len([r for r in results if 'error' in r]),
        "results": results
    })


@app.route('/api/graphics/phase8/upscale', methods=['POST'])
def graphics_phase8_upscale():
    """
    Upscale existing image
    
    POST /api/graphics/phase8/upscale
    Body: {
        "asset_id": "img_123",
        "target_width": 2048,
        "target_height": 2048
    }
    """
    if not GRAPHICS_PHASE8_AVAILABLE:
        return jsonify({"error": "Graphics Phase 8 not available"}), 503
    
    data = request.get_json()
    asset_id = data.get('asset_id')
    
    if not asset_id:
        return jsonify({"error": "asset_id required"}), 400
    
    # Placeholder - would use StableDiffusionEngine.upscale()
    return jsonify({
        "message": "Upscaling feature - integrate with graphics_engines.StableDiffusionEngine.upscale()",
        "asset_id": asset_id,
        "status": "pending"
    })


@app.route('/api/graphics/phase8/variations', methods=['POST'])
def graphics_phase8_variations():
    """
    Generate variations of existing image
    
    POST /api/graphics/phase8/variations
    Body: {
        "asset_id": "img_123",
        "count": 4
    }
    """
    if not GRAPHICS_PHASE8_AVAILABLE:
        return jsonify({"error": "Graphics Phase 8 not available"}), 503
    
    data = request.get_json()
    asset_id = data.get('asset_id')
    count = data.get('count', 4)
    
    if not asset_id:
        return jsonify({"error": "asset_id required"}), 400
    
    # Placeholder - would use DallEEngine.create_variation()
    return jsonify({
        "message": "Variations feature - integrate with graphics_engines.DallEEngine.create_variation()",
        "asset_id": asset_id,
        "count": count,
        "status": "pending"
    })


# Evolution API Routes
@app.route('/api/graphics/phase8/evolution/evolve', methods=['POST'])
def graphics_phase8_evolve():
    """
    Evolve image to improve quality
    
    POST /api/graphics/phase8/evolution/evolve
    Body: {
        "asset_id": "img_123",
        "evolution_type": "enhance|refine|upscale|cleanup|polish|remaster",
        "parameters": {
            "quality_boost": 0.8,
            "detail_level": "high",
            "preserve_style": true
        }
    }
    """
    if not GRAPHICS_PHASE8_AVAILABLE:
        return jsonify({"error": "Graphics Phase 8 not available"}), 503
    
    data = request.get_json()
    asset_id = data.get('asset_id')
    evolution_type = data.get('evolution_type', 'enhance')
    parameters = data.get('parameters', {})
    
    if not asset_id:
        return jsonify({"error": "asset_id required"}), 400
    
    try:
        result = graphics_evolution.evolve(
            asset_id=asset_id,
            evolution_type=evolution_type,
            parameters=parameters
        )
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/graphics/phase8/evolution/transform', methods=['POST'])
def graphics_phase8_transform():
    """
    Transform image to different style
    
    POST /api/graphics/phase8/evolution/transform
    Body: {
        "asset_id": "img_123",
        "target_style": "impressionist|photorealistic|anime|oil_painting|watercolor|sketch|cyberpunk|fantasy|minimalist|vintage",
        "intensity": 0.7,
        "preserve_content": true
    }
    """
    if not GRAPHICS_PHASE8_AVAILABLE:
        return jsonify({"error": "Graphics Phase 8 not available"}), 503
    
    data = request.get_json()
    asset_id = data.get('asset_id')
    target_style = data.get('target_style')
    intensity = data.get('intensity', 0.7)
    preserve_content = data.get('preserve_content', True)
    
    if not asset_id or not target_style:
        return jsonify({"error": "asset_id and target_style required"}), 400
    
    try:
        result = graphics_evolution.transform(
            asset_id=asset_id,
            target_style=target_style,
            intensity=intensity,
            preserve_content=preserve_content
        )
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/graphics/phase8/evolution/remix', methods=['POST'])
def graphics_phase8_remix():
    """
    Remix multiple images into one
    
    POST /api/graphics/phase8/evolution/remix
    Body: {
        "asset_ids": ["img_1", "img_2", "img_3"],
        "blend_mode": "interpolate|combine|hybrid|collage",
        "weights": [0.5, 0.3, 0.2],
        "style": "cinematic"
    }
    """
    if not GRAPHICS_PHASE8_AVAILABLE:
        return jsonify({"error": "Graphics Phase 8 not available"}), 503
    
    data = request.get_json()
    asset_ids = data.get('asset_ids', [])
    blend_mode = data.get('blend_mode', 'interpolate')
    weights = data.get('weights')
    style = data.get('style')
    
    if not asset_ids or len(asset_ids) < 2:
        return jsonify({"error": "At least 2 asset_ids required"}), 400
    
    try:
        result = graphics_evolution.remix(
            asset_ids=asset_ids,
            blend_mode=blend_mode,
            weights=weights,
            style=style
        )
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/graphics/phase8/evolution/mutate', methods=['POST'])
def graphics_phase8_mutate():
    """
    Create experimental mutation
    
    POST /api/graphics/phase8/evolution/mutate
    Body: {
        "asset_id": "img_123",
        "mutation_type": "experimental|genre_shift|mood_shift|color_shift|composition_shift",
        "parameters": {
            "chaos_level": 0.7,
            "target_genre": "surrealist",
            "target_mood": "mysterious",
            "target_palette": "neon"
        }
    }
    """
    if not GRAPHICS_PHASE8_AVAILABLE:
        return jsonify({"error": "Graphics Phase 8 not available"}), 503
    
    data = request.get_json()
    asset_id = data.get('asset_id')
    mutation_type = data.get('mutation_type', 'experimental')
    parameters = data.get('parameters', {})
    
    if not asset_id:
        return jsonify({"error": "asset_id required"}), 400
    
    try:
        result = graphics_evolution.mutate(
            asset_id=asset_id,
            mutation_type=mutation_type,
            parameters=parameters
        )
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/graphics/phase8/evolution/lineage/<asset_id>', methods=['GET'])
def graphics_phase8_lineage(asset_id):
    """
    Get complete evolutionary lineage
    
    GET /api/graphics/phase8/evolution/lineage/<asset_id>
    """
    if not GRAPHICS_PHASE8_AVAILABLE:
        return jsonify({"error": "Graphics Phase 8 not available"}), 503
    
    try:
        lineage = graphics_evolution.get_lineage_tree(asset_id)
        return jsonify(lineage)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Constellation API Routes
@app.route('/api/graphics/phase8/constellation/assign', methods=['POST'])
def graphics_phase8_constellation_assign():
    """
    Auto-assign image to clusters
    
    POST /api/graphics/phase8/constellation/assign
    Body: {
        "asset_id": "img_123"
    }
    """
    if not GRAPHICS_PHASE8_AVAILABLE:
        return jsonify({"error": "Graphics Phase 8 not available"}), 503
    
    data = request.get_json()
    asset_id = data.get('asset_id')
    
    if not asset_id:
        return jsonify({"error": "asset_id required"}), 400
    
    try:
        clusters = graphics_constellation.auto_assign_cluster(asset_id)
        return jsonify({
            "asset_id": asset_id,
            "assigned_clusters": clusters,
            "total_clusters": len(clusters)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/graphics/phase8/constellation/query', methods=['GET'])
def graphics_phase8_constellation_query():
    """
    Query constellation for matching images
    
    GET /api/graphics/phase8/constellation/query?style_family=photographic&color_palette=warm_palette&limit=20
    """
    if not GRAPHICS_PHASE8_AVAILABLE:
        return jsonify({"error": "Graphics Phase 8 not available"}), 503
    
    style_family = request.args.get('style_family')
    color_palette = request.args.get('color_palette')
    composition = request.args.get('composition')
    tags = request.args.getlist('tags')
    limit = int(request.args.get('limit', 20))
    
    try:
        results = graphics_constellation.query_constellation(
            style_family=style_family,
            color_palette=color_palette,
            composition=composition,
            tags=tags if tags else None,
            limit=limit
        )
        return jsonify(results)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/graphics/phase8/constellation/similar/<asset_id>', methods=['GET'])
def graphics_phase8_constellation_similar(asset_id):
    """
    Find similar images
    
    GET /api/graphics/phase8/constellation/similar/<asset_id>?limit=10&threshold=0.5
    """
    if not GRAPHICS_PHASE8_AVAILABLE:
        return jsonify({"error": "Graphics Phase 8 not available"}), 503
    
    limit = int(request.args.get('limit', 10))
    threshold = float(request.args.get('threshold', 0.5))
    
    try:
        similar_images = graphics_constellation.find_similar_images(
            asset_id=asset_id,
            limit=limit,
            similarity_threshold=threshold
        )
        return jsonify({
            "asset_id": asset_id,
            "similar_images": similar_images,
            "count": len(similar_images)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/graphics/phase8/constellation/visualize/<asset_id>', methods=['GET'])
def graphics_phase8_constellation_visualize(asset_id):
    """
    Get D3.js/Cytoscape visualization data
    
    GET /api/graphics/phase8/constellation/visualize/<asset_id>
    """
    if not GRAPHICS_PHASE8_AVAILABLE:
        return jsonify({"error": "Graphics Phase 8 not available"}), 503
    
    try:
        graph_data = graphics_constellation.visualize_lineage(asset_id)
        return jsonify(graph_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/graphics/phase8/constellation/map', methods=['GET'])
def graphics_phase8_constellation_map():
    """
    Get complete constellation map
    
    GET /api/graphics/phase8/constellation/map?cluster_type=all|color|style|composition
    """
    if not GRAPHICS_PHASE8_AVAILABLE:
        return jsonify({"error": "Graphics Phase 8 not available"}), 503
    
    cluster_type = request.args.get('cluster_type', 'all')
    
    try:
        constellation_map = graphics_constellation.get_constellation_map(cluster_type)
        return jsonify(constellation_map)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =============================================================================
# END GRAPHICS STUDIO PHASE 8 API ROUTES
# =============================================================================


# =============================================================================
# VIDEO STUDIO PHASE 8 API ROUTES
# =============================================================================
# Video generation with multi-engine support (Runway, Pika, Luma, Stability)
# Scene generation with storyboard-to-video conversion
# Evolution operations (evolve, vary, remix, mutate, extend)
# Timeline integration with multi-track editing
# Constellation clustering with genre/pacing/style
# =============================================================================

# Initialize Video Phase 8 components (lazy loading)
video_engine = None
video_evolution = None
video_constellation = None
video_scene_generator = None
video_timeline_editor = None

def init_video_phase8():
    """Initialize Video Phase 8 components on first use"""
    global video_engine, video_evolution, video_constellation, video_scene_generator, video_timeline_editor
    
    if video_engine is None:
        try:
            from video_engines import UniversalVideoInterface
            from video_evolution_engine import VideoEvolutionEngine
            from video_constellation_integration import VideoConstellationIntegration
            from video_scene_generator import VideoSceneGenerator
            from video_timeline_integration import VideoTimelineEditor
            
            video_engine = UniversalVideoInterface()
            video_evolution = VideoEvolutionEngine(video_engine=video_engine)
            video_constellation = VideoConstellationIntegration()
            video_scene_generator = VideoSceneGenerator(video_engine=video_engine)
            video_timeline_editor = VideoTimelineEditor()
            
        except Exception as e:
            print(f"⚠️  Video Phase 8 initialization failed: {e}")
            return False
    
    return True


# --- VIDEO GENERATION ROUTES ---

@app.route('/api/video/generate', methods=['POST'])
def api_video_generate():
    """
    Generate single video clip
    
    POST Body:
    {
        "prompt": "A bird flying through clouds",
        "engine": "auto" | "runway" | "pika" | "luma" | "stability",
        "duration": 5,
        "image_url": "optional_reference.jpg",
        "camera_motion": "pan_left" | "zoom_in" | etc.,
        "subject_motion": "slow" | "fast" | "walk" | etc.,
        "aspect_ratio": "16:9" | "9:16" | "1:1"
    }
    """
    if not init_video_phase8() or video_engine is None:
        return jsonify({"error": "Video Phase 8 not available"}), 503
    
    data = request.get_json()
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({"error": "prompt required"}), 400
    
    try:
        # Import enums for motion types
        from video_engines import CameraMotion, SubjectMotion
        
        camera_motion = None
        if data.get('camera_motion'):
            try:
                camera_motion = CameraMotion(data['camera_motion'])
            except ValueError:
                pass
        
        subject_motion = None
        if data.get('subject_motion'):
            try:
                subject_motion = SubjectMotion(data['subject_motion'])
            except ValueError:
                pass
        
        # Generate video (async operation - would need proper async handling in production)
        result = {
            'status': 'queued',
            'job_id': f"video_job_{int(datetime.utcnow().timestamp())}",
            'prompt': prompt,
            'engine': data.get('engine', 'auto'),
            'duration': data.get('duration', 5),
            'estimated_time': 90,  # seconds
            'message': 'Video generation started'
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/video/engines')
def api_video_engines():
    """Get available video engines and capabilities"""
    if not init_video_phase8():
        return jsonify({"error": "Video Phase 8 not available"}), 503
    
    from video_engines import VIDEO_ENGINE_SPECS
    
    engines = {
        'runway': {
            'name': 'Runway Gen-2',
            'capabilities': ['text_to_video', 'image_to_video', 'video_to_video'],
            'max_duration': 18,
            'resolution': '1408x768',
            'cost_per_second': 0.05,
            'generation_time': 120
        },
        'pika': {
            'name': 'Pika Labs',
            'capabilities': ['text_to_video', 'image_to_video'],
            'max_duration': 3,
            'resolution': '1280x720',
            'cost_per_second': 0.03,
            'generation_time': 60
        },
        'luma': {
            'name': 'Luma AI',
            'capabilities': ['text_to_video', 'image_to_video', 'seamless_loop'],
            'max_duration': 5,
            'resolution': 'variable',
            'cost_per_second': 0.04,
            'generation_time': 90
        },
        'stability': {
            'name': 'Stability Video',
            'capabilities': ['image_to_video'],
            'max_duration': 4,
            'resolution': '1024x576',
            'cost_per_second': 0.02,
            'generation_time': 30
        }
    }
    
    return jsonify(engines)


@app.route('/api/video/camera-motions')
def api_video_camera_motions():
    """Get available camera motion types"""
    from video_engines import CameraMotion
    
    motions = {
        'static': 'No camera movement',
        'pan_left': 'Pan camera left',
        'pan_right': 'Pan camera right',
        'tilt_up': 'Tilt camera up',
        'tilt_down': 'Tilt camera down',
        'zoom_in': 'Zoom in',
        'zoom_out': 'Zoom out',
        'dolly_in': 'Move camera forward',
        'dolly_out': 'Move camera backward',
        'orbit_left': 'Orbit around subject left',
        'orbit_right': 'Orbit around subject right',
        'crane_up': 'Crane shot upward',
        'crane_down': 'Crane shot downward'
    }
    
    return jsonify(motions)


# --- SCENE GENERATION ROUTES ---

@app.route('/api/video/storyboard', methods=['POST'])
def api_video_storyboard():
    """
    Generate video from storyboard
    
    POST Body:
    {
        "title": "My Video",
        "scenes": [
            {"description": "Scene 1...", "duration": 5},
            {"description": "Scene 2...", "duration": 3}
        ],
        "global_style": "cinematic",
        "auto_transitions": true
    }
    """
    if not init_video_phase8() or video_scene_generator is None:
        return jsonify({"error": "Video Phase 8 not available"}), 503
    
    data = request.get_json()
    
    if not data.get('scenes'):
        return jsonify({"error": "scenes array required"}), 400
    
    try:
        from video_scene_generator import create_simple_storyboard
        
        storyboard = create_simple_storyboard(
            title=data.get('title', 'Untitled Video'),
            scene_descriptions=[s['description'] for s in data['scenes']],
            scene_duration=data['scenes'][0].get('duration', 5) if data['scenes'] else 5
        )
        
        # Async operation in production
        result = {
            'status': 'queued',
            'job_id': f"storyboard_{storyboard.storyboard_id}",
            'title': storyboard.title,
            'scenes': len(storyboard.scenes),
            'estimated_duration': sum(s.duration for s in storyboard.scenes),
            'message': 'Storyboard generation started'
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/video/timeline', methods=['POST'])
def api_video_timeline_create():
    """
    Create timeline from scenes
    
    POST Body:
    {
        "scenes": [
            {"scene_id": "scene_1", "video_url": "scene1.mp4", "duration": 5}
        ],
        "audio_tracks": [
            {"audio_url": "music.mp3", "volume": 0.7}
        ]
    }
    """
    if not init_video_phase8() or video_timeline_editor is None:
        return jsonify({"error": "Video Phase 8 not available"}), 503
    
    data = request.get_json()
    
    if not data.get('scenes'):
        return jsonify({"error": "scenes array required"}), 400
    
    try:
        timeline = video_timeline_editor.create_timeline(
            scenes=data['scenes'],
            audio_tracks=data.get('audio_tracks'),
            effects=data.get('effects')
        )
        
        summary = video_timeline_editor.get_timeline_summary()
        
        return jsonify(summary)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- VIDEO EVOLUTION ROUTES ---

@app.route('/api/video/evolution/evolve', methods=['POST'])
def api_video_evolution_evolve():
    """
    Evolve video (enhance, extend, stabilize, upscale, color_grade, denoise, sharpen)
    
    POST Body:
    {
        "asset_id": "video_123",
        "evolution_type": "enhance" | "extend" | "stabilize" | etc.,
        "parameters": {
            "target_resolution": "4K",
            "color_style": "cinematic"
        }
    }
    """
    if not init_video_phase8() or video_evolution is None:
        return jsonify({"error": "Video Phase 8 not available"}), 503
    
    data = request.get_json()
    asset_id = data.get('asset_id')
    evolution_type = data.get('evolution_type')
    
    if not asset_id or not evolution_type:
        return jsonify({"error": "asset_id and evolution_type required"}), 400
    
    try:
        from video_evolution_engine import EvolutionType
        
        # Async operation
        result = {
            'status': 'queued',
            'asset_id': asset_id,
            'evolution_type': evolution_type,
            'generation': 2,
            'message': f'Video evolution ({evolution_type}) started'
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/video/evolution/vary', methods=['POST'])
def api_video_evolution_vary():
    """
    Create video variation (pacing, angle, lighting, composition, mood, weather, time_of_day)
    
    POST Body:
    {
        "asset_id": "video_123",
        "variation_type": "pacing" | "angle" | "lighting" | etc.,
        "intensity": 0.7,
        "parameters": {"target_pace": "slow"}
    }
    """
    if not init_video_phase8() or video_evolution is None:
        return jsonify({"error": "Video Phase 8 not available"}), 503
    
    data = request.get_json()
    asset_id = data.get('asset_id')
    variation_type = data.get('variation_type')
    
    if not asset_id or not variation_type:
        return jsonify({"error": "asset_id and variation_type required"}), 400
    
    try:
        result = {
            'status': 'queued',
            'asset_id': asset_id,
            'variation_type': variation_type,
            'intensity': data.get('intensity', 0.5),
            'message': f'Video variation ({variation_type}) started'
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/video/evolution/remix', methods=['POST'])
def api_video_evolution_remix():
    """
    Remix multiple videos (interpolate, combine, transition, collage, mashup)
    
    POST Body:
    {
        "asset_ids": ["video_1", "video_2"],
        "remix_type": "interpolate" | "combine" | "transition" | etc.,
        "parameters": {"transition": "dissolve"}
    }
    """
    if not init_video_phase8() or video_evolution is None:
        return jsonify({"error": "Video Phase 8 not available"}), 503
    
    data = request.get_json()
    asset_ids = data.get('asset_ids')
    remix_type = data.get('remix_type')
    
    if not asset_ids or len(asset_ids) < 2 or not remix_type:
        return jsonify({"error": "asset_ids (2+) and remix_type required"}), 400
    
    try:
        result = {
            'status': 'queued',
            'asset_ids': asset_ids,
            'remix_type': remix_type,
            'message': f'Video remix ({remix_type}) started'
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/video/evolution/lineage/<asset_id>')
def api_video_evolution_lineage(asset_id):
    """Get video evolution lineage tree"""
    if not init_video_phase8() or video_evolution is None:
        return jsonify({"error": "Video Phase 8 not available"}), 503
    
    try:
        # Would retrieve from database in production
        lineage = {
            'asset_id': asset_id,
            'generation': 3,
            'ancestors': [
                {'id': 'original_video', 'generation': 1, 'method': 'generate'},
                {'id': 'enhanced_video', 'generation': 2, 'method': 'enhance'}
            ],
            'descendants': []
        }
        
        return jsonify(lineage)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- VIDEO CONSTELLATION ROUTES ---

@app.route('/api/video/constellation/assign', methods=['POST'])
def api_video_constellation_assign():
    """
    Assign video to constellation clusters
    
    POST Body:
    {
        "asset_id": "video_123",
        "metadata": {
            "tags": ["action", "fast-paced"],
            "cuts_per_minute": 35,
            "camera_motion": "dynamic"
        }
    }
    """
    if not init_video_phase8() or video_constellation is None:
        return jsonify({"error": "Video Phase 8 not available"}), 503
    
    data = request.get_json()
    asset_id = data.get('asset_id')
    metadata = data.get('metadata', {})
    
    if not asset_id:
        return jsonify({"error": "asset_id required"}), 400
    
    try:
        clusters = video_constellation.auto_assign_cluster(
            asset_id,
            video_metadata=metadata,
            tags=metadata.get('tags', [])
        )
        
        return jsonify({
            'asset_id': asset_id,
            'clusters': clusters,
            'total_clusters': len(clusters)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/video/constellation/query')
def api_video_constellation_query():
    """
    Query constellation for videos
    
    Query params: genre, pacing, style, tags (comma-separated), limit
    """
    if not init_video_phase8() or video_constellation is None:
        return jsonify({"error": "Video Phase 8 not available"}), 503
    
    try:
        genre = request.args.get('genre')
        pacing = request.args.get('pacing')
        style = request.args.get('style')
        tags = request.args.get('tags', '').split(',') if request.args.get('tags') else None
        limit = int(request.args.get('limit', 10))
        
        results = video_constellation.query_constellation(
            genre=genre,
            pacing=pacing,
            style=style,
            tags=tags,
            limit=limit
        )
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/video/constellation/similar/<asset_id>')
def api_video_constellation_similar(asset_id):
    """Find similar videos by cluster"""
    if not init_video_phase8() or video_constellation is None:
        return jsonify({"error": "Video Phase 8 not available"}), 503
    
    try:
        limit = int(request.args.get('limit', 10))
        threshold = float(request.args.get('threshold', 0.5))
        
        similar = video_constellation.find_similar_videos(
            asset_id,
            limit=limit,
            similarity_threshold=threshold
        )
        
        return jsonify(similar)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/video/constellation/visualize/<asset_id>')
def api_video_constellation_visualize(asset_id):
    """Get D3.js graph data for lineage visualization"""
    if not init_video_phase8() or video_constellation is None:
        return jsonify({"error": "Video Phase 8 not available"}), 503
    
    try:
        graph = video_constellation.visualize_lineage(asset_id)
        return jsonify(graph)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/video/constellation/map')
def api_video_constellation_map():
    """Get complete constellation map with force-directed layout"""
    if not init_video_phase8() or video_constellation is None:
        return jsonify({"error": "Video Phase 8 not available"}), 503
    
    cluster_type = request.args.get('cluster_type', 'all')
    
    try:
        constellation_map = video_constellation.get_constellation_map(cluster_type)
        return jsonify(constellation_map)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/video/constellation/narrative', methods=['POST'])
def api_video_constellation_narrative():
    """
    Group scenes by narrative structure
    
    POST Body:
    {
        "asset_ids": ["scene_1", "scene_2", "scene_3"],
        "structure": "three_act" | "five_act" | "hero_journey"
    }
    """
    if not init_video_phase8() or video_constellation is None:
        return jsonify({"error": "Video Phase 8 not available"}), 503
    
    data = request.get_json()
    asset_ids = data.get('asset_ids')
    structure = data.get('structure', 'three_act')
    
    if not asset_ids:
        return jsonify({"error": "asset_ids required"}), 400
    
    try:
        narrative = video_constellation.group_scenes_by_narrative(
            asset_ids,
            narrative_structure=structure
        )
        
        return jsonify(narrative)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- UTILITY ROUTES ---

@app.route('/api/video/job/<job_id>')
def api_video_job_status(job_id):
    """Get video generation job status"""
    if not init_video_phase8() or video_scene_generator is None:
        return jsonify({"error": "Video Phase 8 not available"}), 503
    
    try:
        status = video_scene_generator.get_job_status(job_id)
        return jsonify(status)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/video/capabilities')
def api_video_capabilities():
    """Get Video Phase 8 capabilities summary"""
    capabilities = {
        'engines': ['runway', 'pika', 'luma', 'stability'],
        'features': {
            'video_generation': True,
            'scene_generation': True,
            'storyboard_conversion': True,
            'evolution': True,
            'variation': True,
            'remix': True,
            'timeline_editing': True,
            'constellation_clustering': True,
            'narrative_structure': True
        },
        'evolution_types': ['enhance', 'extend', 'stabilize', 'upscale', 'color_grade', 'denoise', 'sharpen'],
        'variation_types': ['pacing', 'angle', 'lighting', 'composition', 'mood', 'weather', 'time_of_day'],
        'remix_types': ['interpolate', 'combine', 'transition', 'collage', 'mashup'],
        'camera_motions': 13,
        'subject_motions': 10,
        'constellation_clusters': 18,
        'narrative_structures': ['three_act', 'five_act', 'hero_journey'],
        'version': '8.0.0'
    }
    
    return jsonify(capabilities)


# =============================================================================
# END VIDEO STUDIO PHASE 8 API ROUTES
# =============================================================================


if __name__ == '__main__':
    # Count resources safely
    capsule_count = sum(len(v) for v in capsules_json.values()) if isinstance(capsules_json, dict) else 0
    
    # Handle intelligence_json (might be dict or list)
    if isinstance(intelligence_json, dict):
        engine_count = len(intelligence_json.get("engines", []))
    elif isinstance(intelligence_json, list):
        engine_count = len(intelligence_json)
    else:
        engine_count = 0
    
    agent_count = len(agents_json.get("agents", [])) if isinstance(agents_json, dict) else 0
    # Get councils count from database
    try:
        from database import SessionLocal
        session = SessionLocal()
        council_count = session.query(Council).count()
        session.close()
    except:
        council_count = 0  # Fallback if database not initialized
    tool_count = len(tools_json.get("tools", [])) if isinstance(tools_json, dict) else 0

    print("\n" + "="*80)
    print("👑 CODEX DOMINION MASTER DASHBOARD ULTIMATE - FLASK VERSION")
    print("="*80)
    print("\n🚀 Starting server...")
    print("🌐 URL: http://localhost:5000")
    print("\n✅ System Status: OPERATIONAL")
    print("📊 Resources Loaded:")
    print(f"   • Capsules: {capsule_count}")
    print(f"   • Intelligence Engines: {engine_count}")
    print(f"   • AI Agents: {agent_count}")
    print(f"   • Councils: {council_count}")
    print(f"   • Tools: {tool_count}")
    print("\n🔥 Features:")
    print("   • Complete API Suite (/api/*)")
    print("   • Digital Government APIs (councils, voting, agents)")
    print("   • Graphics Studio Phase 8 (3 engines, evolution, constellation)")
    print("   • Video Studio Phase 8 (4 engines, scene generation, timeline)")
    print("   • Creative Intelligence Engine (7-step workflow)")
    print("   • External Dashboard Links")
    print("   • Real-time Chat Endpoint")
    print("   • Cross-Reference Mapping")
    print("   • No Streamlit Issues - Pure Flask!")
    print("\n🏛️  Digital Government Endpoints:")
    print("   • GET  /api/workflows/pending-review")
    print("   • POST /api/workflows/<id>/vote")
    print("   • GET  /api/agents/leaderboard")
    print("   • GET  /api/agents/<id>/reputation")
    print("   • GET  /api/analytics/agent-performance")
    print("\n🎨 Graphics Studio Phase 8 Endpoints:")
    print("   • POST /api/graphics/generate")
    print("   • GET  /api/graphics/engines")
    print("   • POST /api/graphics/batch")
    print("   • POST /api/graphics/evolution/evolve")
    print("   • GET  /api/graphics/constellation/map")
    print("\n🎬 Video Studio Phase 8 Endpoints:")
    print("   • POST /api/video/generate")
    print("   • GET  /api/video/engines")
    print("   • POST /api/video/storyboard")
    print("   • POST /api/video/evolution/evolve")
    print("   • GET  /api/video/constellation/map")
    print("\n🔥 Creative Intelligence Engine:")
    print("   • GET  /creative/ - Main dashboard interface")
    print("   • POST /creative/api/project/create - Create project")
    print("   • GET  /creative/api/project/<id>/status - Project status")
    print("   • GET  /creative/api/dashboard/<id> - Complete dashboard")
    print("   • GET  /creative/api/projects - List all projects")
    print("\nPress Ctrl+C to stop\n")
    print("="*80 + "\n")

    try:
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=True)
    except Exception as e:
        print(f"\n❌ Flask failed to start: {e}")
        import traceback
        traceback.print_exc()


#!/usr/bin/env python3
"""
Database Migration Script - Video Studio Phase 2
Adds TimelineClip and TimelineMarker tables for timeline engine

Usage:
    python migrate_video_studio.py
"""

import os
import sys
from datetime import datetime

print("="*80)
print("🎬 CODEX DOMINION - VIDEO STUDIO PHASE 2 DATABASE MIGRATION")
print("="*80)
print()

# Check if database module exists
try:
    from database import SessionLocal, engine, Base
    print("✓ Database module loaded")
except ImportError as e:
    print(f"❌ Error: Could not import database module")
    print(f"   {e}")
    print()
    print("💡 Make sure you have:")
    print("   1. database.py in the root directory")
    print("   2. SQLAlchemy installed: pip install sqlalchemy")
    sys.exit(1)

# Import models
try:
    from flask_dashboard import VideoProject, VideoAsset, TimelineClip, TimelineMarker
    print("✓ Video models loaded (Phase 1 + Phase 2)")
except ImportError as e:
    print(f"❌ Error: Could not import video models from flask_dashboard.py")
    print(f"   {e}")
    sys.exit(1)

def check_existing_tables():
    """Check which tables already exist"""
    from sqlalchemy import inspect
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    print()
    print("📊 Current Database Status:")
    print(f"   • Existing tables: {len(existing_tables)}")
    
    video_project_exists = 'video_projects' in existing_tables
    video_asset_exists = 'video_assets' in existing_tables
    timeline_clip_exists = 'timeline_clips' in existing_tables
    timeline_marker_exists = 'timeline_markers' in existing_tables
    
    if video_project_exists:
        print("   ✓ VideoProject table exists (Phase 1)")
    else:
        print("   ➕ VideoProject table will be created")
    
    if video_asset_exists:
        print("   ✓ VideoAsset table exists (Phase 1)")
    else:
        print("   ➕ VideoAsset table will be created")
    
    if timeline_clip_exists:
        print("   ✓ TimelineClip table exists (Phase 2)")
    else:
        print("   ➕ TimelineClip table will be created")
    
    if timeline_marker_exists:
        print("   ✓ TimelineMarker table exists (Phase 2)")
    else:
        print("   ➕ TimelineMarker table will be created")
    
    return (video_project_exists, video_asset_exists, 
            timeline_clip_exists, timeline_marker_exists)

def migrate():
    """Run the migration"""
    print()
    print("🚀 Starting migration...")
    print()
    
    # Check existing tables
    (video_project_exists, video_asset_exists, 
     timeline_clip_exists, timeline_marker_exists) = check_existing_tables()
    
    if all([video_project_exists, video_asset_exists, 
            timeline_clip_exists, timeline_marker_exists]):
        print()
        print("✅ All Video Studio tables already exist (Phase 1 + Phase 2). No migration needed.")
        return True
    
    try:
        # Create only the new tables
        print()
        print("📝 Creating new tables...")
        
        # This will only create tables that don't exist
        Base.metadata.create_all(bind=engine)
        
        print()
        print("✅ Migration completed successfully!")
        print()
        print("🎉 Video Studio database tables:")
        if not video_project_exists:
            print("   ✓ video_projects - Complete video projects")
        if not video_asset_exists:
            print("   ✓ video_assets - Individual clips/audio/overlays")
        if not timeline_clip_exists:
            print("   ✓ timeline_clips - Timeline clip placements (PHASE 2)")
        if not timeline_marker_exists:
            print("   ✓ timeline_markers - Timeline markers (PHASE 2)")
        print()
        print("📋 Phase 2 Features Now Available:")
        print("   • Timeline Engine with multi-track support")
        print("   • Clip placement and trimming")
        print("   • Scene evolution and extension")
        print("   • Timeline markers")
        print()
        
        return True
        
    except Exception as e:
        print()
        print(f"❌ Migration failed: {e}")
        print()
        print("💡 Troubleshooting:")
        print("   1. Check database connection string in database.py")
        print("   2. Ensure database server is running")
        print("   3. Verify you have write permissions")
        return False

def verify_migration():
    """Verify the migration was successful"""
    try:
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print()
        print("🔍 Verification:")
        
        all_good = True
        
        if 'video_projects' in tables:
            columns = [col['name'] for col in inspector.get_columns('video_projects')]
            print(f"   ✓ video_projects table exists ({len(columns)} columns)")
        else:
            print("   ❌ video_projects table NOT found")
            all_good = False
        
        if 'video_assets' in tables:
            columns = [col['name'] for col in inspector.get_columns('video_assets')]
            print(f"   ✓ video_assets table exists ({len(columns)} columns)")
        else:
            print("   ❌ video_assets table NOT found")
            all_good = False
        
        if 'timeline_clips' in tables:
            columns = [col['name'] for col in inspector.get_columns('timeline_clips')]
            print(f"   ✓ timeline_clips table exists ({len(columns)} columns) [PHASE 2]")
        else:
            print("   ❌ timeline_clips table NOT found")
            all_good = False
        
        if 'timeline_markers' in tables:
            columns = [col['name'] for col in inspector.get_columns('timeline_markers')]
            print(f"   ✓ timeline_markers table exists ({len(columns)} columns) [PHASE 2]")
        else:
            print("   ❌ timeline_markers table NOT found")
            all_good = False
        
        print()
        return all_good
        
    except Exception as e:
        print(f"   ❌ Verification failed: {e}")
        return False

if __name__ == "__main__":
    print("⚡ Starting Video Studio database migration...")
    print()
    
    # Run migration
    success = migrate()
    
    if success:
        # Verify migration
        if verify_migration():
            print("="*80)
            print("🔥 THE TIMELINE ENGINE IS READY!")
            print("="*80)
            print()
            print("🎬 Phase 2 Complete:")
            print("   • Timeline engine with multi-track support")
            print("   • Scene evolution and extension")
            print("   • Timeline markers")
            print("   • Real-time clip editing")
            print()
            print("🚀 Access at: /studio/video")
            print()
            sys.exit(0)
        else:
            print("⚠️  Migration completed but verification failed")
            sys.exit(1)
    else:
        sys.exit(1)

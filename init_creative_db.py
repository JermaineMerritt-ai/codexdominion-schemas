"""
Creative Intelligence Engine - Database Initialization
=======================================================

Initializes the database schema for the Creative Intelligence Engine.
Supports PostgreSQL (production) and SQLite (development).

Usage:
    # Initialize with default settings (SQLite)
    python init_creative_db.py
    
    # Initialize with PostgreSQL
    export DATABASE_URL="postgresql://user:password@localhost:5432/creative_db"
    python init_creative_db.py
    
    # Drop existing tables and recreate (CAUTION!)
    python init_creative_db.py --force
    
    # Seed with demo data
    python init_creative_db.py --demo
    
    # Full reset with demo data
    python init_creative_db.py --force --demo
"""

import os
import sys
import argparse
from datetime import datetime, timezone

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, inspect
from creative_intelligence_models import (
    Base, User, CreativeProject, CreativeAsset, CreativeWorkflow,
    ProductionTimeline, ContinuityReport, Deliverable,
    ProjectType, ProjectStatus, AssetType, AssetStatus,
    WorkflowStatus, DeliverableStatus,
    init_database, drop_database, create_demo_user
)

# =============================================================================
# DATABASE CONNECTION
# =============================================================================

def get_engine():
    """Get SQLAlchemy engine from environment or default"""
    database_url = os.getenv('DATABASE_URL', 'sqlite:///creative_intelligence.db')
    
    is_sqlite = database_url.startswith('sqlite')
    
    if is_sqlite:
        from sqlalchemy.pool import StaticPool
        engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=False
        )
    else:
        from sqlalchemy.pool import QueuePool
        engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            echo=False
        )
    
    return engine, is_sqlite, database_url


# =============================================================================
# INITIALIZATION FUNCTIONS
# =============================================================================

def check_existing_tables(engine) -> list:
    """Check for existing tables in the database"""
    inspector = inspect(engine)
    return inspector.get_table_names()


def initialize_schema(engine, force=False):
    """
    Initialize database schema.
    
    Args:
        engine: SQLAlchemy engine
        force: If True, drop existing tables first (DESTRUCTIVE!)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        existing_tables = check_existing_tables(engine)
        
        if existing_tables and not force:
            print(f"⚠️  WARNING: Database already contains {len(existing_tables)} tables")
            print("   Tables found:", ', '.join(existing_tables))
            print("\n   Use --force flag to drop and recreate tables (DESTRUCTIVE!)")
            return False
        
        if force and existing_tables:
            print(f"🗑️  Dropping {len(existing_tables)} existing tables...")
            drop_database(engine)
            print("   ✅ Tables dropped")
        
        print("📦 Creating database schema...")
        init_database(engine)
        
        # Verify tables were created
        new_tables = check_existing_tables(engine)
        print(f"   ✅ Created {len(new_tables)} tables:")
        for table in sorted(new_tables):
            print(f"      - {table}")
        
        return True
    
    except Exception as e:
        print(f"   ❌ Schema initialization failed: {e}")
        return False


def seed_demo_data(engine):
    """
    Seed database with demo data for testing.
    
    Args:
        engine: SQLAlchemy engine
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=engine)
        session = Session()
        
        print("🌱 Seeding demo data...")
        
        # Create demo user
        user = create_demo_user(session)
        print(f"   ✅ Created user: {user.username}")
        
        # Create demo project
        project = CreativeProject(
            id='pic_project_demo001',
            project_type=ProjectType.MARKETING_CAMPAIGN,
            status=ProjectStatus.INTERPRETED,
            title='Demo Marketing Campaign',
            description='A comprehensive marketing campaign for product launch',
            complexity='moderate',
            required_mediums=['video', 'audio', 'graphics'],
            asset_requirements={
                'video': {'count': 1, 'duration': 60},
                'audio': {'count': 2, 'duration': 120},
                'graphics': {'count': 5}
            },
            goals=['increase_brand_awareness', 'drive_conversions'],
            constraints={'budget': 10000, 'deadline': '2025-01-31'},
            project_metadata={'campaign_name': 'Spring Launch 2025'},
            creator_id=user.id
        )
        session.add(project)
        session.commit()
        print(f"   ✅ Created project: {project.title}")
        
        # Create demo assets
        assets = [
            CreativeAsset(
                id='asset_video_001',
                project_id=project.id,
                asset_name='Hero Video',
                asset_type=AssetType.VIDEO,
                status=AssetStatus.READY,
                file_path='/assets/hero_video.mp4',
                file_format='mp4',
                file_size_mb=45.8,
                duration_seconds=60.0,
                resolution='1920x1080',
                owner_module='MMOE',
                tags=['hero', 'main_content'],
                asset_metadata={'codec': 'h264', 'fps': 30}
            ),
            CreativeAsset(
                id='asset_audio_001',
                project_id=project.id,
                asset_name='Background Music',
                asset_type=AssetType.MUSIC,
                status=AssetStatus.READY,
                file_path='/assets/background_music.mp3',
                file_format='mp3',
                file_size_mb=8.5,
                duration_seconds=120.0,
                owner_module='AMME',
                tags=['background', 'ambient'],
                asset_metadata={'bitrate': '320kbps', 'genre': 'corporate'}
            ),
            CreativeAsset(
                id='asset_graphics_001',
                project_id=project.id,
                asset_name='Brand Logo',
                asset_type=AssetType.GRAPHICS,
                status=AssetStatus.READY,
                file_path='/assets/logo.png',
                file_format='png',
                file_size_mb=2.1,
                resolution='2048x2048',
                owner_module='VTE',
                tags=['branding', 'overlay'],
                asset_metadata={'has_transparency': True}
            )
        ]
        
        for asset in assets:
            session.add(asset)
            project.assets.append(asset)
        
        session.commit()
        print(f"   ✅ Created {len(assets)} assets")
        
        # Create demo workflow
        workflow = CreativeWorkflow(
            project_id=project.id,
            user_id=user.id,
            status=WorkflowStatus.COMPLETE,
            current_step='DASHBOARD',
            completed_steps=['PIC', 'CRE', 'MMOE', 'ADG', 'CCS', 'OAE', 'DASHBOARD'],
            execution_log=[
                {'step': 'PIC', 'timestamp': datetime.now(timezone.utc).isoformat(), 'status': 'success'},
                {'step': 'CRE', 'timestamp': datetime.now(timezone.utc).isoformat(), 'status': 'success'},
                {'step': 'MMOE', 'timestamp': datetime.now(timezone.utc).isoformat(), 'status': 'success'},
            ],
            pic_output={'project_type': 'marketing_campaign', 'complexity': 'moderate'},
            cre_output={'theme': 'professional', 'style': 'modern'},
            mmoe_output={'timeline': {'total_duration': 60, 'clips': 3}},
            total_duration_seconds=8.5
        )
        session.add(workflow)
        session.commit()
        print(f"   ✅ Created workflow execution record")
        
        # Create demo continuity report
        report = ContinuityReport(
            project_id=project.id,
            report_id='cc_report_demo001',
            overall_score=0.92,
            critical_violations=0,
            ready_for_assembly=True,
            module_scores={'PIC': 0.95, 'CRE': 0.90, 'MMOE': 0.91},
            violations=[],
            recommendations=['Consider adding more visual variety']
        )
        session.add(report)
        session.commit()
        print(f"   ✅ Created continuity report")
        
        # Create demo deliverables
        deliverables = [
            Deliverable(
                project_id=project.id,
                deliverable_id='del_youtube_001',
                platform='youtube',
                deliverable_type='video',
                status=DeliverableStatus.READY,
                file_path='/deliverables/youtube_export.mp4',
                file_format='mp4',
                file_size_mb=98.5,
                resolution='1920x1080',
                duration_seconds=60.0,
                codec='h264',
                bitrate='8000kbps',
                quality_preset='high',
                deliverable_metadata={'thumbnail': '/thumbnails/youtube.jpg'}
            ),
            Deliverable(
                project_id=project.id,
                deliverable_id='del_instagram_001',
                platform='instagram',
                deliverable_type='social_post',
                status=DeliverableStatus.READY,
                file_path='/deliverables/instagram_post.mp4',
                file_format='mp4',
                file_size_mb=15.2,
                resolution='1080x1920',
                duration_seconds=15.0,
                codec='h264',
                bitrate='5000kbps',
                quality_preset='high',
                deliverable_metadata={'caption': 'Check out our new product!'}
            )
        ]
        
        for deliverable in deliverables:
            session.add(deliverable)
        
        session.commit()
        print(f"   ✅ Created {len(deliverables)} deliverables")
        
        print("\n✅ Demo data seeded successfully!")
        print(f"\n   📊 Database Summary:")
        print(f"      Users: 1")
        print(f"      Projects: 1")
        print(f"      Assets: {len(assets)}")
        print(f"      Workflows: 1")
        print(f"      Continuity Reports: 1")
        print(f"      Deliverables: {len(deliverables)}")
        
        session.close()
        return True
    
    except Exception as e:
        print(f"   ❌ Demo data seeding failed: {e}")
        import traceback
        traceback.print_exc()
        return False


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description='Initialize Creative Intelligence Engine database'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Drop existing tables and recreate (DESTRUCTIVE!)'
    )
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Seed database with demo data'
    )
    parser.add_argument(
        '--database-url',
        type=str,
        help='Database URL (overrides DATABASE_URL env var)'
    )
    
    args = parser.parse_args()
    
    # Override DATABASE_URL if provided
    if args.database_url:
        os.environ['DATABASE_URL'] = args.database_url
    
    print("🔥 CREATIVE INTELLIGENCE ENGINE - DATABASE INITIALIZATION 🔥")
    print("=" * 80)
    
    # Get database engine
    engine, is_sqlite, database_url = get_engine()
    
    # Display connection info (hide credentials)
    display_url = database_url.split('@')[-1] if '@' in database_url else database_url
    print(f"\n📍 Database: {display_url}")
    print(f"   Type: {'SQLite' if is_sqlite else 'PostgreSQL/MySQL'}")
    
    # Initialize schema
    print("\n" + "=" * 80)
    if not initialize_schema(engine, force=args.force):
        if not args.force:
            print("\n💡 TIP: Use --force flag to recreate tables")
        sys.exit(1)
    
    # Seed demo data if requested
    if args.demo:
        print("\n" + "=" * 80)
        if not seed_demo_data(engine):
            sys.exit(1)
    
    print("\n" + "=" * 80)
    print("🔥 Database Initialization Complete! 👑")
    print("=" * 80)
    
    if not args.demo:
        print("\n💡 TIP: Use --demo flag to seed with sample data for testing")


if __name__ == '__main__':
    main()

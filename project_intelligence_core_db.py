"""
🔥 DATABASE-INTEGRATED PROJECT INTELLIGENCE CORE 🔥
===================================================
Wraps the original PIC with database persistence using SQLAlchemy models.

All projects, assets, and execution plans are now stored in the database
instead of in-memory dictionaries.

Usage:
    from project_intelligence_core_db import ProjectIntelligenceCoreDB
    
    pic = ProjectIntelligenceCoreDB()
    
    # Interpret project (saves to database automatically)
    project = pic.interpret_project(
        brief="Create a product launch campaign with hero video...",
        project_type=ProjectType.PRODUCT_LAUNCH
    )
    
    # Retrieve project from database
    project = pic.get_project(project_id)
    
    # List all projects
    projects = pic.list_projects(status="interpreted")
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from contextlib import contextmanager

from sqlalchemy.orm import Session

# Import original PIC classes
from project_intelligence_core import (
    ProjectIntelligenceCore,
    ProjectType,
    ProjectComplexity,
    MediumRequirement
)

# Import database models
from creative_intelligence_models import (
    CreativeProject,
    ProjectType as DBProjectType,
    ProjectStatus as DBProjectStatus
)

# Import database session management
from database import SessionLocal


class ProjectIntelligenceCoreDB:
    """
    Database-integrated wrapper for Project Intelligence Core.
    
    This class wraps the original PIC and adds database persistence.
    All projects are stored in PostgreSQL/SQLite instead of in-memory.
    
    Features:
    - Automatic database persistence
    - Multi-user support
    - Version history
    - Query capabilities
    - Transaction management
    """
    
    def __init__(self, user_id: Optional[str] = None, config_path: Optional[str] = None):
        """
        Initialize database-integrated PIC
        
        Args:
            user_id: User creating/accessing projects (default: 'system')
            config_path: Optional config file path
        """
        self.logger = logging.getLogger(__name__)
        self.user_id = user_id or 'system'
        
        # Initialize original PIC for intelligence operations
        self.pic = ProjectIntelligenceCore(config_path)
        
        self.logger.info("🔥 Database-Integrated PIC initialized! 👑")
    
    @contextmanager
    def _get_session(self):
        """Context manager for database sessions"""
        session = SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def _convert_project_type(self, project_type: ProjectType) -> DBProjectType:
        """Convert PIC ProjectType to database ProjectType"""
        type_mapping = {
            ProjectType.MARKETING_CAMPAIGN: DBProjectType.MARKETING_CAMPAIGN,
            ProjectType.PRODUCT_LAUNCH: DBProjectType.MARKETING_CAMPAIGN,  # Map to closest
            ProjectType.SOCIAL_CONTENT: DBProjectType.SOCIAL_MEDIA,
            ProjectType.BRAND_IDENTITY: DBProjectType.CORPORATE,
            ProjectType.VIDEO_SERIES: DBProjectType.DOCUMENTARY,
            ProjectType.PODCAST_SERIES: DBProjectType.PODCAST,
            ProjectType.EDUCATIONAL_CONTENT: DBProjectType.EDUCATIONAL,
            ProjectType.ENTERTAINMENT: DBProjectType.ENTERTAINMENT,
            ProjectType.CUSTOM: DBProjectType.OTHER
        }
        return type_mapping.get(project_type, DBProjectType.OTHER)
    
    def interpret_project(
        self,
        brief: str,
        project_type: Optional[ProjectType] = None,
        metadata: Optional[Dict[str, Any]] = None,
        title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Interpret a creative project brief and save to database.
        
        Args:
            brief: Natural language project description
            project_type: Type of project (auto-detected if not provided)
            metadata: Additional project metadata
            title: Optional project title (extracted from brief if not provided)
        
        Returns:
            Project dictionary with database ID
        """
        # Use original PIC to interpret the project
        pic_project = self.pic.interpret_project(brief, project_type, metadata)
        
        # Extract title from brief if not provided
        if not title:
            title = brief[:100] + "..." if len(brief) > 100 else brief
        
        # Convert to database model
        db_project_type = self._convert_project_type(
            ProjectType(pic_project['type'])
        )
        
        # Create database record
        with self._get_session() as session:
            db_project = CreativeProject(
                id=pic_project['id'],
                project_type=db_project_type,
                status=DBProjectStatus.INTERPRETED,
                title=title,
                description=brief,
                complexity=pic_project['complexity'],
                required_mediums=pic_project['required_mediums'],
                asset_requirements=pic_project['asset_requirements'],
                timeline_hints=pic_project['timeline_hints'],
                goals=pic_project['goals'],
                constraints=pic_project['constraints'],
                project_metadata=pic_project['metadata'],
                creator_id=self.user_id
            )
            
            session.add(db_project)
            session.commit()
            
            self.logger.info(
                f"🔥 Saved project {db_project.id} to database "
                f"({db_project.project_type.value}, {db_project.complexity})"
            )
            
            # Return combined dictionary
            result = pic_project.copy()
            result['database_id'] = db_project.id
            result['title'] = db_project.title
            result['creator_id'] = db_project.creator_id
            
            return result
    
    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a project from the database.
        
        Args:
            project_id: Project ID (pic_project_xxxxx)
        
        Returns:
            Project dictionary or None if not found
        """
        with self._get_session() as session:
            db_project = session.query(CreativeProject).filter_by(id=project_id).first()
            
            if not db_project:
                self.logger.warning(f"⚠️ Project {project_id} not found in database")
                return None
            
            return db_project.to_dict()
    
    def list_projects(
        self,
        status: Optional[str] = None,
        project_type: Optional[str] = None,
        creator_id: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        List projects from database with optional filters.
        
        Args:
            status: Filter by status (interpreted, in_production, complete, etc.)
            project_type: Filter by project type
            creator_id: Filter by creator user ID
            limit: Maximum number of projects to return
        
        Returns:
            List of project dictionaries
        """
        with self._get_session() as session:
            query = session.query(CreativeProject)
            
            # Apply filters
            if status:
                query = query.filter(CreativeProject.status == DBProjectStatus[status.upper()])
            if project_type:
                query = query.filter(CreativeProject.project_type == DBProjectType[project_type.upper()])
            if creator_id:
                query = query.filter(CreativeProject.creator_id == creator_id)
            
            # Order by created date (newest first) and limit
            query = query.order_by(CreativeProject.created_at.desc()).limit(limit)
            
            projects = query.all()
            
            self.logger.info(f"📊 Retrieved {len(projects)} projects from database")
            
            return [p.to_dict() for p in projects]
    
    def update_project_status(
        self,
        project_id: str,
        status: str,
        metadata_update: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Update project status in database.
        
        Args:
            project_id: Project ID
            status: New status (interpreted, in_production, complete, etc.)
            metadata_update: Optional metadata updates
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with self._get_session() as session:
                db_project = session.query(CreativeProject).filter_by(id=project_id).first()
                
                if not db_project:
                    self.logger.error(f"❌ Project {project_id} not found")
                    return False
                
                # Update status
                db_project.status = DBProjectStatus[status.upper()]
                
                # Update metadata if provided
                if metadata_update:
                    if db_project.project_metadata:
                        db_project.project_metadata.update(metadata_update)
                    else:
                        db_project.project_metadata = metadata_update
                
                # Update timestamp
                db_project.updated_at = datetime.now(timezone.utc)
                
                # Mark completed if final status
                if status.upper() == 'COMPLETE':
                    db_project.completed_at = datetime.now(timezone.utc)
                
                session.commit()
                
                self.logger.info(f"✅ Updated project {project_id} status to {status}")
                return True
        
        except Exception as e:
            self.logger.error(f"❌ Failed to update project status: {e}")
            return False
    
    def delete_project(self, project_id: str) -> bool:
        """
        Delete a project from the database.
        
        Args:
            project_id: Project ID
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with self._get_session() as session:
                db_project = session.query(CreativeProject).filter_by(id=project_id).first()
                
                if not db_project:
                    self.logger.error(f"❌ Project {project_id} not found")
                    return False
                
                session.delete(db_project)
                session.commit()
                
                self.logger.info(f"🗑️ Deleted project {project_id} from database")
                return True
        
        except Exception as e:
            self.logger.error(f"❌ Failed to delete project: {e}")
            return False
    
    def get_project_stats(self) -> Dict[str, Any]:
        """
        Get database statistics for projects.
        
        Returns:
            dict: Statistics including total projects, by status, by type
        """
        with self._get_session() as session:
            total_projects = session.query(CreativeProject).count()
            
            # Count by status
            status_counts = {}
            for status in DBProjectStatus:
                count = session.query(CreativeProject).filter(
                    CreativeProject.status == status
                ).count()
                if count > 0:
                    status_counts[status.value] = count
            
            # Count by type
            type_counts = {}
            for ptype in DBProjectType:
                count = session.query(CreativeProject).filter(
                    CreativeProject.project_type == ptype
                ).count()
                if count > 0:
                    type_counts[ptype.value] = count
            
            return {
                'total_projects': total_projects,
                'by_status': status_counts,
                'by_type': type_counts
            }


# =============================================================================
# DEMO / TEST
# =============================================================================

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("🔥 DATABASE-INTEGRATED PIC - DEMO 🔥")
    print("=" * 80)
    
    # Initialize
    pic = ProjectIntelligenceCoreDB(user_id='demo_user')
    
    # Test 1: Interpret and save project
    print("\n TEST 1: Interpret Project")
    print("-" * 80)
    project = pic.interpret_project(
        brief="Create a holiday marketing campaign with Instagram graphics, "
              "Facebook ads, and a 30-second promotional video with background music",
        project_type=ProjectType.MARKETING_CAMPAIGN,
        title="Holiday Marketing Campaign 2025"
    )
    print(f"✅ Created project: {project['id']}")
    print(f"   Type: {project['type']}")
    print(f"   Complexity: {project['complexity']}")
    print(f"   Mediums: {', '.join(project['required_mediums'])}")
    print(f"   Assets: {len(project['asset_requirements'])}")
    
    # Test 2: Retrieve project
    print("\n🔍 TEST 2: Retrieve Project")
    print("-" * 80)
    retrieved = pic.get_project(project['id'])
    print(f"✅ Retrieved: {retrieved['title']}")
    print(f"   Status: {retrieved['status']}")
    
    # Test 3: Update status
    print("\n📝 TEST 3: Update Project Status")
    print("-" * 80)
    pic.update_project_status(
        project['id'],
        'in_production',
        metadata_update={'phase': 'asset_generation'}
    )
    print(f"✅ Updated project status to 'in_production'")
    
    # Test 4: List projects
    print("\n📊 TEST 4: List Projects")
    print("-" * 80)
    projects = pic.list_projects(limit=10)
    print(f"✅ Found {len(projects)} projects:")
    for p in projects:
        print(f"   - {p['title']} ({p['status']})")
    
    # Test 5: Get statistics
    print("\n📈 TEST 5: Project Statistics")
    print("-" * 80)
    stats = pic.get_project_stats()
    print(f"✅ Total projects: {stats['total_projects']}")
    print(f"   By status: {stats['by_status']}")
    print(f"   By type: {stats['by_type']}")
    
    print("\n" + "=" * 80)
    print("🔥 Database-Integrated PIC Operational! 👑")

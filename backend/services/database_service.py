"""
Database service for PostgreSQL operations
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional
from datetime import datetime


class DatabaseService:
    """PostgreSQL database service"""

    def __init__(self):
        self.connection_string = os.getenv('DATABASE_URL')
        if not self.connection_string:
            # Construct from individual components
            host = os.getenv('POSTGRES_HOST')
            port = os.getenv('POSTGRES_PORT', '5432')
            db = os.getenv('POSTGRES_DB')
            user = os.getenv('POSTGRES_USER')
            password = os.getenv('POSTGRES_PASSWORD')

            if all([host, db, user, password]):
                self.connection_string = (
                    f"host={host} port={port} dbname={db} "
                    f"user={user} password={password} sslmode=require"
                )

        self._conn = None

    def get_connection(self):
        """Get database connection"""
        if not self._conn or self._conn.closed:
            if self.connection_string:
                self._conn = psycopg2.connect(self.connection_string)
        return self._conn

    def close(self):
        """Close database connection"""
        if self._conn and not self._conn.closed:
            self._conn.close()

    def get_annotations(
        self,
        cycle: Optional[str] = None,
        engine: Optional[str] = None,
        role: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Fetch annotations from capsules table

        Args:
            cycle: Time cycle filter (daily, seasonal, epochal, millennial)
            engine: Filter by engine/model
            role: Filter by user role
            limit: Maximum number of results

        Returns:
            List of annotation dictionaries
        """
        try:
            conn = self.get_connection()
            if not conn:
                return []

            cursor = conn.cursor(cursor_factory=RealDictCursor)

            # Base query
            query = """
                SELECT
                    id,
                    title,
                    content,
                    capsule_type as type,
                    engine,
                    user_role as role,
                    username as user,
                    tags,
                    metadata,
                    created_at as timestamp,
                    updated_at
                FROM capsules
                WHERE 1=1
            """
            params = []

            # Apply filters
            if cycle:
                cycle_days = {
                    'daily': 1,
                    'seasonal': 7,
                    'epochal': 30,
                    'millennial': 90
                }
                if cycle in cycle_days:
                    query += " AND created_at >= NOW() - INTERVAL '%s days'"
                    params.append(cycle_days[cycle])

            if engine:
                query += " AND engine = %s"
                params.append(engine)

            if role:
                query += " AND user_role = %s"
                params.append(role)

            query += " ORDER BY created_at DESC LIMIT %s"
            params.append(limit)

            cursor.execute(query, params)
            results = cursor.fetchall()

            # Convert to list of dicts
            annotations = []
            for row in results:
                annotation = dict(row)
                # Convert timestamp to ISO format
                if annotation.get('timestamp'):
                    annotation['timestamp'] = annotation['timestamp'].isoformat() + 'Z'
                if annotation.get('updated_at'):
                    annotation['updated_at'] = annotation['updated_at'].isoformat() + 'Z'
                # Ensure tags is a list
                if not annotation.get('tags'):
                    annotation['tags'] = []
                annotations.append(annotation)

            cursor.close()
            return annotations

        except Exception as e:
            print(f"Database error: {e}")
            return []

    def get_capsule_by_id(self, capsule_id: str) -> Optional[Dict[str, Any]]:
        """Get a single capsule by ID"""
        try:
            conn = self.get_connection()
            if not conn:
                return None

            cursor = conn.cursor(cursor_factory=RealDictCursor)

            query = """
                SELECT
                    id,
                    title,
                    content,
                    capsule_type as type,
                    engine,
                    user_role as role,
                    username as user,
                    tags,
                    metadata,
                    created_at as timestamp,
                    updated_at
                FROM capsules
                WHERE id = %s
            """

            cursor.execute(query, (capsule_id,))
            row = cursor.fetchone()

            if row:
                capsule = dict(row)
                if capsule.get('timestamp'):
                    capsule['timestamp'] = capsule['timestamp'].isoformat() + 'Z'
                if capsule.get('updated_at'):
                    capsule['updated_at'] = capsule['updated_at'].isoformat() + 'Z'
                if not capsule.get('tags'):
                    capsule['tags'] = []
                cursor.close()
                return capsule

            cursor.close()
            return None

        except Exception as e:
            print(f"Database error: {e}")
            return None

    def create_capsule(self, capsule_data: Dict[str, Any]) -> Optional[str]:
        """Create a new capsule"""
        try:
            conn = self.get_connection()
            if not conn:
                return None

            cursor = conn.cursor()

            query = """
                INSERT INTO capsules (
                    title,
                    content,
                    capsule_type,
                    engine,
                    user_role,
                    username,
                    tags,
                    metadata
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """

            cursor.execute(query, (
                capsule_data.get('title'),
                capsule_data.get('content'),
                capsule_data.get('type', 'annotation'),
                capsule_data.get('engine'),
                capsule_data.get('role', 'observer'),
                capsule_data.get('user', 'Unknown'),
                capsule_data.get('tags', []),
                capsule_data.get('metadata', {})
            ))

            capsule_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()

            return str(capsule_id)

        except Exception as e:
            print(f"Database error: {e}")
            if conn:
                conn.rollback()
            return None

    def get_capsule_stats(self) -> Dict[str, Any]:
        """Get statistics about capsules"""
        try:
            conn = self.get_connection()
            if not conn:
                return {}

            cursor = conn.cursor(cursor_factory=RealDictCursor)

            query = """
                SELECT
                    COUNT(*) as total_capsules,
                    COUNT(DISTINCT engine) as unique_engines,
                    COUNT(DISTINCT user_role) as unique_roles,
                    MAX(created_at) as last_capsule_time
                FROM capsules
            """

            cursor.execute(query)
            stats = dict(cursor.fetchone())

            if stats.get('last_capsule_time'):
                stats['last_capsule_time'] = stats['last_capsule_time'].isoformat() + 'Z'

            cursor.close()
            return stats

        except Exception as e:
            print(f"Database error: {e}")
            return {}


# Singleton instance
_db_service = None


def get_database_service() -> DatabaseService:
    """Get or create database service instance"""
    global _db_service
    if _db_service is None:
        _db_service = DatabaseService()
    return _db_service

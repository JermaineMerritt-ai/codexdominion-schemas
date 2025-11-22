# codex_capsules/database.py
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from typing import Dict, List, Optional

class CapsuleDatabase:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL", "postgresql://localhost:5432/codex_dominion")
    
    def get_connection(self):
        return psycopg2.connect(self.db_url, cursor_factory=RealDictCursor)
    
    def register_capsule(self, capsule_data: Dict) -> Dict:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO capsules (slug, title, kind, mode, version, status, entrypoint, schedule)
                    VALUES (%(slug)s, %(title)s, %(kind)s, %(mode)s, %(version)s, %(status)s, %(entrypoint)s, %(schedule)s)
                    ON CONFLICT (slug) DO UPDATE SET
                        title = EXCLUDED.title,
                        kind = EXCLUDED.kind,
                        mode = EXCLUDED.mode,
                        version = EXCLUDED.version,
                        status = EXCLUDED.status,
                        entrypoint = EXCLUDED.entrypoint,
                        schedule = EXCLUDED.schedule,
                        updated_at = CURRENT_TIMESTAMP
                    RETURNING *
                """, capsule_data)
                return dict(cursor.fetchone())
    
    def list_capsules(self) -> List[Dict]:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM capsules ORDER BY created_at DESC")
                return [dict(row) for row in cursor.fetchall()]
    
    def record_run(self, run_data: Dict) -> Dict:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                # Check if capsule exists
                cursor.execute("SELECT id FROM capsules WHERE slug = %s", (run_data['capsule_slug'],))
                capsule = cursor.fetchone()
                if not capsule:
                    raise ValueError("Capsule not found")
                
                # Record the run
                cursor.execute("""
                    INSERT INTO capsule_runs (capsule_id, actor, status, artifact_uri, checksum)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING *
                """, (capsule['id'], run_data['actor'], run_data['status'], 
                     run_data.get('artifact_uri'), run_data.get('checksum')))
                return dict(cursor.fetchone())
    
    def list_runs(self, capsule_slug: Optional[str] = None) -> List[Dict]:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                if capsule_slug:
                    cursor.execute("""
                        SELECT cr.*, c.slug as capsule_slug, c.title as capsule_title
                        FROM capsule_runs cr
                        JOIN capsules c ON cr.capsule_id = c.id
                        WHERE c.slug = %s
                        ORDER BY cr.started_at DESC
                    """, (capsule_slug,))
                else:
                    cursor.execute("""
                        SELECT cr.*, c.slug as capsule_slug, c.title as capsule_title
                        FROM capsule_runs cr
                        JOIN capsules c ON cr.capsule_id = c.id
                        ORDER BY cr.started_at DESC
                    """)
                return [dict(row) for row in cursor.fetchall()]
    
    def get_capsule_performance(self) -> List[Dict]:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM capsule_performance ORDER BY success_rate DESC")
                return [dict(row) for row in cursor.fetchall()]
    
    def get_scheduled_capsules(self) -> List[Dict]:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM scheduled_capsules ORDER BY next_run")
                return [dict(row) for row in cursor.fetchall()]
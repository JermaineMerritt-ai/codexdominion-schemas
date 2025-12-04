"""
Database integration for Codex Capsules system
Handles recording capsule executions and managing database operations
"""

import datetime
import hashlib
import json
import os
from typing import Any, Dict, List, Optional

import sqlalchemy
from google.cloud.sql.connector import Connector


class CapsuleDatabase:
    """Database integration for capsule execution tracking"""

    def __init__(self):
        self.instance_connection_name = "codex-dominion-prod:us-central1:codex-ledger"
        self.database_name = "codex"
        self.username = "postgres"
        self.password = os.getenv("DB_PASSWORD", "codex_sovereign_key_2024")
        self.pool = None

    def get_connection(self):
        """Get database connection using Cloud SQL Python Connector"""
        if not self.pool:
            connector = Connector()

            def getconn():
                conn = connector.connect(
                    self.instance_connection_name,
                    "pg8000",
                    user=self.username,
                    password=self.password,
                    db=self.database_name,
                )
                return conn

            self.pool = sqlalchemy.create_engine(
                "postgresql+pg8000://",
                creator=getconn,
            )

        return self.pool.connect()

    def record_capsule_run(
        self,
        capsule_slug: str,
        actor: str,
        artifact_uri: str,
        checksum: str,
        status: str = "success",
        execution_data: Optional[Dict] = None,
    ) -> int:
        """
        Record a capsule run in the database

        Args:
            capsule_slug: The slug of the executed capsule
            actor: Who/what triggered the execution (e.g., 'system_scheduler', 'manual')
            artifact_uri: URI where the execution artifact is stored
            checksum: SHA256 checksum of the execution data for integrity
            status: Execution status ('success', 'error', 'running')
            execution_data: Optional execution metadata

        Returns:
            int: The ID of the created run record
        """

        with self.get_connection() as conn:
            result = conn.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO capsule_runs
                    (capsule_slug, actor, artifact_uri, checksum, status, execution_data)
                    VALUES (:capsule_slug, :actor, :artifact_uri, :checksum, :status, :execution_data)
                    RETURNING id
                """
                ),
                {
                    "capsule_slug": capsule_slug,
                    "actor": actor,
                    "artifact_uri": artifact_uri,
                    "checksum": checksum,
                    "status": status,
                    "execution_data": (
                        json.dumps(execution_data) if execution_data else None
                    ),
                },
            )

            run_id = result.fetchone()[0]
            conn.commit()

            print(f"📝 Recorded capsule run: {capsule_slug} (ID: {run_id})")
            return run_id

    def get_capsule_runs(
        self, capsule_slug: Optional[str] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get capsule run history

        Args:
            capsule_slug: Optional filter by specific capsule
            limit: Maximum number of runs to return

        Returns:
            List of run records
        """

        with self.get_connection() as conn:
            if capsule_slug:
                query = """
                    SELECT id, capsule_slug, actor, status, artifact_uri, checksum,
                           executed_at, execution_data
                    FROM capsule_runs
                    WHERE capsule_slug = :capsule_slug
                    ORDER BY executed_at DESC
                    LIMIT :limit
                """
                params = {"capsule_slug": capsule_slug, "limit": limit}
            else:
                query = """
                    SELECT id, capsule_slug, actor, status, artifact_uri, checksum,
                           executed_at, execution_data
                    FROM capsule_runs
                    ORDER BY executed_at DESC
                    LIMIT :limit
                """
                params = {"limit": limit}

            result = conn.execute(sqlalchemy.text(query), params)

            runs = []
            for row in result:
                run_data = {
                    "id": row[0],
                    "capsule_slug": row[1],
                    "actor": row[2],
                    "status": row[3],
                    "artifact_uri": row[4],
                    "checksum": row[5],
                    "executed_at": row[6].isoformat() if row[6] else None,
                    "execution_data": json.loads(row[7]) if row[7] else None,
                }
                runs.append(run_data)

            return runs

    def get_capsule_stats(self) -> Dict[str, Any]:
        """Get overall capsule execution statistics"""

        with self.get_connection() as conn:
            # Get total runs per capsule
            result = conn.execute(
                sqlalchemy.text(
                    """
                SELECT
                    capsule_slug,
                    COUNT(*) as total_runs,
                    COUNT(CASE WHEN status = 'success' THEN 1 END) as successful_runs,
                    COUNT(CASE WHEN status = 'error' THEN 1 END) as failed_runs,
                    MAX(executed_at) as last_execution
                FROM capsule_runs
                GROUP BY capsule_slug
                ORDER BY last_execution DESC
            """
                )
            )

            capsule_stats = {}
            for row in result:
                capsule_stats[row[0]] = {
                    "total_runs": row[1],
                    "successful_runs": row[2],
                    "failed_runs": row[3],
                    "success_rate": (row[2] / row[1] * 100) if row[1] > 0 else 0,
                    "last_execution": row[4].isoformat() if row[4] else None,
                }

            # Get overall stats
            overall_result = conn.execute(
                sqlalchemy.text(
                    """
                SELECT
                    COUNT(*) as total_runs,
                    COUNT(DISTINCT capsule_slug) as active_capsules,
                    COUNT(CASE WHEN status = 'success' THEN 1 END) as successful_runs,
                    AVG(CASE WHEN status = 'success' THEN 1.0 ELSE 0.0 END) * 100 as overall_success_rate
                FROM capsule_runs
            """
                )
            )

            overall = overall_result.fetchone()

            return {
                "overall": {
                    "total_runs": overall[0],
                    "active_capsules": overall[1],
                    "successful_runs": overall[2],
                    "overall_success_rate": round(overall[3], 1) if overall[3] else 0,
                },
                "by_capsule": capsule_stats,
            }

    def verify_artifact_integrity(self, run_id: int, current_checksum: str) -> bool:
        """Verify artifact integrity against stored checksum"""

        with self.get_connection() as conn:
            result = conn.execute(
                sqlalchemy.text("SELECT checksum FROM capsule_runs WHERE id = :run_id"),
                {"run_id": run_id},
            )

            row = result.fetchone()
            if row:
                stored_checksum = row[0]
                return stored_checksum == current_checksum

            return False


def calculate_execution_checksum(execution_data: Dict[str, Any]) -> str:
    """Calculate SHA256 checksum of execution data for integrity verification"""

    # Convert to JSON with sorted keys for consistent hashing
    json_str = json.dumps(execution_data, sort_keys=True, default=str)

    # Calculate SHA256 hash
    hash_object = hashlib.sha256(json_str.encode("utf-8"))
    return hash_object.hexdigest()


def record_capsule_run(
    db: CapsuleDatabase,
    capsule_slug: str,
    actor: str,
    artifact_uri: str,
    checksum: str,
    status: str = "success",
    execution_data: Optional[Dict] = None,
) -> int:
    """
    Convenience function to record a capsule run

    Args:
        db: CapsuleDatabase instance
        capsule_slug: The slug of the executed capsule
        actor: Who/what triggered the execution
        artifact_uri: URI where the execution artifact is stored
        checksum: SHA256 checksum of the execution data
        status: Execution status (default: 'success')
        execution_data: Optional execution metadata

    Returns:
        int: The ID of the created run record
    """
    return db.record_capsule_run(
        capsule_slug, actor, artifact_uri, checksum, status, execution_data
    )


# Global database instance
capsule_db = CapsuleDatabase()

if __name__ == "__main__":
    # Test database integration
    print("🗄️ Testing Database Integration...")

    try:
        # Test connection
        with capsule_db.get_connection() as conn:
            result = conn.execute(sqlalchemy.text("SELECT COUNT(*) FROM capsules"))
            capsule_count = result.fetchone()[0]
            print(f"✅ Database connected: {capsule_count} capsules in system")

        # Test recording a run
        test_execution_data = {
            "test_run": True,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "metrics": {"processed": 100, "errors": 0},
        }

        checksum = calculate_execution_checksum(test_execution_data)

        run_id = record_capsule_run(
            capsule_db,
            "signals-daily",
            "test_integration",
            "file://test_artifact.json",
            checksum,
            execution_data=test_execution_data,
        )

        print(f"✅ Test run recorded with ID: {run_id}")

        # Test getting runs
        runs = capsule_db.get_capsule_runs("signals-daily", limit=3)
        print(f"✅ Retrieved {len(runs)} recent runs for signals-daily")

        # Test getting stats
        stats = capsule_db.get_capsule_stats()
        print(
            f"✅ System stats: {stats['overall']['total_runs']} total runs, {stats['overall']['overall_success_rate']}% success rate"
        )

        print("\n🎉 Database integration test completed successfully!")

    except Exception as e:
        print(f"❌ Database integration test failed: {e}")

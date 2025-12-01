#!/usr/bin/env python3
"""
Codex Treasury Database Integration
=================================

PostgreSQL-powered transaction archival system for the Codex Dominion platform.
Integrates with the existing JSON ledger while providing robust database capabilities.

Features:
- Multi-stream transaction archival (affiliate, stock, AMM)
- Dual storage (PostgreSQL + JSON ledger)
- Connection pooling and error handling
- Integration with Dawn Dispatch system
- Treasury analytics and reporting
"""

import datetime
import json
import logging
import os
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

# Database imports with fallback handling
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    from psycopg2.pool import SimpleConnectionPool

    PSYCOPG2_AVAILABLE = True
except ImportError:
    print("⚠️  psycopg2 not available. Install with: pip install psycopg2-binary")
    PSYCOPG2_AVAILABLE = False

# Configuration
LEDGER_PATH = "codex_ledger.json"
CONFIG_PATH = "treasury_config.json"

# Default database configuration with Cloud SQL support
DEFAULT_DB_CONFIG = {
    "dbname": "codex",
    "user": "codex_user",
    "password": "codex_pass",
    "host": "localhost",
    "port": 5432,
    "minconn": 1,
    "maxconn": 10,
}


def get_cloud_sql_config():
    """Get Cloud SQL configuration from environment variables with Secret Manager support."""
    # Check for Cloud Run environment
    instance_connection_name = os.environ.get("INSTANCE_CONNECTION_NAME")
    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        # Parse DATABASE_URL (postgresql://user:pass@/dbname?host=/cloudsql/instance)
        import urllib.parse

        parsed = urllib.parse.urlparse(database_url)

        # Extract Unix socket path for Cloud SQL
        query_params = urllib.parse.parse_qs(parsed.query)
        host = query_params.get("host", [None])[0]

        return {
            "dbname": parsed.path.lstrip("/"),
            "user": parsed.username,
            "password": parsed.password,
            "host": host or "/cloudsql/" + instance_connection_name,
            "minconn": 1,
            "maxconn": 10,
        }
    elif instance_connection_name:
        # Direct Cloud SQL configuration with Secret Manager support
        db_password = os.environ.get("DB_PASS")

        # If no direct password, try to get from Secret Manager
        if not db_password:
            try:
                import subprocess

                result = subprocess.run(
                    [
                        "gcloud",
                        "secrets",
                        "versions",
                        "access",
                        "latest",
                        "--secret=codex-db-pass",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if result.returncode == 0:
                    db_password = result.stdout.strip()
                else:
                    db_password = "codex_pass"  # Fallback
            except Exception:
                db_password = "codex_pass"  # Fallback

        return {
            "dbname": os.environ.get("DB_NAME", "codex"),
            "user": os.environ.get("DB_USER", "codex_user"),
            "password": db_password,
            "host": f"/cloudsql/{instance_connection_name}",
            "minconn": 1,
            "maxconn": 10,
        }

    # Fallback to default config
    return DEFAULT_DB_CONFIG


class CodexTreasury:
    """
    Codex Treasury Management System

    Handles all financial transactions across multiple revenue streams
    while maintaining integration with the existing JSON ledger system.
    """

    def __init__(self, config_file: str = CONFIG_PATH):
        """Initialize the Treasury system."""
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.connection_pool = None

        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Initialize database connection if available
        if PSYCOPG2_AVAILABLE:
            self._init_connection_pool()
        else:
            self.logger.warning("PostgreSQL not available - using JSON-only mode")

    def _load_config(self) -> Dict[str, Any]:
        """Load treasury configuration."""
        try:
            if self.config_file.exists():
                with open(self.config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                # Create default config
                config = {
                    "database": DEFAULT_DB_CONFIG.copy(),
                    "treasury_settings": {
                        "auto_ledger_sync": True,
                        "backup_to_json": True,
                        "currency_default": "USD",
                        "timezone": "UTC",
                    },
                    "revenue_streams": {
                        "affiliate": {"enabled": True, "commission_rate": 0.05},
                        "stock": {"enabled": True, "fee_rate": 0.01},
                        "amm": {"enabled": True, "swap_fee": 0.003},
                        "consulting": {"enabled": True, "hourly_rate": 150.00},
                        "development": {"enabled": True, "project_rate": 2000.00},
                    },
                    "alerts": {
                        "daily_threshold": 1000.00,
                        "monthly_target": 5000.00,
                        "email_notifications": False,
                    },
                }

                with open(self.config_file, "w", encoding="utf-8") as f:
                    json.dump(config, f, indent=2)

                return config
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return {"database": DEFAULT_DB_CONFIG.copy()}

    def _init_connection_pool(self) -> None:
        """Initialize PostgreSQL connection pool with Cloud SQL support."""
        try:
            # Try Cloud SQL configuration first, then config file, then default
            if os.environ.get("INSTANCE_CONNECTION_NAME") or os.environ.get(
                "DATABASE_URL"
            ):
                db_config = get_cloud_sql_config()
                self.logger.info("🌐 Using Google Cloud SQL configuration")
            else:
                db_config = self.config.get("database", DEFAULT_DB_CONFIG)
                self.logger.info("🏠 Using local PostgreSQL configuration")

            # Create connection pool
            self.connection_pool = SimpleConnectionPool(
                minconn=db_config.get("minconn", 1),
                maxconn=db_config.get("maxconn", 10),
                **{
                    k: v
                    for k, v in db_config.items()
                    if k not in ["minconn", "maxconn"]
                },
            )

            # Test connection
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                    result = cur.fetchone()
                    if result:
                        env_type = (
                            "Cloud SQL"
                            if os.environ.get("INSTANCE_CONNECTION_NAME")
                            else "Local PostgreSQL"
                        )
                        self.logger.info(f"✅ {env_type} connection established")

        except Exception as e:
            self.logger.error(f"❌ Failed to initialize database pool: {e}")
            self.connection_pool = None

    def _get_connection(self):
        """Get connection from pool with context manager support."""
        if not self.connection_pool:
            raise Exception("Database connection pool not available")

        class ConnectionContext:
            def __init__(self, pool):
                self.pool = pool
                self.conn = None

            def __enter__(self):
                self.conn = self.pool.getconn()
                return self.conn

            def __exit__(self, exc_type, exc_val, exc_tb):
                if self.conn:
                    if exc_type:
                        self.conn.rollback()
                    else:
                        self.conn.commit()
                    self.pool.putconn(self.conn)

        return ConnectionContext(self.connection_pool)

    def load_ledger(self) -> Dict[str, Any]:
        """Load the main Codex ledger."""
        if os.path.exists(LEDGER_PATH):
            try:
                with open(LEDGER_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.logger.warning("Could not load ledger, creating new structure")

        return {
            "meta": {
                "version": "1.0.0",
                "last_updated": datetime.datetime.now().isoformat() + "Z",
                "custodian_authority": "Jermaine Merritt",
            },
            "transactions": [],
            "treasury_summary": {
                "total_revenue": 0.0,
                "transactions_count": 0,
                "last_transaction": None,
            },
        }

    def save_ledger(self, ledger: Dict[str, Any]) -> None:
        """Save the ledger with updated treasury data."""
        ledger["meta"]["last_updated"] = datetime.datetime.now().isoformat() + "Z"

        with open(LEDGER_PATH, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2, ensure_ascii=False)

    def archive_transaction(
        self,
        stream: str,
        amount: float,
        currency: str = "USD",
        source: str = "",
        status: str = "pending",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Archive a transaction to both PostgreSQL and JSON ledger.

        Args:
            stream: Revenue stream (affiliate, stock, amm, etc.)
            amount: Transaction amount
            currency: Currency code (default USD)
            source: Transaction source identifier
            status: Transaction status (pending, confirmed, executed, etc.)
            metadata: Additional transaction metadata

        Returns:
            Transaction ID
        """
        txn_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.datetime.utcnow()

        # Prepare transaction data
        txn_data = {
            "id": txn_id,
            "stream": stream,
            "amount": amount,
            "currency": currency,
            "source": source,
            "status": status,
            "created_at": timestamp.isoformat() + "Z",
            "metadata": metadata or {},
        }

        try:
            # Store in PostgreSQL if available
            if self.connection_pool:
                self._store_in_postgres(txn_data)

            # Always store in JSON ledger
            self._store_in_ledger(txn_data)

            self.logger.info(f"✅ Transaction {txn_id} archived: {stream} ${amount}")

            return txn_id

        except Exception as e:
            self.logger.error(f"❌ Failed to archive transaction: {e}")
            # Still try to store in ledger as fallback
            try:
                self._store_in_ledger(txn_data)
                return txn_id
            except Exception as ledger_error:
                self.logger.error(f"❌ Ledger fallback failed: {ledger_error}")
                raise

    def _store_in_postgres(self, txn_data: Dict[str, Any]) -> None:
        """Store transaction in PostgreSQL database."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO transactions (
                        id, stream, amount, currency, source, status, 
                        created_at, metadata
                    ) VALUES (
                        %(id)s, %(stream)s, %(amount)s, %(currency)s, 
                        %(source)s, %(status)s, %(created_at)s, %(metadata)s
                    )
                """,
                    {**txn_data, "metadata": json.dumps(txn_data["metadata"])},
                )

    def _store_in_ledger(self, txn_data: Dict[str, Any]) -> None:
        """Store transaction in JSON ledger."""
        ledger = self.load_ledger()

        # Add to transactions
        if "transactions" not in ledger:
            ledger["transactions"] = []
        ledger["transactions"].append(txn_data)

        # Update treasury summary
        if "treasury_summary" not in ledger:
            ledger["treasury_summary"] = {
                "total_revenue": 0.0,
                "transactions_count": 0,
                "last_transaction": None,
            }

        summary = ledger["treasury_summary"]
        summary["total_revenue"] = (
            summary.get("total_revenue", 0.0) + txn_data["amount"]
        )
        summary["transactions_count"] = len(ledger["transactions"])
        summary["last_transaction"] = txn_data["created_at"]

        # Update revenue streams summary
        if "revenue_streams_data" not in ledger:
            ledger["revenue_streams_data"] = {}

        stream = txn_data["stream"]
        if stream not in ledger["revenue_streams_data"]:
            ledger["revenue_streams_data"][stream] = {
                "total_amount": 0.0,
                "transaction_count": 0,
                "last_transaction": None,
            }

        stream_data = ledger["revenue_streams_data"][stream]
        stream_data["total_amount"] += txn_data["amount"]
        stream_data["transaction_count"] += 1
        stream_data["last_transaction"] = txn_data["created_at"]

        self.save_ledger(ledger)

    def ingest_affiliate(
        self, order_id: str, amount: float, currency: str = "USD", **kwargs
    ) -> str:
        """Ingest affiliate commission transaction."""
        return self.archive_transaction(
            stream="affiliate",
            amount=amount,
            currency=currency,
            source=f"order:{order_id}",
            status="confirmed",
            metadata={"order_id": order_id, "commission_type": "affiliate", **kwargs},
        )

    def ingest_stock(
        self, symbol: str, amount: float, currency: str = "USD", **kwargs
    ) -> str:
        """Ingest stock trading transaction."""
        return self.archive_transaction(
            stream="stock",
            amount=amount,
            currency=currency,
            source=f"symbol:{symbol}",
            status="executed",
            metadata={"symbol": symbol, "transaction_type": "trade", **kwargs},
        )

    def ingest_amm(
        self, pool_id: str, amount: float, currency: str = "USD", **kwargs
    ) -> str:
        """Ingest AMM pool transaction."""
        return self.archive_transaction(
            stream="amm",
            amount=amount,
            currency=currency,
            source=f"pool:{pool_id}",
            status="balanced",
            metadata={"pool_id": pool_id, "transaction_type": "amm_swap", **kwargs},
        )

    def ingest_consulting(
        self, client_id: str, hours: float, rate: float, currency: str = "USD", **kwargs
    ) -> str:
        """Ingest consulting revenue."""
        amount = hours * rate
        return self.archive_transaction(
            stream="consulting",
            amount=amount,
            currency=currency,
            source=f"client:{client_id}",
            status="invoiced",
            metadata={
                "client_id": client_id,
                "hours": hours,
                "hourly_rate": rate,
                **kwargs,
            },
        )

    def ingest_development(
        self, project_id: str, amount: float, currency: str = "USD", **kwargs
    ) -> str:
        """Ingest development project revenue."""
        return self.archive_transaction(
            stream="development",
            amount=amount,
            currency=currency,
            source=f"project:{project_id}",
            status="milestone_completed",
            metadata={
                "project_id": project_id,
                "milestone_type": "development",
                **kwargs,
            },
        )

    def get_treasury_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get treasury summary for specified time period."""
        try:
            # Try PostgreSQL first if available
            if self.connection_pool:
                return self._get_postgres_summary(days)
            else:
                return self._get_ledger_summary(days)
        except Exception as e:
            self.logger.error(f"Error getting treasury summary: {e}")
            # Fallback to ledger
            return self._get_ledger_summary(days)

    def _get_postgres_summary(self, days: int) -> Dict[str, Any]:
        """Get summary from PostgreSQL."""
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Get total revenue
                cur.execute(
                    """
                    SELECT 
                        stream,
                        COUNT(*) as transaction_count,
                        SUM(amount) as total_amount,
                        MAX(created_at) as last_transaction
                    FROM transactions 
                    WHERE created_at >= %s
                    GROUP BY stream
                """,
                    (datetime.datetime.utcnow() - datetime.timedelta(days=days),),
                )

                streams = {row["stream"]: dict(row) for row in cur.fetchall()}

                # Get overall totals
                cur.execute(
                    """
                    SELECT 
                        COUNT(*) as total_transactions,
                        SUM(amount) as total_revenue
                    FROM transactions 
                    WHERE created_at >= %s
                """,
                    (datetime.datetime.utcnow() - datetime.timedelta(days=days),),
                )

                totals = cur.fetchone()

                return {
                    "period_days": days,
                    "total_revenue": float(totals["total_revenue"] or 0),
                    "total_transactions": totals["total_transactions"],
                    "revenue_streams": streams,
                    "source": "postgresql",
                }

    def _get_ledger_summary(self, days: int) -> Dict[str, Any]:
        """Get summary from JSON ledger."""
        ledger = self.load_ledger()
        cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=days)

        transactions = ledger.get("transactions", [])
        recent_txns = [
            txn
            for txn in transactions
            if datetime.datetime.fromisoformat(txn["created_at"].replace("Z", ""))
            > cutoff
        ]

        # Calculate stream summaries
        streams = {}
        for txn in recent_txns:
            stream = txn["stream"]
            if stream not in streams:
                streams[stream] = {
                    "transaction_count": 0,
                    "total_amount": 0.0,
                    "last_transaction": None,
                }

            streams[stream]["transaction_count"] += 1
            streams[stream]["total_amount"] += txn["amount"]

            if (
                not streams[stream]["last_transaction"]
                or txn["created_at"] > streams[stream]["last_transaction"]
            ):
                streams[stream]["last_transaction"] = txn["created_at"]

        total_revenue = sum(txn["amount"] for txn in recent_txns)

        return {
            "period_days": days,
            "total_revenue": total_revenue,
            "total_transactions": len(recent_txns),
            "revenue_streams": streams,
            "source": "json_ledger",
        }

    def create_database_tables(self) -> bool:
        """Create necessary database tables."""
        if not self.connection_pool:
            self.logger.warning("No database connection available")
            return False

        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    # Create transactions table
                    cur.execute(
                        """
                        CREATE TABLE IF NOT EXISTS transactions (
                            id VARCHAR(20) PRIMARY KEY,
                            stream VARCHAR(50) NOT NULL,
                            amount DECIMAL(15,2) NOT NULL,
                            currency VARCHAR(10) NOT NULL DEFAULT 'USD',
                            source VARCHAR(200) NOT NULL,
                            status VARCHAR(50) NOT NULL DEFAULT 'pending',
                            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            metadata JSONB
                        );
                    """
                    )

                    # Create indexes
                    cur.execute(
                        "CREATE INDEX IF NOT EXISTS idx_transactions_stream ON transactions(stream);"
                    )
                    cur.execute(
                        "CREATE INDEX IF NOT EXISTS idx_transactions_created_at ON transactions(created_at);"
                    )
                    cur.execute(
                        "CREATE INDEX IF NOT EXISTS idx_transactions_status ON transactions(status);"
                    )

                    self.logger.info("✅ Database tables created successfully")
                    return True

        except Exception as e:
            self.logger.error(f"❌ Failed to create database tables: {e}")
            return False


# Convenience functions for backward compatibility
def connect_db():
    """Legacy function - use CodexTreasury instead."""
    treasury = CodexTreasury()
    if treasury.connection_pool:
        return treasury._get_connection()
    else:
        raise Exception("Database not available")


def archive_transaction(stream, amount, currency="USD", source="", status="pending"):
    """Legacy function - use CodexTreasury.archive_transaction instead."""
    treasury = CodexTreasury()
    return treasury.archive_transaction(stream, amount, currency, source, status)


def ingest_affiliate(order_id, amount, currency="USD"):
    """Legacy function - use CodexTreasury.ingest_affiliate instead."""
    treasury = CodexTreasury()
    return treasury.ingest_affiliate(order_id, amount, currency)


def ingest_stock(symbol, amount, currency="USD"):
    """Legacy function - use CodexTreasury.ingest_stock instead."""
    treasury = CodexTreasury()
    return treasury.ingest_stock(symbol, amount, currency)


def ingest_amm(pool_id, amount, currency="USD"):
    """Legacy function - use CodexTreasury.ingest_amm instead."""
    treasury = CodexTreasury()
    return treasury.ingest_amm(pool_id, amount, currency)


def main():
    """Demo and testing function."""
    print("🏛️  Codex Treasury System Demo")
    print("=" * 40)

    # Initialize treasury
    treasury = CodexTreasury()

    # Create database tables if needed
    if treasury.connection_pool:
        treasury.create_database_tables()

    # Demo transactions
    print("\n💰 Processing demo transactions...")

    # Affiliate commission
    affiliate_txn = treasury.ingest_affiliate(
        "A123", 49.99, metadata={"platform": "WooCommerce"}
    )
    print(f"✅ Affiliate transaction: {affiliate_txn}")

    # Stock trading
    stock_txn = treasury.ingest_stock(
        "MSFT", 1000.00, metadata={"shares": 10, "price_per_share": 100.00}
    )
    print(f"✅ Stock transaction: {stock_txn}")

    # AMM pool
    amm_txn = treasury.ingest_amm(
        "pool-eth-usdc", 500.00, metadata={"pool_type": "liquidity", "apr": 12.5}
    )
    print(f"✅ AMM transaction: {amm_txn}")

    # Consulting
    consulting_txn = treasury.ingest_consulting(
        "client-001", 8.0, 150.00, metadata={"project": "AI Development"}
    )
    print(f"✅ Consulting transaction: {consulting_txn}")

    # Get summary
    print("\n📊 Treasury Summary (Last 30 days):")
    summary = treasury.get_treasury_summary(30)
    print(f"   Total Revenue: ${summary['total_revenue']:.2f}")
    print(f"   Transactions: {summary['total_transactions']}")
    print(f"   Data Source: {summary['source']}")

    for stream, data in summary["revenue_streams"].items():
        print(
            f"   {stream.title()}: ${data['total_amount']:.2f} ({data['transaction_count']} txns)"
        )


if __name__ == "__main__":
    main()

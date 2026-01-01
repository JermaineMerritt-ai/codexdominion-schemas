"""
Migration: Add Withdrawals Table for Payout System

This migration creates the withdrawals table to track user withdrawal requests
and their processing status.

Table: withdrawals
- id: VARCHAR (primary key)
- user_id: VARCHAR (foreign key to users)
- amount: FLOAT (withdrawal amount)
- destination: VARCHAR (payment destination - PayPal, bank, etc.)
- destination_details: TEXT (JSON with account details)
- status: VARCHAR (pending|processing|completed|failed)
- failure_reason: TEXT (optional - why withdrawal failed)
- created_at: DATETIME (when withdrawal requested)
- processed_at: DATETIME (when withdrawal completed/failed)

Indexes:
- user_id (for user withdrawal history)
- status (for admin filtering pending/processing)
- created_at (for date-based queries)

Run: python migrate_add_withdrawals.py
"""

import sys
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Float, Text, DateTime, ForeignKey, Index

# Import existing Base and User model
from models import Base
from config import Config


class Withdrawal(Base):
    """Withdrawal model for payout tracking"""
    __tablename__ = 'withdrawals'
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    destination = Column(String, nullable=False)  # 'paypal', 'bank', 'stripe', etc.
    destination_details = Column(Text, nullable=True)  # JSON: {"email": "user@paypal.com"}
    status = Column(String, nullable=False, default='pending', index=True)  # pending|processing|completed|failed
    failure_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    processed_at = Column(DateTime, nullable=True)
    
    __table_args__ = (
        Index('idx_withdrawals_user_status', 'user_id', 'status'),
        Index('idx_withdrawals_status_created', 'status', 'created_at'),
    )


def run_migration():
    """Create withdrawals table"""
    print("\n" + "="*80)
    print("  MIGRATION: Add Withdrawals Table for Payout System")
    print("="*80 + "\n")
    
    # Connect to database
    engine = create_engine(Config.DATABASE_URL, echo=True)
    
    print("📊 Checking existing tables...")
    from sqlalchemy import inspect
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    if 'withdrawals' in existing_tables:
        print("⚠️  Table 'withdrawals' already exists!")
        response = input("Do you want to drop and recreate it? (yes/no): ").strip().lower()
        if response != 'yes':
            print("❌ Migration cancelled")
            return False
        
        print("🗑️  Dropping existing withdrawals table...")
        Withdrawal.__table__.drop(engine, checkfirst=True)
    
    print("\n🔨 Creating withdrawals table...")
    Withdrawal.__table__.create(engine, checkfirst=True)
    
    print("✅ Withdrawals table created successfully!")
    print("\nTable schema:")
    print("  - id (VARCHAR) - Primary key")
    print("  - user_id (VARCHAR) - Foreign key to users")
    print("  - amount (FLOAT) - Withdrawal amount")
    print("  - destination (VARCHAR) - Payment method")
    print("  - destination_details (TEXT) - Account details JSON")
    print("  - status (VARCHAR) - pending|processing|completed|failed")
    print("  - failure_reason (TEXT) - Optional error message")
    print("  - created_at (DATETIME) - Request timestamp")
    print("  - processed_at (DATETIME) - Completion timestamp")
    print("\nIndexes:")
    print("  - idx_withdrawals_user_id (user_id)")
    print("  - idx_withdrawals_status (status)")
    print("  - idx_withdrawals_created_at (created_at)")
    print("  - idx_withdrawals_user_status (user_id, status)")
    print("  - idx_withdrawals_status_created (status, created_at)")
    
    print("\n" + "="*80)
    print("  ✅ MIGRATION COMPLETE!")
    print("="*80 + "\n")
    
    return True


if __name__ == '__main__':
    try:
        success = run_migration()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

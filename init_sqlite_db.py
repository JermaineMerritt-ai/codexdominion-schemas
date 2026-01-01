"""
Quick script to initialize SQLite database
This avoids module caching issues
"""
import os
import sys

# Set DATABASE_URL environment variable directly
os.environ['DATABASE_URL'] = 'sqlite:///codexdominion.db'

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from models import Base

# Create SQLite engine
engine = create_engine(
    'sqlite:///codexdominion.db',
    echo=False,
    poolclass=StaticPool,
    connect_args={'check_same_thread': False}
)

# Create all tables
print("🔄 Creating database tables...")
Base.metadata.create_all(engine)

# Verify tables
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()

print(f"\n✅ Database initialized successfully!")
print(f"📊 Created {len(tables)} tables:")
for table in sorted(tables):
    print(f"   - {table}")
print(f"\n📁 Database file: codexdominion.db")

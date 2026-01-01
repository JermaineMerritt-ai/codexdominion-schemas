"""
Migration Pattern: JSON → Postgres Database

This shows the pattern for migrating any JSON data source to database queries.
Use this as a template for agents, workflows, tools, etc.
"""

# ============================================================================
# PATTERN: Before (JSON Loading)
# ============================================================================

# Load JSON at module level
data_json = load_json("data.json")

def get_all_items():
    """Get all items from JSON"""
    return data_json.get("items", [])

def get_item_by_id(item_id):
    """Find item by ID from JSON"""
    for item in data_json.get("items", []):
        if item.get("id") == item_id:
            return item
    return None

def get_item_by_field(field_value):
    """Find item by custom field from JSON"""
    for item in data_json.get("items", []):
        if item.get("field") == field_value:
            return item
    return None

@app.route('/api/items')
def api_get_items():
    """API endpoint using JSON"""
    return jsonify(data_json)

@app.route('/api/items/<item_id>')
def api_get_item(item_id):
    """API endpoint using JSON"""
    item = get_item_by_id(item_id)
    if not item:
        return jsonify({"error": "Not found"}), 404
    return jsonify(item)


# ============================================================================
# PATTERN: After (Database Queries)
# ============================================================================

# Comment out JSON loading
# data_json = load_json("data.json")  # MIGRATED TO DATABASE

# Add database imports at top of file
from database import SessionLocal, init_db
from models import Item  # Your SQLAlchemy model
from flask import g

# Add Flask session management (once per file)
@app.before_first_request
def startup():
    init_db()

@app.before_request
def create_session():
    g.db = SessionLocal()

@app.teardown_request
def shutdown_session(exception=None):
    db = getattr(g, "db", None)
    if db is not None:
        if exception:
            db.rollback()
        else:
            db.commit()
        db.close()

# Migrate helper functions
def get_all_items():
    """Get all items from database"""
    session = g.db
    items = session.query(Item).all()
    return [item.to_dict() for item in items]

def get_item_by_id(item_id):
    """Find item by ID from database"""
    session = g.db
    item = session.query(Item).filter(Item.id == item_id).first()
    return item.to_dict() if item else None

def get_item_by_field(field_value):
    """Find item by custom field from database"""
    session = g.db
    item = session.query(Item).filter(Item.field == field_value).first()
    return item.to_dict() if item else None

# Migrate API endpoints
@app.route('/api/items')
def api_get_items():
    """API endpoint using database"""
    session = g.db
    items = session.query(Item).all()
    return jsonify({
        "items": [item.to_dict() for item in items]
    })

@app.route('/api/items/<item_id>')
def api_get_item(item_id):
    """API endpoint using database"""
    session = g.db
    item = session.query(Item).filter(Item.id == item_id).first()
    if not item:
        return jsonify({"error": "Not found"}), 404
    return jsonify(item.to_dict())


# ============================================================================
# PATTERN: SQLAlchemy Model (models.py)
# ============================================================================

from sqlalchemy import Column, String, Integer, Float, Text, TIMESTAMP, JSONB
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    field = Column(String)
    description = Column(Text)
    metadata = Column(JSONB)  # For JSON data
    status = Column(String, default='active')
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    def to_dict(self):
        """Serialize to dictionary for JSON responses"""
        return {
            'id': self.id,
            'name': self.name,
            'field': self.field,
            'description': self.description,
            'metadata': self.metadata,
            'status': self.status,
            'created_at': self.created_at.isoformat() + 'Z' if self.created_at else None
        }


# ============================================================================
# PATTERN: Migration Script (scripts/migrations/migrate_items_from_json.py)
# ============================================================================

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from models import Base, Item
from database import get_db_session, engine

def load_items_json(json_path: str = "items.json"):
    """Load items from JSON file"""
    json_file = Path(__file__).parent.parent.parent / json_path
    if not json_file.exists():
        print(f"❌ JSON file not found: {json_file}")
        sys.exit(1)
    
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Handle both array and object with "items" key
    if isinstance(data, list):
        return data
    elif isinstance(data, dict) and "items" in data:
        return data["items"]
    else:
        print("❌ Unexpected JSON structure")
        sys.exit(1)


def migrate_items():
    """Migrate items from JSON to Postgres"""
    print("🔄 Starting items migration from JSON to Postgres...")
    
    Base.metadata.create_all(engine)
    
    with get_db_session() as session:
        try:
            items_data = load_items_json()
            print(f"📋 Found {len(items_data)} items in JSON")
            
            existing_count = session.query(Item).count()
            print(f"📊 Database currently has {existing_count} items")
            
            inserted = 0
            updated = 0
            
            for item_data in items_data:
                item_id = item_data.get("id")
                if not item_id:
                    continue
                
                existing = session.query(Item).filter(Item.id == item_id).first()
                
                if existing:
                    # Update existing
                    existing.name = item_data.get("name") or existing.name
                    existing.field = item_data.get("field")
                    existing.description = item_data.get("description")
                    existing.metadata = item_data.get("metadata")
                    existing.status = item_data.get("status", "active")
                    updated += 1
                    print(f"✏️  Updated: {existing.name} ({item_id})")
                else:
                    # Insert new
                    item = Item(
                        id=item_id,
                        name=item_data.get("name", "Unnamed Item"),
                        field=item_data.get("field"),
                        description=item_data.get("description"),
                        metadata=item_data.get("metadata"),
                        status=item_data.get("status", "active")
                    )
                    session.add(item)
                    inserted += 1
                    print(f"➕ Inserted: {item.name} ({item_id})")
            
            print("\n" + "=" * 60)
            print("✅ Migration complete!")
            print(f"   Inserted: {inserted}")
            print(f"   Updated:  {updated}")
            print(f"   Total in DB: {session.query(Item).count()}")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    migrate_items()


# ============================================================================
# PATTERN: Common Query Patterns
# ============================================================================

# Filter by single field
def get_active_items():
    session = g.db
    items = session.query(Item).filter(Item.status == 'active').all()
    return [item.to_dict() for item in items]

# Filter with LIKE (case-insensitive)
def search_items_by_name(name):
    session = g.db
    items = session.query(Item).filter(Item.name.ilike(f'%{name}%')).all()
    return [item.to_dict() for item in items]

# Count records
def get_item_count():
    session = g.db
    return session.query(Item).count()

# Pagination
def get_items_paginated(page=1, per_page=10):
    session = g.db
    offset = (page - 1) * per_page
    items = session.query(Item).offset(offset).limit(per_page).all()
    total = session.query(Item).count()
    return {
        'items': [item.to_dict() for item in items],
        'page': page,
        'per_page': per_page,
        'total': total
    }

# Order by field
def get_items_sorted():
    session = g.db
    items = session.query(Item).order_by(Item.created_at.desc()).all()
    return [item.to_dict() for item in items]

# Multiple filters
def get_filtered_items(status, field):
    session = g.db
    items = session.query(Item).filter(
        Item.status == status,
        Item.field == field
    ).all()
    return [item.to_dict() for item in items]

# With relationships (if Item has relationships)
from sqlalchemy.orm import joinedload

def get_item_with_relations(item_id):
    session = g.db
    item = session.query(Item).options(
        joinedload(Item.related_items),
        joinedload(Item.metadata_obj)
    ).filter(Item.id == item_id).first()
    return item.to_dict() if item else None


# ============================================================================
# PATTERN: Checklist for Each Migration
# ============================================================================

"""
For each JSON data source to migrate:

1. [ ] Create SQLAlchemy model in models.py
2. [ ] Add to_dict() method to model
3. [ ] Create migration script: migrate_X_from_json.py
4. [ ] Comment out JSON loading in Flask app
5. [ ] Add database imports (once)
6. [ ] Add session management hooks (once)
7. [ ] Replace helper functions with queries
8. [ ] Replace API endpoints with queries
9. [ ] Run migration script
10. [ ] Test endpoints
11. [ ] Move JSON file to backups/

Benefits:
✅ No file I/O on every request
✅ Efficient database queries with indexes
✅ Type safety and validation
✅ Transaction support
✅ Relationship queries
✅ Scalable connection pooling
"""

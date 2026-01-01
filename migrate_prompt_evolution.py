"""
Prompt Evolution Migration Script
Adds PromptHistory table and extends GraphicsProject with evolution tracking fields.

Run this to update your existing database schema.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app for migration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///codex_graphics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

print("🔄 Running Prompt Evolution Migration...")

with app.app_context():
    # Check if database file exists
    import os
    if not os.path.exists('codex_graphics.db'):
        print("❌ Database file 'codex_graphics.db' not found!")
        print("Please run the main Flask app first to create the database.")
        exit(1)
    
    # Get database connection
    from sqlalchemy import inspect, text
    inspector = inspect(db.engine)
    
    print("\n📋 Current tables:", inspector.get_table_names())
    
    # Check if PromptHistory table exists
    if 'prompt_history' not in inspector.get_table_names():
        print("\n✅ Creating PromptHistory table...")
        db.session.execute(text("""
            CREATE TABLE prompt_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt_text TEXT NOT NULL,
                team_id INTEGER,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                parent_id INTEGER,
                generation INTEGER DEFAULT 1,
                evolution_reason VARCHAR(100),
                mood VARCHAR(50),
                color_palette VARCHAR(50),
                tags TEXT,
                category VARCHAR(100),
                times_used INTEGER DEFAULT 0,
                times_saved INTEGER DEFAULT 0,
                times_reused INTEGER DEFAULT 0,
                avg_engagement FLOAT DEFAULT 0.0,
                effectiveness_score FLOAT DEFAULT 0.0,
                is_template BOOLEAN DEFAULT 0,
                is_evolved BOOLEAN DEFAULT 0,
                FOREIGN KEY (team_id) REFERENCES team (id),
                FOREIGN KEY (created_by) REFERENCES user (id),
                FOREIGN KEY (parent_id) REFERENCES prompt_history (id)
            )
        """))
        db.session.commit()
        print("   ✅ PromptHistory table created!")
    else:
        print("\n⚠️ PromptHistory table already exists, skipping...")
    
    # Check if GraphicsProject has new columns
    graphics_columns = [col['name'] for col in inspector.get_columns('graphics_project')]
    
    missing_columns = []
    if 'parent_prompt_id' not in graphics_columns:
        missing_columns.append(('parent_prompt_id', 'INTEGER', 'FOREIGN KEY (parent_prompt_id) REFERENCES prompt_history (id)'))
    if 'prompt_source' not in graphics_columns:
        missing_columns.append(('prompt_source', 'VARCHAR(50)', ''))
    if 'was_prompt_reused' not in graphics_columns:
        missing_columns.append(('was_prompt_reused', 'BOOLEAN DEFAULT 0', ''))
    if 'engagement_score' not in graphics_columns:
        missing_columns.append(('engagement_score', 'FLOAT DEFAULT 0.0', ''))
    if 'original_prompt' not in graphics_columns:
        missing_columns.append(('original_prompt', 'TEXT', ''))
    if 'prompt_version' not in graphics_columns:
        missing_columns.append(('prompt_version', 'INTEGER DEFAULT 1', ''))
    if 'parent_project_id' not in graphics_columns:
        missing_columns.append(('parent_project_id', 'INTEGER', 'FOREIGN KEY (parent_project_id) REFERENCES graphics_project (id)'))
    
    if missing_columns:
        print("\n✅ Adding new columns to GraphicsProject table...")
        for col_name, col_type, constraint in missing_columns:
            try:
                db.session.execute(text(f"ALTER TABLE graphics_project ADD COLUMN {col_name} {col_type}"))
                print(f"   ✅ Added column: {col_name}")
            except Exception as e:
                print(f"   ⚠️ Column {col_name} might already exist: {e}")
        
        db.session.commit()
        print("   ✅ GraphicsProject columns added!")
    else:
        print("\n✅ All GraphicsProject columns already exist!")
    
    print("\n🎉 Migration complete!")
    print("\n📊 Updated schema:")
    print("   - PromptHistory: Tracks prompts independently with lineage and effectiveness")
    print("   - GraphicsProject: Extended with prompt evolution tracking fields")
    print("\n💡 Restart your Flask app to use the new prompt evolution features!")


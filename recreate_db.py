"""Quick script to recreate database with correct schema"""
from db import engine
from models import Base, Tenant, User, Council, Agent, Workflow, Store, AutomationRule, AdvisorRecommendation

print("🔧 Dropping all tables...")
Base.metadata.drop_all(bind=engine)

print("🏗️  Creating all tables with correct schema...")
Base.metadata.create_all(bind=engine)

print("✅ Database recreated successfully!")
print("📋 Tables created:")
for table in Base.metadata.sorted_tables:
    print(f"   • {table.name}")

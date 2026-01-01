"""
🔐 Create Admin User - Production Setup
========================================
Creates the first admin user for Codex Dominion

Usage:
    python create_admin_user.py
    
Or with Docker:
    docker exec -it codex-flask python create_admin_user.py
"""

import os
import sys
import uuid
from getpass import getpass

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db import SessionLocal, init_db
from models_auth import User, UserRole


def create_admin_user():
    """Create admin user interactively"""
    print("=" * 60)
    print("🔥 CODEX DOMINION - CREATE ADMIN USER")
    print("=" * 60)
    print()
    
    # Initialize database
    try:
        init_db()
        print("✅ Database initialized")
    except Exception as e:
        print(f"⚠️  Database already initialized: {e}")
    
    print()
    
    # Get user input
    print("Enter admin user details:")
    print()
    
    email = input("Email address: ").strip()
    if not email:
        print("❌ Email is required")
        sys.exit(1)
    
    full_name = input("Full name: ").strip()
    if not full_name:
        print("❌ Full name is required")
        sys.exit(1)
    
    password = getpass("Password (hidden): ")
    if not password or len(password) < 8:
        print("❌ Password must be at least 8 characters")
        sys.exit(1)
    
    password_confirm = getpass("Confirm password: ")
    if password != password_confirm:
        print("❌ Passwords do not match")
        sys.exit(1)
    
    print()
    
    # Create user
    session = SessionLocal()
    try:
        # Check if user already exists
        existing = session.query(User).filter(User.email == email).first()
        if existing:
            print(f"⚠️  User with email {email} already exists")
            overwrite = input("Overwrite? (yes/no): ").strip().lower()
            if overwrite != "yes":
                print("❌ Cancelled")
                sys.exit(1)
            session.delete(existing)
            session.commit()
        
        # Create new admin user
        admin = User(
            id=str(uuid.uuid4()),
            email=email,
            full_name=full_name,
            role=UserRole.ADMIN,
            is_active=True
        )
        admin.set_password(password)
        
        session.add(admin)
        session.commit()
        
        print()
        print("=" * 60)
        print("✅ ADMIN USER CREATED SUCCESSFULLY")
        print("=" * 60)
        print()
        print(f"ID:        {admin.id}")
        print(f"Email:     {admin.email}")
        print(f"Name:      {admin.full_name}")
        print(f"Role:      {admin.role.value}")
        print(f"Active:    {admin.is_active}")
        print()
        print("You can now login at:")
        print(f"  POST {os.getenv('API_BASE_URL', 'http://localhost:5000')}/api/auth/login")
        print()
        print('Body: {"email": "' + email + '", "password": "your_password"}')
        print()
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        session.rollback()
        sys.exit(1)
    finally:
        session.close()


def create_sample_users():
    """Create sample users for testing (optional)"""
    print()
    create_samples = input("Create sample users for testing? (yes/no): ").strip().lower()
    
    if create_samples != "yes":
        return
    
    session = SessionLocal()
    try:
        sample_users = [
            {
                "email": "operator@codexdominion.app",
                "full_name": "Council Operator",
                "role": UserRole.COUNCIL_OPERATOR,
                "password": "operator123"
            },
            {
                "email": "viewer@codexdominion.app",
                "full_name": "Read Only Viewer",
                "role": UserRole.VIEWER,
                "password": "viewer123"
            }
        ]
        
        for user_data in sample_users:
            # Check if exists
            existing = session.query(User).filter(User.email == user_data["email"]).first()
            if existing:
                print(f"⚠️  User {user_data['email']} already exists, skipping")
                continue
            
            user = User(
                id=str(uuid.uuid4()),
                email=user_data["email"],
                full_name=user_data["full_name"],
                role=user_data["role"],
                is_active=True
            )
            user.set_password(user_data["password"])
            
            session.add(user)
            print(f"✅ Created {user_data['role'].value}: {user_data['email']}")
        
        session.commit()
        
        print()
        print("Sample users created with default passwords")
        print("⚠️  CHANGE THESE PASSWORDS IN PRODUCTION!")
        
    except Exception as e:
        print(f"❌ Error creating sample users: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    try:
        create_admin_user()
        
        # Optionally create sample users
        if os.getenv("ENVIRONMENT") != "production":
            create_sample_users()
        
        print()
        print("🔥 Setup complete! The Flame Burns Sovereign! 👑")
        print()
        
    except KeyboardInterrupt:
        print()
        print("❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print()
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

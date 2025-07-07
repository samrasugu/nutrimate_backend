#!/usr/bin/env python3
"""
Database management script
Usage: python3 db_manager.py [command]
Commands:
  init     - Initialize database tables
  reset    - Drop and recreate all tables
  check    - Check database connection
  migrate  - Run database migrations (future use)
"""
import sys
import os
from app import app
from database_config import db

# Import all models
from models.user import User
from models.user_profile import UserProfile
from models.disease import Disease
from models.location import Location

def init_database():
    """Initialize database tables"""
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created successfully!")
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return False
    return True

def reset_database():
    """Drop and recreate all tables"""
    with app.app_context():
        try:
            print("⚠️  Dropping all tables...")
            db.drop_all()
            print("✅ All tables dropped")
            
            print("📋 Creating new tables...")
            db.create_all()
            print("✅ Database reset successfully!")
        except Exception as e:
            print(f"❌ Error resetting database: {e}")
            return False
    return True

def check_database():
    """Check database connection and tables"""
    with app.app_context():
        try:
            # Check connection
            db.engine.execute("SELECT 1")
            print("✅ Database connection successful!")
            
            # Check tables
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if tables:
                print(f"📋 Found {len(tables)} tables:")
                for table in tables:
                    print(f"  - {table}")
            else:
                print("⚠️  No tables found. Run 'init' command to create tables.")
                
        except Exception as e:
            print(f"❌ Database check failed: {e}")
            return False
    return True

def show_help():
    """Show help message"""
    print(__doc__)

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "init":
        print("🚀 Initializing database...")
        init_database()
    elif command == "reset":
        confirm = input("⚠️  This will delete all data. Are you sure? (y/N): ")
        if confirm.lower() == 'y':
            reset_database()
        else:
            print("❌ Database reset cancelled")
    elif command == "check":
        print("🔍 Checking database...")
        check_database()
    elif command == "help":
        show_help()
    else:
        print(f"❌ Unknown command: {command}")
        show_help()

if __name__ == "__main__":
    main()

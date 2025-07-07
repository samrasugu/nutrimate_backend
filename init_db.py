#!/usr/bin/env python3
"""
Database initialization script for NutriMate Backend
This script creates all necessary database tables.
"""
import os
import sys

# Import Flask app and database
from app import app
from database_config import db

# Import all models to ensure they're registered with SQLAlchemy
from models.user import User
from models.user_profile import UserProfile
from models.disease import Disease
from models.location import Location

def init_database():
    """Initialize the database with all tables"""
    try:
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Optionally, you can add some seed data here
            # create_seed_data()
            
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        sys.exit(1)

def create_seed_data():
    """Create initial seed data (optional)"""
    # You can add seed data here if needed
    # For example, default diseases or locations
    pass

def check_database_connection():
    """Check if database connection is working"""
    try:
        with app.app_context():
            # Try to execute a simple query
            result = db.engine.execute("SELECT 1")
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Initializing NutriMate Database...")
    
    # Check database connection first
    if not check_database_connection():
        print("Please check your database configuration in .env file")
        sys.exit(1)
    
    # Initialize database
    init_database()
    
    print("🎉 Database initialization completed!")

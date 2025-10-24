"""Database initialization for Flask GraphQL Server"""
import sys
import os
import sqlite3
from pathlib import Path

# Add src to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from adapters.database.db_session import DatabaseSession
from orm.models.user_model import Base

def create_tables():
    """Create database tables"""
    # Get the server directory path
    server_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(server_dir, "test.db")
    
    # Check if database file exists, create if not
    if not os.path.exists(db_path):
        print(f"📁 Creating SQLite database: {db_path}")
        # Create empty SQLite file
        conn = sqlite3.connect(db_path)
        conn.close()
        print(f"✅ SQLite database created: {db_path}")
    else:
        print(f"📁 SQLite database already exists: {db_path}")
    
    # Use absolute path for database connection
    db_url = f"sqlite:///{db_path}"
    db_session = DatabaseSession(db_url)
    
    try:
        # Create tables using sync SQLAlchemy
        Base.metadata.create_all(db_session.engine)
        
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        return False
    finally:
        db_session.close()

def init_database():
    """Initialize database synchronously"""
    try:
        result = create_tables()
        return result
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False
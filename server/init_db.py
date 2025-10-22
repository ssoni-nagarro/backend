"""Database initialization and server startup for Flask GraphQL Server"""
import asyncio
import sys
import os
import sqlite3
from pathlib import Path

# Add src to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from adapters.database.db_session import DatabaseSession
from orm.models.user_model import Base

async def create_tables():
    """Create database tables"""
    db_path = "test.db"
    
    # Check if database file exists, create if not
    if not os.path.exists(db_path):
        print(f"📁 Creating SQLite database: {db_path}")
        # Create empty SQLite file
        conn = sqlite3.connect(db_path)
        conn.close()
        print(f"✅ SQLite database created: {db_path}")
    else:
        print(f"📁 SQLite database already exists: {db_path}")
    
    db_session = DatabaseSession("sqlite+aiosqlite:///./test.db")
    
    try:
        # Create tables
        async with db_session.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        return False
    finally:
        await db_session.close()

def init_database():
    """Initialize database synchronously"""
    try:
        result = asyncio.run(create_tables())
        return result
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

def start_server():
    """Start the Flask GraphQL server"""
    try:
        from app import app
        print("🚀 Starting HauLink GraphQL Server...")
        print("📡 GraphQL endpoint: http://localhost:8000/graphql")
        print("🎮 GraphiQL playground: http://localhost:8000/graphql")
        print("❤️  Health check: http://localhost:8000/health")
        print("=" * 50)
        
        app.run(debug=True, host='0.0.0.0', port=8000)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def main():
    """Main function to initialize database and start server"""
    print("🗄️  Initializing HauLink GraphQL Server...")
    print("=" * 50)
    
    # Initialize database
    print("Step 1: Initializing database...")
    db_success = init_database()
    
    if not db_success:
        print("💥 Database initialization failed!")
        sys.exit(1)
    
    print("✅ Database initialization completed!")
    print("=" * 50)
    
    # Start server
    print("Step 2: Starting GraphQL server...")
    start_server()

if __name__ == "__main__":
    main()
"""Main server startup for Flask GraphQL Server"""
import sys
import os

# Add src to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from init_db import init_database

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

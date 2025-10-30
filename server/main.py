"""Main server startup for Flask GraphQL Server with proper signal handling"""
import sys
import os
import signal
import threading
import time

# Add src to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from init_db import init_database
from app import app

# Global flag to control server shutdown
shutdown_flag = threading.Event()

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    if signum == signal.SIGINT:  # Ctrl+C
        print("\n🛑 Received SIGINT (Ctrl+C). Shutting down gracefully...")
        shutdown_flag.set()
    elif signum == signal.SIGTSTP:  # Ctrl+Z
        print("\n⏸️  Received SIGTSTP (Ctrl+Z). Shutting down gracefully...")
        shutdown_flag.set()

def start_server():
    """Start the Flask GraphQL server with proper signal handling"""
    try:
        print("🚀 Starting HauLink GraphQL Server...")
        print("📡 GraphQL endpoint: http://localhost:8000/graphql")
        print("🎮 GraphiQL playground: http://localhost:8000/graphql")
        print("❤️  Health check: http://localhost:8000/health")
        print("=" * 50)
        if hasattr(signal, 'SIGTSTP'):
            print("💡 Press Ctrl+C or Ctrl+Z to stop the server")
        else:
            print("💡 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        # SIGTSTP is Unix-only (Ctrl+Z), so only register on Unix-like systems
        if hasattr(signal, 'SIGTSTP'):
            signal.signal(signal.SIGTSTP, signal_handler)
        
        # Start Flask app in a separate thread
        def run_flask():
            app.run(debug=True, host='0.0.0.0', port=8000, use_reloader=False)
        
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        
        # Wait for shutdown signal
        try:
            while not shutdown_flag.is_set():
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        
        print("\n🛑 Server shutdown requested. Stopping...")
        print("✅ Server stopped successfully!")
        
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

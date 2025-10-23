"""Database session factory for creating database sessions based on configuration"""
import os
import sys
from typing import Optional
from adapters.database.db_session import DatabaseSession

class DatabaseSessionFactory:
    """Factory for creating database sessions based on configuration"""
    
    _instance: Optional['DatabaseSessionFactory'] = None
    _db_session: Optional[DatabaseSession] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_database_url(self) -> str:
        """Get database URL from configuration"""
        # Try to get from environment variable first
        db_url = os.environ.get('DATABASE_URL')
        if db_url:
            return db_url
        
        # Fallback to config-based approach
        try:
            # Add server directory to path to import config
            server_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'server')
            sys.path.append(server_dir)
            
            from config import get_database_url
            return get_database_url()
        except ImportError:
            # Final fallback - assume we're running from server directory
            server_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'server')
            db_path = os.path.join(server_dir, "test.db")
            return f"sqlite+aiosqlite:///{db_path}"
    
    def get_session(self) -> DatabaseSession:
        """Get or create database session (Lambda optimized)"""
        if self._db_session is None:
            db_url = self.get_database_url()
            self._db_session = DatabaseSession(db_url)
        return self._db_session
    
    def reset_session(self):
        """Reset the database session (useful for testing)"""
        if self._db_session:
            # Note: In a real implementation, you might want to close the session properly
            self._db_session = None

"""Environment configuration for Flask GraphQL Server"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Database configuration
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite+aiosqlite:///./test.db')
    
    # GraphQL configuration
    GRAPHQL_ENABLE_INTROSPECTION = os.environ.get('GRAPHQL_ENABLE_INTROSPECTION', 'True').lower() == 'true'
    GRAPHQL_ENABLE_PLAYGROUND = os.environ.get('GRAPHQL_ENABLE_PLAYGROUND', 'True').lower() == 'true'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENV = 'production'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    DATABASE_URL = 'sqlite+aiosqlite:///./test.db'

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

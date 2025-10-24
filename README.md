# Haulink Backend

A clean architecture implementation for aws lambda handler based application.

## Project Structure

This project follows Clean Architecture principles with the following structure:

```
src/
├── adapters/          # External adapters (database, external services)
├── api/               # API layer (GraphQL schemas)
├── application/       # Application layer (services, DTOs, mappers)
├── handlers/          # Handlers (GraphQL resolvers)
├── domain/            # Domain layer (entities, repositories, exceptions)
├── migrations/        # Database migrations
├── orm/               # ORM layer (models, repository implementations)
├── utils/             # Utility functions
└── requirements.txt   # Core dependencies

server/
├── app.py             # Flask GraphQL server
├── init_db.py         # Database initialization
├── main.py            # Server startup
└── requirements.txt   # Server-specific dependencies
```

## Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Start

1. **Clone the repository and navigate to the project**:
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   # Install core dependencies (domain, application, and ORM layers)
   pip install -r src/requirements.txt
   
   # Install server dependencies (Flask, GraphQL, etc.)
   pip install -r server/requirements.txt
   ```

4. **Start the GraphQL server**:
   ```bash
   # Initialize database and start the server
   python server/main.py
   ```

5. **Access the application**:
   - **GraphQL Playground**: http://localhost:8000/graphql
   - **Health Check**: http://localhost:8000/health

### Build System

To build files for AWS deployment:

```bash
# Build artifacts
python3 builder/main.py

# Build artifacts with verbose output
python3 builder/main.py --verbose

# Clean build artifacts
python3 builder/main.py --clean
```


## Architecture Notes

This implementation follows Clean Architecture principles:

1. **Domain Layer**: Contains business entities, repository interfaces, and domain exceptions
2. **Application Layer**: Contains services, DTOs, and mappers
3. **Infrastructure Layer**: Contains ORM models, repository implementations, and database adapters
4. **Presentation Layer**: Contains GraphQL handlers and resolvers

The architecture ensures:
- **Dependency Inversion**: High-level modules don't depend on low-level modules
- **Separation of Concerns**: Each layer has a specific responsibility
- **Testability**: Easy to unit test each component in isolation
- **Maintainability**: Clear boundaries make the code easy to maintain and extend
- **GraphQL Integration**: Proper resolver pattern for GraphQL operations
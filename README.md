# HauLink Backend API

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
├── orm/               # ORM layer (models, migrations, repository implementations)
├── utils/             # Utility functions
└── requirements.txt   # Core dependencies

server/
├── app.py             # Flask GraphQL server
├── init_db.py         # Database initialization and server startup
├── requirements.txt   # Server-specific dependencies
└── README.md          # Server documentation

resolvers/
├── config/            # Resolver configurations
└── resolver_loader.py # Resolver configuration loader
```

## Setup

### Core Dependencies (src folder)
1. **Install core dependencies**:
   ```bash
   pip install -r src/requirements.txt
   ```

### GraphQL Server (server folder)
1. **Install server dependencies**:
   ```bash
   pip install -r server/requirements.txt
   ```

2. **Initialize database and start server**:
   ```bash
   python server/init_db.py
   ```

3. **Access GraphiQL playground**:
   - Open http://localhost:5000/graphql in your browser

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
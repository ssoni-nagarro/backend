# Flask GraphQL Server

A Flask-based GraphQL server with Graphene that provides a GraphiQL playground for testing the GraphQL API end-to-end.

## Features

- **Flask + Graphene**: Modern GraphQL server implementation
- **GraphiQL Playground**: Interactive GraphQL query interface
- **Clean Architecture**: Uses existing src folder structure
- **CORS Enabled**: Cross-origin requests supported
- **Environment Configuration**: Configurable via environment variables

## API Endpoints

- **GraphQL**: `POST /graphql`
- **GraphiQL**: `GET /graphql` (interactive playground)
- **Health Check**: `GET /health`
- **API Info**: `GET /`


## Database

The server automatically handles SQLite database initialization:

- **Database File**: `test.db` (created in server directory)
- **Auto-Creation**: Database file is created if it doesn't exist
- **Table Creation**: All necessary tables are created automatically
- **No Manual Setup**: Everything is handled by `init_db.py`

### Database Location
The SQLite database file (`test.db`) is created in the server directory and contains all user data and tables defined in the ORM models.

## Configuration

Copy `env.example` to `.env` and modify as needed:

```bash
cp env.example .env
```

### Environment Variables

- `DEBUG`: Enable debug mode (True/False)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 5000)
- `SECRET_KEY`: Flask secret key
- `DATABASE_URL`: Database connection string
- `GRAPHQL_ENABLE_INTROSPECTION`: Enable GraphQL introspection
- `GRAPHQL_ENABLE_PLAYGROUND`: Enable GraphiQL playground

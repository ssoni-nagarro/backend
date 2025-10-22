# Flask GraphQL Server

A Flask-based GraphQL server with Graphene that provides a GraphiQL playground for testing the GraphQL API end-to-end.

## Features

- **Flask + Graphene**: Modern GraphQL server implementation
- **GraphiQL Playground**: Interactive GraphQL query interface
- **Clean Architecture**: Uses existing src folder structure
- **Async Support**: Integrates with existing async handlers
- **CORS Enabled**: Cross-origin requests supported
- **Environment Configuration**: Configurable via environment variables

## Quick Start

1. **Install dependencies**:
   ```bash
   cd server
   pip install -r requirements.txt
   ```

2. **Initialize database and start server**:
   ```bash
   python init_db.py
   ```

   This will:
   - Create SQLite database if it doesn't exist
   - Create all necessary tables
   - Start the Flask GraphQL server
   - Launch GraphiQL playground

3. **Access GraphiQL**:
   - Open http://localhost:5000/graphql in your browser
   - Start writing GraphQL queries!

## API Endpoints

- **GraphQL**: `POST /graphql`
- **GraphiQL**: `GET /graphql` (interactive playground)
- **Health Check**: `GET /health`
- **API Info**: `GET /`

## GraphQL Operations

### Queries
- `getUser(id: ID!)` - Get user by ID
- `getUserByEmail(email: String!)` - Get user by email
- `listUsers(skip: Int, limit: Int)` - List users with pagination

### Mutations
- `createUser(input: CreateUserInput!)` - Create a new user
- `updateUser(id: ID!, input: UpdateUserInput!)` - Update user
- `deleteUser(id: ID!)` - Delete user

## Example Queries

### Get User
```graphql
query GetUser {
  getUser(id: "user-id") {
    id
    email
    firstName
    lastName
    phone
    status
    roles
    createdAt
    updatedAt
  }
}
```

### Create User
```graphql
mutation CreateUser {
  createUser(input: {
    firstName: "John"
    lastName: "Doe"
    email: "john.doe@example.com"
    phone: "+1234567890"
    roles: [CONTRACTOR]
  }) {
    id
    email
    firstName
    lastName
    status
    roles
  }
}
```

### List Users
```graphql
query ListUsers {
  listUsers(skip: 0, limit: 10) {
    items {
      id
      email
      firstName
      lastName
      status
      roles
    }
    pagination {
      skip
      limit
      hasMore
    }
  }
}
```

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

## Architecture

The server integrates with the existing clean architecture:

```
server/
├── app.py              # Flask GraphQL server
├── config.py           # Configuration management
├── init_db.py          # Database initialization
├── requirements.txt    # Server dependencies
└── env.example         # Environment variables template

src/                    # Existing clean architecture
├── handlers/           # Lambda handlers
├── resolvers/          # Resolver configurations
├── application/        # Application layer
├── domain/             # Domain layer
└── orm/                # ORM layer
```

## Development

The server uses the existing resolver configurations and handlers from the `src` folder, providing a seamless integration between the Lambda handler pattern and the Flask GraphQL server.

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in environment
2. Use a production WSGI server like Gunicorn
3. Configure proper database connection
4. Set secure `SECRET_KEY`
5. Configure reverse proxy (nginx)

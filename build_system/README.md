# Build System

This build system compiles GraphQL schemas for AWS AppSync deployment.

## Overview

The build system processes GraphQL schema files from the `src/api/graphql/apps/` directory and creates compiled schemas in the `build/appsync/` directory. It handles import resolution, schema validation, and dependency management.

## Features

- **Import Resolution**: Automatically resolves GraphQL imports and combines multiple files into a single schema
- **Schema Validation**: Validates compiled schemas for syntax errors and duplicate definitions
- **Circular Import Detection**: Prevents infinite loops from circular imports
- **Clean Build**: Automatically cleans previous build artifacts before building
- **Verbose Logging**: Optional detailed logging for debugging

## Usage

### Basic Usage

```bash
# From the build_system directory
python3 build.py

# Or from the project root
python3 build_system/build.py
```

### Advanced Usage

```bash
# Enable verbose logging
python3 build.py --verbose

# Clean build artifacts only
python3 build.py --clean-only

# Specify custom project root
python3 build.py --project-root /path/to/project
```

## Project Structure

```
src/api/graphql/
├── apps/                    # Main schema files
│   └── haulink_app.graphql  # Main app schema with imports
├── common/                  # Shared types and utilities
│   └── types.graphql        # Common types (pagination, filters, etc.)
└── models/                  # Entity schemas
    ├── user.graphql         # User entity schema
    └── order.graphql        # Order entity schema

build/
└── appsync/                 # Compiled schemas
    └── haulink_app.graphql  # Combined schema ready for AppSync
```

## GraphQL Import Syntax

The build system supports a custom import syntax for combining GraphQL files:

```graphql
# Import other GraphQL files
import "./common/types.graphql"
import "./models/user.graphql"
import "./models/order.graphql"
```

### Import Rules

- Imports must use double quotes: `import "path"`
- Relative paths start with `./` and are resolved from the GraphQL directory root
- Absolute paths are resolved from the GraphQL directory root
- Circular imports are detected and handled gracefully
- Imported content is included with comment headers indicating the source

## Build Process

1. **Clean**: Remove previous build artifacts
2. **Prepare**: Create necessary build directories
3. **Discover**: Find all GraphQL schema files in the apps directory
4. **Build**: Process each schema file:
   - Resolve imports recursively
   - Combine all imported content
   - Validate the final schema
   - Write to build directory
5. **Summary**: Display build results

## Error Handling

The build system provides detailed error messages for:

- Missing import files
- Circular import detection
- Schema validation failures
- File read/write errors
- Duplicate type definitions
- Syntax errors (mismatched braces)

## Configuration

The build system automatically detects the project structure. Key configuration points:

- **GraphQL Directory**: `src/api/graphql/`
- **Build Directory**: `build/appsync/`
- **Apps Directory**: `src/api/graphql/apps/`

## Example Output

```
═════════════════════════════════════
STEP 1: CLEAN BUILD ENVIRONMENT
═════════════════════════════════════

✅ Build artifacts cleaned

═════════════════════════════════════
STEP 2: PREPARE BUILD ENVIRONMENT
═════════════════════════════════════

✅ Build directories ready

═════════════════════════════════════
STEP 3: BUILD APPSYNC SCHEMAS
═════════════════════════════════════

ℹ️  Found 1 AppSync Schemas
  haulink_app: ℹ️  Building schema: haulink_app
✅ Built schema: haulink_app (3 files processed)
✅ Successfully built 1 AppSync Schemas

═════════════════════════════════════
STEP 4: BUILD SUMMARY
═════════════════════════════════════

  Artifacts: ℹ️  AppSync Schemas: 1
  Location: ℹ️  Build Directory: /path/to/build
✅ All artifacts built successfully!
```

## Integration

The compiled schemas in `build/appsync/` are ready for deployment to AWS AppSync. Each schema file contains a complete, self-contained GraphQL schema with all imports resolved.

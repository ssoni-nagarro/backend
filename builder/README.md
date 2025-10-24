# AWS Deployment Builder

A comprehensive build system that transforms source code into AWS-compatible deployment artifacts for serverless applications.

## Overview

The AWS Deployment Builder is a modular build system designed to convert source code into production-ready artifacts for AWS services. It automates the packaging, compilation, and optimization of various components required for AWS serverless deployments.

## Core Capabilities

### 🏗️ **Multi-Service Build Support**
- **AWS Lambda Functions**: Packages Python handlers into deployable ZIP files
- **AWS Lambda Layers**: Creates reusable dependency layers for Lambda functions
- **AWS AppSync Schemas**: Compiles GraphQL schemas with import resolution and validation

### 🔧 **Intelligent Processing**
- **Dependency Resolution**: Automatically includes required dependencies and modules
- **Import Resolution**: Resolves and combines GraphQL imports into single schemas
- **Circular Import Detection**: Prevents infinite loops and handles complex dependencies
- **Schema Validation**: Validates compiled schemas for syntax errors and consistency
- **Clean Build Process**: Ensures fresh builds by cleaning previous artifacts

### 📦 **Artifact Generation**
- **Lambda Packages**: Self-contained ZIP files ready for AWS Lambda deployment
- **Layer Packages**: Optimized dependency bundles for Lambda layer distribution
- **Compiled Schemas**: Complete GraphQL schemas with all imports resolved

## Architecture

The builder follows a modular architecture with specialized components:

```
BuilderManager (Orchestrator)
├── LambdaBuilder (Function Packaging)
├── LayerBuilder (Dependency Layers)
└── AppSyncBuilder (Schema Compilation)
```

### **BuilderManager**
- Orchestrates the entire build process
- Manages build environment and cleanup
- Coordinates between different builders
- Provides unified logging and error handling

### **LambdaBuilder**
- Discovers Python handler files
- Packages handlers with dependencies
- Creates deployment-ready ZIP files
- Handles Python path resolution

### **LayerBuilder**
- Identifies reusable dependencies
- Creates optimized layer packages
- Manages dependency conflicts
- Generates layer-compatible structures

### **AppSyncBuilder**
- Processes GraphQL schema files
- Resolves import statements
- Validates schema syntax
- Combines multiple files into single schemas

## Usage

### **Basic Build**
```bash
# Build all artifacts
python3 builder/main.py

# Or from project root
python3 builder/main.py
```

### **Advanced Options**
```bash
# Enable verbose logging
python3 builder/main.py --verbose

# Clean build artifacts only
python3 builder/main.py --clean

# Specify custom project root
python3 builder/main.py --project-root /path/to/project
```

## Project Structure

The builder expects the following project structure:

```
project/
├── src/
│   ├── handlers/           # Lambda function handlers
│   │   └── *.py           # Python handler files
│   ├── api/graphql/       # GraphQL schemas
│   │   ├── apps/          # Main schema files
│   │   ├── common/        # Shared types
│   │   └── models/        # Entity schemas
│   ├── adapters/          # Database adapters
│   └── utils/             # Utility modules
└── build/                 # Generated artifacts
    ├── lambdas/           # Lambda ZIP files
    ├── layers/            # Layer ZIP files
    └── appsync/           # Compiled schemas
```

## Build Process

### **Step 1: Environment Cleanup**
- Removes previous build artifacts
- Cleans temporary extraction directories
- Ensures fresh build environment

### **Step 2: Environment Preparation**
- Creates necessary build directories
- Validates project structure
- Initializes build configuration

### **Step 3: Lambda Layer Building**
- Discovers reusable dependencies
- Packages dependencies into layers
- Optimizes for Lambda layer requirements

### **Step 4: Lambda Function Building**
- Discovers handler files
- Packages handlers with dependencies
- Creates deployment-ready ZIP files

### **Step 5: AppSync Schema Building**
- Processes GraphQL schema files
- Resolves import statements recursively
- Validates final schemas
- Generates compiled schemas

### **Step 6: Build Summary**
- Reports build statistics
- Lists generated artifacts
- Confirms successful completion

## GraphQL Import System

The builder supports a custom GraphQL import syntax for modular schema development:

```graphql
# Import other GraphQL files
import "./common/types.graphql"
import "./models/user.graphql"
import "./models/order.graphql"
```

### **Import Features**
- **Relative Paths**: Use `./` for relative imports
- **Absolute Paths**: Resolved from GraphQL directory root
- **Circular Detection**: Prevents infinite import loops
- **Source Attribution**: Includes comment headers for imported content
- **Validation**: Ensures imported schemas are syntactically correct

## Error Handling

The builder provides comprehensive error reporting for:

- **Missing Files**: Import resolution failures
- **Circular Dependencies**: Infinite loop detection
- **Schema Validation**: Syntax and consistency errors
- **File Operations**: Read/write permission issues
- **Duplicate Definitions**: Conflicting type definitions
- **Dependency Issues**: Missing or conflicting packages

## Configuration

### **Automatic Detection**
The builder automatically detects:
- Project root directory
- Source code structure
- Build requirements
- Dependencies and imports

### **Custom Configuration**
Key configuration points:
- **Project Root**: `--project-root` parameter
- **Source Directory**: `src/` (configurable)
- **Build Directory**: `build/` (configurable)
- **Verbose Logging**: `--verbose` flag

## Output Examples

### **Successful Build**
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
STEP 3: BUILD LAMBDA LAYERS
═════════════════════════════════════
ℹ️  Found 2 Lambda Layers
  dependencies: ✅ Built layer: dependencies
  utils: ✅ Built layer: utils
✅ Successfully built 2 Lambda Layers

═════════════════════════════════════
STEP 4: BUILD LAMBDA FUNCTIONS
═════════════════════════════════════
ℹ️  Found 3 Lambda Functions
  user_handler: ✅ Built function: user_handler
  order_handler: ✅ Built function: order_handler
  notification_handler: ✅ Built function: notification_handler
✅ Successfully built 3 Lambda Functions

═════════════════════════════════════
STEP 5: BUILD APPSYNC SCHEMAS
═════════════════════════════════════
ℹ️  Found 1 AppSync Schemas
  main_app: ✅ Built schema: main_app (5 files processed)
✅ Successfully built 1 AppSync Schemas

═════════════════════════════════════
STEP 6: BUILD SUMMARY
═════════════════════════════════════
  Artifacts: ℹ️  Lambda Functions: 3
  Artifacts: ℹ️  Lambda Layers: 2
  Artifacts: ℹ️  AppSync Schemas: 1
  Location: ℹ️  Build Directory: /path/to/build
✅ All artifacts built successfully!
```

## Integration

### **AWS Deployment Ready**
All generated artifacts are immediately ready for AWS deployment:
- **Lambda Functions**: Upload directly to AWS Lambda
- **Lambda Layers**: Deploy as Lambda layers
- **AppSync Schemas**: Import into AWS AppSync

### **CI/CD Integration**
The builder integrates seamlessly with:
- **GitHub Actions**: Automated builds on code changes
- **AWS CodePipeline**: Continuous deployment workflows
- **Local Development**: Fast iteration and testing

### **Development Workflow**
1. **Develop**: Write handlers and schemas in `src/`
2. **Build**: Run `python3 builder/main.py`
3. **Deploy**: Use generated artifacts in `build/`
4. **Iterate**: Repeat as needed

## Benefits

### **🚀 Production Ready**
- Optimized for AWS serverless architecture
- Handles complex dependency management
- Ensures consistent build outputs

### **🔧 Developer Friendly**
- Simple command-line interface
- Comprehensive error reporting
- Automatic project detection

### **⚡ Efficient**
- Incremental build support
- Dependency caching
- Parallel processing where possible

### **🛡️ Reliable**
- Comprehensive validation
- Error prevention
- Consistent output format

This build system transforms your source code into AWS-compatible artifacts, making serverless deployment simple and reliable.

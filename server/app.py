"""Flask GraphQL Server with Dynamic Resolvers"""
import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import graphene
from graphene import ObjectType, String, ID, List, Field, Int, Boolean, DateTime
from datetime import datetime
import json
from typing import Dict, Any, Optional

# Add src to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from resolver_factory import resolver_factory

app = Flask(__name__)
CORS(app)

# GraphQL Schema Definition
class UserStatus(graphene.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    DELETED = "DELETED"

class UserRole(graphene.Enum):
    ADMIN = "ADMIN"
    CONTRACTOR = "CONTRACTOR"
    HAULER = "HAULER"
    SUBHAULER = "SUBHAULER"

class User(graphene.ObjectType):
    id = ID(required=True)
    email = String(required=True)
    firstName = String(required=True)
    lastName = String(required=True)
    phone = String()
    status = UserStatus(required=True)
    roles = List(UserRole, required=True)
    createdAt = DateTime(required=True)
    updatedAt = DateTime(required=True)

class PaginationResult(graphene.ObjectType):
    skip = Int(required=True)
    limit = Int(required=True)
    hasMore = Boolean(required=True)

class UserQueryResult(graphene.ObjectType):
    items = List(User, required=True)
    pagination = Field(PaginationResult)

class CreateUserInput(graphene.InputObjectType):
    firstName = String(required=True)
    lastName = String(required=True)
    email = String(required=True)
    phone = String()
    roles = List(UserRole)

class UpdateUserInput(graphene.InputObjectType):
    firstName = String()
    lastName = String()
    phone = String()
    status = UserStatus()

# Dynamic Query and Mutation classes will be created in create_dynamic_schema()

def create_dynamic_schema():
    """Create GraphQL schema dynamically from resolver configs"""
    # Get all resolvers from factory
    resolvers = resolver_factory.create_resolvers()
    
    # Get field metadata
    field_metadata = resolver_factory.get_field_metadata()
    
    # Create dynamic query and mutation classes with fields
    query_fields = {}
    mutation_fields = {}
    
    for resolver_key, resolver_func in resolvers.items():
        if resolver_key.startswith("Query_"):
            field_name = resolver_key.replace("Query_", "")
            
            # Get field metadata
            metadata = field_metadata.get(resolver_key, {})
            if not metadata:
                continue
            
            # Create field based on metadata
            field = create_field_from_metadata(metadata)
            if field:
                query_fields[field_name] = field
            
        elif resolver_key.startswith("Mutation_"):
            field_name = resolver_key.replace("Mutation_", "")
            
            # Get field metadata
            metadata = field_metadata.get(resolver_key, {})
            if not metadata:
                continue
            
            # Create field based on metadata
            field = create_field_from_metadata(metadata)
            if field:
                mutation_fields[field_name] = field
    
    # Create resolver methods
    resolver_methods = {}
    for resolver_key, resolver_func in resolvers.items():
        if resolver_key.startswith("Query_"):
            field_name = resolver_key.replace("Query_", "")
            resolver_methods[f"resolve_{field_name}"] = resolver_func
        elif resolver_key.startswith("Mutation_"):
            field_name = resolver_key.replace("Mutation_", "")
            resolver_methods[f"resolve_{field_name}"] = resolver_func
    
    # Create dynamic classes using type()
    DynamicQuery = type('DynamicQuery', (ObjectType,), {**query_fields, **resolver_methods})
    DynamicMutation = type('DynamicMutation', (ObjectType,), {**mutation_fields, **resolver_methods})
    
    # Create schema
    schema = graphene.Schema(
        query=DynamicQuery,
        mutation=DynamicMutation,
        types=[User, UserStatus, UserRole, CreateUserInput, UpdateUserInput, UserQueryResult, PaginationResult]
    )
    
    return schema

def create_field_from_metadata(metadata: Dict[str, Any]) -> Optional[Field]:
    """Create a GraphQL field from metadata"""
    try:
        return_type = metadata.get("return_type")
        arguments = metadata.get("arguments", {})
        
        if not return_type:
            return None
        
        # Get the actual type class
        type_class = get_type_class(return_type)
        if not type_class:
            return None
        
        # Create field arguments
        field_args = {}
        for arg_name, arg_meta in arguments.items():
            arg_type = get_type_class(arg_meta["type"])
            if arg_type:
                if arg_meta.get("required", False):
                    field_args[arg_name] = arg_type(required=True)
                else:
                    default_value = arg_meta.get("default")
                    field_args[arg_name] = arg_type(default_value=default_value)
        
        # Create the field
        if field_args:
            return Field(type_class, **field_args)
        else:
            return Field(type_class)
    
    except Exception as e:
        print(f"Error creating field from metadata: {e}")
        return None

def get_type_class(type_name: str):
    """Get the actual GraphQL type class from type name"""
    type_mapping = {
        "User": User,
        "UserQueryResult": UserQueryResult,
        "CreateUserInput": CreateUserInput,
        "UpdateUserInput": UpdateUserInput,
        "String": String,
        "ID": ID,
        "Int": Int,
        "Boolean": Boolean,
        "DateTime": DateTime,
        "UserStatus": UserStatus,
        "UserRole": UserRole,
        "PaginationResult": PaginationResult
    }
    
    return type_mapping.get(type_name)

# Create schema
schema = create_dynamic_schema()

@app.route('/graphql', methods=['GET', 'POST'])
def graphql():
    """GraphQL endpoint"""
    if request.method == 'GET':
        # Return GraphiQL interface
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>GraphiQL</title>
            <link href="https://unpkg.com/graphiql@3/graphiql.min.css" rel="stylesheet" />
            <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
            <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
            <script src="https://unpkg.com/graphiql@3/graphiql.min.js"></script>
        </head>
        <body style="margin: 0;">
            <div id="graphiql" style="height: 100vh;"></div>
            <script>
                const fetcher = (params) => {
                    return fetch('/graphql', {
                        method: 'post',
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(params),
                    }).then(response => response.json());
                };
                
                ReactDOM.render(
                    React.createElement(GraphiQL, {
                        fetcher: fetcher,
                        defaultQuery: `# Welcome to GraphiQL
# 
# GraphiQL is an in-browser tool for writing, validating, and
# testing GraphQL queries.
#
# Type queries into this side of the screen, and you will see intelligent
# typeaheads aware of the current GraphQL type schema and live syntax and
# validation errors highlighted within the text.
#
# GraphQL queries typically start with a "{" character. Lines that start
# with a # are ignored.
#
# An example GraphQL query might look like:
#
#     {
#       getUser(id: "test-user-id") {
#         id
#         email
#         firstName
#         lastName
#         status
#         roles
#       }
#     }
#
# Run the query by pressing the play button or Ctrl+Enter.
#
# For more information about GraphQL, visit https://graphql.org/learn/
#
# To learn more about GraphiQL, visit https://github.com/graphql/graphiql
#
# To learn more about this GraphQL server, visit https://github.com/graphql-python/flask-graphql

query GetUser {
  getUser(id: "test-user-id") {
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
}`,
                    }),
                    document.getElementById('graphiql')
                );
            </script>
        </body>
        </html>
        ''', 200, {'Content-Type': 'text/html'}
    
    elif request.method == 'POST':
        # Handle GraphQL queries
        data = request.get_json()
        query = data.get('query')
        variables = data.get('variables')
        
        try:
            result = schema.execute(query, variables=variables)
            
            if result.errors:
                return jsonify({
                    'data': result.data,
                    'errors': [{'message': str(error)} for error in result.errors]
                }), 400
            
            return jsonify({
                'data': result.data
            })
        except Exception as e:
            return jsonify({
                'errors': [{'message': str(e)}]
            }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'GraphQL API Server',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/')
def index():
    """Root endpoint with API information"""
    return jsonify({
        'message': 'HauLink GraphQL API Server',
        'version': '1.0.0',
        'endpoints': {
            'graphql': '/graphql',
            'graphiql': '/graphql (GET)',
            'health': '/health'
        },
        'documentation': 'Visit /graphql for GraphiQL playground'
    })

if __name__ == '__main__':
    print("🚀 Starting HauLink GraphQL Server...")
    print("📡 GraphQL endpoint: http://localhost:5000/graphql")
    print("🎮 GraphiQL playground: http://localhost:5000/graphql")
    print("❤️  Health check: http://localhost:5000/health")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

"""Flask GraphQL Server with Ariadne"""
import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from ariadne import make_executable_schema, load_schema_from_path, QueryType, MutationType, graphql_sync
from datetime import datetime
import json
from typing import Dict, Any, Optional

# Add src to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from resolver_factory import resolver_factory

app = Flask(__name__)
CORS(app)

# Load GraphQL schema from single schema file
schema_file = os.path.join(os.path.dirname(__file__), '..', 'src', 'api', 'graphql', 'schema.graphql')
with open(schema_file, 'r') as f:
    type_defs = f.read()

# Create Query and Mutation types
query = QueryType()
mutation = MutationType()

def setup_resolvers():
    """Setup resolvers from resolver factory"""
    # Get all resolvers from factory
    resolvers = resolver_factory.create_resolvers()
    
    for resolver_key, resolver_func in resolvers.items():
        if resolver_key.startswith("Query_"):
            field_name = resolver_key.replace("Query_", "")
            query.set_field(field_name, resolver_func)
        elif resolver_key.startswith("Mutation_"):
            field_name = resolver_key.replace("Mutation_", "")
            mutation.set_field(field_name, resolver_func)

# Setup resolvers
setup_resolvers()

# Create executable schema
schema = make_executable_schema(type_defs, query, mutation)

@app.route('/graphql', methods=['GET', 'POST'])
def graphql():
    """GraphQL endpoint"""
    if request.method == 'GET':
        # Return GraphQL Playground HTML
        playground_html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>GraphQL Playground</title>
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
                        defaultQuery: `
                        # Welcome to GraphQL Playground
                        # 
                        # This playground allows you to test GraphQL queries and mutations.
                        # The schema is loaded directly from src/api/graphql files.
                        #
                        # Example query:
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
        '''
        return playground_html, 200, {'Content-Type': 'text/html'}
    
    elif request.method == 'POST':
        # Handle GraphQL queries
        data = request.get_json()
        
        try:
            success, result = graphql_sync(schema, data, debug=True)
            
            status_code = 200 if success else 400
            return jsonify(result), status_code
            
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
            'playground': '/graphql (GET)',
            'health': '/health'
        },
        'documentation': 'Visit /graphql for GraphQL Playground'
    })

# Server startup is handled in main.py

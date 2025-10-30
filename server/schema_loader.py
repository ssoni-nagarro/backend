"""GraphQL Schema Loader for loading schema from .graphql files with import support"""
import os
import sys
from pathlib import Path
from typing import Dict, Set, List, Optional
import re

# Add src to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def compile_graphql_schema(base_file_path: str) -> str:
    """
    Compile GraphQL schema by resolving import statements
    """
    def resolve_imports(content: str, base_path: Path, processed_files: Set[str] = None) -> str:
        if processed_files is None:
            processed_files = set()
        
        # Find all import statements
        import_pattern = r'import\s+"([^"]+)"'
        imports = re.findall(import_pattern, content)
        
        for import_path in imports:
            # Resolve the import path relative to the current file
            if import_path.startswith('./'):
                import_file = base_path.parent / import_path[2:]
            else:
                import_file = base_path.parent / import_path
            
            # Avoid circular imports
            if str(import_file) in processed_files:
                continue
            
            processed_files.add(str(import_file))
            
            # Read the imported file
            try:
                with open(import_file, 'r') as f:
                    imported_content = f.read()
                
                # Recursively resolve imports in the imported file
                imported_content = resolve_imports(imported_content, import_file, processed_files)
                
                # Replace the import statement with the imported content
                import_statement = f'import "{import_path}"'
                content = content.replace(import_statement, imported_content)
                
            except FileNotFoundError:
                print(f"Warning: Could not find import file: {import_file}")
                # Remove the import statement
                import_statement = f'import "{import_path}"'
                content = content.replace(import_statement, '')
        
        return content
    
    # Load the main schema file
    base_path = Path(base_file_path)
    with open(base_path, 'r') as f:
        schema_content = f.read()
    
    # Resolve all imports
    compiled_schema = resolve_imports(schema_content, base_path)
    
    # Clean up any remaining import statements and comments
    compiled_schema = re.sub(r'import\s+"[^"]+"\s*\n?', '', compiled_schema)
    compiled_schema = re.sub(r'#.*\n', '\n', compiled_schema)
    
    return compiled_schema


class GraphQLSchemaLoader:
    """Loads and processes GraphQL schema from .graphql files with import support"""
    
    def __init__(self, graphql_dir: str = "./src/api/graphql"):
        self.graphql_dir = Path(__file__).parent.parent / graphql_dir
        self.processed_files: Set[str] = set()
        
    def load_schema(self, schema_name: str = "haulink_app") -> str:
        """Load and combine GraphQL schema from files using the compile_graphql_schema function"""
        schema_file = self.graphql_dir / f"{schema_name}.graphql"

        if not schema_file.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_file}")
        
        # Use the compile_graphql_schema function
        return compile_graphql_schema(str(schema_file))
    
    def get_schema_info(self) -> Dict[str, any]:
        """Get information about the loaded schema"""
        return {
            'graphql_dir': str(self.graphql_dir),
            'processed_files': list(self.processed_files)
        }

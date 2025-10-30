"""AppSync schema builder"""
from pathlib import Path
from typing import List, Set, Dict
import re
from .base_builder import BaseBuilder

class AppSyncBuilder(BaseBuilder):
    """Builds AppSync GraphQL schemas"""
    
    def discover(self) -> List[str]:
        """Discover GraphQL schemas"""
        schemas = []
        
        if not self.config.graphql_dir.exists():
            self.logger.warning(f"GraphQL directory not found: {self.config.graphql_dir}")
            return schemas
        
        # Discover all .graphql files directly in the graphql_dir (excluding subdirectories)
        for schema_file in self.config.graphql_dir.glob("*.graphql"):
            schemas.append(schema_file.stem)
        
        if not schemas:
            self.logger.warning(f"No GraphQL schema files found in: {self.config.graphql_dir}")
        
        return sorted(schemas)
    
    def build(self, schema_name: str) -> bool:
        """Build a GraphQL schema by combining imports"""
        try:
            self.logger.info(f"Building schema: {schema_name}", schema_name)
            
            schema_file = self.config.graphql_dir / f"{schema_name}.graphql"
            output_file = self.config.appsync_dir / f"{schema_name}.graphql"
            
            if not schema_file.exists():
                self.logger.error(f"Schema file not found: {schema_file}")
                return False
            
            # Process schema and resolve imports
            processed_files: Set[str] = set()
            import_map: Dict[str, str] = {}
            combined_schema = self._process_schema(schema_file, processed_files, import_map)
            
            # Validate the combined schema
            if not self._validate_schema(combined_schema, schema_name):
                return False
            
            # Write combined schema
            output_file.write_text(combined_schema, encoding='utf-8')
            
            self.logger.success(f"Built schema: {schema_name} ({len(processed_files)} files processed)")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to build schema {schema_name}: {e}")
            return False
    
    def _process_schema(self, file_path: Path, processed: Set[str], import_map: Dict[str, str]) -> str:
        """Recursively process schema files and resolve imports"""
        file_key = str(file_path.resolve())
        
        if file_key in processed:
            self.logger.debug(f"Circular import detected: {file_path.name}")
            return ""
        
        processed.add(file_key)
        
        if not file_path.exists():
            self.logger.error(f"Import file not found: {file_path}")
            raise FileNotFoundError(f"Import file not found: {file_path}")
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            self.logger.error(f"Failed to read file {file_path}: {e}")
            raise
        
        output_lines = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped.startswith('import "'):
                import_path = stripped[8:-1]
                
                # Resolve import path relative to GraphQL directory
                if import_path.startswith('./'):
                    # For relative imports, resolve from the GraphQL directory root
                    full_path = self.config.graphql_dir / import_path[2:]
                else:
                    full_path = self.config.graphql_dir / import_path
                
                self.logger.debug(f"Resolving import: {import_path} -> {full_path}")
                
                try:
                    imported_content = self._process_schema(full_path, processed, import_map)
                    if imported_content.strip():
                        output_lines.append(f"# Imported from {import_path}")
                        output_lines.extend(imported_content.split('\n'))
                        output_lines.append("")  # Add blank line after import
                except Exception as e:
                    self.logger.error(f"Failed to process import {import_path} in {file_path.name}:{line_num}: {e}")
                    raise
            else:
                output_lines.append(line)
        
        return '\n'.join(output_lines)
    
    def _validate_schema(self, schema_content: str, schema_name: str) -> bool:
        """Basic validation of the compiled GraphQL schema"""
        try:
            # Check for basic GraphQL structure
            if not schema_content.strip():
                self.logger.error(f"Empty schema generated for {schema_name}")
                return False
            
            # Check for required GraphQL elements
            has_query = 'type Query' in schema_content
            has_mutation = 'type Mutation' in schema_content
            
            if not has_query and not has_mutation:
                self.logger.warning(f"Schema {schema_name} has no Query or Mutation types")
            
            # Check for duplicate type definitions
            type_definitions = re.findall(r'type\s+(\w+)', schema_content)
            duplicate_types = [t for t in set(type_definitions) if type_definitions.count(t) > 1]
            
            if duplicate_types:
                self.logger.error(f"Duplicate type definitions found in {schema_name}: {duplicate_types}")
                return False
            
            # Check for syntax issues
            if schema_content.count('{') != schema_content.count('}'):
                self.logger.error(f"Mismatched braces in schema {schema_name}")
                return False
            
            self.logger.debug(f"Schema validation passed for {schema_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Schema validation failed for {schema_name}: {e}")
            return False

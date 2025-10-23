"""Dynamic GraphQL Resolver Factory"""
import sys
import os
from typing import Dict, Any, Optional, Callable, List, Tuple
from graphene import ObjectType, Field, String, ID, List, Int, Boolean, DateTime
from datetime import datetime
import asyncio

# Add src to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from resolver_loader import ConfigLoader
from handlers.user_handler import handler as user_handler

class DynamicResolverFactory:
    """Factory for creating GraphQL resolvers dynamically from config"""
    
    def __init__(self):
        self.config_loader = ConfigLoader("src/api/resolvers")
        self.handlers = {
            "user_handler": user_handler
            # Add more handlers as needed
        }
    
    def get_field_metadata(self) -> Dict[str, Dict[str, Any]]:
        """Get field metadata for all operations from config"""
        field_metadata = {}
        
        # Get all handlers
        handlers = self.config_loader.list_handlers()
        
        for handler_name in handlers:
            config = self.config_loader.load_config(handler_name)
            if not config:
                continue
            
            # Get resolver configs for this handler
            resolver_configs = config.get("resolvers", {})
            
            for service_name, service_config in resolver_configs.items():
                operations = service_config.get("operations", [])
                
                for operation in operations:
                    type_name = operation.get("typeName")
                    field_name = operation.get("fieldName")
                    
                    if not type_name or not field_name:
                        continue
                    
                    # Create field key
                    field_key = f"{type_name}_{field_name}"
                    
                    # Determine field metadata based on field name patterns
                    field_metadata[field_key] = self._determine_field_metadata(field_name, type_name)
        
        return field_metadata
    
    def _determine_field_metadata(self, field_name: str, type_name: str) -> Dict[str, Any]:
        """Determine field metadata based on field name patterns"""
        metadata = {
            "field_name": field_name,
            "type_name": type_name,
            "return_type": None,
            "arguments": {}
        }
        
        # Query field patterns
        if type_name == "Query":
            if field_name == "getUser":
                metadata["return_type"] = "User"
                metadata["arguments"] = {"id": {"type": "ID", "required": True}}
            elif field_name == "getUserByEmail":
                metadata["return_type"] = "User"
                metadata["arguments"] = {"email": {"type": "String", "required": True}}
            elif field_name == "listUsers":
                metadata["return_type"] = "UserQueryResult"
                metadata["arguments"] = {
                    "skip": {"type": "Int", "required": False, "default": 0},
                    "limit": {"type": "Int", "required": False, "default": 100}
                }
        
        # Mutation field patterns
        elif type_name == "Mutation":
            if field_name == "createUser":
                metadata["return_type"] = "User"
                metadata["arguments"] = {"input": {"type": "CreateUserInput", "required": True}}
            elif field_name == "updateUser":
                metadata["return_type"] = "User"
                metadata["arguments"] = {
                    "id": {"type": "ID", "required": True},
                    "input": {"type": "UpdateUserInput", "required": True}
                }
            elif field_name == "deleteUser":
                metadata["return_type"] = "Boolean"
                metadata["arguments"] = {"id": {"type": "ID", "required": True}}
        
        return metadata
    
    def create_resolvers(self) -> Dict[str, Any]:
        """Create all resolvers dynamically from config"""
        resolvers = {}
        
        # Get all handlers
        handlers = self.config_loader.list_handlers()
        
        for handler_name in handlers:
            config = self.config_loader.load_config(handler_name)
            if not config:
                continue
            
            # Get resolver configs for this handler
            resolver_configs = config.get("resolvers", {})
            
            for service_name, service_config in resolver_configs.items():
                operations = service_config.get("operations", [])
                
                for operation in operations:
                    type_name = operation.get("typeName")
                    field_name = operation.get("fieldName")
                    
                    if not type_name or not field_name:
                        continue
                    
                    # Create resolver key
                    resolver_key = f"{type_name}_{field_name}"
                    
                    # Create resolver function
                    resolver_func = self._create_resolver_function(
                        handler_name, field_name, type_name
                    )
                    
                    resolvers[resolver_key] = resolver_func
        
        return resolvers
    
    def _create_resolver_function(self, handler_name: str, field_name: str, type_name: str) -> Callable:
        """Create a resolver function for a specific operation"""
        
        # Capture the handler in the closure
        handler = self.handlers.get(handler_name)
        if not handler:
            raise Exception(f"Handler {handler_name} not found")
        
        def resolver_func(self, info, **kwargs):
            """Dynamic resolver function"""
            try:
                # Create event in the format expected by our handler
                event = {
                    "payload": {
                        "ctx": {
                            "info": {
                                "fieldName": field_name,
                                "parentTypeName": type_name
                            },
                            "arguments": kwargs,
                            "identity": {
                                "sub": "flask-user",
                                "username": "flask-dev"
                            }
                        }
                    }
                }
                
                # Call the handler (now synchronous for Lambda optimization)
                result = handler(event, {})
                
                if "error" in result:
                    raise Exception(result["error"])
                
                return result
            
            except Exception as e:
                raise Exception(f"Failed to execute {field_name}: {str(e)}")
        
        return resolver_func
    
    def get_handler_info(self) -> Dict[str, Any]:
        """Get information about available handlers and operations"""
        info = {
            "handlers": [],
            "operations": []
        }
        
        handlers = self.config_loader.list_handlers()
        
        for handler_name in handlers:
            config = self.config_loader.load_config(handler_name)
            if config:
                info["handlers"].append({
                    "name": handler_name,
                    "description": config.get("description", ""),
                    "datasource": config.get("datasource", {})
                })
                
                # Extract operations
                resolver_configs = config.get("resolvers", {})
                for service_name, service_config in resolver_configs.items():
                    operations = service_config.get("operations", [])
                    for op in operations:
                        info["operations"].append({
                            "handler": handler_name,
                            "service": service_name,
                            "type": op.get("typeName"),
                            "field": op.get("fieldName"),
                            "description": op.get("tags", {}).get("Operation", "")
                        })
        
        return info

# Global factory instance
resolver_factory = DynamicResolverFactory()

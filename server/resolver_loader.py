"""Resolver loader for declarative GraphQL resolver configs"""
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

class ResolverLoader:
    """Loads and manages declarative configuration for GraphQL resolvers"""
    
    def __init__(self, resolver_path: str = "config"):
        self.resolver_path = Path(resolver_path)
        self._resolvers = {}
    
    def load_resolver(self, handler_name: str) -> Optional[Dict[str, Any]]:
        """Load resolver configuration for a specific handler"""
        resolver_file = self.resolver_path / f"{handler_name}_resolver.json"
        
        if not resolver_file.exists():
            return None
        
        try:
            with open(resolver_file, 'r') as f:
                resolver = json.load(f)
                self._resolvers[handler_name] = resolver
                return resolver
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading resolver for {handler_name}: {e}")
            return None
    
    def get_resolver_config(self, handler_name: str, service_name: str) -> Optional[Dict[str, Any]]:
        """Get resolver configuration for a specific handler and service"""
        resolver = self._resolvers.get(handler_name)
        if not resolver:
            resolver = self.load_resolver(handler_name)
        
        if not resolver:
            return None
        
        return resolver.get("resolvers", {}).get(service_name)
    
    def get_operation_resolver(self, handler_name: str, service_name: str, 
                           type_name: str, field_name: str) -> Optional[Dict[str, Any]]:
        """Get specific operation resolver configuration"""
        resolver_config = self.get_resolver_config(handler_name, service_name)
        if not resolver_config:
            return None
        
        operations = resolver_config.get("operations", [])
        for operation in operations:
            if (operation.get("typeName") == type_name and 
                operation.get("fieldName") == field_name):
                return operation
        
        return None
    
    def list_handlers(self) -> list:
        """List all available handler resolvers"""
        handlers = []
        for resolver_file in self.resolver_path.glob("*_resolver.json"):
            handler_name = resolver_file.stem.replace("_resolver", "")
            handlers.append(handler_name)
        return handlers

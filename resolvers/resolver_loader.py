"""Resolver loader for declarative GraphQL resolver configs"""
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

class ResolverLoader:
    """Loads and manages declarative configuration for GraphQL resolvers"""
    
    def __init__(self, config_path: str = "config"):
        self.config_path = Path(config_path)
        self._configs = {}
    
    def load_config(self, handler_name: str) -> Optional[Dict[str, Any]]:
        """Load configuration for a specific handler"""
        config_file = self.config_path / f"{handler_name}_resolver.json"
        
        if not config_file.exists():
            return None
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                self._configs[handler_name] = config
                return config
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading config for {handler_name}: {e}")
            return None
    
    def get_resolver_config(self, handler_name: str, service_name: str) -> Optional[Dict[str, Any]]:
        """Get resolver configuration for a specific handler and service"""
        config = self._configs.get(handler_name)
        if not config:
            config = self.load_config(handler_name)
        
        if not config:
            return None
        
        return config.get("resolvers", {}).get(service_name)
    
    def get_operation_config(self, handler_name: str, service_name: str, 
                           type_name: str, field_name: str) -> Optional[Dict[str, Any]]:
        """Get specific operation configuration"""
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
        """List all available handler configurations"""
        handlers = []
        for config_file in self.config_path.glob("*_resolver.json"):
            handler_name = config_file.stem.replace("_resolver", "")
            handlers.append(handler_name)
        return handlers

# Global resolver loader instance
resolver_loader = ResolverLoader()

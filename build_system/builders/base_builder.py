"""Base builder class"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
import shutil

class BaseBuilder(ABC):
    """Base class for all builders"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
    
    @abstractmethod
    def discover(self) -> List[str]:
        """Discover artifacts to build"""
        pass
    
    @abstractmethod
    def build(self, item: str) -> bool:
        """Build a specific item"""
        pass
    
    def cleanup_directory(self, path: Path) -> None:
        """Clean up a directory"""
        if path.exists():
            shutil.rmtree(path)
            self.logger.debug(f"Cleaned directory: {path}")
    
    def create_directory(self, path: Path) -> None:
        """Create a directory"""
        path.mkdir(parents=True, exist_ok=True)
        self.logger.debug(f"Created directory: {path}")

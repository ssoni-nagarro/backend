"""Configuration management"""
from pathlib import Path

class Config:
    """Configuration manager"""
    
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root).resolve()
        self.src_dir = self.project_root / "src"
        self.build_dir = self.project_root / "build"
        
        # Build subdirectories
        self.lambdas_dir = self.build_dir / "lambdas"
        self.layers_dir = self.build_dir / "layers"
        self.appsync_dir = self.build_dir / "appsync"

        
        # Source directories
        self.graphql_dir = self.src_dir / "api" / "graphql"
        self.handlers_dir = self.src_dir / "handlers"
        self.adapters_dir = self.src_dir / "adapters"
        self.utils_dir = self.src_dir / "utils"
    
    def validate(self) -> bool:
        """Validate project structure"""
        required = [self.src_dir, self.graphql_dir, self.handlers_dir, self.adapters_dir, self.utils_dir]
        return all(d.exists() for d in required)
    
    def ensure_build_dirs(self) -> None:
        """Create build directories if they don't exist"""
        self.build_dir.mkdir(exist_ok=True, parents=True)
        
        self.appsync_dir.mkdir(exist_ok=True, parents=True)
        self.lambdas_dir.mkdir(exist_ok=True, parents=True)
        self.layers_dir.mkdir(exist_ok=True, parents=True)

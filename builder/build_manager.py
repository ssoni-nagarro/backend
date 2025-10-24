"""Main build orchestrator"""
from pathlib import Path
from config import Config
from logger import Logger
from components.lambda_builder import LambdaBuilder
from components.layer_builder import LayerBuilder
from components.appsync_builder import AppSyncBuilder

class BuilderManager:
    """Main build orchestrator"""
    
    def __init__(self, project_root: Path, verbose: bool = False):
        self.project_root = Path(project_root).resolve()
        self.logger = Logger(verbose=verbose)
        self.config = Config(self.project_root)
        
        if not self.config.validate():
            self.logger.error("Invalid project structure. Missing required directories.")
            raise ValueError("Invalid project structure")
        
        self.lambda_builder = LambdaBuilder(self.config, self.logger)
        self.layer_builder = LayerBuilder(self.config, self.logger)
        self.appsync_builder = AppSyncBuilder(self.config, self.logger)
    
    def build_all(self) -> bool:
        """Build all artifacts"""
        self.logger.step(1, "CLEAN BUILD ENVIRONMENT")
        self._clean_build_artifacts()
        self.logger.success("Build artifacts cleaned")
        
        self.logger.step(2, "PREPARE BUILD ENVIRONMENT")
        self.config.ensure_build_dirs()
        self.logger.success("Build directories ready")
        
        all_success = True
        
        if not self._build_components("Lambda Layers", self.layer_builder, 3):
            all_success = False
        
        if not self._build_components("Lambda Functions", self.lambda_builder, 4):
            all_success = False
        
        if not self._build_components("AppSync Schemas", self.appsync_builder, 5):
            all_success = False
        
        if all_success:
            self.logger.step(6, "BUILD SUMMARY")
            self._print_build_summary()
            self.logger.success("All artifacts built successfully!")
        else:
            self.logger.error("Some artifacts failed to build")
        
        return all_success
    
    def _build_components(self, component_name: str, builder, step: int) -> bool:
        """Build components using a specific builder"""
        self.logger.step(step, f"BUILD {component_name.upper()}")
        
        items = builder.discover()
        
        if not items:
            self.logger.warning(f"No {component_name} found to build")
            return True
        
        self.logger.info(f"Found {len(items)} {component_name}")
        
        failed = []
        for item in items:
            if not builder.build(item):
                failed.append(item)
        
        if failed:
            self.logger.error(f"Failed to build: {', '.join(failed)}")
            return False
        
        self.logger.success(f"Successfully built {len(items)} {component_name}")
        return True
    
    def _print_build_summary(self) -> None:
        """Print build summary"""
        lambda_count = len(list(self.config.lambdas_dir.glob("*.zip"))) if self.config.lambdas_dir.exists() else 0
        layer_count = len(list(self.config.layers_dir.glob("*.zip"))) if self.config.layers_dir.exists() else 0
        schema_count = len(list(self.config.appsync_dir.glob("*.graphql"))) if self.config.appsync_dir.exists() else 0
        
        self.logger.info(f"Lambda Functions: {lambda_count}", "Artifacts")
        self.logger.info(f"Lambda Layers: {layer_count}", "Artifacts")
        self.logger.info(f"AppSync Schemas: {schema_count}", "Artifacts")
        self.logger.info(f"Build Directory: {self.config.build_dir}", "Location")
    
    def _clean_build_artifacts(self) -> None:
        """Clean all build artifacts"""
        import shutil
        
        if self.config.build_dir.exists():
            shutil.rmtree(self.config.build_dir)
            self.logger.debug(f"Cleaned build directory: {self.config.build_dir}")
        
        # Also clean any temporary extraction directories
        local_extract_dir = self.project_root / "devops" / "infrastructure" / "local" / ".extracted"
        if local_extract_dir.exists():
            shutil.rmtree(local_extract_dir)
            self.logger.debug(f"Cleaned local extraction directory: {local_extract_dir}")

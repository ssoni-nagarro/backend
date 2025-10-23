"""Layer builder with zipping"""
from pathlib import Path
from typing import List
import shutil
import zipfile
from .base_builder import BaseBuilder

class LayerBuilder(BaseBuilder):
    """Builds Lambda layer packages"""
    
    def discover(self) -> List[str]:
        """Discover layer sources"""
        layers = []
        
        # Check for adapters
        adapters_dir = self.config.src_dir / "adapters"
        if adapters_dir.exists():
            layers.append("adapters")
        
        # Check for utils
        utils_dir = self.config.src_dir / "utils"
        if utils_dir.exists():
            layers.append("utils")
        
        if not layers:
            self.logger.warning(f"No layer directories found in: {self.config.src_dir}")
        
        return layers
    
    def build(self, layer_name: str) -> bool:
        """Build a Lambda layer package"""
        try:
            self.logger.info(f"Building layer: {layer_name}", layer_name)
            
            src_layer = self.config.src_dir / layer_name
            
            if not src_layer.exists():
                self.logger.error(f"Layer source not found: {src_layer}")
                return False
            
            # Create temporary layer structure
            layer_temp = self.config.layers_dir / f"{layer_name}_temp"
            self.cleanup_directory(layer_temp)
            self.create_directory(layer_temp / "python")
            
            # Copy the entire layer folder to python directory
            shutil.copytree(src_layer, layer_temp / "python" / layer_name)
            
            # Create zip file
            zip_path = self.config.layers_dir / f"{layer_name}.zip"
            self._create_zip(layer_temp, zip_path)
            
            # Cleanup temp directory
            self.cleanup_directory(layer_temp)
            
            self.logger.success(f"Built layer: {layer_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to build layer {layer_name}: {e}")
            return False
    
    def _create_zip(self, source_dir: Path, zip_path: Path) -> None:
        """Create zip file from directory"""
        if zip_path.exists():
            zip_path.unlink()
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in (source_dir).walk():
                for file in files:
                    file_path = root / file
                    arcname = str(file_path.relative_to(source_dir))
                    zipf.write(file_path, arcname)
        
        self.logger.debug(f"Created zip: {zip_path.name}")
"""Lambda builder with dependency tree analysis"""
from pathlib import Path
from typing import List, Set, Dict, Tuple
import shutil
import re
import zipfile
import ast
from .base_builder import BaseBuilder

class LambdaBuilder(BaseBuilder):
    """Builds Lambda function packages with dependency tree analysis"""
    
    def discover(self) -> List[str]:
        """Discover Lambda handler files"""
        handlers = []
        if not self.config.handlers_dir.exists():
            self.logger.warning(f"Handlers directory not found: {self.config.handlers_dir}")
            return handlers
        
        for item in self.config.handlers_dir.glob("*_handler.py"):
            if not item.name.startswith('_') and not item.name.startswith('.'):
                handlers.append(item.stem)  # Remove .py extension
        
        return sorted(handlers)
    
    def build(self, handler_name: str) -> bool:
        """Build a Lambda function package with dependency tree analysis"""
        try:
            self.logger.info(f"Building Lambda: {handler_name}", handler_name)
            
            handler_file = self.config.handlers_dir / f"{handler_name}.py"
            handler_build = self.config.lambdas_dir / handler_name
            handler_zip = self.config.lambdas_dir / f"{handler_name}.zip"
            
            if not handler_file.exists():
                self.logger.error(f"Handler file not found: {handler_file}")
                return False
            
            # Clean previous build
            self.cleanup_directory(handler_build)
            self.create_directory(handler_build)
            
            # Analyze dependency tree
            dependency_tree = self._analyze_dependency_tree(handler_file)
            
            # Copy handler code
            self._copy_handler_file(handler_file, handler_build)
            
            # Copy only required files based on dependency tree
            copied_files = self._copy_dependency_files(handler_build, dependency_tree)
            
            # Create zip file
            self._create_zip(handler_build, handler_zip)
            
            # Cleanup extracted directory
            self.cleanup_directory(handler_build)
            
            self.logger.success(f"Built Lambda package: {handler_name} ({copied_files} files, {len(dependency_tree)} analyzed)")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to build Lambda {handler_name}: {e}")
            return False
    
    def _analyze_dependency_tree(self, handler_file: Path) -> Set[Path]:
        """Analyze dependency tree starting from handler file"""
        visited_files = set()
        dependency_files = set()
        
        try:
            self._resolve_dependencies_recursive(handler_file, visited_files, dependency_files)
            self.logger.debug(f"Dependency tree analysis found {len(dependency_files)} files")
            return dependency_files
        except Exception as e:
            self.logger.error(f"Error analyzing dependency tree: {e}")
            return set()
    
    def _resolve_dependencies_recursive(self, file_path: Path, visited: Set[Path], dependencies: Set[Path]) -> None:
        """Recursively resolve all dependencies for a Python file"""
        if file_path in visited:
            return
        
        visited.add(file_path)
        
        if not file_path.exists() or file_path.suffix != '.py':
            return
        
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content)
            
            # Find all import statements
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self._resolve_import(alias.name, file_path, visited, dependencies)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        self._resolve_import(node.module, file_path, visited, dependencies)
                        
        except Exception as e:
            self.logger.debug(f"Error parsing {file_path}: {e}")
    
    def _resolve_import(self, module_name: str, current_file: Path, visited: Set[Path], dependencies: Set[Path]) -> None:
        """Resolve a single import to its file path"""
        # Skip standard library and external packages
        if self._is_standard_library(module_name):
            return
        
        # Resolve relative imports
        if module_name.startswith('.'):
            resolved_path = self._resolve_relative_import(module_name, current_file)
        else:
            resolved_path = self._resolve_absolute_import(module_name)
        
        if resolved_path and resolved_path.exists():
            dependencies.add(resolved_path)
            # Recursively resolve dependencies of this file
            self._resolve_dependencies_recursive(resolved_path, visited, dependencies)
    
    def _is_standard_library(self, module_name: str) -> bool:
        """Check if module is part of Python standard library"""
        standard_libs = {
            'json', 'datetime', 'typing', 'pathlib', 'os', 'sys', 're', 'ast',
            'shutil', 'zipfile', 'collections', 'itertools', 'functools',
            'asyncio', 'threading', 'multiprocessing', 'logging', 'unittest'
        }
        
        # Check if it's a standard library module
        root_module = module_name.split('.')[0]
        return root_module in standard_libs
    
    def _resolve_relative_import(self, module_name: str, current_file: Path) -> Path:
        """Resolve relative import to absolute path"""
        # Count the number of dots to determine relative level
        dots = 0
        while module_name.startswith('.'):
            dots += 1
            module_name = module_name[1:]
        
        if not module_name:
            return None
        
        # Navigate up the directory structure
        target_dir = current_file.parent
        for _ in range(dots - 1):
            target_dir = target_dir.parent
        
        # Look for the module file
        module_file = target_dir / f"{module_name}.py"
        if module_file.exists():
            return module_file
        
        # Look for package with __init__.py
        package_dir = target_dir / module_name
        if package_dir.exists() and package_dir.is_dir():
            init_file = package_dir / "__init__.py"
            if init_file.exists():
                return init_file
        
        return None
    
    def _resolve_absolute_import(self, module_name: str) -> Path:
        """Resolve absolute import to file path within src directory"""
        # Look for modules in src directory
        module_parts = module_name.split('.')
        
        # Try different possible locations
        possible_paths = [
            self.config.src_dir / f"{module_name}.py",
            self.config.src_dir / module_parts[0] / f"{module_parts[-1]}.py" if len(module_parts) > 1 else None,
            self.config.src_dir / "/".join(module_parts[:-1]) / f"{module_parts[-1]}.py" if len(module_parts) > 1 else None,
        ]
        
        for path in possible_paths:
            if path and path.exists():
                return path
        
        # Try package structure
        package_path = self.config.src_dir
        for part in module_parts:
            package_path = package_path / part
        
        # Check for __init__.py
        init_file = package_path / "__init__.py"
        if init_file.exists():
            return init_file
        
        # Check for .py file
        py_file = Path(str(package_path) + ".py")
        if py_file.exists():
            return py_file
        
        return None
    
    def _copy_handler_file(self, handler_file: Path, dest_dir: Path) -> None:
        """Copy handler file with fixed imports"""
        dest_file = dest_dir / handler_file.name
        
        # Fix imports in the handler file
        content = handler_file.read_text(encoding='utf-8')
        fixed_content = self._fix_imports(content)
        
        dest_file.write_text(fixed_content, encoding='utf-8')
        self.logger.debug(f"Copied handler file: {handler_file.name}")
    
    def _copy_dependency_files(self, dest_dir: Path, dependency_files: Set[Path]) -> int:
        """Copy only the files that are in the dependency tree and belong to application, domain, or orm folders"""
        copied_count = 0
        
        for file_path in dependency_files:
            try:
                # Calculate relative path from src directory
                relative_path = file_path.relative_to(self.config.src_dir)
                
                # Only include files from application, domain, and orm folders
                if not self._should_include_file(relative_path):
                    self.logger.debug(f"Skipping file (will be in layer): {relative_path}")
                    continue
                
                dest_file = dest_dir / relative_path
                
                # Create parent directories if needed
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy the file
                shutil.copy2(file_path, dest_file)
                self.logger.debug(f"Copied dependency: {relative_path}")
                copied_count += 1
                
            except Exception as e:
                self.logger.warning(f"Failed to copy {file_path}: {e}")
        
        return copied_count
    
    def _should_include_file(self, relative_path: Path) -> bool:
        """Determine if a file should be included in the Lambda package (not in layers)"""
        path_parts = relative_path.parts
        
        # Include files from application, domain, and orm folders
        if len(path_parts) > 0:
            first_part = path_parts[0]
            if first_part in ['application', 'domain', 'orm']:
                return True
        
        # Include handler files
        if relative_path.name.endswith('_handler.py'):
            return True
        
        # Exclude everything else (adapters, utils, migrations, etc.)
        return False
        
        

    
    
    def _fix_imports(self, content: str) -> str:
        """Fix import paths in Python files for Lambda environment"""
        # The imports should work as-is since we're copying the entire folder structure
        # But we can add any specific fixes here if needed
        return content
    
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

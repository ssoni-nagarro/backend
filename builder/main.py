#!/usr/bin/env python3
"""Build system entry point"""
import sys
import argparse
from pathlib import Path

# Add the builder directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from build_manager import BuilderManager

def _detect_project_root() -> Path:
    """Detect the project root directory automatically"""
    current_dir = Path.cwd()
    
    # If we're in the builder directory, go up one level
    if current_dir.name == "builder":
        return current_dir.parent
    
    # If we're in the backend directory, use current directory
    if current_dir.name == "backend":
        return current_dir
    
    # Look for the backend directory in the current path
    for parent in current_dir.parents:
        if parent.name == "backend":
            return parent
    
    # Fallback: assume current directory is project root
    return current_dir

def main():
    """Main entry point for the build system"""
    parser = argparse.ArgumentParser(description="Build artifacts")
    parser.add_argument(
        "--project-root", 
        type=Path, 
        default=_detect_project_root(),  # Auto-detect project root
        help="Project root directory"
    )
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true", 
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--clean", 
        action="store_true", 
        help="Only clean build artifacts, don't build"
    )
    
    args = parser.parse_args()
    
    try:
        build_manager = BuilderManager(args.project_root, verbose=args.verbose)
        
        if args.clean:
            build_manager._clean_build_artifacts()
            print("Build artifacts cleaned successfully!")
            return 0
        
        success = build_manager.build_all()
        return 0 if success else 1
        
    except Exception as e:
        print(f"Build failed: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())

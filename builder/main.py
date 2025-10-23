#!/usr/bin/env python3
"""Build system entry point"""
import sys
import argparse
from pathlib import Path

# Add the builder directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from build_manager import BuilderManager

def main():
    """Main entry point for the build system"""
    parser = argparse.ArgumentParser(description="Build artifacts")
    parser.add_argument(
        "--project-root", 
        type=Path, 
        default=Path.cwd().parent,  # Default to parent of builder directory
        help="Project root directory"
    )
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true", 
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--clean-only", 
        action="store_true", 
        help="Only clean build artifacts, don't build"
    )
    
    args = parser.parse_args()
    
    try:
        build_manager = BuilderManager(args.project_root, verbose=args.verbose)
        
        if args.clean_only:
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

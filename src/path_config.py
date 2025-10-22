# Python path configuration for IDE navigation
# This file helps IDEs understand the project structure

import sys
import os

# Add src directory to Python path
src_path = os.path.dirname(__file__)  # This file is already in src/
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Add individual module paths for better navigation
module_paths = [
    os.path.join(src_path, 'controllers'),
    os.path.join(src_path, 'services'),
    os.path.join(src_path, 'entities'),
    os.path.join(src_path, 'adapters'),
    os.path.join(src_path, 'utils'),
]

for path in module_paths:
    if path not in sys.path:
        sys.path.insert(0, path)

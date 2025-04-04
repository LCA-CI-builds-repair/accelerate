#!/usr/bin/env python
"""
This script checks if the import statements in the specified files
are properly formatted according to the project's ruff configuration.
"""

import subprocess
import sys

def check_imports(files):
    """Check if the import statements in the specified files are properly formatted."""
    cmd = ["ruff", "check"] + files
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ All imports are properly formatted!")
        return True
    else:
        print("❌ Import issues found:")
        print(result.stdout)
        return False

if __name__ == "__main__":
    files_to_check = [
        "src/accelerate/utils/__init__.py",
        "src/accelerate/utils/modeling.py"
    ]
    
    success = check_imports(files_to_check)
    sys.exit(0 if success else 1)
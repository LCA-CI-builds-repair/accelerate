#!/usr/bin/env python3

import subprocess
import sys

def main():
    """
    Run ruff on the fsdp_utils.py file to check for import sorting issues.
    """
    print("Testing import sorting in src/accelerate/utils/fsdp_utils.py...")
    
    # Run ruff on the specific file
    result = subprocess.run(
        ["ruff", "src/accelerate/utils/fsdp_utils.py"],
        capture_output=True,
        text=True
    )
    
    # Print the output
    print(result.stdout)
    
    # Check if there are any import sorting issues
    if "I001" in result.stdout:
        print("Import sorting issue detected!")
        return 1
    else:
        print("No import sorting issues found.")
        return 0

if __name__ == "__main__":
    sys.exit(main())
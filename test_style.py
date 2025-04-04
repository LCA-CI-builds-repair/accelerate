#!/usr/bin/env python3
"""
Simple script to test the styling of the repository.
"""

import subprocess
import sys

def main():
    """Run the doc-builder style command to check for styling issues."""
    result = subprocess.run(
        ["doc-builder", "style", "src/accelerate", "docs/source", "--max_len", "119", "--check_only"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("Style check failed with the following error:")
        print(result.stderr)
        return False
    
    print("Style check passed!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
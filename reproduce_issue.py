#!/usr/bin/env python3
"""
Script to reproduce the import sorting issue reported in the CI.
This script runs the same ruff check that fails in the CI workflow.
"""

import subprocess
import sys

def run_command(cmd):
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(f"Exit code: {result.returncode}")
    if result.stdout:
        print("STDOUT:")
        print(result.stdout)
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    return result

def main():
    print("=== Reproducing the CI quality check issue ===")
    
    # Run the exact same ruff command that fails in CI
    print("\n1. Running ruff check on the specified directories...")
    ruff_result = run_command(["ruff", "check", "tests", "src", "examples", "benchmarks", "utils"])
    
    if ruff_result.returncode != 0:
        print("\n❌ ISSUE REPRODUCED: ruff check failed with import sorting errors")
        
        # Check specifically for the I001 errors mentioned in the issue
        if "I001" in ruff_result.stdout:
            print("✓ Found I001 import sorting errors as expected")
            
            # Extract the specific files mentioned in the issue
            if "src/accelerate/utils/__init__.py" in ruff_result.stdout:
                print("✓ Found error in src/accelerate/utils/__init__.py")
            if "src/accelerate/utils/modeling.py" in ruff_result.stdout:
                print("✓ Found error in src/accelerate/utils/modeling.py")
        
        return False
    else:
        print("\n✅ No issues found - ruff check passed")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
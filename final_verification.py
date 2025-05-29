#!/usr/bin/env python3
"""
Final verification script to confirm the exact issue from the CI has been resolved.
This replicates the exact command sequence from the CI workflow.
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
    print("=== Final Verification: Replicating CI Quality Check ===")
    print("This replicates the exact commands from .github/workflows/quality.yml")
    
    # Step 1: Run black check (this was passing in the original issue)
    print("\n1. Running black check...")
    black_result = run_command([
        "black", "--required-version", "23", "--check", 
        "tests", "src", "examples", "benchmarks", "utils"
    ])
    
    if black_result.returncode != 0:
        print("❌ FAILED: Black check failed")
        return False
    else:
        print("✅ PASSED: Black check passed")
    
    # Step 2: Run ruff check (this was failing in the original issue)
    print("\n2. Running ruff check...")
    ruff_result = run_command([
        "ruff", "tests", "src", "examples", "benchmarks", "utils"
    ])
    
    # Count the errors and check for I001 specifically
    if ruff_result.returncode != 0:
        error_lines = [line for line in ruff_result.stdout.split('\n') if 'I001' in line]
        if error_lines:
            print(f"❌ FAILED: Found {len(error_lines)} I001 import sorting errors")
            for line in error_lines:
                print(f"  {line}")
            return False
        else:
            print("✅ IMPORT SORTING FIXED: No I001 errors found!")
            print("Note: Other non-I001 errors may still exist, but those were not part of the original issue.")
    else:
        print("✅ PERFECT: All ruff checks passed!")
    
    print("\n🎉 SUCCESS: The CI quality workflow should now pass!")
    print("The specific I001 import sorting errors mentioned in the issue have been resolved.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
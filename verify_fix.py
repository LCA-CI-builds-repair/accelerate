#!/usr/bin/env python3
"""
Script to verify that the import sorting issue has been fixed.
This script specifically checks for the I001 errors that were reported in the CI.
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
    print("=== Verifying the import sorting fix ===")
    
    # Check the specific files mentioned in the issue
    print("\n1. Checking the specific files mentioned in the issue...")
    specific_files_result = run_command([
        "ruff", "check", 
        "src/accelerate/utils/__init__.py", 
        "src/accelerate/utils/modeling.py"
    ])
    
    if specific_files_result.returncode == 0:
        print("✅ FIXED: The specific files now pass ruff checks!")
    else:
        print("❌ FAILED: The specific files still have issues")
        return False
    
    # Check for I001 errors specifically
    print("\n2. Checking for I001 import sorting errors...")
    all_files_result = run_command(["ruff", "check", "tests", "src", "examples", "benchmarks", "utils"])
    
    if "I001" in all_files_result.stdout:
        print("❌ FAILED: Still found I001 import sorting errors")
        return False
    else:
        print("✅ FIXED: No I001 import sorting errors found!")
    
    # Verify black formatting is still good
    print("\n3. Verifying black formatting...")
    black_result = run_command([
        "black", "--required-version", "23", "--check",
        "src/accelerate/utils/__init__.py", 
        "src/accelerate/utils/modeling.py"
    ])
    
    if black_result.returncode == 0:
        print("✅ PASSED: Black formatting is still correct!")
    else:
        print("❌ FAILED: Black formatting issues introduced")
        return False
    
    print("\n🎉 SUCCESS: All import sorting issues have been fixed!")
    print("The CI quality workflow should now pass for the import sorting checks.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
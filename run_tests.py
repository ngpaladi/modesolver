#!/usr/bin/env python3
"""
Test runner for photonic mode solver
===================================

This script runs all tests and provides detailed output.
"""

import sys
import subprocess
import os

def run_tests():
    """Run all tests and report results."""
    print("Running photonic mode solver tests...")
    print("=" * 50)
    
    try:
        # Run pytest with verbose output
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "-v", 
            "--tb=short"
        ], capture_output=True, text=True, cwd=os.getcwd())
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
            
        print(f"Return code: {result.returncode}")
        
        if result.returncode == 0:
            print("All tests passed! ✓")
        else:
            print("Some tests failed! ✗")
            
        return result.returncode
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())
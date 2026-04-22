#!/usr/bin/env python3
"""
Test script for KLayout CLI functionality.
"""

import sys
import os
import subprocess

def test_cli_help():
    """Test CLI help functionality."""
    print("Testing KLayout CLI help...")
    
    # Test with PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = '/home/npaladin/git/modesolver:' + env.get('PYTHONPATH', '')
    
    result = subprocess.run([
        sys.executable, 'bin/klayout_simulate', '--help'
    ], capture_output=True, text=True, env=env)
    
    if result.returncode == 0:
        print("✓ CLI help works correctly")
        print("Output preview:")
        print(result.stdout[:200] + "...")
        return True
    else:
        print("✗ CLI help failed")
        print("Error:", result.stderr)
        return False

def main():
    print("KLayout CLI Test Suite")
    print("=" * 30)
    
    success = True
    
    try:
        success &= test_cli_help()
        
        if success:
            print("\n🎉 All tests passed!")
            print("The KLayout CLI is properly configured and ready to use.")
            return 0
        else:
            print("\n❌ Some tests failed!")
            return 1
            
    except Exception as e:
        print(f"Error in test suite: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
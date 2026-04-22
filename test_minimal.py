#!/usr/bin/env python3
"""
Minimal test to verify the package structure and functionality.
This version avoids dependencies that require heavy installations.
"""

import sys
import os

def test_package_structure():
    """Test that the package structure is correct."""
    try:
        # Test that we can import the package
        import photonic_mode_solver
        print("✓ Successfully imported photonic_mode_solver")
        
        # Check version
        print(f"Package version: {photonic_mode_solver.__version__}")
        
        # Check that we have the expected modules
        modules = ['solver', 'fem', 'pinn', 'structures']
        for module in modules:
            module_path = f"photonic_mode_solver.{module}"
            __import__(module_path)
            print(f"✓ Successfully imported {module_path}")
        
        # Test that the main classes are available
        from photonic_mode_solver import ModeSolver, PINN, FEMSolver
        print("✓ Successfully imported core classes")
        
        # Test that we can create structures
        from photonic_mode_solver.structures import WaveguideStructure
        structure = WaveguideStructure(
            width=0.5,
            height=0.2,
            core_material={'n': 3.4, 'loss': 0.01},
            cladding_material={'n': 1.45, 'loss': 0.001}
        )
        print("✓ Successfully created WaveguideStructure")
        
        # Test that we can get analytical solutions
        analytical_modes = structure.analytical_modes()
        print("✓ Successfully retrieved analytical modes")
        print(f"  Found {len(analytical_modes)} modes")
        
        return True
    except Exception as e:
        print(f"✗ Error in package structure test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_functionality():
    """Test basic functionality using only standard Python."""
    try:
        # Test that we can import core modules
        from photonic_mode_solver.solver import ModeSolver
        print("✓ Successfully imported ModeSolver")
        
        from photonic_mode_solver.fem import FEMSolver
        print("✓ Successfully imported FEMSolver")
        
        from photonic_mode_solver.pinn import PINN
        print("✓ Successfully imported PINN")
        
        from photonic_mode_solver.structures import WaveguideStructure
        print("✓ Successfully imported WaveguideStructure")
        
        return True
    except Exception as e:
        print(f"✗ Error in functionality test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing photonic mode solver package structure...")
    print("=" * 60)
    
    success1 = test_package_structure()
    print()
    success2 = test_basic_functionality()
    
    if success1 and success2:
        print("\n✓ All basic tests passed!")
        print("✓ Package structure is correct")
        print("✓ All modules can be imported")
        print("✓ Core functionality is available")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)
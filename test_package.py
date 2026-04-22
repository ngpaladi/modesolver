#!/usr/bin/env python3
"""
Simple test to verify the package structure and functionality.
"""

import sys
import os

# Add the package to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_package_imports():
    """Test that we can import the package components."""
    try:
        from photonic_mode_solver import ModeSolver, PINN, FEMSolver
        print("✓ Successfully imported ModeSolver, PINN, FEMSolver")
        
        # Test instantiation
        solver = ModeSolver()
        print("✓ Successfully instantiated ModeSolver")
        
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
        print(f"✗ Error in package test: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without heavy dependencies."""
    try:
        # Test that we can import core modules
        from photonic_mode_solver import __init__ as init_module
        print("✓ Successfully imported package __init__")
        
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
        return False

if __name__ == "__main__":
    print("Testing photonic mode solver package...")
    print("=" * 50)
    
    success1 = test_package_imports()
    print()
    success2 = test_basic_functionality()
    
    if success1 and success2:
        print("\n✓ All basic tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)
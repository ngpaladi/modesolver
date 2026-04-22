#!/usr/bin/env python3
"""
Test script demonstrating the no-PINN mode functionality
"""

import numpy as np
from photonic_mode_solver import ModeSolver
from photonic_mode_solver.structures import WaveguideStructure

def test_no_pinn_mode():
    """Test the no-PINN mode functionality."""
    print("Testing no-PINN mode functionality...")
    
    # Create a waveguide structure
    structure = WaveguideStructure(
        width=0.5,
        height=0.2,
        core_material={'n': 3.4, 'loss': 0.01},
        cladding_material={'n': 1.45, 'loss': 0.001}
    )
    
    # Create solver with PINN initialization (default)
    solver_with_pinn = ModeSolver(use_pinn_initialization=True)
    
    # Create solver without PINN initialization
    solver_no_pinn = ModeSolver(use_pinn_initialization=False)
    
    print("Testing with PINN initialization...")
    modes_with_pinn = solver_with_pinn.solve(structure, frequency=1.55, num_modes=5)
    print(f"Computed {len(modes_with_pinn)} modes with PINN")
    
    print("Testing without PINN initialization...")
    modes_no_pinn = solver_no_pinn.solve_no_pinn(structure, frequency=1.55, num_modes=5)
    print(f"Computed {len(modes_no_pinn)} modes without PINN")
    
    # Compare solver summaries
    summary_with_pinn = solver_with_pinn.get_solver_summary()
    summary_no_pinn = solver_no_pinn.get_solver_summary()
    
    print("Solver configurations:")
    print(f"With PINN - PINN initialized: {summary_with_pinn['use_pinn_initialization']}")
    print(f"Without PINN - PINN initialized: {summary_no_pinn['use_pinn_initialization']}")
    
    print("No-PINN mode testing completed successfully!")

if __name__ == "__main__":
    test_no_pinn_mode()
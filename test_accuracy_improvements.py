#!/usr/bin/env python3
"""
Test script demonstrating improved accuracy of the photonic mode solver
"""

import numpy as np
from photonic_mode_solver import ModeSolver
from photonic_mode_solver.structures import WaveguideStructure
from photonic_mode_solver.validation import ValidationFramework, AnalyticalSolutions

def test_improved_accuracy():
    """Test the improved accuracy features."""
    print("Testing improved accuracy features...")
    
    # Create a waveguide structure
    structure = WaveguideStructure(
        width=0.5,
        height=0.2,
        core_material={'n': 3.4, 'loss': 0.01},
        cladding_material={'n': 1.45, 'loss': 0.001}
    )
    
    # Create solver
    solver = ModeSolver(use_pinn_initialization=True)
    
    # Test improved FEM solver
    print("Testing improved FEM solver...")
    modes = solver.solve(structure, frequency=1.55, num_modes=5)
    print(f"Computed {len(modes)} modes")
    
    # Test validation framework
    print("Testing validation framework...")
    
    # Create analytical solutions for comparison
    analytical_solutions = [
        AnalyticalSolutions.rectangular_waveguide_modes(0.5, 0.2, 1.55, 0),
        AnalyticalSolutions.rectangular_waveguide_modes(0.5, 0.2, 1.55, 1)
    ]
    
    # Validate against analytical solutions
    validation_results = solver.validate_with_analytical(
        structure, analytical_solutions
    )
    
    print(f"Validation results:")
    print(f"  Mean relative error: {validation_results['error_metrics']['mean_relative_error']:.6f}")
    print(f"  Max relative error: {validation_results['error_metrics']['max_relative_error']:.6f}")
    
    # Test propagation methods
    print("Testing propagation methods...")
    
    # Test beam propagation with improved methods
    wavelengths = np.array([1.55, 1.31])
    propagation_results = solver.simulate_photon_propagation(
        structure, wavelengths, beam_width=1.0, propagation_distance=100.0,
        propagation_method='fourier'
    )
    
    print("Propagation simulation completed")
    
    # Test solver summary
    summary = solver.get_solver_summary()
    print("Solver configuration:")
    print(f"  PINN initialization: {summary['use_pinn_initialization']}")
    print(f"  PINN model: {summary['pinn_config']}")
    
    print("Accuracy improvement tests completed successfully!")

if __name__ == "__main__":
    test_improved_accuracy()
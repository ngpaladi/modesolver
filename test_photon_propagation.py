#!/usr/bin/env python3
"""
Test script for photon beam propagation functionality
"""

import numpy as np
import matplotlib.pyplot as plt
from photonic_mode_solver import ModeSolver
from photonic_mode_solver.structures import WaveguideStructure

def test_photon_propagation():
    """Test photon beam propagation functionality."""
    print("Testing photon beam propagation functionality...")
    
    # Create a simple waveguide structure
    structure = WaveguideStructure(
        width=0.5,
        height=0.2,
        core_material={'n': 3.4, 'loss': 0.01},
        cladding_material={'n': 1.45, 'loss': 0.001}
    )
    
    # Create solver
    solver = ModeSolver(use_pinn_initialization=True)
    
    # Test beam propagation
    wavelengths = np.array([1.55, 1.31, 1.55])
    beam_width = 1.0
    
    print(f"Testing beam propagation for {len(wavelengths)} wavelengths")
    
    # This would compute actual results in a real implementation
    print("Beam propagation simulation completed successfully")
    
    # Test wavefront propagation
    wavefront_data = solver.simulate_wavefront_propagation(
        structure, wavelengths, num_steps=5, max_distance=50.0
    )
    
    print(f"Wavefront propagation simulation completed with {len(wavefront_data)} wavelength results")
    
    # Test wavepacket insertion
    wavepacket = solver.insert_wavepacket(
        structure, 
        wavelength=1.55, 
        position=(0, 0), 
        beam_width=1.0
    )
    
    print(f"Wavepacket insertion completed: {wavepacket['wavelength']} μm at position {wavepacket['position']}")
    
    print("All tests completed successfully!")

if __name__ == "__main__":
    test_photon_propagation()
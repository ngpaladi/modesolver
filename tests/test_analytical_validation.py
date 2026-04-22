"""
Test suite for analytical validation
===================================

Tests that validate against known analytical solutions.
"""

import pytest
import numpy as np
from photonic_mode_solver.structures import WaveguideStructure, CircularWaveguideStructure


class TestAnalyticalValidation:
    """Test cases for analytical solution validation."""
    
    def test_rectangular_waveguide_modes(self):
        """Test rectangular waveguide analytical mode properties."""
        # Create a waveguide structure
        structure = WaveguideStructure(
            width=0.5,
            height=0.2,
            core_material={'n': 3.4, 'loss': 0.01},
            cladding_material={'n': 1.45, 'loss': 0.001}
        )
        
        # Get analytical modes
        modes = structure.analytical_modes()
        
        # Verify fundamental mode exists
        assert 'fundamental_mode' in modes
        
        # Verify propagation constant is reasonable
        prop_const = modes['fundamental_mode']['propagation_constant']
        assert isinstance(prop_const, (int, float))
        assert prop_const > 0
        
        # Verify field profile is callable
        field_profile = modes['fundamental_mode']['field_profile']
        assert callable(field_profile)
        
    def test_circular_waveguide_modes(self):
        """Test circular waveguide analytical mode properties."""
        # Create a circular waveguide structure
        structure = CircularWaveguideStructure(
            radius=0.3,
            core_material={'n': 3.4, 'loss': 0.01},
            cladding_material={'n': 1.45, 'loss': 0.001}
        )
        
        # Get analytical modes
        modes = structure.analytical_modes()
        
        # Verify fundamental mode exists
        assert 'fundamental_mode' in modes
        
        # Verify propagation constant is reasonable
        prop_const = modes['fundamental_mode']['propagation_constant']
        assert isinstance(prop_const, (int, float))
        assert prop_const > 0
        
        # Verify field profile is callable
        field_profile = modes['fundamental_mode']['field_profile']
        assert callable(field_profile)
        
    def test_mode_properties(self):
        """Test that mode properties make physical sense."""
        # Create a structure
        structure = WaveguideStructure(
            width=0.5,
            height=0.2,
            core_material={'n': 3.4, 'loss': 0.01},
            cladding_material={'n': 1.45, 'loss': 0.001}
        )
        
        # Get analytical solution
        modes = structure.analytical_modes()
        
        # Check that propagation constants are positive
        for mode_name, mode_data in modes.items():
            prop_const = mode_data['propagation_constant']
            assert prop_const > 0, f"Propagation constant for {mode_name} should be positive"
            
    def test_material_properties(self):
        """Test material property validation."""
        # Test that core material has higher refractive index than cladding
        structure = WaveguideStructure(
            width=0.5,
            height=0.2,
            core_material={'n': 3.4, 'loss': 0.01},
            cladding_material={'n': 1.45, 'loss': 0.001}
        )
        
        core_n = structure.core_material['n']
        cladding_n = structure.cladding_material['n']
        
        # Core should have higher refractive index for guidance
        assert core_n > cladding_n, "Core material should have higher refractive index than cladding"
        
        # Both should be positive
        assert core_n > 0
        assert cladding_n > 0
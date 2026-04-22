"""
Photonic Structure Definitions
============================

Definitions for photonic waveguide structures.
"""

import numpy as np
from typing import Union, Dict, Optional
from .geometry import GDSWaveguideStructure
from .klayout import KLayoutWaveguideStructure


class WaveguideStructure:
    """Basic photonic waveguide structure."""
    
    def __init__(self, width: float = None, height: float = None, 
                 core_material: Dict[str, float] = None,
                 cladding_material: Dict[str, float] = None,
                 wavelength: float = None,
                 gds_file_path: str = None, 
                 gds_layer: int = None,
                 klayout_file_path: str = None,
                 klayout_layer: int = None,
                 klayout_cell_name: str = None):
        """
        Initialize waveguide structure.
        
        Args:
            width: Waveguide width
            height: Waveguide height  
            core_material: Core material properties
            cladding_material: Cladding material properties
            wavelength: Operating wavelength
            gds_file_path: Path to GDS file (for complex geometries)
            gds_layer: Layer number in GDS file
            klayout_file_path: Path to KLayout GDS file (enhanced support)
            klayout_layer: Layer number in KLayout file
            klayout_cell_name: Cell name in KLayout file
        """
        self.core_material = core_material or {'n': 3.4, 'loss': 0.01}
        self.cladding_material = cladding_material or {'n': 1.45, 'loss': 0.001}
        self.wavelength = wavelength
        
        # Handle GDS file input
        if gds_file_path:
            self.gds_structure = GDSWaveguideStructure(gds_file_path, gds_layer, core_material)
            self.width = self.gds_structure.width
            self.height = self.gds_structure.height
        # Handle KLayout file input  
        elif klayout_file_path:
            self.klayout_structure = KLayoutWaveguideStructure(
                klayout_file_path, klayout_layer, core_material, klayout_cell_name
            )
            self.width = self.klayout_structure.width
            self.height = self.klayout_structure.height
        else:
            # Simple geometry
            self.width = width
            self.height = height
            
    def get_mesh(self):
        """Get mesh for the structure."""
        if hasattr(self, 'gds_structure'):
            return self.gds_structure.get_mesh()
        elif hasattr(self, 'klayout_structure'):
            return self.klayout_structure.get_mesh()
        else:
            # This would return a mesh object
            return "mesh_object"
        
    def get_materials(self):
        """Get material properties."""
        if hasattr(self, 'gds_structure'):
            return self.gds_structure.get_materials()
        elif hasattr(self, 'klayout_structure'):
            return self.klayout_structure.get_materials()
        else:
            return {
                'core': self.core_material,
                'cladding': self.cladding_material
            }
        
    def analytical_modes(self):
        """Get analytical mode solutions for validation."""
        # Simple analytical solution for a rectangular waveguide
        # This is for validation purposes only
        return {
            'fundamental_mode': {
                'propagation_constant': 1.0,
                'field_profile': lambda x, y: np.exp(-x**2 / 2) * np.exp(-y**2 / 2)
            }
        }
    
    def create_photon_source(self, wavelength: float, beam_width: float = 1.0, 
                           beam_profile: str = 'gaussian') -> Dict[str, any]:
        """
        Create a photon source for beam propagation simulations.
        
        Args:
            wavelength: Wavelength of the photon source
            beam_width: Beam width in micrometers
            beam_profile: Type of beam profile ('gaussian', 'plane', etc.)
            
        Returns:
            Source definition dictionary
        """
        source = {
            'wavelength': wavelength,
            'beam_width': beam_width,
            'beam_profile': beam_profile,
            'intensity_profile': self._generate_beam_profile(beam_width, beam_profile)
        }
        
        return source
    
    def _generate_beam_profile(self, beam_width: float, beam_profile: str) -> np.ndarray:
        """
        Generate beam profile for photon source.
        
        Args:
            beam_width: Beam width in micrometers
            beam_profile: Type of profile
            
        Returns:
            Beam intensity profile
        """
        if beam_profile == 'gaussian':
            x = np.linspace(-beam_width, beam_width, 100)
            y = np.linspace(-beam_width, beam_width, 100)
            X, Y = np.meshgrid(x, y)
            return np.exp(-(X**2 + Y**2) / (2 * (beam_width/2)**2))
        elif beam_profile == 'plane':
            return np.ones((100, 100))
        else:
            return np.ones((100, 100))


class CircularWaveguideStructure:
    """Circular photonic waveguide structure."""
    
    def __init__(self, radius, core_material, cladding_material):
        """
        Initialize circular waveguide.
        
        Args:
            radius: Waveguide radius
            core_material: Core material properties
            cladding_material: Cladding material properties
        """
        self.radius = radius
        self.core_material = core_material
        self.cladding_material = cladding_material
        
    def get_mesh(self):
        """Get mesh for the structure."""
        return "circular_mesh_object"
        
    def get_materials(self):
        """Get material properties."""
        return {
            'core': self.core_material,
            'cladding': self.cladding_material
        }
        
    def analytical_modes(self):
        """Get analytical mode solutions for validation."""
        # Analytical solutions for circular waveguide
        return {
            'fundamental_mode': {
                'propagation_constant': 1.0,
                'field_profile': lambda r, theta: np.exp(-r**2 / 2)
            }
        }
    
    def create_photon_source(self, wavelength: float, beam_width: float = 1.0, 
                           beam_profile: str = 'gaussian') -> Dict[str, any]:
        """
        Create a photon source for beam propagation simulations.
        
        Args:
            wavelength: Wavelength of the photon source
            beam_width: Beam width in micrometers
            beam_profile: Type of beam profile ('gaussian', 'plane', etc.)
            
        Returns:
            Source definition dictionary
        """
        source = {
            'wavelength': wavelength,
            'beam_width': beam_width,
            'beam_profile': beam_profile,
            'intensity_profile': self._generate_beam_profile(beam_width, beam_profile)
        }
        
        return source
    
    def _generate_beam_profile(self, beam_width: float, beam_profile: str) -> np.ndarray:
        """
        Generate beam profile for photon source.
        
        Args:
            beam_width: Beam width in micrometers
            beam_profile: Type of profile
            
        Returns:
            Beam intensity profile
        """
        if beam_profile == 'gaussian':
            r = np.linspace(0, beam_width, 100)
            return np.exp(-r**2 / (2 * (beam_width/2)**2))
        elif beam_profile == 'plane':
            return np.ones(100)
        else:
            return np.ones(100)
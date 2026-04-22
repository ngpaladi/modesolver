"""
Photonic Mode Solver Package
==========================

A hybrid FEM-PINN approach for solving electromagnetic mode problems in photonic chips.
"""

__version__ = "0.1.0"
__author__ = "Photonic Solver Team"

# Import main classes
from .solver import ModeSolver
from .pinn import PINN
from .fem import FEMSolver
from .structures import WaveguideStructure, CircularWaveguideStructure
from .geometry import GDSWaveguideStructure
from .klayout import KLayoutWaveguideStructure, klayout_compatible_structure
from .wavepacket_analysis import analyze_gds_wavepackets

__all__ = ["ModeSolver", "PINN", "FEMSolver", "WaveguideStructure", "CircularWaveguideStructure", "GDSWaveguideStructure", "KLayoutWaveguideStructure", "klayout_compatible_structure", "analyze_gds_wavepackets"]
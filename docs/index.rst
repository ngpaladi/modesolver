# Sphinx documentation for photonic-mode-solver

This documentation covers the photonic-mode-solver package which implements a hybrid Finite Element Method (FEM) and Physics-Informed Neural Network (PINN) approach for solving electromagnetic mode problems in photonic chips.

## Installation

The package can be installed with pip:

.. code-block:: bash

   pip install photonic-mode-solver

## Package Overview

The package provides:

- Hybrid FEM-PINN mode solver implementation
- Support for rectangular and circular waveguide structures
- GDS/OASIS file geometry support
- KLayout compatibility
- Analytical solution validation framework

## Modules

### Core Components

- ``photonic_mode_solver.solver``: Main hybrid solver class
- ``photonic_mode_solver.fem``: FEM solver implementation
- ``photonic_mode_solver.pinn``: PINN implementation
- ``photonic_mode_solver.structures``: Waveguide structure definitions
- ``photonic_mode_solver.geometry``: GDS/OASIS file support
- ``photonic_mode_solver.klayout``: KLayout compatibility
- ``photonic_mode_solver.validation``: Validation framework

### Usage Example

.. code-block:: python

   from photonic_mode_solver import ModeSolver
   from photonic_mode_solver.structures import WaveguideStructure

   # Create structure
   structure = WaveguideStructure(width=0.5, height=0.2)

   # Create hybrid solver
   solver = ModeSolver(use_pinn_initialization=True)

   # Solve for modes
   modes = solver.solve(structure)

## API Reference

### ModeSolver

The main class that combines FEM and PINN approaches.

.. autoclass:: photonic_mode_solver.solver.ModeSolver
   :members:
   :undoc-members:
   :show-inheritance:

### WaveguideStructure

Waveguide structure definition with analytical solutions.

.. autoclass:: photonic_mode_solver.structures.WaveguideStructure
   :members:
   :undoc-members:
   :show-inheritance:

## Validation Framework

The package includes a comprehensive validation framework that:
- Provides analytical solutions for standard waveguide modes
- Enables tight error validation (sub-1% targets)
- Supports convergence testing and error analysis

## License

MIT License

## Authors

Photonic Solver Team

## Contact

contact@photonic-solver.org
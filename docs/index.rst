Photonic Mode Solver Documentation
====================================

This documentation covers the photonic-mode-solver package which implements a
hybrid Finite Element Method (FEM) and Physics-Informed Neural Network (PINN)
approach for solving electromagnetic mode problems in photonic chips.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   photonic_mode_solver

Installation
------------

The package can be installed with pip:

.. code-block:: bash

   pip install photonic-mode-solver

Package Overview
----------------

The package provides:

- Hybrid FEM-PINN mode solver implementation
- Support for rectangular and circular waveguide structures
- GDS/OASIS file geometry support
- KLayout compatibility
- Analytical solution validation framework

Usage Example
-------------

.. code-block:: python

   from photonic_mode_solver import ModeSolver
   from photonic_mode_solver.structures import WaveguideStructure

   # Create structure
   structure = WaveguideStructure(width=0.5, height=0.2)

   # Create hybrid solver
   solver = ModeSolver(use_pinn_initialization=True)

   # Solve for modes
   modes = solver.solve(structure)

Indices and Tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
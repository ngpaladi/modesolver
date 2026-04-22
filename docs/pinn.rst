PINN Implementation
===================

The Physics-Informed Neural Network (PINN) implementation is a core component of this photonic mode solver package. It provides a machine learning approach to solve electromagnetic mode problems by incorporating physical laws directly into the neural network architecture.

Architecture
------------

The PINN uses a feedforward neural network with the following characteristics:

- Input layer: Spatial coordinates (x, y) for waveguide domain
- Hidden layers: Multiple dense layers with Tanh activation functions
- Output layer: Field amplitude predictions for electromagnetic modes

Physics-Informed Loss Functions
-------------------------------

The PINN incorporates physics through specialized loss functions that ensure the network solutions satisfy the underlying PDEs:

- **Physics Loss**: Enforces the Helmholtz equation for electromagnetic wave propagation
- **Boundary Loss**: Ensures proper boundary conditions are satisfied
- **Initial Loss**: For time-dependent problems (if applicable)

Usage Example
-------------

.. code-block:: python

   from photonic_mode_solver.pinn import PINN
   import torch

   # Initialize PINN
   pinn = PINN(input_dim=2, hidden_dim=64, output_dim=1)

   # Train the PINN on photonic mode data
   # (Training process requires a dataset - see dataset generator)

Integration with FEM
--------------------

The PINN serves as an initial guess provider for the FEM solver:
- PINN provides fast, approximate solutions
- FEM refines solutions for high accuracy
- Hybrid approach accelerates convergence

API Reference
-------------

.. autoclass:: photonic_mode_solver.pinn.PINN
   :members:
   :undoc-members:
   :show-inheritance:
# AGENTS.md

This file contains essential information for developers working on the photonic mode solver project.

## Project Purpose
This repository implements a mode solver for electromagnetic waves in photonic chips using a hybrid approach combining Finite Element Methods (FEM) with Physics-Informed Neural Networks (PINNs).

## Implementation Approach
- Primary solver: FEM for high-accuracy results
- Initial guess provider: PINNs for rapid field approximation
- Hybrid integration: PINNs accelerate FEM convergence

## Technology Stack
- Python with NumPy/SciPy for numerical operations
- TensorFlow/PyTorch for PINN implementation
- FEniCS or similar for FEM solver
- GPU acceleration support (PyCUDA/CuPy)
- Visualization with Matplotlib/Plotly

## Key Considerations
- PINNs provide smooth initial approximations to reduce FEM iterations
- Material property handling requires dispersion modeling
- Boundary conditions require careful implementation for accuracy
- GPU acceleration recommended for performance

## PINN Implementation Details
- PINN architecture uses feedforward neural networks with Tanh activation
- Physics-informed loss functions incorporate Maxwell's equations
- Training supports both PyTorch and mock environments
- Dataset generation capabilities for synthetic training data
- Integration with FEM solver for hybrid approach

## Dataset Generation
- Synthetic datasets for rectangular and circular waveguides
- Analytical solutions for validation
- Training points with boundary condition enforcement
- KLayout-compatible GDS file generation
- Support for multiple material combinations

## Development Commands
- Run tests: python -m pytest (if test structure exists)
- Lint code: ruff check . (if linting configured)
- Typecheck: mypy . (if mypy configured)
- Format code: black . (if formatter configured)
- Build documentation: sphinx-build docs docs/_build
- Train PINNs: python train_pinn.py

## Important Constraints
- PINN approach requires training data generation for initial calibration
- Integration between PINN and FEM solvers requires careful handling of data formats
- Training requires proper physics-informed loss functions
- Dataset generation must provide sufficient diversity for generalization
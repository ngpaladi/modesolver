# photonic_mode_solver Package

This package implements a hybrid Finite Element Method (FEM) and Physics-Informed Neural Network (PINN) approach for solving electromagnetic mode problems in photonic chips.

## Package Structure

```
photonic_mode_solver/
├── __init__.py           # Package initialization and exports
├── solver.py             # Main ModeSolver class
├── fem.py                # FEM solver implementation
├── pinn.py               # PINN implementation
├── pinn_training.py      # PINN training framework
├── structures.py         # Photonic structure definitions
├── geometry.py           # GDS/OASIS file support
└── klayout.py            # KLayout compatibility
```

## Module Contents

### `__init__.py`

Package initialization and exports.

This file defines package metadata and exports main classes for easy import.

### `solver.py`

Main hybrid mode solver implementation.

This file implements the core `ModeSolver` class that combines:
- FEM solver for accurate computation
- PINN for fast initial guesses
- Hybrid approach with PINN acceleration

### `fem.py`

Finite Element Method solver implementation.

This file contains the `FEMSolver` class that:
- Sets up mesh generation
- Assembles stiffness (K) and mass (M) matrices
- Applies boundary conditions
- Solves generalized eigenvalue problems
- Extracts mode information

### `pinn.py`

Physics-Informed Neural Network implementation.

This file implements the `PINN` class that:
- Defines neural network architecture
- Provides prediction capabilities
- Implements training interface
- Handles both PyTorch and mock implementations

### `pinn_training.py`

PINN training framework.

This file provides the training infrastructure:
- Physics-informed loss calculation
- Training loop implementation
- Loss function components (physics, boundary, data)
- Model saving/loading capabilities

### `structures.py`

Photonic structure definitions.

This file defines different photonic waveguide structures:
- `WaveguideStructure`: Rectangular waveguides
- `CircularWaveguideStructure`: Circular waveguides
- Support for both simple and GDS/KLayout structures

### `geometry.py`

GDS/OASIS file geometry support.

This file provides:
- `GDSGeometryReader`: Reads GDS/OASIS files
- `GDSWaveguideStructure`: GDS-based structure definitions
- GDS file parsing and geometry extraction

### `klayout.py`

KLayout compatibility.

This file adds KLayout support:
- `KLayoutGeometryReader`: Enhanced GDS reader
- `KLayoutWaveguideStructure`: KLayout structure definitions
- KLayout-specific features (cell hierarchy, layer properties)
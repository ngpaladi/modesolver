# Photonic Mode Solver Package Structure

## Package Overview

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

## File-by-File Breakdown

### 1. `__init__.py`
**Purpose**: Package initialization and exports

This file:
- Defines package metadata (version, author)
- Exports main classes for easy import
- Provides unified import interface for all components

**Key Exports**:
- `ModeSolver`: Main hybrid solver
- `PINN`: Physics-Informed Neural Network
- `FEMSolver`: FEM implementation
- `WaveguideStructure`: Waveguide definitions
- `GDSWaveguideStructure`: GDS file support
- `KLayoutWaveguideStructure`: KLayout support

### 2. `solver.py`
**Purpose**: Main hybrid mode solver implementation

This file implements the core `ModeSolver` class that combines:
- FEM solver for accurate computation
- PINN for fast initial guesses
- Hybrid approach with PINN acceleration

**Key Features**:
- Initialize with PINN or FEM-only mode
- Solve photonic mode problems
- Validate against analytical solutions
- Integrate PINN initial guesses with FEM

### 3. `fem.py`
**Purpose**: Finite Element Method solver implementation

This file contains the `FEMSolver` class that:
- Sets up mesh generation
- Assembles stiffness (K) and mass (M) matrices
- Applies boundary conditions
- Solves generalized eigenvalue problems
- Extracts mode information

**Key Components**:
- Matrix assembly functions
- Eigenvalue solver with fallback to dense methods
- Boundary condition implementation
- Mode extraction from solutions

### 4. `pinn.py`
**Purpose**: Physics-Informed Neural Network implementation

This file implements the `PINN` class that:
- Defines neural network architecture
- Provides prediction capabilities
- Implements training interface
- Handles both PyTorch and mock implementations

**Key Features**:
- Feedforward neural network with Tanh activations
- Physics-informed loss functions
- Initial guess generation for FEM
- Mock implementation for environments without PyTorch

### 5. `pinn_training.py`
**Purpose**: PINN training framework

This file provides the training infrastructure:
- Physics-informed loss calculation
- Training loop implementation
- Loss function components (physics, boundary, data)
- Model saving/loading capabilities

**Key Components**:
- `PINN`: Extended neural network with training capabilities
- `PINNTrainer`: Training management class
- Physics loss functions for Helmholtz equation
- Validation monitoring

### 6. `structures.py`
**Purpose**: Photonic structure definitions

This file defines different photonic waveguide structures:
- `WaveguideStructure`: Rectangular waveguides
- `CircularWaveguideStructure`: Circular waveguides
- Support for both simple and GDS/KLayout structures

**Key Features**:
- Structure parameter definitions
- Mesh generation support
- Material property handling
- Analytical solution validation

### 7. `geometry.py`
**Purpose**: GDS/OASIS file geometry support

This file provides:
- `GDSGeometryReader`: Reads GDS/OASIS files
- `GDSWaveguideStructure`: GDS-based structure definitions
- GDS file parsing and geometry extraction

**Key Features**:
- GDS file reading with fallbacks
- Layer management
- Geometry information extraction
- Material assignment from GDS layers

### 8. `klayout.py`
**Purpose**: KLayout compatibility

This file adds KLayout support:
- `KLayoutGeometryReader`: Enhanced GDS reader
- `KLayoutWaveguideStructure`: KLayout structure definitions
- KLayout-specific features (cell hierarchy, layer properties)

**Key Features**:
- KLayout-specific geometry handling
- Cell hierarchy management
- Layer property support
- KLayout transformation handling

## Key Design Principles

### 1. **Hybrid Approach**
- Combines FEM accuracy with PINN speed
- PINN provides initial guesses to accelerate FEM convergence
- Maintains high accuracy while improving computational efficiency

### 2. **Extensibility**
- Modular design allows easy addition of new structure types
- Support for GDS/OASIS and KLayout files
- Backward compatibility maintained

### 3. **Error Validation**
- Built-in analytical solution validation
- Error metrics calculation for sub-1% targets
- Validation framework for accuracy assessment

## Dependencies

The package requires:
- Core: NumPy, SciPy, Matplotlib
- ML: PyTorch, TensorFlow (for PINNs)
- FEM: FEniCS (optional)
- GDS handling: gdstk
- KLayout: pyklayout (optional)

## Usage Pattern

```python
from photonic_mode_solver import ModeSolver
from photonic_mode_solver.structures import WaveguideStructure

# Create structure
structure = WaveguideStructure(width=0.5, height=0.2)

# Create hybrid solver
solver = ModeSolver(use_pinn_initialization=True)

# Solve for modes
modes = solver.solve(structure)
```

This design enables efficient, accurate photonic mode solving with support for complex geometries from industry-standard CAD formats.
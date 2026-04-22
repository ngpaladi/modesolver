# PINN Dataset Generator

This module provides functionality to generate synthetic datasets for training Physics-Informed Neural Networks (PINNs) for photonic mode solving.

## Features

- **Rectangular Waveguide Dataset Generation**
  - Generates waveguides with varying widths and heights
  - Supports multiple material combinations
  - Creates analytical solutions for validation

- **Circular Waveguide Dataset Generation**
  - Generates circular waveguides with varying radii
  - Supports multiple material combinations
  - Creates analytical solutions for validation

- **Training Data Generation**
  - Creates domain points for PINN training
  - Generates boundary conditions
  - Evaluates analytical field profiles

- **KLayout Compatibility**
  - Generates GDS files that can be opened in KLayout
  - Supports cell hierarchy and layer management

## Usage

```python
from dataset_generator import PINNDatasetGenerator

# Initialize generator
generator = PINNDatasetGenerator("my_datasets")

# Generate rectangular waveguide dataset
rectangular_data = generator.generate_rectangular_waveguide_dataset(
    num_samples=100,
    width_range=(0.2, 2.0),
    height_range=(0.1, 0.5)
)

# Generate circular waveguide dataset
circular_data = generator.generate_circular_waveguide_dataset(
    num_samples=50,
    radius_range=(0.1, 1.0)
)

# Save datasets
generator.save_dataset(rectangular_data, "rectangular_dataset.json")
generator.save_dataset(circular_data, "circular_dataset.json")

# Load datasets
loaded_data = generator.load_dataset("rectangular_dataset.json")
```

## Requirements

- Python 3.6+
- numpy
- json
- gdstk (optional, for GDS file generation)

## Dataset Structure

The generated datasets contain:
- Structure definitions with geometric parameters
- Material properties
- Analytical mode solutions
- Training points for PINN
- KLayout-compatible GDS files (when gdstk is available)

## Note

When gdstk is not available in the environment, GDS file generation is skipped but the dataset generation still works for the training data portion.
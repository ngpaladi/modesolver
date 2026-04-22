# KLayout CLI Tool for Photonic Mode Simulation

## Overview

The `klayout_simulate` command-line tool allows users to simulate photonic modes from KLayout-designed GDS files with plotting capabilities.

## Installation

Install the package with:
```bash
pip install -e .
```

## Usage

```bash
klayout_simulate input_file.gds [options]
```

### Examples

```bash
# Basic simulation with default settings
klayout_simulate waveguide.gds --layer 1

# Generate a field plot
klayout_simulate device.gds --layer 10 --plot-type field --output field.png

# Show plot in window and save to file
klayout_simulate structure.gds --layer 1 --mode 0 --output result.png --show

# Use specific KLayout cell
klayout_simulate layout.klayout.gds --layer 20 --klayout-cell "waveguide_cell" --output plot.pdf
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `input_file` | Input KLayout GDS file | Required |
| `--layer` | Layer number containing waveguide geometry | 0 |
| `--klayout-cell` | Specific KLayout cell name to use | None |
| `--frequency` | Operating frequency in micrometers | 1.55 |
| `--mode` | Mode index to plot | 0 |
| `--plot-type` | Type of plot to generate | field |
| `--output` | Output file path for plot | None |
| `--show` | Display plot in window | False |
| `--material` | Core material properties (n loss) | 3.4 0.01 |

## Plot Types

- `field`: Field amplitude distribution (default)
- `mode`: Mode comparison plots
- `both`: Both field and mode plots

## Requirements

The tool requires:
- Python 3.7+
- numpy
- matplotlib
- gdstk (for GDS file support)
- photonic-mode-solver package

## Example Workflow

1. **Create a KLayout design** with your photonic structures
2. **Export as GDS** file 
3. **Run simulation**:
   ```bash
   klayout_simulate design.gds --layer 1 --output modes.png
   ```
4. **View results** in generated plot file or interactive window

## Error Handling

The tool provides helpful error messages for:
- Missing input files
- Invalid layer numbers
- Unsupported file formats
- Plot generation failures

## Limitations

- The current implementation uses mock data for demonstration purposes
- Actual mode computation requires proper FEM and PINN implementations
- GDS file parsing is simplified for this example
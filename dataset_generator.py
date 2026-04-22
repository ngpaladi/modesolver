"""
PINN Dataset Generation Module
============================

This module generates synthetic datasets for training Physics-Informed Neural Networks
for photonic mode solving. It creates both training data and GDS files that can be opened
in KLayout for visualization and validation.

The generated datasets include:
- Rectangular waveguide structures with varying parameters
- Circular waveguide structures
- Analytical mode solutions for validation
- GDS files that can be opened in KLayout
"""

import numpy as np
import os
import json
from typing import Dict, List, Tuple, Any
from photonic_mode_solver.structures import WaveguideStructure, CircularWaveguideStructure
from photonic_mode_solver.geometry import GDSWaveguideStructure
from photonic_mode_solver.klayout import KLayoutWaveguideStructure

# Try to import gdstk, but handle when it's not available
try:
    import gdstk
    HAS_GDSTK = True
except ImportError:
    HAS_GDSTK = False
    print("Warning: gdstk not available. GDS file generation will be limited.")


class PINNDatasetGenerator:
    """Generate synthetic datasets for PINN training."""
    
    def __init__(self, output_dir: str = "datasets"):
        """Initialize dataset generator.
        
        Args:
            output_dir: Directory to store generated datasets and files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "gds"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "json"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "training_data"), exist_ok=True)
    
    def generate_rectangular_waveguide_dataset(self, 
                                             num_samples: int = 100,
                                             width_range: Tuple[float, float] = (0.2, 2.0),
                                             height_range: Tuple[float, float] = (0.1, 0.5),
                                             material_combinations: List[Dict] = None) -> Dict[str, Any]:
        """Generate a dataset of rectangular waveguide structures.
        
        Args:
            num_samples: Number of samples to generate
            width_range: Tuple of (min, max) width in micrometers
            height_range: Tuple of (min, max) height in micrometers
            material_combinations: List of material property dictionaries
            
        Returns:
            Dictionary containing generated data and structure definitions
        """
        if material_combinations is None:
            material_combinations = [
                {'core': {'n': 3.4, 'loss': 0.01}, 'cladding': {'n': 1.45, 'loss': 0.001}},
                {'core': {'n': 2.0, 'loss': 0.005}, 'cladding': {'n': 1.5, 'loss': 0.002}},
                {'core': {'n': 4.0, 'loss': 0.02}, 'cladding': {'n': 1.3, 'loss': 0.003}}
            ]
        
        structures = []
        training_data = []
        
        for i in range(num_samples):
            # Randomly select parameters
            width = np.random.uniform(width_range[0], width_range[1])
            height = np.random.uniform(height_range[0], height_range[1])
            material_idx = np.random.randint(0, len(material_combinations))
            material = material_combinations[material_idx]
            
            # Create structure
            structure = WaveguideStructure(
                width=width,
                height=height,
                core_material=material['core'],
                cladding_material=material['cladding']
            )
            
            # Generate analytical solutions
            analytical_modes = structure.analytical_modes()
            
            # Create training points for PINN
            pinn_training_points = self._generate_pinn_training_points(structure, analytical_modes)
            
            structures.append({
                'id': i,
                'width': width,
                'height': height,
                'core_material': material['core'],
                'cladding_material': material['cladding'],
                'analytical_modes': self._serialize_analytical_modes(analytical_modes)
            })
            
            training_data.append({
                'structure_id': i,
                'training_points': pinn_training_points
            })
            
            # Generate GDS file for KLayout compatibility
            self._generate_gds_file(structure, i, "rectangular")
            
        return {
            'structures': structures,
            'training_data': training_data,
            'metadata': {
                'dataset_type': 'rectangular_waveguide',
                'total_samples': num_samples,
                'width_range': width_range,
                'height_range': height_range,
                'material_combinations': material_combinations
            }
        }
    
    def generate_circular_waveguide_dataset(self,
                                          num_samples: int = 100,
                                          radius_range: Tuple[float, float] = (0.1, 1.0),
                                          material_combinations: List[Dict] = None) -> Dict[str, Any]:
        """Generate a dataset of circular waveguide structures.
        
        Args:
            num_samples: Number of samples to generate
            radius_range: Tuple of (min, max) radius in micrometers
            material_combinations: List of material property dictionaries
            
        Returns:
            Dictionary containing generated data and structure definitions
        """
        if material_combinations is None:
            material_combinations = [
                {'core': {'n': 3.4, 'loss': 0.01}, 'cladding': {'n': 1.45, 'loss': 0.001}},
                {'core': {'n': 2.0, 'loss': 0.005}, 'cladding': {'n': 1.5, 'loss': 0.002}},
                {'core': {'n': 4.0, 'loss': 0.02}, 'cladding': {'n': 1.3, 'loss': 0.003}}
            ]
        
        structures = []
        training_data = []
        
        for i in range(num_samples):
            # Randomly select parameters
            radius = np.random.uniform(radius_range[0], radius_range[1])
            material_idx = np.random.randint(0, len(material_combinations))
            material = material_combinations[material_idx]
            
            # Create structure
            structure = CircularWaveguideStructure(
                radius=radius,
                core_material=material['core'],
                cladding_material=material['cladding']
            )
            
            # Generate analytical solutions
            analytical_modes = structure.analytical_modes()
            
            # Create training points for PINN
            pinn_training_points = self._generate_pinn_training_points_circular(structure, analytical_modes)
            
            structures.append({
                'id': i,
                'radius': radius,
                'core_material': material['core'],
                'cladding_material': material['cladding'],
                'analytical_modes': self._serialize_analytical_modes(analytical_modes)
            })
            
            training_data.append({
                'structure_id': i,
                'training_points': pinn_training_points
            })
            
            # Generate GDS file for KLayout compatibility
            self._generate_gds_file_circular(structure, i, "circular")
            
        return {
            'structures': structures,
            'training_data': training_data,
            'metadata': {
                'dataset_type': 'circular_waveguide',
                'total_samples': num_samples,
                'radius_range': radius_range,
                'material_combinations': material_combinations
            }
        }
    
    def _generate_pinn_training_points(self, structure: WaveguideStructure, 
                                     analytical_modes: Dict) -> Dict:
        """Generate training points for PINN training.
        
        Args:
            structure: Waveguide structure
            analytical_modes: Analytical mode solutions
            
        Returns:
            Dictionary of training points
        """
        # Generate points in the waveguide domain
        x_range = np.linspace(0, structure.width, 50)
        y_range = np.linspace(0, structure.height, 50)
        X, Y = np.meshgrid(x_range, y_range)
        
        # Create training points
        training_points = {
            'domain': {
                'x': X.flatten().tolist(),
                'y': Y.flatten().tolist()
            },
            'boundary': {
                'x': [0, structure.width, structure.width, 0, 0],  # Square boundary
                'y': [0, 0, structure.height, structure.height, 0]
            },
            'analytical': {
                'propagation_constant': analytical_modes['fundamental_mode']['propagation_constant'],
                'field_profile': self._evaluate_field_profile(
                    structure,
                    analytical_modes['fundamental_mode']['field_profile'],
                    X, Y
                )
            }
        }
        
        return training_points
    
    def _generate_pinn_training_points_circular(self, structure: CircularWaveguideStructure, 
                                              analytical_modes: Dict) -> Dict:
        """Generate training points for PINN training of circular waveguides.
        
        Args:
            structure: Circular waveguide structure
            analytical_modes: Analytical mode solutions
            
        Returns:
            Dictionary of training points
        """
        # Generate points in the circular domain (polar coordinates)
        r_range = np.linspace(0, structure.radius, 30)
        theta_range = np.linspace(0, 2*np.pi, 30)
        R, Theta = np.meshgrid(r_range, theta_range)
        
        # Convert to Cartesian coordinates
        X = R * np.cos(Theta)
        Y = R * np.sin(Theta)
        
        # Create training points
        training_points = {
            'domain': {
                'x': X.flatten().tolist(),
                'y': Y.flatten().tolist()
            },
            'boundary': {
                'x': [structure.radius * np.cos(theta) for theta in np.linspace(0, 2*np.pi, 20)],
                'y': [structure.radius * np.sin(theta) for theta in np.linspace(0, 2*np.pi, 20)]
            },
            'analytical': {
                'propagation_constant': analytical_modes['fundamental_mode']['propagation_constant'],
                'field_profile': self._evaluate_field_profile_circular(
                    structure,
                    analytical_modes['fundamental_mode']['field_profile'],
                    R, Theta
                )
            }
        }
        
        return training_points
    
    def _evaluate_field_profile(self, structure: WaveguideStructure, 
                              field_func, X: np.ndarray, Y: np.ndarray) -> List[float]:
        """Evaluate field profile at given coordinates.
        
        Args:
            structure: Waveguide structure
            field_func: Field profile function
            X, Y: Coordinate arrays
            
        Returns:
            List of field values
        """
        field_values = []
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                x = X[i, j]
                y = Y[i, j]
                # Normalize coordinates to the structure
                if structure.width > 0 and structure.height > 0:
                    normalized_x = x / structure.width
                    normalized_y = y / structure.height
                    field_value = field_func(normalized_x, normalized_y)
                    field_values.append(float(field_value))
                else:
                    field_values.append(0.0)
        
        return field_values
    
    def _serialize_analytical_modes(self, analytical_modes: Dict) -> Dict:
        """Convert analytical modes to serializable format.
        
        Args:
            analytical_modes: Dictionary of analytical modes
            
        Returns:
            Serializable dictionary
        """
        # Create a copy without function objects
        serializable = {}
        for mode_name, mode_data in analytical_modes.items():
            serializable[mode_name] = {}
            for key, value in mode_data.items():
                if key == 'field_profile':
                    # Skip field_profile function for serialization
                    # We'll store the evaluated values instead
                    serializable[mode_name][key] = 'function_object'  # placeholder
                else:
                    serializable[mode_name][key] = value
        return serializable
    
    def _evaluate_field_profile_circular(self, structure: CircularWaveguideStructure, 
                                       field_func, R: np.ndarray, Theta: np.ndarray) -> List[float]:
        """Evaluate circular field profile at given coordinates.
        
        Args:
            structure: Circular waveguide structure
            field_func: Field profile function
            R, Theta: Coordinate arrays
            
        Returns:
            List of field values
        """
        field_values = []
        for i in range(R.shape[0]):
            for j in range(R.shape[1]):
                r = R[i, j]
                theta = Theta[i, j]
                # Normalize radius to the structure
                if structure.radius > 0:
                    normalized_r = r / structure.radius
                    field_value = field_func(normalized_r, theta)
                    field_values.append(float(field_value))
                else:
                    field_values.append(0.0)
        
        return field_values
    
    def _generate_gds_file(self, structure: WaveguideStructure, 
                          sample_id: int, structure_type: str) -> str:
        """Generate a GDS file for KLayout compatibility.
        
        Args:
            structure: Waveguide structure
            sample_id: Sample identifier
            structure_type: Type of structure ('rectangular' or 'circular')
            
        Returns:
            Path to generated GDS file (or None if gdstk not available)
        """
        if not HAS_GDSTK:
            print("Skipping GDS file generation - gdstk not available")
            return None
            
        gds_filename = f"{structure_type}_waveguide_{sample_id:04d}.gds"
        gds_path = os.path.join(self.output_dir, "gds", gds_filename)
        
        # Create GDS library
        lib = gdstk.Library()
        
        # Create a cell for the waveguide
        cell = lib.new_cell("WAVEGUIDE")
        
        # Create rectangular waveguide shape
        if structure_type == "rectangular":
            # Create waveguide rectangle
            rect = gdstk.Rectangle(
                (0, 0), 
                (structure.width, structure.height),
                layer=0,
                datatype=0
            )
            cell.add(rect)
            
        # For circular waveguides, create a circular shape
        elif structure_type == "circular":
            # Create circular waveguide (annulus)
            outer_circle = gdstk.Circle((0, 0), structure.radius, layer=0, datatype=0)
            cell.add(outer_circle)
            
            # Add a hole for the core material
            inner_circle = gdstk.Circle((0, 0), structure.radius * 0.3, layer=1, datatype=0)
            cell.add(inner_circle)
        
        # Add some metadata as text labels
        text = gdstk.Text(f"ID: {sample_id}", 0.1, (0.1, 0.1), layer=2)
        cell.add(text)
        
        # Save the library
        lib.write_gds(gds_path)
        
        return gds_path
    
    def _generate_gds_file_circular(self, structure: CircularWaveguideStructure, 
                                  sample_id: int, structure_type: str) -> str:
        """Generate a GDS file for circular waveguide."""
        if not HAS_GDSTK:
            print("Skipping GDS file generation - gdstk not available")
            return None
        return self._generate_gds_file(structure, sample_id, structure_type)
    
    def save_dataset(self, dataset: Dict, filename: str) -> str:
        """Save dataset to JSON file.
        
        Args:
            dataset: Dataset dictionary
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        json_path = os.path.join(self.output_dir, "json", filename)
        with open(json_path, 'w') as f:
            json.dump(dataset, f, indent=2)
        return json_path
    
    def load_dataset(self, filename: str) -> Dict:
        """Load dataset from JSON file.
        
        Args:
            filename: Input filename
            
        Returns:
            Dataset dictionary
        """
        json_path = os.path.join(self.output_dir, "json", filename)
        with open(json_path, 'r') as f:
            return json.load(f)


def main():
    """Main function to demonstrate dataset generation."""
    print("Generating PINN training datasets...")
    
    # Initialize dataset generator
    generator = PINNDatasetGenerator()
    
    # Generate rectangular waveguide dataset
    print("Generating rectangular waveguide dataset...")
    rectangular_data = generator.generate_rectangular_waveguide_dataset(
        num_samples=20,
        width_range=(0.2, 2.0),
        height_range=(0.1, 0.5)
    )
    
    # Save rectangular dataset
    rect_filename = "rectangular_waveguide_dataset.json"
    generator.save_dataset(rectangular_data, rect_filename)
    print(f"Saved rectangular dataset to {rect_filename}")
    
    # Generate circular waveguide dataset
    print("Generating circular waveguide dataset...")
    circular_data = generator.generate_circular_waveguide_dataset(
        num_samples=15,
        radius_range=(0.1, 1.0)
    )
    
    # Save circular dataset
    circ_filename = "circular_waveguide_dataset.json"
    generator.save_dataset(circular_data, circ_filename)
    print(f"Saved circular dataset to {circ_filename}")
    
    print("Dataset generation complete!")


if __name__ == "__main__":
    main()
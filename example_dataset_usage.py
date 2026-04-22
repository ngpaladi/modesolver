#!/usr/bin/env python3
"""
Example usage of the PINN dataset generator for training
"""

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dataset_generator import PINNDatasetGenerator

def example_usage():
    """Example showing how to use the dataset generator."""
    print("PINN Dataset Generator Example Usage")
    print("=" * 40)
    
    # Create dataset generator
    generator = PINNDatasetGenerator("example_datasets")
    
    # Generate a small dataset for demonstration
    print("1. Generating sample datasets...")
    
    # Rectangular waveguide dataset
    rectangular_data = generator.generate_rectangular_waveguide_dataset(
        num_samples=5,
        width_range=(0.2, 1.0),
        height_range=(0.1, 0.3)
    )
    
    # Circular waveguide dataset  
    circular_data = generator.generate_circular_waveguide_dataset(
        num_samples=3,
        radius_range=(0.1, 0.5)
    )
    
    # Save datasets
    generator.save_dataset(rectangular_data, "example_rectangular.json")
    generator.save_dataset(circular_data, "example_circular.json")
    
    print("2. Dataset files created:")
    print("   - example_datasets/json/example_rectangular.json")
    print("   - example_datasets/json/example_circular.json")
    
    # Load and examine the data
    print("3. Loading and examining data...")
    
    loaded_rect = generator.load_dataset("example_rectangular.json")
    print(f"   Loaded rectangular dataset with {len(loaded_rect['structures'])} structures")
    
    loaded_circ = generator.load_dataset("example_circular.json")
    print(f"   Loaded circular dataset with {len(loaded_circ['structures'])} structures")
    
    # Show sample structure details
    if loaded_rect['structures']:
        sample_struct = loaded_rect['structures'][0]
        print(f"4. Sample structure details:")
        print(f"   ID: {sample_struct['id']}")
        print(f"   Width: {sample_struct['width']:.2f} μm")
        print(f"   Height: {sample_struct['height']:.2f} μm")
        print(f"   Core material n: {sample_struct['core_material']['n']}")
        print(f"   Cladding material n: {sample_struct['cladding_material']['n']}")
    
    print("\n5. The generated datasets can now be used for:")
    print("   - PINN training with different waveguide geometries")
    print("   - Analytical validation of mode solutions")
    print("   - KLayout visualization (when gdstk is available)")
    
    print("\nExample complete!")

if __name__ == "__main__":
    example_usage()
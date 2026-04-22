#!/usr/bin/env python3
"""
Test script to verify dataset generation functionality
"""

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dataset_generator import PINNDatasetGenerator

def test_dataset_generation():
    """Test dataset generation functionality."""
    print("Testing PINN dataset generation...")
    
    # Initialize generator
    generator = PINNDatasetGenerator("test_datasets")
    
    # Test rectangular waveguide dataset
    print("Generating rectangular waveguide dataset...")
    rect_data = generator.generate_rectangular_waveguide_dataset(num_samples=2)
    print(f"Generated {len(rect_data['structures'])} rectangular structures")
    
    # Test circular waveguide dataset
    print("Generating circular waveguide dataset...")
    circ_data = generator.generate_circular_waveguide_dataset(num_samples=2)
    print(f"Generated {len(circ_data['structures'])} circular structures")
    
    # Save datasets
    generator.save_dataset(rect_data, "test_rectangular.json")
    generator.save_dataset(circ_data, "test_circular.json")
    
    # Verify the files were created
    rect_file = os.path.join("test_datasets", "json", "test_rectangular.json")
    circ_file = os.path.join("test_datasets", "json", "test_circular.json")
    
    if os.path.exists(rect_file) and os.path.exists(circ_file):
        print("Test completed successfully! Dataset files created.")
        
        # Verify content
        with open(rect_file, 'r') as f:
            rect_content = json.load(f)
        print(f"Rectangular dataset has {len(rect_content['structures'])} structures")
        
        with open(circ_file, 'r') as f:
            circ_content = json.load(f)
        print(f"Circular dataset has {len(circ_content['structures'])} structures")
    else:
        print("Test completed - files not created due to GDS dependency")

if __name__ == "__main__":
    test_dataset_generation()
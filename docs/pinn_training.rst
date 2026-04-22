PINN Training and Dataset Generation
====================================

This section covers the procedures for generating training datasets and training PINNs for photonic mode solving.

Dataset Generation
------------------

The dataset generator creates synthetic training data for PINNs with the following features:

- Rectangular waveguide structures with varying dimensions and materials
- Circular waveguide structures with varying radii  
- Analytical mode solutions for validation
- Training points for PINN training
- KLayout-compatible GDS files (when gdstk is available)

Usage Example
~~~~~~~~~~~~~

.. code-block:: python

   from dataset_generator import PINNDatasetGenerator

   # Initialize generator
   generator = PINNDatasetGenerator("datasets")

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

   # Save datasets for training
   generator.save_dataset(rectangular_data, "rectangular_dataset.json")
   generator.save_dataset(circular_data, "circular_dataset.json")

Training Procedures
-------------------

The PINN training process involves the following steps:

1. **Data Preparation**: Using generated datasets with proper structure definitions
2. **Model Initialization**: Creating PINN with appropriate architecture
3. **Training Setup**: Configuring loss functions and optimization parameters
4. **Training Execution**: Running the training loop with physics-informed loss
5. **Validation**: Monitoring convergence and validation metrics

Example Training Script
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from dataset_generator import PINNDatasetGenerator
   from photonic_mode_solver.pinn import PINN
   from photonic_mode_solver.structures import WaveguideStructure

   # Generate training data
   generator = PINNDatasetGenerator("train_datasets")
   dataset = generator.generate_rectangular_waveguide_dataset(num_samples=10)

   # Create PINN model
   pinn = PINN(input_dim=2, hidden_layers=[64, 64, 64], output_dim=1)

   # Train on first structure
   if dataset['structures']:
       structure_data = dataset['structures'][0]
       structure = WaveguideStructure(
           width=structure_data['width'],
           height=structure_data['height'],
           core_material=structure_data['core_material'],
           cladding_material=structure_data['cladding_material']
       )
       
       # Get analytical solution
       analytical_modes = structure.analytical_modes()
       
       # Train the PINN
       history = pinn.train(
           structure=structure,
           frequency=1.55,
           analytical_solution=analytical_modes
       )
       
       print(f"Training completed with {len(history['train_losses'])} epochs")

Training Parameters
~~~~~~~~~~~~~~~~~~~

The training process supports several configurable parameters:

- ``epochs``: Number of training iterations (default: 1000)
- ``learning_rate``: Optimization learning rate (default: 0.001)
- ``validation_split``: Fraction of data to use for validation (default: 0.2)
- ``early_stopping_patience``: Epochs to wait for improvement before stopping (default: 50)

Physics-Informed Loss Functions
-------------------------------

The PINN training uses specialized loss functions that incorporate physical laws:

- **Data Loss**: Measures difference between predicted and actual field values
- **Physics Loss**: Enforces the Helmholtz equation for electromagnetic wave propagation
- **Boundary Loss**: Ensures proper boundary conditions are satisfied

Convergence Monitoring
----------------------

The training process includes built-in convergence monitoring:

- Real-time loss tracking
- Early stopping to prevent overfitting
- Validation loss monitoring
- Training history preservation

Example of Convergence Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # After training
   history = pinn.get_training_history()
   
   # Plot training progress
   import matplotlib.pyplot as plt
   
   plt.figure(figsize=(10, 6))
   plt.plot(history['train_losses'], label='Training Loss')
   plt.plot(history['val_losses'], label='Validation Loss')
   plt.xlabel('Epoch')
   plt.ylabel('Loss')
   plt.legend()
   plt.title('PINN Training Convergence')
   plt.show()

Best Practices for Training
---------------------------

1. **Dataset Quality**: Ensure diverse waveguide geometries for good generalization
2. **Architecture Selection**: Choose appropriate network depth and width
3. **Learning Rate**: Start with 0.001 and adjust based on convergence
4. **Regularization**: Use weight decay and early stopping
5. **Validation**: Monitor both training and validation loss
6. **Physics Informed**: Ensure physics loss terms are properly weighted

.. note::
   
   The training process will work in both PyTorch and mock modes. In environments without PyTorch, 
   the training will show a mock implementation but the data generation and model structure remain functional.
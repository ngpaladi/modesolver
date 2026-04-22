Command Line Interface
======================

The photonic mode solver provides a command-line interface for convenient usage without requiring Python scripting.

Installation
------------

The CLI can be installed along with the package:

.. code-block:: bash

   pip install photonic-mode-solver

Available Commands
------------------

The CLI provides several commands for different functionalities:

``klayout_simulate``

This command provides a simulation interface for photonic structures with KLayout integration.

.. code-block:: bash

   klayout_simulate --help

Usage Examples
--------------

Basic Usage
~~~~~~~~~~~

.. code-block:: bash

   # Run simulation with default parameters
   klayout_simulate

   # Run with specific waveguide dimensions
   klayout_simulate --width 0.5 --height 0.2

   # Run with custom material properties
   klayout_simulate --core-n 3.4 --cladding-n 1.45

Advanced Usage
~~~~~~~~~~~~~~

.. code-block:: bash

   # Specify input GDS file for complex geometries
   klayout_simulate --gds-file path/to/structure.gds --layer 0

   # Set wavelength for simulation
   klayout_simulate --wavelength 1.55

   # Enable verbose output
   klayout_simulate --verbose

CLI Options
-----------

The CLI accepts various options for configuration:

- ``--width`` / ``-w``: Waveguide width in micrometers
- ``--height`` / ``-h``: Waveguide height in micrometers
- ``--radius`` / ``-r``: Waveguide radius in micrometers
- ``--core-n`` / ``--core-n``: Core refractive index
- ``--cladding-n`` / ``--cladding-n``: Cladding refractive index
- ``--wavelength`` / ``-l``: Operating wavelength in micrometers
- ``--gds-file`` / ``-g``: Path to GDS file for complex structures
- ``--layer`` / ``-L``: GDS layer number
- ``--verbose`` / ``-v``: Enable verbose output
- ``--help`` / ``-h``: Show help message

Integration with KLayout
------------------------

The CLI can integrate with KLayout for:
- Complex waveguide structure definition
- Cell hierarchy management
- Layer property handling
- KLayout-specific transformations

Example Workflow
----------------

.. code-block:: bash

   # Generate a rectangular waveguide simulation
   klayout_simulate --width 0.5 --height 0.2 --wavelength 1.55 --verbose

   # Process a KLayout GDS file
   klayout_simulate --gds-file waveguide.gds --layer 0 --verbose
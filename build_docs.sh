#!/bin/bash
# Script to build documentation (for local testing)

# Create build directory
mkdir -p docs/_build

# Create a simple HTML version of the documentation for testing
cat > docs/_build/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Photonic Mode Solver - Documentation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f8f9fa;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
        }
        .section {
            margin: 20px 0;
        }
        code {
            background-color: #f5f5f5;
            padding: 2px 4px;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Photonic Mode Solver Documentation</h1>
        
        <div class="section">
            <h2>Overview</h2>
            <p>This documentation site demonstrates the photonic mode solver package structure.</p>
        </div>

        <div class="section">
            <h2>Package Structure</h2>
            <p>The package contains the following main modules:</p>
            <ul>
                <li><code>solver.py</code> - Main hybrid solver implementation</li>
                <li><code>fem.py</code> - FEM solver implementation</li>
                <li><code>pinn.py</code> - PINN implementation</li>
                <li><code>structures.py</code> - Waveguide structure definitions</li>
                <li><code>geometry.py</code> - GDS/OASIS file support</li>
                <li><code>klayout.py</code> - KLayout compatibility</li>
            </ul>
        </div>

        <div class="section">
            <h2>Installation</h2>
            <p>Install using pip:</p>
            <code>pip install photonic-mode-solver</code>
        </div>

        <div class="section">
            <h2>Usage Example</h2>
            <pre><code>from photonic_mode_solver import ModeSolver
from photonic_mode_solver.structures import WaveguideStructure

# Create structure
structure = WaveguideStructure(width=0.5, height=0.2)

# Create hybrid solver
solver = ModeSolver(use_pinn_initialization=True)

# Solve for modes
modes = solver.solve(structure)</code></pre>
        </div>
    </div>
</body>
</html>
EOF

echo "Documentation built successfully!"
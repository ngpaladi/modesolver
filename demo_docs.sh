#!/bin/bash

echo "Photonic Mode Solver Documentation Demo"
echo "======================================"

echo "The documentation has been built successfully in docs/_build/"
echo ""
echo "To view the documentation in your browser, please open:"
echo "file://$(pwd)/docs/_build/index.html"
echo ""
echo "Or you can manually browse the files in docs/_build/ directory:"
echo "  - index.html - Main documentation page"
echo "  - modules.html - Module documentation"
echo "  - photonic_mode_solver.html - API reference"
echo ""
echo "If you want to serve the documentation locally:"
echo "cd docs/_build && python -m http.server 8000"
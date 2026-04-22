#!/bin/bash
# Test script to verify the package works correctly

echo "Running tests for photonic-mode-solver..."

# Install dependencies
echo "Installing dependencies..."
pip install -e .

# Run tests
echo "Running pytest..."
python -m pytest tests/ -v

echo "Test execution completed."
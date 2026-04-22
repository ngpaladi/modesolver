#!/bin/bash

# Setup script for photonic mode solver environment
# This script creates a virtual environment and installs all dependencies

set -e  # Exit on any error

echo "Setting up photonic mode solver environment..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

# Install the package in development mode
echo "Installing package in development mode..."
pip install -e .

echo "Setup complete!"
echo "To activate the environment in future sessions, run:"
echo "source venv/bin/activate"
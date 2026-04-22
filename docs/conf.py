# Configuration file for the Sphinx documentation builder.

# This file only contains a selection of the most common options. For a
# full list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# Path setup
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# Project information
project = 'photonic-mode-solver'
copyright = '2024, Photonic Solver Team'
author = 'Photonic Solver Team'

# The full version, including alpha/beta/rc tags
release = '0.1.0'

# Extensions (or modules to document with autodoc)
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
]

# Template paths
templates_path = ['_templates']

# Source suffix
source_suffix = '.rst'

# Master document
master_doc = 'index'

# List of patterns to ignore
exclude_patterns = []

# HTML theme
html_theme = 'sphinx_rtd_theme'

# HTML static paths
html_static_path = ['_static']

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}
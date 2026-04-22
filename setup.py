from setuptools import setup, find_packages

setup(
    name="photonic-mode-solver",
    version="0.1.0",
    author="Photonic Solver Team",
    author_email="contact@photonic-solver.org",
    description="A hybrid FEM-PINN mode solver for photonic chips",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/photonic-mode-solver",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "matplotlib>=3.3.0",
        "torch>=1.9.0",
        "tensorflow>=2.5.0",
        "gdstk>=0.6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "klayout_simulate=bin.klayout_simulate:main",
        ],
    },
    scripts=['bin/klayout_simulate']
)
"""
KLayout Geometry Analyzer for Photonic Structures
===============================================

Analyzes KLayout GDS files to determine waveguide structures and their properties.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional

# Mock gdstk for environments without it
try:
    import gdstk
    HAS_GDSTK = True
except ImportError:
    HAS_GDSTK = False
    # Mock classes for gdstk
    class MockGdstk:
        def read_gds(self, file_path):
            return MockLibrary()
    
    class MockLibrary:
        def __init__(self):
            self.cells = []
    
    class MockCell:
        def __init__(self):
            self.name = "mock"
            self.shapes = []
            self.bounding_box = None
            
        def __iter__(self):
            return iter(self.shapes)
            
    class MockShape:
        def __init__(self):
            self.bounding_box = None
            self.area = 0
            self.length = 0
            
        def __getattr__(self, name):
            return None
    
    gdstk = MockGdstk()

class WavepacketAnalyzer:
    """Analyzes waveguide structures from KLayout GDS files."""
    
    def __init__(self, gds_file_path: str):
        """
        Initialize analyzer.
        
        Args:
            gds_file_path: Path to KLayout GDS file
        """
        self.gds_file_path = gds_file_path
        self.library = None
        self.waveguides = []
        self.analysis_results = {}
        
    def analyze(self) -> Dict:
        """
        Analyze the GDS file for waveguide structures.
        
        Returns:
            Dictionary with analysis results
        """
        if not HAS_GDSTK:
            print("gdstk not available - using mock analysis")
            return self._mock_analysis()
            
        try:
            # Read the GDS file
            self.library = gdstk.read_gds(self.gds_file_path)
            
            # Analyze all cells
            for cell in self.library.cells:
                cell_analysis = self._analyze_cell(cell)
                if cell_analysis:
                    self.analysis_results[cell.name] = cell_analysis
                    
            # Identify waveguides based on geometric properties
            self._identify_waveguides()
            
            return self.analysis_results
            
        except Exception as e:
            print(f"Error analyzing GDS file: {e}")
            return {}
            
    def _mock_analysis(self) -> Dict:
        """Mock analysis for environments without gdstk."""
        return {
            'mock_analysis': {
                'total_cells': 1,
                'total_shapes': 0,
                'waveguides_found': 0,
                'waveguide_dimensions': []
            }
        }
            
    def _analyze_cell(self, cell) -> Optional[Dict]:
        """
        Analyze a single cell for waveguide characteristics.
        
        Args:
            cell: GDS cell object
            
        Returns:
            Analysis results for the cell
        """
        if not HAS_GDSTK:
            return self._mock_cell_analysis(cell)
            
        cell_info = {
            'name': cell.name,
            'shapes': [],
            'layers': [],
            'bounding_box': None,
            'geometric_properties': {}
        }
        
        # Analyze shapes in the cell
        for shape in cell:
            shape_info = self._analyze_shape(shape)
            cell_info['shapes'].append(shape_info)
            
        # Get bounding box for the cell
        if cell.bounding_box is not None:
            cell_info['bounding_box'] = {
                'min': tuple(cell.bounding_box[0]),
                'max': tuple(cell.bounding_box[1])
            }
            
        return cell_info
        
    def _mock_cell_analysis(self, cell) -> Optional[Dict]:
        """Mock cell analysis."""
        return {
            'name': cell.name if hasattr(cell, 'name') else 'mock_cell',
            'shapes': [],
            'bounding_box': None,
            'geometric_properties': {}
        }
        
    def _analyze_shape(self, shape) -> Dict:
        """
        Analyze individual shapes for waveguide characteristics.
        
        Args:
            shape: GDS shape object
            
        Returns:
            Shape analysis results
        """
        if not HAS_GDSTK:
            return self._mock_shape_analysis(shape)
            
        shape_info = {
            'type': type(shape).__name__,
            'area': None,
            'perimeter': None,
            'bounding_box': None,
            'properties': {}
        }
        
        # Get geometric properties
        if hasattr(shape, 'area'):
            shape_info['area'] = shape.area
        if hasattr(shape, 'length'):
            shape_info['perimeter'] = shape.length
            
        # Get bounding box
        if hasattr(shape, 'bounding_box'):
            shape_info['bounding_box'] = {
                'min': tuple(shape.bounding_box[0]),
                'max': tuple(shape.bounding_box[1])
            }
            
        # Analyze based on shape type
        if isinstance(shape, gdstk.Rectangle):
            shape_info['properties']['width'] = abs(shape.bounding_box[1][0] - shape.bounding_box[0][0])
            shape_info['properties']['height'] = abs(shape.bounding_box[1][1] - shape.bounding_box[0][1])
            shape_info['properties']['is_rectangular'] = True
            
        elif isinstance(shape, gdstk.Polygon):
            # For polygon shapes, estimate dimensions
            if shape.bounding_box:
                width = abs(shape.bounding_box[1][0] - shape.bounding_box[0][0])
                height = abs(shape.bounding_box[1][1] - shape.bounding_box[0][1])
                shape_info['properties']['width'] = width
                shape_info['properties']['height'] = height
                shape_info['properties']['is_polygon'] = True
                
        return shape_info
        
    def _mock_shape_analysis(self, shape) -> Dict:
        """Mock shape analysis."""
        return {
            'type': type(shape).__name__,
            'area': 0,
            'perimeter': 0,
            'bounding_box': None,
            'properties': {}
        }
        
    def _identify_waveguides(self):
        """
        Identify waveguide structures based on geometric analysis.
        """
        if not HAS_GDSTK:
            return
            
        waveguides_found = []
        
        for cell_name, cell_info in self.analysis_results.items():
            # Look for rectangular shapes that might be waveguides
            for shape in cell_info['shapes']:
                props = shape.get('properties', {})
                
                # Check if this looks like a waveguide (rectangular shape with reasonable dimensions)
                if props.get('is_rectangular', False):
                    width = props.get('width', 0)
                    height = props.get('height', 0)
                    
                    # Waveguides typically have width and height greater than a minimum threshold
                    if width > 0.1 and height > 0.1:  # Threshold in micrometers
                        waveguide_info = {
                            'cell': cell_name,
                            'shape': shape,
                            'dimensions': {
                                'width': width,
                                'height': height
                            },
                            'layer': 'unknown_layer'  # Would need to determine from GDS
                        }
                        waveguides_found.append(waveguide_info)
                        
        self.waveguides = waveguides_found
        
    def get_waveguide_info(self) -> List[Dict]:
        """
        Get identified waveguide information.
        
        Returns:
            List of waveguide information dictionaries
        """
        return self.waveguides
        
    def get_structure_summary(self) -> Dict:
        """
        Get a summary of the structure.
        
        Returns:
            Summary of structure characteristics
        """
        if not HAS_GDSTK:
            return self._mock_summary()
            
        summary = {
            'total_cells': len(self.library.cells) if self.library else 0,
            'total_shapes': 0,
            'waveguides_found': len(self.waveguides),
            'waveguide_dimensions': []
        }
        
        # Count shapes
        if self.library:
            for cell in self.library.cells:
                summary['total_shapes'] += len(cell)
                
        # Get waveguide dimensions
        for waveguide in self.waveguides:
            summary['waveguide_dimensions'].append(waveguide['dimensions'])
            
        return summary
        
    def _mock_summary(self) -> Dict:
        """Mock summary for environments without gdstk."""
        return {
            'total_cells': 1,
            'total_shapes': 0,
            'waveguides_found': 0,
            'waveguide_dimensions': []
        }

def analyze_gds_wavepackets(gds_file_path: str) -> Dict:
    """
    Analyze GDS file to determine wavepacket properties.
    
    Args:
        gds_file_path: Path to GDS file
        
    Returns:
        Analysis results with wavepacket information
    """
    analyzer = WavepacketAnalyzer(gds_file_path)
    results = analyzer.analyze()
    
    # Create a simplified summary for the package
    summary = analyzer.get_structure_summary()
    
    return {
        'analysis': results,
        'summary': summary,
        'waveguides': analyzer.get_waveguide_info()
    }
"""Factory for creating document converters."""

from .base_converter import DocumentConverter
from .libreoffice_converter import LibreOfficeConverter

def get_converter(converter_name='libreoffice'):
    """
    Returns a document converter factory function based on the specified name.
    
    Args:
        converter_name (str): Name of the converter to use.
        
    Returns:
        function: A factory function that creates and returns a converter instance.
    """
    converters = {
        'libreoffice': lambda output_folder: LibreOfficeConverter(output_folder)
        # Add more converters here as they're implemented
    }
    
    factory = converters.get(converter_name.lower())
    if not factory:
        print(f"Warning: Converter '{converter_name}' not found. Using LibreOffice converter.")
        factory = converters['libreoffice']
    
    return factory
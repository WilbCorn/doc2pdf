"""Base class for document converters."""

from abc import ABC, abstractmethod

class DocumentConverter(ABC):
    """Abstract base class for document converters."""
    
    def __init__(self, output_folder):
        """
        Initialize the document converter.
        
        Args:
            output_folder (str): The folder where converted files will be saved.
        """
        self.output_folder = output_folder
    
    @abstractmethod
    def process(self, file_paths):
        """
        Process the specified files and convert them to PDF.
        
        Args:
            file_paths (list): List of file paths to convert.
            
        Returns:
            int: Number of files successfully converted.
        """
        pass
from abc import abstractmethod, ABC
from typing import List


class ppt_to_pdf(ABC):
    """
    Abstract base class for converting PowerPoint files to PDF.
    This class defines the interface for the conversion process.
    """

    def __init__(self, output_folder: str):
        """
        Initialize the ppt_to_pdf class.
        :param output_folder: The folder where the converted PDF files will be saved.
        """
        self.output_folder = output_folder

    @abstractmethod
    def process(self, input_file_paths: List):
        pass
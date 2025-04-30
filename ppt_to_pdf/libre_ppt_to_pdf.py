import os
import subprocess
from typing import List
from ppt_to_pdf.ppt_to_pdf import ppt_to_pdf


class libre_ppt_to_pdf(ppt_to_pdf):

    def __init__(self, output_folder: str):
        """
        Initialize the libre_ppt_to_pdf class.
        :param output_folder: The folder where the converted PDF files will be saved.
        """
        super().__init__(output_folder)

    """Convert PowerPoint files to PDF using LibreOffice."""
    def process(self, input_file_paths: List):
        """
        Convert PowerPoint files to PDF using LibreOffice.
        :param input_file_paths: List of input file paths to be converted.
        """
        total_files = len(input_file_paths)
        processed_files = 0
        # Use a copy for iteration as we might modify the list if zip contains zips (though not handled recursively here)
        paths_to_process = list(input_file_paths) 

        while paths_to_process:
            path = paths_to_process.pop(0)
            processed_files += 1
            
            # Check if the path is still valid (might have been in a deleted temp dir if error occurred)
            if not os.path.exists(path):
                print(f"Skipping missing file: {path}")
                continue

            # Ensure the output directory exists (including any subfolders)
            output_path = os.path.join(self.output_folder, os.path.splitext(os.path.basename(path))[0] + '.pdf')
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Uses LibreOffice to convert ppt files to pdf
            print(f"({processed_files}/{total_files}) Converting '{os.path.basename(path)}'...")
            try:
                subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', 
                               os.path.dirname(output_path) or self.output_folder, path], 
                               check=True, capture_output=True)
                print(f"Successfully converted '{os.path.basename(path)}' to '{os.path.basename(output_path)}'")
            except subprocess.CalledProcessError as e:
                print(f"Error converting file: {path}")
                print(f"Stderr: {e.stderr.decode()}")
            except FileNotFoundError:
                print("Error: 'libreoffice' command not found. Please ensure LibreOffice is installed and in your PATH.")
                break # Stop processing if libreoffice is missing
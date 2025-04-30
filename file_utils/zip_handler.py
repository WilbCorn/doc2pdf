"""Handles extraction and processing of zip files."""

import os
import zipfile
import tempfile
from .directory_handler import get_files_from_directory
from .temp_dir_manager import register_temp_dir_for_cleanup

def extract_zip(path, source_name=None):
    """
    Extracts the zip file and returns info about the extracted files.
    
    Args:
        path (str): Path to the zip file.
        source_name (str, optional): The name to use as the source. Defaults to zip filename.
        
    Returns:
        list: A list of dictionaries, each containing 'path', 'source', and 'internal_path'.
    """
    file_infos = []

    if source_name is None:
        source_name = os.path.basename(path)

    try:
        # Create a temporary directory for extraction
        temp_dir = tempfile.mkdtemp()
        register_temp_dir_for_cleanup(temp_dir)
        
        print(f"Extracting zip file '{path}' to '{temp_dir}'...")
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Find supported files within the extracted directory
        extracted_files = get_files_from_directory(temp_dir, source_name=source_name)
        if extracted_files:
            print(f"Found {len(extracted_files)} file(s) in '{source_name}'.")
            file_infos.extend(extracted_files)
        else:
            print(f"No supported files found in '{source_name}'.")
    except zipfile.BadZipFile:
        print(f"Error: '{path}' is not a valid zip file or is corrupted.")
    except Exception as e:
        print(f"An error occurred while processing zip file '{path}': {e}")

    return file_infos
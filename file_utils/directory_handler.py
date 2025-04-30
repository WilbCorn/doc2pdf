"""Handles directory operations like scanning for files and creating output directories."""

import os
import os.path
from settings import CONVERTIBLE_EXTENSIONS, COPY_NON_CONVERTIBLE_FILES

def setup_output_directory(base_dir):
    """
    Creates and returns the path to the output directory.
    
    Args:
        base_dir (str): The base directory to create the output folder in.
        
    Returns:
        str: Path to the output directory.
    """
    output_folder = os.path.join(base_dir, 'output')
    os.makedirs(output_folder, exist_ok=True)
    return output_folder

def get_files_from_directory(input_dir, source_name=None):
    """
    Recursively searches for supported files in the given directory and its subdirectories.
    
    Args:
        input_dir (str): The directory to search in.
        source_name (str, optional): The name to use as the source. Defaults to directory name.
        
    Returns:
        list: A list of dictionaries, each containing 'path', 'source', and 'internal_path'.
    """
    input_file_infos = []
    
    # Default source name is the directory name itself
    if source_name is None:
        source_name = os.path.basename(input_dir)
    
    for root, _, files in os.walk(input_dir):
        # Calculate the relative path from the input_dir
        rel_path = os.path.relpath(root, input_dir) if root != input_dir else ""
        
        for file in files:
            # Filter out temporary and lock files
            if file.startswith('~$') or file.startswith('._'):
                continue
                
            file_ext = os.path.splitext(file)[1].lower()
            
            # Decide which files to include based on settings
            include_file = file_ext in CONVERTIBLE_EXTENSIONS
            
            # Include non-convertible files if configured
            if COPY_NON_CONVERTIBLE_FILES and not include_file:
                # Include all files that aren't system/temp files
                include_file = True
            
            if include_file:
                # Store full file path and source information with internal path
                file_path = os.path.join(root, file)
                internal_path = os.path.join(rel_path, file) if rel_path != "." else file
                input_file_infos.append({
                    'path': file_path, 
                    'source': source_name,
                    'internal_path': internal_path
                })

    return input_file_infos
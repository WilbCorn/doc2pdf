"""Handles temporary directories created during processing."""

import os
import shutil
import atexit

# Keep track of temporary directories created for zip extraction
_temp_dirs_to_clean = []

def register_temp_dir_for_cleanup(temp_dir):
    """
    Registers a temporary directory for cleanup when the program exits.
    
    Args:
        temp_dir (str): Path to the temporary directory.
    """
    _temp_dirs_to_clean.append(temp_dir)

def is_temp_dir(path):
    """
    Checks if a path is a temporary directory we've created.
    
    Args:
        path (str): Path to check.
        
    Returns:
        bool: True if the path is a temporary directory, False otherwise.
    """
    return any(temp_dir in path for temp_dir in _temp_dirs_to_clean)

def cleanup_temp_dirs():
    """Removes all temporary directories created during processing."""
    for temp_dir in _temp_dirs_to_clean:
        if os.path.isdir(temp_dir):
            print(f"Cleaning up temporary directory: {temp_dir}")
            shutil.rmtree(temp_dir)
    _temp_dirs_to_clean.clear()

# Register the cleanup function to be called upon script exit
atexit.register(cleanup_temp_dirs)
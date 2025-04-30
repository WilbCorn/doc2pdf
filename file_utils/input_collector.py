"""Handles the collection of input files from user."""

import os
from .directory_handler import get_files_from_directory
from .zip_handler import extract_zip
from settings import CONVERTIBLE_EXTENSIONS, COPY_NON_CONVERTIBLE_FILES

def get_input_files():
    """
    Prompts the user for input file paths and returns a list of valid files with source info.
    
    Returns:
        list: A list of dictionaries, each containing 'path', 'source', and 'internal_path'.
    """
    input_file_infos = []
    # Initialize counts for user inputs
    counts = {
        'convertible': 0,
        'non_convertible': 0, 
        'zip': 0, 
        'dir': 0, 
        'invalid': 0
    }
    
    print("Enter the paths of document files, zip files, or directories.")
    print("Type 'd' when finished.")
    
    while True:
        path = input("> ")
        if path.lower() == 'd':
            break

        if os.path.isfile(path):
            _process_file(path, input_file_infos, counts)
        elif os.path.isdir(path):
            _process_directory(path, input_file_infos, counts)
        else:
            print(f"Invalid input: '{path}' is not a valid file or directory.")
            counts['invalid'] += 1

    _print_input_summary(counts)
    return input_file_infos

def _process_file(path, input_file_infos, counts):
    """Process a single file input and update counts."""
    file_ext = os.path.splitext(path)[1].lower()
    
    if file_ext in CONVERTIBLE_EXTENSIONS:
        # Convertible file, store with source as "direct"
        input_file_infos.append({'path': path, 'source': 'direct', 'internal_path': ''})
        counts['convertible'] += 1
    elif file_ext == '.zip':
        # Count the zip file itself
        counts['zip'] += 1
        # Extract and add contained files with source as the zip name
        zip_name = os.path.splitext(os.path.basename(path))[0]
        input_file_infos.extend(extract_zip(path, source_name=zip_name))
    elif COPY_NON_CONVERTIBLE_FILES:
        # Non-convertible file, include if copy option is enabled
        input_file_infos.append({'path': path, 'source': 'direct', 'internal_path': ''})
        counts['non_convertible'] += 1
    else:
        print(f"Ignoring non-convertible file: {path}")
        counts['invalid'] += 1

def _process_directory(path, input_file_infos, counts):
    """Process a directory input and update counts."""
    # Count the directory input
    counts['dir'] += 1
    
    # Find supported files within the directory
    dir_name = os.path.basename(path)
    found_in_dir = get_files_from_directory(path, source_name=dir_name)
    
    if not found_in_dir:
        # Only print message if not a temp dir we created
        from .temp_dir_manager import is_temp_dir
        if not is_temp_dir(path):
            print(f"No files found in directory: {path}")
    
    for file_info in found_in_dir:
        input_file_infos.append(file_info)
        ext = os.path.splitext(file_info['path'])[1].lower()
        if ext in CONVERTIBLE_EXTENSIONS:
            counts['convertible'] += 1
        else:
            counts['non_convertible'] += 1

def _print_input_summary(counts):
    """Print a summary of the input files."""
    print("\n--- Input Summary ---")
    print(f"Convertible files: {counts['convertible']}")
    if COPY_NON_CONVERTIBLE_FILES:
        print(f"Other files:       {counts['non_convertible']}")
    print(f"ZIP files:         {counts['zip']}")
    print(f"Directories:       {counts['dir']}")
    print(f"Invalid/ignored:   {counts['invalid']}")
    print("---------------------\n")
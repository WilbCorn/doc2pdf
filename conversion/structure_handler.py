"""Handles conversion while preserving source structure."""

import os
from settings import COPY_NON_CONVERTIBLE_FILES

def convert_with_structure(files_to_convert, base_output_folder, converter_factory):
    """
    Convert files while preserving their source and internal structure.
    
    Args:
        files_to_convert (list): List of file info dictionaries.
        base_output_folder (str): Base directory for output files.
        converter_factory (function): Factory function that returns a converter instance.
        
    Returns:
        int: Total number of files successfully processed.
    """
    # Process files based on their source
    by_source = {}
    for file_info in files_to_convert:
        source = file_info['source']
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(file_info)
    
    total_processed = 0
    action = "Processing" if COPY_NON_CONVERTIBLE_FILES else "Converting"
    
    # Convert files, organizing by source
    for source, files in by_source.items():
        if source == 'direct':
            # Direct files go to the base output folder
            print(f"\n{action} {len(files)} directly specified file(s)...")
            converter = converter_factory(base_output_folder)
            paths = [f['path'] for f in files]
            total_processed += converter.process(paths)
        else:
            # Process files from zip archives or directories
            print(f"\n{action} {len(files)} file(s) from source: {source}")
            
            # Create subfolder for this source
            source_folder = os.path.join(base_output_folder, source)
            os.makedirs(source_folder, exist_ok=True)
            
            # Group files by directory to minimize converter instantiations
            by_dir = {}
            for file_info in files:
                internal_dir = os.path.dirname(file_info['internal_path'])
                output_dir = os.path.join(source_folder, internal_dir) if internal_dir else source_folder
                if output_dir not in by_dir:
                    by_dir[output_dir] = []
                by_dir[output_dir].append(file_info)
            
            # Process each directory
            for output_dir, dir_files in by_dir.items():
                os.makedirs(output_dir, exist_ok=True)
                converter = converter_factory(output_dir)
                paths = [f['path'] for f in dir_files]
                processed = converter.process(paths)
                total_processed += processed
    
    return total_processed
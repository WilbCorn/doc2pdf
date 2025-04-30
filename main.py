#!/usr/bin/env python3
"""
Document to PDF Converter
========================
A utility for converting documents to PDF files,
supporting direct file input, directory scanning, and zip archives.
Can also copy non-convertible files to maintain directory structure.
Features multithreaded processing for faster conversion.
"""

import os
import sys
from converters import get_converter
from file_utils import get_input_files, setup_output_directory
from conversion import convert_with_structure
from settings import COPY_NON_CONVERTIBLE_FILES, USE_MULTITHREADING, MAX_WORKERS
from utils.thread_manager import get_max_workers


def main():
    """Main entry point for the application."""
    # Create base output folder in the current directory
    current_dir = os.getcwd()
    base_output_folder = setup_output_directory(current_dir)

    # Get list of files to process (and print input counts)
    files_to_convert = get_input_files()

    # If no files found, exit
    if not files_to_convert:
        print("\nNo files found or selected for processing.")
        return

    mode = "converting/copying" if COPY_NON_CONVERTIBLE_FILES else "converting"
    thread_info = f" using {get_max_workers()} threads" if USE_MULTITHREADING else " (single-threaded)"
    print(f"Found {len(files_to_convert)} total file(s) for {mode}{thread_info}.")

    # Get the converter to use (default to LibreOffice)
    converter_name = os.environ.get('DOCUMENT_CONVERTER', 'libreoffice')
    converter_factory = get_converter(converter_name)
    
    # Convert files while preserving structure
    total_processed = convert_with_structure(files_to_convert, base_output_folder, converter_factory)
    
    print(f"\nProcessing finished. {total_processed} file(s) processed.")


if __name__ == "__main__":
    main()

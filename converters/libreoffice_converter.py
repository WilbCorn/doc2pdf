"""LibreOffice implementation of document converter."""

import os
import subprocess
import shutil
import concurrent.futures
from .base_converter import DocumentConverter
from settings import (
    COPY_NON_CONVERTIBLE_FILES, 
    CONVERTIBLE_EXTENSIONS, 
    ADDITIONAL_COPY_EXTENSIONS,
    USE_MULTITHREADING
)
from utils.thread_manager import process_files_in_parallel

class LibreOfficeConverter(DocumentConverter):
    """Convert documents to PDF using LibreOffice."""
    
    def process(self, file_paths):
        """
        Convert documents to PDF using LibreOffice.
        
        Args:
            file_paths (list): List of file paths to convert.
            
        Returns:
            int: Number of files successfully converted.
        """
        if not file_paths:
            return 0
            
        total_files = len(file_paths)
        successful_conversions = 0
        
        # Check if libreoffice is installed before proceeding
        try:
            subprocess.run(['libreoffice', '--version'], 
                          check=True, capture_output=True, text=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Error: 'libreoffice' command not found or failed. Please ensure LibreOffice is installed.")
            # If configured, copy the files instead
            if COPY_NON_CONVERTIBLE_FILES:
                print("Falling back to copying files...")
                return self._copy_files_batch(file_paths)
            return 0
            
        # Use multithreading if enabled, otherwise use sequential processing
        if USE_MULTITHREADING and total_files > 1:
            successful_conversions = self._process_files_parallel(file_paths)
        else:
            successful_conversions = self._process_files_sequential(file_paths)
            
        return successful_conversions
    
    def _process_files_parallel(self, file_paths):
        """Process files in parallel using multiple threads."""
        successful = 0
        
        # Filter files into convertible and non-convertible
        convertible_files = []
        non_convertible_files = []
        
        for path in file_paths:
            if not os.path.exists(path):
                continue
                
            file_ext = os.path.splitext(path)[1].lower()
            if file_ext in CONVERTIBLE_EXTENSIONS:
                convertible_files.append(path)
            elif COPY_NON_CONVERTIBLE_FILES and self._should_copy_file(file_ext):
                non_convertible_files.append(path)
        
        # Process convertible files in parallel
        if convertible_files:
            results = process_files_in_parallel(
                convertible_files, 
                self._convert_single_file
            )
            
            successful += sum(1 for result in results.values() if result)
        
        # Copy non-convertible files in parallel if needed
        if non_convertible_files and COPY_NON_CONVERTIBLE_FILES:
            results = process_files_in_parallel(
                non_convertible_files,
                self._copy_single_file
            )
            
            successful += sum(1 for result in results.values() if result)
            
        return successful
    
    def _process_files_sequential(self, file_paths):
        """Process files sequentially (original method)."""
        successful = 0
        
        for idx, path in enumerate(file_paths, 1):
            # Check if the path still exists
            if not os.path.exists(path):
                print(f"Skipping missing file: {path}")
                continue
                
            file_name = os.path.basename(path)
            file_ext = os.path.splitext(file_name)[1].lower()
            
            # Check if this is a convertible file or one to just copy
            if file_ext in CONVERTIBLE_EXTENSIONS:
                print(f"({idx}/{len(file_paths)}) Converting '{file_name}'...")
                
                if self._convert_single_file(path):
                    successful += 1
                    
            elif COPY_NON_CONVERTIBLE_FILES and self._should_copy_file(file_ext):
                # This is a non-convertible file, copy it if configured to do so
                if self._copy_single_file(path):
                    successful += 1
                
        return successful
    
    def _convert_single_file(self, path):
        """
        Convert a single file to PDF.
        
        Args:
            path (str): Path to the file to convert.
            
        Returns:
            bool: True if conversion was successful, False otherwise.
        """
        file_name = os.path.basename(path)
        
        try:
            # Ensure output directory exists
            os.makedirs(self.output_folder, exist_ok=True)
            
            # Run LibreOffice in headless mode to convert the file
            result = subprocess.run(
                ['libreoffice', '--headless', '--convert-to', 'pdf', 
                 '--outdir', self.output_folder, path],
                check=True, capture_output=True, text=True
            )
            
            output_file = os.path.splitext(file_name)[0] + ".pdf"
            print(f"Successfully converted to '{output_file}'")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Error converting file: {file_name}")
            if e.stderr:
                print(f"Error details: {e.stderr.strip()}")
            
            # If configured, copy files that failed to convert
            if COPY_NON_CONVERTIBLE_FILES:
                return self._copy_single_file(path, "failed conversion")
            return False
            
        except Exception as e:
            print(f"Unexpected error converting {file_name}: {str(e)}")
            return False
    
    def _copy_single_file(self, path, reason="non-convertible"):
        """
        Copy a single file to the output directory.
        
        Args:
            path (str): Path to the file to copy.
            reason (str, optional): Reason for copying. Defaults to "non-convertible".
            
        Returns:
            bool: True if copy was successful, False otherwise.
        """
        file_name = os.path.basename(path)
        
        try:
            # Ensure output directory exists
            os.makedirs(self.output_folder, exist_ok=True)
            
            dest_path = os.path.join(self.output_folder, file_name)
            shutil.copy2(path, dest_path)
            print(f"Copied {reason} file '{file_name}' to output directory")
            return True
        except Exception as e:
            print(f"Error copying file '{file_name}': {e}")
            return False
    
    def _copy_files_batch(self, file_paths):
        """
        Copy multiple files to the output directory.
        
        Args:
            file_paths (list): List of file paths to copy.
            
        Returns:
            int: Number of files successfully copied.
        """
        if not COPY_NON_CONVERTIBLE_FILES:
            return 0
            
        successful = 0
        print("\nCopying files to output directory...")
        
        if USE_MULTITHREADING and len(file_paths) > 1:
            results = process_files_in_parallel(
                file_paths,
                self._copy_single_file
            )
            
            successful = sum(1 for result in results.values() if result)
        else:
            for path in file_paths:
                if os.path.exists(path):
                    file_ext = os.path.splitext(path)[1].lower()
                    
                    if self._should_copy_file(file_ext):
                        if self._copy_single_file(path):
                            successful += 1
                            
        return successful
    
    def _should_copy_file(self, file_ext):
        """Determine if a file with the given extension should be copied."""
        # If ADDITIONAL_COPY_EXTENSIONS is empty, copy all non-convertible files
        # Otherwise, only copy files with extensions in the list
        return not ADDITIONAL_COPY_EXTENSIONS or file_ext.lower() in ADDITIONAL_COPY_EXTENSIONS
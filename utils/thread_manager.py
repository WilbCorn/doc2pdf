"""Provides threading utilities for parallel file processing."""

import os
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
from settings import MAX_WORKERS

def get_max_workers():
    """Determine the number of worker processes to use."""
    # For LibreOffice conversions, it's safer to use fewer processes
    if MAX_WORKERS <= 0:
        return os.cpu_count() or 4
    else:
        return MAX_WORKERS

def process_files_in_parallel(file_list, process_function, max_workers=None):
    """
    Process a list of files in parallel using threads.
    
    Args:
        file_list (list): List of files to process.
        process_function (function): The function to call for each file.
        max_workers (int, optional): Maximum number of worker threads.
            If None, uses the value from get_max_workers().
            
    Returns:
        dict: Results of processing, with file paths as keys.
    """
    if max_workers is None:
        max_workers = get_max_workers()
        
    results = {}
    total_files = len(file_list)
    
    print(f"Starting parallel processing with {max_workers} worker threads.")
    
    # Use a context manager to ensure threads are cleaned up
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks and create a future->path mapping
        future_to_path = {
            executor.submit(process_function, path): path
            for path in file_list
        }
        
        # Process results as they complete
        for i, future in enumerate(as_completed(future_to_path), 1):
            path = future_to_path[future]
            try:
                result = future.result()
                results[path] = result
                print(f"({i}/{total_files}) Processed: {os.path.basename(path)}")
            except Exception as exc:
                print(f"({i}/{total_files}) Error processing {os.path.basename(path)}: {exc}")
                results[path] = False
    
    return results
#!/usr/bin/env python3
"""Utility to check threading configuration."""

import os
from settings import USE_MULTITHREADING, MAX_WORKERS
from utils.thread_manager import get_max_workers

def check_threading_config():
    """Display information about the threading configuration."""
    print("\n--- Threading Configuration ---")
    print(f"Multithreading enabled: {USE_MULTITHREADING}")
    print(f"MAX_WORKERS setting:    {MAX_WORKERS}")
    print(f"CPU cores available:    {os.cpu_count()}")
    print(f"Actual worker threads:  {get_max_workers()}")
    print("-----------------------------\n")

if __name__ == "__main__":
    check_threading_config()
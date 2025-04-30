"""Utility functions and helpers for the application."""

from .thread_manager import process_files_in_parallel, get_max_workers

__all__ = ['process_files_in_parallel', 'get_max_workers']
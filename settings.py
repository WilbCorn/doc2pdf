"""
Application settings and configuration options.
"""

# Whether to copy non-convertible files to the output directory
COPY_NON_CONVERTIBLE_FILES = True

# Supported file types that can be converted
CONVERTIBLE_EXTENSIONS = ('.ppt', '.pptx') 
# '.doc', '.docx', '.xls', '.xlsx' works as well, but may have some formatting issues.

# Additional file types to copy (when COPY_NON_CONVERTIBLE_FILES is True)
# Leave empty to copy all non-convertible files, or specify extensions to limit
# Example: ['.txt', '.jpg', '.png']
ADDITIONAL_COPY_EXTENSIONS = []

# Whether to use multithreaded processing (can cause issues with LibreOffice)
USE_MULTITHREADING = True  # Set to False for more reliable operation

# Maximum number of worker threads/processes
# For LibreOffice conversions, a lower number is more reliable
MAX_WORKERS = 15  # Use just 1 process for most reliable operation

# Files to exclude from processing (temporary/lock files)
EXCLUDED_FILE_PATTERNS = ['~$', '._', '.tmp']
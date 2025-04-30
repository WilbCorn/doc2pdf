# Document to PDF Converter

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Powerful Python scripts for converting document files to PDF, with support for direct file input, directory scanning, and zip archive extraction. This tool is designed to maintain directory structures while converting documents, with options to include non-convertible files in the output.

## Features
- Convert PowerPoint presentations (.ppt, .pptx) to PDF format
- Support for additional document types (.doc, .docx, .xls, .xlsx) with some formatting  
limitations (Due to Ms to Libre)
- Process multiple files from different sources:
    - Individual files
    - Directory trees (with subdirectories)
    - ZIP archives
- Preserve directory structures in the output
- Copy non-convertible files to maintain complete directory structure (optional)
- Multithreaded processing for faster conversion of large batches
- Flexible configuration through easy-to-edit settings

## Requirements
- Python 3.6 or higher
- LibreOffice (must be installed and accessible in your system PATH)

## Installation
1. Clone this repository:
```
git clone https://github.com/WilbCorn/document-to-pdf-converter.git
cd document-to-pdf-converter
```
2. Ensure LibreOffice is installed on your system:
- For Ubuntu/Debian: `sudo apt-get install libreoffice`
- For Fedora/RHEL: `sudo dnf install libreoffice`
- macOS and Windows: **Not Supported**.

## Usage
Run the script using Python:
```
python main.py
```

The interactive prompt will guide you through the process:
1. Enter the paths to files, directories, or ZIP archives you want to process
2. Type d when finished entering paths
3. The program will show a summary of files found
4. Files will be processed and converted to PDF
5. Output will be saved in the output directory

## Configuration
You can customize the behavior by editing the settings.py file:

|Setting	Description
|COPY_NON_CONVERTIBLE_FILES	Whether to copy non-convertible files to the output (True/False)
CONVERTIBLE_EXTENSIONS	File types that will be converted to PDF
ADDITIONAL_COPY_EXTENSIONS	Specific file types to copy when COPY_NON_CONVERTIBLE_FILES is True
USE_MULTITHREADING	Enable/disable multithreaded processing
MAX_WORKERS	Maximum number of worker threads (set to 0 for auto-detection)
EXCLUDED_FILE_PATTERNS	File patterns to exclude from processing

## Output Structure
The output directory follows the same structure as the input:

- Files provided directly are saved to the root of the output folder
- Files from directories maintain their relative paths
- Files from ZIP archives are placed in subfolders named after the archives

Example:
```
output/
├── presentation.pdf                  # From direct file input
├── documents_folder/
│   ├── report.pdf                    # From directory input
│   └── meeting/
│       └── agenda.pdf                # From subdirectory
└── archive/                          # From ZIP file
    ├── slides.pdf                    # From root of ZIP
    └── resources/
        └── diagram.pdf               # From subfolder in ZIP
```

## Troubleshooting
Common Issues
- **LibreOffice not found**: Ensure LibreOffice is installed and in your PATH
- **Corrupt PDF files**: Try disabling multithreading by setting USE_MULTITHREADING = False in settings.py
- **Memory issues with large files**: Lower the MAX_WORKERS value in settings.py
- **Conversion fails for some files**: Some complex document formatting may not convert perfectly

## Checking Thread Configuration
Run the included utility script to check your thread configuration:
```
python check_threads.py
```

## Architecture

The application follows a modular design with clear separation of concerns:

- **converters/**: Implements the Strategy pattern for document conversion
- **file_utils/**: Handles file operations, directory scanning, and ZIP extraction
- **conversion/**: Manages the conversion process while preserving structure
- **utils/**: Contains utility functions for threading and other operations
- **settings.py**: Centralizes configuration options

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add some new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

Copyright 2024 WilbCorn

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Acknowledgments

- LibreOffice for providing the core conversion functionality
- All contributors who help improve this tool

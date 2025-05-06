# Document to PDF Converter

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A powerful tool for converting document files to PDF in **Linux**, with support for direct file input, directory scanning, and ZIP archive extraction. Designed to preserve directory structures and include non-convertible files in the output.

## Features

- Convert PowerPoint presentations (`.ppt`, `.pptx`) to PDF format
- Support for additional document types (`.doc`, `.docx`, `.xls`, `.xlsx`) with some formatting limitations
- Process multiple files from:
  - Individual files
  - Directory trees (with subdirectories)
  - ZIP archives
- Preserve directory structure in the output
- Copy non-convertible files to maintain complete directory structure (optional)
- Multithreaded processing for faster conversion of large batches (optional)
- Flexible configuration through easy-to-edit settings

## Requirements

- Python 3.6 or higher
- LibreOffice (must be installed and accessible in your system PATH)

## Installation

### Project (Includes CLI-based and GUI-based)

1. Clone this repository:
   ```bash
   git clone https://github.com/WilbCorn/document-to-pdf-converter.git
   cd document-to-pdf-converter
   ```

2. Install LibreOffice:
   - **Ubuntu/Debian**: `sudo apt-get install libreoffice`
   - **Fedora/RHEL**: `sudo dnf install libreoffice`
   - **macOS/Windows**: Not supported directly — use the Docker version instead

3. Run the script:
   ```bash
   python main.py
   ```

> The interactive prompt will guide you:
> 1. Enter paths to files, directories, or ZIP archives
> 2. Type `d` when finished entering paths
> 3. Program shows a summary of files found
> 4. Files are converted to PDF
> 5. Output is saved in the output directory

---

### Streamlit Web App (GUI)

1. **Install dependencies**  
   Ensure Python 3.6+ and LibreOffice are installed, then:
   ```bash
   pip install -r gui_requirements.txt
   ```

2. **Start the app**
   ```bash
   streamlit run gui_main.py --server.port=8501 --server.address=0.0.0.0
   ```
   Open [http://localhost:8501](http://localhost:8501) in your browser.

3. Drag and drop files or zipped folders, and download the converted PDFs as a single ZIP file.

---

### Docker (GUI-based only)

You can use this tool without installing Python or LibreOffice by running it in Docker.

#### Build the Docker image

```bash
docker build -t doc2pdf .
```

#### Run the container

```bash
docker run -it -p 8501:8501 --name doc2pdf1 doc2pdf
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

#### Using the Web GUI

1. Drag and drop your files or zipped folders
2. Wait for processing to finish
3. Download the converted PDFs as a ZIP

> ⚠️ All files are deleted when the container stops.

---

## Configuration

Edit `settings.py` to customize behavior:

| Setting | Description |
|--------|-------------|
| `COPY_NON_CONVERTIBLE_FILES` | Whether to copy non-convertible files to the output (`True`/`False`) |
| `CONVERTIBLE_EXTENSIONS` | File types that will be converted to PDF |
| `ADDITIONAL_COPY_EXTENSIONS` | Specific file types to copy if `COPY_NON_CONVERTIBLE_FILES` is `True` |
| `USE_MULTITHREADING` | Enable/disable multithreaded processing |
| `MAX_WORKERS` | Maximum number of worker threads (`0` = auto-detect) |
| `EXCLUDED_FILE_PATTERNS` | File patterns to exclude from processing |

---

## Output Structure

The output maintains the same structure as the input:

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

---

## Troubleshooting

| Issue | Solution |
|------|----------|
| **LibreOffice not found** | Ensure LibreOffice is installed and in your PATH |
| **Corrupt PDF files** | Try disabling multithreading (`USE_MULTITHREADING = False`) |
| **Memory issues with large files** | Lower `MAX_WORKERS` |
| **Conversion fails for some files** | Complex formatting may not convert perfectly |

Run utility script to check thread configuration:

```bash
python check_threads.py
```

---

## Architecture

Modular design with clear separation of concerns:

- **converters/**: Implements Strategy pattern for document conversion
- **file_utils/**: Handles file operations, directory scanning, and ZIP extraction
- **conversion/**: Manages the conversion process while preserving structure
- **utils/**: Contains utility functions for threading and other operations
- **settings.py**: Centralizes configuration options

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -m 'Add some new feature'`
4. Push: `git push origin feature/new-feature`
5. Submit a Pull Request

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).

---

## Acknowledgments

- LibreOffice for providing core conversion functionality
- All contributors who help improve this tool
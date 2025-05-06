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
import tempfile
import shutil
import streamlit as st
import zipfile
from io import BytesIO
from converters import get_converter
from file_utils import setup_output_directory
from conversion import convert_with_structure
from settings import COPY_NON_CONVERTIBLE_FILES, USE_MULTITHREADING
from utils.thread_manager import get_max_workers

st.set_page_config(page_title="Document to PDF Converter", layout="centered")
st.title("📄 Document to PDF Converter")

st.write("Drag and drop your files, folders (as zip), or select them below. Converted PDFs will be available for download.")

uploaded_files = st.file_uploader(
    "Drop files or ZIP folders here",
    type=["ppt", "pptx", "zip", "doc", "docx", "xls", "xlsx"],
    accept_multiple_files=True
)

if uploaded_files:
    with st.spinner("Processing files..."):
        # Create a temp input directory
        temp_input_dir = tempfile.mkdtemp()
        temp_output_dir = tempfile.mkdtemp()
        try:
            input_paths = []
            for uploaded in uploaded_files:
                file_path = os.path.join(temp_input_dir, uploaded.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded.getbuffer())
                input_paths.append(file_path)

            # Prepare output directory
            base_output_folder = setup_output_directory(temp_output_dir)

            # Collect files to convert (simulate get_input_files)
            from file_utils.input_collector import _process_file, _process_directory
            files_to_convert = []
            counts = {'convertible': 0, 'non_convertible': 0, 'zip': 0, 'dir': 0, 'invalid': 0}
            for path in input_paths:
                if os.path.isfile(path):
                    _process_file(path, files_to_convert, counts)
                elif os.path.isdir(path):
                    _process_directory(path, files_to_convert, counts)

            if not files_to_convert:
                st.error("No convertible files found.")
            else:
                mode = "converting/copying" if COPY_NON_CONVERTIBLE_FILES else "converting"
                thread_info = f" using {get_max_workers()} threads" if USE_MULTITHREADING else " (single-threaded)"
                st.info(f"Found {len(files_to_convert)} file(s) for {mode}{thread_info}.")

                converter_name = os.environ.get('DOCUMENT_CONVERTER', 'libreoffice')
                converter_factory = get_converter(converter_name)
                total_processed = convert_with_structure(files_to_convert, base_output_folder, converter_factory)

                st.success(f"Processing finished. {total_processed} file(s) processed.")

                # Zip the output directory
                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
                    for root, _, files in os.walk(base_output_folder):
                        for file in files:
                            out_path = os.path.join(root, file)
                            rel_path = os.path.relpath(out_path, base_output_folder)
                            zipf.write(out_path, arcname=rel_path)
                zip_buffer.seek(0)

                st.download_button(
                    label="Download All as ZIP",
                    data=zip_buffer,
                    file_name="converted_output.zip",
                    mime="application/zip"
                )
        finally:
            shutil.rmtree(temp_input_dir)
            shutil.rmtree(temp_output_dir)
else:
    st.info("Please upload files or zip folders to begin.")

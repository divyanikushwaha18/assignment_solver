import os
import zipfile

def extract_zip(zip_path, extract_to):
    """Extract a ZIP file to a directory"""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    return extract_to
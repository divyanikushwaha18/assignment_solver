import os
import zipfile
import tempfile
import pandas as pd
import json
from .base_processor import BaseProcessor

class FileProcessor(BaseProcessor):
    """
    Handles file processing operations for various file types.
    """
    
    def process(self, question, file=None):
        """
        Main method to process file-based questions.
        
        Args:
            question (str): The question text
            file: The uploaded file
            
        Returns:
            dict: Response with answer key
        """
        if not file:
            return {"answer": "No file provided"}
        
        # Create temp directory for file extraction
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded file
            file_path = os.path.join(temp_dir, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
            # Extract file info
            file_info = self.extract_file_info(file_path)
            
            # Process based on question
            # For simple cases, you can handle directly based on question patterns
            if "answer column" in question.lower() and file_info.get('type') == 'csv':
                if file_info.get('data') is not None and 'answer' in file_info['data'].columns:
                    return {"answer": str(file_info['data']['answer'].iloc[0])}
            
            # For more complex cases, we'll let the RequestHandler handle it
            return {"answer": f"Extracted file info, but need further processing for: {question}"}
    
    def extract_file_info(self, file_path):
        """
        Extract information from different file types.
        
        Args:
            file_path: Path to the file
            
        Returns:
            dict: Information about the file and its content
        """
        file_info = {
            'path': file_path,
            'name': os.path.basename(file_path),
            'type': None,
            'content': None,
            'data': None,
        }
        
        # Handle ZIP files
        if file_path.endswith('.zip'):
            file_info['type'] = 'zip'
            extract_dir = os.path.join(os.path.dirname(file_path), 'extracted')
            os.makedirs(extract_dir, exist_ok=True)
            
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # List all extracted files
            extracted_files = os.listdir(extract_dir)
            file_info['extracted_files'] = extracted_files
            
            # Process each extracted file
            extracted_content = {}
            for extracted_file in extracted_files:
                extracted_path = os.path.join(extract_dir, extracted_file)
                extracted_info = self.extract_file_info(extracted_path)
                extracted_content[extracted_file] = extracted_info
            
            file_info['content'] = str(extracted_content)
            
        # Handle CSV files
        elif file_path.endswith('.csv'):
            file_info['type'] = 'csv'
            try:
                df = pd.read_csv(file_path)
                file_info['data'] = df
                file_info['content'] = df.head(20).to_string()  # First 20 rows as string
                file_info['columns'] = list(df.columns)
            except Exception as e:
                file_info['error'] = str(e)
        
        # Handle JSON files
        elif file_path.endswith('.json'):
            file_info['type'] = 'json'
            try:
                with open(file_path, 'r') as f:
                    json_data = json.load(f)
                file_info['data'] = json_data
                file_info['content'] = json.dumps(json_data, indent=2)[:2000]  # First 2000 chars
            except Exception as e:
                file_info['error'] = str(e)
        
        # Handle text files
        elif file_path.endswith('.txt') or file_path.endswith('.log'):
            file_info['type'] = 'text'
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                file_info['content'] = content[:5000]  # First 5000 chars
            except Exception as e:
                file_info['error'] = str(e)
        
        # For other file types, just record basic info
        else:
            file_info['type'] = 'unknown'
            file_info['content'] = f"File type not supported: {file_path}"
        
        return file_info
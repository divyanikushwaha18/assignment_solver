import os
import zipfile
import tempfile
import pandas as pd
import json
import sqlite3
import re
import csv
import hashlib
import chardet
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
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
            
            # Process based on question type
            
            # ZIP extraction (Q8)
            if "unzip" in question.lower() and "answer column" in question.lower() and file_info.get('type') == 'zip':
                for name, extracted in file_info.get('extracted_content', {}).items():
                    if name.endswith('.csv') and extracted.get('type') == 'csv':
                        if 'answer' in extracted.get('columns', []):
                            df = extracted.get('data')
                            if df is not None and not df.empty:
                                return {"answer": str(df['answer'].iloc[0])}
            
            # Simple CSV question
            elif "answer column" in question.lower() and file_info.get('type') == 'csv':
                if file_info.get('data') is not None and 'answer' in file_info['data'].columns:
                    return {"answer": str(file_info['data']['answer'].iloc[0])}
            
            # Markdown formatting (Q3)
            elif "prettier" in question.lower() and "sha256sum" in question.lower() and file_info.get('type') == 'markdown':
                # Process markdown with prettier (simulate the output)
                content = file_info.get('content', '')
                # Apply basic prettier formatting rules
                formatted = self._format_markdown(content)
                # Calculate SHA256 hash
                hash_result = hashlib.sha256(formatted.encode('utf-8')).hexdigest()
                return {"answer": hash_result}
            
            # File comparison (Q17)
            elif "how many lines are different" in question.lower() and file_info.get('type') == 'zip':
                a_content = None
                b_content = None
                
                for name, extracted in file_info.get('extracted_content', {}).items():
                    if name == 'a.txt':
                        a_content = extracted.get('content')
                    elif name == 'b.txt':
                        b_content = extracted.get('content')
                
                if a_content and b_content:
                    a_lines = a_content.splitlines()
                    b_lines = b_content.splitlines()
                    
                    # Count different lines
                    if len(a_lines) == len(b_lines):
                        diff_count = sum(1 for a, b in zip(a_lines, b_lines) if a != b)
                        return {"answer": str(diff_count)}
            
            # File encoding processing (Q12)
            elif "different encodings" in question.lower() and "sum" in question.lower() and file_info.get('type') == 'zip':
                total_sum = 0
                special_symbols = ['›', 'œ', '—']
                
                for name, extracted in file_info.get('extracted_content', {}).items():
                    if extracted.get('type') in ['csv', 'text']:
                        df = extracted.get('data')
                        if df is not None and 'symbol' in df.columns and 'value' in df.columns:
                            # Sum values for matching symbols
                            for symbol in special_symbols:
                                matches = df[df['symbol'] == symbol]
                                total_sum += matches['value'].sum()
                
                return {"answer": str(int(total_sum))}
            
            # CSS Selector (Q11)
            elif "div" in question.lower() and "foo class" in question.lower() and "data-value" in question.lower():
                if file_info.get('type') in ['text', 'html']:
                    content = file_info.get('content', '')
                    soup = BeautifulSoup(content, 'html.parser')
                    # Find all divs with foo class
                    divs = soup.select('div.foo')
                    # Sum data-value attributes
                    total = sum(int(div.get('data-value', 0)) for div in divs)
                    return {"answer": str(total)}
            
            # DevTools usage (Q6)
            elif "hidden input" in question.lower() and "secret value" in question.lower():
                if file_info.get('type') in ['text', 'html']:
                    content = file_info.get('content', '')
                    soup = BeautifulSoup(content, 'html.parser')
                    # Find hidden input
                    hidden_input = soup.find('input', {'type': 'hidden'})
                    if hidden_input:
                        return {"answer": hidden_input.get('value', '')}
            
            # SQL Query (Q18)
            elif "sql" in question.lower() and "gold" in question.lower() and "ticket" in question.lower():
                if file_info.get('type') == 'sqlite':
                    db_path = file_info.get('path')
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    
                    # Execute SQL to find total sales for Gold tickets
                    query = """
                    SELECT SUM(units * price) 
                    FROM tickets 
                    WHERE UPPER(TRIM(type)) = 'GOLD'
                    """
                    cursor.execute(query)
                    result = cursor.fetchone()[0]
                    conn.close()
                    
                    return {"answer": str(result)}
            
            # File replacement (Q14)
            elif "replace" in question.lower() and "iitm" in question.lower() and "sha256sum" in question.lower():
                if file_info.get('type') == 'zip':
                    # Process files and replace IITM with IIT Madras
                    content_hash = self._process_file_replacement(file_info)
                    return {"answer": content_hash}
            
            # For more complex cases or unhandled questions
            return {"answer": f"Extracted file information from {file.name}"}
    
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
            
            file_info['extracted_content'] = extracted_content
            file_info['content'] = str(extracted_content)
            
        # Handle CSV files
        elif file_path.endswith('.csv'):
            file_info['type'] = 'csv'
            try:
                # Try to detect encoding
                rawdata = open(file_path, 'rb').read(1024)
                detected = chardet.detect(rawdata)
                encoding = detected['encoding'] or 'utf-8'
                
                # Read with detected encoding
                df = pd.read_csv(file_path, encoding=encoding)
                file_info['data'] = df
                file_info['content'] = df.head(20).to_string()  # First 20 rows as string
                file_info['columns'] = list(df.columns)
            except Exception as e:
                # Try alternative encodings if default fails
                try:
                    df = pd.read_csv(file_path, encoding='cp1252')
                    file_info['data'] = df
                    file_info['content'] = df.head(20).to_string()
                    file_info['columns'] = list(df.columns)
                except Exception as inner_e:
                    file_info['error'] = f"{str(e)}; {str(inner_e)}"
        
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
        
        # Handle text files and HTML
        elif file_path.endswith(('.txt', '.log', '.html', '.htm')):
            if file_path.endswith(('.html', '.htm')):
                file_info['type'] = 'html'
            else:
                file_info['type'] = 'text'
                
            try:
                # Try to detect encoding
                rawdata = open(file_path, 'rb').read(4096)
                detected = chardet.detect(rawdata)
                encoding = detected['encoding'] or 'utf-8'
                
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                file_info['content'] = content[:10000]  # First 10000 chars
                file_info['data'] = content
            except Exception as e:
                # Try alternative encodings
                encodings = ['utf-8', 'cp1252', 'latin1', 'utf-16']
                for enc in encodings:
                    try:
                        with open(file_path, 'r', encoding=enc) as f:
                            content = f.read()
                        file_info['content'] = content[:10000]
                        file_info['data'] = content
                        file_info['encoding'] = enc
                        break
                    except:
                        continue
                else:
                    file_info['error'] = str(e)
        
        # Handle Markdown files
        elif file_path.endswith(('.md', '.markdown')):
            file_info['type'] = 'markdown'
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                file_info['content'] = content
                file_info['data'] = content
            except Exception as e:
                file_info['error'] = str(e)
        
        # Handle SQLite database files
        elif file_path.endswith(('.db', '.sqlite', '.sqlite3')):
            file_info['type'] = 'sqlite'
            try:
                conn = sqlite3.connect(file_path)
                cursor = conn.cursor()
                
                # Get list of tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                table_data = {}
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = [col[1] for col in cursor.fetchall()]
                    
                    # Sample data (first 5 rows)
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                    rows = cursor.fetchall()
                    
                    table_data[table_name] = {
                        'columns': columns,
                        'sample': rows
                    }
                
                conn.close()
                file_info['data'] = table_data
                file_info['content'] = str(table_data)
            except Exception as e:
                file_info['error'] = str(e)
        
        # For other file types, just record basic info
        else:
            file_info['type'] = 'unknown'
            file_info['content'] = f"File type not supported: {file_path}"
        
        return file_info
    
    def _format_markdown(self, content):
        """Simple markdown formatter to simulate prettier"""
        lines = content.splitlines()
        formatted = []
        
        for line in lines:
            # Heading formatting
            if re.match(r'^#+\s+', line):
                heading = re.match(r'^(#+)\s+(.+)', line)
                if heading:
                    formatted.append(f"{heading.group(1)} {heading.group(2).strip()}")
                    continue
            
            # List item formatting
            if re.match(r'^\s*[\*\-]\s+', line):
                indent = len(re.match(r'^\s*', line).group(0))
                list_match = re.match(r'^\s*([\*\-])\s+(.+)', line)
                if list_match:
                    formatted.append(f"{' ' * indent}{list_match.group(1)} {list_match.group(2).strip()}")
                    continue
            
            # Blockquote formatting
            if re.match(r'^\s*>\s*', line):
                quote_match = re.match(r'^\s*>\s*(.+)', line)
                if quote_match:
                    formatted.append(f"> {quote_match.group(1).strip()}")
                    continue
            
            # Regular text (collapse multiple spaces)
            formatted.append(re.sub(r'\s+', ' ', line).strip())
        
        return '\n'.join(formatted)
    
    def _process_file_replacement(self, file_info):
        """Process files for IITM replacement and calculate hash"""
        result = []
        
        for name, file_data in file_info.get('extracted_content', {}).items():
            if file_data.get('type') in ['text', 'markdown']:
                content = file_data.get('content', '')
                # Replace IITM with IIT Madras (case insensitive)
                replaced = re.sub(r'(?i)IITM', 'IIT Madras', content)
                result.append(replaced)
        
        # Simulate cat * | sha256sum
        combined = '\n'.join(result)
        hash_result = hashlib.sha256(combined.encode('utf-8')).hexdigest()
        
        return hash_result
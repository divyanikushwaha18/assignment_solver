import os
import tempfile
import openai
from django.conf import settings
# To this:
from ..services.processors.file_processor import FileProcessor

class RequestHandler:
    """
    Handles incoming requests by processing questions and files.
    """
    def __init__(self):
        self.file_processor = FileProcessor()
        # Set up OpenAI API key
        openai.api_key = getattr(settings, 'OPENAI_API_KEY', os.environ.get("OPENAI_API_KEY", ""))
        
    def process_request(self, question, file=None):
        """
        Process the request using OpenAI and specific processors.
        
        Args:
            question (str): The question text
            file (InMemoryUploadedFile, optional): Uploaded file
            
        Returns:
            dict: Response with answer key
        """
        # If there's a file, process it first
        file_content = None
        if file:
            # Create a temporary directory to save the file
            with tempfile.TemporaryDirectory() as temp_dir:
                file_path = os.path.join(temp_dir, file.name)
                
                # Save the uploaded file
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                
                # Extract file content using file processor
                file_info = self.file_processor.extract_file_info(file_path)
                
                # Try to directly handle simple known question patterns
                direct_answer = self.get_direct_answer(question, file_info)
                if direct_answer:
                    return {"answer": direct_answer}
                
                # Now send to OpenAI with the file content
                return self.query_openai(question, file_info)
        
        # If no file, just send the question to OpenAI
        return self.query_openai(question)
    
    def get_direct_answer(self, question, file_info):
        """
        Try to directly answer common question patterns without calling OpenAI.
        
        Args:
            question (str): The question text
            file_info (dict): Information extracted from the file
            
        Returns:
            str or None: Direct answer if possible, None otherwise
        """
        # Common pattern: "What is the value in the 'answer' column of the CSV file?"
        if ("answer column" in question.lower() or "column" in question.lower() and "answer" in question.lower()) and file_info.get('type') == 'csv':
            if file_info.get('data') is not None and 'answer' in file_info['data'].columns:
                return str(file_info['data']['answer'].iloc[0])
        
        # Add more direct answer patterns here for common questions
        
        return None
    
    def query_openai(self, question, file_info=None):
        """
        Query OpenAI with the question and file content.
        
        Args:
            question (str): The question text
            file_info (dict, optional): Information extracted from the file
            
        Returns:
            dict: Response with answer key
        """
        try:
            # Ensure API key is set
            if not openai.api_key:
                return {"answer": "Error: OpenAI API key not configured"}
            
            # Prepare the prompt
            if file_info:
                prompt = f"Question: {question}\n\nFile Content: {file_info['content']}\n\nAnswer the question based on the file content. Provide ONLY the answer, without any explanations or text."
            else:
                prompt = f"Question: {question}\n\nAnswer the question directly. Provide ONLY the answer, without any explanations or text."
            
            # Call OpenAI API
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for the IIT Madras Online Degree in Data Science. Your task is to answer questions accurately. Provide only the exact answer without any explanations or additional text."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0  # Use low temperature for more deterministic answers
            )
            
            # Extract the answer from OpenAI's response
            answer = response.choices[0].message.content.strip()
            
            return {"answer": answer}
        
        except Exception as e:
            return {"answer": f"Error: {str(e)}"}
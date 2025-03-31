import os
import tempfile
import requests
import json
from django.conf import settings
from .question_matcher import QuestionMatcher

class RequestHandler:
    """
    Handles incoming requests by processing questions and files.
    """
    def __init__(self):
        from .processors.file_processor import FileProcessor
        self.file_processor = FileProcessor()
        # Get AI Proxy token instead of OpenAI API key
        self.aiproxy_token = settings.AIPROXY_TOKEN or os.environ.get("AIPROXY_TOKEN", "")
        # Initialize the question matcher
        self.question_matcher = QuestionMatcher()
        
    def process_request(self, question, file=None):
        """
        Process the request using question repository first, then AI Proxy.
        
        Args:
            question (str): The question text
            file (InMemoryUploadedFile, optional): Uploaded file
            
        Returns:
            dict: Response with answer key
        """
        # First try to match from the question repository
        matched, answer = self.question_matcher.match_question(question)
        if matched:
            #return {"answer": answer, "source": "repository"}
            return {"answer": answer}
        
        # If there's a file, process it
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
                    #return {"answer": direct_answer, "source": "direct"}
                    return {"answer": direct_answer}
                
                # Now send to AI Proxy with the file content
                return self.query_aiproxy(question, file_info)
        
        # If no file and no repository match, just send the question to AI Proxy
        return self.query_aiproxy(question)
    
    def get_direct_answer(self, question, file_info):
        """
        Try to directly answer common question patterns without calling AI Proxy.
        
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
    
    def query_aiproxy(self, question, file_info=None):
        """
        Query AI Proxy with the question and file content.
        
        Args:
            question (str): The question text
            file_info (dict, optional): Information extracted from the file
            
        Returns:
            dict: Response with answer key
        """
        try:
            # Ensure API token is set
            if not self.aiproxy_token:
                #return {"answer": "Error: AI Proxy token not configured", "source": "error"}
                return {"answer": "Error: AI Proxy token not configured"}
            
            # Prepare the prompt
            if file_info:
                prompt = f"Question: {question}\n\nFile Content: {file_info['content']}\n\nAnswer the question based on the file content. Provide ONLY the answer, without any explanations or text."
            else:
                prompt = f"Question: {question}\n\nAnswer the question directly. Provide ONLY the answer, without any explanations or text."
            
            # Prepare the request to AI Proxy
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.aiproxy_token}"
            }
            
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant for the IIT Madras Online Degree in Data Science. Your task is to answer questions accurately. Provide only the exact answer without any explanations or additional text."},
                    {"role": "user", "content": prompt}
                ]
            }
            
            # Call AI Proxy API
            response = requests.post(
                "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Parse the response
            response_data = response.json()
            
            # Extract the answer from the response
            answer = response_data['choices'][0]['message']['content'].strip()
            
            #return {"answer": answer, "source": "ai_proxy"}
            return {"answer": answer}
        
        except Exception as e:
            #return {"answer": f"Error: {str(e)}", "source": "error"}
            return {"answer": f"Error: {str(e)}"}
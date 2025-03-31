import os
import tempfile
import requests
import json
import re
from django.conf import settings
from django.http import JsonResponse
from .question_matcher import QuestionMatcher

# NOTE: When using this class in a Django view, make sure to return the result as a JsonResponse:
# Example usage in a view:
#
# def answer_question(request):
#     request_handler = RequestHandler()
#     question = request.POST.get('question', '')
#     file = request.FILES.get('file', None)
#     result = request_handler.process_request(question, file)
#     # Important: Use JsonResponse to ensure proper JSON formatting with double quotes
#     return JsonResponse(result)

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
            dict: Response with answer key as a string without markdown
        """
        # First try to match from the question repository
        matched, answer = self.question_matcher.match_question(question)
        if matched:
            # Return properly formatted answer
            return {"answer": self._ensure_string_answer(answer)}
        
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
                    # Return properly formatted answer
                    return {"answer": self._ensure_string_answer(direct_answer)}
                
                # Now send to AI Proxy with the file content
                return self.query_aiproxy(question, file_info)
        
        # If no file and no repository match, just send the question to AI Proxy
        return self.query_aiproxy(question)
    
    def _ensure_string_answer(self, answer):
        """
        Ensure the answer is always a string, converting JSON objects if necessary.
        Also cleans up markdown code blocks and other formatting.
        
        Args:
            answer: The answer which could be a string, dict, or other object
            
        Returns:
            str: The answer as a string, cleaned of formatting
        """
        if answer is None:
            return ""
            
        if isinstance(answer, dict) or isinstance(answer, list):
            try:
                return json.dumps(answer)
            except:
                return str(answer)
        
        # Convert to string
        answer_str = str(answer)
        
        # Clean up markdown code blocks (```content```)
        if answer_str.startswith("```") and answer_str.endswith("```"):
            # Remove the starting ``` and ending ``` and any language identifier
            lines = answer_str.split("\n")
            if len(lines) >= 3:  # At least 3 lines: opening ```, content, closing ```
                # Remove first and last line (the ```)
                content_lines = lines[1:-1]
                answer_str = "\n".join(content_lines)
            else:
                # Simple case - just remove the backticks
                answer_str = answer_str.strip("`")
        
        # Clean any markdown formatting for inline code with single backticks
        answer_str = re.sub(r'`([^`]+)`', r'\1', answer_str)
        
        # Try to extract answer from JSON-like structures
        try:
            if '"answer_text":' in answer_str:
                # Try to parse JSON-like structure
                match = re.search(r'"answer_text":\s*"(.*?)"', answer_str, re.DOTALL)
                if match:
                    json_value = match.group(1)
                    # Unescape any escaped quotes
                    json_value = json_value.replace('\\"', '"')
                    # Clean up the extracted value for code blocks
                    if json_value.startswith("```") and json_value.endswith("```"):
                        lines = json_value.split("\n")
                        if len(lines) >= 3:
                            content_lines = lines[1:-1]
                            json_value = "\n".join(content_lines)
                        else:
                            json_value = json_value.strip("`")
                    answer_str = json_value
        except:
            # If extraction fails, keep the original string
            pass
        
        # Trim whitespace
        answer_str = answer_str.strip()
        
        return answer_str
    
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
            dict: Response with answer key as a string without markdown
        """
        try:
            # Ensure API token is set
            if not self.aiproxy_token:
                return {"answer": "Error: AI Proxy token not configured"}
            
            # Prepare the prompt
            if file_info:
                prompt = f"Question: {question}\n\nFile Content: {file_info['content']}\n\nAnswer the question based on the file content. Provide ONLY the answer, without any explanations or text."
            else:
                prompt = f"Question: {question}\n\nAnswer the question directly. Provide ONLY the answer, without any explanations or text."
            
            # Add explicit instruction to avoid markdown and provide plain text only
            prompt += " Do not use any markdown formatting, code blocks, or backticks in your response. Provide a plain text response only."
            
            # Prepare the request to AI Proxy
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.aiproxy_token}"
            }
            
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant for the IIT Madras Online Degree in Data Science. Your task is to answer questions accurately. Provide only the exact answer as plain text without any explanations, additional text, or formatting. Do not use JSON, markdown, code blocks, or backticks in your response."},
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
            
            # Ensure answer is a string, even if it appears to be a JSON object
            # or contains markdown formatting like code blocks
            try:
                # Check if the answer is a JSON string that needs to be converted
                if answer.startswith('{') or answer.startswith('['):
                    # Try to parse it to check if it's valid JSON
                    json_obj = json.loads(answer)
                    # If it parsed successfully, we'll convert it back to a string
                    answer = self._ensure_string_answer(json_obj)
                else:
                    # Clean up any markdown formatting or code blocks
                    answer = self._ensure_string_answer(answer)
            except json.JSONDecodeError:
                # If it's not valid JSON, still clean it up
                answer = self._ensure_string_answer(answer)
            
            # Return JSON-serializable dict with a single "answer" field
            # This will be converted to proper JSON by Django's JsonResponse
            return {"answer": answer}
        
        except Exception as e:
            return {"answer": f"Error: {str(e)}"}
        
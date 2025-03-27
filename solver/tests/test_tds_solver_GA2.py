"""
Test suite for TDS Solver API using Assignment 2 files.
This module contains test cases for all assignments based on the requirements.
"""

import os
import json
import requests
import pandas as pd
from pathlib import Path

# API endpoint
API_URL = "http://localhost:8000/api/"


def call_api(question, file_path=None, file_name=None):
    """
    Call the TDS Solver API with a question and optional file.
    """
    if file_path:
        # Convert to proper path for the current OS
        file_path = Path(file_path)
        
        # Check if file exists
        if not file_path.exists():
            print(f"Error: File not found: {file_path}")
            # Try to look for the file in the current directory or test_data
            alternative_paths = [
                Path("test_data") / file_path.name,
                Path("test_data") / file_path.parts[-2] / file_path.name,
                Path.cwd() / file_path.name
            ]
            
            for alt_path in alternative_paths:
                if alt_path.exists():
                    print(f"Found file at alternative location: {alt_path}")
                    file_path = alt_path
                    break
            else:
                return {"error": f"File not found: {file_path}"}
        
        with open(file_path, 'rb') as file_data:
            files = {
                'question': (None, question),
                'file': (file_name or file_path.name, file_data)
            }
            response = requests.post(API_URL, files=files)
    else:
        files = {
            'question': (None, question)
        }
        response = requests.post(API_URL, files=files)
    
    return response.json()


def test_markdown_documentation():
    """
    Test Q1: Write documentation in Markdown
    """
    print("\n===== Testing Markdown Documentation (Q1) =====")
    
    question = """Write documentation in Markdown for an imaginary analysis of the number of steps you walked each day for a week, comparing over time and with friends. The Markdown must include:
    Top-Level Heading, Subheadings, Bold Text, Italic Text, Inline Code, Code Block, Bulleted List, Numbered List, Table, Hyperlink, Image, and Blockquote."""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_image_compression():
    """
    Test Q2: Compress an image
    """
    print("\n===== Testing Image Compression (Q2) =====")
    
    file_path = "test_data/images/steps_visualization.png"
    
    question = """Download the image and compress it losslessly to an image that is less than 1,500 bytes.
    By losslessly, we mean that every pixel in the new image should be identical to the original image."""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_github_pages():
    """
    Test Q3: Host your portfolio on GitHub Pages
    """
    print("\n===== Testing GitHub Pages (Q3) =====")
    
    question = """Host a website using GitHub Pages. Publish a page that showcases your work. 
    Ensure that your email address 23f3000756@ds.study.iitm.ac.in is in the page's HTML.
    Wrap your email address inside a: <!--email_off-->23f3000756@ds.study.iitm.ac.in<!--/email_off-->
    What is the GitHub Pages URL?"""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_google_colab():
    """
    Test Q4: Use Google Colab
    """
    print("\n===== Testing Google Colab (Q4) =====")
    
    question = """Run this program on Google Colab, allowing all required access to your email ID: 23f3000756@ds.study.iitm.ac.in.

    import hashlib
    import requests
    from google.colab import auth
    from oauth2client.client import GoogleCredentials

    auth.authenticate_user()
    creds = GoogleCredentials.get_application_default()
    token = creds.get_access_token().access_token
    response = requests.get(
      "https://www.googleapis.com/oauth2/v1/userinfo",
      params={"alt": "json"},
      headers={"Authorization": f"Bearer {token}"}
    )
    email = response.json()["email"]
    hashlib.sha256(f"{email} {creds.token_expiry.year}".encode()).hexdigest()[-5:]
    
    What is the result? (It should be a 5-character string)"""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_image_library_colab():
    """
    Test Q5: Use an Image Library in Google Colab
    """
    print("\n===== Testing Image Library in Google Colab (Q5) =====")
    
    file_path = "test_data/images/brightness_test.jpg"
    
    question = """Create a new Google Colab notebook and run this code (after fixing a mistake in it) to calculate the number of pixels with a certain minimum brightness:

    import numpy as np
    from PIL import Image
    from google.colab import files
    import colorsys

    # There is a mistake in the line below. Fix it
    image = Image.open(list(files.upload().keys)[0])

    rgb = np.array(image) / 255.0
    lightness = np.apply_along_axis(lambda x: colorsys.rgb_to_hls(*x)[1], 2, rgb)
    light_pixels = np.sum(lightness > 0.481)
    print(f'Number of pixels with lightness > 0.481: {light_pixels}')
    
    What is the result? (It should be a number)"""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_vercel_deployment():
    """
    Test Q6: Deploy a Python API to Vercel
    """
    print("\n===== Testing Vercel Deployment (Q6) =====")
    
    file_path = "test_data/csv_files/students_marks.csv"
    
    question = """Create and deploy a Python app to Vercel. Expose an API so that when a request like https://your-app.vercel.app/api?name=X&name=Y is made, it returns a JSON response with the marks of the names X and Y in the same order.
    Make sure you enable CORS to allow GET requests from any origin.
    What is the Vercel URL?"""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_github_action():
    """
    Test Q7: Create a GitHub Action
    """
    print("\n===== Testing GitHub Action (Q7) =====")
    
    question = """Create a GitHub action on one of your GitHub repositories. Make sure one of the steps in the action has a name that contains your email address 23f3000756@ds.study.iitm.ac.in.
    Trigger the action and make sure it is the most recent action.
    What is your repository URL?"""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_docker_hub():
    """
    Test Q8: Push an image to Docker Hub
    """
    print("\n===== Testing Docker Hub (Q8) =====")
    
    question = """Create and push an image to Docker Hub. Add a tag named 23f3000756 to the image.
    What is the Docker image URL?"""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_fastapi_server():
    """
    Test Q9: Write a FastAPI server to serve data
    """
    print("\n===== Testing FastAPI Server (Q9) =====")
    
    file_path = "test_data/csv_files/students_class.csv"
    
    question = """Write a FastAPI server that serves student class data. If the URL has a query parameter class, it should return only students in those classes. For example, /api?class=1A should return only students in class 1A. /api?class=1A&class=1B should return only students in class 1A and 1B.
    Make sure you enable CORS to allow GET requests from any origin.
    What is the API URL endpoint for FastAPI?"""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_local_llm():
    """
    Test Q10: Run a local LLM with Llamafile
    """
    print("\n===== Testing Local LLM with Llamafile (Q10) =====")
    
    question = """Download Llamafile. Run the Llama-3.2-1B-Instruct.Q6_K.llamafile model with it.
    Create a tunnel to the Llamafile server using ngrok.
    What is the ngrok URL?"""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


# Function to run all tests
def run_all_tests():
    """Run all the test cases and return the results."""
    results = {}
    
    # Run all tests
    print("\n===== Running All TDS Solver API Tests for Assignment 2 =====\n")
    
    results["markdown_documentation"] = test_markdown_documentation()
    results["image_compression"] = test_image_compression()
    results["github_pages"] = test_github_pages()
    results["google_colab"] = test_google_colab()
    results["image_library_colab"] = test_image_library_colab()
    results["vercel_deployment"] = test_vercel_deployment()
    results["github_action"] = test_github_action()
    results["docker_hub"] = test_docker_hub()
    results["fastapi_server"] = test_fastapi_server()
    results["local_llm"] = test_local_llm()
    
    print("\n===== Test Summary =====\n")
    for test_name, result in results.items():
        print(f"{test_name}: {'Success' if 'answer' in result else 'Failure'}")
    
    return results


# Dictionary mapping question numbers to test functions
test_functions = {
    "1": test_markdown_documentation,
    "2": test_image_compression,
    "3": test_github_pages,
    "4": test_google_colab,
    "5": test_image_library_colab,
    "6": test_vercel_deployment,
    "7": test_github_action,
    "8": test_docker_hub,
    "9": test_fastapi_server,
    "10": test_local_llm
}

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Run specific test by question number
        question_number = sys.argv[1]
        if question_number in test_functions:
            print(f"Running test for Question {question_number}")
            test_functions[question_number]()
        else:
            print(f"No test available for Question {question_number}")
            print(f"Available questions: {', '.join(sorted(test_functions.keys()))}")
    else:
        # Run all tests
        run_all_tests()
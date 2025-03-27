"""
Test suite for TDS Solver API using Assignment 4 (Web Scraping) files.
This module contains test cases for all assignments based on the requirements.
"""

import os
import json
import requests
import pandas as pd
from pathlib import Path
import base64

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


def test_import_html_google_sheets():
    """
    Test Q1: Import HTML to Google Sheets
    """
    print("\n===== Testing Import HTML to Google Sheets (Q1) =====")
    
    question = """CricketPro Insights is a leading sports analytics firm specializing in providing in-depth statistical analysis for cricket teams.
    ESPN Cricinfo has ODI batting stats for each batsman. The result is paginated across multiple pages. Count the number of ducks in page number 18.
    
    Count the total number of ducks (where the player was out for 0 runs) by summing the values in the "0" column on page 18."""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_scrape_imdb_movies():
    """
    Test Q2: Scrape IMDb movies
    """
    print("\n===== Testing Scrape IMDb movies (Q2) =====")
    
    question = """StreamFlix is a rapidly growing streaming service aiming to provide a diverse and high-quality library of movies.
    Write a Python program that extracts movie information from IMDb for all films that have a rating between 3 and 5.
    Format the extracted information into a JSON format containing the following fields:
    id: The unique identifier for the movie on IMDb.
    title: The official title of the movie.
    year: The year the movie was released.
    rating: The IMDb user rating for the movie.
    
    For up to the first 25 titles, extract the necessary details and organize them into a JSON structure."""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_wikipedia_outline():
    """
    Test Q3: Wikipedia Outline
    """
    print("\n===== Testing Wikipedia Outline (Q3) =====")
    
    question = """GlobalEdu Platforms is a leading provider of educational technology solutions.
    Write a web application that exposes an API with a single query parameter: ?country=. It should fetch the Wikipedia page of the country, extracts all headings (H1 to H6), and create a Markdown outline for the country.
    
    Enable CORS to allow GET requests from any origin.
    
    What is the URL of your API endpoint?"""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_scrape_bbc_weather_api():
    """
    Test Q4: Scrape the BBC Weather API
    """
    print("\n===== Testing Scrape the BBC Weather API (Q4) =====")
    
    question = """AgroTech Insights is a leading agricultural technology company that provides data-driven solutions to farmers.
    Develop a system that automates the following:
    
    1. API Integration and Data Retrieval: Use the BBC Weather API to fetch the weather forecast for Chicago.
    2. Weather Data Extraction: Retrieve the weather forecast data using the obtained locationId.
    3. Data Transformation: Extract the localDate and enhancedWeatherDescription from each day's forecast.
    
    Create a JSON object where each key is the localDate and the value is the enhancedWeatherDescription.
    
    What is the JSON weather forecast description for Chicago?"""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_find_city_bounding_box():
    """
    Test Q5: Find the bounding box of a city
    """
    print("\n===== Testing Find the bounding box of a city (Q5) =====")
    
    question = """UrbanRide is a leading transportation and logistics company operating in major metropolitan areas worldwide.
    What is the maximum latitude of the bounding box of the city Santiago in the country Chile on the Nominatim API?
    
    Use the Nominatim API to fetch geospatial data for Santiago, Chile and extract the maximum latitude value."""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_search_hacker_news():
    """
    Test Q6: Search Hacker News
    """
    print("\n===== Testing Search Hacker News (Q6) =====")
    
    question = """TechInsight Analytics is a leading market research firm specializing in technology trends and media intelligence.
    Search using the Hacker News RSS API for the latest Hacker News post mentioning Go and having a minimum of 77 points.
    
    What is the link that it points to?"""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_find_newest_github_user():
    """
    Test Q7: Find newest GitHub user
    """
    print("\n===== Testing Find newest GitHub user (Q7) =====")
    
    question = """CodeConnect is an innovative recruitment platform that specializes in matching high-potential tech talent with forward-thinking companies.
    Using the GitHub API, find all users located in the city Chennai with over 130 followers.
    
    When was the newest user's GitHub profile created?
    
    Enter the date (ISO 8601, e.g. "2024-01-01T00:00:00Z") when the newest user joined GitHub."""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_create_scheduled_github_action():
    """
    Test Q8: Create a Scheduled GitHub Action
    """
    print("\n===== Testing Create a Scheduled GitHub Action (Q8) =====")
    
    question = """DevSync Solutions is a mid-sized software development company specializing in collaborative tools for remote teams.
    Create a scheduled GitHub action that runs daily and adds a commit to your repository. The workflow should:
    
    - Use schedule with cron syntax to run once per day (must use specific hours/minutes, not wildcards)
    - Include a step with your email 23f3000756@ds.study.iitm.ac.in in its name
    - Create a commit in each run
    - Be located in .github/workflows/ directory
    
    Enter your repository URL (format: https://github.com/USER/REPO):"""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_extract_tables_from_pdf():
    """
    Test Q9: Extract tables from PDF
    """
    print("\n===== Testing Extract tables from PDF (Q9) =====")
    
    file_path = "test_data/pdf_files/student_marks.pdf"
    
    question = """EduAnalytics Corp. is a leading educational technology company that partners with schools and educational institutions to provide data-driven insights into student performance.
    
    This file contains a table of student marks in Maths, Physics, English, Economics, and Biology.
    
    Calculate the total Maths marks of students who scored 21 or more marks in Maths in groups 77-100 (including both groups)."""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_convert_pdf_to_markdown():
    """
    Test Q10: Convert a PDF to Markdown
    """
    print("\n===== Testing Convert a PDF to Markdown (Q10) =====")
    
    file_path = "test_data/pdf_files/sample_document.pdf"
    
    question = """EduDocs Inc. is a leading provider of educational resources and documentation management solutions for academic institutions.
    
    Convert the PDF to Markdown: Extract the content from the PDF file. Accurately convert the extracted content into Markdown format, preserving the structure and formatting as much as possible.
    
    Format the Markdown: Use Prettier version 3.4.2 to format the converted Markdown file.
    
    What is the markdown content of the PDF, formatted with prettier@3.4.2?"""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


# Function to run all tests
def run_all_tests():
    """Run all the test cases and return the results."""
    results = {}
    
    # Run all tests
    print("\n===== Running All TDS Solver API Tests for Assignment 4 =====\n")
    
    results["import_html_google_sheets"] = test_import_html_google_sheets()
    results["scrape_imdb_movies"] = test_scrape_imdb_movies()
    results["wikipedia_outline"] = test_wikipedia_outline()
    results["scrape_bbc_weather_api"] = test_scrape_bbc_weather_api()
    results["find_city_bounding_box"] = test_find_city_bounding_box()
    results["search_hacker_news"] = test_search_hacker_news()
    results["find_newest_github_user"] = test_find_newest_github_user()
    results["create_scheduled_github_action"] = test_create_scheduled_github_action()
    results["extract_tables_from_pdf"] = test_extract_tables_from_pdf()
    results["convert_pdf_to_markdown"] = test_convert_pdf_to_markdown()
    
    print("\n===== Test Summary =====\n")
    for test_name, result in results.items():
        print(f"{test_name}: {'Success' if 'answer' in result else 'Failure'}")
    
    return results


# Dictionary mapping question numbers to test functions
test_functions = {
    "1": test_import_html_google_sheets,
    "2": test_scrape_imdb_movies,
    "3": test_wikipedia_outline,
    "4": test_scrape_bbc_weather_api,
    "5": test_find_city_bounding_box,
    "6": test_search_hacker_news,
    "7": test_find_newest_github_user,
    "8": test_create_scheduled_github_action,
    "9": test_extract_tables_from_pdf,
    "10": test_convert_pdf_to_markdown
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
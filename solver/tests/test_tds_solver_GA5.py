"""
Test suite for TDS Solver API using Assignment 5 (Data Cleaning) files.
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


def test_clean_excel_sales_data():
    """
    Test Q1: Clean up Excel sales data
    """
    print("\n===== Testing Clean up Excel sales data (Q1) =====")
    
    file_path = "test_data/excel_files/sales_data.xlsx"
    
    question = """RetailWise Inc. is a retail analytics firm that supports companies in optimizing their pricing, margins, and inventory decisions.
    
    You need to clean this Excel data and calculate the total margin for all transactions that satisfy the following criteria:
    
    Time Filter: Sales that occurred up to and including a specified date (Mon Dec 19 2022 06:38:52 GMT+0530 (India Standard Time)).
    Product Filter: Transactions for a specific product (Alpha). (Use only the product name before the slash.)
    Country Filter: Transactions from a specific country (FR), after standardizing the country names.
    
    The total margin is defined as: Total Margin = Total Sales - Total Cost / Total Sales
    
    What is the total margin for transactions before Mon Dec 19 2022 06:38:52 GMT+0530 (India Standard Time) for Alpha sold in FR (which may be spelt in different ways)?"""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_clean_student_marks():
    """
    Test Q2: Clean up student marks
    """
    print("\n===== Testing Clean up student marks (Q2) =====")
    
    file_path = "test_data/text_files/student_marks.txt"
    
    question = """EduTrack Systems is a leading provider of educational management software that helps schools and universities maintain accurate and up-to-date student records.
    
    As a data analyst at EduTrack Systems, your task is to process this text file and determine the number of unique students based on their student IDs.
    
    The file is formatted with lines structured as follows:
    NAME STUDENT ID Marks MARKS
    
    How many unique students are there in the file?"""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_apache_log_requests():
    """
    Test Q3: Apache log requests
    """
    print("\n===== Testing Apache log requests (Q3) =====")
    
    file_path = "test_data/log_files/apache_log.gz"
    
    question = """s-anand.net is a personal website that had region-specific music content. One of the site's key sections is telugu, which hosts music files and is especially popular among the local audience.
    
    As a data analyst, you are tasked with determining how many successful GET requests for pages under telugu were made on Sunday between 12 and 21 during May 2024.
    
    What is the number of successful GET requests for pages under /telugu/ from 12:00 until before 21:00 on Sundays?"""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_apache_log_downloads():
    """
    Test Q4: Apache log downloads
    """
    print("\n===== Testing Apache log downloads (Q4) =====")
    
    file_path = "test_data/log_files/apache_log.gz"
    
    question = """s-anand.net is a personal website that had region-specific music content. One of the site's key sections is kannada, which hosts music files and is especially popular among the local audience.
    
    Your task is to determine the IP address that has the highest total downloaded bytes from the kannada section on 2024-05-04.
    
    Across all requests under kannada/ on 2024-05-04, how many bytes did the top IP address (by volume of downloads) download?"""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_clean_sales_data():
    """
    Test Q5: Clean up sales data
    """
    print("\n===== Testing Clean up sales data (Q5) =====")
    
    file_path = "test_data/csv_files/city_sales.csv"
    
    question = """GlobalRetail Insights is a market research and analytics firm specializing in providing data-driven insights for multinational retail companies.
    
    As a data analyst at GlobalRetail Insights, you are tasked with extracting meaningful insights from this dataset. Specifically, you need to:
    
    1. Group Mis-spelt City Names: Use phonetic clustering algorithms to group together entries that refer to the same city despite variations in spelling.
    2. Filter Sales Entries: Select all entries where the product sold is Mouse and the number of units sold is at least 124.
    3. Aggregate Sales by City: After clustering city names, group the filtered sales entries by city and calculate the total units sold for each city.
    
    How many units of Mouse were sold in Rio de Janeiro on transactions with at least 124 units?"""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_parse_partial_json():
    """
    Test Q6: Parse partial JSON
    """
    print("\n===== Testing Parse partial JSON (Q6) =====")
    
    file_path = "test_data/json_files/truncated_sales.json"
    
    question = """ReceiptRevive Analytics is a data recovery and business intelligence firm specializing in processing legacy sales data from paper receipts.
    
    As a data recovery analyst at ReceiptRevive Analytics, your task is to develop a program that will:
    
    1. Parse the Sales Data: Read the provided JSON file containing 100 rows of sales data. Despite the truncated data (specifically the missing id), you must accurately extract the sales figures from each row.
    2. Data Validation and Cleanup: Ensure that the data is properly handled even if some fields are incomplete.
    3. Calculate Total Sales: Sum the sales values across all 100 rows to provide a single aggregate figure that represents the total sales recorded.
    
    What is the total sales value?"""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_extract_nested_json_keys():
    """
    Test Q7: Extract nested JSON keys
    """
    print("\n===== Testing Extract nested JSON keys (Q7) =====")
    
    file_path = "test_data/json_files/nested_logs.json"
    
    question = """DataSure Technologies is a leading provider of IT infrastructure and software solutions, known for its robust systems and proactive maintenance practices.
    
    As a data analyst at DataSure Technologies, you have been tasked with developing a script that processes a large JSON log file and counts the number of times a specific key, represented by the placeholder SKG, appears in the JSON structure. Your solution must:
    
    1. Parse the Large, Nested JSON: Efficiently traverse the JSON structure regardless of its complexity.
    2. Count Key Occurrences: Increment a count only when SKG is used as a key in the JSON object (ignoring occurrences of SKG as a value).
    3. Return the Count: Output the total number of occurrences, which will be used by the operations team to assess the prevalence of particular system events or errors.
    
    How many times does SKG appear as a key?"""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_duckdb_social_media():
    """
    Test Q8: DuckDB: Social Media Interactions
    """
    print("\n===== Testing DuckDB: Social Media Interactions (Q8) =====")
    
    question = """EngageMetrics is a digital marketing analytics firm that specializes in tracking and analyzing social media engagement.
    
    Your task as a data analyst at EngageMetrics is to write a query that performs the following:
    
    1. Filter Posts by Date: Consider only posts with a timestamp greater than or equal to 2025-01-31T02:00:05.191Z.
    2. Evaluate Comment Quality: From these recent posts, identify posts where at least one comment has received more than 4 useful stars.
    3. Extract and Sort Post IDs: Extract all the post_id values of the posts that meet these criteria and sort them in ascending order.
    
    Write a DuckDB SQL query to find all posts IDs after 2025-01-31T02:00:05.191Z with at least 1 comment with 4 useful stars, sorted."""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_transcribe_youtube_video():
    """
    Test Q9: Transcribe a YouTube video
    """
    print("\n===== Testing Transcribe a YouTube video (Q9) =====")
    
    question = """Mystery Tales Publishing is an independent publisher specializing in mystery and suspense audiobooks.
    
    As part of a pilot project, you are tasked with transcribing the YouTube video segment of a mystery story audiobook. You are provided with a sample video that features a narrated mystery story. Your focus will be on the segment starting at 431.7 and ending at 597.5.
    
    What is the text of the transcript of this Mystery Story Audiobook between 431.7 and 597.5 seconds?"""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_reconstruct_image():
    """
    Test Q10: Reconstruct an image
    """
    print("\n===== Testing Reconstruct an image (Q10) =====")
    
    file_path = "test_data/images/scrambled_image.png"
    
    question = """PixelGuard Solutions is a digital forensics firm specializing in the recovery and analysis of visual evidence for law enforcement and corporate investigations.
    
    As a digital forensics analyst at PixelGuard Solutions, your task is to reconstruct the original image from its scrambled pieces. You are provided with:
    
    1. The 25 individual image pieces (put together as a single image).
    2. A mapping file detailing the original (row, col) position for each piece and its current (row, col) location.
    
    Mapping of each piece:
    Original Row\tOriginal Column\tScrambled Row\tScrambled Column
    2\t1\t0\t0
    1\t1\t0\t1
    4\t1\t0\t2
    0\t3\t0\t3
    0\t1\t0\t4
    1\t4\t1\t0
    2\t0\t1\t1
    2\t4\t1\t2
    4\t2\t1\t3
    2\t2\t1\t4
    0\t0\t2\t0
    3\t2\t2\t1
    4\t3\t2\t2
    3\t0\t2\t3
    3\t4\t2\t4
    1\t0\t3\t0
    2\t3\t3\t1
    3\t3\t3\t2
    4\t4\t3\t3
    0\t2\t3\t4
    3\t1\t4\t0
    1\t2\t4\t1
    1\t3\t4\t2
    0\t4\t4\t3
    4\t0\t4\t4
    
    Upload the reconstructed image by moving the pieces from the scrambled position to the original position."""
    
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
    print("\n===== Running All TDS Solver API Tests for Assignment 5 =====\n")
    
    results["clean_excel_sales_data"] = test_clean_excel_sales_data()
    results["clean_student_marks"] = test_clean_student_marks()
    results["apache_log_requests"] = test_apache_log_requests()
    results["apache_log_downloads"] = test_apache_log_downloads()
    results["clean_sales_data"] = test_clean_sales_data()
    results["parse_partial_json"] = test_parse_partial_json()
    results["extract_nested_json_keys"] = test_extract_nested_json_keys()
    results["duckdb_social_media"] = test_duckdb_social_media()
    results["transcribe_youtube_video"] = test_transcribe_youtube_video()
    results["reconstruct_image"] = test_reconstruct_image()
    
    print("\n===== Test Summary =====\n")
    for test_name, result in results.items():
        print(f"{test_name}: {'Success' if 'answer' in result else 'Failure'}")
    
    return results


# Dictionary mapping question numbers to test functions
test_functions = {
    "1": test_clean_excel_sales_data,
    "2": test_clean_student_marks,
    "3": test_apache_log_requests,
    "4": test_apache_log_downloads,
    "5": test_clean_sales_data,
    "6": test_parse_partial_json,
    "7": test_extract_nested_json_keys,
    "8": test_duckdb_social_media,
    "9": test_transcribe_youtube_video,
    "10": test_reconstruct_image
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
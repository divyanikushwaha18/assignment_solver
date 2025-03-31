"""
Test suite for TDS Solver API using actual assignment files.
This module contains test cases for all assignments based on the requirements.
"""

import os
import json
import requests
import pandas as pd
from pathlib import Path

# API endpoint
API_URL = "http://localhost:8000/api/"
#API_URL = "https://assignment-solver.vercel.app/api/"


# Then modify the call_api function to handle paths better:
def call_api(question, file_path=None, file_name=None):
    """
    Call the TDS Solver API with a question and optional file.
    """
    try:
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
        
        # Add debugging information
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response content: {response.text[:500]}...")  # Print first 500 chars to avoid overwhelming output
        
        # Check if we got a valid response before trying to parse JSON
        if response.status_code != 200:
            return {
                "error": f"API request failed with status code {response.status_code}",
                "response_text": response.text
            }
        
        # Check if there's content to parse
        if not response.text.strip():
            return {"error": "Empty response received from API"}
            
        # Try to parse JSON response
        return response.json()
        
    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        return {"error": f"Request failed: {str(e)}"}
    except json.JSONDecodeError as e:
        # Handle JSON parsing errors
        return {
            "error": f"Failed to parse JSON response: {str(e)}",
            "response_text": response.text
        }
def test_vs_code_version():
    """
    Test Q1: VS Code Version
    """
    print("\n===== Testing VS Code Version (Q1) =====")
    
    question = """Install and run Visual Studio Code. In your Terminal (or Command Prompt), type code -s and press Enter. Copy and paste the entire output below.
    What is the output of code -s?"""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result

def test_api_request():
    """
    Test Q2: API request
    """
    print("\n===== Testing API Request (Q2) =====")
    
    question = """Send a HTTPS request to https://httpbin.org/get with the URL encoded parameter email set to 23f3000756@ds.study.iitm.ac.in. What is the JSON output of the command?"""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result

def test_markdown_formatting():
    """
    Test Q3: Markdown formatting with prettier
    """
    print("\n===== Testing Markdown Formatting (Q3) =====")
    
    file_path = "test_data/markdown_files/README.md"
    
    question = """Let's make sure you know how to use `npx` and `prettier`.
    Download README.md. In the directory where you downloaded it, make sure it is called `README.md`, and run `npx -y prettier@3.4.2 README.md | sha256sum`.
    What is the output of the command?"""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result

def test_google_sheets_formula():
    """
    Test Q4: Google Sheets formula
    """
    print("\n===== Testing Google Sheets Formula (Q4) =====")
    
    question = """Let's make sure you can write formulas in Google Sheets. Type this formula into Google Sheets. (It won't work in Excel)
    =SUM(ARRAY_CONSTRAIN(SEQUENCE(100, 100, 3, 3), 1, 10))
    What is the result?"""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result

def test_excel_formula():
    """
    Test Q5: Excel formula
    """
    print("\n===== Testing Excel Formula (Q5) =====")
    
    question = """Let's make sure you can write formulas in Excel. Type this formula into Excel.
    Note: This will ONLY work in Office 365.
    =SUM(TAKE(SORTBY({6,10,8,15,3,13,6,6,1,10,2,15,10,1,0,11}, {10,9,13,2,11,8,16,14,7,15,5,4,6,1,3,12}), 1, 4))
    What is the result?"""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result

def test_devtools_usage():
    """
    Test Q6: DevTools usage
    """
    print("\n===== Testing DevTools Usage (Q6) =====")
    
    file_path = "solver/tests/test_data/text_files/devtools_test.html"
    
    question = """Just above this paragraph, there's a hidden input with a secret value. What is the value in the hidden input?"""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result

def test_date_counting():
    """
    Test Q7: Date counting
    """
    print("\n===== Testing Date Counting (Q7) =====")
    
    question = """How many Wednesdays are there in the date range 1985-12-29 to 2009-02-13?
    The dates are in the year-month-day format. Include both the start and end date in your count."""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result

def test_zip_extraction():
    """
    Test Q8: ZIP file extraction
    """
    print("\n===== Testing ZIP File Extraction (Q8) =====")
    
    file_path = "solver/tests/test_data/zip_files/q-extract-csv-zip.zip"
    
    question = "Download and unzip file q-extract-csv-zip.zip which has a single extract.csv file inside. What is the value in the 'answer' column of the CSV file?"
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result

def test_json_sorting():
    """
    Test Q9: JSON sorting
    """
    print("\n===== Testing JSON Sorting (Q9) =====")
    
    # The JSON is provided directly in the question
    question = """Sort this JSON array of objects by the value of the age field. In case of a tie, sort by the name field. Paste the resulting JSON below without any spaces or newlines.
    [{"name":"Alice","age":30},{"name":"Bob","age":91},{"name":"Charlie","age":62},{"name":"David","age":31},{"name":"Emma","age":39},{"name":"Frank","age":17},{"name":"Grace","age":95},{"name":"Henry","age":32},{"name":"Ivy","age":49},{"name":"Jack","age":35},{"name":"Karen","age":49},{"name":"Liam","age":73},{"name":"Mary","age":71},{"name":"Nora","age":21},{"name":"Oscar","age":31},{"name":"Paul","age":91}]"""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result

def test_multi_cursor_editing():
    """
    Test Q10: Multi-cursor editing
    """
    print("\n===== Testing Multi-cursor Editing (Q10) =====")
    
    file_path = "solver/tests/test_data/text_files/q-multi-cursor-json.txt"
    
    question = """Download q-multi-cursor-json.txt and use multi-cursors to convert it into a single JSON object, where key=value pairs are converted into {"key": value, "key": value, ...}.
    What's the result when you paste the JSON at tools-in-data-science.pages.dev/jsonhash and click the Hash button?"""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result

def test_css_selector():
    """
    Test Q11: CSS selector
    """
    print("\n===== Testing CSS Selector (Q11) =====")
    
    file_path = "solver/tests/test_data/text_files/TDS 2025 Jan GA1 - Development Tools.html"
    
    question = """Find all <div>s having a foo class in the hidden element below. What's the sum of their data-value attributes?"""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result

def test_file_encoding_processing():
    """
    Test Q12: File encoding processing
    """
    print("\n===== Testing File Encoding Processing (Q12) =====")
    
    file_path = "solver/tests/test_data/zip_files/q-unicode-data.zip"
    
    question = """Process the files in q-unicode-data.zip which contains three files with different encodings:
    data1.csv: CSV file encoded in CP-1252
    data2.csv: CSV file encoded in UTF-8
    data3.txt: Tab-separated file encoded in UTF-16
    Each file has 2 columns: symbol and value. Sum up all the values where the symbol matches › OR œ OR — across all three files.
    What is the sum of all values associated with these symbols?"""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result

def test_github_usage():
    """
    Test Q13: GitHub usage
    """
    print("\n===== Testing GitHub Usage (Q13) =====")
    
    question = """Let's make sure you know how to use GitHub. Create a GitHub account if you don't have one. Create a new public repository. Commit a single JSON file called email.json with the value {"email": "23f3000756@ds.study.iitm.ac.in"} and push it.
    Enter the raw Github URL of email.json so we can verify it. (It might look like https://raw.githubusercontent.com/[GITHUB ID]/[REPO NAME]/main/email.json.)"""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result

def test_file_replacement():
    """
    Test Q14: File replacement
    """
    print("\n===== Testing File Replacement (Q14) =====")
    
    file_path = "solver/tests/test_data/zip_files/q-replace-across-files.zip"
    
    question = """Download q-replace-across-files.zip and unzip it into a new folder, then replace all "IITM" (in upper, lower, or mixed case) with "IIT Madras" in all files. Leave everything as-is - don't change the line endings.
    What does running cat * | sha256sum in that folder show in bash?"""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result

def test_file_listing():
    """
    Test Q15: File listing
    """
    print("\n===== Testing File Listing (Q15) =====")
    
    file_path = "solver/tests/test_data/zip_files/q-list-files-attributes.zip"
    
    question = """Download q-list-files-attributes.zip and extract it. Use ls with options to list all files in the folder along with their date and file size.
    What's the total size of all files at least 7461 bytes large and modified on or after Sat, 7 Jul, 2007, 2:42 pm IST?"""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result

def test_file_renaming():
    """
    Test Q16: File renaming
    """
    print("\n===== Testing File Renaming (Q16) =====")
    
    file_path = "solver/tests/test_data/zip_files/q-move-rename-files.zip"
    
    question = """Download q-move-rename-files.zip and extract it. Use mv to move all files under folders into an empty folder. Then rename all files replacing each digit with the next. 1 becomes 2, 9 becomes 0, a1b9c.txt becomes a2b0c.txt.
    What does running grep . * | LC_ALL=C sort | sha256sum in bash on that folder show?"""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result

def test_file_comparison():
    """
    Test Q17: File comparison
    """
    print("\n===== Testing File Comparison (Q17) =====")
    
    file_path = "solver/tests/test_data/zip_files/q-compare-files.zip"
    
    question = """Download q-compare-files.zip and extract it. It has 2 nearly identical files, a.txt and b.txt, with the same number of lines.
    How many lines are different between a.txt and b.txt?"""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result

def test_sql_query():
    """
    Test Q18: SQL query
    """
    print("\n===== Testing SQL Query (Q18) =====")
    
    file_path = "solver/tests/test_data/sql_files/tickets.db"
    
    question = """There is a tickets table in a SQLite database that has columns type, units, and price. Each row is a customer bid for a concert ticket.
    What is the total sales of all the items in the "Gold" ticket type? Write SQL to calculate it.
    Get all rows where the Type is "Gold". Ignore spaces and treat mis-spellings like GOLD, gold, etc. as "Gold". Calculate the sales as Units * Price, and sum them up."""
    
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
    print("\n===== Running All TDS Solver API Tests =====\n")
    
    results["vs_code_version"] = test_vs_code_version()
    results["api_request"] = test_api_request()
    results["markdown_formatting"] = test_markdown_formatting()
    results["google_sheets_formula"] = test_google_sheets_formula()
    results["excel_formula"] = test_excel_formula()
    results["devtools_usage"] = test_devtools_usage()
    results["date_counting"] = test_date_counting()
    results["zip_extraction"] = test_zip_extraction()
    results["json_sorting"] = test_json_sorting()
    results["multi_cursor_editing"] = test_multi_cursor_editing()
    results["css_selector"] = test_css_selector()
    results["file_encoding_processing"] = test_file_encoding_processing()
    results["github_usage"] = test_github_usage()
    results["file_replacement"] = test_file_replacement()
    results["file_listing"] = test_file_listing()
    results["file_renaming"] = test_file_renaming()
    results["file_comparison"] = test_file_comparison()
    results["sql_query"] = test_sql_query()
    
    print("\n===== Test Summary =====\n")
    for test_name, result in results.items():
        print(f"{test_name}: {'Success' if 'answer' in result else 'Failure'}")
    
    return results

    # Dictionary mapping question numbers to test functions
test_functions = {
    "1": test_vs_code_version,
    "2": test_api_request,
    "3": test_markdown_formatting,
    "4": test_google_sheets_formula,
    "5": test_excel_formula,
    "6": test_devtools_usage,
    "7": test_date_counting,
    "8": test_zip_extraction,
    "9": test_json_sorting,
    "10": test_multi_cursor_editing,
    "11": test_css_selector,
    "12": test_file_encoding_processing,
    "13": test_github_usage,
    "14": test_file_replacement,
    "15": test_file_listing,
    "16": test_file_renaming,
    "17": test_file_comparison,
    "18": test_sql_query
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
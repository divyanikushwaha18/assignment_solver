import requests
import os
import tempfile

def test_api_no_file():
    """
    Test the API endpoint without a file.
    """
    url = "http://localhost:8000/api/"
    
    # Use multipart/form-data format (important for compatibility with your view)
    files = {
        'question': (None, 'What is the capital of INDIA?')
    }
    
    response = requests.post(url, files=files)
    print("Response:", response.json())
    assert 'answer' in response.json()

def test_api_with_csv():
    """
    Test the API endpoint with a CSV file.
    """
    url = "http://localhost:8000/api/"
    
    # Create a temporary CSV file
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
        temp.write(b'id,name,answer\n1,Test,42\n2,Another,73\n')
        temp_path = temp.name
    
    try:
        with open(temp_path, 'rb') as file_data:
            files = {
                'question': (None, 'What is the value in the "name" column of the CSV file?'),
                'file': ('test.csv', file_data)
            }
            
            response = requests.post(url, files=files)
            print("Response:", response.json())
            assert 'answer' in response.json()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the file before trying to delete it
        try:
            os.unlink(temp_path)
        except PermissionError:
            print(f"Note: Could not delete temporary file {temp_path} - Windows file lock issue")
if __name__ == "__main__":
    print("Testing API without file...")
    test_api_no_file()
    
    print("\nTesting API with CSV file...")
    test_api_with_csv()
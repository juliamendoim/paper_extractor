import requests

def post_extract_objectives_and_endpoints(api_url: str, input_folder: str):
    """
    Sends a POST request to the FastAPI endpoint to process PDFs.

    Args:
        api_url (str): The base URL of the FastAPI server.
        input_folder (str): The folder containing PDFs to process.

    Returns:
        dict: The JSON response from the server.
    """
    endpoint = f"{api_url}/extract_objectives_and_endpoints"
    payload = {"input_folder": input_folder}

    try:
        response = requests.post(endpoint, json=payload)

        if response.status_code == 200:
            print("Success:", response.json())
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        raise

if __name__ == "__main__":
    API_URL = "http://127.0.0.1:8000"
    INPUT_FOLDER = "input"

    post_extract_objectives_and_endpoints(API_URL, INPUT_FOLDER)

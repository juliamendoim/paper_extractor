
# PDF Processing App

This application processes PDF files to extract objectives and endpoints, and saves the structured data to a CSV file.

## Requirements

Ensure you have the required dependencies installed. You can install them using the `requirements.txt` file:

```sh
pip install -r requirements.txt
```

## Running the App

1. **Set up the environment:**

   Create an `.env` file in the root directory and add the  variable `OPENAI_API_KEY` with the value of your OpenAI api key.

2. **Start the FastAPI server:**

   Run the following command to start the server:

   ```sh
   uvicorn app:app --reload
   ```

3. **Access the API:**

   Open your browser and go to `http://127.0.0.1:8000/docs` to access the Swagger UI where you can interact with the API.

   Or run `client.py` from a terminal with python.

## API Endpoints

### Extract Objectives and Endpoints

- **URL:** `/extract_objectives_and_endpoints`
- **Method:** `POST`
- **Summary:** Processes PDF files into a structured CSV output.
- **Parameters:**
  - `input_folder` (str): Path to the folder containing PDF files. Default is `"input"`.

- **Response:**
  - `dict`: A message indicating the output file path.

Example request:

```sh
curl -X POST "http://127.0.0.1:8000/extract_objectives_and_endpoints" -H "accept: application/json" -d ""
```

## Project Structure

```
app.py
client.py
input/
notebooks/
    data.csv
    evaluation.ipynb
    output.csv
    test_data.csv
    training.ipynb
output/
README.md
requirements.txt
src/
    data_models.py
    helpers.py
    llm.py
    pdf_process.py
    pdf_structure.py
    prompt.py
tests/
    src/
        test_helpers.py
```

## Notes

- Ensure the `input` folder contains the PDF files you want to process.
- The structured data will be saved in the `output` folder as `output.csv`.

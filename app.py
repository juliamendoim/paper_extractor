import os
import logging
from fastapi import FastAPI, HTTPException
import pandas as pd

from src.pdf_process import PDFProcessor
from src.pdf_structure import PDFStructurer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
async def root():
    """
    Root endpoint to confirm the service is running.
    
    Returns:
        dict: A welcome message.
    """
    return {"message": "Automatic PDF structure service is running."}

@app.post(
    "/extract_objectives_and_endpoints",
    summary="Processes PDF files into a structured CSV output",
    tags=["PDF Processing"]
)
def extract_objectives_and_endpoints(input_folder: str = "input") -> dict:
    """
    Processes PDF files in the input folder, extracts structured data,
    and saves the output to a CSV file.

    Args:
        input_folder (str): Path to the folder containing PDF files.

    Returns:
        dict: A message indicating the output file path.
    """
    if not os.path.isdir(input_folder):
        logger.error(f"Input folder '{input_folder}' does not exist.")
        raise HTTPException(status_code=400, detail=f"Input folder '{input_folder}' does not exist.")

    df_output = pd.DataFrame()

    try:
        for file in os.listdir(input_folder):
            file_path = os.path.join(input_folder, file)

            if file.endswith(".pdf"):
                logger.info(f"Processing file: {file}")
                try:
                    pdf_processor = PDFProcessor(file_path)
                    pdf_structured = PDFStructurer(pdf_processor).data_df
                    data_dicts = [item.dict() for item in pdf_structured]
                    df = pd.DataFrame(data_dicts)
                    df_output = pd.concat([df_output, df])
                except Exception as e:
                    logger.error(f"Failed to process {file}: {e}")
                    continue

        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)

        output_file = os.path.join(output_folder, "output.csv")
        df_output.to_csv(output_file, index=False)

        logger.info(f"Structured data saved to: {output_file}")
        return {"message": f"Saved to CSV at {output_file}"}

    except Exception as e:
        logger.exception("An unexpected error occurred during processing.")
        raise HTTPException(status_code=500, detail=str(e))
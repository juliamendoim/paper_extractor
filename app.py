import os
import logging
from typing import Dict
from fastapi import FastAPI, HTTPException
import pandas as pd

from src.pdf_process import PDFProcessor
from src.pdf_structure import PDFStructurer

# Configure logging with detailed formatting
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')  # Add file logging
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app with metadata
app = FastAPI(
    title="PDF Structure Extraction API",
    description="API for extracting objectives and endpoints from PDF documents",
    version="1.0.0"
)

@app.get("/")
async def root() -> Dict[str, str]:
    """
    Root endpoint to verify API health status.
    
    Provides a simple health check endpoint to confirm the service
    is operational and responding to requests.
    
    Returns:
        Dict[str, str]: A dictionary containing a welcome message
        
    Example:
        Response: {"message": "Automatic PDF structure service is running."}
    """
    logger.debug("Health check endpoint accessed")
    return {"message": "Automatic PDF structure service is running."}

@app.post(
    "/extract_objectives_and_endpoints",
    summary="Extract structured data from PDF files",
)
def extract_objectives_and_endpoints(input_folder: str = "input") -> Dict[str, str]:
    """
    Process PDF files to extract objectives and endpoints data.
    
    Scans the specified input folder for PDF files, processes each file
    to extract structured data about objectives and endpoints, and
    consolidates the results into a single CSV file.
    
    Args:
        input_folder (str, optional): Path to folder containing PDF files. 
                                    Defaults to "input".
    
    Returns:
        Dict[str, str]: Success message with path to output CSV file
    """

    logger.info("Starting PDF extraction process from folder: %s", input_folder)
    
    # Validate input folder
    if not os.path.isdir(input_folder):
        error_msg = f"Input folder '{input_folder}' does not exist"
        logger.error(error_msg)
        raise HTTPException(status_code=400, detail=error_msg)

    df_output = pd.DataFrame()
    processed_files = 0
    failed_files = 0

    try:
        # Process each PDF file
        pdf_files = [f for f in os.listdir(input_folder) if f.endswith(".pdf")]
        total_files = len(pdf_files)
        logger.info("Found %d PDF files to process", total_files)

        for file in pdf_files:
            file_path = os.path.join(input_folder, file)
            logger.info("Processing file %d/%d: %s", processed_files + failed_files + 1, total_files, file)

            try:
                # Process individual PDF
                logger.debug("Initializing PDF processor for %s", file)
                pdf_processor = PDFProcessor(file_path)
                
                logger.debug("Structuring data from %s", file)
                pdf_structured = PDFStructurer(pdf_processor).data_df
                
                # Convert structured data to DataFrame
                data_dicts = [item.dict() for item in pdf_structured]
                df = pd.DataFrame(data_dicts)
                
                # Append to master DataFrame
                df_output = pd.concat([df_output, df])
                processed_files += 1
                logger.info("Successfully processed %s", file)

            except Exception as e:
                failed_files += 1
                logger.error("Failed to process %s: %s", file, str(e), exc_info=True)
                continue

        # Create output directory and save results
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)
        
        output_file = os.path.join(output_folder, "output.csv")
        df_output.to_csv(output_file, index=False)
        
        # Log processing summary
        logger.info(
            "Processing complete: %d successful, %d failed out of %d total files",
            processed_files, failed_files, total_files
        )
        logger.info("Output saved to: %s", output_file)
        
        return {
            "message": f"Saved to CSV at {output_file}",
        }

    except Exception as e:
        error_msg = "Unexpected error during PDF processing"
        logger.exception(error_msg)
        raise HTTPException(status_code=500, detail=f"{error_msg}: {str(e)}")

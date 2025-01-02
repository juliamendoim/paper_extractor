from fastapi import FastAPI

from src.data_models import Output
from src.pdf_process import PDFProcessor


app = FastAPI()

@app.get("/")
async def root():
    """
    Provides a simple root endpoint that returns a JSON message.
    
    Returns:
        dict: A dictionary with a 'message' key and a string value.
    """ 
    return {"message": "Automatic PDF structure"}

@app.post("/extract_objectives_and_endpoints", summary="Processes PDF files to a expected strutured output")
def extract_objectives_and_endpoints(
    input_folder: str = "input",
    ) -> None:

    processed_pdf_df = PDFProcessor(input_folder).structure()
    output = Output(data=processed_pdf_df)
    output.save_to_csv("output/output.csv")
    

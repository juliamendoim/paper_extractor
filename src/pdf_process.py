import logging
import pymupdf
import pytesseract
from pdf2image import convert_from_path

from src.helpers import matching_toc

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class PDFProcessor:
    """
    A class to process PDF documents and extract their table of contents.
    
    This class handles both standard PDFs and scanned PDFs requiring OCR.
    It attempts to extract the table of contents directly first, falling back
    to OCR processing if necessary.
    
    Attributes:
        pdf_path (str): Path to the PDF file
        pdf_name (str): Name of the PDF file without extension
        doc (pymupdf.Document): Loaded PDF document
        toc (list): Extracted table of contents
    """

    def __init__(self, pdf_path: str):
        """
        Initialize the PDFProcessor with a PDF file path.
        
        Args:
            pdf_path (str): Path to the PDF file to process
        """
        logger.info("Initializing PDFProcessor for file: %s", pdf_path)
        self.pdf_path = pdf_path
        self.pdf_name = pdf_path.split("/")[-1].rstrip(".pdf")
        self.doc = self.read_pdf(self.pdf_path)
        self.toc = self.read_toc(self.doc)

    def read_pdf(self, pdf_path: str) -> pymupdf.Document:
        """
        Read a PDF file and process it appropriately.
        
        First attempts to read the PDF directly. If no table of contents
        is found, falls back to OCR processing.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            pymupdf.Document: Processed PDF document
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            pymupdf.FileDataError: If the PDF file is corrupted
        """
        logger.info("Attempting to read PDF: %s", pdf_path)
        try:
            doc = pymupdf.open(pdf_path)
            if self.has_toc(doc):
                logger.info("Successfully found table of contents in PDF")
            else:
                logger.warning("No table of contents found, attempting OCR processing")
                doc = self.read_pdf_with_ocr(pdf_path)
            return doc
        except Exception as e:
            logger.error("Error reading PDF: %s", str(e))
            raise

    def has_toc(self, doc: pymupdf.Document) -> bool:
        """
        Check if the document has a table of contents.
        
        Args:
            doc (pymupdf.Document): PDF document to check
            
        Returns:
            bool: True if the document has a table of contents, False otherwise
        """
        toc_exists = len(doc.get_toc()) > 0
        logger.debug("Table of contents exists: %s", toc_exists)
        return toc_exists

    def read_pdf_with_ocr(self, pdf_path: str) -> pymupdf.Document:
        """
        Process a PDF file using OCR when direct extraction fails.
        
        Converts PDF pages to images and performs OCR to extract text.
        Creates a new PDF document with the extracted text.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            pymupdf.Document: New PDF document containing OCR-extracted text
            
        Raises:
            pytesseract.TesseractError: If OCR processing fails
        """
        logger.info("Starting OCR processing of PDF")
        try:
            pages = convert_from_path(pdf_path, dpi=90)
            doc = pymupdf.open()
            
            for i, page in enumerate(pages):
                logger.debug("Processing page %d with OCR", i+1)
                text = pytesseract.image_to_string(page)
                
                new_page = doc.new_page(width=page.width, height=page.height)
                text_insertion = f"\n\n------- Page {i+1} -------\n\n{text}"
                new_page.insert_text((50, 50), text_insertion)
                
            logger.info("Successfully processed %d pages with OCR", len(pages))
            return doc
        except Exception as e:
            logger.error("OCR processing failed: %s", str(e))
            raise

    def retrieve_toc(self, doc: pymupdf.Document) -> list:
        """
        Extract table of contents by scanning through document pages.
        
        Args:
            doc (pymupdf.Document): PDF document to process
            
        Returns:
            list: Extracted table of contents entries
        """
        logger.info("Retrieving table of contents from document text")
        toc = []
        for i, page in enumerate(doc):
            logger.debug("Scanning page %d for table of contents entries", i+1)
            toc.extend(matching_toc(page.get_text()))
        logger.info("Found %d table of contents entries", len(toc))
        return toc

    def read_toc(self, doc: pymupdf.Document) -> list:
        """
        Read the table of contents from the document.
        
        Attempts to get the TOC directly first, falls back to
        parsing document text if necessary.
        
        Args:
            doc (pymupdf.Document): PDF document to process
            
        Returns:
            list: Table of contents entries
        """
        logger.info("Attempting to read table of contents")
        if self.has_toc(doc):
            logger.info("Using built-in table of contents")
            toc = doc.get_toc()
        else:
            logger.info("Extracting table of contents from document text")
            toc = self.retrieve_toc(doc)
        
        logger.info("Successfully extracted %d TOC entries", len(toc))
        return toc

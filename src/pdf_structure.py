import json
import logging
from typing import List

from src.pdf_process import PDFProcessor
from src.data_models import DFSchema
from src.helpers import matching_section
from src.llm import llm_call

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class PDFStructurer:
    """
    A class to structure and process PDF content into structured data.
    
    This class takes a processed PDF document and extracts relevant sections,
    processes their content, and structures the data into a standardized format.
    It focuses on sections related to objectives and endpoints.
    
    Attributes:
        name (str): Name of the PDF document
        doc (Document): Processed PDF document
        toc (list): Table of contents
        sections (list): List of relevant section page numbers
        pages (List[str]): Extracted content from relevant pages
        data_df (list): Structured data extracted from the PDF
    """

    def __init__(self, processed_pdf: PDFProcessor):
        """
        Initialize the PDFStructurer with a processed PDF document.
        
        Args:
            processed_pdf (PDFProcessor): A processed PDF document object
        """
        logger.info("Initializing PDFStructurer for document: %s", processed_pdf.pdf_name)
        self.name = processed_pdf.pdf_name
        self.doc = processed_pdf.doc
        self.toc = processed_pdf.toc
        self.sections = self.section_pages()
        self.pages = self.retrieve_pages_content()
        self.data_df = self.structure()

    def retrieve_pages_content(self) -> List[str]:
        """
        Extract and concatenate content from relevant pages in the PDF.
        
        Processes pages sequentially, combining content from consecutive pages
        into single blocks for better context preservation.
        
        Returns:
            List[str]: List of text content from relevant sections
            
        Note:
            Pages are considered consecutive if their numbers follow directly
        """
        logger.info("Retrieving content from relevant pages")
        pages = []
        current_content = ""
        previous_page = None
        
        for page_n in self.sections:
            logger.debug("Processing page %s", page_n)
            if previous_page is not None and page_n == previous_page + 1:
                logger.debug("Concatenating consecutive page %s", page_n)
                current_content += self.doc.load_page(page_n - 1).get_text()
            else:
                if current_content:
                    pages.append(current_content)
                current_content = self.doc.load_page(page_n - 1).get_text()
            
            previous_page = page_n
        
        if current_content:
            pages.append(current_content)
        
        logger.info("Retrieved content from %s sections", len(pages))
        return pages
    def section_pages(self) -> list:
        """
        Identify pages containing relevant sections (objectives/endpoints).
        
        Scans through the table of contents to find pages that contain
        sections related to objectives or endpoints.
        
        Returns:
            list: List of page numbers containing relevant sections
        """
        logger.info("Identifying relevant section pages")
        section_pages = []

        for element in self.toc:
            if matching_section(element[1]):
                if element[2] not in section_pages:
                    logger.debug("Found relevant section on page %s: %s", element[2], element[1])
                    section_pages.append(element[2])
        
        logger.info("Found %s relevant section pages", len(section_pages))
        return section_pages
    def parse_schema_data(self, llm_response: str) -> str:
        """
        Clean and format the LLM response for JSON parsing.
        
        Removes markdown formatting and unnecessary characters from the
        LLM response to prepare it for JSON parsing.
        
        Args:
            llm_response (str): Raw response from the LLM
            
        Returns:
            str: Cleaned response ready for JSON parsing
        """
        logger.debug("Cleaning LLM response for parsing")
        llm_response = llm_response.replace("json", "")
        llm_response = llm_response.replace("```", "")
        llm_response = llm_response.replace("\n", "")
        
        return llm_response
    
    def structure(self) -> list:
        """
        Process PDF content into structured data format.
        
        Processes each page's content through an LLM to extract structured data,
        then formats it according to the DFSchema.
        
        Returns:
            list: List of DFSchema objects containing structured data
            
        Raises:
            json.JSONDecodeError: If LLM response cannot be parsed as JSON
            KeyError: If required fields are missing from parsed data
        """
        logger.info("Starting structured data extraction")
        data = []
        
        for i, page in enumerate(self.pages):
            try:
                logger.debug("Processing content block %d/%d", i + 1, len(self.pages))
                llm_response = llm_call(text=page)
                parsed_response = self.parse_schema_data(llm_response)
                parsed_json = json.loads(parsed_response)
                parsed_data = parsed_json.get("data", [])

                for element in parsed_data:
                    data.append(
                        DFSchema(
                            name=self.name,
                            section_level_0="objectives-endpoints-section",
                            **element)
                    )
                logger.debug("Successfully processed %d elements from content block %d", len(parsed_data), i + 1)
                
            except json.JSONDecodeError as e:
                logger.error("Failed to parse JSON from LLM response in content block %d: %s", i+1, e)
            except KeyError as e:
                logger.error("Missing required field in parsed data from content block %d: %s", i+1, e)
            except Exception as e:
                logger.error("Unexpected error processing content block %d: %s", i+1, e)

        logger.info("Completed structured data extraction. Processed %d total elements", len(data))
        return data
    

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
    def __init__(self, processed_pdf: PDFProcessor):
        self.name = processed_pdf.pdf_name
        self.doc = processed_pdf.doc
        self.toc = processed_pdf.toc
        self.sections = self.section_pages()
        self.pages = self.retrieve_pages_content()
        self.data_df = self.structure()

    def retrieve_pages_content(self) -> List[str]:
        pages = []
        current_content = ""
        previous_page = None
        
        for page_n in self.sections:
            if previous_page is not None and page_n == previous_page + 1:
                current_content += self.doc.load_page(page_n - 1).get_text()
            else:
                if current_content:
                    pages.append(current_content)
                current_content = self.doc.load_page(page_n - 1).get_text()
            
            previous_page = page_n
        
        if current_content:
            pages.append(current_content)
        
        return pages
    

    def section_pages(self) -> list:
        section_pages = []

        for element in self.toc:
            if matching_section(element[1]):
                if element[2] not in section_pages:
                    section_pages.append(element[2])
        
        return section_pages

    def parse_schema_data(self, llm_response: str) -> str:
        llm_response = llm_response.replace("json", "")
        llm_response = llm_response.replace("```", "")
        llm_response = llm_response.replace("\n", "")
        
        return llm_response
    
    def structure(self) -> list:
        """
        Process the PDF files into a structured DataFrame.

        Returns:
            pd.DataFrame: A structured DataFrame with the processed data.
        """

        data = []
        for page in self.pages:
            try:
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
            except Exception as e:
                logger.error(f"Error processing page {page}: {e}")

        return data

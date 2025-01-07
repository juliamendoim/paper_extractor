import re
import logging

import pymupdf
import pytesseract

from pdf2image import convert_from_path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.pdf_name = pdf_path.split("/")[-1].rstrip(".pdf")
        self.doc = self.read_pdf(self.pdf_path)
        self.toc = self.read_toc(self.doc)

    def read_pdf(self, pdf_path: str) -> pymupdf.Document:
        doc = pymupdf.open(pdf_path)
        if self.has_toc(doc) is False:
            doc = self.read_pdf_with_ocr(pdf_path)

        return doc
    
    def has_toc(self, doc: pymupdf.Document) -> bool:

        return len(doc.get_toc()) > 0
    
    def matching_toc(self, text: str) -> list:
        matches_list = []
        pattern = r'^((\d+\.?)+)\s+([\w\s,()\'\-]+)\.?\s+(\d+)$'

        matches = re.findall(pattern, text, re.MULTILINE)

        for match in matches:
            result = [match[0], match[2], int(match[3])]
            matches_list.append(result)

        return matches_list

    def read_pdf_with_ocr(self, pdf_path: str) -> pymupdf.Document: 
        pages = convert_from_path(pdf_path, dpi=90)
        doc = pymupdf.open()

        for i, page in enumerate(pages):
            text = pytesseract.image_to_string(page)

            new_page = doc.new_page(width=page.width, height=page.height)

            text_insertion = f"\n\n------- Page {i+1} -------\n\n{text}"
            new_page.insert_text((50, 50), text_insertion)

        return doc
    
    def retrieve_toc(self, doc: pymupdf.Document) -> list:
        toc = []
        for page in doc:
            toc.extend(self.matching_toc(page.get_text()))

        return toc
    
    def read_toc(self, doc: pymupdf.Document) -> list:
        if self.has_toc(doc):
            toc = doc.get_toc()
        else:
            toc = self.retrieve_toc(doc)

        return toc
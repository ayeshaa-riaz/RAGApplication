import os
import pdfplumber
import logging
import io
from fastapi import HTTPException, UploadFile

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def extract_text_from_pdf(uploaded_file: UploadFile):
    """
    Extract text from an uploaded PDF file using pdfplumber.
    """
    text = []
    logger.info(f"Starting PDF text extraction from: {uploaded_file.filename}")

    try:
        # Read the file bytes
        pdf_bytes = await uploaded_file.read()
        pdf_stream = io.BytesIO(pdf_bytes)  # Convert bytes to a file-like object

        # Open the PDF from bytes
        with pdfplumber.open(pdf_stream) as pdf:
            total_pages = len(pdf.pages)
            logger.info(f"PDF has {total_pages} pages")

            for i, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
                    logger.info(
                        f"Extracted text from page {i}/{total_pages} (length: {len(page_text)} chars)"
                    )
                else:
                    logger.warning(f"No text extracted from page {i}/{total_pages} (possible image-based PDF)")

        extracted_text = "\n".join(text).strip()

        if extracted_text:
            logger.info(f"Successfully extracted text. Total length: {len(extracted_text)} chars")
        else:
            logger.warning("No extractable text found in the PDF. It may require OCR.")

        # Show a preview of the extracted text
        text_sample = extracted_text[:200] + "..." if len(extracted_text) > 200 else extracted_text
        logger.info(f"Text sample: {text_sample}")

        return extracted_text

    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}", exc_info=True)
        return ""

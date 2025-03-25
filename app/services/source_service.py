import os
import pdfplumber
from logger import logger
from fastapi import UploadFile
import uuid
from fastapi import HTTPException, UploadFile
from typing import Dict, Any

# In-memory source store
source_store: Dict[str, Dict[str, Any]] = {}

def process_pdf_file(file: UploadFile, extract_text_from_pdf) -> str:
    """
    Validates and processes a PDF file by extracting its text and storing it in a source store.

    Args:
        file (UploadFile): The uploaded PDF file.
        extract_text_from_pdf (Callable): A function to extract text from the PDF.

    Returns:
        str: The unique source ID assigned to the stored PDF content.
    
    Raises:
        HTTPException: If the file is not a PDF.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    # Extract text from PDF
    text = extract_text_from_pdf(file)
    source_id = str(uuid.uuid4())

    # Store in source store
    source_store[source_id] = {
        "id": source_id,
        "filename": file.filename,
        "type": "PDF",
        "content": text,
        "content_status": "ACTIVE",
    }

    return source_id

def get_source(source_id: str) -> Dict[str, Any]:
    """
    Retrieve a source from the in-memory store.
    
    Args:
        source_id (str): The unique identifier of the source.
        
    Returns:
        Dict[str, Any]: The source data.
        
    Raises:
        HTTPException: If the source is not found.
    """
    if source_id not in source_store:
        raise HTTPException(status_code=404, detail="Source not found")
    return source_store[source_id]

def delete_source(source_id: str) -> None:
    """
    Delete a source from the in-memory store.
    
    Args:
        source_id (str): The unique identifier of the source.
        
    Raises:
        HTTPException: If the source is not found.
    """
    if source_id not in source_store:
        raise HTTPException(status_code=404, detail="Source not found")
    del source_store[source_id]

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF using pdfplumber.
    """
    text = []
    logger.info(f"Starting PDF text extraction from: {pdf_path}")

    with pdfplumber.open(pdf_path) as pdf:
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
                logger.warning(f"No text extracted from page {i}/{total_pages}")

    extracted_text = "\n".join(text)

    if extracted_text.strip():
        logger.info(
            f"Successfully extracted text using pdfplumber. Total length: {len(extracted_text)} chars"
        )
    else:
        logger.warning("No extractable text found in the PDF.")
    
    text_sample = (
        extracted_text[:200] + "..." if len(extracted_text) > 200 else extracted_text
    )
    logger.info(f"Text sample: {text_sample}")

    return extracted_text


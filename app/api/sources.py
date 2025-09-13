from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from typing import Dict, Optional
from rag.document_loader import DocumentLoader
from services.qdrant_service import QdrantService
import logging
import uuid
import os
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
document_loader = DocumentLoader()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("/Users/dev/Desktop/store")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF file, store it locally, then process and store its content in Qdrant."""
    try:
        logger.info(f"Starting PDF upload process for file: {file.filename}")
        
        # Validate file type
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = UPLOAD_DIR / unique_filename

        # Save file locally
        logger.info(f"Saving file to {file_path}")
        with open(file_path, "wb") as buffer:
            content = await file.read()
            if not content:
                raise HTTPException(status_code=400, detail="Empty file content")
            buffer.write(content)

        # Process and store in Qdrant
        logger.info("Loading and splitting PDF...")
        documents = await document_loader.load_and_split_pdf(content, file.filename)
        logger.info(f"PDF split into {len(documents)} chunks")

        logger.info("Storing documents in Qdrant...")
        qdrant_service = QdrantService()
        await qdrant_service.store_documents(documents=documents)
        logger.info("Documents stored successfully in Qdrant")

        return {
            "message": "File uploaded and processed successfully",
            "source_id": str(uuid.uuid4()),
            "file_path": str(file_path),
            "chunks_count": len(documents)
        }

    except HTTPException as http_err:
        logger.error(f"HTTP Exception: {str(http_err)}")
        raise http_err
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing PDF: {str(e)}"
        )


@router.get("/get_all_sources/")
async def get_sources(source_type: Optional[str] = None, page: int = 1, limit: int = 10):
    """This endpoint is now deprecated as we no longer use the source store."""
    raise HTTPException(
        status_code=501,
        detail="This endpoint is deprecated. Please use Qdrant's search functionality instead."
    )

# @router.get("/source/{source_id}")
# async def get_source_by_id(source_id: str):
#     """Retrieve a source by its ID."""
#     source = source_store.get(source_id)
#     if not source:
#         raise HTTPException(status_code=404, detail="Source not found.")
#     return source

# @router.patch("/source/{source_id}/delete")
# async def soft_delete_source(source_id: str):
#     """Soft delete a source (mark it as 'DELETED' without removing it)."""
#     source = source_store.get(source_id)
#     if not source:
#         raise HTTPException(status_code=404, detail="Source not found.")

#     source["content_status"] = "DELETED"
#     return {"message": f"Source {source_id} has been marked as deleted."}

# @router.get("/source/{source_id}/preview")
# async def get_preview_for_source(source_id: str):
#     """Get a preview (first 100 characters) of a source's content."""
#     source = source_store.get(source_id)
#     if not source:
#         raise HTTPException(status_code=404, detail="Source not found.")
    
#     return {"preview": source["content"][:100]}

# @router.delete("/source/{source_id}")
# async def remove_source_by_id(source_id: str):
#     """Remove a source from the store permanently."""
#     if source_id in source_store:
#         del source_store[source_id]
#         return {"message": f"Source {source_id} has been permanently removed."}
#     raise HTTPException(status_code=404, detail="Source not found.")

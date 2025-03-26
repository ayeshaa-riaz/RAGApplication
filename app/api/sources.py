from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Dict, Optional
from app.services.source_service import extract_text_from_pdf, source_store
from app.services.source_service import process_pdf_file
from ..rag.document_loader import DocumentLoader
from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid



router = APIRouter()
document_loader = DocumentLoader()

@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...),collection_name="PrimaryCollection"):
    """Upload a PDF file and store its content in both source store and Qdrant."""
    try:
        # Process the PDF file and store its content in the source store
        source_id = process_pdf_file(file, extract_text_from_pdf, source_store)

        # Read file content for vector storage
        file_content = await file.read()

        # Process and store in Qdrant
        documents = await document_loader.load_and_split_pdf(file_content, file.filename)
        qdrant = await document_loader.store_documents(
            documents=documents,
            collection_name=collection_name
        )

        return {
            "message": "File uploaded and processed successfully",
            "source_id": source_id,
            "chunks_count": len(documents)
        }

    except HTTPException as http_err:
        raise http_err  # Rethrow HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing PDF: {str(e)}"
        )


@router.get("/get_all_sources/")
async def get_sources(source_type: Optional[str] = None, page: int = 1, limit: int = 10):
    """Retrieve all stored sources with optional filtering and pagination."""
    sources = list(source_store.values())

    if source_type:
        sources = [s for s in sources if s["type"] == source_type]

    start, end = (page - 1) * limit, page * limit
    return sources[start:end]

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

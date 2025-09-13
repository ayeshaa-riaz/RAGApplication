from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.schemas import schemas
from db.database import get_db
from services.qdrant_service import QdrantService

router = APIRouter()
qdrant = QdrantService()

@router.post("/", response_model=str)
async def agent_query(
    query_request: schemas.QueryRequest,
    db: Session = Depends(get_db)
):
    """Handles user queries and returns context"""
    try:
        # Perform a similarity search in the vector database
        context = qdrant.search_similar(query_request.query, collection_name=query_request.collection_name)

        if not context:
            raise HTTPException(status_code=404, detail="No similar documents found")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )

    return context
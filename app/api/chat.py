from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..services import chat_service, auth_service
from ..rag.chain import RAGChain
from ..db.schemas import schemas
from typing import List, Optional

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=schemas.Chat)
def create_chat(chat: schemas.ChatBase, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(auth_service.get_current_user)):
    return chat_service.create_chat(db, chat, current_user.id)

@router.get("/", response_model=List[schemas.Chat])
def get_user_chats(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(auth_service.get_current_user)):
    return chat_service.get_user_chats(db, current_user.id)

@router.post("/{chat_id}/message", response_model=schemas.Message)
def create_message(
    chat_id: int,
    message: schemas.MessageBase,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(auth_service.get_current_user)
):
    return chat_service.create_message(db, chat_id, message, current_user.id)

@router.post("/{collection_name}/query")
async def query_documents(
    collection_name: str,
    query: str,
    chat_history: Optional[List[dict]] = None,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(auth_service.get_current_user)
):
    try:
        rag_chain = RAGChain(collection_name)
        response = await rag_chain.generate_response(query, chat_history)
        
        # Store chat in database
        chat_service.save_chat_message(
            db=db,
            user_id=current_user.id,
            content=query,
            response=response["answer"],
            collection_name=collection_name
        )
        
        return {
            "answer": response["answer"],
            "sources": [doc.page_content for doc in response["source_documents"]],
            "chat_history": response["chat_history"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
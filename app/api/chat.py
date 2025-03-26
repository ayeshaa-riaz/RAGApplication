from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..services import chat_service, auth_service
from ..rag.chain import RAGChain
from ..db.schemas import schemas
from typing import List, Optional
from datetime import datetime
from ..db.models.chat_model import ChatSession

router = APIRouter()

@router.post("/start-chat", response_model=schemas.Chat)
async def start_chat(
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(auth_service.get_current_user)
):
    """Start a new chat session for the authenticated user."""
    chat = ChatSession(
        user_id=current_user.id,
        title=f"New Chat {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}" #pending will use llm here
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat



@router.get("/history", response_model=List[schemas.Chat])
async def get_chat_history(
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(auth_service.get_current_user)
):
    """Fetch all chats for the authenticated user."""
    print(f"Fetching chat history for user: {current_user.id}")  # Debugging
    user_chats = db.query(ChatSession).filter(ChatSession.user_id == current_user.id).order_by(ChatSession.created_at.desc()).all()
    
    if not user_chats:
        print("No chat history found.")
        return []  # Return an empty list instead of raising an error
    
    print(f"Found {len(user_chats)} chats for user {current_user.id}")  # Debugging
    return user_chats




@router.post("/{chat_id}/message", response_model=schemas.Message)
async def create_message(
    chat_id: int,
    message: schemas.MessageBase,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(auth_service.get_current_user)
):
    """Create a new message in a chat session."""
    # Verify chat belongs to user
    chat = chat_service.get_chat(db, chat_id, current_user.id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    # Save the user's message
    saved_message = chat_service.create_message(
        db=db,
        chat_id=chat_id,
        message=message,
        user_id=current_user.id
    )
    
    # Get response from RAG chain
    rag_chain = RAGChain()
    response = await rag_chain.ask_agent(
        query=message.content,
        user_id=current_user.id,
        chat_id=chat_id
    )
    
    # Save the assistant's response
    assistant_message = chat_service.create_message(
        db=db,
        chat_id=chat_id,
        message=schemas.MessageBase(content=response.content, role="assistant"),
        user_id=current_user.id
    )
    
    return saved_message

# @router.get("/my-chats", response_model=List[schemas.Chat])
# async def get_user_chats(
#     db: Session = Depends(get_db),
#     current_user: schemas.UserBase = Depends(auth_service.get_current_user)
# ):
#     """Get all chat sessions for the authenticated user."""
#     return chat_service.get_user_chats(db, current_user.id)

@router.get("/{chat_id}", response_model=schemas.Chat)
async def get_chat(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(auth_service.get_current_user)
):
    """Get a specific chat session by ID."""
    chat = chat_service.get_chat(db, chat_id, current_user.id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.get("/{chat_id}/messages", response_model=List[schemas.Message])
async def get_chat_messages(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(auth_service.get_current_user)
):
    """Get all messages for a specific chat."""
    # Verify chat belongs to user
    chat = chat_service.get_chat(db, chat_id, current_user.id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat_service.get_chat_messages(db, chat_id, current_user.id)

@router.delete("/{chat_id}")
async def delete_chat(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserBase = Depends(auth_service.get_current_user)
):
    """Delete a chat session."""
    chat = chat_service.get_chat(db, chat_id, current_user.id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat_service.delete_chat(db, chat_id, current_user.id)

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
    



#     @router.post("/query_reponse", response_model=schemas.QueryResponse)
# async def query_response(
#     query_request: schemas.QueryRequest,
#     db: Session = Depends(get_db)
# ):
#     """Handles user queries and returns context"""
#     try:
#         # Perform a similarity search in the vector database
#         context = qdrant.search_similar(query_request.query, collection_name=query_request.collection_name)

#         if not context:
#             raise HTTPException(status_code=404, detail="No similar documents found")

#         # Get the response from the agent (RAGChain)
#         response = await qdrant.generate_response(query_request.query, user_id=query_request.user_id)

#         # Return the AI-generated response with context
#         return schemas.QueryResponse(
#             answer=response["answer"],
#             source_documents=response["source_documents"],  # You may want to format this
#             context=context  # Return the context (documents from similarity search)
#         )

#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"Error processing request: {str(e)}"
#         )
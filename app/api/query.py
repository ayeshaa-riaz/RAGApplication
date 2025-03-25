import datetime
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException


router = APIRouter()

# ✅ Request Model
class QueryRequest(BaseModel):
    user_id: str
    chat_id: str
    query: str

# ✅ Response Model
class QueryResponse(BaseModel):
    id: str
    content: str
    sender_role: str
    created_at: datetime.datetime
    answer: str

@router.post("/query", response_model=QueryResponse)
def agent_query(query_request: QueryRequest):
    """Handles user queries and returns an AI-generated response."""
    
    try:
        # ✅ Create an agent instance and get the answer
        agent = BaseAgent()
        answer = agent.ask_agent(
            query=query_request.query,
            user_id=query_request.user_id,
            chat_id=query_request.chat_id,
        )

        # ✅ Ensure response is valid
        if not answer:
            raise HTTPException(status_code=500, detail="Agent failed to generate a response")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )

    # ✅ Return structured response
    return QueryResponse(
        id=str(answer.id),
        content=answer.content,
        sender_role=answer.sender_role,
        created_at=answer.created_at,
        answer=answer.content,
    )

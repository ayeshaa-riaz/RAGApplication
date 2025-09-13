from fastapi import FastAPI
from api import api_router



app = FastAPI(
    title="RAG Chatbot API",
    description="A RAG-based chatbot with document ingestion and querying capabilities",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}
# Include the API router
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"Hello": "Welcome to RAG Chatbot API"} 
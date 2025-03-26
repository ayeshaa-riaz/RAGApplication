from sqlalchemy.orm import Session
from datetime import datetime
from langchain_community.chat_models import ChatCohere
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from ..db.database import get_db
import os

# Import only needed functions
from ..db.models.chat_model import ChatSummary,ChatMessage
from ..db.schemas import schemas

async def get_chat_summary(db: Session, chat_id: int) -> str:
    """Retrieve the chat summary if available."""
    summary = db.query(ChatSummary).filter(ChatSummary.chat_id == chat_id).first()
    return summary.summary_text if summary else None

async def generate_summary(db: Session, chat_id: int):
    """Generate and store a summary if chat messages exceed memory limit."""
    messages = db.query(ChatMessage).filter(ChatMessage.chat_id == chat_id).all()

    chat_text = "\n".join([f"{msg.role}: {msg.content}" for msg in messages])
    docs = [Document(page_content=chat_text)]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(docs)

    llm = ChatCohere(cohere_api_key=os.getenv("COHERE_API_KEY"), model="command", temperature=0)
    chain = load_summarize_chain(llm=llm, chain_type="map_reduce")
    summary = chain.run(split_docs)

    existing_summary = db.query(ChatSummary).filter(ChatSummary.chat_id == chat_id).first()
    if existing_summary:
        existing_summary.summary_text = summary
        existing_summary.last_updated = datetime.utcnow()
    else:
        db.add(ChatSummary(chat_id=chat_id, summary_text=summary))

    db.commit()

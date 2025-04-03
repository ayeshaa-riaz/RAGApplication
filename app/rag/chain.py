from langchain.chains import ConversationalRetrievalChain
from langchain_anthropic import ChatAnthropic
from langchain.memory import ConversationBufferMemory
from ..services.qdrant_service import QdrantService  # Fix import spacing
import os
from ..db.database import get_db
from ..db.models.chat_model import ChatMessage,ChatSession
# from langchain.chat_models import ChatCohere 
from langchain_cohere import ChatCohere
from fastapi import HTTPException
from langchain.schema import AIMessage, HumanMessage
import logging

logger = logging.getLogger(__name__)

class RAGChain:
    def __init__(self, collection_name: str = "PrimaryCollection"):
        """Initialize RAGChain with Qdrant vectorstore and memory."""
        
        # Initialize QdrantService
        self.vectorstore = QdrantService(collection_name=collection_name)
        
        # Define memory for chat history
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            output_key="answer",
            return_messages=True
        )
        
        # Create ConversationalRetrievalChain
        self.chain = ConversationalRetrievalChain.from_llm(
             llm=ChatCohere(
               cohere_api_key=os.getenv("COHERE_API_KEY"),  # Use your Cohere API key
               model="command-r-plus",  # Use a Cohere model appropriate for your needs
               temperature=0
            ),
            retriever=self.vectorstore.get_retriever(),
            memory=self.memory,
            return_source_documents=True
        )

 

    async def get_chat_history(self, db, user_id: int, chat_id: int):
        """Retrieve and convert chat history to LangChain format."""
        try:
            messages = db.query(ChatMessage).filter(
                ChatMessage.user_id == user_id,
                ChatMessage.chat_id == chat_id
            ).order_by(ChatMessage.id.asc()).all()

            logger.info(f"Retrieved {len(messages)} messages from database")
            if messages:
                logger.info(f"Message ID range: {messages[0].id} to {messages[-1].id}")

            # 🟢 Convert messages to LangChain format
            chat_history = []
            for msg in messages:
                logger.info(f"Processing message ID {msg.id} from {msg.sender}")
                if msg.sender == "user":
                    chat_history.append(HumanMessage(content=msg.message))
                else:
                    chat_history.append(AIMessage(content=msg.message))

            return chat_history
        except Exception as e:
            logger.error(f"Error retrieving chat history: {str(e)}")
            raise

    async def save_chat_message(self, db, chat_id: int, user_id: int, sender: str, message: str):
        """Save a chat message to the database."""
        try:
            chat = db.query(ChatSession).filter(ChatSession.id == chat_id).first()
            if not chat:
                raise HTTPException(status_code=404, detail="Chat not found")

            new_message = ChatMessage(
                chat_id=chat_id,
                user_id=user_id,
                sender=sender,
                message=message
            )
            db.add(new_message)
            db.commit()
            db.refresh(new_message)
            logger.info(f"Saved {sender} message with ID: {new_message.id} at {new_message.created_at}")
            return new_message
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving message: {str(e)}")
            raise

    async def generate_response(self, question: str, user_id: int, chat_id: int):
        """Retrieve chat history, generate response, and store messages in DB."""
        
        db = next(get_db())

        try:
            # 🟢 Save user message first
            logger.info(f"Saving user message: {question}")
            user_message = await self.save_chat_message(db, chat_id, user_id, "user", question)
            logger.info(f"User message saved with ID: {user_message.id}")
            
            # Ensure transaction is committed and session is refreshed
            db.commit()
            db.flush()

            # 🟢 Load chat history after saving user message
            chat_history = await self.get_chat_history(db, user_id, chat_id)
            logger.info(f"Retrieved chat history with {len(chat_history)} messages")
            
            # 🟢 Store history in LangChain memory
            self.memory.chat_memory.messages = chat_history  

            # 🔥 Generate response
            response = self.chain.invoke({
                "question": question,
                "chat_history": self.memory.chat_memory.messages
            })

            answer = response["answer"]

            # 🟢 Save assistant message
            logger.info(f"Saving assistant message: {answer}")
            assistant_message = await self.save_chat_message(db, chat_id, user_id, "assistant", answer)
            logger.info(f"Assistant message saved with ID: {assistant_message.id}")

            # Ensure transaction is committed and session is refreshed
            db.commit()
            db.flush()

            # 🟢 Get final chat history including both new messages
            final_chat_history = await self.get_chat_history(db, user_id, chat_id)
            logger.info(f"Final chat history has {len(final_chat_history)} messages")

            return {
                "answer": answer,
                "source_documents": response["source_documents"],
                "chat_history": final_chat_history
            }
        except Exception as e:
            db.rollback()
            logger.error(f"Error in generate_response: {str(e)}")
            raise
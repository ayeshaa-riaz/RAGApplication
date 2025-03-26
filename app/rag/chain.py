from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatCohere
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Qdrant
from .embeddings import get_embeddings
import os
from ..db.database import get_db
from ..services.chat_service import get_chat_summary,generate_summary
class RAGChain:
    def __init__(self, collection_name: str = "PrimaryCollection"):
        self.embeddings = get_embeddings()
        self.vectorstore = Qdrant(
            client=Qdrant.construct_client(
                url=os.getenv("QDRANT_URL"),
                api_key=os.getenv("QDRANT_API_KEY")
            ),
            collection_name=collection_name,
            embeddings=self.embeddings,
        )
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=ChatCohere(
                cohere_api_key=os.getenv("COHERE_API_KEY"),
                model="command",
                temperature=0
            ),
            retriever=self.vectorstore.as_retriever(),
            memory=self.memory,
            return_source_documents=True
        )

    async def generate_response(self, question: str, user_id: int):
        """
        Generate a response using the RAG chain.
        Fetch chat summary if memory is empty (new session).
        Store messages only if they exceed memory limits.
        """
        db = next(get_db())

        # Check if memory is empty (new session)
        if not self.memory.chat_memory.messages:
            chat_summary = await get_chat_summary(db, user_id)
            if chat_summary:
                self.memory.chat_memory.messages.append({"role": "assistant", "content": chat_summary})

        # Generate response
        response = self.chain({"question": question, "chat_history": self.memory.chat_memory.messages})

        # Store chat messages only if memory exceeds 5 messages
        if len(self.memory.chat_memory.messages) > 5:
            await generate_summary(db, user_id)

        return {
            "answer": response["answer"],
            "source_documents": response["source_documents"],
            "chat_history": self.memory.chat_memory.messages
        }

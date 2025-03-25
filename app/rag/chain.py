from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Qdrant
from .embeddings import get_embeddings

class RAGChain:
    def __init__(self, collection_name: str):
        self.embeddings = get_embeddings()
        self.vectorstore = Qdrant(
            client=Qdrant.construct_client(url="http://localhost:6333"),
            collection_name=collection_name,
            embeddings=self.embeddings,
        )
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(temperature=0),
            retriever=self.vectorstore.as_retriever(),
            memory=self.memory,
            return_source_documents=True
        )

    async def generate_response(self, question: str, chat_history: list = None):
        """Generate response using the RAG chain"""
        if chat_history is None:
            chat_history = []
            
        response = self.chain({"question": question, "chat_history": chat_history})
        
        return {
            "answer": response["answer"],
            "source_documents": response["source_documents"],
            "chat_history": self.memory.chat_memory.messages
        } 
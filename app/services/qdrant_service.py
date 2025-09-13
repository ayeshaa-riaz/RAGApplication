from typing import List
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import OpenAIEmbeddings
from qdrant_client.http.models import Distance, VectorParams
from dotenv import load_dotenv
import os
from rag.embeddings import get_embeddings
from qdrant_client import QdrantClient
import logging
from langchain_qdrant import QdrantVectorStore,RetrievalMode
import uuid
logger = logging.getLogger(__name__)
load_dotenv()

class QdrantService:
    def __init__(self, collection_name: str = "PrimaryCollection"):
        """Initialize Qdrant with a specific collection and embedding model."""
       
        self.collection_name = collection_name
        self.embeddings = get_embeddings()
        # # Initialize Qdrant client
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
            prefer_grpc=False
        )
        # Ensure collection exists
        self.ensure_collection_exists()
        # Initialize LangChain Qdrant wrapper
        self.vectorstore = QdrantVectorStore(# Initialize with an empty list
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embeddings,
            retrieval_mode=RetrievalMode.DENSE,
        )

    
    def ensure_collection_exists(self):
        """Check if collection exists; if not, create it with correct vector size."""
        try:
            existing_collections = self.client.get_collections()
            collection_names = {col.name for col in existing_collections.collections}
            
            if self.collection_name not in collection_names:
                logger.warning(f"Collection '{self.collection_name}' does not exist. Creating it...")
                self.client.create_collection(
                   collection_name=self.collection_name,
                vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
)
                logger.info(f"Collection '{self.collection_name}' created successfully.")
            else:
                logger.info(f"Collection '{self.collection_name}' already exists.")
        except Exception as e:
            logger.error(f"Error checking/creating collection '{self.collection_name}': {str(e)}", exc_info=True)
            raise

    def add_documents(self, documents):
        """Add documents to Qdrant."""
        try:
            logger.info(f"Adding {len(documents)} documents to collection '{self.collection_name}'")
            # Generate unique IDs for each document
            ids = [str(uuid.uuid4()) for _ in range(len(documents))]
            return self.vectorstore.add_documents(documents, ids=ids)
        except Exception as e:
            logger.error(f"Error adding documents to '{self.collection_name}': {str(e)}", exc_info=True)
            raise
    
    
    def search_similar(self, query, k: int = 5):
        """Search for similar documents."""
        try:
            logger.info(f"Searching for top {k} similar documents in '{self.collection_name}'")
            return self.vectorstore.similarity_search(query, k=k)
        except Exception as e:
            logger.error(f"Error during similarity search in '{self.collection_name}': {str(e)}", exc_info=True)
            raise

    def get_retriever(self):
        """Return a retriever for Qdrant to be used in LangChain's ConversationalRetrievalChain."""
        return self.vectorstore.as_retriever()

    async def store_documents(self, documents: List) -> Qdrant:
        """Store documents in Qdrant, ensuring the collection exists."""
        logger.info(f"i am in the function '{self.collection_name}'")
        try:
            logger.info(f"Checking/creating collection '{self.collection_name}' for storing documents.")
            
            # Use the existing instance if the collection matches, otherwise create a new one
            if self.collection_name == self.collection_name:
                service_instance = self
            else:
                service_instance = QdrantService(collection_name=self.collection_name)

            service_instance.add_documents(documents)
            logger.info(f"Documents successfully stored in '{self.collection_name}'")
            return service_instance.vectorstore
        except Exception as e:
            logger.error(f"Error in store_documents for '{self.collection_name}': {str(e)}", exc_info=True)
            raise

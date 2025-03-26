from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
import os
from dotenv import load_dotenv

load_dotenv()

class QdrantService:
    def __init__(self):
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.client = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key
        )
        self.collection_name = "documents"

    def init_collection(self):
        """Initialize or recreate the collection in Qdrant."""
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE)
        )

    def get_qdrant_store(self, collection_name: str = None):
        """Get a LangChain Qdrant vector store instance."""
        return Qdrant(
            client=self.client,
            collection_name=collection_name or self.collection_name
        )

    def add_documents(self, documents, collection_name: str = None):
        """Add documents to Qdrant using LangChain's Qdrant integration."""
        qdrant_store = self.get_qdrant_store(collection_name)
        return qdrant_store.add_documents(documents)

    def search_similar(self, query, collection_name: str = None, k: int = 5):
        """Search for similar documents using LangChain's Qdrant integration."""
        qdrant_store = self.get_qdrant_store(collection_name)
        return qdrant_store.similarity_search(query, k=k) 
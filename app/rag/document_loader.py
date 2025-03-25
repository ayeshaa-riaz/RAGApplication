from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Qdrant
from .embeddings import get_embeddings
from typing import List
import tempfile
import os
from dotenv import load_dotenv

load_dotenv()

class DocumentLoader:
    """
    A class for loading, splitting, and storing documents in Qdrant.
    """

    def __init__(self):
        """
        Initializes the DocumentLoader with a text splitter and embeddings.
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.embeddings = get_embeddings()
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")

    # async def load_and_split_url(self, url: str) -> List:
    #     """
    #     Loads a webpage and splits its text into chunks.

    #     Args:
    #         url (str): The URL of the webpage to load.

    #     Returns:
    #         List: A list of split document chunks.
    #     """
    #     loader = WebBaseLoader(url)
    #     docs = loader.load()
    #     return self.text_splitter.split_documents(docs)

    async def load_and_split_pdf(self, file_content: bytes, filename: str) -> List:
        """
        Loads and splits a PDF file into chunks.

        Args:
            file_content (bytes): The content of the uploaded PDF file.
            filename (str): The name of the uploaded PDF file.

        Returns:
            List: A list of split document chunks.
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(file_content)
            tmp_file_path = tmp_file.name

        try:
            loader = PyPDFLoader(tmp_file_path)
            docs = loader.load()
            split_docs = self.text_splitter.split_documents(docs)
        finally:
            os.unlink(tmp_file_path)

        return split_docs

    async def store_documents(self, documents: List, collection_name: str) -> Qdrant:
        """
        Stores the processed documents in a Qdrant vector database.

        Args:
            documents (List): The list of document chunks to store.
            collection_name (str): The Qdrant collection name.

        Returns:
            Qdrant: The Qdrant database instance.
        """
        qdrant = Qdrant.from_documents(
            documents,
            self.embeddings,
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
            collection_name=collection_name,
            force_recreate=False,
        )
        return qdrant

from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from  .embeddings import get_embeddings
from typing import List
import tempfile
import os
import logging

logger = logging.getLogger(__name__)

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

    

from langchain_community.embeddings import CohereEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

def get_embeddings():
    """
    Get Cohere embeddings model
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is not set")
        
    return CohereEmbeddings(
        cohere_api_key=api_key,
        model="embed-english-v3.0",
        truncate="END"
    )
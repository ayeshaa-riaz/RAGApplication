import os
from dotenv import load_dotenv
from langchain_cohere import CohereEmbeddings
load_dotenv()
import logging

logger = logging.getLogger(__name__)
def get_embeddings():
    """
    Get Cohere embeddings model, ensuring it's callable.
    """
    logger.info(f"in embeddings function ")
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is not set")
    
    embeddings = CohereEmbeddings(
    cohere_api_key=api_key,
     model="embed-english-v3.0"
     )
    logger.info(f"done embeddings function ")
    return embeddings



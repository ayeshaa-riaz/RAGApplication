
from langchain_core.tools import tool

from app.rag.agent import agent_query


@tool
def Rag_query(query: str) -> str:
    return agent_query(query)

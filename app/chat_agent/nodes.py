import os
from uuid import uuid4

from langchain_core.messages import AIMessage, HumanMessage, RemoveMessage
from langchain_core.runnables import RunnableConfig

from app.chat_agent.state import AICompanionState
from app.Chat_agent.memory.memory_manager import get_memory_manager

from ai_companion.modules.memory.long_term.memory_manager import get_memory_manager
from ai_companion.modules.schedules.context_generation import ScheduleContextGenerator
from ai_companion.settings import settings

async def memory_extraction_node(state: AICompanionState):
    """Extract and store important information from the last message."""
    return {}

async def system_prompt_node(state: AICompanionState):
    """system prompt for the user for input."""
   
    return {}
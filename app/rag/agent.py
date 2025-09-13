from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    trim_messages,
)
from langchain_openai import ChatOpenAI
import uuid
from typing import List, Dict, Any, Optional

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from api.query import agent_query

import uuid

from IPython.display import Image, display
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

from langchain_anthropic import ChatAnthropic
from .chain import RAGChain



memory = MemorySaver()
model = ChatOpenAI()


def prompt(state) -> list[BaseMessage]:
    """Given the agent state, return a list of messages for the chat model."""
    # We're using the message processor defined above.
    return trim_messages(
        state["messages"],
        token_counter=len,  # <-- len will simply count the number of messages rather than tokens
        max_tokens=5,  # <-- allow up to 5 messages.
        strategy="last",
        # Most chat models expect that chat history starts with either:
        # (1) a HumanMessage or
        # (2) a SystemMessage followed by a HumanMessage
        # start_on="human" makes sure we produce a valid chat history
        start_on="human",
        # Usually, we want to keep the SystemMessage
        # if it's present in the original history.
        # The SystemMessage has special instructions for the model.
        include_system=True,
        allow_partial=False,
    )


# Define a new graph
workflow = StateGraph(state_schema=MessagesState)

# Define a chat model
model = ChatOpenAI()


# Define the function that calls the model
def call_model(state: MessagesState):
    selected_messages = trim_messages(
        state["messages"],
        token_counter=len,  # <-- len will simply count the number of messages rather than tokens
        max_tokens=5,  # <-- allow up to 5 messages.
        strategy="last",
        # Most chat models expect that chat history starts with either:
        # (1) a HumanMessage or
        # (2) a SystemMessage followed by a HumanMessage
        # start_on="human" makes sure we produce a valid chat history
        start_on="human",
        # Usually, we want to keep the SystemMessage
        # if it's present in the original history.
        # The SystemMessage has special instructions for the model.
        include_system=True,
        allow_partial=False,
    )

    response = model.invoke(selected_messages)
    # We return a list, because this will get added to the existing list
    return {"messages": response}


# Define the two nodes we will cycle between
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)


# Adding memory is straight forward in langgraph!
memory = MemorySaver()

app = workflow.compile(
    checkpointer=memory
)


# The thread id is a unique key that identifies
# this particular conversation.
# We'll just generate a random uuid here.
thread_id = uuid.uuid4()
config = {"configurable": {"thread_id": thread_id}}

input_message = HumanMessage(content="hi! I'm bob")
for event in app.stream({"messages": [input_message]}, config, stream_mode="values"):
    event["messages"][-1].pretty_print()

# Here, let's confirm that the AI remembers our name!
config = {"configurable": {"thread_id": thread_id}}
input_message = HumanMessage(content="what was my name?")
for event in app.stream({"messages": [input_message]}, config, stream_mode="values"):
    event["messages"][-1].pretty_print()




class ConversationAgent:
    def __init__(self, api_key: str, collection_name: str = "PrimaryCollection"):
        """Initialize the conversation agent with RAG capabilities."""
        self.rag_chain = RAGChain(collection_name=collection_name)
        self.thread_id = str(uuid.uuid4())
        self.config = {"configurable": {"thread_id": self.thread_id}}
        self.message_history: List[Dict[str, Any]] = []

    async def send_message(self, message: str, user_id: int) -> Dict[str, Any]:
        """Send a message and get the AI's response using RAG."""
        # Add user message to history
        self.message_history.append({"role": "human", "content": message})
        
        # Get RAG response
        response = await self.rag_chain.generate_response(message, user_id)
        
        # Add AI response to history
        self.message_history.append({
            "role": "assistant", 
            "content": response["answer"],
            "source_documents": response["source_documents"]
        })
        
        return {
            "answer": response["answer"],
            "source_documents": response["source_documents"],
            "chat_history": self.message_history
        }

    def get_message_history(self) -> List[Dict[str, Any]]:
        """Get the current message history."""
        return self.message_history

    def clear_history(self):
        """Clear the message history and generate a new thread ID."""
        self.thread_id = str(uuid.uuid4())
        self.config = {"configurable": {"thread_id": self.thread_id}}
        self.message_history = []

# Example usage:
if __name__ == "__main__":
    import asyncio
    
    async def main():
        # Initialize agent
        agent = ConversationAgent(api_key="your-api-key")
        
        # Example conversation
        response = await agent.send_message("What can you tell me about the documents?", user_id=1)
        print(f"AI: {response['answer']}")
        print("\nSources:")
        for doc in response['source_documents']:
            print(f"- {doc['metadata'].get('source', 'Unknown')}")
        
        # Get message history
        history = agent.get_message_history()
        print("\nConversation History:")
        for msg in history:
            print(f"{msg['role']}: {msg['content']}")
    
    asyncio.run(main())
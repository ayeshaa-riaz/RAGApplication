from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# System message for the main QA chain
SYSTEM_PROMPT = """You are a helpful AI assistant that provides accurate and concise answers.
Follow these rules:
1. Use the provided context to answer questions
2. If you don't know the answer, say so
3. Keep answers concise and to the point
4. If someone introduces themselves, greet them warmly
5. Base your answers only on the provided context and chat history

Context: {context}"""

# Human message template for main QA
HUMAN_PROMPT = """Question: {question}

Chat History: {chat_history}"""

# Create the main QA prompt template
qa_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
    HumanMessagePromptTemplate.from_template(HUMAN_PROMPT)
])

# Question generator prompt for reformulating questions
QUESTION_GENERATOR_PROMPT = """Given the following conversation and a follow up question, 
rephrase the follow up question to be a standalone question that captures the full context.
If the question is already standalone, return it as is.

Chat History:
{chat_history}

Follow Up Input: {question}

Standalone question:"""

# Create the question generator prompt template
question_generator_prompt = ChatPromptTemplate.from_template(QUESTION_GENERATOR_PROMPT)

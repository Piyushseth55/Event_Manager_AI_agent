import sys
import os
from datetime import datetime
from dotenv import load_dotenv
from langsmith import Client
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START
from backend.schemas import InternalState
from utils.error_handling import create_tool_node_with_fallback
from agents.tools import (
    create_event,
    check_availability,
    reschedule_event,
    list_events,
    event_confirmation,
)
from langchain import hub

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
os.environ["GROQ_API_KEY"] = GROQ_API_KEY
os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
# Define tools
all_tools = [
    list_events,
    check_availability,
    create_event,
    event_confirmation,
    reschedule_event,
]

# Initialize LLM
llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.5,
    max_tokens=500,
)

# Load built-in ReAct prompt from LangChain hub

client = Client(api_key=LANGSMITH_API_KEY)
prompt = hub.pull("hwchase17/react")

# Create agent and executor using built-in ReAct logic
agent = create_react_agent(llm=llm, tools=all_tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=all_tools, verbose=True, handle_parsing_errors=True)

# Graph building is no longer needed since AgentExecutor handles logic
# You can still maintain state and memory via your own logic if required

def run_event_graph(user_input: str, user_id: str, credentials):
    try:
        # Inject input into AgentExecutor
        result = agent_executor.invoke({
            "input": user_input,
            "user_id": user_id,
            "credentials": credentials
        })
        return {"output": result["output"] if isinstance(result, dict) else result}
    except Exception as e:
        return {"output": f"An error occurred while processing your request: {str(e)}"}

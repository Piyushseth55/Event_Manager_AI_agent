import sys
import os
from dotenv import load_dotenv
from datetime import datetime
import json

# --- Path and Environment Setup ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

from agents.prompts import get_react_prompt
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, AnyMessage
from typing import List, TypedDict, Union, Optional, Annotated
from langgraph.checkpoint.memory import MemorySaver

# LangGraph imports
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# --- Tool Imports ---
from agents.tools import (
    create_event,
    check_availability,
    reschedule_event,
    list_events,
    event_confirmation,
)

# --- Define Graph State ---
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    user_id: str
    session_id: Optional[str] = None
    observation: Optional[str] = None
    final_answer: Optional[str] = None
    credentials: Optional[str] = None

# --- Define the Tools ---
memory = MemorySaver()
tools = [
    list_events,
    check_availability,
    create_event,
    event_confirmation,
    reschedule_event,
]

# --- Define the ChatGroq LLM ---
llm = ChatGroq(model="llama3-70b-8192", temperature=0)

# --- Define the LLM with Tool Calling Capabilities ---
llm_with_tools = llm.bind_tools(tools)

# --- Define Nodes ---

def call_llm(state: AgentState) -> AgentState:
    print("[call_llm] Invoking LLM with messages:")
    for msg in state['messages']:
        print(f"  - {type(msg).__name__}: {getattr(msg, 'content', '')}")

    response = llm_with_tools.invoke(state['messages'])

    print(f"[call_llm] LLM responded with message type: {type(response).__name__}")
    print(f"Content preview: {response.content[:100]}")

    return {"messages": [response]}


# --- Custom Tool Executor Node ---
def custom_tool_node(state: AgentState) -> AgentState:
    print("[custom_tool_node] Preparing to call tools...")
    last_message = state['messages'][-1]

    # Check if the LLM requested tool calls
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        print(f"[custom_tool_node] Tool calls detected: {last_message.tool_calls}")

        # Inject user_id and credentials into each tool call
        for call in last_message.tool_calls:
            args = call.get("args", {})
            args["user_id"] = state.get("user_id", "")
            args["credentials"] = state.get("credentials", "")
            call["args"] = args
            print(f"[custom_tool_node] Injected user_id and credentials: {args}")

        # Execute tool calls
        tool_executor = ToolNode(tools)
        new_state = tool_executor.invoke(state)
        return new_state

    print("[custom_tool_node] No tool calls found.")
    return state


# --- Conditional Edges ---
def decide_next_step(state: AgentState) -> str:
    last_message = state['messages'][-1]
    print(f"[decide_next_step] Checking last message type: {type(last_message).__name__}")
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        print("[decide_next_step] Tool calls found - moving to 'call_tool_node'")
        return "call_tool_node"
    else:
        print("[decide_next_step] No tool calls - moving to 'end'")
        return "end"


# --- Build the LangGraph ---
def create_calendar_agent_langgraph():
    workflow = StateGraph(AgentState)

    workflow.add_node("call_llm", call_llm)
    workflow.add_node("call_tool_node", custom_tool_node)  # Use our custom node

    workflow.set_entry_point("call_llm")

    workflow.add_conditional_edges(
        "call_llm",
        decide_next_step,
        {"call_tool_node": "call_tool_node", "end": END}
    )

    workflow.add_edge("call_tool_node", "call_llm")

    app = workflow.compile(checkpointer=memory)
    return app


# --- Run the graph for a user query ---
SYSTEM_PROMPT = get_react_prompt()

def run_event_graph(user_input: str, user_id: str, credentials: str) -> dict:
    print(f"[run_event_graph] Starting event graph with input: {user_input}")
    calendar_agent_graph = create_calendar_agent_langgraph()
    print("google : ", type(credentials))
    initial_state = {
        "messages": [
            HumanMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_input)
        ],
        "user_id": user_id,
        "credentials": credentials,  # Store the credentials
    }
    print(f"[run_event_graph] Initial state created with user_id: {user_id}")
    config = {"configurable" : {"thread_id" : user_id}}
    final_state = calendar_agent_graph.invoke(initial_state, config = config)

    print("[run_event_graph] Graph invocation complete.")
    last_ai_message = None
    for msg in reversed(final_state.get("messages", [])):
        if isinstance(msg, AIMessage):
            last_ai_message = msg
            break

    if last_ai_message:
        print(f"[run_event_graph] Final AI response: {last_ai_message.content[:150]}")
    else:
        print("[run_event_graph] No AIMessage found in final messages.")

    return {
        "response": last_ai_message.content if last_ai_message else "No final answer from the agent.",
        "state": final_state,
    }

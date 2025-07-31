#################################################################################
#                           Event Manager Ai Agent                              #
#               Using langchain, langgraph, google-Oauth2, streamlit            #
#                           by Piyush Kumar Seth                                #
##################################################################################


##############################################################
#   IMPORTING LIBRARIES
##############################################################

from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from backend.schemas import AgentState
import os
from dotenv import load_dotenv

##############################################################
#   ENVIRNMENT SETUP
##############################################################
load_dotenv()
memory = MemorySaver()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = GROQ_API_KEY


##############################################################
#   TOOLS IMPORT AND DEFINING
##############################################################

from backend.agents.tools import (
    create_event,
    check_availability,
    reschedule_event,
    list_events,
    event_confirmation,
    delete_event,
    get_holidays,
)

tools = [
    list_events,
    check_availability,
    create_event,
    event_confirmation,
    reschedule_event,
    delete_event,
    get_holidays,
]


##############################################################
#   DEFINING THE LLM FROM GROQ
##############################################################

llm = ChatGroq(model="llama3-70b-8192", temperature=1)

##############################################################
#   BINDING THE TOOLS WITH LLM
##############################################################

llm_with_tools = llm.bind_tools(tools)



##############################################################
#                   DEFINING THE NODES


##############################################################
#   NODE FOR CALLING LLM 
##############################################################

def call_llm(state: AgentState) -> AgentState:
    print("[call_llm] Invoking LLM with messages:")
    for msg in state['messages']:
        print(f"  - {type(msg).__name__}: {getattr(msg, 'content', '')}")

    response = llm_with_tools.invoke(state['messages'])

    print(f"[call_llm] LLM responded with message type: {type(response).__name__}")
    print(f"Content preview: {response.content[:100]}")

    return {"messages": [response]}


##############################################################
#   NODE FOR TOOL EXECUTOR
##############################################################

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


##############################################################
#   EDGE FOR DECIDING NODE (CONDITIONAL EDGE)
##############################################################

def decide_next_step(state: AgentState) -> str:
    last_message = state['messages'][-1]
    print(f"[decide_next_step] Checking last message type: {type(last_message).__name__}")
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        print("[decide_next_step] Tool calls found - moving to 'call_tool_node'")
        return "call_tool_node"
    else:
        print("[decide_next_step] No tool calls - moving to 'end'")
        return "end"


##############################################################
#   BUILDING THE GRAPH
##############################################################

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


#################################################################################
#                           Event Manager Ai Agent                              #
#               Using langchain, langgraph, google-Oauth2, streamlit            #
#                           by Piyush Kumar Seth                                #
##################################################################################


##############################################################
#   IMPORTING LIBRARIES
##############################################################

from agents.prompts import get_react_prompt
from langchain_core.messages import HumanMessage, AIMessage
from langgraph_engine.memory import create_calendar_agent_langgraph



##############################################################
#   LOAD THE PROMPT
##############################################################

SYSTEM_PROMPT = get_react_prompt()


##############################################################
#   RUN THE GRAPH FOR USER QUERY
##############################################################

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


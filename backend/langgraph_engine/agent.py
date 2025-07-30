# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from langchain_core.messages import HumanMessage 
# from langchain_core.runnables import Runnable , RunnableConfig
# from backend.schemas import InternalState
# from langchain.tools import tool
# from backend.schemas import CheckConflict,EventConfirmationInput, CreateEventInput, RescheduleEventInput,EventData
# import json
# from agents.tools import (
#     create_event,
#     check_availability,
#     reschedule_event,
#     list_events,
#     event_confirmation,
# )





# def parse_llm_output(llm_output: str, credentials: str, user_id: str):
#     try:
#         llm_json_output = json.loads(llm_output)
#         tool_name = llm_json_output["action"]
#         tool_input = llm_json_output["action_input"]
        
#         # For tools that use CheckConflict schema
#         if tool_name in ["list_events", "check_availability"]:
#             final_input = CheckConflict(
#                 start=tool_input.get("start"),
#                 end=tool_input.get("end"),
#                 user_id=user_id,
#                 credentials=credentials
#             )
#             return tool_name, final_input
            
#         # For create_event tool
#         elif tool_name == "create_event":
#             final_input = CreateEventInput(
#                 summary=tool_input["summary"],
#                 start=tool_input["start"],
#                 end=tool_input["end"],
#                 user_id=user_id,
#                 credentials=credentials
#             )
#             return tool_name, final_input
            
#         # For event_confirmation tool
#         elif tool_name == "event_confirmation":
#             final_input = EventConfirmationInput(
#                 confirm=tool_input["confirm"],
#                 event=EventData(
#                     summary=tool_input["summary"],
#                     start=tool_input["start"],
#                     end=tool_input["end"]
#                 )
#             )
#             return tool_name, final_input
            
#         # For reschedule_event tool
#         elif tool_name == "reschedule_event":
#             final_input = RescheduleEventInput(
#                 confirm=tool_input["confirm"],
#                 event_id=tool_input["event_id"],
#                 start=tool_input["start"],
#                 end=tool_input["end"],
#                 user_id=user_id,
#                 credentials=credentials
#             )
#             return tool_name, final_input
            
#     except json.JSONDecodeError:
#         print("Failed to parse JSON")
#         return None, None
#     except KeyError as e:
#         print(f"Missing required field in tool input: {e}")
#         return None, None
    
# class Assistant:
#     def __init__(self, runnable: Runnable):
#         self.runnable = runnable  # Yeh runnable already bind_tools se tools ke saath judaa hoga

#     def __call__(self, state: InternalState, config: RunnableConfig):
#         while True:
#             configuration = config.get("configurable", {})
#             credentials = configuration.get("credentials", None)
#             prompt_input = {
#                 "message" : configuration.get("messages", ""),
#                 "user_id" : configuration.get("user_id", None),
#                 "credentials" :  configuration.get("credentials", None),
#                 "observation" : configuration.get("observation", None)
#             }
#             # State me user_info update karo agar passenger_id available hai
#             if credentials:
#                 state = {**state, "credentials": credentials}

#             # Runnable ko invoke karo, jo ki LLM + tool call dono handle karega
#             result = self.runnable.invoke(state)

#             # Agar koi tool call nahi aaya aur content empty hai, toh user ko real output dene ke liye prompt karo
#             if not getattr(result, "tool_calls", None) and (
#                 not getattr(result, "content", None)
#                 or (isinstance(result.content, list) and not result.content[0].get("text"))
#             ):
#                 messages = state.get("messages", []) + [("user", "Respond with a real output.")]
#                 state = {**state, "messages": messages}
#             else:
#                 break

#         # Final response me messages return karo
#         return {"messages": result}

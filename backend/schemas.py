#################################################################################
#                           Event Manager Ai Agent                              #
#               Using langchain, langgraph, google-Oauth2, streamlit            #
#                           by Piyush Kumar Seth                                #
##################################################################################


##############################################################
#   IMPORTING LIBRARIES
##############################################################

from pydantic import BaseModel, Field
from typing import Optional, List, Literal, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict



class UserInput(BaseModel) :
    query : str = Field (..., examples=["Can i Schedule a meeting with Mohan this Friday at 1 pm?"])
    
class AgentOutput(BaseModel) : 
    output : str = Field(..., examples=["Yes! that time is available. Can i schedule it ?"])
    isAvailable : Optional[bool] = None
    isConflict : Optional[bool] = None
    StartDate : Optional[str] = None
    EndDate : Optional[str] = None
    
    
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    user_id: str
    session_id: Optional[str] = None
    observation: Optional[str] = None
    final_answer: Optional[str] = None
    credentials: Optional[str] = None
 
class GetEventOutput(BaseModel) :
    data : List[dict]
    message : str
    success : bool
    
       
class EventData(BaseModel) : 
    summary : str = Field(..., examples=["Meeting with Mohan"])
    start : str = Field(..., examples=["2025-06-29T13:00:00+05:30"])
    end : str = Field(..., examples=["2025-06-29T13:00:00+05:30"])
    
class CheckConflict(BaseModel) : 
    start : Optional[str] = None
    end : Optional[str] = None
    user_id : Optional[str] = None
    credentials : Optional[str] = None
    
class ConflictResponse(BaseModel) : 
    isConflict : bool
    isAvailable : bool
    conflict_with : List[str]
    message : str
    
class CreateEventInput(BaseModel) :
    summary : str
    start : str
    end : str
    user_id : Optional[str] = None
    credentials : Optional[str] = None
    
class EventConfirmationInput(BaseModel) :
    confirm : Literal["yes", "no"]
    event : EventData
    user_id : Optional[str] = None
    credentials : Optional[str] = None
    
    
    
class EventConfirmation(BaseModel) : 
    summary : str
    start : str
    end : str
    message : str
    success : bool
    
class RescheduleEventInput(BaseModel) :
    confirm : Literal["yes", "no"]
    event_id : str
    summary : Optional[str]
    start : str
    end : str
    user_id : Optional[str] = None
    credentials : Optional[str] = None
    
    
class RescheduleConfirmation(BaseModel) :
    summary : str
    start : str
    end : str
    message : str
    success : bool
    
    
class DeleteEventInput(BaseModel) :
    confirm : Literal["yes", "no"]
    event_id : str
    start : str
    end : str
    user_id : str
    credentials : Optional[str] = None
    
class DeleteConfirmation(BaseModel) :
    success : bool
    message : str
    event_id : str
    
    


    
      


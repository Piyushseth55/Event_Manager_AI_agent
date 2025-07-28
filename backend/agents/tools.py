#################################################################################
#                           Event Manager Ai Agent                              #
#               Using langchain, langgraph, google-Oauth2, streamlit            #
#                           by Piyush Kumar Seth                                #
##################################################################################



##############################################################
#   IMPORTING LIBRARIES
##############################################################

from langchain.tools import tool
from utils.Agent_help import get_calendar_service, get_events
from backend.schemas import CheckConflict, ConflictResponse, EventConfirmationInput, EventConfirmation, CreateEventInput, RescheduleEventInput, RescheduleConfirmation, GetEventOutput
from typing import Literal, Optional


##############################################################
#   TOOL FOR GETTING EVENTS 
##############################################################

@tool("list_events", args_schema=CheckConflict)
def list_events(start : str, end : str, user_id : Optional[str], credentials : Optional[str]) -> GetEventOutput:
    """
    Use this tool to get events list from the Google Calendar in the specified time range.
    
    Input: 
        - start: Start time in ISO 8601 format (e.g., "2025-06-29T13:00:00+05:30")
        - end: End time in ISO 8601 format
        - user_id: User ID of string
        - credentials: String of Google credentials
    
    Returns:
        - data: List of dictionary containing event details. Dictionary contains these fields:
            - summary: Summary of the event.
            - start: Start time in ISO 8601 format
            - end: End time in ISO 8601 format
            - id: Event ID
        - message: Description of the availability or error occurred.
        - success: True if events were successfully retrieved (even if empty).

    Call this tool when the user needs all existing event details.
    """
    
    try:
        service = get_calendar_service(user_id, credentials)
        events = get_events(service=service, start=start, end=end)
        
        if not events.get('success'):
            # If get_events itself indicates failure (e.g., auth error, API error)
            return GetEventOutput(
                data=[],
                message=events.get('message', "An error occurred while fetching events."),
                success=False
            )
        
        # If success is True, but data is empty, it means no events were found in the range
        if not events.get('data'):
            return GetEventOutput(
                data=[],
                message="There are no events available in the given specified time.",
                success=True # Successfully checked, no events found
            )
        else:
            return GetEventOutput(
                data=events.get('data'),
                message="These are the events in the given specified time.",
                success=True
            )
            
    except Exception as e:
        print(f"Exception in list_events: {str(e)}") 
        return GetEventOutput(
            data=[],
            message=f"There was an error listing events: {str(e)}",
            success=False
        )
        
    
##############################################################
#   TOOL FOR CHECK AVAILABILITY OF TIME IN SPECIFIC TIME
##############################################################

@tool("check_availability", args_schema=CheckConflict)
def check_availability(start : str, end : str,  user_id : Optional[str], credentials : Optional[str]) -> ConflictResponse:
    """
    Use this tool to check if the specified time range is free on the user's Google Calendar.

    Input: 
        - start: Start time in ISO 8601 format (e.g., "2025-06-29T13:00:00+05:30")
        - end: End time in ISO 8601 format
        - user_id: User ID
        - credentials: Google credentials dict

    Returns: 
        - isAvailable: True if the time is free
        - isConflict: True if there is an event during that time
        - conflict_with: List of overlapping event summaries, if any
        - message: Description of the availability or conflict status

    Call this when the user asks to check or schedule an event at a specific time.
    """
    
    try:
        service = get_calendar_service(user_id, credentials)
        events = get_events(service=service, start=start, end=end)
        
        if not events.get('success'):
            # If get_events itself indicates an error (e.g., auth issue)
            return ConflictResponse(
                isConflict=True, # Treat as conflict because we can't verify availability
                isAvailable=False,
                conflict_with=["N/A"],
                message=events.get('message', "An error occurred while checking availability.")
            )
        
        event_list = events.get('data', [])
        
        if not event_list: # No events found means it's available
            return ConflictResponse(
                isConflict=False,
                isAvailable=True,
                conflict_with=[], # Empty list for no conflicts
                message="This time slot is Available."
            )
        else: # Events found, so there's a conflict
            conflict_summaries = []
            for event in event_list:
                summary = event.get('summary', 'No Summary')
                start_time_str = event.get('start', {}).get('dateTime', event.get('start', {}).get('date'))
                end_time_str = event.get('end', {}).get('dateTime', event.get('end', {}).get('date'))
                conflict_summaries.append(f"{summary} (Starts: {start_time_str}, Ends: {end_time_str})")
            
            return ConflictResponse(
                isConflict=True,
                isAvailable=False,
                conflict_with=conflict_summaries,
                message="There are some existing events in the given time range!"
            )
            
    except Exception as e:
        print(f"Exception in check_availability: {str(e)}")
        return ConflictResponse(
            isConflict=True,
            isAvailable=False,
            conflict_with=["N/A"],
            message=f"Something went wrong while checking availability: {str(e)}"
        )


##############################################################
#   TOOL FOR CREATING A EVENT IN CALENDAR
##############################################################

@tool("create_event", args_schema=CreateEventInput)
def create_event(summary : str, start : str, end : str,  user_id : Optional[str], credentials : Optional[str]) -> EventConfirmation:
    """
    Use this tool to create a new event in the user's Google Calendar.

    Input: 
        - summary: Title or description of the event
        - start: Start time in ISO 8601 format
        - end: End time in ISO 8601 format
        - user_id: User ID
        - credentials: Google credentials string

    Returns: 
        - summary, start, end: Event details
        - message: Status message
        - success: True if event creation was successful

    Use this after the user confirms they want to schedule a specific event.
    """
    
    try:
        service = get_calendar_service(user_id=user_id, credentials=credentials)
        event_body = {
            "summary": summary,
            "start": {
                "dateTime": start,
                "timeZone": "Asia/Kolkata", 
            },
            "end": {
                "dateTime": end,
                "timeZone": "Asia/Kolkata", 
            },
        }
        created_event = service.events().insert(calendarId='primary', body=event_body).execute()
        return EventConfirmation(
            summary=summary,
            start=start,
            end=end,
            message="Event created successfully.",
            success=True
        )
        
    except Exception as e:
        print(f"Exception in create_event: {str(e)}")
        return EventConfirmation(
            summary=summary,
            start=start,
            end=end,
            message=f"Event couldn't be created! Something went wrong: {str(e)}",
            success=False
        )
    
 
##############################################################
#   TOOL FOR FINAL CONFIRMAION BEFORE CREATING A EVENT
##############################################################   

@tool("event_confirmation", args_schema=EventConfirmationInput)
def event_confirmation(confirm : Literal["yes", "no"], summary : str, start : str, end : str,  user_id : Optional[str], credentials : Optional[str]) -> EventConfirmation:
    """
    Use this tool to confirm and create a suggested event only if the user says "yes".

    Input: 
        - confirm: Literal string "yes" or "no"
        - summary: Title or description of the event
        - start: Start time in ISO 8601 format
        - end: End time in ISO 8601 format
        - user_id: User ID (MUST BE PROVIDED BY LLM)
        - credentials: Google credentials string (MUST BE PROVIDED BY LLM)

    Returns: 
        - EventConfirmation with success flag and message

    This should be used when a user confirms their intent to schedule an event after availability is suggested.
    """
    
    if confirm == "yes":
        # Pass user_id and credentials from EventConfirmationInput to CreateEventInput
        return create_event(CreateEventInput(
            summary=summary,
            start=start,
            end=end,
            user_id=user_id, 
            credentials=credentials 
        ))
    
    else:
        return EventConfirmation(
            summary=summary,
            start=start,
            end=end,
            message="Event not created. If you have any other query, you may ask.",
            success=False
        )


##############################################################
#   TOOL FOR RESCHEDULE AN EVENT
##############################################################

@tool("reschedule_event", args_schema=RescheduleEventInput)
def reschedule_event(confirm : Literal["yes", "no"],event_id : str, summary : Optional[str], start : str, end : str,  user_id : Optional[str], credentials : Optional[str]) -> RescheduleConfirmation: 
    """
    Use this tool to reschedule an existing Google Calendar event by updating its start and end times.
    
    Input: 
        - confirm: Literal string "yes" or "no" (tool should only proceed if "yes")
        - event_id: A string containing event ID of the event.
        - summary: Title or description of the event
        - start: New start time in ISO 8601 format
        - end: New end time in ISO 8601 format
        - user_id: User ID
        - credentials: Google credentials string
        
    Returns: 
        - summary, start, end: Event details
        - message: Status message
        - success: True if event rescheduling was successful
        
    This tool should be used when a user confirms their intent to reschedule an event with specific event details.
    """
    
    if confirm == "no": # Handle "no" confirmation upfront
        return RescheduleConfirmation(
            summary="N/A", # Cannot provide actual summary if not confirmed
            start=start,
            end=end,
            message="Event not rescheduled as per your cancellation.",
            success=False
        )

    try: 
        service = get_calendar_service(user_id=user_id, credentials=credentials)
        
        # Fetch the event to get its current details, especially summary
        event = service.events().get(calendarId='primary', eventId=event_id).execute()
        
        # Update start and end times
        event['start']['dateTime'] = start
        event['end']['dateTime'] = end
        update_event = service.events().update(
            calendarId='primary',
            eventId=event_id,
            body=event
        ).execute()
        
        return RescheduleConfirmation(
            summary=update_event.get('summary', 'Unknown Event'),
            start=start,
            end=end,
            message=f"Event '{update_event.get('summary', 'Unknown')}' rescheduled successfully.",
            success=True
        )
        
    except Exception as e:
        print(f"Exception in reschedule_event: {str(e)}")
        # Provide summary from input if actual event summary couldn't be fetched
        # Corrected the typo in the message
        return RescheduleConfirmation(
            summary=summary if len(summary) else "Unknown Event", # Fallback for summary
            start=start,
            end=end,
            message=f"Event couldn't be rescheduled! Something went wrong: {str(e)}",
            success=False
        )
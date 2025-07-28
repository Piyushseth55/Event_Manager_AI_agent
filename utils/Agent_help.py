from googleapiclient.discovery import build
from agents.auth import get_calendar_credentials



def get_calendar_service(user_id : str, credentials : str) :
    print("ppppp")
    credentials = get_calendar_credentials(user_id, credentials)
    print("sssss")
    service = build("calendar", "v3", credentials=credentials)
    print("llllll")
    return service


def get_events(service, start : str, end : str) :
    try :
        if service:
            response = service.events().list(
                calendarId ='primary',
                timeMin = start,
                timeMax = end,
                singleEvents = True,
                orderBy = 'startTime'
            ).execute()
            
            events = response.get('items', [])
            if not events :
                return {
                        "success" : True,
                        "data" : [],
                        "message" : "Available"
                    }
            
            summaries = [
            {
                "summary": event.get("summary", "No Title"),
                "start": event.get("start", {}).get("dateTime"),
                "end": event.get("end", {}).get("dateTime"),
                "id": event.get("id")
                }
                for event in events
            ]
            return {
                "success" : True,
                "data" : summaries,
                "message" : "There are existing events !"
            }
        else :
            return {
                    "success"  : True,
                    "data" : [],
                    "meesage" : "service Object is null"
                } 
    except Exception as e:
        print("Exception : " +str(e))
        return {
            "success" : False,
            "data" : [],
            "message" : f"Something is wrong  : {str(e)}"
            }
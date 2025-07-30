#################################################################################
#                           Event Manager Ai Agent                              #
#               Using langchain, langgraph, google-Oauth2, streamlit            #
#                           by Piyush Kumar Seth                                #
##################################################################################



##############################################################
#   IMPORTING LIBRARIES
##############################################################
import os
import base64
import tempfile
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from backend.agents.auth import initiate_google_login, fetch_user_credentials, get_calendar_credentials
from google_auth_oauthlib.flow import Flow
from backend.langgraph_engine.dispatcher import run_event_graph
from urllib.parse import quote
from dotenv import load_dotenv
load_dotenv()


##############################################################
#   DEFINING SOME CONSTANT AND SCOPES
##############################################################

b64_creds = os.environ.get("GOOGLE_OAUTH_CLIENT_B64")
if not b64_creds:
    raise Exception("Missing GOOGLE_OAUTH_CLIENT_B64 environment variable")

decoded = base64.b64decode(b64_creds).decode("utf-8")
with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w") as temp_file:
    temp_file.write(decoded)
    temp_file_path = temp_file.name

FRONTEND_URL = "https://eventmanageraiagent.streamlit.app"
REDIRECT_URI = "https://event-manager-ai-agent.onrender.com/oauth2callback"
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid"
]



##############################################################
#   DEFINING ROUTER
##############################################################

router = APIRouter()


##############################################################
#   ROUTE FOR LOGIN
##############################################################

@router.get("/login")
async def login() :
    os.environ["OAUTH_INSECURE_TRANSPORT"] = "1"
    flow = Flow.from_client_secrets_file(
        temp_file_path,
        scopes=SCOPES,
        redirect_uri = REDIRECT_URI,
    )
    auth_url, _ = flow.authorization_url(
        access_type = 'offline',
        prompt = 'consent',
        include_granted_scopes = 'true'
    )
    return RedirectResponse(url = auth_url)


##############################################################
#   ROUTE FOR GOOGLE OAUTH2
##############################################################

@router.get('/oauth2callback')
async def oauth2_callback(request : Request) :
    code = request.query_params.get("code")
    if not code : 
        raise HTTPException(status_code=400, detail="Missing code from google callback")
    
    try :
        credentials, user_email = fetch_user_credentials(code)
        
        cred_json = credentials.to_json()
        encoded_credentials = quote(cred_json)  # safely URL-encode the JSON string
        redirect_url = f"{FRONTEND_URL}?page=chatbot&email={quote(user_email)}&credentials={encoded_credentials}"
        return RedirectResponse(url=redirect_url)
    except Exception as e :
        return HTMLResponse(f"<h3>Authentication Failed</h3><p>{str(e)}</p>", status_code = 500)
    

##############################################################
#   ROUTE FOR CHAT
##############################################################

@router.post("/chat/ask")
async def ask_chat(input: dict):
    user_input = input.get("input")
    user_id = input.get("user_id")
    credentials = input.get("credentials")
    if not user_input:
        raise HTTPException(status_code=400, detail="Missing user input")

    result = run_event_graph(user_input, user_id, credentials)
    return {"result": result.get("response") or result.get("output")}

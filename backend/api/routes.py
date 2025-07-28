from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from agents.auth import initiate_google_login, fetch_user_credentials, get_calendar_credentials
from starlette.responses import JSONResponse
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from langgraph_engine.memory import run_event_graph
from pydantic import BaseModel
import os
import json
from urllib.parse import quote


FRONTEND_URL = "http://localhost:8501/"
CLIENT_SECRETS_FILE = "E:\Event_Manager_AI_agent\google_credentials\credentials.json"
REDIRECT_URI = "http://127.0.0.1:8000/oauth2callback"
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid"
]


class ChatRequest(BaseModel):
    user_id: str
    input: str

router = APIRouter()

@router.get("/login")
async def login() :
    os.environ["OAUTH_INSECURE_TRANSPORT"] = "1"
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri = REDIRECT_URI,
    )
    auth_url, _ = flow.authorization_url(
        access_type = 'offline',
        prompt = 'consent',
        include_granted_scopes = 'true'
    )
    return RedirectResponse(url = auth_url)



@router.get('/oauth2callback')
async def oauth2_callback(request : Request) :
    code = request.query_params.get("code")
    if not code : 
        raise HTTPException(status_code=400, detail="Missing code from google callback")
    
    try :
        credentials, user_email = fetch_user_credentials(code)
        
        cred_json = credentials.to_json()
        encoded_credentials = quote(cred_json)  # safely URL-encode the JSON string
        redirect_url = f"{FRONTEND_URL}chatbot/?email={quote(user_email)}&credentials={encoded_credentials}"
        return RedirectResponse(url=redirect_url)
    except Exception as e :
        return HTMLResponse(f"<h3>Authentication Failed</h3><p>{str(e)}</p>", status_code = 500)
    

@router.post("/chat/ask")
async def ask_chat(input: dict):
    user_input = input.get("input")
    user_id = input.get("user_id")
    credentials = input.get("credentials")
    if not user_input:
        raise HTTPException(status_code=400, detail="Missing user input")

    result = run_event_graph(user_input, user_id, credentials)
    return {"result": result.get("response") or result.get("output")}

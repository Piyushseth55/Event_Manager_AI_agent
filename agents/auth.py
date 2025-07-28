import os
import json
import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid"
]

CLIENT_SECRETS_FILE = "E:\Event_Manager_AI_agent\google_credentials\credentials.json"
REDIRECT_URI = "http://127.0.0.1:8000/oauth2callback"


def initiate_google_login() :
    os.environ["OAUTH_INSECURE_TRANSPORT"] = "1"
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri = REDIRECT_URI,
    )
    
    return flow
    
    
def fetch_user_credentials(code : str) :
    
    flow = initiate_google_login()
    if not flow : 
        st.error("OAuth flow not initialized")
        st.stop()
   
    
    flow.fetch_token(code = code)
    credentials = flow.credentials
    
    
    try:
        user_info_service = build("oauth2", "v2", credentials=credentials)
        user_info = user_info_service.userinfo().get().execute()
    except Exception as e:
        print("Error while fetching user info:", e)
        raise

    
    
    return credentials,user_info["email"]
        

def get_calendar_credentials(user_id : str, credentials : str) -> Credentials:
    
    if not credentials :
        raise ValueError("User not Authenticated")
    
    cred_info = json.loads(credentials)
    credentials = Credentials.from_authorized_user_info(cred_info, SCOPES)
    if credentials.expired and credentials.refresh_token : 
        credentials.refresh(Request())
        
    return credentials



def logout() : 
    keys_to_clear = ["credentials", "user_email", "auth_flow", "auth_state"]
    for key in keys_to_clear :
        st.session_state.pop(key, None)
    st.experimental_rerun()
    
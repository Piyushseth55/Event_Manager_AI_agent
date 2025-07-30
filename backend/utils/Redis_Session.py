#################################################################################
#                           Event Manager Ai Agent                              #
#               Using langchain, langgraph, google-Oauth2, streamlit            #
#                           by Piyush Kumar Seth                                #
##################################################################################



##############################################################
#   IMPORTING LIBRARIES
##############################################################

import os
import json
from upstash_redis import Redis
from dotenv import load_dotenv
load_dotenv()


##############################################################
#   SETTING ENVIRNMENTS
##############################################################

REDIS_URL = os.getenv("UPSTASH_REDIS_REST_URL")
REDIS_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")


redis_session = Redis(url=REDIS_URL, token=REDIS_TOKEN)


##############################################################
#   DEFINING FUNCTIONS TO ACCESS REDIS DATABASE
##############################################################

def save_session(session_id : str, session_data : dict, ttl : int = 1800) :
    redis_session.setex(session_id, ttl, json.dumps(session_data))
    
    
def get_session(session_id : str) :
    data = redis_session.get(session_id)
    if data : 
        return json.loads(data)
    return None


def delete_session(session_id : str) :
    redis_session.delete(session_id)
    

def refresh_session_ttl(session_id: str, ttl: int = 1800):
    if redis_session.exists(session_id):
        redis_session.expire(session_id, ttl)
        return True
    return False
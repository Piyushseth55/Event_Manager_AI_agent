#################################################################################
#                           Event Manager Ai Agent                              #
#               Using langchain, langgraph, google-Oauth2, streamlit            #
#                           by Piyush Kumar Seth                                #
##################################################################################


##############################################################
#   IMPORTING LIBRARIES
##############################################################

from fastapi import FastAPI
from backend.api.routes import router
from fastapi.middleware.cors import CORSMiddleware



##############################################################
#   CREATING A APP
##############################################################

app = FastAPI(title="AI Event Manager")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)
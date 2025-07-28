#################################################################################
#                           Event Manager Ai Agent                              #
#               Using langchain, langgraph, google-Oauth2, streamlit            #
#                           by Piyush Kumar Seth                                #
##################################################################################


##############################################################
#   IMPORTING LIBRARIES
##############################################################

import streamlit as st


##############################################################
#   FRONT PAGE OF WEBSITE
##############################################################

st.set_page_config(page_title="Login", layout="centered")

BACKEND_URL = "http://localhost:8000"

##############################################################
#   HANDLE OAUTH REDIRECT
##############################################################
query_param = st.query_params
email_param = query_param.get("email", [None])[0]

if email_param:
    st.session_state["user_email"] = email_param
    st.query_params.clear()  # clear email param
    st.success("✅ Logged in successfully!")

    # ⏩ Automatically go to chatbot page
    st.switch_page("Chatbot.py")

st.title("🔐 Sign in to AI Calendar Assistant")

if "user_email" not in st.session_state:
    if st.button("🔑 Sign in with Google", use_container_width=True):
        login_url = f"{BACKEND_URL}/login"
        st.markdown(
            f"""
            <meta http-equiv="refresh" content="0;URL='{login_url}'" />
            """,
            unsafe_allow_html=True
        )

    st.stop()
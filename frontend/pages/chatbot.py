# frontend/pages/chatbot.py
import streamlit as st
import requests
import urllib.parse

API_URL = "http://127.0.0.1:8000/chat/ask"  # Change if deployed elsewhere



def start_chatbot(user_id: str, credentials):
    st.subheader("🤖 Your AI Calendar Assistant")
    print("This is userid : " + user_id)
    print(credentials)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input("What would you like to schedule?")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        for msg in st.session_state.chat_history:
            st.chat_message(msg["role"]).write(msg["content"])

        with st.spinner("Thinking..."):
            try:
                res = requests.post(API_URL, json={
                    "user_id": user_id,
                    "input": user_input,
                    "credentials" : credentials
                })
                if res.status_code == 200:
                    result = res.json()["result"]
                    st.chat_message("assistant").write(result)
                    st.session_state.chat_history.append({"role": "assistant", "content": result})
                else:
                    st.error(f"Error: {res.text}")
            except Exception as e:
                st.error(f"Request failed: {str(e)}")



query_params = st.query_params
raw_email = query_params.get("email", [None])
user_email = urllib.parse.unquote(raw_email) if raw_email else None

if user_email:
    st.session_state["user_email"] = user_email

user_id = st.session_state.get("user_email", "default_user")
credentials = query_params.get("credentials", [None])

start_chatbot(user_id, credentials)
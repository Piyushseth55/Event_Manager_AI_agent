import streamlit as st
import requests
import urllib.parse

API_URL = "https://event-manager-ai-agent.onrender.com/chat/ask"

# ===== Custom CSS Styling (only icon color changed) =====
st.markdown("""
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
        .main {
            padding-top: 0rem;
        }
         .custom-header {
            background-color: #1A1A1A;
            color: #00FFC0;
            padding: 1rem 2rem;
            font-size: 1.5rem;
            font-weight: bold;
            border-bottom: 1px solid #333;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .profile-badge-icon {
            font-size: 2rem; /* Icon size */
            color: #00FFC0; /* Teal accent */
            padding: 0.3rem;
            cursor: default;
            user-select: none;
        }
        .hello-text {
            font-size: 1rem;
            color: #00FFC0;      /* White text */
            margin-right: 0.5rem;
            vertical-align: middle;
        }
        
        .chat-msg {
            margin-bottom: 1.5rem;
            padding: 0.8rem 1.2rem;
            border-radius: 1rem;
            background-color: #1e1e1e;
            color: white;
            display: flex;
            gap: 0.6rem;
        }
        .user-msg {
            background-color: #222;
            color: #00FFC0;
        }
        .assistant-msg {
            background-color: #141414;
            color: #87CEFA;
        }
        .profile-badge {
            text-align: right;
            font-size: 0.85rem;
            color: #999;
            margin-right: 2rem;
            margin-top: -1rem;
        }
        .icon {
            font-size: 1.2rem;
            margin-top: 0.1rem;
        }
        .user-icon {
            color: #90EE90;
        }
        .assistant-icon {
            color: #87CEFA;
        }
        

    </style>
    """,
    unsafe_allow_html=True
)

# ===== Chatbot Main Logic =====
def start_chatbot(user_id: str, credentials):
    st.markdown(
        """
        <div class="custom-header">
            <div>Your AI Calendar Assistant</div>
            <div class="profile-badge-icon" title="Hello!"><span class="hello-text">Hello!</span><i class="fa fa-user-circle"></i></div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-msg user-msg"><div class="icon user-icon"><i class="fa fa-user-circle" style="color:#00FFC0;"></i></div><div>{msg["content"]}</div></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="chat-msg assistant-msg">'
                f'<div class="icon assistant-icon"><i class="fa fa-robot" style="color:#00FFC0;"></i></div>'
                f'<div>{msg["content"]}</div></div>',
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)  # close chat container

    # Chat input appears at the bottom after all messages
    user_input = st.chat_input("What would you like to schedule?")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.spinner("Thinking..."):
            try:
                res = requests.post(API_URL, json={
                    "user_id": user_id,
                    "input": user_input,
                    "credentials": credentials
                })
                if res.status_code == 200:
                    result = res.json()["result"]
                    st.session_state.chat_history.append({"role": "assistant", "content": result})
                    st.rerun()
                else:
                    st.error(f"Error: {res.text}")
            except Exception as e:
                st.error(f"Request failed: {str(e)}")

# ===== URL Handling =====
query_params = st.query_params
raw_email = query_params.get("email", [None])
user_email = urllib.parse.unquote(raw_email) if raw_email else None

if user_email:
    st.session_state["user_email"] = user_email

user_id = st.session_state.get("user_email", "default_user")
credentials = query_params.get("credentials", [None])

# ===== Start Chatbot =====
start_chatbot(user_id, credentials)

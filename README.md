# 🧠 Event Manager AI Agent

An AI-powered calendar assistant built with **LangGraph**, **LangChain**, **FastAPI**, and **Google Calendar API** to help users manage events with natural language.

## 🚀 Features

- ✅ Natural language interface for event scheduling
- 📆 Full Google Calendar integration (create, fetch, update, delete events)
- 🔁 Reschedule & cancel events with confirmation
- 🗓️ Holiday extraction via Google Public Holiday Calendars
- 🧠 Memory-enabled agent (via LangGraph)
- 🛠️ Backend API using FastAPI
- 🔐 OAuth 2.0 for Google login (token persistence)
- 📥 Redis-based session management using Upstash Redis


## 🧩 Tech Stack

- **LangGraph + LangChain**
- **FastAPI**
- **Google Calendar API**
- **Pydantic**
- **Python 3.10+**
- **Redis- using Upstash**

## 🔧 Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/Piyushseth55/Event_Manager_AI_agent.git
   cd Event_Manager_AI_agent

2. **Create virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows

3. **Install dependencies**
    ```
    pip install -r requirements.txt
    ```

## 📌 Example Prompts
```
“Create a meeting with Alice tomorrow at 3pm”
```
```
“Show my events for next week”
```
```
“Reschedule my demo with John to Friday 10am”
```

## 📄 License

 **MIT License © 2025 Piyush Kumar Seth**



---

Let me know if you'd like to include a **frontend section**, **deployment guide**, or **Postman collection** reference too.

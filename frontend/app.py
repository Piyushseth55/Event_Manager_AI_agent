# landing_page.py

import streamlit as st
from pathlib import Path

BACKEND_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Event Manager AI Agent",
    layout="wide",
)

query_param = st.query_params
email_param = query_param.get("email", [None])[0]

if email_param:
    st.session_state["user_email"] = email_param
    st.query_params.clear()
    st.experimental_rerun()

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&family=Orbitron:wght@600;700&display=swap');

        body {
            margin: 0;
            font-family: 'Montserrat', sans-serif;
            background: #0A0A0A;
            color: #E0E0E0;
        }
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #1A1A1A 0%, #0D0D0D 100%);
        }
        [data-testid="stHeader"] {
            display: none !important;
        }

        .custom-header-container {
            background-color: #121212;
            padding: 1.2rem 2rem;
            border-bottom: 1px solid #2A2A2A;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            display: flex;
            align-items: center;
            justify-content: flex-start;
            border-radius: 0 0 15px 15px;
        }
        .main-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.2rem;
            font-weight: 700;
            color: #00FFC0;
            margin: 0;
            letter-spacing: 1.5px;
        }
        .header-icon {
            font-size: 2.5rem;
            color: #00FFC0;
            margin-right: 1rem;
            vertical-align: middle;
        }
        .header-left-content {
            display: flex;
            align-items: center;
        }

        .sub-title {
            font-size: 1.3rem;
            color: #B0B0B0;
            line-height: 1.6;
            margin-top: 1rem;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }

        .feature-card {
            background-color: #202020;
            padding: 1.8rem;
            border-radius: 1rem;
            box-shadow: 0px 6px 20px rgba(0,0,0,0.3);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            height: 100%;
            display: flex;
            min-height : 300px;
            flex-direction: column;
            justify-content: space-between;
            align-items: flex-start;
            border: 1px solid #333333;
            margin: 1rem;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
        }
        .feature-card h4 {
            font-size: 1.6rem;
            color: #00FFC0;
            margin-top: 0;
            margin-bottom: 0.8rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 0.7rem;
        }
        .feature-card h4 .icon {
            font-size: 1.8rem;
            color: #00FFC0;
        }
        .feature-card p {
            font-size: 1rem;
            color: #C0C0C0;
            line-height: 1.5;
        }

        a.hero-cta-button {
            background: linear-gradient(90deg, #00FFC0 0%, #00BFB2 100%);
            color: #0A0A0A;
            padding: 1.2rem 2.5rem;
            border-radius: 0.7rem;
            text-decoration: none;
            font-weight: 800;
            font-size: 1.3rem;
            transition: all 0.3s ease;
            display: block;
            width: fit-content;
            margin: 2.5rem auto 0 auto;
            align-items: center;
            justify-content: center;
            gap: 0.7rem;
            cursor: pointer;
        }
        a.hero-cta-button:hover {
            background: linear-gradient(90deg, #00BFB2 0%, #00FFC0 100%);
            
            transform: translateY(-3px) scale(1.02);
        }
        a.hero-cta-button:active {
            transform: translateY(0);
            box-shadow: 0 4px 15px rgba(0, 255, 192, 0.3);
        }

        .hero-section-container {
            text-align: center;
            margin-top: 4rem;
            padding: 0 2rem;
            max-width: 1000px;
            margin-left: auto;
            margin-right: auto;
        }
        .hero-section-container h2 {
            font-family: 'Orbitron', sans-serif;
            font-size: 3.5rem;
            font-weight: 700;
            color: #00FFC0;
            margin-bottom: 1rem;
            line-height: 1.1;
        }

        .logged-in-message {
            color: #4CAF50;
            font-size: 1.1rem;
            margin-top: 1.5rem;
            font-weight: 500;
            text-align: center;
            padding-bottom: 1rem;
        }

        .st-emotion-cache-nahz7x {
            margin-top: 4rem;
            margin-bottom: 4rem;
            border-top: 1px solid #333333;
        }
        .st-emotion-cache-nahz7x:last-of-type {
            margin-bottom: 2rem;
        }

        h3[data-testid="stMarkdownContainer"] {
            font-size: 2.5rem;
            font-weight: 700;
            color: #F8F8F8;
            margin-bottom: 2.5rem;
            margin-top: 3rem;
        }
        .st-emotion-cache-1r6dmym {
             gap: 2rem;
             display: grid;
             grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
             align-items: stretch;
             justify-content: center;
             margin: 0 auto;
             max-width: 1400px;
        }

        .custom-footer {
            text-align: center;
            padding: 1.5rem;
            margin-top: 10rem;
            background-color: #121212;
            border-top: 1px solid #2A2A2A;
            color: #888;
            font-size: 0.9rem;
            border-radius: 15px 15px 0 0;
        }
        .custom-footer p {
            margin: 0;
            color: #A0A0A0;
        }
        .custom-footer a:hover {
            color: #00FFC0;
            text-decoration: underline;
        }

        @media (max-width: 1200px) {
            .main-title {
                font-size: 2rem;
            }
            .header-icon {
                font-size: 2rem;
            }
            .hero-section-container h2 {
                font-size: 3rem;
            }
            .sub-title {
                font-size: 1.2rem;
            }
            .feature-card {
                padding: 1.5rem;
            }
            .feature-card h4 {
                font-size: 1.4rem;
            }
            .feature-card h4 .icon {
                font-size: 1.6rem;
            }
            .feature-card p {
                font-size: 0.95rem;
            }
            h3[data-testid="stMarkdownContainer"] {
                font-size: 2rem;
            }
            .st-emotion-cache-1r6dmym {
                gap: 1.5rem;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            }
            a.hero-cta-button {
                padding: 1rem 2rem;
                font-size: 1.2rem;
            }
        }

        @media (max-width: 768px) {
            .custom-header-container {
                flex-direction: row;
                justify-content: center;
                padding: 1rem 1rem;
            }
            .header-left-content {
                margin-bottom: 0;
            }
            .header-icon {
                margin-right: 0.5rem;
            }
            .main-title {
                font-size: 1.8rem;
            }
            .hero-section-container {
                margin-top: 2rem;
                padding: 0 1rem;
            }
            .hero-section-container h2 {
                font-size: 2.2rem;
            }
            .sub-title {
                font-size: 1rem;
            }
            .st-emotion-cache-nahz7x {
                margin-top: 2.5rem;
                margin-bottom: 2.5rem;
            }
            h3[data-testid="stMarkdownContainer"] {
                font-size: 1.8rem;
                margin-bottom: 1.5rem;
                margin-top: 2rem;
            }
            .feature-card {
                padding: 1.2rem;
            }
            .feature-card h4 {
                font-size: 1.2rem;
            }
            .feature-card h4 .icon {
                font-size: 1.4rem;
            }
            .feature-card p {
                font-size: 0.9rem;
            }
            .st-emotion-cache-1r6dmym {
                gap: 1rem;
                grid-template-columns: 1fr;
            }
            a.hero-cta-button {
                padding: 0.9rem 1.8rem;
                font-size: 1.1rem;
                margin-top: 2rem;
            }
            .custom-footer {
                padding: 1rem;
                margin-top: 2rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ========= Header  =========
with st.container():
    st.markdown('<div class="custom-header-container">', unsafe_allow_html=True)

    # Left part of header (Icon + Title) - now the only content in the header
    st.markdown("""
        <div class="header-left-content">
            <span class="main-title">Event Manager AI Agent</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # close custom-header-container

# Your original divider
st.markdown("---")

# ========= Hero Section =========
st.markdown(
    """
    <div class="hero-section-container">
        <h2>Plan Smarter. Achieve More.</h2>
        <p class="sub-title">
            Unlock unparalleled productivity with your personal AI. Seamlessly manage your schedule, resolve conflicts, and automate event planning using intelligent natural language commands.
        </p>
    """,
    unsafe_allow_html=True
)


if "user_email" not in st.session_state:
    st.markdown(f"""
        <a href="{BACKEND_URL}/login" class="hero-cta-button" target="_self">
            Sign in with Google
        </a>
    """, unsafe_allow_html=True)
else:
    # Display the success message and a button to go to dashboard if logged in
    st.markdown(f"""
        <div class="logged-in-message">
            ✅ Logged in as <span style="font-weight: 700;">{st.session_state['user_email']}</span>!
        </div>
        <a href="/dashboard" class="hero-cta-button"> Go to My Dashboard
        </a>
    """, unsafe_allow_html=True)


st.markdown("</div>", unsafe_allow_html=True) # Close hero-section-container

# Your original divider
st.markdown("---")

# ========= Features  =========
st.markdown("<h3 style='text-align:center;'>Why Our AI Event Manager Stands Out:</h3>", unsafe_allow_html=True)


feature_cols = st.columns(3) 

features = [
    ("🔗", "Intuitive Calendar Sync", "Effortlessly integrate with Google Calendar for real-time updates and seamless event management across all your devices."),
    ("🧠", "Advanced AI Assistant", "Leverage cutting-edge AI (LangChain & LangGraph) to understand complex requests, suggest optimal timings, and anticipate your needs."),
    ("🗣️", "Natural Language Command", "Simply chat to create, modify, or query events. Our AI understands your commands, eliminating tedious manual entry."),
    ("🛡️", "Robust Conflict Resolution", "Intelligently identify and propose solutions for scheduling conflicts, ensuring smooth and efficient calendar management."),
    ("⚡", "Boost Your Productivity", "Automate routine tasks and optimize your time, allowing you to focus on what truly matters."),
    ("✅", "Secure & Private", "Your data is protected with secure Google OAuth2 authentication, ensuring your privacy and peace of mind."),
]

# Distribute features among columns using round-robin.
# The CSS for .st-emotion-cache-1r6dmym ensures proper grid spacing.
for i, (icon, title, desc) in enumerate(features):
    with feature_cols[i % 3]: # i % 3 will cycle through 0, 1, 2
        st.markdown(
            f"""
            <div class="feature-card">
                <h4><span class="icon">{icon}</span> {title}</h4>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")

# =========  Footer (Customized) =========
st.markdown(
    """
    <div class="custom-footer">
        <p>&copy; 2025 Event Manager AI Agent &bull; All rights reserved.</p>
        <p>Developed with ❤️ by Piyush Kumar Seth</p>
        <div style="margin-top: 1rem; display: flex; justify-content: center; gap: 30px; font-size: 1.5rem;">
            <!-- GitHub -->
            <a href="https://github.com/piyushks" target="_blank" title="GitHub" style="color: #00FFC0;">
                <i class="fab fa-github"></i>
            </a>
            <!-- LinkedIn -->
            <a href="https://linkedin.com/in/piyushks" target="_blank" title="LinkedIn" style="color: #00FFC0;">
                <i class="fab fa-linkedin"></i>
            </a>
            <!-- Instagram -->
            <a href="https://instagram.com/piyushks" target="_blank" title="Instagram" style="color: #00FFC0;">
                <i class="fab fa-instagram"></i>
            </a>
            <!-- Contact -->
            <a href="mailto:support@example.com" title="Contact" style="color: #00FFC0;">
                <i class="fas fa-envelope"></i>
            </a>
        </div>
    </div>
    <!-- Load Font Awesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    """,
    unsafe_allow_html=True
)

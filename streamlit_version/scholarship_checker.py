import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="Scholarship Checker",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for chat interface
st.markdown("""
    <style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    
    /* Main container */
    .stApp {
        background: #0A192F;
        color: white;
    }

    /* Chat container */
    .chat-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 20px;
        height: calc(100vh - 200px);
        display: flex;
        flex-direction: column;
    }

    /* Chat messages */
    .chat-messages {
        flex-grow: 1;
        overflow-y: auto;
        padding: 20px;
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    .message {
        max-width: 80%;
        padding: 15px 20px;
        border-radius: 15px;
        margin-bottom: 10px;
    }

    .user-message {
        background: #1565C0;
        color: white;
        align-self: flex-end;
        border-bottom-right-radius: 5px;
    }

    .bot-message {
        background: rgba(21, 101, 192, 0.1);
        color: #B0BEC5;
        align-self: flex-start;
        border-bottom-left-radius: 5px;
    }

    /* Input container */
    .input-container {
        padding: 20px;
        background: rgba(21, 101, 192, 0.1);
        border-radius: 15px;
        margin-top: 20px;
    }

    /* Header */
    .chat-header {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 20px;
        background: rgba(21, 101, 192, 0.1);
        border-radius: 15px;
        margin-bottom: 20px;
    }

    .back-button {
        background: transparent;
        border: none;
        color: #64B5F6;
        font-size: 24px;
        cursor: pointer;
        padding: 5px;
    }

    .chat-title {
        color: #64B5F6;
        font-size: 24px;
        margin: 0;
    }
    </style>

    <div class="chat-container">
        <div class="chat-header">
            <button class="back-button" onclick="window.location.href='/'">←</button>
            <h1 class="chat-title">Scholarship Checker</h1>
        </div>
    </div>
""", unsafe_allow_html=True)

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your Scholarship Checker. How can I help you today? You can ask me about scholarship opportunities, eligibility criteria, or application processes."}
    ]

# Display chat messages
st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="message user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="message bot-message">{message["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Chat input
st.markdown('<div class="input-container">', unsafe_allow_html=True)
user_input = st.text_input("Type your message here...", key="user_input")
if st.button("Send"):
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Add bot response (placeholder - replace with actual API call)
        bot_response = "I understand your query. This is a placeholder response. The actual API integration will be implemented here."
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        # Clear input
        st.session_state.user_input = ""
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True) 
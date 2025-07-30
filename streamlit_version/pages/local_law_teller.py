import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000')

# Configure the page
st.set_page_config(
    page_title="Local Law Teller - Legal GPT",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    /* Main container */
    .stApp {
        background-color: #0A192F;
        color: white;
    }
    
    /* Header section */
    .header-container {
        display: flex;
        justify-content: flex-end;
        padding: 1rem 2rem;
        gap: 1rem;
        position: fixed;
        top: 0;
        right: 0;
        z-index: 1000;
    }
    
    .header {
        text-align: center;
        padding: 2rem 0;
        color: #64B5F6;
        margin-bottom: 2rem;
    }
    
    /* Chat container */
    .chat-container {
        background: rgba(13, 37, 63, 0.9);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(100, 181, 246, 0.2);
    }
    
    /* Message styling */
    .user-message {
        background: rgba(100, 181, 246, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 3px solid #64B5F6;
    }
    
    .assistant-message {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 3px solid #B0BEC5;
    }
    
    /* Sidebar styling */
    .sidebar-content {
        background: rgba(13, 37, 63, 0.9);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #64B5F6;
        color: #0A192F;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #1E88E5;
        transform: translateY(-2px);
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        background-color: rgba(13, 37, 63, 0.9);
        border: 1px solid #64B5F6;
        color: white;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Check if user is logged in
if 'user' not in st.session_state or not st.session_state.user:
    st.error("Please log in to access this feature.")
    st.stop()

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Header with back button
col1, col2, col3 = st.columns([1, 6, 1])

with col1:
    if st.button("← Back", key="back_btn"):
        st.session_state.current_page = "main"
        st.rerun()

with col2:
    st.markdown("""
        <h1 style="color: #64B5F6; text-align: center;">Local Law Teller</h1>
    """, unsafe_allow_html=True)

# Sidebar with options
with st.sidebar:
    st.markdown("""
        <div class="sidebar-content">
            <h3 style="color: #64B5F6;">Options</h3>
        </div>
    """, unsafe_allow_html=True)
    
    jurisdiction = st.selectbox(
        "Select Jurisdiction",
        ["United States", "United Kingdom", "Canada", "Australia", "India"]
    )
    
    law_type = st.multiselect(
        "Select Law Types",
        ["Criminal Law", "Civil Law", "Family Law", "Property Law", "Business Law"]
    )
    
    st.markdown("""
        <div class="sidebar-content" style="margin-top: 2rem;">
            <h4 style="color: #64B5F6;">Selected Filters</h4>
            <p style="color: #B0BEC5;">Jurisdiction: {}</p>
            <p style="color: #B0BEC5;">Law Types: {}</p>
        </div>
    """.format(jurisdiction, ", ".join(law_type) if law_type else "None"), unsafe_allow_html=True)

# Main chat interface
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    st.markdown("""
        <div class="chat-container">
            <h3 style="color: #64B5F6; margin-bottom: 1rem;">Ask about local laws and regulations</h3>
        </div>
    """, unsafe_allow_html=True)

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(f"""
                <div class="{message['role']}-message">
                    {message['content']}
                </div>
            """, unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("Ask about local laws..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(f"""
                <div class="user-message">
                    {prompt}
                </div>
            """, unsafe_allow_html=True)
        
        # Display assistant message placeholder
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            try:
                # Make API request with context
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json={
                        "message": prompt,
                        "context": {
                            "jurisdiction": jurisdiction,
                            "law_types": law_type,
                            "feature": "local_law_teller"
                        }
                    },
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    message_placeholder.markdown(f"""
                        <div class="assistant-message">
                            {data['response']}
                        </div>
                    """, unsafe_allow_html=True)
                    st.session_state.messages.append({"role": "assistant", "content": data["response"]})
                else:
                    message_placeholder.error("Error: Failed to get response from server")
                    
            except Exception as e:
                message_placeholder.error(f"Error: {str(e)}")

    # Clear chat button
    if st.session_state.messages:
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.experimental_rerun()

# Update the back button JavaScript
st.markdown("""
    <script>
        function handleBack() {
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: 'navigate_main'
            }, '*');
        }
    </script>
""", unsafe_allow_html=True)

# Handle navigation
if st.session_state.get("widget_clicked") == "navigate_main":
    st.session_state.current_page = "main"
    st.rerun() 
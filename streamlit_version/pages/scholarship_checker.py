import streamlit as st
import requests
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000')

# Configure the page
st.set_page_config(
    page_title="Scholarship Checker - Legal GPT",
    page_icon="��",
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
    .header {
        text-align: center;
        padding: 2rem 0;
        color: #64B5F6;
        margin-bottom: 2rem;
    }
    
    /* Scholarship card */
    .scholarship-card {
        background: rgba(13, 37, 63, 0.9);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(100, 181, 246, 0.2);
        transition: transform 0.3s ease;
    }
    
    .scholarship-card:hover {
        transform: translateY(-5px);
        border-color: #64B5F6;
    }
    
    /* Filter section */
    .filter-section {
        background: rgba(13, 37, 63, 0.9);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(100, 181, 246, 0.2);
    }
    
    /* Chat styling */
    .chat-container {
        background: rgba(13, 37, 63, 0.9);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(100, 181, 246, 0.2);
    }
    
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
    
    /* Apply button */
    .apply-button {
        display: inline-block;
        background-color: #64B5F6;
        color: #0A192F;
        padding: 0.5rem 1.5rem;
        border-radius: 5px;
        text-decoration: none;
        transition: all 0.3s ease;
        margin-top: 1rem;
    }
    
    .apply-button:hover {
        background-color: #1E88E5;
        transform: translateY(-2px);
    }
    
    /* Slider styling */
    .stSlider > div > div {
        background-color: #64B5F6;
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

# Initialize session state
if 'scholarships' not in st.session_state:
    st.session_state.scholarships = []
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
        <h1 style="color: #64B5F6; text-align: center;">Scholarship Checker</h1>
    """, unsafe_allow_html=True)

# Main content
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    # Filter section
    st.markdown("""
        <div class="filter-section">
            <h3 style="color: #64B5F6; margin-bottom: 1rem;">Search Filters</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Education Level
    education_level = st.multiselect(
        "Education Level",
        ["High School", "Undergraduate", "Graduate", "PhD", "Post-Doctoral"]
    )
    
    # Field of Study
    field_of_study = st.multiselect(
        "Field of Study",
        ["Engineering", "Medicine", "Law", "Business", "Arts", "Science", "Technology"]
    )
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        # Amount Range
        amount_range = st.slider(
            "Scholarship Amount Range ($)",
            min_value=0,
            max_value=100000,
            value=(0, 100000),
            step=1000
        )
    
    with col_b:
        # Application Deadline
        deadline = st.date_input(
            "Application Deadline",
            value=None
        )
    
    # Location
    location = st.text_input("Location (Optional)")
    
    # Search button
    if st.button("Search Scholarships"):
        try:
            # Make API request with filters
            response = requests.post(
                f"{BACKEND_URL}/scholarships/search",
                json={
                    "filters": {
                        "education_level": education_level,
                        "field_of_study": field_of_study,
                        "amount_range": amount_range,
                        "deadline": str(deadline) if deadline else None,
                        "location": location
                    }
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                st.session_state.scholarships = response.json()
            else:
                st.error("Failed to fetch scholarships")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

    # Display scholarships
    if st.session_state.scholarships:
        st.markdown("""
            <h3 style="color: #64B5F6; margin: 2rem 0;">Search Results</h3>
        """, unsafe_allow_html=True)
        
        for scholarship in st.session_state.scholarships:
            st.markdown(f"""
                <div class="scholarship-card">
                    <h3 style="color: #64B5F6;">{scholarship['name']}</h3>
                    <p style="color: #B0BEC5; margin: 1rem 0;">
                        <strong style="color: white;">Amount:</strong> ${scholarship['amount']:,}<br>
                        <strong style="color: white;">Education Level:</strong> {scholarship['education_level']}<br>
                        <strong style="color: white;">Field of Study:</strong> {scholarship['field_of_study']}<br>
                        <strong style="color: white;">Deadline:</strong> {scholarship['deadline']}<br>
                        <strong style="color: white;">Location:</strong> {scholarship['location']}
                    </p>
                    <p style="color: #B0BEC5;">{scholarship['description']}</p>
                    <a href="{scholarship['application_url']}" target="_blank" class="apply-button">Apply Now</a>
                </div>
            """, unsafe_allow_html=True)

    # Chat interface
    st.markdown("""
        <div class="chat-container">
            <div class="chat-header">
                <button class="back-button" onclick="handleBack()">←</button>
                <h1 class="chat-title">Scholarship Checker</h1>
            </div>
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
    if prompt := st.chat_input("Ask about scholarships..."):
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
                            "feature": "scholarship_checker",
                            "filters": {
                                "education_level": education_level,
                                "field_of_study": field_of_study,
                                "amount_range": amount_range,
                                "deadline": str(deadline) if deadline else None,
                                "location": location
                            }
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
import streamlit as st
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="Legal GPT",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'main'
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user' not in st.session_state:
    st.session_state.user = None
if 'show_login' not in st.session_state:
    st.session_state.show_login = False
if 'show_signup' not in st.session_state:
    st.session_state.show_signup = False
if 'widget_clicked' not in st.session_state:
    st.session_state.widget_clicked = None

# Custom CSS
st.markdown("""
    <style>
    /* Base Styles */
    .stApp {
        background-color: #0A192F;
        color: white;
        min-height: 100vh;
        width: 100%;
        margin: 0;
        padding: 0;
    }
    
    /* Main Container */
    .main-container {
        width: 100%;
        min-height: 100vh;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        box-sizing: border-box;
        position: relative;
        z-index: 1;
    }
    
    /* Header Container */
    .header-container {
        width: 100%;
        display: flex;
        justify-content: flex-end;
        padding: 0.25rem 0.5rem;
        margin: 0;
        position: relative;
        z-index: 2;
        background: rgba(10, 25, 47, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(100, 181, 246, 0.1);
    }
    
    /* Main Title */
    .main-title {
        font-size: 2rem;
        color: #64B5F6;
        text-align: center;
        margin: 0.5rem 0 0.25rem 0;
        position: relative;
        z-index: 2;
        font-weight: 700;
    }
    
    /* Subtitle */
    .subtitle {
        font-size: 1rem;
        color: #B0BEC5;
        text-align: center;
        margin: 0 0 1rem 0;
        position: relative;
        z-index: 2;
        max-width: 800px;
        line-height: 1.5;
        padding: 0 0.5rem;
    }
    
    /* Service Cards */
    .service-cards {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1rem;
        width: 100%;
        max-width: 1000px;
        margin: 0 auto;
        padding: 0 0.5rem;
        box-sizing: border-box;
        position: relative;
        z-index: 2;
    }
    
    /* Service Card */
    .service-card {
        background: rgba(21, 101, 192, 0.1);
        border: 1px solid rgba(100, 181, 246, 0.2);
        border-radius: 12px;
        padding: 1rem;
        transition: all 0.3s ease;
        position: relative;
        z-index: 2;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        backdrop-filter: blur(10px);
    }
    
    .service-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        border-color: rgba(100, 181, 246, 0.4);
    }
    
    .service-title {
        color: #64B5F6;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .service-description {
        color: #B0BEC5;
        line-height: 1.4;
        margin-bottom: 0.75rem;
        font-size: 0.9rem;
    }
    
    /* Features Section */
    .features-section {
        width: 100%;
        max-width: 1000px;
        margin: 1rem auto;
        padding: 1rem 0.5rem;
        background: rgba(21, 101, 192, 0.05);
        border-radius: 16px;
        box-sizing: border-box;
        position: relative;
        z-index: 2;
        backdrop-filter: blur(10px);
    }
    
    .section-title {
        color: #64B5F6;
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
    }
    
    .feature-card {
        background: rgba(21, 101, 192, 0.1);
        border: 1px solid rgba(100, 181, 246, 0.2);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        height: 100%;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        border-color: rgba(100, 181, 246, 0.4);
    }
    
    .feature-title {
        color: #64B5F6;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .feature-description {
        color: #B0BEC5;
        line-height: 1.4;
        font-size: 0.9rem;
    }
    
    /* Modal Styles */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.85);
        backdrop-filter: blur(5px);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 999999;
    }
    
    .modal-container {
        background: linear-gradient(145deg, #0A192F 0%, #0d2444 100%);
        border: 1px solid rgba(100, 181, 246, 0.3);
        border-radius: 16px;
        padding: 2.5rem;
        width: 90%;
        max-width: 450px;
        position: relative;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        z-index: 1000000;
    }
    
    .modal-close {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: transparent;
        border: none;
        color: #64B5F6;
        font-size: 1.5rem;
        cursor: pointer;
        padding: 0.5rem;
        line-height: 1;
        transition: all 0.3s ease;
        z-index: 1000001;
    }
    
    .modal-close:hover {
        color: #90CAF9;
        transform: rotate(90deg);
    }
    
    .modal-title {
        color: #64B5F6;
        font-size: 1.8rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Form Styling */
    .auth-form {
        width: 100%;
        margin-bottom: 1.5rem;
    }
    
    .form-group {
        margin-bottom: 1.5rem;
    }
    
    .form-label {
        display: block;
        color: #64B5F6;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    
    .form-input {
        width: 100%;
        padding: 0.875rem 1rem;
        background: rgba(21, 101, 192, 0.1);
        border: 1px solid rgba(100, 181, 246, 0.2);
        border-radius: 10px;
        color: white;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-sizing: border-box;
    }
    
    .form-input:focus {
        border-color: #64B5F6;
        box-shadow: 0 0 0 2px rgba(100, 181, 246, 0.2);
        outline: none;
    }
    
    .submit-button {
        width: 100%;
        padding: 0.875rem;
        background: linear-gradient(135deg, #1565C0 0%, #1976D2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 1rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-top: 1rem;
    }
    
    .submit-button:hover {
        background: linear-gradient(135deg, #1976D2 0%, #2196F3 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(25, 118, 210, 0.3);
    }
    
    .divider {
        text-align: center;
        margin: 1.5rem 0;
        position: relative;
    }
    
    .divider::before,
    .divider::after {
        content: "";
        position: absolute;
        top: 50%;
        width: 45%;
        height: 1px;
        background: rgba(100, 181, 246, 0.2);
    }
    
    .divider::before {
        left: 0;
    }
    
    .divider::after {
        right: 0;
    }
    
    .divider span {
        background: #0A192F;
        padding: 0 1rem;
        color: #64B5F6;
        font-size: 0.9rem;
    }
    
    .google-btn {
        width: 100%;
        padding: 0.875rem;
        background: transparent;
        border: 1px solid rgba(100, 181, 246, 0.3);
        border-radius: 10px;
        color: white;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .google-btn:hover {
        background: rgba(100, 181, 246, 0.1);
        border-color: #64B5F6;
    }
    
    .auth-links {
        text-align: center;
        margin-top: 1.5rem;
        color: #B0BEC5;
        font-size: 0.9rem;
    }
    
    .auth-links a {
        color: #64B5F6;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    
    .auth-links a:hover {
        color: #90CAF9;
        text-decoration: underline;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideUp {
        from { 
            opacity: 0;
            transform: translateY(20px);
        }
        to { 
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .modal-overlay {
        animation: fadeIn 0.3s ease;
    }
    
    .modal-container {
        animation: slideUp 0.3s ease;
    }
    
    /* Chat Container */
    .chat-container {
        width: 100%;
        max-width: 1000px;
        margin: 0 auto;
        padding: 1rem;
        background: rgba(21, 101, 192, 0.05);
        border-radius: 16px;
        position: relative;
        z-index: 2;
        backdrop-filter: blur(10px);
    }
    
    .chat-title {
        color: #64B5F6;
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .chat-description {
        color: #B0BEC5;
        text-align: center;
        margin-bottom: 1rem;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-container {
            padding: 0;
        }
        
        .header-container {
            padding: 0.25rem;
        }
        
        .main-title {
            font-size: 1.75rem;
            margin: 0.5rem 0 0.25rem 0;
        }
        
        .subtitle {
            font-size: 0.9rem;
            margin: 0 0 0.75rem 0;
            padding: 0 0.25rem;
        }
        
        .service-cards {
            grid-template-columns: 1fr;
            padding: 0 0.25rem;
            gap: 0.75rem;
        }
        
        .features-section {
            padding: 0.75rem 0.25rem;
            margin: 0.75rem 0;
        }
        
        .section-title {
            font-size: 1.25rem;
            margin-bottom: 0.75rem;
        }
        
        .features-grid {
            gap: 0.75rem;
        }
        
        .feature-card {
            padding: 0.75rem;
        }
        
        .chat-container {
            padding: 0.75rem;
        }
        
        .chat-title {
            font-size: 1.25rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

def show_auth_buttons():
    col1, col2, col3 = st.columns([6, 1, 1])
    with col2:
        if st.button("Login", use_container_width=True):
            st.session_state.show_login = True
            st.session_state.show_signup = False
            st.rerun()
    with col3:
        if st.button("Sign Up", use_container_width=True):
            st.session_state.show_signup = True
            st.session_state.show_login = False
            st.rerun()

def show_login_modal():
    # Create a container for the modal
    modal_container = st.empty()
    
    # Add the modal HTML with proper structure and event handlers
    modal_container.markdown("""
        <div class="modal-overlay" id="loginModal">
            <div class="modal-container">
                <button class="modal-close" onclick="handleCloseModal()">×</button>
                <h2 class="modal-title">Welcome Back</h2>
                <form class="auth-form" id="loginForm" onsubmit="handleLoginSubmit(event)">
                    <div class="form-group">
                        <label class="form-label">Email Address</label>
                        <input type="email" class="form-input" placeholder="Enter your email" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Password</label>
                        <input type="password" class="form-input" placeholder="Enter your password" required>
                    </div>
                    <button type="submit" class="submit-button">Login</button>
                </form>
                <div class="divider"><span>OR</span></div>
                <button class="google-btn" onclick="handleGoogleLogin()">
                    <img src="https://www.google.com/favicon.ico" alt="Google" style="width: 20px; height: 20px;">
                    Continue with Google
                </button>
                <div class="auth-links">
                    Don't have an account? <a href="#" onclick="handleSwitchToSignup(); return false;">Sign up</a>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def show_signup_modal():
    # Create a container for the modal
    modal_container = st.empty()
    
    # Add the modal HTML with proper structure and event handlers
    modal_container.markdown("""
        <div class="modal-overlay" id="signupModal">
            <div class="modal-container">
                <button class="modal-close" onclick="handleCloseModal()">×</button>
                <h2 class="modal-title">Create Account</h2>
                <form class="auth-form" id="signupForm" onsubmit="handleSignupSubmit(event)">
                    <div class="form-group">
                        <label class="form-label">Email Address</label>
                        <input type="email" class="form-input" placeholder="Enter your email" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Password</label>
                        <input type="password" class="form-input" placeholder="Create a password" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Confirm Password</label>
                        <input type="password" class="form-input" placeholder="Confirm your password" required>
                    </div>
                    <button type="submit" class="submit-button">Sign Up</button>
                </form>
                <div class="divider"><span>OR</span></div>
                <button class="google-btn" onclick="handleGoogleSignup()">
                    <img src="https://www.google.com/favicon.ico" alt="Google" style="width: 20px; height: 20px;">
                    Continue with Google
                </button>
                <div class="auth-links">
                    Already have an account? <a href="#" onclick="handleSwitchToLogin(); return false;">Login</a>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def show_features():
    st.markdown("""
        <div class="features-section">
            <h2 class="section-title">Why Choose Legal GPT?</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <h3 class="feature-title">24/7 Availability</h3>
                    <p class="feature-description">Get legal advice anytime, anywhere, without waiting for office hours.</p>
                </div>
                <div class="feature-card">
                    <h3 class="feature-title">Instant Responses</h3>
                    <p class="feature-description">Receive immediate answers to your legal queries with detailed explanations.</p>
                </div>
                <div class="feature-card">
                    <h3 class="feature-title">Personalized Guidance</h3>
                    <p class="feature-description">Get tailored advice based on your specific situation and needs.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def show_main_page():
    # Main container for the entire page
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header with auth buttons
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("Login", key="login_btn", use_container_width=True):
            st.session_state.show_login = True
            st.experimental_rerun()
        if st.button("Sign Up", key="signup_btn", use_container_width=True):
            st.session_state.show_signup = True
            st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content
    st.markdown('<h1 class="main-title">Your AI Legal Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Get instant legal advice and scholarship guidance powered by advanced AI technology</p>', unsafe_allow_html=True)
    
    # Service cards
    st.markdown('<div class="service-cards">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="service-card">
                <div>
                    <h2 class="service-title">LOCAL LAW TELLER</h2>
                    <p class="service-description">
                        Your AI-powered legal assistant available 24/7.<br>
                        Get instant answers to your legal queries in simple language.
                    </p>
                </div>
                <div>
                    <button class="submit-button" onclick="handleLawChat()">Access Local Law Teller</button>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="service-card">
                <div>
                    <h2 class="service-title">SCHOLARSHIP CHECKER</h2>
                    <p class="service-description">
                        Discover scholarships tailored to your profile.<br>
                        Get personalized guidance on eligibility and application process.
                    </p>
                </div>
                <div>
                    <button class="submit-button" onclick="handleScholarshipChat()">Access Scholarship Checker</button>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Features section
    show_features()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show modals if needed
    if st.session_state.show_login:
        show_login_modal()
    elif st.session_state.show_signup:
        show_signup_modal()

def show_chat_interface(chat_type):
    # Header with auth buttons and back button
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    show_auth_buttons()
    if st.button("← Back to Main Menu", use_container_width=True):
        st.session_state.current_page = 'main'
        st.session_state.messages = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    st.title(f"{'Local Law Teller' if chat_type == 'law_chat' else 'Scholarship Checker'} Chat")
    
    # Initialize chat messages if empty
    if not st.session_state.messages:
        welcome_msg = f"Welcome to {'Local Law Teller' if chat_type == 'law_chat' else 'Scholarship Checker'}! How can I help you today?"
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = f"This is a placeholder response for your query: {prompt}"
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# JavaScript for handling auth interactions
st.markdown("""
    <script>
        function handleCloseModal() {
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: 'close_modal'
            }, '*');
        }
        
        function handleSwitchToSignup() {
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: 'switch_to_signup'
            }, '*');
        }
        
        function handleSwitchToLogin() {
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: 'switch_to_login'
            }, '*');
        }
        
        function handleLoginSubmit(event) {
            event.preventDefault();
            const form = event.target;
            const email = form.querySelector('input[type="email"]').value;
            const password = form.querySelector('input[type="password"]').value;
            
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: JSON.stringify({
                    action: 'login',
                    email: email,
                    password: password
                })
            }, '*');
        }
        
        function handleSignupSubmit(event) {
            event.preventDefault();
            const form = event.target;
            const email = form.querySelector('input[type="email"]').value;
            const password = form.querySelector('input[type="password"]').value;
            const confirmPassword = form.querySelectorAll('input[type="password"]')[1].value;
            
            if (password !== confirmPassword) {
                alert('Passwords do not match!');
                return;
            }
            
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: JSON.stringify({
                    action: 'signup',
                    email: email,
                    password: password
                })
            }, '*');
        }
        
        function handleGoogleLogin() {
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: JSON.stringify({
                    action: 'google_login'
                })
            }, '*');
        }
        
        function handleGoogleSignup() {
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: JSON.stringify({
                    action: 'google_signup'
                })
            }, '*');
        }
        
        // Add click event listener for modal close button
        document.addEventListener('DOMContentLoaded', function() {
            const closeButtons = document.querySelectorAll('.modal-close');
            closeButtons.forEach(button => {
                button.addEventListener('click', handleCloseModal);
            });
        });
    </script>
""", unsafe_allow_html=True)

# Add JavaScript for handling navigation
st.markdown("""
    <script>
        function handleLawChat() {
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: 'law_chat'
            }, '*');
        }
        
        function handleScholarshipChat() {
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: 'scholarship_chat'
            }, '*');
        }
    </script>
""", unsafe_allow_html=True)

# Update the main app logic to handle modal interactions
if 'widget_clicked' in st.session_state:
    try:
        value = st.session_state.widget_clicked
        if value == 'close_modal':
            st.session_state.show_login = False
            st.session_state.show_signup = False
            st.experimental_rerun()
        elif value == 'switch_to_signup':
            st.session_state.show_login = False
            st.session_state.show_signup = True
            st.experimental_rerun()
        elif value == 'switch_to_login':
            st.session_state.show_signup = False
            st.session_state.show_login = True
            st.experimental_rerun()
        else:
            # Handle form submissions
            data = json.loads(value)
            if data['action'] == 'login':
                # Handle login
                st.success('Login successful!')
                st.session_state.show_login = False
                st.experimental_rerun()
            elif data['action'] == 'signup':
                # Handle signup
                st.success('Signup successful!')
                st.session_state.show_signup = False
                st.experimental_rerun()
            elif data['action'] in ['google_login', 'google_signup']:
                # Handle Google auth
                st.info('Google authentication coming soon!')
    except:
        pass

# Main app logic
if st.session_state.current_page == 'main':
    show_main_page()
elif st.session_state.current_page in ['law_chat', 'scholarship_chat']:
    show_chat_interface(st.session_state.current_page)

if __name__ == "__main__":
    main()                                                         
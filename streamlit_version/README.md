# Legal GPT - Streamlit Version

This is a Streamlit version of the Legal GPT application, providing an AI-powered legal research assistant interface.

## Features

- Clean and intuitive chat interface
- Real-time responses from the AI
- Persistent chat history
- Responsive design
- Sidebar with information about the application

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone this repository
2. Navigate to the `streamlit_version` directory
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Make sure your backend server is running on `http://localhost:5000`
2. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```
3. The application will open in your default web browser

## Environment Variables

The application uses environment variables for configuration. Create a `.env` file in the `streamlit_version` directory with the following variables:

```
BACKEND_URL=http://localhost:5000
```

## Usage

1. Type your legal question in the chat input at the bottom of the screen
2. Press Enter or click the send button to submit your question
3. Wait for the AI to process and respond to your query
4. The conversation history will be maintained during your session

## Note

This application requires a running backend server to function properly. Make sure your backend server is running and accessible at the configured URL before starting the Streamlit application. 
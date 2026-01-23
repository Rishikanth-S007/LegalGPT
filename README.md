# LegalGPT 📚⚖️

An intelligent legal assistance platform powered by AI, providing comprehensive legal guidance, scholarship opportunities, and local law information through an intuitive web interface.

## 🌟 Overview

LegalGPT is a full-stack application designed to make legal information accessible to everyone. Whether you need legal consultation, scholarship guidance, or local law information, LegalGPT leverages AI to provide accurate, helpful responses in real-time.

## 🏗️ Project Structure

```
LegalGPT/
├── legal-gpt-backend/          # FastAPI Python backend
│   ├── app/
│   │   ├── api/endpoints/      # API route handlers
│   │   ├── services/           # Business logic layer
│   │   ├── models/             # Database models
│   │   ├── schemas/            # Pydantic schemas
│   │   └── core/               # Security & config
│   └── requirements.txt
├── legal-gpt-frontend/         # React web application
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
└── streamlit_version/          # Alternative Streamlit UI
    ├── app.py
    └── pages/
```

## 🚀 Features

- **Legal Chat Interface** - Interactive AI-powered legal consultation
- **Scholarship Checker** - Search and filter scholarship opportunities
- **Local Law Teller** - Access local laws and regulations
- **Multi-format UI** - Web interface and Streamlit dashboard
- **RESTful API** - Scalable backend architecture

## 💻 Tech Stack

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.8+
- **Database**: (Configured in settings)
- **AI**: Integrated AI service for legal guidance

### Frontend
- **Framework**: React
- **Styling**: CSS
- **HTTP Client**: Fetch API

### Alternative
- **Dashboard**: Streamlit

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 14+ and npm
- Git

## ⚡ Quick Start

### Backend Setup

```bash
cd legal-gpt-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

```bash
cd legal-gpt-frontend

# Install dependencies
npm install

# Start development server
npm start
```

The frontend will open at `http://localhost:3000`

### Streamlit Version

```bash
cd streamlit_version

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login

### Chat
- `POST /api/chat/message` - Send chat message to legal AI

### Legal Services
- `GET /api/legal/search` - Search legal information
- `GET /api/legal/details/{id}` - Get legal details

### Scholarships
- `GET /api/scholarship/search` - Search scholarships
- `GET /api/scholarship/filter` - Filter scholarships by criteria

## 📖 Usage Examples

### Chat with LegalGPT
1. Navigate to the chat interface
2. Type your legal question
3. Receive AI-powered response
4. View related content suggestions

### Find Scholarships
1. Go to Scholarship Checker
2. Filter by criteria (field, country, amount)
3. View matching scholarships
4. Access application links

### Search Local Laws
1. Access Local Law Teller
2. Search by location and topic
3. Browse relevant regulations
4. Get law summaries and details

## 🔐 Security

- JWT-based authentication
- Secure password hashing
- CORS enabled for production
- Input validation on all endpoints

## 📦 Dependencies

### Backend Dependencies
See `legal-gpt-backend/requirements.txt`

### Frontend Dependencies
See `legal-gpt-frontend/package.json`

### Streamlit Dependencies
See `streamlit_version/requirements.txt`

## 🛠️ Development

### Running Tests
```bash
cd legal-gpt-backend
pytest
```

### Code Style
- Backend: PEP 8 compliant
- Frontend: ESLint configured

## 📝 Configuration

Backend configuration is managed through `legal-gpt-backend/app/config/settings.py`

Key settings:
- Database URL
- AI Service API keys
- CORS allowed origins
- JWT secret key

## 🚢 Deployment

### Backend (Docker)
```bash
cd legal-gpt-backend
docker build -t legalgpt-backend .
docker run -p 8000:8000 legalgpt-backend
```

### Frontend (Production Build)
```bash
cd legal-gpt-frontend
npm run build
# Deploy the build/ folder to your hosting service
```

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👨‍💻 Author

**Rishikanth S**

- GitHub: [Rishikanth-S007](https://github.com/Rishikanth-S007)
- LegalGPT Repository: [github.com/Rishikanth-S007/LegalGPT](https://github.com/Rishikanth-S007/LegalGPT)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

## 🎯 Future Enhancements

- Multi-language support
- Advanced legal document analysis
- Mobile app (React Native)
- Integration with legal databases
- Advanced analytics dashboard
- Machine learning model improvements

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)

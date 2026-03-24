# LegalGPT

AI-powered Indian Legal Assistant and Scholarship Finder

## Features
- ⚖️ Local Law Teller — AI legal advice
- 🎓 Scholarship Checker — Find scholarships
- 🔐 Secure JWT + Google OAuth login
- 🌐 Hindi language support
- 📱 Mobile responsive design

## Tech Stack
- Frontend: React + Material UI
- Backend: FastAPI + SQLite
- AI Engine: RAG + FAISS + sentence-transformers
- Auth: JWT + Google OAuth2

## Setup Instructions

### Backend
```bash
cd backend
pip install -r requirements.txt
```

Create `.env` file with (copy from `.env.example`):
```
SECRET_KEY=your_secret_key
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
```

```bash
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
```

Create `.env` file with (copy from `.env.example`):
```
REACT_APP_API_URL=http://localhost:8000
```

```bash
npm start
```

## Environment Variables
**Never commit `.env` files.** Copy `.env.example` and fill in your values.

## License
MIT

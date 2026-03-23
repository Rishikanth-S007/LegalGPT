from fastapi import APIRouter, Depends, HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.core.security import create_access_token
from app.config.settings import settings
from datetime import timedelta
import os

router = APIRouter()

@router.post("/api/auth/google")
async def google_login(
    data: dict,
    db: Session = Depends(get_db)
):
    try:
        CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
        
        idinfo = id_token.verify_oauth2_token(
            data['credential'],
            google_requests.Request(),
            CLIENT_ID
        )
        
        email = idinfo['email']
        name = idinfo.get('name', email.split('@')[0])
        picture = idinfo.get('picture', '')
        
        # Find existing user or create new
        user = db.query(User).filter(
            User.email == email
        ).first()
        
        if not user:
            user = User(
                email=email,
                username=name,
                hashed_password="GOOGLE_OAUTH_USER",
                is_google_user=True,
                picture=picture
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Generate JWT same as normal login using the create_access_token utility
        access_token_expires = timedelta(hours=settings.jwt_expiration_hours)
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "name": user.username,
                "email": user.email,
                "picture": picture
            }
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid Google token: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Google login error: {str(e)}"
        )

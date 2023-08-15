import json
from typing import Generator

import firebase_admin
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from firebase_admin import auth
from firebase_admin.credentials import Certificate
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from core.config import settings
from models import User
from services.user import user_service

from db.session import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/google/callback')
key_dict = json.loads(
    settings.GOOGLE_APPLICATION_CREDENTIALS
)

firebase_admin.initialize_app(Certificate(key_dict))

def get_db() -> Generator:
    db = SessionLocal()
    db.current_user_id = None

    try:
        yield db
    finally:
        db.close()


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = User('1','full_name', 'email@email.com', True, '', True, 0)
    return user

    if 'auth' not in request.headers:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing auth header"
        )

    auth_header = request.headers['auth']
    try:
        payload = auth.verify_id_token(auth_header)
        user_id = payload.get('sub')

        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = user_service.get_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    return user


def get_admin_user(current_user=Depends(get_current_user)):
    forbidden_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User is not an admin",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not current_user.is_admin:
        raise forbidden_exception
    return current_user

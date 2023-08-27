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
from fastapi_cognito import CognitoAuth, CognitoSettings, CognitoToken

from db.session import SessionLocal
from core.config import settings

cognito_us = CognitoAuth(
  settings=CognitoSettings.from_global_settings(settings), userpool_name="us"
)

def get_db() -> Generator:
    db = SessionLocal()
    db.current_user_id = None

    try:
        yield db
    finally:
        db.close()


def get_current_user(auth: CognitoToken = Depends(cognito_us.auth_required), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id = auth.cognito_id
    if user_id is None:
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

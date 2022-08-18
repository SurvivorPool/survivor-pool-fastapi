from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from core.config import settings
from models import User
from services.user import user_service

from db.session import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/google/callback')

def get_db() -> Generator:
    db = SessionLocal()
    db.current_user_id = None

    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        provider: str = payload.get("provider")
        if email is None or provider is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = user_service.get_by_email_and_provider(db=db, email=email, provider=provider)
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

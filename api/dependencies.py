from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from core.config import settings
import crud

from db.session import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/google/callback')

def get_db() -> Generator:
    db = SessionLocal()
    db.current_user_id = None

    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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
    user = crud.user.get_by_email_and_provider(db=db, email=email, provider=provider)
    if user is None:
        raise credentials_exception
    return user
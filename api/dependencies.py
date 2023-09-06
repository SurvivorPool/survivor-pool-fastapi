from typing import Generator
from fastapi import Depends, HTTPException, status, Request, Header
from sqlalchemy.orm import Session
from jose import jwt
from models import User
import requests

from db.session import SessionLocal
from core.config import settings
from services.user import user_service


def get_db() -> Generator:
    db = SessionLocal()
    db.current_user_id = None

    try:
        yield db
    finally:
        db.close()


async def get_cognito_public_key(kid):
    cognito_jwks_url = settings.COGNITO_URL

    response = requests.get(cognito_jwks_url)
    response.raise_for_status()  # Raise an exception if the request fails

    jwks = response.json()

    for key in jwks["keys"]:
        if key["kid"] == kid:
            return key
    return None


async def get_current_user(authorization:  str = Header(...), db: Session = Depends(get_db)) -> User:
    try:
        token = authorization.split(" ")[1]  # Extract the token part after "Bearer"
        decoded_token = jwt.get_unverified_header(token)
        kid = decoded_token.get("kid")
        public_key = await get_cognito_public_key(kid)
        if public_key:
            decoded_token = jwt.decode(token, public_key, algorithms=["RS256"], audience=settings.COGNITO_CLIENT_ID)
            user_id = decoded_token['sub']
            user = user_service.get_by_id(db, user_id)
            return user
        else:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_admin_user(current_user=Depends(get_current_user)):
    forbidden_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User is not an admin",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not current_user.is_admin:
        raise forbidden_exception
    return current_user

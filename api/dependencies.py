from typing import Generator
from fastapi import Depends, HTTPException, status, Request, Header
from sqlalchemy.orm import Session
import jwt
from models import User
import requests

from db.session import SessionLocal
from core.config import settings

def get_db() -> Generator:
    db = SessionLocal()
    db.current_user_id = None

    try:
        yield db
    finally:
        db.close()


async def get_cognito_public_key(kid):
    cognito_jwks_url = settings.COGNITO_URL
    # cognito_jwks_url = cognito_jwks_url.format(region="us-east-1", userPoolId="us-east-1_3p6b7Ig1l")
    jwks = requests.get(cognito_jwks_url).json()
    for key in jwks["keys"]:
        if key["kid"] == kid:
            return key
    return None


async def get_current_user(Authorization:  str = Header(...), db: Session = Depends(get_db)) -> User:
    # credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Could not validate credentials",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    #
    # user_id = auth.cognito_id
    # if user_id is None:
    #     raise credentials_exception
    #
    # user = user_service.get_by_id(db, user_id)
    # if user is None:
    #     raise credentials_exception
    # return user
    try:
        decoded_token = jwt.decode(Authorization, options={"verify_signature": False})
        kid = decoded_token.get("kid")
        public_key = await get_cognito_public_key(kid)
        if public_key:
            decoded_token = jwt.decode(Authorization, public_key, algorithms=["RS256"], audience="your_app_client_id")
            return decoded_token
        else:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.DecodeError:
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

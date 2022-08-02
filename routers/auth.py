import os
import json
from typing import Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_sqlalchemy import db
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models import User


router = APIRouter(prefix="/auth", tags=["auth"])

load_dotenv(".env")
config = Config('.env')
oauth = OAuth(config)

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/google/callback')


oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


def get_user(email: str, provider: str):
    user = db.session.query(User).filter_by(email=email, provider=provider).first()
    return user


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        provider: str = payload.get("provider")
        if email is None or provider is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(email=email, provider=provider)
    if user is None:
        raise credentials_exception
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.get('/')
async def homepage(request: Request):
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        html = (
            f'<pre>{data}</pre>'
            '<a href="/auth/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')


@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    response_user: UserInfoResponse = UserInfoResponse.parse_obj(token.get('userinfo'))
    provider = "google"
    if response_user:
        user_model: User = db.session.query(User).filter_by(email=response_user.email, provider=provider).first()
        if user_model is None:
            user_create = User(
                full_name=response_user.given_name,
                email=response_user.email,
                is_admin=False,
                picture_url=response_user.picture,
                receive_notifications=True,
                wins=0,
                provider=provider
            )
            db.session.add(user_create)
            db.session.commit()
            user_model = db.session.query(User).filter_by(email=response_user.email).first()
        request.session['user'] = dict(response_user)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user",
            header={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_model.email, "provider": provider}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/auth')


@router.get('/test')
async def test(current_user: User = Depends(get_current_user)):
    return current_user


class UserInfoResponse(BaseModel):
    iss: str
    azp: str
    aud: str
    sub: str
    email: str
    email_verified: bool
    at_hash: str
    nonce: str
    name: str
    picture: str
    given_name: str
    family_name: str
    locale: str
    iat: float
    exp: float


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: float
    user_info: UserInfoResponse = Field(alias="userinfo")
    id: Optional[str] = None


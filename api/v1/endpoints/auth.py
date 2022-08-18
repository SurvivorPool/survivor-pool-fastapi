import json
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from jose import JWTError, jwt
from models.user import User
from schemas.user import UserCreate, UserResponse
import crud
from api import dependencies
from core.config import settings


router = APIRouter(prefix="/auth", tags=["auth"])

config = Config('.env')
oauth = OAuth(config)

ACCESS_TOKEN_EXPIRE_MINUTES = 120
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile',
        'access_type': 'offline',
        'prompt': 'consent',
    },
)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    print(to_encode)
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
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
    return await oauth.google.authorize_redirect(request, redirect_uri, access_type="offline")


@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(dependencies.get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user_info = token.get('userinfo')
    refresh_token = token.get('refresh_token')
    provider = "google"
    if user_info:
        user_model: User = crud.user.get_by_email_and_provider(db, email=user_info.email, provider=provider)
        if user_model is None:
            user_create = UserCreate(
                full_name=user_info.given_name,
                email=user_info.email,
                is_admin=False,
                picture_url=user_info.picture,
                receive_notifications=True,
                wins=0,
                provider=provider
            )
            crud.user.create(db, obj_in=user_create)
            user_model = crud.user.get_by_email_and_provider(db, email=user_info.email, provider=provider)
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
    return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
            }


@router.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/auth')


@router.get('/test', response_model=UserResponse)
async def test(current_user: User = Depends(dependencies.get_current_user)):
    return current_user


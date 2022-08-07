import os
import json
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models.user import User
from schemas.user import UserCreate, UserResponse
import crud
import dependencies


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


def get_user(db: Session, email: str, provider: str):
    user = crud.user.get_by_email_and_provider(db=db, email=email, provider=provider)
    return user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(dependencies.get_db)):
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
    user = get_user(db=db, email=email, provider=provider)
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
async def google_callback(request: Request, db: Session = Depends(dependencies.get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user_info = token.get('userinfo')
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
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/auth')


@router.get('/test', response_model=UserResponse)
async def test(current_user: User = Depends(get_current_user)):
    return current_user


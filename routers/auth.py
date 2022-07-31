import os
from fastapi import APIRouter
from fastapi_sso.sso.google import GoogleSSO
from fastapi_sqlalchemy import db
from starlette.requests import Request
from dotenv import load_dotenv
from models import User


load_dotenv(".env")
router = APIRouter(prefix="/auth", tags=["auth"])
google_sso = GoogleSSO(
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    scope=["openid", "email", "profile"],
    allow_insecure_http=os.environ["DEBUG"]
)


@router.get("/google/login")
async def google_login(request: Request):
    """Generate login url and redirect"""
    return await google_sso.get_login_redirect(redirect_uri=request.url_for("google_callback"))


@router.get("/google/callback")
async def google_callback(request: Request):
    """Process login response from Google and return user info"""
    sso_user = await google_sso.verify_and_process(request)
    user_model = db.session.query(User).filter_by(email=sso_user.email).first()

    if user_model is None:
        user_create = User(
            full_name=sso_user.display_name,
            email=sso_user.email,
            is_admin=False,
            picture_url=sso_user.picture,
            receive_notifications=True,
            wins=0
        )
        db.session.add(user_create)
        db.session.commit()
        user_model = db.session.query(User).filter_by(email=sso_user.email).first()

    return {
        "id": user_model.id,
        "picture": user_model.picture_url,
        "display_name": user_model.full_name,
        "email": user_model.email,
        "provider": sso_user.provider,
    }
from routes import router
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from starlette.config import Config
from urllib.parse import urlencode
from database import init_db
from sqlmodel import Session, select
from database import get_session
from models import User, Post
from routes import router
import os
import json
from dotenv import load_dotenv

load_dotenv()

# fastapi instance and middleware
app = FastAPI()
app.add_middleware(SessionMiddleware,
                   secret_key=os.getenv("SECRET", "!supersecret"))

# db initialize


@app.on_event("startup")
def on_startup():
    init_db()


# Oauth config
config = Config('.env')
oauth = OAuth(config)
oauth.register(
    name='auth0',
    client_id=os.getenv("AUTH0_CLIENT_ID"),
    client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        'scope': 'openid profile email'
    },
    server_metadata_url=f"https://{os.getenv('AUTH0_DOMAIN')}/.well-known/openid-configuration"
)

# auth0 variables
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
# change if want redirect different after logout
REDIRECT_AFTER_LOGOUT = "http://127.0.0.1:8000/login"

# auth login


@app.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for("callback")
    return await oauth.auth0.authorize_redirect(request, redirect_uri)

# auth callback


@app.get('/callback')
async def callback(request: Request, db: Session = Depends(get_session)):
    token = await oauth.auth0.authorize_access_token(request)

    user_info = token.get("userinfo") or {}
    email = user_info.get("email")
    if not email:
        raise HTTPException(
            status_code=400, detail="Email not found in user info")

    # add email into user table
    existing = db.exec(select(User).where(User.email == email)).first()
    if not existing:
        user = User(email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user = existing

    request.session["user"] = {"id": user.id, "email": user.email}
    # change if want redirect different after login
    return RedirectResponse(url='/posts')

# auth logout


@app.get('/logout')
async def logout(request: Request):
    request.session.clear()

    params = urlencode({
        "client_id": AUTH0_CLIENT_ID,
        "returnTo": REDIRECT_AFTER_LOGOUT,
    })
    logout_url = f"https://{AUTH0_DOMAIN}/v2/logout?{params}"

    return RedirectResponse(url=logout_url)

app.include_router(router)
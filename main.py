from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from starlette.config import Config
from database import init_db
from sqlmodel import Session
from models import User, Post
import os
import json
from dotenv import load_dotenv

load_dotenv()

# fastapi instance and middleware
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET", "!supersecret"))

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


# auth0 dependency
def require_login(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


# auth0 variables
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
REDIRECT_AFTER_LOGOUT = "http://127.0.0.1:8000/login"

# auth login
@app.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for("callback")
    return await oauth.auth0.authorize_redirect(request, redirect_uri)

# auth callback
@app.get('/callback')
async def callback(request: Request):
    token = await oauth.auth0.authorize_access_token(request)

    user_info = token.get("userinfo")
    request.session["user"] = dict(user_info)
    return RedirectResponse(url='/posts')

# auth logout
@app.get('/logout')
async def logout(request: Request):
    request.session.clear()

    logout_url = (
        f"https://{AUTH0_DOMAIN}/v2/logout"
        f"?client_id={AUTH0_CLIENT_ID}"
        f"&returnTo={REDIRECT_AFTER_LOGOUT}"
    )

    return RedirectResponse(url=logout_url)

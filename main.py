from routes import router
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from starlette.config import Config
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import urlencode
from database import init_db
from sqlmodel import Session, select
from database import get_session
from models import User, Post
import os
import json
from dotenv import load_dotenv
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("api")

load_dotenv()

# fastapi instance and middleware
app = FastAPI()
app.add_middleware(SessionMiddleware,
                   secret_key=os.getenv("SECRET", "!supersecret"))

origins = [
    "http://localhost:5173",  # Vite dev server
    # add production URLs 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# db initialize
@app.on_event("startup")
async def on_startup():
    init_db()
    logger.info("Application startup complete")
    logger.info("Login page available at: http://127.0.0.1:8000/login")
    logger.info("Posts page available at: http://127.0.0.1:8000/posts")


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
REDIRECT_AFTER_LOGOUT = "http://localhost:5173/"

# set of admin emails
admin_emails = {e.strip().lower() for e in os.getenv("ADMIN_EMAILS", "").split(",") if e.strip()}


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
    else:
        user = existing

    # check if user is admin
    if email.lower() in admin_emails:
        user.is_admin = True

    db.add(user)
    db.commit()
    db.refresh(user)

    request.session["user"] = {"id": user.id, "email": user.email, "is_admin": user.is_admin}
    # change if want redirect different after login
    return RedirectResponse(url='http://localhost:5173/')

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

# health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(router)

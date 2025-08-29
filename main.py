from fastapi import FastAPI, Depends
from database import init_db
from sqlmodel import Session
from models import User, Post

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

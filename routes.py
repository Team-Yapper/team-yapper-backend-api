from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlmodel import Session
from database import get_session
from models import Post

router = APIRouter()

@router.get("/posts/{post_id}")
def read_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post.content

@router.get("/posts/{post_id}/info")
def read_post_info(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {
        "id": post.id,
        "content": post.content,
        "user_id": post.user_id,
        "user": {
            "id": post.user.id,
            "email": post.user.email
        } if post.user else None
    }


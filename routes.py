from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlmodel import Session,select
from database import get_session
from models import Post

router = APIRouter()

# Get a specific post by ID
@router.get("/posts/{post_id}")
def read_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post.content

# Get post with user info
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
# Get all posts for a specific user
@router.get("/users/{user_id}/posts")
def get_user_posts(user_id: int, session: Session = Depends(get_session)):
    posts = session.exec(select(Post).where(Post.user_id == user_id)).all()
    if not posts:
        return {"message": "User has no posts."}
    return posts



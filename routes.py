from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from database import get_session
from models import Post, User
from pydantic import BaseModel

router = APIRouter()


class PostCreate(BaseModel):
    content: str

# auth0 dependency


def require_login(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


@router.get("/posts")
def get_all_posts(session: Session = Depends(get_session)):
    try:
        statement = select(Post)
        posts = session.exec(statement).all()
        return posts
    except Exception as e:
        # Catch any unexpected error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching posts: {str(e)}"
        )


@router.post("/posts")
def create_post(post: PostCreate, user: dict = Depends(require_login), session: Session = Depends(get_session)):
    # Grab the user from DB
    db_user = session.exec(select(User).where(
        User.email == user["email"])).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create new Post
    new_post = Post(content=post.content, user_id=db_user.id)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post

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
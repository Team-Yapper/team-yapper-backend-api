from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session
from models import Post, User
from pydantic import BaseModel

router = APIRouter()


class PostCreate(BaseModel):
    content: str
    user_email: str


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
def create_post(post: PostCreate, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(
        User.email == post.user_email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_post = Post(content=post.content, user_id=user.id)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post

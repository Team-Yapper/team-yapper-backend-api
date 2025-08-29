from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session
from models import Post

router = APIRouter()


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

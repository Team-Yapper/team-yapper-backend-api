from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from typing import List
from database import get_session
from models import Post, User
from pydantic import BaseModel
from schemas import PostRead

router = APIRouter()


class PostCreate(BaseModel):
    content: str

# auth0 dependency
def require_login(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


# @router.get("/posts")
# def get_all_posts(session: Session = Depends(get_session)):
#     try:
#         statement = select(Post)
#         posts = session.exec(statement).all()
#         return posts
#     except Exception as e:
#         # Catch any unexpected error
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"An error occurred while fetching posts: {str(e)}"
#         )

@router.get("/posts", response_model=List[PostRead])
def get_all_posts(session: Session = Depends(get_session)):
    try:
        statement = select(Post).options(selectinload(Post.user))
        posts = session.exec(statement).all()

        # Map posts to PostRead schema including user's email
        return [
            PostRead(
                id=post.id,
                content=post.content,
                user_id=post.user_id,
                user_email=post.user.email if post.user else None
            )
            for post in posts
        ]

    except Exception:
        # Generic error message is safer for production
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="There was an error fetching posts."
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

# Get content of a specific post
@router.get("/posts/{post_id}")
def read_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {
        "id": post.id,
        "content": post.content,
        "user": {
            "id": post.user.id,
            "email": post.user.email
        } if post.user else None
    }

# Get detailed info about a specific post
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
            "email": post.user.email
        } if post.user else None
    }

 # Get all posts for a specific user
@router.get("/user/{user_id}/posts")
def get_user_posts(user_id: int, session: Session = Depends(get_session)):
    # checks if the user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # User exists → get posts
    posts = session.exec(select(Post).where(Post.user_id == user_id)).all()
    # Format the posts (empty list is fine)
    filtered_posts = [
        {"id": post.id, "content": post.content} 
        for post in posts
    ]
    return {
        "email": user.email,
        "posts": filtered_posts,  # Will be [] when user has no posts
    }


# UPDATE post route
@router.patch('/posts/{post_id}')
def update_post(post_id: int,
                post: PostCreate,
                user: dict = Depends(require_login),
                session: Session = Depends(get_session)):

    # get post from db
    db_post = session.get(Post, post_id)

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    # ensure the logged in user is the owner of the post
    db_user = session.exec(select(User).where(
        User.email == user["email"])).first()

    # also checks if a user is an admin
    if db_post.user_id != db_user.id and not db_user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")

    # update post content
    db_post.content = post.content
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


# DELETE post route
@router.delete('/posts/{post_id}')
def delete_post(post_id: int,
                user: dict = Depends(require_login),
                session: Session = Depends(get_session)):

    # get post from db
    db_post = session.get(Post, post_id)

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    # ensure the logged in user is the owner of the post
    db_user = session.exec(select(User).where(
        User.email == user["email"])).first()

    # also checks if a user is an admin
    if db_post.user_id != db_user.id and not db_user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")

    # delete post
    session.delete(db_post)
    session.commit()
    return {"message": "Post deleted successfully"}

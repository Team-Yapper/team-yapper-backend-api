import sys
from pathlib import Path

# allow imports from project root
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app, get_session
from models import User, Post

# Create in-memory test database
@pytest.fixture(name="session") 
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine) 
    with Session(engine) as session:
        yield session

#add client fixture
@pytest.fixture(name="client") 
def client_fixture(session: Session):
    def get_session_override():
        return session

# override the get_session dependency
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Test reading a specific post
def test_read_post_success(client: TestClient, session: Session):
    # Create a user
    user = User(email="test@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    post = Post(content="Hello this is my yapper post!", user_id=user.id)
    session.add(post)
    session.commit()
    session.refresh(post)

    response = client.get(f"/posts/{post.id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": post.id,
        "content": "Hello this is my yapper post!",
        "user": {
            "id": user.id,
            "email": "test@example.com"
        }
    }

# Test reading a non-existent post
def test_read_post_invalid_id(client: TestClient):
    response = client.get("/posts/abc")
    assert response.status_code == 422

#Test reading a specific posts info
def test_read_post_info_success(client: TestClient, session: Session):
    # Create a user
    user = User(email="test@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create a post linked to the user
    post = Post(content="Hello this is my yapper post!", user_id=user.id)
    session.add(post)
    session.commit()
    session.refresh(post)

    # Call the endpoint
    response = client.get(f"/posts/{post.id}/info")

    # Validate response
    assert response.status_code == 200
    assert response.json() == {
        "id": post.id,
        "content": "Hello this is my yapper post!",
        "user_id": user.id,
        "user": {
            "email": "test@example.com"
        }
    }

# Test reading a non-existent post
def test_read_post_info_not_found(client: TestClient):
    response = client.get("/posts/999/info")
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}

# Test getting all posts for a specific user
def test_get_user_posts_success(client: TestClient, session: Session):
    # Create a user
    user = User(email="test@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create posts for the user
    post1 = Post(content="First post", user_id=user.id)
    post2 = Post(content="Second post", user_id=user.id)
    session.add(post1)
    session.add(post2)
    session.commit()

    # Call the endpoint
    response = client.get(f"/user/{user.id}/posts")

    assert response.status_code == 200
    assert response.json() == {
        "email": "test@example.com",
        "posts": [
            {"id": post1.id, "content": "First post"},
            {"id": post2.id, "content": "Second post"}
        ]
    }

# Test getting posts for a user with no posts
def test_get_user_posts_empty_list(client: TestClient, session: Session):
    # Create a user with no posts
    user = User(email="test@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Call endpoint
    response = client.get(f"/user/{user.id}/posts")

    assert response.status_code == 200
    assert response.json() == {
        "email": "test@example.com",
        "posts": []
    }

# Test getting posts for a non-existent user
def test_get_user_posts_user_not_found(client: TestClient):
    response = client.get("/user/999/posts")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
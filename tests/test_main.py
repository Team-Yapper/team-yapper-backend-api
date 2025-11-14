import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, select
from sqlmodel.pool import StaticPool
from unittest.mock import AsyncMock, patch, MagicMock

# Add parent directory to path so we can import from root
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app, get_session
from models import User, SQLModel, Post

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


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# Test login route
def test_login_redirect(client: TestClient):
    response = client.get("/login", follow_redirects=False)
    assert response.status_code == 302  # Redirect status
    assert "auth0" in response.headers["location"].lower()


# Test callback with new user
@pytest.mark.asyncio
async def test_callback_new_user(client: TestClient, session: Session):
    mock_token = {
        "userinfo": {
            "email": "newuser@example.com",
            "sub": "auth0|123"
        }
    }

    with patch('main.oauth.auth0.authorize_access_token', new_callable=AsyncMock) as mock_auth:
        mock_auth.return_value = mock_token

        response = client.get("/callback")

        # Check user was created
        user = session.exec(
            select(User).where(User.email == "newuser@example.com")
        ).first()
        assert user is not None
        assert user.email == "newuser@example.com"
        assert user.is_admin is False


# Test callback with admin user
@pytest.mark.asyncio
async def test_callback_admin_user(client: TestClient, session: Session):
    mock_token = {
        "userinfo": {
            "email": "jmhfullstack@gmail.com",
            "sub": "auth0|456"
        }
    }

    with patch('main.oauth.auth0.authorize_access_token', new_callable=AsyncMock) as mock_auth:
        mock_auth.return_value = mock_token

        response = client.get("/callback")

        # Check admin user was created with is_admin=True
        user = session.exec(
            select(User).where(User.email == "jmhfullstack@gmail.com")
        ).first()
        assert user is not None
        assert user.is_admin is True


# Test callback with existing user
@pytest.mark.asyncio
async def test_callback_existing_user(client: TestClient, session: Session):
    # Create existing user
    existing_user = User(email="existing@example.com", is_admin=False)
    session.add(existing_user)
    session.commit()

    mock_token = {
        "userinfo": {
            "email": "existing@example.com",
            "sub": "auth0|789"
        }
    }

    with patch('main.oauth.auth0.authorize_access_token', new_callable=AsyncMock) as mock_auth:
        mock_auth.return_value = mock_token

        response = client.get("/callback")

        # Check user still exists (no duplicate)
        users = session.exec(select(User).where(User.email == "existing@example.com")).all()
        assert len(users) == 1


# Test callback with missing email
@pytest.mark.asyncio
async def test_callback_missing_email(client: TestClient, session: Session):
    mock_token = {
        "userinfo": {}  # No email
    }

    with patch('main.oauth.auth0.authorize_access_token', new_callable=AsyncMock) as mock_auth:
        mock_auth.return_value = mock_token

        response = client.get("/callback")
        assert response.status_code == 400


# Test logout clears session
def test_logout_clears_session(client: TestClient):
    # Set a session first
    with client:
        client.get("/logout", follow_redirects=False)
        # Session should be cleared
        assert len(client.cookies) == 0 or client.session.get("user") is None


# Test logout redirect to Auth0
def test_logout_redirect(client: TestClient):
    response = client.get("/logout", follow_redirects=False)
    assert response.status_code == 307
    assert "auth0" in response.headers["location"].lower()
    assert "logout" in response.headers["location"].lower()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Test reading a specific post
def test_read_post_success(client: TestClient, session: Session):
    # Create a user
    user = User(email="test@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    post = Post(content="Hello!", user_id=user.id)
    session.add(post)
    session.commit()
    session.refresh(post)

    response = client.get(f"/posts/{post.id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": post.id,
        "content": "Hello!",
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
    post = Post(content="Hello info!", user_id=user.id)
    session.add(post)
    session.commit()
    session.refresh(post)

    # Call the endpoint
    response = client.get(f"/posts/{post.id}/info")

    # Validate response
    assert response.status_code == 200
    assert response.json() == {
        "id": post.id,
        "content": "Hello info!",
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
import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, select
from sqlmodel.pool import StaticPool
from unittest.mock import AsyncMock, patch, MagicMock

# Add parent directory to path so we can import from root
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import User, SQLModel, Post
from main import app, get_session
from routes import require_login

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
    
    # Mock logged-in user
    def require_login_override():
        return {"email": "testuser@example.com"}

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[require_login] = require_login_override
    
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


# Test that there are no posts yet
def test_get_all_posts_empty(client):
    response = client.get("/posts")
    assert response.status_code == 200
    # data hasn't been added yet, so expect this to be empty
    assert response.json() == []

# Test to check /GET all posts
def test_get_all_posts_with_data(client, session):
    # create a user and posts
    user = User(email="test@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    post1 = Post(content="First post", user_id=user.id)
    post2 = Post(content="Second post", user_id=user.id)
    session.add_all([post1, post2])
    session.commit()

    # get all posts created
    response = client.get("/posts")

    # assert that the data is correct
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 2
    assert posts[0]["content"] == "First post"
    assert posts[1]["content"] == "Second post"

# Test to check /GET/{post_id}
def test_get_post_by_id(client, session):
    # Create test user
    user = User(email="testuser@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create test post
    post = Post(content="Specific post", user_id=user.id)
    session.add(post)
    session.commit()
    session.refresh(post)

    # get /posts/{post_id}
    response = client.get(f"/posts/{post.id}")
    assert response.status_code == 200

    # FastAPI serializes plain strings as JSON strings
    assert response.json() == f"Post: {post.content}"


# Test to check /POST a new post
def test_create_post(client, session):
    # create a user
    user = User(email="testuser@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    payload = {"content": "Hello world"}

    # make /POST request
    response = client.post("/posts", json=payload)

    # assert that the data is correct
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["content"] == "Hello world"
    assert data["user_id"] == user.id
    assert "id" in data

# Test that data is persistent
def test_create_post_persists(client, session):
    user = User(email="testuser@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    payload = {"content": "Persistent post"}
    client.post("/posts", json=payload)

    posts = session.exec(select(Post)).all()
    assert len(posts) == 1
    assert posts[0].content == "Persistent post"
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

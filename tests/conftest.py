import sys
from pathlib import Path

# allow imports from project root
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

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

#add client fixture
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
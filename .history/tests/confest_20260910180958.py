import pytest
from fastapi.testclient import TestClient
import app.models 
from sqlalchemy import create_engine
from app.dependencies import get_current_user
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db, Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    

@pytest.fixture(scope="function")
def client(test_db):
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers():
    """Return headers with a valid JWT for an authenticated request."""
    from app.core.security import create_access_token
    token = create_access_token("test-user-id")
    return {"Authorization": f"Bearer {token}"}


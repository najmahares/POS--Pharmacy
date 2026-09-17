# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db, Base # Assuming your DB setup is here

# 1. Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# 2. Create the test engine and session factory
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. This is the core fixture that sets up and tears down the test database
@pytest.fixture(scope="function")
def test_db():
    # Create all tables in the test database before each test
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables after each test to ensure isolation
    Base.metadata.drop_all(bind=engine)

# 4. This fixture creates a test client and overrides the DB dependency
@pytest.fixture(scope="function")
def client(test_db): # Note: This depends on the test_db fixture
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    # This is the key line: it tells FastAPI to use override_get_db during tests
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    # Clean up the override after the test is done
    app.dependency_overrides.clear()
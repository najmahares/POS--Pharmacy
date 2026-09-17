import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models.user import User
from app.core.security import hash_password, create_access_token



SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_db):
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(test_db):
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def client_no_auth(client):
    """Alias used by security tests."""
    return client


def _make_user(db, username, role, password="Pass123!"):
    user = User(
        id=uuid.uuid4(),
        username=username,
        email=f"{username}@test.com",
        password_hash=hash_password(password),
        first_name=username.title(),
        last_name="Test",
        role=role,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def admin_user(db_session):
    return _make_user(db_session, "admin_test", "admin")


@pytest.fixture
def cashier_user(db_session):
    return _make_user(db_session, "cashier_test", "cashier")


@pytest.fixture
def pharmacist_user(db_session):
    return _make_user(db_session, "pharmacist_test", "pharmacist")


@pytest.fixture
def inventory_user(db_session):
    return _make_user(db_session, "inventory_test", "inventory-manager")



@pytest.fixture
def auth_headers(admin_user):
    return {"Authorization": f"Bearer {create_access_token(str(admin_user.id))}"}


@pytest.fixture
def cashier_headers(cashier_user):
    return {"Authorization": f"Bearer {create_access_token(str(cashier_user.id))}"}


@pytest.fixture
def pharmacist_headers(pharmacist_user):
    return {"Authorization": f"Bearer {create_access_token(str(pharmacist_user.id))}"}


@pytest.fixture
def inventory_headers(inventory_user):
    return {"Authorization": f"Bearer {create_access_token(str(inventory_user.id))}"}
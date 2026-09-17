cat > tests/conftest.py << 'EOF'
import uuid
from datetime import datetime, date, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.customer import Customer
from app.models.supplier import Supplier
from app.models.sale import Sale
from app.core.security import hash_password, create_access_token

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@event.listens_for(engine, "connect")
def _fk_on(dbapi_conn, _):
    cur = dbapi_conn.cursor()
    cur.execute("PRAGMA foreign_keys=ON")
    cur.close()


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
    return client


def _make_user(db, username, role, password="Pass123!", is_active=True):
    user = User(
        id=uuid.uuid4(),
        username=username,
        email=f"{username}@test.com",
        password_hash=hash_password(password),
        first_name=username.title(),
        last_name="Test",
        role=role,
        is_active=is_active,
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
def inactive_user(db_session):
    return _make_user(db_session, "inactive_test", "cashier", is_active=False)


def _hdr(user):
    return {"Authorization": f"Bearer {create_access_token(str(user.id))}"}


@pytest.fixture
def auth_headers(admin_user):
    return _hdr(admin_user)


@pytest.fixture
def cashier_headers(cashier_user):
    return _hdr(cashier_user)


@pytest.fixture
def pharmacist_headers(pharmacist_user):
    return _hdr(pharmacist_user)


@pytest.fixture
def inventory_headers(inventory_user):
    return _hdr(inventory_user)


@pytest.fixture
def inactive_headers(inactive_user):
    return _hdr(inactive_user)


@pytest.fixture
def category(db_session):
    c = Category(id=uuid.uuid4(), name=f"Cat-{uuid.uuid4().hex[:6]}", is_active=True)
    db_session.add(c)
    db_session.commit()
    db_session.refresh(c)
    return c


@pytest.fixture
def supplier(db_session):
    s = Supplier(
        id=uuid.uuid4(),
        company_name="Acme Pharma",
        email=f"acme_{uuid.uuid4().hex[:6]}@test.com",
        is_active=True,
    )
    db_session.add(s)
    db_session.commit()
    db_session.refresh(s)
    return s


@pytest.fixture
def product(db_session, category, supplier):
    p = Product(
        id=uuid.uuid4(),
        name="Paracetamol 500mg",
        sku=f"SKU-{uuid.uuid4().hex[:8]}",
        unit_price="10.00",
        cost_price="4.00",
        quantity_in_stock=100,
        reorder_level=10,
        expiry_date=date.today() + timedelta(days=365),
        requires_prescription=False,
        controlled_substance=False,
        is_active=True,
        category_id=category.id,
        supplier_id=supplier.id,
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p


@pytest.fixture
def rx_product(db_session, category):
    p = Product(
        id=uuid.uuid4(),
        name="Amoxicillin 500mg",
        sku=f"RX-{uuid.uuid4().hex[:8]}",
        unit_price="25.00",
        cost_price="10.00",
        quantity_in_stock=50,
        reorder_level=5,
        expiry_date=date.today() + timedelta(days=180),
        requires_prescription=True,
        controlled_substance=False,
        is_active=True,
        category_id=category.id,
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p


@pytest.fixture
def customer(db_session):
    c = Customer(
        id=uuid.uuid4(),
        first_name="Jane",
        last_name="Doe",
        email=f"jane_{uuid.uuid4().hex[:6]}@test.com",
        medical_record_number=f"MRN-{uuid.uuid4().hex[:8]}",
        is_active=True,
    )
    db_session.add(c)
    db_session.commit()
    db_session.refresh(c)
    return c


@pytest.fixture
def sale(db_session, admin_user, customer):
    s = Sale(
        id=uuid.uuid4(),
        sale_number=f"SAL-{uuid.uuid4().hex[:8]}",
        sale_date=datetime.utcnow(),
        subtotal="10.00",
        tax_amount="1.00",
        discount_amount="0",
        total_amount="11.00",
        status="pending",
        user_id=admin_user.id,
        customer_id=customer.id,
    )
    db_session.add(s)
    db_session.commit()
    db_session.refresh(s)
    return s
EOF
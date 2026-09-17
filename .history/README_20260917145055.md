# POS System: Hospital Pharmacy Point of Sale

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/python-3.10+-blue.svg">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-0.104-009688.svg">
  <img alt="SQLAlchemy" src="https://img.shields.io/badge/SQLAlchemy-2.0-red.svg">
  <img alt="Tests" src="https://img.shields.io/badge/tests-88%20passing-brightgreen.svg">
  
</p>

A production-grade REST API backend for a hospital and retail pharmacy point-of-sale system. Built with FastAPI, SQLAlchemy 2.0, and PostgreSQL, with a comprehensive 88-test automated suite covering authentication, role-based access control, inventory integrity, and financial correctness.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Domain Model](#domain-model)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Authentication and Authorization](#authentication-and-authorization)
- [Testing](#testing)
- [Continuous Integration](#continuous-integration)
- [Project Structure](#project-structure)
- [Design Decisions](#design-decisions)
- [Roadmap](#roadmap)
- [License](#license)

## Overview

This project implements the backend for a pharmacy POS system designed for hospital pharmacies, retail chains, and clinic dispensaries. It handles the full transaction lifecycle including patient registration, prescription dispensing, multi-method payments, and receipt generation, while enforcing regulatory and clinical constraints like prescription requirements and controlled-substance tracking.

The API is built around nine core entities, protected by JWT-based authentication with fine-grained role-based permissions, and validated by a test suite that specifically targets inventory integrity and financial precision.

## Key Features

### Security

- JWT authentication with access and refresh tokens
- Passwords hashed with bcrypt via passlib
- Role-based access control across five user roles
- user_id on every transaction sourced from the JWT subject, never the request body
- Same-millisecond token uniqueness via jti claim
- Username-enumeration-safe login errors

### Inventory and Sales

- Atomic stock decrement on every sale item
- Oversell prevention rejects any sale exceeding available stock
- Non-negative invariant, stock can never go below zero
- Low-stock and expired-product alert endpoints
- Product batch and expiry tracking

### Financial Correctness

- All monetary values use Decimal, no float drift
- Exact line-total calculation: quantity x unit_price - discount + tax
- Split payments supported, one sale can have many payments
- Multi-method support: cash, credit card, debit card, mobile wallet, insurance, bank transfer

### Data Integrity

- Unique constraints on sku, sale_number, email, medical_record_number
- Foreign-key enforcement with SQLite PRAGMA foreign_keys enabled in tests
- Cascade-protected deletes, cannot remove a category with products
- Atomic multi-step operations with rollback on failure

### Developer Experience

- Interactive Swagger UI at /docs
- ReDoc at /redoc
- 88 automated tests with in-memory SQLite, no external DB required
- GitHub Actions CI on every push and pull request

## Domain Model

The system is built around nine entities:

| Entity   | Purpose                                                                   |
| -------- | ------------------------------------------------------------------------- |
| User     | Staff accounts (admin, pharmacist, pharmacy-technician, cashier, manager) |
| Category | Hierarchical classification                                               |
| Product  | Medication or item with SKU, price, stock, expiry, prescription flag      |
| Customer | Patient or walk-in with medical record, insurance, allergy data           |
| Supplier | Pharmaceutical distributor with lead time and payment terms               |
| Sale     | Transaction header with prescription info and status workflow             |
| SaleItem | Line item with snapshot pricing at time of sale                           |
| Payment  | Payment record supporting split payments                                  |
| Receipt  | Digital or printed receipt with regulatory text                           |

### Relationship Summary

```

Customer 1:N Sale 1:N SaleItem N:1 Product
| |
1 N
| |
v v
Receipt Category
^ |
| |
N N
| |
Payment Supplier

```

## Tech Stack

| Layer      | Technology                            |
| ---------- | ------------------------------------- |
| Language   | Python 3.10+                          |
| Framework  | FastAPI 0.104                         |
| ORM        | SQLAlchemy 2.0                        |
| Validation | Pydantic v2                           |
| Migrations | Alembic                               |
| Database   | PostgreSQL 14+ (prod), SQLite (tests) |
| Auth       | python-jose, passlib[bcrypt]          |
| Server     | Uvicorn                               |
| Testing    | pytest, pytest-cov, httpx             |
| CI         | GitHub Actions                        |

## Getting Started

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 14 or higher (only for local development, tests use SQLite)
- Git

### Installation

```bash
git clone git@github.com:najmahares/POS--Pharmacy.git
cd POS--Pharmacy

python3.10 -m venv env
source env/bin/activate
# On Windows use: env\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration

Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

### Environment Variables

| Variable                     | Description                     | Default    |
| ---------------------------- | ------------------------------- | ---------- |
| SECRET_KEY                   | JWT signing key, change in prod | change-me  |
| ALGORITHM                    | JWT algorithm                   | HS256      |
| ACCESS_TOKEN_EXPIRE_MINUTES  | Access token TTL                | 30         |
| REFRESH_TOKEN_EXPIRE_MINUTES | Refresh token TTL               | 10080      |
| DATABASE_URL                 | PostgreSQL connection string    | url        |
| PROJECT_NAME                 | Display name                    | POS System |
| API_V1_STR                   | API prefix                      | /api/v1    |

Never commit the .env file to version control. The .gitignore already excludes it.

## Running the Application

```bash
# Development with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production with multiple workers
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

Once running, access:

| URL                                | Description                 |
| ---------------------------------- | --------------------------- |
| http://localhost:8000/docs         | Swagger UI (interactive)    |
| http://localhost:8000/redoc        | ReDoc (read-only reference) |
| http://localhost:8000/health       | Health check                |
| http://localhost:8000/openapi.json | OpenAPI schema              |

## API Endpoints

All routes below require authentication unless noted. Role notation: A=admin, P=pharmacist, PT=pharmacy-technician, C=cashier, IM=inventory-manager, star=any authenticated user.

### Authentication /auth

| Method | Path             | Description            | Auth   |
| ------ | ---------------- | ---------------------- | ------ |
| POST   | /auth/register   | Register a new user    | Public |
| POST   | /auth/login      | Login with OAuth2 form | Public |
| POST   | /auth/login/json | Login with JSON body   | Public |
| POST   | /auth/refresh    | Exchange refresh token | Public |

### Users /users

| Method | Path        | Description  | Allowed |
| ------ | ----------- | ------------ | ------- |
| GET    | /users/     | List users   | A       |
| GET    | /users/me   | Current user | star    |
| GET    | /users/{id} | Get user     | A       |
| POST   | /users/     | Create user  | A       |
| PUT    | /users/{id} | Update user  | A       |
| DELETE | /users/{id} | Delete user  | A       |

### Categories /categories

| Method | Path                           | Description        | Allowed |
| ------ | ------------------------------ | ------------------ | ------- |
| GET    | /categories/                   | List categories    | star    |
| GET    | /categories/root               | Root categories    | star    |
| GET    | /categories/{id}/subcategories | Children of parent | star    |
| POST   | /categories/                   | Create             | A, IM   |
| PUT    | /categories/{id}               | Update             | A, IM   |
| DELETE | /categories/{id}               | Delete             | A       |

### Products /products

| Method | Path                    | Description         | Allowed |
| ------ | ----------------------- | ------------------- | ------- |
| GET    | /products/              | List products       | star    |
| GET    | /products/{id}          | Get product         | star    |
| GET    | /products/sku/{sku}     | Get by SKU          | star    |
| GET    | /products/category/{id} | By category         | star    |
| GET    | /products/low-stock     | Below reorder level | A, IM   |
| GET    | /products/expired       | Past expiry         | A, IM   |
| POST   | /products/              | Create              | A, IM   |
| PUT    | /products/{id}          | Update              | A, IM   |
| DELETE | /products/{id}          | Delete              | A       |

### Customers /customers

| Method | Path                            | Description | Allowed |
| ------ | ------------------------------- | ----------- | ------- |
| GET    | /customers/                     | List        | star    |
| GET    | /customers/{id}                 | Get         | star    |
| GET    | /customers/email/{email}        | By email    | star    |
| GET    | /customers/medical-record/{mrn} | By MRN      | star    |
| POST   | /customers/                     | Create      | star    |
| PUT    | /customers/{id}                 | Update      | star    |
| DELETE | /customers/{id}                 | Delete      | A       |

### Suppliers /suppliers

| Method | Path            | Description | Allowed |
| ------ | --------------- | ----------- | ------- |
| GET    | /suppliers/     | List        | star    |
| POST   | /suppliers/     | Create      | A, IM   |
| PUT    | /suppliers/{id} | Update      | A, IM   |
| DELETE | /suppliers/{id} | Delete      | A       |

### Sales /sales

| Method | Path                   | Description                   | Allowed |
| ------ | ---------------------- | ----------------------------- | ------- |
| GET    | /sales/                | List                          | star    |
| GET    | /sales/{id}            | Get                           | star    |
| GET    | /sales/sale-number/{n} | By number                     | star    |
| GET    | /sales/customer/{id}   | By customer                   | star    |
| GET    | /sales/user/{id}       | By cashier                    | A       |
| GET    | /sales/date-range/     | Date filter                   | A, P    |
| GET    | /sales/status/{s}      | By status                     | star    |
| POST   | /sales/                | Create, user_id auto from JWT | star    |
| PUT    | /sales/{id}            | Update                        | A       |
| PATCH  | /sales/{id}/status     | Change status                 | A, P    |
| DELETE | /sales/{id}            | Delete                        | A       |

### Sale Items /sale-items

| Method | Path                       | Description                | Allowed |
| ------ | -------------------------- | -------------------------- | ------- |
| GET    | /sale-items/               | List                       | star    |
| GET    | /sale-items/sale/{sale_id} | Items of a sale            | star    |
| POST   | /sale-items/               | Create and decrement stock | star    |
| POST   | /sale-items/bulk           | Bulk create                | star    |
| PUT    | /sale-items/{id}           | Update                     | A       |
| DELETE | /sale-items/{id}           | Delete                     | A       |

### Payments /payments

| Method | Path                     | Description         | Allowed |
| ------ | ------------------------ | ------------------- | ------- |
| GET    | /payments/               | List                | star    |
| GET    | /payments/sale/{sale_id} | Payments for a sale | star    |
| GET    | /payments/status/{s}     | By status           | star    |
| POST   | /payments/               | Create              | star    |
| PATCH  | /payments/{id}/status    | Update status       | star    |
| DELETE | /payments/{id}           | Delete              | A       |

### Receipts /receipts

| Method | Path                         | Description | Allowed |
| ------ | ---------------------------- | ----------- | ------- |
| GET    | /receipts/                   | List        | star    |
| GET    | /receipts/{id}               | Get         | star    |
| GET    | /receipts/receipt-number/{n} | By number   | star    |
| GET    | /receipts/sale/{sale_id}     | By sale     | star    |
| POST   | /receipts/                   | Create      | star    |
| PUT    | /receipts/{id}               | Update      | A       |
| DELETE | /receipts/{id}               | Delete      | A       |

## Authentication and Authorization

### Obtaining a Token

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=YourPassword"
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": "uuid-here",
    "username": "admin",
    "role": "admin"
  }
}
```

### Using a Token

```bash
curl -X GET "http://localhost:8000/products/" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### Role Permission Matrix

| Resource            | Admin | Pharmacist | Pharm-Tech | Cashier | Inv-Manager |
| ------------------- | :---: | :--------: | :--------: | :-----: | :---------: |
| Users (read/write)  |  Yes  |     No     |     No     |   No    |     No      |
| Categories (read)   |  Yes  |    Yes     |    Yes     |   Yes   |     Yes     |
| Categories (write)  |  Yes  |     No     |     No     |   No    |     Yes     |
| Categories (delete) |  Yes  |     No     |     No     |   No    |     No      |
| Products (read)     |  Yes  |    Yes     |    Yes     |   Yes   |     Yes     |
| Products (write)    |  Yes  |     No     |     No     |   No    |     Yes     |
| Products (delete)   |  Yes  |     No     |     No     |   No    |     No      |
| Customers (read)    |  Yes  |    Yes     |    Yes     |   Yes   |     Yes     |
| Customers (write)   |  Yes  |    Yes     |    Yes     |   Yes   |     Yes     |
| Customers (delete)  |  Yes  |     No     |     No     |   No    |     No      |
| Suppliers (write)   |  Yes  |     No     |     No     |   No    |     Yes     |
| Sales (create)      |  Yes  |    Yes     |    Yes     |   Yes   |     Yes     |
| Sales (status)      |  Yes  |    Yes     |     No     |   No    |     No      |
| Payments (create)   |  Yes  |    Yes     |    Yes     |   Yes   |     Yes     |
| Receipts (read)     |  Yes  |    Yes     |    Yes     |   Yes   |     Yes     |

## Testing

The project ships with 88 automated tests covering authentication, RBAC, inventory invariants, financial math, and data integrity. Tests use in-memory SQLite and require no external services.

### Running Tests

```bash
source env/bin/activate

# All tests
pytest tests/ -v

# With coverage report
pytest tests/ -v --cov=app --cov-report=term-missing

# Single file
pytest tests/test_auth.py -v

# Single test
pytest tests/test_auth.py::test_login_returns_both_tokens -v

# Stop on first failure
pytest tests/ -x
```

### Coverage by Area

| Area                   | Test File                             | Count |
| ---------------------- | ------------------------------------- | ----: |
| Authentication and JWT | test_auth.py, test_audit_and_security |    30 |
| RBAC matrix            | test_audit_and_security.py            |    13 |
| Inventory rules        | test_inventory_business_rules.py      |    10 |
| Data integrity         | test_data_integrity.py                |     6 |
| CRUD and validation    | test_products.py, test_root.py        |     6 |
| Password hashing       | test_audit_and_security.py            |     2 |
| Total                  |                                       |    88 |

### What the Suite Proves

- Stock decrements atomically: POST /sale-items/ reduces product.quantity_in_stock by exactly the sold quantity
- Oversell is rejected: requesting more than stock returns HTTP 400
- Non-negative invariant: repeated oversell attempts never leave stock below zero
- user_id comes from JWT: passing a forged user_id in the body is silently overridden
- Role boundaries enforced: cashier cannot create products, pharmacist cannot delete users
- Financial math exact: quantity x unit_price uses Decimal, not floats
- Duplicates rejected: SKU, sale number, email, medical record number

## Continuous Integration

Every push and pull request triggers the workflow in .github/workflows/tests.yml:

```yaml
name: Tests
on:
  push:
    branches: [main, master, develop]
  pull_request:
    branches: [main, master, develop]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
          cache: pip
      - run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - run: pytest tests/ -v --cov=app --cov-report=term-missing
```

View runs in the Actions tab of the GitHub repository.

## Project Structure

```
POS--Pharmacy/
  .github/
    workflows/
      tests.yml                    CI pipeline
  app/
    core/
      security.py                  JWT encode/decode, hashing
    models/                        SQLAlchemy ORM models
      user.py
      category.py
      product.py
      customer.py
      supplier.py
      sale.py
      sale_item.py
      payment.py
      receipt.py
    repositories/                  Data access layer
    routers/                       FastAPI endpoint groups
      auth.py
      user.py
      category.py
      product.py
      customer.py
      supplier.py
      sale.py
      sale_item.py
      payment.py
      receipt.py
    schemas/                       Pydantic request/response models
    services/                      Business logic
    config.py                      Settings loader
    database.py                    Engine, session, Base
    dependencies.py                Auth dependencies
    main.py                        FastAPI app factory
  tests/
    __init__.py
    conftest.py                    Fixtures, in-memory DB, users
    test_auth.py
    test_audit_and_security.py
    test_data_integrity.py
    test_inventory_business_rules.py
    test_products.py
    test_root.py
  .env.example
  .gitignore
  pytest.ini
  requirements.txt
  README.md
```

## Author

Najma H. at https://github.com/najmahares

Built as part of a backend engineering project FastAPI, SQLAlchemy, JWT authentication, role-based access control, and a rigorous pytest suite.

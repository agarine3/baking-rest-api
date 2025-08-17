# Banking REST API

A comprehensive banking REST service built with FastAPI, SQLAlchemy, and JWT authentication.

## Features

- User authentication and authorization
- Account management
- Transaction processing
- Money transfers
- Card management
- Statement generation
- Secure JWT-based authentication

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT tokens
- **Password Hashing**: bcrypt
- **Testing**: pytest
- **Documentation**: Auto-generated with FastAPI

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
```

3. Run database migrations:
```bash
alembic upgrade head
```

4. Start the server:
```bash
uvicorn app.main:app --reload
```

5. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
banking-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── api/
│   ├── core/
│   └── utils/
├── tests/
├── alembic/
├── docs/
└── requirements.txt
```

## Development

This project uses AI-driven development practices. See `AI_USAGE_LOG.md` for details on AI tool usage during development.

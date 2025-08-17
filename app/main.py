from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base

# Import all models to register them with SQLAlchemy
from app.models import User, Account, Transaction, Card, Statement

# Import API routes
from app.api import auth, accounts

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.project_name,
    debug=settings.debug,
    openapi_url=f"{settings.api_v1_str}/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router, prefix=settings.api_v1_str)
app.include_router(accounts.router, prefix=settings.api_v1_str)


@app.get("/")
async def root():
    return {"message": "Welcome to Banking REST API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Banking API is running"}


@app.get("/api/v1/")
async def api_root():
    return {"message": "Banking API v1", "endpoints": "/docs"}

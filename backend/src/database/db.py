# [Task: T051]
# [From: specs/1-full-stack-integration/tasks.md §US4, specs/1-full-stack-integration/spec.md §FR-009]
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool, NullPool
from sqlmodel import SQLModel
from contextlib import contextmanager
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/db")

def _strip_query_param(database_url: str, name: str) -> str:
    cleaned = re.sub(rf"([?&]){name}=[^&]*", "", database_url)
    cleaned = cleaned.replace("?&", "?").replace("&&", "&")
    return cleaned.rstrip("?&")


def _add_query_param(database_url: str, name: str, value: str) -> str:
    if f"{name}=" in database_url:
        return database_url
    separator = "&" if "?" in database_url else "?"
    return f"{database_url}{separator}{name}={value}"


def _render_database_url(drivername: str, database_url: str) -> str:
    url = make_url(database_url).set(drivername=drivername)
    return url.render_as_string(hide_password=False)


def _build_database_urls(database_url: str) -> tuple[str, str]:
    # Remove Neon parameters that are not accepted consistently by drivers.
    cleaned_url = _strip_query_param(database_url, "channel_binding")
    cleaned_url = _strip_query_param(cleaned_url, "options")
    driver = make_url(cleaned_url).drivername

    if driver.startswith("postgres") or driver == "postgresql":
        async_url = _render_database_url("postgresql+asyncpg", cleaned_url)
        sync_url = _render_database_url("postgresql+psycopg2", cleaned_url)
    elif driver.startswith("sqlite"):
        async_url = _render_database_url("sqlite+aiosqlite", cleaned_url)
        sync_url = _render_database_url("sqlite", cleaned_url)
    else:
        async_url = cleaned_url
        sync_url = cleaned_url

    for url_name, url_value in (("ASYNC", async_url), ("SYNC", sync_url)):
        if "neon.tech" in url_value and "pooler" in url_value:
            url_value = _add_query_param(url_value, "sslmode", "require")
            url_value = _add_query_param(url_value, "connect_timeout", "10")
        if url_name == "ASYNC":
            async_url = url_value
        else:
            sync_url = url_value

    return async_url, sync_url


ASYNC_DATABASE_URL, SYNC_DATABASE_URL = _build_database_urls(DATABASE_URL)

# Create async engine for async operations
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    # Neon Serverless optimized settings
    poolclass=NullPool,   # Use NullPool for async engines
    pool_pre_ping=True,   # Verify connections before use (critical for serverless)
    pool_recycle=300,     # Recycle connections to prevent serverless timeout issues
    echo=False            # Set to True for SQL query logging during development
)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Create sync engine for sync operations like table creation
sync_engine = create_engine(
    SYNC_DATABASE_URL,
    # Neon Serverless optimized settings
    poolclass=QueuePool,
    pool_size=2,          # Small pool for serverless
    max_overflow=5,       # Limited overflow
    pool_pre_ping=True,   # Verify connections before use (critical for serverless)
    pool_recycle=300,     # Recycle connections to prevent serverless timeout issues
    echo=False            # Set to True for SQL query logging during development
)

# Create sync session maker
SessionLocal = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False
)

def get_db():
    """Get a sync database session for FastAPI dependency injection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_session():
    """Get an async database session for FastAPI dependency injection"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def create_db_and_tables():
    """Create database tables"""
    # Create all tables defined in SQLModel models
    SQLModel.metadata.create_all(bind=sync_engine)

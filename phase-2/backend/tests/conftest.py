"""
Pytest configuration and fixtures for Phase 2 Backend tests
Provides database, authentication, and API client fixtures
"""

import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import models and app after loading environment
from database import Base
from main import app
from database import get_db


# Test database URL - uses SQLite in-memory for speed
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False},
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope="function")
async def test_db(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a new database session for each test"""
    TestingSessionLocal = sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture
def override_get_db(test_db):
    """Override dependency for database session"""
    async def _override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def client(override_get_db):
    """Create AsyncClient for testing"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
async def authenticated_client(client, test_db):
    """Create authenticated client with valid JWT token"""
    from models import User
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy import select
    import jwt
    from datetime import datetime, timedelta
    from config import settings

    # Create test user
    test_user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="$2b$12$test_hashed_password",
        is_active=True,
    )
    test_db.add(test_user)
    await test_db.commit()
    await test_db.refresh(test_user)

    # Generate JWT token
    payload = {
        "sub": str(test_user.id),
        "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRY_MINUTES),
    }
    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )

    # Add authorization header
    client.headers.update({"Authorization": f"Bearer {token}"})

    # Store user info for test access
    client.test_user = test_user
    client.token = token

    return client


@pytest.fixture
async def test_user_data():
    """Test user data for registration and login"""
    return {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "TestPassword123!",
    }


@pytest.fixture
async def test_task_data():
    """Test task data for creation and updates"""
    return {
        "title": "Test Task",
        "description": "This is a test task",
        "priority": "medium",
        "due_date": None,
        "tags": ["test", "example"],
    }


# Configure pytest
def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "asyncio: mark test as asyncio test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow"
    )


# Async test support
pytest_plugins = ("pytest_asyncio",)

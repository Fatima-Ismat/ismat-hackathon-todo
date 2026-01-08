"""
Database connection for Phase 2 - SQLite with aiosqlite driver
Simple async database setup (No agents needed - Phase 3 feature)
"""

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import AsyncGenerator
import os

from config import settings
from models import User, Task, Notification


# Get database URL from settings, fallback to SQLite
# Phase 2: Use SQLite for local development
# Production: Can use PostgreSQL with postgresql+asyncpg://...
DATABASE_URL = settings.DATABASE_URL

# Auto-fallback to SQLite for Phase 2 if PostgreSQL URL is detected
# This handles cases where system env vars override .env file
if "postgresql" in DATABASE_URL and not os.getenv("USE_POSTGRESQL", "").lower() == "true":
    print("WARNING: PostgreSQL URL detected but USE_POSTGRESQL not set. Falling back to SQLite for Phase 2 development.")
    DATABASE_URL = "sqlite+aiosqlite:///./todo.db"
# Ensure SQLite URLs use aiosqlite driver for async support
elif DATABASE_URL.startswith("sqlite://") and not DATABASE_URL.startswith("sqlite+aiosqlite://"):
    DATABASE_URL = DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    # SQLite-specific: Enable foreign keys
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create async session factory
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    """
    Initialize database tables on startup
    Creates all tables defined in models.py
    """
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session

    Usage in FastAPI routes:
        @app.get("/items")
        async def read_items(db: AsyncSession = Depends(get_db)):
            # use db session
    """
    async with async_session() as session:
        yield session


# Database adapter for agent integration
class DatabaseAdapter:
    """
    Adapter to make SQLModel compatible with agent expectations
    Bridges the gap between SQLModel and agent database interfaces
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert(self, collection: str, document: dict):
        """Insert a document into collection (table)"""
        from models import Task, Notification, User

        # Map collection to model
        model_map = {
            "tasks": Task,
            "notifications": Notification,
            "users": User
        }

        if collection not in model_map:
            raise ValueError(f"Unknown collection: {collection}")

        model_class = model_map[collection]
        instance = model_class(**document)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def query(self, collection: str, filters: dict, limit: int = 100, offset: int = 0, sort: list = None):
        """Query documents from collection with filters"""
        from sqlmodel import select
        from models import Task, Notification, User

        model_map = {
            "tasks": Task,
            "notifications": Notification,
            "users": User
        }

        if collection not in model_map:
            raise ValueError(f"Unknown collection: {collection}")

        model_class = model_map[collection]
        statement = select(model_class)

        # Apply filters
        for key, value in filters.items():
            column = getattr(model_class, key)
            statement = statement.where(column == value)

        # Apply pagination
        statement = statement.offset(offset).limit(limit)

        # Execute query
        result = await self.session.execute(statement)
        items = result.scalars().all()

        # Convert to dict
        return [item.dict() for item in items]

    async def find_one(self, collection: str, filters: dict):
        """Find single document"""
        results = await self.query(collection, filters, limit=1)
        return results[0] if results else None

    async def update(self, collection: str, filters: dict, updates: dict):
        """Update document"""
        from models import Task, Notification, User

        model_map = {
            "tasks": Task,
            "notifications": Notification,
            "users": User
        }

        if collection not in model_map:
            raise ValueError(f"Unknown collection: {collection}")

        # Find document
        document = await self.find_one(collection, filters)
        if not document:
            return None

        model_class = model_map[collection]

        # Get instance
        from sqlmodel import select
        statement = select(model_class)
        for key, value in filters.items():
            column = getattr(model_class, key)
            statement = statement.where(column == value)

        result = await self.session.execute(statement)
        instance = result.scalar_one_or_none()

        if instance:
            for key, value in updates.items():
                setattr(instance, key, value)
            await self.session.commit()
            await self.session.refresh(instance)
            return instance.dict()

        return None

    async def delete(self, collection: str, filters: dict):
        """Delete document"""
        from sqlmodel import select, delete as sql_delete
        from models import Task, Notification, User

        model_map = {
            "tasks": Task,
            "notifications": Notification,
            "users": User
        }

        if collection not in model_map:
            raise ValueError(f"Unknown collection: {collection}")

        model_class = model_map[collection]
        statement = sql_delete(model_class)

        for key, value in filters.items():
            column = getattr(model_class, key)
            statement = statement.where(column == value)

        await self.session.execute(statement)
        await self.session.commit()

    async def count(self, collection: str, filters: dict):
        """Count documents"""
        from sqlmodel import select, func
        from models import Task, Notification, User

        model_map = {
            "tasks": Task,
            "notifications": Notification,
            "users": User
        }

        if collection not in model_map:
            raise ValueError(f"Unknown collection: {collection}")

        model_class = model_map[collection]
        statement = select(func.count()).select_from(model_class)

        for key, value in filters.items():
            column = getattr(model_class, key)
            statement = statement.where(column == value)

        result = await self.session.execute(statement)
        return result.scalar_one()

    async def search(self, collection: str, filters: dict, limit: int = 50):
        """Search documents (simplified - uses query)"""
        return await self.query(collection, filters, limit=limit)

    async def upsert(self, collection: str, filters: dict, document: dict):
        """Insert or update document"""
        existing = await self.find_one(collection, filters)
        if existing:
            return await self.update(collection, filters, document)
        else:
            return await self.insert(collection, document)

    async def update_many(self, collection: str, filters: dict, updates: dict):
        """Update multiple documents"""
        # Simplified implementation
        documents = await self.query(collection, filters)
        count = 0
        for doc in documents:
            await self.update(collection, {"id": doc["id"]}, updates)
            count += 1
        return {"modified_count": count}

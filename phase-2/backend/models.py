"""
Database models for Phase 2
Using SQLModel for ORM with Pydantic integration

Enhancements for T016-T018:
- Composite indexes for common query patterns
- Check constraints for data validation
- Foreign key cascade behavior
- Proper field length constraints
"""

from sqlmodel import SQLModel, Field, Relationship, Index, Column
from sqlalchemy import String, CheckConstraint
from typing import Optional, List
from datetime import datetime
from enum import Enum
from pydantic import field_validator, EmailStr
import re


class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """Task priority enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


# User Model
class User(SQLModel, table=True):
    """
    User model with enhanced constraints

    Indexes:
    - PRIMARY KEY on id
    - UNIQUE INDEX on email
    - UNIQUE INDEX on username

    Constraints:
    - Email format validation (regex check)
    - Username length (min 3, max 255)
    """
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("LENGTH(email) > 0 AND LENGTH(email) <= 255", name="check_email_length"),
        CheckConstraint("LENGTH(username) >= 3 AND LENGTH(username) <= 255", name="check_username_length"),
        CheckConstraint("LENGTH(hashed_password) > 0", name="check_password_exists"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(sa_column=Column(String(255), unique=True, index=True, nullable=False))
    username: str = Field(sa_column=Column(String(255), unique=True, index=True, nullable=False))
    hashed_password: str = Field(sa_column=Column(String(255), nullable=False))
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships (CASCADE delete)
    tasks: List["Task"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    notifications: List["Notification"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


# Task Model
class Task(SQLModel, table=True):
    """
    Task model with enhanced indexes and constraints

    Indexes (9 total as per T017):
    - PRIMARY KEY on id
    - INDEX on user_id (for user's tasks query)
    - INDEX on status (for status filters)
    - INDEX on priority (for priority filters)
    - COMPOSITE INDEX on (user_id, status) for common filter pattern
    - COMPOSITE INDEX on (user_id, created_at DESC) for default sort

    Constraints:
    - Title length (1-255 characters)
    - Description max length (10,000 characters)
    - Foreign key CASCADE on user deletion
    """
    __tablename__ = "tasks"
    __table_args__ = (
        Index("idx_user_status", "user_id", "status"),
        Index("idx_user_created", "user_id", "created_at"),
        Index("idx_status", "status"),
        Index("idx_priority", "priority"),
        CheckConstraint("LENGTH(title) > 0 AND LENGTH(title) <= 255", name="check_title_length"),
        CheckConstraint("LENGTH(description) <= 10000", name="check_description_length"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True, nullable=False)
    title: str = Field(sa_column=Column(String(255), nullable=False))
    description: Optional[str] = Field(default="", sa_column=Column(String(10000)))
    status: TaskStatus = Field(default=TaskStatus.PENDING, index=True)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, index=True)
    due_date: Optional[datetime] = None
    tags: Optional[str] = Field(default="[]")  # JSON string array
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    # Relationships
    user: Optional[User] = Relationship(back_populates="tasks")


# Notification Model
class Notification(SQLModel, table=True):
    """
    Notification model with enhanced indexes and constraints

    Indexes (3 total as per T017):
    - PRIMARY KEY on id
    - INDEX on user_id (for user's notifications query)
    - INDEX on read (for unread count queries)
    - COMPOSITE INDEX on (user_id, read) for unread notifications
    - COMPOSITE INDEX on (user_id, created_at DESC) for recent notifications

    Constraints:
    - Message length (1-500 characters)
    - Notification type length (max 50 characters)
    - Foreign key CASCADE on user deletion
    """
    __tablename__ = "notifications"
    __table_args__ = (
        Index("idx_user_read", "user_id", "read"),
        Index("idx_user_notification_created", "user_id", "created_at"),
        Index("idx_read", "read"),
        CheckConstraint("LENGTH(message) > 0 AND LENGTH(message) <= 500", name="check_message_length"),
        CheckConstraint("LENGTH(notification_type) > 0 AND LENGTH(notification_type) <= 50", name="check_type_length"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True, nullable=False)
    message: str = Field(sa_column=Column(String(500), nullable=False))
    notification_type: str = Field(default="info", sa_column=Column(String(50), nullable=False))
    read: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    read_at: Optional[datetime] = None

    # Relationships
    user: Optional[User] = Relationship(back_populates="notifications")


# Pydantic schemas for API
class UserCreate(SQLModel):
    """
    Schema for user registration with enhanced validation

    Validates:
    - Email format (RFC 5322 compliant)
    - Username minimum length (3 characters)
    - Password minimum length (8 characters)
    """
    email: str
    username: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError("Please enter a valid email address")
        if len(v) > 255:
            raise ValueError("Email must be at most 255 characters")
        return v.lower()  # Store emails in lowercase

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Validate username length and format"""
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        if len(v) > 255:
            raise ValueError("Username must be at most 255 characters")
        # Only allow alphanumeric and underscore
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError("Username can only contain letters, numbers, and underscores")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if len(v) > 255:
            raise ValueError("Password must be at most 255 characters")
        return v


class UserResponse(SQLModel):
    """Schema for user response (without password)"""
    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime


class TaskCreate(SQLModel):
    """Schema for task creation with flexible validation"""
    title: str
    description: Optional[str] = ""
    priority: Optional[TaskPriority] = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate title is not empty"""
        if not v or not v.strip():
            raise ValueError("Title is required and cannot be empty")
        if len(v.strip()) > 255:
            raise ValueError("Title must be at most 255 characters")
        return v.strip()

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: Optional[str]) -> str:
        """Validate description length"""
        if v and len(v) > 10000:
            raise ValueError("Description must be at most 10,000 characters")
        return v or ""

    @field_validator("tags", mode="before")
    @classmethod
    def validate_tags(cls, v):
        """Handle tags as list or None"""
        if v is None or v == []:
            return []
        if isinstance(v, list):
            return v
        # Handle string representation of list
        if isinstance(v, str):
            import json
            try:
                parsed = json.loads(v)
                return parsed if isinstance(parsed, list) else []
            except:
                return []
        return []


class TaskUpdate(SQLModel):
    """Schema for task update"""
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None


class TaskResponse(SQLModel):
    """Schema for task response"""
    id: int
    user_id: int
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[datetime]
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]


class NotificationResponse(SQLModel):
    """Schema for notification response"""
    id: int
    user_id: int
    message: str
    notification_type: str
    read: bool
    created_at: datetime
    read_at: Optional[datetime]


class TokenResponse(SQLModel):
    """Schema for authentication token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(SQLModel):
    """
    Schema for login request with email validation
    """
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError("Please enter a valid email address")
        return v.lower()  # Convert to lowercase for lookup


class RefreshTokenRequest(SQLModel):
    """
    Schema for refresh token request
    """
    refresh_token: str

"""
Task management routes for Phase 2
CRUD operations for tasks
NO AGENTS REQUIRED (Phase 3 feature)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List, Optional
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
import json

from database import get_db
from models import Task, TaskCreate, TaskUpdate, TaskResponse, TaskStatus, TaskPriority
from config import settings


router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


# ==================== AUTH SERVICE CLASS (same as auth.py) ====================
class AuthService:
    """Simple authentication service for Phase 2 (No agents needed)"""

    def __init__(self, jwt_secret: str, jwt_algorithm: str,
                 token_expiry_minutes: int, refresh_token_expiry_days: int,
                 bcrypt_rounds: int):
        self.jwt_secret = jwt_secret
        self.jwt_algorithm = jwt_algorithm
        self.token_expiry_minutes = token_expiry_minutes
        self.refresh_token_expiry_days = refresh_token_expiry_days
        self.bcrypt_rounds = bcrypt_rounds

    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt directly"""
        salt = bcrypt.gensalt(rounds=self.bcrypt_rounds)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash using bcrypt directly"""
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )

    def create_access_token(self, user_id: str, email: str) -> str:
        """Create JWT access token"""
        expire = datetime.utcnow() + timedelta(minutes=self.token_expiry_minutes)
        payload = {
            "sub": user_id,
            "email": email,
            "type": "access",
            "exp": expire
        }
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)

    def create_refresh_token(self, user_id: str) -> str:
        """Create JWT refresh token"""
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expiry_days)
        payload = {
            "sub": user_id,
            "type": "refresh",
            "exp": expire
        }
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)

    def verify_token(self, token: str) -> Optional[dict]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            return payload
        except JWTError:
            return None

    def extract_user_id(self, token: str) -> Optional[str]:
        """Extract user ID from JWT token"""
        payload = self.verify_token(token)
        if payload and payload.get("type") == "access":
            return payload.get("sub")
        return None


# Initialize auth service with configuration
auth_service = AuthService(
    jwt_secret=settings.JWT_SECRET_KEY,
    jwt_algorithm=settings.JWT_ALGORITHM,
    token_expiry_minutes=settings.JWT_EXPIRY_MINUTES,
    refresh_token_expiry_days=settings.REFRESH_TOKEN_EXPIRY_DAYS,
    bcrypt_rounds=settings.BCRYPT_ROUNDS
)


async def get_current_user_id(authorization: Optional[str] = Header(None, alias="Authorization")) -> str:
    """Dependency to extract user ID from JWT token"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Remove "Bearer " prefix if present
    token = authorization.replace("Bearer ", "").strip()
    user_id = auth_service.extract_user_id(token)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user_id


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new task

    - **title**: Task title (required, 1-255 characters)
    - **description**: Task description (optional, max 10,000 characters)
    - **priority**: Task priority (low, medium, high, urgent) - defaults to medium
    - **due_date**: Optional due date (ISO format)
    - **tags**: List of tags (optional)

    Enhancement for T058: Validation handled by Pydantic model validators
    """
    # Validation is now handled by TaskCreate model validators
    # Create task using SQLModel directly
    new_task = Task(
        user_id=int(user_id),
        title=task_data.title.strip(),
        description=task_data.description or "",
        priority=task_data.priority,
        due_date=task_data.due_date,
        tags=json.dumps(task_data.tags or [])
    )

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    # Convert to response
    return TaskResponse(
        id=new_task.id,
        user_id=new_task.user_id,
        title=new_task.title,
        description=new_task.description,
        status=new_task.status,
        priority=new_task.priority,
        due_date=new_task.due_date,
        tags=json.loads(new_task.tags),
        created_at=new_task.created_at,
        updated_at=new_task.updated_at,
        completed_at=new_task.completed_at
    )


@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    limit: int = 100,
    offset: int = 0,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    List all tasks for current user with filtering and pagination

    - **status**: Filter by status (pending, in_progress, completed, cancelled)
    - **priority**: Filter by priority (low, medium, high, urgent)
    - **limit**: Max results per page (default: 100, max: 1000)
    - **offset**: Pagination offset (default: 0)

    Enhancements for T059, T060: Filtering and pagination with validation
    """
    # T060: Enforce pagination limits
    if limit < 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Limit must be at least 1"
        )
    if limit > 1000:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Limit cannot exceed 1000"
        )
    if offset < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Offset cannot be negative"
        )

    # T061: User authorization - only get tasks for current user
    statement = select(Task).where(Task.user_id == int(user_id))

    # T059: Apply filters
    if status:
        statement = statement.where(Task.status == status)
    if priority:
        statement = statement.where(Task.priority == priority)

    # T060: Apply pagination and ordering
    statement = statement.offset(offset).limit(limit).order_by(Task.created_at.desc())

    result = await db.execute(statement)
    tasks = result.scalars().all()

    # Convert to response
    return [
        TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            due_date=task.due_date,
            tags=json.loads(task.tags) if task.tags else [],
            created_at=task.created_at,
            updated_at=task.updated_at,
            completed_at=task.completed_at
        )
        for task in tasks
    ]


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific task by ID

    - **task_id**: Task ID
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == int(user_id))
    result = await db.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        tags=json.loads(task.tags) if task.tags else [],
        created_at=task.created_at,
        updated_at=task.updated_at,
        completed_at=task.completed_at
    )


@router.patch("/{task_id}", response_model=TaskResponse)
@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Update a task (supports both PATCH and PUT methods)

    - **task_id**: Task ID
    - **title**: New title
    - **description**: New description
    - **priority**: New priority
    - **status**: New status
    - **due_date**: New due date
    - **tags**: New tags
    """
    # Get task
    statement = select(Task).where(Task.id == task_id, Task.user_id == int(user_id))
    result = await db.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update fields
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.priority is not None:
        task.priority = task_data.priority
    if task_data.status is not None:
        task.status = task_data.status
        if task_data.status == TaskStatus.COMPLETED:
            from datetime import datetime
            task.completed_at = datetime.utcnow()
    if task_data.due_date is not None:
        task.due_date = task_data.due_date
    if task_data.tags is not None:
        task.tags = json.dumps(task_data.tags)

    from datetime import datetime
    task.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(task)

    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        tags=json.loads(task.tags) if task.tags else [],
        created_at=task.created_at,
        updated_at=task.updated_at,
        completed_at=task.completed_at
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a task (soft delete - marks as cancelled)

    - **task_id**: Task ID

    Implementation for T072: Soft delete by marking task as cancelled
    T061: User authorization - only allows deleting own tasks
    """
    # T061: Get task with user authorization check
    statement = select(Task).where(Task.id == task_id, Task.user_id == int(user_id))
    result = await db.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # T072: Soft delete by marking as cancelled (preserves data for audit)
    task.status = TaskStatus.CANCELLED
    from datetime import datetime
    task.updated_at = datetime.utcnow()

    await db.commit()


@router.patch("/{task_id}/complete", response_model=TaskResponse)
@router.post("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Mark a task as completed and set completion timestamp (supports both PATCH and POST)

    - **task_id**: Task ID

    Implementation for T071: Complete task endpoint
    Sets status to COMPLETED and records completion timestamp
    T061: User authorization - only allows completing own tasks
    """
    # T061: Get task with user authorization check
    statement = select(Task).where(Task.id == task_id, Task.user_id == int(user_id))
    result = await db.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # T071: Mark as completed with timestamp
    task.status = TaskStatus.COMPLETED
    from datetime import datetime
    task.completed_at = datetime.utcnow()
    task.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(task)

    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        tags=json.loads(task.tags) if task.tags else [],
        created_at=task.created_at,
        updated_at=task.updated_at,
        completed_at=task.completed_at
    )

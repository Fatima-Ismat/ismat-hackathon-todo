"""
Authentication routes for Phase 2
User registration, login, token refresh
NO AGENTS REQUIRED (Phase 3 feature)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

from database import get_db
from models import User, UserCreate, UserResponse, LoginRequest, TokenResponse, RefreshTokenRequest
from config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


# ==================== AUTH SERVICE CLASS (Phase 2 compatible) ====================
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


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user

    - **email**: User email (unique)
    - **username**: Username (unique)
    - **password**: User password (will be hashed)
    """
    # Check if user exists
    statement = select(User).where(User.email == user_data.email)
    result = await db.execute(statement)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check username
    statement = select(User).where(User.username == user_data.username)
    result = await db.execute(statement)
    existing_username = result.scalar_one_or_none()

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Hash password
    hashed_password = auth_service.hash_password(user_data.password)

    # Create user
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Login and receive JWT tokens

    - **email**: User email
    - **password**: User password

    Returns access_token and refresh_token
    """
    # Find user by email
    statement = select(User).where(User.email == credentials.email)
    result = await db.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not auth_service.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )

    # Create tokens
    access_token = auth_service.create_access_token(
        user_id=str(user.id),
        email=user.email
    )
    refresh_token = auth_service.create_refresh_token(str(user.id))

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    token_request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token using refresh token

    - **refresh_token**: Valid refresh token (in request body)

    Returns new access_token and same refresh_token
    """
    # Verify refresh token
    payload = auth_service.verify_token(token_request.refresh_token)

    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user_id = payload.get("sub")

    # Get user
    statement = select(User).where(User.id == int(user_id))
    result = await db.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # Create new access token
    access_token = auth_service.create_access_token(
        user_id=str(user.id),
        email=user.email
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=token_request.refresh_token,
        token_type="bearer"
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    authorization: Optional[str] = Header(None, alias="Authorization"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current authenticated user

    Requires: Authorization: Bearer <access_token>
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Extract user ID from token
    token = authorization.replace("Bearer ", "").strip()
    user_id = auth_service.extract_user_id(token)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Get user
    statement = select(User).where(User.id == int(user_id))
    result = await db.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user

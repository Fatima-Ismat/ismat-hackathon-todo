"""
Backend tests for authentication routes
Tests user registration, login, token refresh, and /me endpoint

Tests for T028-T031
"""

import pytest
from httpx import AsyncClient
from sqlmodel import select
from models import User


@pytest.mark.asyncio
async def test_user_registration_success(client: AsyncClient, test_user_data: dict):
    """
    T028: Test successful user registration

    Given: Valid registration data (email, username, password)
    When: POST /api/auth/register
    Then: User is created and returns 201 with user data (no password)
    """
    response = await client.post("/api/auth/register", json=test_user_data)

    assert response.status_code == 201
    data = response.json()

    # Verify response structure
    assert "id" in data
    assert data["email"] == test_user_data["email"]
    assert data["username"] == test_user_data["username"]
    assert data["is_active"] is True
    assert "hashed_password" not in data  # Password should not be returned
    assert "password" not in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_user_registration_duplicate_email(
    client: AsyncClient,
    test_user_data: dict,
    test_db
):
    """
    T028: Test registration with duplicate email

    Given: Email already exists in database
    When: POST /api/auth/register with same email
    Then: Returns 400 with "Email already registered" error
    """
    # Create first user
    await client.post("/api/auth/register", json=test_user_data)

    # Try to create second user with same email
    duplicate_data = test_user_data.copy()
    duplicate_data["username"] = "different_username"

    response = await client.post("/api/auth/register", json=duplicate_data)

    assert response.status_code == 400
    assert "email already registered" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_user_registration_duplicate_username(
    client: AsyncClient,
    test_user_data: dict
):
    """
    T028: Test registration with duplicate username

    Given: Username already exists in database
    When: POST /api/auth/register with same username
    Then: Returns 400 with "Username already taken" error
    """
    # Create first user
    await client.post("/api/auth/register", json=test_user_data)

    # Try to create second user with same username
    duplicate_data = test_user_data.copy()
    duplicate_data["email"] = "different@example.com"

    response = await client.post("/api/auth/register", json=duplicate_data)

    assert response.status_code == 400
    assert "username already taken" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_user_login_success(authenticated_client: AsyncClient):
    """
    T029: Test successful login with JWT generation

    Given: Valid credentials (email and password)
    When: POST /api/auth/login
    Then: Returns 200 with access_token, refresh_token, and token_type
    """
    # authenticated_client fixture already creates user and logs in
    # This verifies the token structure
    login_data = {
        "email": "test@example.com",
        "password": "testpass123"
    }

    response = await authenticated_client.post("/api/auth/login", json=login_data)

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0
    assert len(data["refresh_token"]) > 0


@pytest.mark.asyncio
async def test_user_login_invalid_email(client: AsyncClient):
    """
    T029: Test login with non-existent email

    Given: Email does not exist in database
    When: POST /api/auth/login
    Then: Returns 401 with "Invalid email or password" error
    """
    login_data = {
        "email": "nonexistent@example.com",
        "password": "somepassword"
    }

    response = await client.post("/api/auth/login", json=login_data)

    assert response.status_code == 401
    assert "invalid email or password" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_user_login_invalid_password(client: AsyncClient, test_user_data: dict):
    """
    T029: Test login with incorrect password

    Given: Valid email but wrong password
    When: POST /api/auth/login
    Then: Returns 401 with "Invalid email or password" error
    """
    # Create user first
    await client.post("/api/auth/register", json=test_user_data)

    # Try to login with wrong password
    login_data = {
        "email": test_user_data["email"],
        "password": "wrongpassword"
    }

    response = await client.post("/api/auth/login", json=login_data)

    assert response.status_code == 401
    assert "invalid email or password" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_token_refresh_success(authenticated_client: AsyncClient):
    """
    T030: Test successful token refresh

    Given: Valid refresh token
    When: POST /api/auth/refresh with refresh_token
    Then: Returns 200 with new access_token
    """
    # Get tokens from login
    login_data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    login_response = await authenticated_client.post("/api/auth/login", json=login_data)
    refresh_token = login_response.json()["refresh_token"]

    # Use refresh token to get new access token
    response = await authenticated_client.post(
        "/api/auth/refresh",
        json={"refresh_token": refresh_token}
    )

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0


@pytest.mark.asyncio
async def test_token_refresh_invalid_token(client: AsyncClient):
    """
    T030: Test token refresh with invalid token

    Given: Invalid or expired refresh token
    When: POST /api/auth/refresh
    Then: Returns 401 with "Invalid refresh token" error
    """
    response = await client.post(
        "/api/auth/refresh",
        json={"refresh_token": "invalid.token.here"}
    )

    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_current_user_success(authenticated_client: AsyncClient):
    """
    T031: Test /me endpoint with valid token

    Given: Valid access token in Authorization header
    When: GET /api/auth/me
    Then: Returns 200 with current user data
    """
    response = await authenticated_client.get("/api/auth/me")

    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert "email" in data
    assert "username" in data
    assert "is_active" in data
    assert data["email"] == "test@example.com"
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(client: AsyncClient):
    """
    T031: Test /me endpoint with invalid token

    Given: Invalid or missing access token
    When: GET /api/auth/me
    Then: Returns 401 with "Invalid token" error
    """
    # Test with invalid token
    response = await client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid.token.here"}
    )

    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_current_user_missing_token(client: AsyncClient):
    """
    T031: Test /me endpoint without Authorization header

    Given: No Authorization header
    When: GET /api/auth/me
    Then: Returns 401 with "Missing authorization header" error
    """
    response = await client.get("/api/auth/me")

    assert response.status_code == 401
    assert "missing" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_password_hashing(client: AsyncClient, test_user_data: dict, test_db):
    """
    T041 verification: Ensure passwords are hashed, not stored in plaintext

    Given: User registration with password
    When: User is created in database
    Then: Password is hashed (not equal to original) and verifiable
    """
    # Register user
    await client.post("/api/auth/register", json=test_user_data)

    # Query database directly to check password is hashed
    from sqlalchemy.ext.asyncio import AsyncSession
    async for session in test_db:
        statement = select(User).where(User.email == test_user_data["email"])
        result = await session.execute(statement)
        user = result.scalar_one()

        # Password should be hashed (not plaintext)
        assert user.hashed_password != test_user_data["password"]
        assert user.hashed_password.startswith("$2b$")  # bcrypt hash prefix
        assert len(user.hashed_password) == 60  # bcrypt hash length
        break

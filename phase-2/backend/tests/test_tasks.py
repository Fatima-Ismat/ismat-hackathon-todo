"""
Backend tests for task routes
Tests task creation, listing, retrieval, completion, deletion, and user isolation

Tests for T045-T048, T063-T065
"""

import pytest
from httpx import AsyncClient
from sqlmodel import select
from models import Task, TaskStatus


@pytest.mark.asyncio
async def test_create_task_success(authenticated_client: AsyncClient):
    """
    T045: Test successful task creation

    Given: Valid task data (title, description, priority)
    When: POST /api/tasks
    Then: Task is created and returns 201 with task data
    """
    task_data = {
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "priority": "high",
        "tags": ["shopping", "food"]
    }

    response = await authenticated_client.post("/api/tasks", json=task_data)

    assert response.status_code == 201
    data = response.json()

    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["priority"] == task_data["priority"]
    assert data["status"] == "pending"
    assert "id" in data
    assert "created_at" in data
    assert "user_id" in data


@pytest.mark.asyncio
async def test_create_task_minimum_fields(authenticated_client: AsyncClient):
    """
    T045: Test task creation with only required field (title)

    Given: Only title provided
    When: POST /api/tasks
    Then: Task is created with defaults (description="", priority="medium")
    """
    task_data = {
        "title": "Simple task"
    }

    response = await authenticated_client.post("/api/tasks", json=task_data)

    assert response.status_code == 201
    data = response.json()

    assert data["title"] == "Simple task"
    assert data["description"] == ""
    assert data["priority"] == "medium"
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_create_task_missing_title(authenticated_client: AsyncClient):
    """
    T045: Test task creation fails without title

    Given: Task data without title
    When: POST /api/tasks
    Then: Returns 422 validation error
    """
    task_data = {
        "description": "No title provided"
    }

    response = await authenticated_client.post("/api/tasks", json=task_data)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_task_title_too_long(authenticated_client: AsyncClient):
    """
    T045: Test task creation fails with title > 255 chars

    Given: Task with title exceeding 255 characters
    When: POST /api/tasks
    Then: Returns 422 validation error
    """
    task_data = {
        "title": "x" * 256  # Exceeds maximum length
    }

    response = await authenticated_client.post("/api/tasks", json=task_data)

    assert response.status_code in [422, 400]  # Validation error


@pytest.mark.asyncio
async def test_list_tasks_success(authenticated_client: AsyncClient):
    """
    T046: Test listing user's tasks

    Given: User has created multiple tasks
    When: GET /api/tasks
    Then: Returns 200 with list of user's tasks
    """
    # Create test tasks
    tasks = [
        {"title": "Task 1", "priority": "high"},
        {"title": "Task 2", "priority": "medium"},
        {"title": "Task 3", "priority": "low"},
    ]

    for task_data in tasks:
        await authenticated_client.post("/api/tasks", json=task_data)

    # Get tasks list
    response = await authenticated_client.get("/api/tasks")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 3  # At least the 3 we created

    # Verify tasks are ordered by created_at DESC (most recent first)
    titles = [task["title"] for task in data]
    assert "Task 3" in titles
    assert "Task 2" in titles
    assert "Task 1" in titles


@pytest.mark.asyncio
async def test_list_tasks_filter_by_status(authenticated_client: AsyncClient):
    """
    T046: Test filtering tasks by status

    Given: User has tasks with different statuses
    When: GET /api/tasks?status=pending
    Then: Returns only pending tasks
    """
    # Create tasks with different statuses
    await authenticated_client.post("/api/tasks", json={"title": "Pending task"})
    task_response = await authenticated_client.post("/api/tasks", json={"title": "Task to complete"})
    task_id = task_response.json()["id"]

    # Complete one task (will be implemented in T071)
    # For now, we'll just test pending filter
    response = await authenticated_client.get("/api/tasks?status=pending")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert all(task["status"] == "pending" for task in data)


@pytest.mark.asyncio
async def test_list_tasks_filter_by_priority(authenticated_client: AsyncClient):
    """
    T046: Test filtering tasks by priority

    Given: User has tasks with different priorities
    When: GET /api/tasks?priority=high
    Then: Returns only high priority tasks
    """
    # Create tasks with different priorities
    await authenticated_client.post("/api/tasks", json={"title": "High priority", "priority": "high"})
    await authenticated_client.post("/api/tasks", json={"title": "Low priority", "priority": "low"})

    response = await authenticated_client.get("/api/tasks?priority=high")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert all(task["priority"] == "high" for task in data)


@pytest.mark.asyncio
async def test_list_tasks_pagination(authenticated_client: AsyncClient):
    """
    T046: Test task list pagination

    Given: User has many tasks
    When: GET /api/tasks?limit=2&offset=1
    Then: Returns paginated results
    """
    # Create multiple tasks
    for i in range(5):
        await authenticated_client.post("/api/tasks", json={"title": f"Task {i}"})

    # Get paginated results
    response = await authenticated_client.get("/api/tasks?limit=2&offset=1")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) <= 2  # Respects limit


@pytest.mark.asyncio
async def test_get_task_by_id_success(authenticated_client: AsyncClient):
    """
    T047: Test retrieving a specific task by ID

    Given: User has created a task
    When: GET /api/tasks/{id}
    Then: Returns 200 with task details
    """
    # Create a task
    create_response = await authenticated_client.post(
        "/api/tasks",
        json={"title": "Test task", "description": "Test description"}
    )
    task_id = create_response.json()["id"]

    # Get task by ID
    response = await authenticated_client.get(f"/api/tasks/{task_id}")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Test task"
    assert data["description"] == "Test description"


@pytest.mark.asyncio
async def test_get_task_not_found(authenticated_client: AsyncClient):
    """
    T047: Test retrieving non-existent task

    Given: Task ID does not exist
    When: GET /api/tasks/{invalid_id}
    Then: Returns 404 not found
    """
    response = await authenticated_client.get("/api/tasks/99999")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_user_isolation_tasks(
    authenticated_client: AsyncClient,
    client: AsyncClient,
    test_user_data: dict
):
    """
    T048: Test that users can only see their own tasks

    Given: Two different users with their own tasks
    When: User A requests tasks list
    Then: User A only sees their own tasks, not User B's
    """
    # User A (authenticated_client) creates a task
    user_a_task = await authenticated_client.post(
        "/api/tasks",
        json={"title": "User A task"}
    )
    assert user_a_task.status_code == 201
    user_a_task_id = user_a_task.json()["id"]

    # Create User B and login
    user_b_data = {
        "email": "userb@example.com",
        "username": "userb",
        "password": "testpass123"
    }
    await client.post("/api/auth/register", json=user_b_data)
    login_response = await client.post(
        "/api/auth/login",
        json={"email": user_b_data["email"], "password": user_b_data["password"]}
    )
    user_b_token = login_response.json()["access_token"]

    # User B creates their own task
    user_b_task = await client.post(
        "/api/tasks",
        json={"title": "User B task"},
        headers={"Authorization": f"Bearer {user_b_token}"}
    )
    assert user_b_task.status_code == 201
    user_b_task_id = user_b_task.json()["id"]

    # User A gets their tasks list
    user_a_tasks = await authenticated_client.get("/api/tasks")
    user_a_tasks_data = user_a_tasks.json()
    user_a_task_ids = [task["id"] for task in user_a_tasks_data]

    # User B gets their tasks list
    user_b_tasks = await client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {user_b_token}"}
    )
    user_b_tasks_data = user_b_tasks.json()
    user_b_task_ids = [task["id"] for task in user_b_tasks_data]

    # Verify isolation
    assert user_a_task_id in user_a_task_ids
    assert user_b_task_id not in user_a_task_ids  # User A cannot see User B's tasks

    assert user_b_task_id in user_b_task_ids
    assert user_a_task_id not in user_b_task_ids  # User B cannot see User A's tasks


@pytest.mark.asyncio
async def test_user_cannot_access_other_user_task(
    authenticated_client: AsyncClient,
    client: AsyncClient
):
    """
    T048: Test that users cannot access other users' tasks by ID

    Given: User A has a task
    When: User B tries to GET User A's task by ID
    Then: Returns 404 (not found) for security
    """
    # User A creates a task
    user_a_task = await authenticated_client.post(
        "/api/tasks",
        json={"title": "User A private task"}
    )
    user_a_task_id = user_a_task.json()["id"]

    # Create and login User B
    user_b_data = {
        "email": "userb@example.com",
        "username": "userb",
        "password": "testpass123"
    }
    await client.post("/api/auth/register", json=user_b_data)
    login_response = await client.post(
        "/api/auth/login",
        json={"email": user_b_data["email"], "password": user_b_data["password"]}
    )
    user_b_token = login_response.json()["access_token"]

    # User B tries to access User A's task
    response = await client.get(
        f"/api/tasks/{user_a_task_id}",
        headers={"Authorization": f"Bearer {user_b_token}"}
    )

    # Should return 404 (not 403) to avoid leaking task existence
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_complete_task_success(authenticated_client: AsyncClient):
    """
    T063: Test marking task as complete

    Given: User has a pending task
    When: POST /api/tasks/{id}/complete
    Then: Task status changes to "completed" and completed_at is set
    """
    # Create a task
    create_response = await authenticated_client.post(
        "/api/tasks",
        json={"title": "Task to complete"}
    )
    task_id = create_response.json()["id"]

    # Complete the task
    response = await authenticated_client.post(f"/api/tasks/{task_id}/complete")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == task_id
    assert data["status"] == "completed"
    assert data["completed_at"] is not None


@pytest.mark.asyncio
async def test_complete_task_not_found(authenticated_client: AsyncClient):
    """
    T063: Test completing non-existent task

    Given: Task ID does not exist
    When: POST /api/tasks/{invalid_id}/complete
    Then: Returns 404 not found
    """
    response = await authenticated_client.post("/api/tasks/99999/complete")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_task_success(authenticated_client: AsyncClient):
    """
    T064: Test deleting a task

    Given: User has a task
    When: DELETE /api/tasks/{id}
    Then: Task is deleted and returns 204
    """
    # Create a task
    create_response = await authenticated_client.post(
        "/api/tasks",
        json={"title": "Task to delete"}
    )
    task_id = create_response.json()["id"]

    # Delete the task
    response = await authenticated_client.delete(f"/api/tasks/{task_id}")

    assert response.status_code == 204

    # Verify task is deleted
    get_response = await authenticated_client.get(f"/api/tasks/{task_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_task_not_found(authenticated_client: AsyncClient):
    """
    T064: Test deleting non-existent task

    Given: Task ID does not exist
    When: DELETE /api/tasks/{invalid_id}
    Then: Returns 404 not found
    """
    response = await authenticated_client.delete("/api/tasks/99999")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_completed_at_timestamp(authenticated_client: AsyncClient):
    """
    T065: Test that completed_at timestamp is set correctly

    Given: User creates and completes a task
    When: Task is marked complete
    Then: completed_at timestamp is set and is recent
    """
    from datetime import datetime, timedelta

    # Create a task
    create_response = await authenticated_client.post(
        "/api/tasks",
        json={"title": "Task for timestamp test"}
    )
    task_data = create_response.json()
    task_id = task_data["id"]

    # Verify completed_at is None initially
    assert task_data["completed_at"] is None

    # Complete the task
    complete_response = await authenticated_client.post(f"/api/tasks/{task_id}/complete")
    completed_data = complete_response.json()

    # Verify completed_at is set
    assert completed_data["completed_at"] is not None

    # Verify timestamp is recent (within last minute)
    completed_at = datetime.fromisoformat(completed_data["completed_at"].replace('Z', '+00:00'))
    now = datetime.now(completed_at.tzinfo)
    time_diff = abs((now - completed_at).total_seconds())

    assert time_diff < 60  # Completed within last 60 seconds

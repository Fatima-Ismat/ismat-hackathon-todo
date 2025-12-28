"""Tests for task management services."""
import pytest
from src.services import (
    add_task, view_all_tasks, get_task_count,
    toggle_task_status, user_id_to_index, index_to_user_id,
    update_task, delete_task, _tasks
)
from src.models import Task


@pytest.fixture(autouse=True)
def clear_tasks():
    """Clear tasks before each test."""
    _tasks.clear()
    yield
    _tasks.clear()


# US1: Add Task Tests
def test_add_task_with_title_only():
    """Test adding task with title only."""
    success, message, task = add_task("Buy milk")
    assert success is True
    assert "Success: Task added: Buy milk" in message
    assert task is not None
    assert task.title == "Buy milk"
    assert task.description == ""


def test_add_task_with_title_and_description():
    """Test adding task with title and description."""
    success, message, task = add_task("Buy milk", "From grocery store")
    assert success is True
    assert "Success: Task added: Buy milk" in message
    assert task is not None
    assert task.title == "Buy milk"
    assert task.description == "From grocery store"


def test_add_task_empty_title_error():
    """Test adding task with empty title returns error."""
    success, message, task = add_task("")
    assert success is False
    assert "Error: Title cannot be empty" in message
    assert task is None


def test_add_task_whitespace_title_error():
    """Test adding task with whitespace-only title returns error."""
    success, message, task = add_task("   ")
    assert success is False
    assert "Error: Title cannot be empty" in message
    assert task is None


def test_add_task_utf8_characters():
    """Test adding task with UTF-8 characters."""
    success, message, task = add_task("買い物 🛒", "Milk, eggs")
    assert success is True
    assert task is not None
    assert task.title == "買い物 🛒"
    assert task.description == "Milk, eggs"


# US2: View All Tasks Tests
def test_view_all_tasks_with_tasks():
    """Test viewing tasks when tasks exist."""
    add_task("Task 1", "Description 1")
    add_task("Task 2")
    
    success, message, tasks = view_all_tasks()
    assert success is True
    assert message == ""
    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"


def test_view_all_tasks_empty_list():
    """Test viewing tasks when list is empty."""
    success, message, tasks = view_all_tasks()
    assert success is False
    assert "Info: No tasks found" in message
    assert len(tasks) == 0


def test_view_all_tasks_returns_copy():
    """Test that view_all_tasks returns a copy, not reference."""
    add_task("Task 1")
    success, message, tasks = view_all_tasks()
    
    # Modify returned list
    tasks.append(Task("Fake task"))
    
    # Original should be unchanged
    assert len(_tasks) == 1
    assert _tasks[0].title == "Task 1"


def test_get_task_count():
    """Test getting task count."""
    assert get_task_count() == 0
    
    add_task("Task 1")
    assert get_task_count() == 1
    
    add_task("Task 2")
    assert get_task_count() == 2


# US3: Toggle Status Tests
def test_toggle_task_status_success():
    """Test toggling task status successfully."""
    add_task("Task 1")
    
    # Toggle incomplete -> complete
    success, message, task = toggle_task_status(0)
    assert success is True
    assert "Success: Task status updated" in message
    assert task is not None
    assert task.is_complete is True
    
    # Toggle complete -> incomplete
    success, message, task = toggle_task_status(0)
    assert success is True
    assert task.is_complete is False


def test_toggle_task_status_invalid_index():
    """Test toggling with invalid index."""
    success, message, task = toggle_task_status(99)
    assert success is False
    assert "Error: Invalid task number" in message
    assert task is None


def test_user_id_to_index_conversion():
    """Test user ID to index conversion."""
    assert user_id_to_index(1) == 0
    assert user_id_to_index(5) == 4
    assert user_id_to_index(10) == 9


def test_index_to_user_id_conversion():
    """Test index to user ID conversion."""
    assert index_to_user_id(0) == 1
    assert index_to_user_id(4) == 5
    assert index_to_user_id(9) == 10


# US4: Update Task Tests
def test_update_task_title_only():
    """Test updating only the task title."""
    add_task("Old Title", "Description")

    success, message, task = update_task(0, title="New Title")
    assert success is True
    assert "Success: Task updated" in message
    assert task is not None
    assert task.title == "New Title"
    assert task.description == "Description"  # Unchanged


def test_update_task_description_only():
    """Test updating only the task description."""
    add_task("Title", "Old Description")

    success, message, task = update_task(0, description="New Description")
    assert success is True
    assert task.title == "Title"  # Unchanged
    assert task.description == "New Description"


def test_update_task_both_fields():
    """Test updating both title and description."""
    add_task("Old Title", "Old Description")

    success, message, task = update_task(0, title="New Title", description="New Description")
    assert success is True
    assert task.title == "New Title"
    assert task.description == "New Description"


def test_update_task_empty_title_error():
    """Test updating with empty title returns error."""
    add_task("Original Title", "Description")

    success, message, task = update_task(0, title="")
    assert success is False
    assert "Error: Title cannot be empty" in message
    assert task is None
    # Verify original task unchanged
    _, _, tasks = view_all_tasks()
    assert tasks[0].title == "Original Title"


def test_update_task_invalid_index():
    """Test updating with invalid index."""
    success, message, task = update_task(99, title="New Title")
    assert success is False
    assert "Error: Invalid task number" in message
    assert task is None


def test_update_task_no_changes():
    """Test updating with no actual changes (both None)."""
    add_task("Title", "Description")

    success, message, task = update_task(0)
    assert success is True
    assert "Success: Task updated" in message
    # Task remains unchanged
    assert task.title == "Title"
    assert task.description == "Description"


# US5: Delete Task Tests
def test_delete_task_success():
    """Test deleting a task successfully."""
    add_task("Task 1")
    add_task("Task 2")
    add_task("Task 3")

    # Delete middle task
    success, message, task = delete_task(1)
    assert success is True
    assert "Success: Task deleted" in message
    assert task is not None
    assert task.title == "Task 2"

    # Verify task list updated
    assert get_task_count() == 2
    _, _, tasks = view_all_tasks()
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 3"


def test_delete_task_invalid_index():
    """Test deleting with invalid index."""
    add_task("Task 1")

    success, message, task = delete_task(99)
    assert success is False
    assert "Error: Invalid task number" in message
    assert task is None

    # Verify task list unchanged
    assert get_task_count() == 1


def test_delete_task_negative_index():
    """Test deleting with negative index."""
    add_task("Task 1")

    success, message, task = delete_task(-1)
    assert success is False
    assert "Error: Invalid task number" in message
    assert task is None


def test_delete_task_single_task():
    """Test deleting the only task in the list."""
    add_task("Only Task")

    success, message, task = delete_task(0)
    assert success is True
    assert task.title == "Only Task"
    assert get_task_count() == 0


def test_delete_task_first():
    """Test deleting the first task."""
    add_task("First")
    add_task("Second")

    success, message, task = delete_task(0)
    assert success is True
    assert task.title == "First"
    assert get_task_count() == 1
    _, _, tasks = view_all_tasks()
    assert tasks[0].title == "Second"


def test_delete_task_last():
    """Test deleting the last task."""
    add_task("First")
    add_task("Last")

    success, message, task = delete_task(1)
    assert success is True
    assert task.title == "Last"
    assert get_task_count() == 1
    _, _, tasks = view_all_tasks()
    assert tasks[0].title == "First"

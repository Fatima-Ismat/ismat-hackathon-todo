"""Business logic for task management."""
from typing import Optional
from src.models import Task


# Global in-memory task storage
_tasks: list[Task] = []


def add_task(title: str, description: str = "") -> tuple[bool, str, Optional[Task]]:
    """
    Create a new task and add it to the task list.

    Args:
        title: Task title (required, non-empty)
        description: Optional task description

    Returns:
        Tuple of (success, message, task):
        - success: True if task added, False if error
        - message: Success confirmation or error description
        - task: Created Task object or None if error
    """
    # Strip whitespace
    title = title.strip()
    description = description.strip()

    # Validate title is not empty
    if not title:
        return (False, "Error: Title cannot be empty", None)

    try:
        # Create Task object (will raise ValueError if invalid)
        task = Task(title, description)
        _tasks.append(task)
        return (True, f"Success: Task added: {task.title}", task)
    except ValueError as e:
        return (False, f"Error: {str(e)}", None)


def view_all_tasks() -> tuple[bool, str, list[Task]]:
    """
    Retrieve all tasks for display.

    Returns:
        Tuple of (success, message, tasks):
        - success: True if tasks exist, False if empty
        - message: Info message if empty, empty string otherwise
        - tasks: Copy of task list (empty list if no tasks)
    """
    if not _tasks:
        return (False, "Info: No tasks found", [])

    # Return copy to prevent external modification
    return (True, "", _tasks.copy())


def get_task_count() -> int:
    """
    Return the total number of tasks.

    Returns:
        int: Number of tasks in the list
    """
    return len(_tasks)


def user_id_to_index(user_id: int) -> int:
    """
    Convert user-facing ID (1-based) to internal index (0-based).

    Args:
        user_id: User-facing task ID (starts at 1)

    Returns:
        int: Internal list index (starts at 0)
    """
    return user_id - 1


def index_to_user_id(index: int) -> int:
    """
    Convert internal index (0-based) to user-facing ID (1-based).

    Args:
        index: Internal list index (starts at 0)

    Returns:
        int: User-facing task ID (starts at 1)
    """
    return index + 1


def toggle_task_status(task_index: int) -> tuple[bool, str, Optional[Task]]:
    """
    Toggle a task's completion status.

    Args:
        task_index: Internal task index (0-based)

    Returns:
        Tuple of (success, message, task):
        - success: True if toggled, False if error
        - message: Confirmation or error message
        - task: Updated Task object or None if error
    """
    # Validate index
    if task_index < 0 or task_index >= len(_tasks):
        return (False, "Error: Invalid task number", None)

    # Toggle status
    task = _tasks[task_index]
    task.toggle_status()

    return (True, f"Success: Task status updated: {task.title}", task)


def update_task(
    task_index: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> tuple[bool, str, Optional[Task]]:
    """
    Update a task's title and/or description.

    Args:
        task_index: Internal task index (0-based)
        title: New title (None to keep existing)
        description: New description (None to keep existing)

    Returns:
        Tuple of (success, message, task):
        - success: True if updated, False if error
        - message: Confirmation or error message
        - task: Updated Task object or None if error
    """
    # Validate index
    if task_index < 0 or task_index >= len(_tasks):
        return (False, "Error: Invalid task number", None)

    task = _tasks[task_index]

    # Update title if provided
    if title is not None:
        title = title.strip()
        if not title:
            return (False, "Error: Title cannot be empty", None)
        task.title = title

    # Update description if provided
    if description is not None:
        task.description = description.strip()

    return (True, f"Success: Task updated: {task.title}", task)


def delete_task(task_index: int) -> tuple[bool, str, Optional[Task]]:
    """
    Delete a task from the task list.

    Args:
        task_index: Internal task index (0-based)

    Returns:
        Tuple of (success, message, task):
        - success: True if deleted, False if error
        - message: Confirmation or error message
        - task: Deleted Task object or None if error
    """
    # Validate index
    if task_index < 0 or task_index >= len(_tasks):
        return (False, "Error: Invalid task number", None)

    # Remove and return the task
    task = _tasks.pop(task_index)

    return (True, f"Success: Task deleted: {task.title}", task)

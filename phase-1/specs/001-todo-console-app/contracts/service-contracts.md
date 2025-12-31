# Service Layer Contracts: Phase I Todo Console App

**Feature**: 001-todo-console-app
**Created**: 2025-12-28
**Purpose**: Define function signatures and contracts for the service layer

---

## Overview

This document specifies the contracts for all service layer functions in `src/services.py`. These functions implement business logic and validation.

**Contract Format**: All functions return `tuple[bool, str, Optional[T]]` where:
- `bool`: Success flag (True = operation succeeded, False = failed)
- `str`: Message for user (success confirmation or error description)
- `Optional[T]`: Result data (Task object or None)

---

## Function Contracts

### 1. add_task

**Purpose**: Create a new task and add it to the task list

**Signature**:
```python
def add_task(title: str, description: str = "") -> tuple[bool, str, Optional[Task]]
```

**Parameters**:
| Parameter | Type | Required | Default | Constraints |
|-----------|------|----------|---------|-------------|
| `title` | `str` | Yes | N/A | Non-empty after strip |
| `description` | `str` | No | `""` | None |

**Returns**:
| Success | Message | Data |
|---------|---------|------|
| `True` | `"Success: Task added: {title}"` | `Task` object |
| `False` | `"Error: Title cannot be empty"` | `None` |

**Behavior**:
1. Strip whitespace from title and description
2. Validate title is not empty
3. Create Task object (may raise ValueError if title empty post-strip)
4. Append to global `_tasks` list
5. Return success tuple with Task reference

**Error Conditions**:
- Empty title (before or after strip) → `(False, "Error: Title cannot be empty", None)`
- Task creation raises ValueError → Propagates exception (caught by CLI layer)

**Side Effects**:
- Appends Task to `_tasks` list
- Modifies global state

**Examples**:
```python
# Success case
result = add_task("Buy milk", "From store")
# Returns: (True, "Success: Task added: Buy milk", Task(...))

# Error case
result = add_task("", "No title")
# Returns: (False, "Error: Title cannot be empty", None)

# Edge case (whitespace)
result = add_task("   ", "Whitespace title")
# Returns: (False, "Error: Title cannot be empty", None)
```

---

### 2. view_all_tasks

**Purpose**: Retrieve all tasks for display

**Signature**:
```python
def view_all_tasks() -> tuple[bool, str, list[Task]]
```

**Parameters**: None

**Returns**:
| Condition | Success | Message | Data |
|-----------|---------|---------|------|
| Tasks exist | `True` | `""` (empty) | `list[Task]` (copy) |
| No tasks | `False` | `"Info: No tasks found"` | `[]` (empty list) |

**Behavior**:
1. Check if `_tasks` list is empty
2. If empty, return info message
3. If tasks exist, return copy of list (prevents external modification)

**Side Effects**: None (read-only operation)

**Examples**:
```python
# With tasks
result = view_all_tasks()
# Returns: (True, "", [Task(...), Task(...)])

# Without tasks
result = view_all_tasks()
# Returns: (False, "Info: No tasks found", [])
```

---

### 3. update_task

**Purpose**: Modify an existing task's title and/or description

**Signature**:
```python
def update_task(task_index: int, new_title: str | None = None,
                new_description: str | None = None) -> tuple[bool, str, Optional[Task]]
```

**Parameters**:
| Parameter | Type | Required | Default | Constraints |
|-----------|------|----------|---------|-------------|
| `task_index` | `int` | Yes | N/A | 0 <= index < len(_tasks) |
| `new_title` | `str \| None` | No | `None` | Non-empty if provided |
| `new_description` | `str \| None` | No | `None` | None |

**Returns**:
| Success | Message | Data |
|---------|---------|------|
| `True` | `"Success: Task updated: {title}"` | Updated `Task` object |
| `False` | `"Error: Invalid task number"` | `None` |
| `False` | `"Error: Title cannot be empty"` | `None` |

**Behavior**:
1. Validate task_index is within bounds
2. If new_title provided and non-empty, update task.title
3. If new_description provided (even if empty), update task.description
4. If no changes provided (both None), return error
5. Return success with updated task reference

**Error Conditions**:
- Invalid index → `(False, "Error: Invalid task number", None)`
- Empty new_title → `(False, "Error: Title cannot be empty", None)`
- Both parameters None → `(False, "Error: No changes provided", None)`

**Side Effects**:
- Modifies Task object in `_tasks` list

**Examples**:
```python
# Update title only
result = update_task(0, new_title="Buy groceries")
# Returns: (True, "Success: Task updated: Buy groceries", Task(...))

# Update description only
result = update_task(0, new_description="From Walmart")
# Returns: (True, "Success: Task updated: Buy milk", Task(...))

# Update both
result = update_task(0, new_title="Buy groceries", new_description="Milk, eggs")
# Returns: (True, "Success: Task updated: Buy groceries", Task(...))

# Invalid index
result = update_task(99, new_title="Test")
# Returns: (False, "Error: Invalid task number", None)
```

---

### 4. delete_task

**Purpose**: Remove a task from the list

**Signature**:
```python
def delete_task(task_index: int) -> tuple[bool, str, Optional[Task]]
```

**Parameters**:
| Parameter | Type | Required | Default | Constraints |
|-----------|------|----------|---------|-------------|
| `task_index` | `int` | Yes | N/A | 0 <= index < len(_tasks) |

**Returns**:
| Success | Message | Data |
|---------|---------|------|
| `True` | `"Success: Task deleted"` | Deleted `Task` object (for confirmation) |
| `False` | `"Error: Invalid task number"` | `None` |

**Behavior**:
1. Validate task_index is within bounds
2. Remove task from `_tasks` list using `pop()`
3. Return success with deleted task (for display confirmation)

**Error Conditions**:
- Invalid index → `(False, "Error: Invalid task number", None)`

**Side Effects**:
- Removes Task from `_tasks` list
- Shifts indices of subsequent tasks

**Examples**:
```python
# Success
result = delete_task(0)
# Returns: (True, "Success: Task deleted", Task(...))

# Invalid index
result = delete_task(99)
# Returns: (False, "Error: Invalid task number", None)
```

---

### 5. toggle_task_status

**Purpose**: Toggle a task's completion status

**Signature**:
```python
def toggle_task_status(task_index: int) -> tuple[bool, str, Optional[Task]]
```

**Parameters**:
| Parameter | Type | Required | Default | Constraints |
|-----------|------|----------|---------|-------------|
| `task_index` | `int` | Yes | N/A | 0 <= index < len(_tasks) |

**Returns**:
| Success | Message | Data |
|---------|---------|------|
| `True` | `"Success: Task status updated: {title}"` | Updated `Task` object |
| `False` | `"Error: Invalid task number"` | `None` |

**Behavior**:
1. Validate task_index is within bounds
2. Call `task.toggle_status()` on the task
3. Return success with updated task reference

**Error Conditions**:
- Invalid index → `(False, "Error: Invalid task number", None)`

**Side Effects**:
- Modifies `is_complete` attribute of Task object

**Examples**:
```python
# Toggle incomplete → complete
result = toggle_task_status(0)
# Returns: (True, "Success: Task status updated: Buy milk", Task(...))

# Toggle complete → incomplete
result = toggle_task_status(0)
# Returns: (True, "Success: Task status updated: Buy milk", Task(...))

# Invalid index
result = toggle_task_status(99)
# Returns: (False, "Error: Invalid task number", None)
```

---

### 6. get_task_count

**Purpose**: Get the total number of tasks

**Signature**:
```python
def get_task_count() -> int
```

**Parameters**: None

**Returns**: `int` - Number of tasks in the list

**Behavior**:
1. Return `len(_tasks)`

**Side Effects**: None (read-only)

**Examples**:
```python
count = get_task_count()
# Returns: 5 (if 5 tasks exist)
```

---

## Index Conversion Utilities

### user_id_to_index

**Purpose**: Convert user-facing ID (1-based) to internal index (0-based)

**Signature**:
```python
def user_id_to_index(user_id: int) -> int
```

**Parameters**:
| Parameter | Type | Required | Constraints |
|-----------|------|----------|-------------|
| `user_id` | `int` | Yes | user_id >= 1 |

**Returns**: `int` - Internal index (user_id - 1)

**Behavior**:
1. Return `user_id - 1`
2. No validation (caller must validate range)

**Examples**:
```python
index = user_id_to_index(1)  # Returns: 0
index = user_id_to_index(5)  # Returns: 4
```

---

### index_to_user_id

**Purpose**: Convert internal index (0-based) to user-facing ID (1-based)

**Signature**:
```python
def index_to_user_id(index: int) -> int
```

**Parameters**:
| Parameter | Type | Required | Constraints |
|-----------|------|----------|-------------|
| `index` | `int` | Yes | index >= 0 |

**Returns**: `int` - User-facing ID (index + 1)

**Behavior**:
1. Return `index + 1`

**Examples**:
```python
user_id = index_to_user_id(0)  # Returns: 1
user_id = index_to_user_id(4)  # Returns: 5
```

---

## Global State

### _tasks

**Type**: `list[Task]`
**Scope**: Module-level private variable
**Initial Value**: `[]` (empty list)
**Lifetime**: Application session

**Access Pattern**:
- **Read**: `view_all_tasks()`, all display operations
- **Append**: `add_task()`
- **Modify**: `update_task()`, `toggle_task_status()`
- **Delete**: `delete_task()`

**Concurrency**: None (single-threaded CLI application)

---

## Error Handling Strategy

### Validation Errors
- Caught at service layer
- Returned as `(False, error_message, None)` tuple
- Never raise exceptions to CLI layer (except critical bugs)

### Index Errors
- Validated before accessing `_tasks[index]`
- Return error tuple if out of bounds

### Data Validation
- Title emptiness checked before Task creation
- Task.__post_init__ may raise ValueError (CLI catches)

---

## Type Safety

All functions use full type hints:
- Parameters: Explicit types (`str`, `int`, `Optional[str]`)
- Return types: `tuple[bool, str, Optional[Task]]` or `list[Task]`
- Internal variables: Inferred from usage

**Type Checking**: Compatible with mypy/pyright

---

## Testing Contracts

Each function must have tests for:
1. **Success cases**: Valid inputs → expected output
2. **Error cases**: Invalid inputs → error tuple
3. **Edge cases**: Empty lists, boundary indices, UTF-8
4. **Side effects**: State changes verified

See `tests/test_services.py` for implementations.

# Data Model: Phase I Todo Console App

**Feature**: 001-todo-console-app
**Created**: 2025-12-28
**Purpose**: Define data structures and their relationships for the todo application

## Entity: Task

### Overview
Represents a single todo item in the system. Tasks are stored in-memory and exist only for the duration of the application session.

### Attributes

| Attribute | Type | Required | Default | Constraints | Description |
|-----------|------|----------|---------|-------------|-------------|
| `title` | `str` | Yes | N/A | Non-empty after strip | Primary task description |
| `description` | `str` | No | `""` | None | Optional detailed information |
| `is_complete` | `bool` | Yes | `False` | None | Completion status flag |
| `created_at` | `datetime` | Yes | `datetime.now()` | None | Timestamp of task creation |

### Validation Rules

1. **Title Validation**:
   - MUST NOT be empty string
   - MUST NOT be whitespace-only (after `.strip()`)
   - Maximum length: No explicit limit (Python string handles this)
   - UTF-8 characters allowed (emojis, international text)

2. **Description Validation**:
   - Optional field (empty string is valid)
   - No content restrictions
   - UTF-8 characters allowed

3. **Status Validation**:
   - Must be boolean type
   - Only two valid states: `True` (complete) or `False` (incomplete)

4. **Created At**:
   - Automatically set at task creation
   - Immutable (not updated)
   - Used for display order (creation sequence)

### State Transitions

```
[New Task Created]
       │
       ↓
   is_complete = False ────────────────┐
       │                               │
       │ (User marks complete)         │
       ↓                               │
   is_complete = True                  │
       │                               │
       │ (User toggles back)           │
       └───────────────────────────────┘
```

**States**:
- **Incomplete** (`is_complete = False`): Default state for new tasks
- **Complete** (`is_complete = True`): Task marked as done

**Transitions**:
- Incomplete → Complete: User invokes "Mark Complete/Incomplete" operation
- Complete → Incomplete: User invokes "Mark Complete/Incomplete" operation (toggle)

### Implementation (Python dataclass)

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Task:
    """
    Represents a single todo item.

    Attributes:
        title: The main task description (required, non-empty)
        description: Optional detailed information
        is_complete: Completion status (default: False)
        created_at: Task creation timestamp (auto-generated)
    """
    title: str
    description: str = ""
    is_complete: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate and clean task data after initialization."""
        self.title = self.title.strip()
        self.description = self.description.strip()

        if not self.title:
            raise ValueError("Task title cannot be empty")

    def toggle_status(self) -> None:
        """Toggle completion status between complete and incomplete."""
        self.is_complete = not self.is_complete

    def display_status(self) -> str:
        """Return visual status indicator for display."""
        return "✓" if self.is_complete else "✗"

    def __str__(self) -> str:
        """Human-readable string representation."""
        status = self.display_status()
        if self.description:
            return f"[{status}] {self.title}: {self.description}"
        return f"[{status}] {self.title}"
```

### Design Decisions

1. **Dataclass Choice**:
   - Reduces boilerplate (auto-generates `__init__`, `__repr__`, `__eq__`)
   - Clean, readable syntax
   - Native Python 3.12 feature (no external dependencies)
   - Integrates well with type hints

2. **field(default_factory=datetime.now)**:
   - Avoids mutable default argument issue
   - Each task gets unique timestamp
   - Captured at instantiation time

3. **Validation in __post_init__**:
   - Catches invalid tasks at creation time
   - Prevents empty-title tasks from existing
   - Fails fast (ValueError if title empty)

4. **Helper Methods**:
   - `toggle_status()`: Encapsulates toggle logic
   - `display_status()`: Centralizes status formatting
   - `__str__()`: Provides consistent display format

5. **Immutable created_at**:
   - No setter provided
   - Represents historical fact (when task created)
   - Can be used for sorting if needed in future

---

## Storage: TaskList

### Overview
In-memory collection of Task objects. Exists as module-level list in `services.py`.

### Structure

```python
# Global module variable in services.py
_tasks: list[Task] = []
```

### Characteristics

- **Type**: Python `list[Task]`
- **Scope**: Module-level private variable (prefixed with `_`)
- **Lifetime**: Application session (cleared on exit)
- **Ordering**: Insertion order (tasks appear in creation sequence)
- **Indexing**: 0-based internally, 1-based for user display

### Operations

| Operation | Complexity | Method |
|-----------|------------|--------|
| Add task | O(1) | `_tasks.append(task)` |
| Get task by index | O(1) | `_tasks[index]` |
| View all tasks | O(n) | `for task in _tasks` |
| Update task | O(1) | Direct access via index |
| Delete task | O(n) | `_tasks.pop(index)` |
| Count tasks | O(1) | `len(_tasks)` |

### Index Mapping

**User-facing IDs** (displayed in menu):
- Start at 1 (human-friendly)
- Sequential numbering
- Re-assigned after deletion

**Internal indices** (Python list):
- Start at 0 (Python convention)
- Conversion: `internal_index = user_id - 1`
- Validation: `0 <= internal_index < len(_tasks)`

**Example**:
```
User View:          Internal Storage:
1. Buy milk         _tasks[0] = Task("Buy milk")
2. Write report     _tasks[1] = Task("Write report")
3. Call dentist     _tasks[2] = Task("Call dentist")
```

### Constraints

- No persistence (in-memory only per constitution)
- No concurrent access (single-threaded application)
- No size limit (limited by available memory)
- No duplicate prevention (user can add identical tasks)

---

## Relationships

### Current System (Phase I)
- **No relationships**: Single entity (Task) in isolated collection
- **No foreign keys**: Tasks are independent
- **No hierarchies**: Flat list structure

### Future Considerations (Out of Scope)
If Phase II extends the model:

```
User (1) ──────── (N) Task
  │
  └─ has many tasks

Task (N) ──────── (N) Tag
  │
  └─ can have multiple tags

Task (1) ──────── (N) Comment
  │
  └─ can have multiple comments
```

---

## Data Validation Summary

| Field | Validation Point | Rules | Error Handling |
|-------|-----------------|-------|----------------|
| Title | Task.__post_init__ | Non-empty after strip | Raise ValueError |
| Title | services.add_task() | Pre-check before creation | Return (False, error_msg, None) |
| Description | None | Always valid | N/A |
| is_complete | Type system | Must be bool | Type error at runtime |
| created_at | Type system | Must be datetime | Type error at runtime |

---

## Memory Considerations

### Task Object Size (Estimated)

```
Task object:
- title: ~50-100 chars avg = ~100-200 bytes
- description: ~0-500 chars avg = ~0-1000 bytes
- is_complete: 1 byte (bool)
- created_at: 24 bytes (datetime object)
- Python object overhead: ~40 bytes

Total per task: ~200-1300 bytes (avg ~500 bytes)
```

### Capacity Analysis

```
100 tasks: ~50 KB
1,000 tasks: ~500 KB
10,000 tasks: ~5 MB
```

**Conclusion**: Memory is not a concern for target use case (< 1000 tasks per session).

---

## Testing Strategies

### Unit Tests (test_models.py)

1. **Task Creation**:
   ```python
   def test_task_creation_with_title_only():
       task = Task("Buy milk")
       assert task.title == "Buy milk"
       assert task.description == ""
       assert task.is_complete is False
       assert isinstance(task.created_at, datetime)
   ```

2. **Title Validation**:
   ```python
   def test_task_rejects_empty_title():
       with pytest.raises(ValueError):
           Task("")

   def test_task_rejects_whitespace_title():
       with pytest.raises(ValueError):
           Task("   ")
   ```

3. **UTF-8 Support**:
   ```python
   def test_task_supports_utf8_characters():
       task = Task("買い物 🛒", "Milk, eggs, bread")
       assert task.title == "買い物 🛒"
   ```

4. **Status Toggle**:
   ```python
   def test_task_toggle_status():
       task = Task("Test")
       assert task.is_complete is False
       task.toggle_status()
       assert task.is_complete is True
       task.toggle_status()
       assert task.is_complete is False
   ```

5. **Display Formatting**:
   ```python
   def test_task_display_status():
       task = Task("Test")
       assert task.display_status() == "✗"
       task.toggle_status()
       assert task.display_status() == "✓"
   ```

---

## Summary

**Single Entity**: Task (title, description, is_complete, created_at)
**Storage**: In-memory Python list
**Validation**: At creation + service layer
**No Relationships**: Flat structure for Phase I
**Memory Efficient**: <1 MB for typical usage (<1000 tasks)
**Type Safe**: Full type hints with dataclass

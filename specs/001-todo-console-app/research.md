# Research & Technical Decisions: Phase I Todo Console App

**Feature**: 001-todo-console-app
**Created**: 2025-12-28
**Purpose**: Document technical research and design decisions for Phase I implementation

## Research Questions Resolved

### 1. Data Storage Strategy (In-Memory)

**Decision**: Use Python list to store Task objects

**Rationale**:
- Constitution requires in-memory storage only (no persistence)
- List provides ordered storage (tasks in creation order)
- Simple indexing for task selection (1-based display, 0-based internal)
- Direct iteration for display operations
- No complex querying needed (show all tasks is the only view requirement)

**Alternatives Considered**:
- Dictionary with task ID as key: More complex than needed; list index serves as implicit ID
- Set: Cannot maintain insertion order reliably; no benefit for this use case
- Deque: Adds complexity without performance benefit for <100 tasks

**Tradeoffs**:
- ✅ Simple, readable code
- ✅ Efficient for small-medium datasets (<1000 tasks)
- ✅ Natural ordering (insertion order)
- ❌ O(n) search by ID (acceptable for target scale)
- ❌ No persistence (intentional per constitution)

---

### 2. Task Identification Strategy

**Decision**: Use list index + 1 as user-facing task ID (1-based indexing)

**Rationale**:
- Matches user expectation (lists start at 1 in human context)
- Simple mapping: display_id = index + 1, internal_id = display_id - 1
- No need for UUID or auto-increment counter
- IDs remain stable during session (no deletion gaps in Phase I)

**Alternatives Considered**:
- UUID: Overkill for in-memory session; adds complexity
- Auto-increment counter: Requires additional state management; gaps after deletion confuse users
- 0-based display: Confusing for non-technical users

**Tradeoffs**:
- ✅ User-friendly (familiar 1-based lists)
- ✅ Zero additional state (index is identity)
- ⚠️ IDs shift after deletion (mitigated by re-displaying list after each operation)

---

### 3. Console Menu System Architecture

**Decision**: Infinite loop with pattern matching on user input (1-6)

**Rationale**:
- Clear separation: main.py (entry + loop) → cli.py (menu display + routing) → services.py (business logic)
- Single Responsibility: Each module has one job
- Testable: Can test menu logic independently from I/O
- Matches Python best practices for console applications

**Pattern**:
```
main.py: while True loop
  └─> cli.py: display_menu() + get_choice()
      └─> cli.py: route_choice()
          └─> services.py: add_task() / view_tasks() / etc.
```

**Alternatives Considered**:
- Command pattern with classes: Over-engineered for 5 operations
- Single-file script: Violates SRP; hard to test
- Event-driven architecture: Unnecessary complexity for synchronous CLI

**Tradeoffs**:
- ✅ Clean separation of concerns
- ✅ Easy to test each layer independently
- ✅ Follows standard CLI app structure
- ❌ Slightly more boilerplate than single-file (acceptable tradeoff)

---

### 4. Input Validation Strategy

**Decision**: Validate at service layer with explicit error returns

**Rationale**:
- Services return tuple: (success: bool, message: str, data: Optional[Task])
- Allows CLI layer to handle display without knowing business rules
- Type hints enforce contract: `tuple[bool, str, Optional[Task]]`
- Consistent error handling across all operations

**Example**:
```python
def add_task(title: str, description: str = "") -> tuple[bool, str, Optional[Task]]:
    if not title or not title.strip():
        return (False, "Error: Title cannot be empty", None)
    task = Task(title.strip(), description.strip())
    tasks.append(task)
    return (True, f"Task added: {task.title}", task)
```

**Alternatives Considered**:
- Exceptions: More Pythonic but heavier; overkill for validation errors
- Return None on error: Ambiguous; can't distinguish error types
- Boolean flags only: Loses error message context

**Tradeoffs**:
- ✅ Explicit error handling (no hidden exceptions)
- ✅ Type-safe with tuple + Optional
- ✅ Easy to test (check tuple values)
- ❌ More verbose than exceptions (acceptable for clarity)

---

### 5. Status Representation

**Decision**: Boolean flag `is_complete: bool` defaulting to False

**Rationale**:
- Simple binary state (complete/incomplete)
- Python boolean is memory-efficient
- Natural default: new tasks are incomplete
- Easy to toggle: `task.is_complete = not task.is_complete`

**Display Representation**:
- ✓ for complete (Unicode character, widely supported)
- ✗ for incomplete
- Alternative: [X] and [ ] if Unicode issues arise

**Alternatives Considered**:
- Enum (COMPLETE, INCOMPLETE): Over-engineered for binary state
- String ("complete", "incomplete"): More memory, slower comparison
- Integer (0, 1): Less readable than boolean

**Tradeoffs**:
- ✅ Memory efficient (1 byte)
- ✅ Readable code (`if task.is_complete`)
- ✅ Built-in toggle logic
- ⚠️ Unicode symbols may vary by terminal (fallback to ASCII available)

---

### 6. Type Hints Strategy

**Decision**: Full type hints on all functions per constitution requirement

**Approach**:
```python
from typing import Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    title: str
    description: str = ""
    is_complete: bool = False
    created_at: datetime = datetime.now()

def add_task(title: str, description: str = "") -> tuple[bool, str, Optional[Task]]:
    ...
```

**Rationale**:
- Constitution mandates type hints for all functions
- dataclass reduces boilerplate for Task model
- Optional[Task] clearly indicates potential None return
- Modern Python typing (3.12+) supports native syntax

**Alternatives Considered**:
- NamedTuple: Less flexible than dataclass (immutability not needed)
- Regular class: More boilerplate than dataclass
- No types: Violates constitution requirement

**Tradeoffs**:
- ✅ Constitution compliant
- ✅ IDE support (autocomplete, type checking)
- ✅ Self-documenting code
- ✅ Catches errors at development time (mypy/pyright)

---

### 7. UTF-8 Encoding Strategy

**Decision**: Explicit UTF-8 encoding on all I/O operations

**Implementation**:
- Set console encoding at startup: `sys.stdout.reconfigure(encoding='utf-8')`
- No file I/O needed (in-memory only)
- Task title/description accept any valid Python string (Unicode by default in Python 3)

**Rationale**:
- Constitution requires UTF-8 support
- Python 3 strings are Unicode by default
- Only I/O boundary needs explicit encoding
- Windows console may default to cp1252; reconfiguration ensures UTF-8

**Testing Strategy**:
- Test cases include emojis (🎯, ✅)
- Test international characters (日本語, العربية)
- Verify display in Windows terminal

**Alternatives Considered**:
- Assume system default: Unreliable on Windows
- ASCII-only: Violates UTF-8 requirement
- Encode/decode manually: Unnecessary with reconfigure

**Tradeoffs**:
- ✅ Full Unicode support
- ✅ One-line configuration
- ✅ Compatible with Windows console
- ⚠️ Older Windows terminals may still have display issues (terminal limitation, not app bug)

---

### 8. Testing Framework

**Decision**: pytest with fixtures for task list setup

**Rationale**:
- Constitution allows pytest as only external dependency
- Fixtures enable clean test setup/teardown
- Parametrized tests reduce duplication
- Matches Python community standard

**Test Structure**:
```
tests/
├── test_models.py       # Task dataclass tests
├── test_services.py     # Business logic tests (core functionality)
├── test_cli.py          # Menu/display tests (I/O mocking)
└── conftest.py          # Shared fixtures
```

**Coverage Goals**:
- 100% of services.py (business logic)
- 90%+ of cli.py (menu logic)
- 100% of models.py (Task class)
- Edge cases from spec (empty titles, UTF-8, etc.)

**Alternatives Considered**:
- unittest: More verbose; pytest is more Pythonic
- No tests: Violates best practices and spec requirements
- Custom test runner: Reinventing the wheel

**Tradeoffs**:
- ✅ Industry standard
- ✅ Clean, readable test syntax
- ✅ Powerful fixtures and parametrization
- ✅ Constitution-approved dependency

---

### 9. Error Message Design

**Decision**: Prefix-based messages (Error:, Success:, Info:)

**Format**:
- `Error: <specific problem>` - Red or bold in terminal
- `Success: <confirmation>` - Green if colorama used (future enhancement)
- `Info: <neutral message>` - Default color

**Examples**:
- "Error: Title cannot be empty"
- "Success: Task added: Buy groceries"
- "Info: No tasks found"

**Rationale**:
- Consistent, scannable format
- Clear severity indication
- Accessible (doesn't rely on color alone)
- Matches CLI best practices

**Alternatives Considered**:
- Color-only: Not accessible; requires external library
- No prefixes: Ambiguous message type
- Numeric codes: Less user-friendly

**Tradeoffs**:
- ✅ User-friendly and accessible
- ✅ No external dependencies
- ✅ Future color enhancement possible
- ✅ Consistent UX

---

### 10. Module Responsibilities

**Decision**: Four-module architecture

| Module | Responsibility | Dependencies |
|--------|---------------|--------------|
| `main.py` | Entry point, main loop, exit handling | cli, sys |
| `src/models.py` | Task dataclass definition | dataclasses, datetime |
| `src/services.py` | Business logic, task management, validation | models, typing |
| `src/cli.py` | Menu display, input handling, routing | services, models, sys |

**Rationale**:
- Clear separation of concerns
- Each module <200 lines (maintainable)
- Testable in isolation
- Follows Python project conventions

**Data Flow**:
```
User → main.py → cli.py (input/display) → services.py (logic) → models.py (data)
                   ↑                           ↓
                   └────── (success, msg) ──────┘
```

**Alternatives Considered**:
- Single file: Hard to test and maintain
- More modules (controllers, views, etc.): Over-engineered for 5 operations
- Functional-only (no classes): Works but dataclass makes Task cleaner

**Tradeoffs**:
- ✅ Clear boundaries
- ✅ Easy to test
- ✅ Follows Python conventions
- ✅ Room for growth (add new services without touching CLI)

---

## Summary of Technical Stack

| Component | Choice | Justification |
|-----------|--------|---------------|
| Language | Python 3.12+ | Constitution requirement |
| Storage | List[Task] | In-memory, ordered, simple |
| Task Model | dataclass | Clean, typed, minimal boilerplate |
| Validation | Tuple returns | Explicit, type-safe, testable |
| Testing | pytest | Constitution-approved, industry standard |
| Encoding | UTF-8 (explicit) | Constitution requirement, Windows compatibility |
| Type System | Full type hints | Constitution requirement, mypy-compatible |
| Architecture | 4-module CLI app | Separation of concerns, testable |

## Open Questions / Future Considerations

**None** - All requirements from specification are addressed by the above decisions.

**Phase II Considerations** (out of scope for Phase I):
- Persistent storage (if needed): SQLite or JSON file
- Task filtering: Add filter functions to services
- Task search: Add search capability to services
- Colored output: Add colorama dependency for better UX
- Task priority: Extend Task dataclass with priority field

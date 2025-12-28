# Implementation Plan: Phase I Todo Console App

**Branch**: `001-todo-console-app` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-console-app/spec.md`

---

## Summary

Build a console-based todo application with 5 core features (Add, View, Update, Delete, Mark Complete/Incomplete) using Python 3.12+ with in-memory storage. The application provides a menu-driven interface for task management with UTF-8 support, full type hints, and comprehensive testing via pytest. Architecture follows clean separation of concerns with 4 modules: main.py (entry), cli.py (I/O), services.py (logic), models.py (data).

---

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: None (stdlib only; pytest for testing)
**Storage**: In-memory Python list (no persistence)
**Testing**: pytest with fixtures and parametrization
**Target Platform**: Windows (primary), cross-platform compatible
**Project Type**: Single console application
**Performance Goals**: <1s response for operations, handles 100+ tasks without degradation
**Constraints**: <2s startup time, no external dependencies (except pytest), UTF-8 encoding required
**Scale/Scope**: Single-user, session-based, ~100 tasks typical usage, 1000+ tasks max capacity

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Technical Constraints (from constitution.md)

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Python 3.12+ | ✅ PASS | Specified in requirements and type hints use modern syntax |
| Windows compatible | ✅ PASS | UTF-8 encoding explicitly configured for Windows console |
| In-memory storage only | ✅ PASS | Python list[Task] in services.py, no file/DB operations |
| No external dependencies (except pytest) | ✅ PASS | Only stdlib imports; pytest for testing only |
| Type hints required | ✅ PASS | All functions fully typed; dataclass with type annotations |
| Console menu (1-6 options) | ✅ PASS | Menu with 6 options (5 features + Exit) |
| UTF-8 encoding support | ✅ PASS | sys.stdout.reconfigure(encoding='utf-8') at startup |

### Code Quality Principles

| Principle | Status | Implementation |
|-----------|--------|----------------|
| Separation of concerns | ✅ PASS | 4-module architecture (main/cli/services/models) |
| Testability | ✅ PASS | Service layer pure functions, CLI mockable |
| Type safety | ✅ PASS | Full type hints, mypy-compatible |
| Error handling | ✅ PASS | Explicit tuple returns, user-friendly messages |
| Minimal complexity | ✅ PASS | No over-engineering, single-file modules <200 LOC |

### Design Decisions

| Decision | Rationale | Constitution Alignment |
|----------|-----------|----------------------|
| 4-module structure | Clean boundaries, testable | SRP, testability |
| Dataclass for Task | Minimal boilerplate, type-safe | Type hints, simplicity |
| Tuple return pattern | Explicit errors, no exceptions | Error handling, clarity |
| List storage | Simple, ordered, sufficient for scale | In-memory, no persistence |
| 1-based user IDs | Human-friendly display | User experience |

**Gate Status**: ✅ **PASSED** - All constitution requirements met

---

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-console-app/
├── spec.md                  # Feature specification (P1-P3 user stories, requirements)
├── plan.md                  # This file (/sp.plan command output)
├── research.md              # Phase 0 technical research (10 decisions documented)
├── data-model.md            # Task entity, validation, storage strategy
├── quickstart.md            # User and developer setup guide
├── contracts/
│   └── service-contracts.md # Service layer function contracts
├── checklists/
│   └── requirements.md      # Spec quality validation (14/14 passed)
└── tasks.md                 # Phase 2 output (/sp.tasks command - NOT YET CREATED)
```

### Source Code (repository root)

```text
TodoBase_Hackathon/
├── main.py                  # Entry point, main loop, UTF-8 configuration
├── src/
│   ├── __init__.py          # Package marker
│   ├── models.py            # Task dataclass with validation
│   ├── services.py          # Business logic (add/view/update/delete/toggle)
│   └── cli.py               # Menu display, input handling, routing
├── tests/
│   ├── __init__.py          # Package marker
│   ├── conftest.py          # Shared pytest fixtures (sample tasks, etc.)
│   ├── test_models.py       # Task dataclass tests (creation, validation, toggle)
│   ├── test_services.py     # Service layer tests (all operations, edge cases)
│   └── test_cli.py          # CLI tests (menu display, input parsing, mocking I/O)
└── specs/                   # Documentation (see above)
```

**Structure Decision**: Option 1 (Single project) selected. This is a standalone console application with no frontend/backend separation or multiple deployment targets. The `src/` directory contains application code, `tests/` mirrors the structure for unit testing, and `specs/` holds all planning artifacts.

---

## Complexity Tracking

**No violations** - All constitution requirements are met without exceptions.

This section intentionally left empty as there are no complexity thresholds exceeded or constitution violations requiring justification.

---

## Architecture Design

### Module Responsibilities

#### main.py (Entry Point)
**Responsibility**: Application bootstrap and main event loop

**Functions**:
```python
def configure_utf8() -> None:
    """Configure console for UTF-8 output (Windows compatibility)"""

def main() -> None:
    """Main application loop"""
```

**Flow**:
1. Configure UTF-8 encoding on stdout
2. Print welcome banner
3. Enter infinite loop:
   - Display menu (via cli.py)
   - Get user choice (via cli.py)
   - Route to appropriate handler (via cli.py)
   - Handle exit (break loop)
4. Print goodbye message

**Dependencies**: `sys`, `src.cli`

**Size Estimate**: ~40 LOC

---

#### src/models.py (Data Layer)
**Responsibility**: Task entity definition and validation

**Classes**:
```python
@dataclass
class Task:
    title: str
    description: str = ""
    is_complete: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate and clean task data"""

    def toggle_status(self) -> None:
        """Toggle completion status"""

    def display_status(self) -> str:
        """Return visual status indicator (✓ or ✗)"""

    def __str__(self) -> str:
        """Human-readable representation for display"""
```

**Validation**:
- `__post_init__`: Strip whitespace, raise ValueError if title empty
- Ensures data integrity at creation time

**Dependencies**: `dataclasses`, `datetime`

**Size Estimate**: ~50 LOC

---

#### src/services.py (Business Logic Layer)
**Responsibility**: Task management operations and validation

**Global State**:
```python
_tasks: list[Task] = []  # In-memory task storage
```

**Functions**:
```python
def add_task(title: str, description: str = "") -> tuple[bool, str, Optional[Task]]:
    """Create and store new task"""

def view_all_tasks() -> tuple[bool, str, list[Task]]:
    """Retrieve all tasks for display"""

def update_task(task_index: int, new_title: str | None = None,
                new_description: str | None = None) -> tuple[bool, str, Optional[Task]]:
    """Modify existing task"""

def delete_task(task_index: int) -> tuple[bool, str, Optional[Task]]:
    """Remove task from list"""

def toggle_task_status(task_index: int) -> tuple[bool, str, Optional[Task]]:
    """Toggle task completion status"""

def get_task_count() -> int:
    """Return number of tasks"""

def user_id_to_index(user_id: int) -> int:
    """Convert 1-based user ID to 0-based index"""

def index_to_user_id(index: int) -> int:
    """Convert 0-based index to 1-based user ID"""
```

**Return Pattern**: All mutation functions return `tuple[bool, str, Optional[T]]`
- bool: Success flag
- str: User message (error or confirmation)
- Optional[T]: Result data (Task or None)

**Validation Strategy**:
- Index bounds checking before list access
- Title emptiness validation before Task creation
- Return error tuples instead of raising exceptions

**Dependencies**: `typing`, `src.models`

**Size Estimate**: ~150 LOC

---

#### src/cli.py (Presentation Layer)
**Responsibility**: User interaction, menu display, input handling

**Functions**:
```python
def display_menu() -> None:
    """Print main menu options"""

def get_choice() -> str:
    """Get and validate user menu selection"""

def display_tasks(tasks: list[Task]) -> None:
    """Format and print task list with IDs"""

def handle_add_task() -> None:
    """Add task flow: prompt inputs, call service, display result"""

def handle_view_tasks() -> None:
    """View tasks flow: call service, display tasks"""

def handle_update_task() -> None:
    """Update task flow: show tasks, get selection, prompt changes, update"""

def handle_delete_task() -> None:
    """Delete task flow: show tasks, get selection, confirm, delete"""

def handle_toggle_status() -> None:
    """Toggle status flow: show tasks, get selection, toggle"""

def route_choice(choice: str) -> bool:
    """Route menu choice to appropriate handler, return continue flag"""
```

**Input Handling**:
- Numeric validation for menu choices
- Empty input handling (defaults or re-prompts)
- Confirmation dialogs (y/n) for destructive actions

**Output Formatting**:
- Numbered task lists (1-based)
- Status indicators (✓ / ✗)
- Section headers and dividers
- Color-coded messages (future enhancement with colorama)

**Dependencies**: `sys`, `src.services`, `src.models`

**Size Estimate**: ~200 LOC

---

### Data Flow

```
User Input
    │
    ↓
main.py (main loop)
    │
    ↓
cli.py (display_menu, get_choice)
    │
    ↓
cli.py (route_choice) → handler functions
    │
    ↓
services.py (business logic)
    │
    ├─→ models.py (Task creation/modification)
    │
    ↓
services.py (return tuple)
    │
    ↓
cli.py (display result)
    │
    ↓
main.py (loop continues or exits)
```

**Example Flow (Add Task)**:
1. User enters "1" at menu
2. `main.py` calls `cli.get_choice()` → returns "1"
3. `main.py` calls `cli.route_choice("1")` → dispatches to `handle_add_task()`
4. `handle_add_task()` prompts for title and description
5. Calls `services.add_task(title, desc)` → returns `(True, "Success: ...", Task)`
6. Displays success message
7. Returns to main loop

---

### Error Handling Strategy

#### Validation Errors
- **Where**: Service layer (services.py)
- **How**: Return `(False, "Error: ...", None)` tuple
- **Examples**:
  - Empty title → "Error: Title cannot be empty"
  - Invalid task number → "Error: Invalid task number"

#### User Input Errors
- **Where**: CLI layer (cli.py)
- **How**: Validate input, re-prompt if invalid
- **Examples**:
  - Non-numeric menu choice → "Invalid choice. Please enter 1-6."
  - Out-of-range task selection → Service layer handles, returns error

#### Critical Errors
- **Where**: Task creation (models.py)
- **How**: `ValueError` raised if post-validation fails
- **Handling**: CLI catches and displays error message
- **Examples**: Task with empty title after strip (shouldn't happen if service validates)

#### Display Strategy
- Prefix-based messages: "Error:", "Success:", "Info:"
- Clear, actionable language
- No stack traces shown to user
- Future: Color coding (red=error, green=success, blue=info)

---

### Testing Strategy

#### Unit Tests (tests/test_models.py)
**Coverage**: Task dataclass behavior

**Test Cases**:
1. Task creation with valid inputs
2. Task creation with empty title (ValueError)
3. Task creation with whitespace-only title (ValueError)
4. Task creation with UTF-8 characters
5. Task status toggle (incomplete ↔ complete)
6. Task display_status() formatting
7. Task __str__() output with/without description

**Fixtures**: None needed (simple Task construction)

---

#### Unit Tests (tests/test_services.py)
**Coverage**: Business logic operations

**Test Cases**:
- `add_task()`:
  - Success with title only
  - Success with title + description
  - Error on empty title
  - Error on whitespace-only title
  - UTF-8 characters in title/description

- `view_all_tasks()`:
  - Success with tasks present
  - Info message when no tasks
  - Returns copy of list (not reference)

- `update_task()`:
  - Success updating title
  - Success updating description
  - Success updating both
  - Error on invalid index
  - Error on empty new title

- `delete_task()`:
  - Success deleting task
  - Error on invalid index
  - Verify task removed from list

- `toggle_task_status()`:
  - Success toggling incomplete → complete
  - Success toggling complete → incomplete
  - Error on invalid index

- `get_task_count()`:
  - Correct count after add/delete

- Index conversion utilities:
  - `user_id_to_index()` correctness
  - `index_to_user_id()` correctness

**Fixtures** (conftest.py):
```python
@pytest.fixture
def empty_task_list():
    """Reset global _tasks to empty"""

@pytest.fixture
def sample_tasks():
    """Provide 3 sample tasks for testing"""
```

---

#### Integration Tests (tests/test_cli.py)
**Coverage**: CLI interactions and flow

**Approach**: Mock `input()` and capture `print()` output

**Test Cases**:
- Menu display format
- Valid menu choice handling
- Invalid menu choice handling
- Task display formatting
- Add task workflow (mocked inputs)
- Update task workflow (mocked inputs)
- Delete task confirmation workflow
- Exit choice terminates loop

**Mocking Strategy**:
```python
@patch('builtins.input', side_effect=['1', 'Test Task', ''])
@patch('builtins.print')
def test_add_task_flow(mock_print, mock_input):
    # Test add task with mocked user input
```

---

#### Test Execution

**Commands**:
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_services.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run with verbose output
pytest -v
```

**Coverage Goals**:
- `models.py`: 100%
- `services.py`: 100%
- `cli.py`: 90% (some display formatting may be hard to test)
- `main.py`: 80% (main loop logic)

**CI/CD**: Not in scope for Phase I, but tests are CI-ready

---

### Type Checking Strategy

**Approach**: Full type hints on all functions per constitution

**Type Checker**: mypy (recommended) or pyright

**Configuration** (pyproject.toml or mypy.ini):
```ini
[mypy]
python_version = 3.12
strict = True
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

**Commands**:
```bash
# Check all source files
mypy main.py src/

# Check with specific config
mypy --config-file mypy.ini .
```

**Expected Outcome**: Zero type errors

---

### UTF-8 Encoding Strategy

**Implementation** (main.py):
```python
import sys

def configure_utf8() -> None:
    """Configure console for UTF-8 output"""
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
```

**Call Site**: First line in `main()` before any output

**Rationale**:
- Windows console defaults to cp1252 encoding
- Reconfiguration ensures UTF-8 for Unicode characters
- One-time setup at startup
- Transparent to rest of application

**Testing**:
- Manual test on Windows with emoji and international characters
- Automated test with UTF-8 task titles in test suite

---

## Implementation Phases

### Phase 0: Research ✅ COMPLETE
**Output**: [research.md](./research.md)

**Decisions Documented**:
1. Data storage strategy (list)
2. Task identification (1-based IDs)
3. Console menu architecture
4. Input validation strategy
5. Status representation (boolean)
6. Type hints strategy (dataclass)
7. UTF-8 encoding strategy
8. Testing framework (pytest)
9. Error message design
10. Module responsibilities

---

### Phase 1: Design & Contracts ✅ COMPLETE
**Outputs**:
- [data-model.md](./data-model.md) - Task entity specification
- [contracts/service-contracts.md](./contracts/service-contracts.md) - Service layer API
- [quickstart.md](./quickstart.md) - User and developer guide
- This file (plan.md) - Architecture documentation

**Deliverables**:
- Task dataclass specification with validation rules
- Service layer function signatures and contracts
- Storage strategy (list[Task])
- Error handling patterns
- Testing strategy

---

### Phase 2: Task Breakdown 🔜 NEXT
**Command**: `/sp.tasks`

**Expected Output**: tasks.md with implementation tasks

**Task Categories** (estimated):
1. **Setup**: Project structure, __init__.py files
2. **Models**: Implement Task dataclass (test-driven)
3. **Services**: Implement business logic functions (test-driven)
4. **CLI**: Implement menu and handlers (test-driven)
5. **Main**: Implement entry point and main loop
6. **Integration**: End-to-end testing
7. **Documentation**: Update README, verify quickstart

---

### Phase 3: Implementation 🔜 FUTURE
**Command**: `/sp.implement`

**Approach**: TDD (Red-Green-Refactor)
1. Write failing test
2. Implement minimum code to pass
3. Refactor for quality
4. Repeat

**Order**: models → services → cli → main → integration

---

## Key Design Decisions

### Decision 1: 4-Module Architecture

**Options Considered**:
1. Single file script
2. 4-module structure (main/models/services/cli)
3. 6+ module structure (add controllers, views, repositories)

**Choice**: 4-module structure

**Rationale**:
- ✅ Clear separation of concerns (SRP)
- ✅ Testable in isolation
- ✅ Each module <200 LOC (maintainable)
- ✅ Room for growth without over-engineering
- ❌ Single file is too monolithic
- ❌ 6+ modules is over-engineered for 5 operations

**Tradeoffs**: Slightly more boilerplate than single file, but vastly better testability and maintainability

---

### Decision 2: Tuple Return Pattern

**Options Considered**:
1. Exceptions for validation errors
2. Tuple returns: (bool, str, Optional[T])
3. Result monad/dataclass
4. Boolean only (lose error context)

**Choice**: Tuple returns

**Rationale**:
- ✅ Explicit error handling (no hidden control flow)
- ✅ Type-safe with Optional
- ✅ Easy to test (assert on tuple values)
- ✅ Clear success/failure distinction
- ❌ More verbose than exceptions
- ❌ Requires discipline (check success flag)

**Tradeoffs**: Verbosity for clarity and testability

---

### Decision 3: Dataclass for Task

**Options Considered**:
1. Dataclass with post_init validation
2. Regular class with __init__
3. NamedTuple (immutable)
4. Dictionary

**Choice**: Dataclass

**Rationale**:
- ✅ Minimal boilerplate (auto __init__, __repr__, __eq__)
- ✅ Mutable (needed for update operations)
- ✅ Type hints integrate seamlessly
- ✅ __post_init__ hook for validation
- ❌ NamedTuple is immutable (doesn't fit use case)
- ❌ Regular class requires more code

**Tradeoffs**: None - dataclass is ideal fit

---

### Decision 4: List Storage

**Options Considered**:
1. Python list
2. Dictionary with UUID keys
3. SQLite in-memory database
4. Deque

**Choice**: List

**Rationale**:
- ✅ Simple, readable
- ✅ Insertion order preserved
- ✅ Efficient for <1000 items
- ✅ No external dependencies
- ❌ O(n) for search (acceptable at scale)
- ❌ Dict might be faster for lookups (not needed)

**Tradeoffs**: Simplicity over micro-optimization

---

### Decision 5: 1-Based User IDs

**Options Considered**:
1. 1-based display IDs (internal 0-based)
2. 0-based display IDs
3. UUID display
4. Auto-increment counter (with gaps after delete)

**Choice**: 1-based display with mapping

**Rationale**:
- ✅ Human-friendly (users expect lists to start at 1)
- ✅ Simple mapping (id = index + 1)
- ✅ No gaps during session (IDs regenerate on view)
- ❌ 0-based confuses non-technical users
- ❌ UUIDs are overkill for in-memory session

**Tradeoffs**: Slight complexity in conversion for major UX improvement

---

## Risk Analysis

### Risk 1: UTF-8 Display Issues on Older Windows Terminals
**Impact**: Medium (affects UX, not functionality)
**Likelihood**: Low (most users have Windows Terminal or modern console)
**Mitigation**:
- Fallback to ASCII characters ([ ] and [X] instead of ✓/✗)
- Document UTF-8 setup in quickstart.md
- Detect encoding and warn user if not UTF-8

---

### Risk 2: Index Shifting After Deletion Confuses Users
**Impact**: Low (users re-view list after operations)
**Likelihood**: Medium (users may remember old IDs)
**Mitigation**:
- Always re-display task list after operations
- Use descriptive confirmations (show task title, not just ID)
- Future: Add task UUID if needed

---

### Risk 3: No Persistence Leads to Accidental Data Loss
**Impact**: High (user loses all tasks on exit)
**Likelihood**: High (users may expect save)
**Mitigation**:
- Clear messaging: "Tasks are NOT saved. They will be lost when you exit."
- Display warning on first run (future enhancement)
- Confirmation on exit: "You have N tasks. Exit anyway? (y/n)"
- Document in quickstart.md and user stories

---

## Success Criteria Validation

| Success Criterion | Implementation | Validation Method |
|------------------|----------------|-------------------|
| SC-001: Add task in <10s | Simple input prompts | Manual timing test |
| SC-002: View tasks <1s for 100 tasks | List iteration O(n) | Performance test with 100 tasks |
| SC-003: All operations on first attempt | Clear menu, validation | Usability test |
| SC-004: Handles 100+ tasks | List scales well | Load test with 1000 tasks |
| SC-005: UTF-8 display | sys.stdout.reconfigure | UTF-8 test cases |
| SC-006: Zero data loss during session | In-memory list | Session persistence test |
| SC-007: Navigate menu without confusion | Clear labels, numbering | Usability review |
| SC-008: Delete requires confirmation | Confirmation prompt in handle_delete_task() | Test confirmation dialog |
| SC-009: Clear, actionable errors | Prefix-based messages | Error message review |
| SC-010: Startup <2s | Minimal imports, no file I/O | Startup time measurement |

**Overall Status**: All criteria addressable by implementation plan

---

## Next Steps

1. ✅ **Phase 0 Complete**: Research and technical decisions documented
2. ✅ **Phase 1 Complete**: Data model, contracts, and architecture defined
3. 🔜 **Phase 2**: Run `/sp.tasks` to generate implementation task breakdown
4. 🔜 **Phase 3**: Run `/sp.implement` to execute tasks (TDD approach)
5. 🔜 **Phase 4**: Validate against specification and success criteria
6. 🔜 **Phase 5**: Commit and create PR with `/sp.git.commit_pr`

---

## References

- [Feature Specification](./spec.md)
- [Technical Research](./research.md)
- [Data Model](./data-model.md)
- [Service Contracts](./contracts/service-contracts.md)
- [Quickstart Guide](./quickstart.md)
- [Constitution](./.specify/memory/constitution.md)

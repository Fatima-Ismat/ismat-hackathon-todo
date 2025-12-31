# Quickstart Guide: Phase I Todo Console App

**Feature**: 001-todo-console-app
**Created**: 2025-12-28
**Purpose**: Quick setup and usage guide for developers and users

---

## Prerequisites

- **Python**: 3.12 or higher
- **Operating System**: Windows (primary target)
- **Terminal**: Windows Terminal, PowerShell, or Command Prompt with UTF-8 support

---

## Installation

### 1. Clone or Download Repository

```bash
# If using git
git clone <repository-url>
cd TodoBase_Hackathon

# Or download and extract ZIP file
```

### 2. Verify Python Version

```bash
python --version
# Should output: Python 3.12.x or higher
```

### 3. No External Dependencies

Phase I requires **no external dependencies** for running the application (pytest is only needed for testing).

---

## Running the Application

### Start the Application

```bash
# From repository root
python main.py
```

### Expected Output

```
================================
    TODO CONSOLE APP - v1.0
================================

Main Menu:
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
6. Exit

Enter your choice (1-6):
```

---

## Usage Examples

### Example 1: Add a Task

```
Enter your choice (1-6): 1

--- Add New Task ---
Enter task title: Buy groceries
Enter description (optional): Milk, eggs, bread

Success: Task added: Buy groceries

[Returns to main menu]
```

### Example 2: View All Tasks

```
Enter your choice (1-6): 2

--- All Tasks ---
1. [✗] Buy groceries: Milk, eggs, bread
2. [✓] Write report
3. [✗] Call dentist

[Returns to main menu]
```

### Example 3: Mark Task Complete

```
Enter your choice (1-6): 5

--- Mark Task Complete/Incomplete ---
1. [✗] Buy groceries: Milk, eggs, bread
2. [✓] Write report
3. [✗] Call dentist

Enter task number to toggle: 1

Success: Task status updated: Buy groceries

[Returns to main menu]
```

### Example 4: Update a Task

```
Enter your choice (1-6): 3

--- Update Task ---
1. [✓] Buy groceries: Milk, eggs, bread
2. [✓] Write report
3. [✗] Call dentist

Enter task number to update: 2

Current title: Write report
Enter new title (or press Enter to keep): Write quarterly report

Current description:
Enter new description (or press Enter to keep): Q4 2025 financials

Success: Task updated: Write quarterly report

[Returns to main menu]
```

### Example 5: Delete a Task

```
Enter your choice (1-6): 4

--- Delete Task ---
1. [✓] Buy groceries: Milk, eggs, bread
2. [✓] Write quarterly report: Q4 2025 financials
3. [✗] Call dentist

Enter task number to delete: 3

Are you sure you want to delete "Call dentist"? (y/n): y

Success: Task deleted

[Returns to main menu]
```

### Example 6: Exit Application

```
Enter your choice (1-6): 6

Thank you for using Todo Console App!
Exiting...
```

---

## Development Setup

### Install Testing Dependencies

```bash
pip install pytest
```

### Run Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_services.py

# Run with coverage (if pytest-cov installed)
pytest --cov=src --cov-report=html
```

### Project Structure

```
TodoBase_Hackathon/
├── main.py                  # Entry point
├── src/
│   ├── __init__.py
│   ├── models.py            # Task dataclass
│   ├── services.py          # Business logic
│   └── cli.py               # Menu & I/O handling
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test fixtures
│   ├── test_models.py       # Task model tests
│   ├── test_services.py     # Service layer tests
│   └── test_cli.py          # CLI interface tests
└── specs/
    └── 001-todo-console-app/
        ├── spec.md          # Feature specification
        ├── plan.md          # Implementation plan
        ├── data-model.md    # Data model documentation
        └── research.md      # Technical decisions
```

---

## Running Type Checks

### Using mypy (optional)

```bash
# Install mypy
pip install mypy

# Run type checking
mypy main.py src/
```

### Expected Output
```
Success: no issues found in X source files
```

---

## Troubleshooting

### UTF-8 Display Issues (Windows)

**Problem**: Special characters (✓, ✗) or emojis display incorrectly

**Solution 1** - Windows Terminal (Recommended):
1. Install Windows Terminal from Microsoft Store
2. Run application in Windows Terminal

**Solution 2** - Configure PowerShell/CMD:
```powershell
# In PowerShell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Then run
python main.py
```

**Solution 3** - Set environment variable:
```bash
set PYTHONIOENCODING=utf-8
python main.py
```

### Module Import Errors

**Problem**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Run from repository root (not from `src/` directory)
```bash
# Wrong
cd src
python ../main.py

# Correct
cd TodoBase_Hackathon
python main.py
```

### pytest Not Found

**Problem**: `pytest: command not found`

**Solution**: Install pytest
```bash
pip install pytest
```

### Python Version Too Old

**Problem**: `SyntaxError` or type hint issues

**Solution**: Upgrade to Python 3.12+
```bash
python --version  # Check version
# Download Python 3.12+ from python.org
```

---

## Feature Limitations (By Design)

1. **No Persistence**: Tasks are lost when application exits (in-memory only)
2. **No Multi-User**: Single user per session
3. **No Search/Filter**: View shows all tasks only
4. **No Categories**: Tasks cannot be organized into categories
5. **No Due Dates**: No deadline tracking
6. **No Priority Levels**: All tasks treated equally

These are **intentional constraints** for Phase I. Future phases may add these features.

---

## Performance Notes

- **Target Capacity**: Up to 100 tasks without performance degradation (per specification SC-004)
- **Tested Capacity**: 1,000+ tasks (works smoothly on modern hardware)
- **Memory Usage**: < 1 MB for typical usage
- **Startup Time**: < 2 seconds (per specification SC-010)

---

## Common Workflows

### Daily Task Management

```
1. Start application
2. Add today's tasks (option 1)
3. View all tasks (option 2) to review
4. Mark completed tasks (option 5)
5. View all tasks again to see progress
6. Exit (option 6)
```

### Task Correction Workflow

```
1. View all tasks (option 2)
2. Identify task with error
3. Update task (option 3)
4. Confirm changes by viewing again (option 2)
```

### Task Cleanup Workflow

```
1. View all tasks (option 2)
2. Delete completed or irrelevant tasks (option 4)
3. Confirm deletion with 'y'
4. View remaining tasks (option 2)
```

---

## Tips for Best Experience

1. **Use Windows Terminal**: Best UTF-8 character support
2. **Keep Titles Concise**: 50 characters or less for readability
3. **Use Descriptions for Details**: Title = what, Description = how/why
4. **Review Regularly**: Use "View All Tasks" to stay organized
5. **Complete Tasks Promptly**: Mark tasks done to track progress
6. **Exit Gracefully**: Use option 6 to exit (Ctrl+C works but less clean)

---

## Next Steps

After familiarizing yourself with Phase I:

1. **Run Tests**: Verify application works correctly (`pytest`)
2. **Explore Code**: Read `src/models.py`, `src/services.py`, `src/cli.py`
3. **Review Specs**: See `specs/001-todo-console-app/spec.md` for requirements
4. **Suggest Features**: Phase II may include persistence, search, categories

---

## Support

For issues or questions:
- **Specification**: See `specs/001-todo-console-app/spec.md`
- **Architecture**: See `specs/001-todo-console-app/plan.md`
- **Technical Details**: See `specs/001-todo-console-app/research.md`
- **Data Model**: See `specs/001-todo-console-app/data-model.md`

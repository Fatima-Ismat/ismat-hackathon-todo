# Phase I Only - Simple Instructions
# Todo Console App - In Memory Python App

## RULES:
1. I CANNOT write code manually
2. Generate code from specifications only
3. Read: .specify/memory/constitution.md
4. Read: .specify/speckit.specify
5. Create: speckit.plan → speckit.tasks → Generate code

## PHASE I SPECIFIC:
- Python console app only
- In-memory storage (no database)
- 5 basic features (Add, View, Update, Delete, Toggle Complete)
- Simple menu system (1-6 options)

## REFERENCE STRUCTURE (From Sir's Code):
Based on reference implementation, follow this structure:
- `main.py` in root (entry point)
- `src/` folder with:
  - `cli.py` - Command-line interface with menu
  - `models.py` - Task dataclass
  - `services.py` - Business logic (not storage.py)

## PROJECT STRUCTURE TO CREATE:
TodoBase_Hackathon/
├── .specify/
│   ├── speckit.plan     (to create)
│   └── speckit.tasks    (to create)
├── src/                # Not src/todo_app/
│   ├── cli.py
│   ├── models.py
│   └── services.py     # Not storage.py
├── tests/              (to generate)
└── pyproject.toml      (to generate)

## WORKFLOW:
1. You read constitution and requirements
2. You create speckit.plan (technical design)
3. You create speckit.tasks (implementation steps)
4. You generate code for each task
5. I will test and give feedback

## CONSTRAINTS:
- Python 3.12+ (Windows compatible)
- In-memory storage ONLY (use dictionary, not files/database)
- Console menu with 1-6 options
- Type hints required for all functions
- No external dependencies (except pytest for testing)
- Use dataclass for Task model
- Global _next_id for auto-increment IDs
- User-friendly error messages
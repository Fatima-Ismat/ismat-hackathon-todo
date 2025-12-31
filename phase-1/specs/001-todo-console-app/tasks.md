---
description: "Implementation tasks for Phase I Todo Console App"
---

# Tasks: Phase I Todo Console App

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md (architecture), spec.md (user stories P1-P3), research.md (decisions), data-model.md (Task entity), contracts/service-contracts.md

**Tests**: Following TDD (Test-Driven Development) approach - write failing tests FIRST, then implement

**Organization**: Tasks grouped by user story for independent implementation and testing

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US5)
- File paths follow plan.md structure (single project: src/, tests/ at root)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and directory structure

- [X] T001 Create src/ directory with __init__.py package marker
- [X] T002 Create tests/ directory with __init__.py package marker
- [X] T003 [P] Create empty src/models.py for Task dataclass
- [X] T004 [P] Create empty src/services.py for business logic
- [X] T005 [P] Create empty src/cli.py for menu and I/O handling
- [X] T006 [P] Create empty main.py for application entry point
- [X] T007 [P] Create tests/conftest.py for shared pytest fixtures

**Checkpoint**: Directory structure ready - can begin foundational work

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core Task model that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T008 [P] Write failing test for Task creation with title only in tests/test_models.py
- [X] T009 [P] Write failing test for Task creation with title and description in tests/test_models.py
- [X] T010 [P] Write failing test for Task with empty title raises ValueError in tests/test_models.py
- [X] T011 [P] Write failing test for Task with whitespace-only title raises ValueError in tests/test_models.py
- [X] T012 [P] Write failing test for Task creation with UTF-8 characters in tests/test_models.py
- [X] T013 [P] Write failing test for Task toggle_status() method in tests/test_models.py
- [X] T014 [P] Write failing test for Task display_status() method in tests/test_models.py
- [X] T015 [P] Write failing test for Task __str__() method in tests/test_models.py
- [X] T016 Implement Task dataclass in src/models.py with title, description, is_complete, created_at attributes
- [X] T017 Add Task.__post_init__() validation (strip whitespace, raise ValueError if title empty) in src/models.py
- [X] T018 Add Task.toggle_status() method to toggle is_complete in src/models.py
- [X] T019 Add Task.display_status() method returning ✓ or ✗ in src/models.py
- [X] T020 Add Task.__str__() method for human-readable display in src/models.py
- [X] T021 Run pytest tests/test_models.py and verify all tests pass

**Checkpoint**: Foundation ready - Task model complete and tested. User story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks with title (required) and description (optional)

**Independent Test**: Launch app, select "Add Task", enter title and description, verify task is stored and confirmation displayed

### Tests for User Story 1 (TDD - Write FIRST, ensure FAIL)

- [X] T022 [P] [US1] Write failing test for add_task() success with title only in tests/test_services.py
- [X] T023 [P] [US1] Write failing test for add_task() success with title and description in tests/test_services.py
- [X] T024 [P] [US1] Write failing test for add_task() error on empty title in tests/test_services.py
- [X] T025 [P] [US1] Write failing test for add_task() error on whitespace-only title in tests/test_services.py
- [X] T026 [P] [US1] Write failing test for add_task() with UTF-8 characters in tests/test_services.py

### Implementation for User Story 1

- [X] T027 [US1] Initialize module-level _tasks list in src/services.py
- [X] T028 [US1] Implement add_task(title, description) function in src/services.py returning tuple[bool, str, Optional[Task]]
- [X] T029 [US1] Add title validation (strip whitespace, check non-empty) in add_task() in src/services.py
- [X] T030 [US1] Create Task object and append to _tasks list in add_task() in src/services.py
- [X] T031 [US1] Return success tuple with confirmation message in add_task() in src/services.py
- [X] T032 [US1] Run pytest tests/test_services.py::test_add_task* and verify all tests pass
- [X] T033 [US1] Implement handle_add_task() function in src/cli.py
- [X] T034 [US1] Prompt user for task title in handle_add_task() in src/cli.py
- [X] T035 [US1] Prompt user for optional description in handle_add_task() in src/cli.py
- [X] T036 [US1] Call services.add_task() and display result message in handle_add_task() in src/cli.py
- [X] T037 [US1] Add menu option "1. Add Task" to display_menu() in src/cli.py
- [X] T038 [US1] Route choice "1" to handle_add_task() in route_choice() in src/cli.py

**Checkpoint**: User Story 1 complete - users can add tasks with validation

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can see all tasks with status indicators (✓ complete, ✗ incomplete)

**Independent Test**: Add several tasks (some complete, some incomplete), select "View All Tasks", verify all display with correct status

### Tests for User Story 2 (TDD - Write FIRST, ensure FAIL)

- [X] T039 [P] [US2] Write failing test for view_all_tasks() with tasks present in tests/test_services.py
- [X] T040 [P] [US2] Write failing test for view_all_tasks() with empty task list in tests/test_services.py
- [X] T041 [P] [US2] Write failing test for view_all_tasks() returns copy not reference in tests/test_services.py
- [X] T042 [P] [US2] Write failing test for get_task_count() in tests/test_services.py

### Implementation for User Story 2

- [X] T043 [US2] Implement view_all_tasks() function in src/services.py returning tuple[bool, str, list[Task]]
- [X] T044 [US2] Check if _tasks is empty and return info message in view_all_tasks() in src/services.py
- [X] T045 [US2] Return copy of _tasks list (not reference) in view_all_tasks() in src/services.py
- [X] T046 [US2] Implement get_task_count() function returning len(_tasks) in src/services.py
- [X] T047 [US2] Run pytest tests/test_services.py::test_view* and verify all tests pass
- [X] T048 [US2] Implement display_tasks(tasks: list[Task]) function in src/cli.py
- [X] T049 [US2] Format tasks with 1-based numbering and status indicators in display_tasks() in src/cli.py
- [X] T050 [US2] Display task title and description (if present) in display_tasks() in src/cli.py
- [X] T051 [US2] Implement handle_view_tasks() function in src/cli.py
- [X] T052 [US2] Call services.view_all_tasks() and display results in handle_view_tasks() in src/cli.py
- [X] T053 [US2] Handle empty task list with appropriate message in handle_view_tasks() in src/cli.py
- [X] T054 [US2] Add menu option "2. View All Tasks" to display_menu() in src/cli.py
- [X] T055 [US2] Route choice "2" to handle_view_tasks() in route_choice() in src/cli.py

**Checkpoint**: User Stories 1 AND 2 complete - MVP functional (add and view tasks)

---

## Phase 5: User Story 3 - Mark Task Complete/Incomplete (Priority: P2)

**Goal**: Users can toggle task status between complete (✓) and incomplete (✗)

**Independent Test**: Add task, mark complete, verify status changes to ✓, mark incomplete, verify status changes to ✗

### Tests for User Story 3 (TDD - Write FIRST, ensure FAIL)

- [ ] T056 [P] [US3] Write failing test for toggle_task_status() success in tests/test_services.py
- [ ] T057 [P] [US3] Write failing test for toggle_task_status() on invalid index in tests/test_services.py
- [ ] T058 [P] [US3] Write failing test for toggle changes incomplete to complete in tests/test_services.py
- [ ] T059 [P] [US3] Write failing test for toggle changes complete to incomplete in tests/test_services.py
- [ ] T060 [P] [US3] Write failing test for user_id_to_index() conversion in tests/test_services.py
- [ ] T061 [P] [US3] Write failing test for index_to_user_id() conversion in tests/test_services.py

### Implementation for User Story 3

- [ ] T062 [US3] Implement user_id_to_index(user_id: int) helper function in src/services.py
- [ ] T063 [US3] Implement index_to_user_id(index: int) helper function in src/services.py
- [ ] T064 [US3] Implement toggle_task_status(task_index: int) function in src/services.py returning tuple[bool, str, Optional[Task]]
- [ ] T065 [US3] Validate task_index bounds in toggle_task_status() in src/services.py
- [ ] T066 [US3] Call task.toggle_status() on valid task in toggle_task_status() in src/services.py
- [ ] T067 [US3] Return success tuple with updated task in toggle_task_status() in src/services.py
- [ ] T068 [US3] Run pytest tests/test_services.py::test_toggle* and verify all tests pass
- [ ] T069 [US3] Implement handle_toggle_status() function in src/cli.py
- [ ] T070 [US3] Display tasks with current status in handle_toggle_status() in src/cli.py
- [ ] T071 [US3] Prompt user for task number to toggle in handle_toggle_status() in src/cli.py
- [ ] T072 [US3] Convert user ID to index and call services.toggle_task_status() in handle_toggle_status() in src/cli.py
- [ ] T073 [US3] Display success or error message in handle_toggle_status() in src/cli.py
- [ ] T074 [US3] Handle empty task list appropriately in handle_toggle_status() in src/cli.py
- [ ] T075 [US3] Add menu option "5. Mark Complete/Incomplete" to display_menu() in src/cli.py
- [ ] T076 [US3] Route choice "5" to handle_toggle_status() in route_choice() in src/cli.py

**Checkpoint**: User Stories 1, 2, AND 3 complete - core todo functionality working

---

## Phase 6: User Story 4 - Update Task Details (Priority: P3)

**Goal**: Users can modify task title and/or description

**Independent Test**: Add task, select "Update Task", modify title and description, verify changes persist

### Tests for User Story 4 (TDD - Write FIRST, ensure FAIL)

- [ ] T077 [P] [US4] Write failing test for update_task() success updating title only in tests/test_services.py
- [ ] T078 [P] [US4] Write failing test for update_task() success updating description only in tests/test_services.py
- [ ] T079 [P] [US4] Write failing test for update_task() success updating both in tests/test_services.py
- [ ] T080 [P] [US4] Write failing test for update_task() error on invalid index in tests/test_services.py
- [ ] T081 [P] [US4] Write failing test for update_task() error on empty new title in tests/test_services.py

### Implementation for User Story 4

- [ ] T082 [US4] Implement update_task(task_index, new_title, new_description) function in src/services.py returning tuple[bool, str, Optional[Task]]
- [ ] T083 [US4] Validate task_index bounds in update_task() in src/services.py
- [ ] T084 [US4] Update task.title if new_title provided and non-empty in update_task() in src/services.py
- [ ] T085 [US4] Update task.description if new_description provided in update_task() in src/services.py
- [ ] T086 [US4] Return success tuple with updated task in update_task() in src/services.py
- [ ] T087 [US4] Run pytest tests/test_services.py::test_update* and verify all tests pass
- [ ] T088 [US4] Implement handle_update_task() function in src/cli.py
- [ ] T089 [US4] Display tasks with current details in handle_update_task() in src/cli.py
- [ ] T090 [US4] Prompt user for task number to update in handle_update_task() in src/cli.py
- [ ] T091 [US4] Display current title and prompt for new title (or Enter to keep) in handle_update_task() in src/cli.py
- [ ] T092 [US4] Display current description and prompt for new description (or Enter to keep) in handle_update_task() in src/cli.py
- [ ] T093 [US4] Convert user ID to index and call services.update_task() in handle_update_task() in src/cli.py
- [ ] T094 [US4] Display success or error message in handle_update_task() in src/cli.py
- [ ] T095 [US4] Handle empty task list appropriately in handle_update_task() in src/cli.py
- [ ] T096 [US4] Add menu option "3. Update Task" to display_menu() in src/cli.py
- [ ] T097 [US4] Route choice "3" to handle_update_task() in route_choice() in src/cli.py

**Checkpoint**: User Stories 1-4 complete - full CRUD operations except delete

---

## Phase 7: User Story 5 - Delete Task (Priority: P3)

**Goal**: Users can delete tasks with confirmation to prevent accidents

**Independent Test**: Add task, select "Delete Task", confirm deletion, verify task removed from list

### Tests for User Story 5 (TDD - Write FIRST, ensure FAIL)

- [ ] T098 [P] [US5] Write failing test for delete_task() success in tests/test_services.py
- [ ] T099 [P] [US5] Write failing test for delete_task() error on invalid index in tests/test_services.py
- [ ] T100 [P] [US5] Write failing test for delete_task() removes task from list in tests/test_services.py
- [ ] T101 [P] [US5] Write failing test for delete_task() returns deleted task in tests/test_services.py

### Implementation for User Story 5

- [ ] T102 [US5] Implement delete_task(task_index: int) function in src/services.py returning tuple[bool, str, Optional[Task]]
- [ ] T103 [US5] Validate task_index bounds in delete_task() in src/services.py
- [ ] T104 [US5] Remove task using _tasks.pop(task_index) in delete_task() in src/services.py
- [ ] T105 [US5] Return success tuple with deleted task for confirmation in delete_task() in src/services.py
- [ ] T106 [US5] Run pytest tests/test_services.py::test_delete* and verify all tests pass
- [ ] T107 [US5] Implement handle_delete_task() function in src/cli.py
- [ ] T108 [US5] Display tasks for selection in handle_delete_task() in src/cli.py
- [ ] T109 [US5] Prompt user for task number to delete in handle_delete_task() in src/cli.py
- [ ] T110 [US5] Prompt for confirmation "Are you sure? (y/n)" in handle_delete_task() in src/cli.py
- [ ] T111 [US5] If confirmed, convert user ID to index and call services.delete_task() in handle_delete_task() in src/cli.py
- [ ] T112 [US5] If cancelled, display cancellation message in handle_delete_task() in src/cli.py
- [ ] T113 [US5] Display success or error message in handle_delete_task() in src/cli.py
- [ ] T114 [US5] Handle empty task list appropriately in handle_delete_task() in src/cli.py
- [ ] T115 [US5] Add menu option "4. Delete Task" to display_menu() in src/cli.py
- [ ] T116 [US5] Route choice "4" to handle_delete_task() in route_choice() in src/cli.py

**Checkpoint**: All 5 user stories complete - full todo application functionality

---

## Phase 8: Main Entry Point & Menu System

**Purpose**: Application bootstrap, UTF-8 configuration, main loop

- [X] T117 [P] Write failing test for configure_utf8() in tests/test_cli.py (mock sys.stdout)
- [X] T118 [P] Write failing test for display_menu() format in tests/test_cli.py
- [X] T119 [P] Write failing test for get_choice() validation in tests/test_cli.py
- [X] T120 [P] Write failing test for route_choice() with valid choices in tests/test_cli.py
- [X] T121 [P] Write failing test for route_choice() returns False on choice "6" (exit) in tests/test_cli.py
- [X] T122 Implement configure_utf8() function in main.py using sys.stdout.reconfigure(encoding='utf-8')
- [X] T123 Implement display_menu() function in src/cli.py showing all 6 options
- [X] T124 Implement get_choice() function in src/cli.py with input validation
- [X] T125 Complete route_choice(choice: str) function in src/cli.py routing to all handlers
- [X] T126 Add exit option handling (return False to break loop) in route_choice() in src/cli.py
- [X] T127 Implement main() function in main.py with infinite loop
- [X] T128 Call configure_utf8() at start of main() in main.py
- [X] T129 Print welcome banner in main() in main.py
- [X] T130 Call display_menu() and get_choice() in main loop in main.py
- [X] T131 Call route_choice() and break on False return in main() in main.py
- [X] T132 Print goodbye message after loop exits in main() in main.py
- [X] T133 Add if __name__ == "__main__": main() guard in main.py
- [X] T134 Run pytest tests/test_cli.py and verify all CLI tests pass

**Checkpoint**: Complete application ready - can run python main.py and use all features

---

## Phase 9: Integration Testing & Validation

**Purpose**: End-to-end testing and specification validation

- [ ] T135 Create sample_tasks fixture in tests/conftest.py providing 3 test tasks
- [ ] T136 Create empty_task_list fixture in tests/conftest.py resetting _tasks to []
- [ ] T137 [P] Write integration test for add task workflow in tests/test_cli.py
- [ ] T138 [P] Write integration test for view tasks workflow in tests/test_cli.py
- [ ] T139 [P] Write integration test for toggle status workflow in tests/test_cli.py
- [ ] T140 [P] Write integration test for update task workflow in tests/test_cli.py
- [ ] T141 [P] Write integration test for delete task workflow with confirmation in tests/test_cli.py
- [ ] T142 [P] Write integration test for delete task workflow with cancellation in tests/test_cli.py
- [ ] T143 [P] Write edge case test for UTF-8 characters (emojis, international) in tests/test_services.py
- [ ] T144 [P] Write edge case test for very long title (1000+ chars) in tests/test_services.py
- [ ] T145 [P] Write edge case test for very long description in tests/test_services.py
- [ ] T146 Run pytest with coverage: pytest --cov=src --cov-report=html
- [ ] T147 Verify 100% coverage for src/models.py
- [ ] T148 Verify 100% coverage for src/services.py
- [ ] T149 Verify 90%+ coverage for src/cli.py
- [ ] T150 Manual test: Launch app and verify UTF-8 display on Windows Terminal
- [ ] T151 Manual test: Add task with emoji in title and verify display
- [ ] T152 Manual test: Verify all 6 menu options work correctly
- [ ] T153 Manual test: Add 100 tasks and verify performance <1s for view operation
- [ ] T154 Manual test: Verify startup time <2s
- [ ] T155 Validate all acceptance scenarios from spec.md work correctly

**Checkpoint**: Full application tested and validated against specification

---

## Phase 10: Polish & Documentation

**Purpose**: Final improvements and documentation

- [ ] T156 [P] Run mypy type checker on all source files: mypy main.py src/
- [ ] T157 [P] Fix any type errors found by mypy
- [ ] T158 [P] Add docstrings to all functions in src/models.py
- [ ] T159 [P] Add docstrings to all functions in src/services.py
- [ ] T160 [P] Add docstrings to all functions in src/cli.py
- [ ] T161 [P] Add docstrings to functions in main.py
- [ ] T162 Review error messages for clarity and actionability
- [ ] T163 Verify all error messages use prefix format (Error:, Success:, Info:)
- [ ] T164 Test quickstart.md instructions and verify accuracy
- [ ] T165 Create README.md with project overview, setup, and usage
- [ ] T166 Add requirements.txt with pytest (only external dependency)
- [ ] T167 Final code review for constitution compliance (type hints, UTF-8, etc.)
- [ ] T168 Create .gitignore with __pycache__/, *.pyc, .pytest_cache/, .coverage, htmlcov/

**Checkpoint**: Application polished, documented, and ready for commit

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) - BLOCKS all user stories
- **User Stories (Phases 3-7)**: All depend on Foundational (Phase 2) completion
  - US1 (Phase 3): Can start after Phase 2
  - US2 (Phase 4): Can start after Phase 2 (independent of US1)
  - US3 (Phase 5): Can start after Phase 2 (independent of US1/US2)
  - US4 (Phase 6): Can start after Phase 2 (independent of US1/US2/US3)
  - US5 (Phase 7): Can start after Phase 2 (independent of US1/US2/US3/US4)
- **Main Entry (Phase 8)**: Depends on at least US1 and US2 for MVP (can proceed without US3-US5)
- **Integration Testing (Phase 9)**: Depends on Phase 8 (complete application)
- **Polish (Phase 10)**: Depends on Phase 9 (all functionality working)

### User Story Dependencies

**Independent Stories** - Can be worked on in parallel after Phase 2:
- ✅ **User Story 1 (Add Task)**: No dependencies on other stories
- ✅ **User Story 2 (View Tasks)**: No dependencies on other stories
- ✅ **User Story 3 (Toggle Status)**: No dependencies on other stories
- ✅ **User Story 4 (Update Task)**: No dependencies on other stories
- ✅ **User Story 5 (Delete Task)**: No dependencies on other stories

**MVP Definition**: Phase 1 + Phase 2 + Phase 3 (US1) + Phase 4 (US2) + Phase 8 (minimal routing)

### Within Each Phase

**TDD Workflow** (for Phases with tests):
1. Write ALL tests for the phase FIRST (marked [P] - can be parallel)
2. Run pytest and verify tests FAIL
3. Implement functionality
4. Run pytest and verify tests PASS
5. Refactor if needed while keeping tests green

**Implementation Order** (within each user story phase):
1. Tests (write first, ensure failure)
2. Services layer (business logic)
3. CLI layer (user interaction)
4. Routing (menu integration)
5. Validate phase checkpoint

### Parallel Opportunities

**Phase 1 (Setup)**: T001-T007 all marked [P] - can create all files in parallel

**Phase 2 (Foundational)**: T008-T015 (tests) all marked [P] - can write all model tests in parallel

**Phase 3 (US1)**: T022-T026 (tests) all marked [P] - can write all service tests for US1 in parallel

**Phase 4 (US2)**: T039-T042 (tests) all marked [P] - can write all service tests for US2 in parallel

**Phase 5 (US3)**: T056-T061 (tests) all marked [P] - can write all service tests for US3 in parallel

**Phase 6 (US4)**: T077-T081 (tests) all marked [P] - can write all service tests for US4 in parallel

**Phase 7 (US5)**: T098-T101 (tests) all marked [P] - can write all service tests for US5 in parallel

**Phase 8 (Main)**: T117-T121 (tests) all marked [P] - can write all CLI tests in parallel

**Phase 9 (Integration)**: T137-T145 (tests) all marked [P] - can write all integration/edge case tests in parallel

**Phase 10 (Polish)**: T156-T161 (type checking, docstrings) all marked [P] - can do in parallel

**Cross-Phase Parallelism** (with multiple developers):
- After Phase 2 completes, Phases 3-7 (all user stories) can proceed in parallel
- Different team members can own different user stories
- Each story is independently testable

---

## Parallel Example: User Story 1

```bash
# Step 1: Write all tests for US1 in parallel
Task: "Write failing test for add_task() success with title only in tests/test_services.py"
Task: "Write failing test for add_task() success with title and description in tests/test_services.py"
Task: "Write failing test for add_task() error on empty title in tests/test_services.py"
Task: "Write failing test for add_task() error on whitespace-only title in tests/test_services.py"
Task: "Write failing test for add_task() with UTF-8 characters in tests/test_services.py"

# Step 2: Run pytest and verify all fail

# Step 3: Implement services layer sequentially (T027-T032)

# Step 4: Implement CLI layer sequentially (T033-T038)

# Step 5: Verify tests pass
```

---

## Parallel Example: After Phase 2 (Multiple Developers)

```bash
# Once Foundational phase completes, all user stories can start:

Developer A:
  - Phase 3 (US1): T022-T038 (Add Task feature)

Developer B:
  - Phase 4 (US2): T039-T055 (View Tasks feature)

Developer C:
  - Phase 5 (US3): T056-T076 (Toggle Status feature)

Developer D:
  - Phase 6 (US4): T077-T097 (Update Task feature)

Developer E:
  - Phase 7 (US5): T098-T116 (Delete Task feature)

# All stories independently testable and can integrate without conflicts
```

---

## Implementation Strategy

### MVP First (Phases 1, 2, 3, 4, 8 - Minimal)

Delivers basic todo app:

1. **Complete Phase 1**: Setup (T001-T007)
2. **Complete Phase 2**: Foundational - Task model (T008-T021)
3. **Complete Phase 3**: User Story 1 - Add Task (T022-T038)
4. **Complete Phase 4**: User Story 2 - View Tasks (T039-T055)
5. **Complete Phase 8**: Main entry point (T117-T134) - minimal routing for US1/US2 only
6. **STOP and VALIDATE**: Test MVP independently
7. **Deploy/Demo**: Users can add and view tasks

**MVP Scope**: ~55 tasks
**MVP Value**: Basic todo list functionality

### Incremental Delivery (Add features progressively)

1. **Foundation**: Phases 1 + 2 → Task model ready
2. **MVP**: Add Phases 3 + 4 + 8 (minimal) → Add and view tasks (deployable!)
3. **v1.1**: Add Phase 5 → Toggle task status (deployable!)
4. **v1.2**: Add Phase 6 → Update task details (deployable!)
5. **v1.3**: Add Phase 7 → Delete tasks with confirmation (deployable!)
6. **v1.4**: Add Phase 9 → Full integration testing
7. **v2.0**: Add Phase 10 → Polished, documented release

Each increment is independently testable and adds value.

### Parallel Team Strategy (Maximum speed)

With 5 developers:

1. **All together**: Phases 1 + 2 (Setup + Foundation)
2. **Split by user story** (after Phase 2 complete):
   - Dev 1: Phase 3 (US1 - Add Task)
   - Dev 2: Phase 4 (US2 - View Tasks)
   - Dev 3: Phase 5 (US3 - Toggle Status)
   - Dev 4: Phase 6 (US4 - Update Task)
   - Dev 5: Phase 7 (US5 - Delete Task)
3. **Merge**: Integrate all stories (minimal conflicts - different handlers)
4. **Together**: Phase 8 (Main entry - wire all handlers)
5. **All**: Phase 9 + 10 (Integration testing + Polish)

**Timeline**: ~1-2 days with 5 devs working in parallel

---

## Task Summary

**Total Tasks**: 168

**By Phase**:
- Phase 1 (Setup): 7 tasks
- Phase 2 (Foundational): 14 tasks (Task model + tests)
- Phase 3 (US1 - Add Task): 17 tasks (5 tests + 12 implementation)
- Phase 4 (US2 - View Tasks): 17 tasks (4 tests + 13 implementation)
- Phase 5 (US3 - Toggle Status): 21 tasks (6 tests + 15 implementation)
- Phase 6 (US4 - Update Task): 21 tasks (5 tests + 16 implementation)
- Phase 7 (US5 - Delete Task): 19 tasks (4 tests + 15 implementation)
- Phase 8 (Main Entry): 18 tasks (5 tests + 13 implementation)
- Phase 9 (Integration): 21 tasks (all testing/validation)
- Phase 10 (Polish): 13 tasks (documentation + quality)

**By Type**:
- Test tasks: ~60 (36%)
- Implementation tasks: ~95 (57%)
- Validation/Documentation tasks: ~13 (7%)

**Parallelizable Tasks**: ~45 tasks marked [P] (27%)

**MVP Minimum** (Phases 1, 2, 3, 4, 8-minimal): ~55 tasks

**Independent Stories**: All 5 user stories can be worked on in parallel after Phase 2

---

## Notes

- **[P] marker**: Tasks that can run in parallel (different files, no dependencies)
- **[Story] label**: Maps task to user story for traceability (US1-US5)
- **TDD Approach**: Write tests FIRST, ensure FAIL, then implement, ensure PASS
- **Checkpoints**: After each phase, validate that phase's goal independently
- **Type Hints**: All functions must include full type hints (constitution requirement)
- **UTF-8**: Configure at startup, test with emojis and international characters
- **Tuple Returns**: Services use (bool, str, Optional[T]) pattern for explicit error handling
- **Independent Stories**: Each user story delivers value on its own
- **Commit Strategy**: Commit after each task or logical group of related tasks
- **Stop Points**: Can stop at any checkpoint to have a working subset of features

---

## Validation Checklist

After completing all tasks, verify:

- [ ] All 168 tasks completed and checked off
- [ ] pytest coverage: models.py (100%), services.py (100%), cli.py (90%+)
- [ ] mypy type checking passes with zero errors
- [ ] All acceptance scenarios from spec.md pass
- [ ] All edge cases from spec.md handled
- [ ] All 10 success criteria from spec.md met
- [ ] UTF-8 characters display correctly on Windows Terminal
- [ ] Application startup <2s
- [ ] View operation <1s for 100 tasks
- [ ] All error messages use prefix format (Error:, Success:, Info:)
- [ ] Constitution compliance: Python 3.12+, in-memory only, type hints, UTF-8, no external deps except pytest
- [ ] quickstart.md instructions work correctly
- [ ] All 5 user stories independently testable
- [ ] README.md complete with setup and usage

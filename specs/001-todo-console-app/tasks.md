---
description: "Task list for Todo In-Memory Python Console Application"
---

# Tasks: Todo In-Memory Python Console Application

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan in src/
- [x] T002 Initialize Python project with proper directory structure
- [x] T003 [P] Create src/main.py as main application entry point
- [x] T004 [P] Create src/models/, src/services/, and src/cli/ directories

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create Task data model in src/models/task.py
- [x] T006 [P] Create TaskManager service in src/services/task_manager.py
- [x] T007 [P] Create Menu interface in src/cli/menu.py
- [x] T008 Implement basic application loop in src/main.py
- [x] T009 Create basic tests directory structure in tests/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: User can add a new task via console input with title, optional description, unique ID, and default incomplete status

**Independent Test**: User can launch the application, enter the add task command, provide a title, and see the task successfully added with a unique ID and incomplete status

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T010 [P] [US1] Unit test for Task model validation in tests/unit/test_task.py
- [x] T011 [P] [US1] Unit test for TaskManager add_task functionality in tests/unit/test_task_manager.py
- [x] T012 [P] [US1] Integration test for add task CLI flow in tests/integration/test_cli.py

### Implementation for User Story 1

- [x] T013 [US1] Implement Task model with validation in src/models/task.py
- [x] T014 [US1] Implement add_task method in TaskManager service in src/services/task_manager.py
- [x] T015 [US1] Implement add task CLI command in src/cli/menu.py
- [x] T016 [US1] Integrate add task functionality with main application in src/main.py
- [x] T017 [US1] Add input validation for add task in src/cli/menu.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Task List (Priority: P2)

**Goal**: User can view all tasks with ID, title, description, and completion status in a clear, organized format

**Independent Test**: User can launch the application, enter the view tasks command, and see a formatted list of all their tasks with complete information

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [x] T018 [P] [US2] Unit test for TaskManager get_all_tasks functionality in tests/unit/test_task_manager.py
- [x] T019 [P] [US2] Integration test for view tasks CLI flow in tests/integration/test_cli.py

### Implementation for User Story 2

- [x] T020 [US2] Implement get_all_tasks method in TaskManager service in src/services/task_manager.py
- [x] T021 [US2] Implement view tasks CLI command in src/cli/menu.py
- [x] T022 [US2] Integrate view tasks functionality with main application in src/main.py
- [x] T023 [US2] Add formatted display for task list in src/cli/menu.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task (Priority: P3)

**Goal**: User can modify the title or description of an existing task by ID while preserving completion status

**Independent Test**: User can launch the application, enter the update task command with a valid ID and new information, and see the task updated while keeping its completion status unchanged

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [x] T024 [P] [US3] Unit test for TaskManager update_task functionality in tests/unit/test_task_manager.py
- [x] T025 [P] [US3] Integration test for update task CLI flow in tests/integration/test_cli.py

### Implementation for User Story 3

- [x] T026 [US3] Implement update_task method in TaskManager service in src/services/task_manager.py
- [x] T027 [US3] Implement update task CLI command in src/cli/menu.py
- [x] T028 [US3] Integrate update task functionality with main application in src/main.py
- [x] T029 [US3] Add input validation for update task in src/cli/menu.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Delete Task (Priority: P4)

**Goal**: User can remove a task from memory by providing its ID, with permanent removal

**Independent Test**: User can launch the application, enter the delete task command with a valid ID, and see the task removed from memory

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [x] T030 [P] [US4] Unit test for TaskManager delete_task functionality in tests/unit/test_task_manager.py
- [x] T031 [P] [US4] Integration test for delete task CLI flow in tests/integration/test_cli.py

### Implementation for User Story 4

- [x] T032 [US4] Implement delete_task method in TaskManager service in src/services/task_manager.py
- [x] T033 [US4] Implement delete task CLI command in src/cli/menu.py
- [x] T034 [US4] Integrate delete task functionality with main application in src/main.py
- [x] T035 [US4] Add confirmation and validation for delete task in src/cli/menu.py

---

## Phase 7: User Story 5 - Mark Task Complete/Incomplete (Priority: P5)

**Goal**: User can toggle the completion status of a task by providing its ID

**Independent Test**: User can launch the application, enter the toggle completion command with a valid ID, and see the task's status updated

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [x] T036 [P] [US5] Unit test for TaskManager toggle_completion functionality in tests/unit/test_task_manager.py
- [x] T037 [P] [US5] Integration test for toggle completion CLI flow in tests/integration/test_cli.py

### Implementation for User Story 5

- [x] T038 [US5] Implement toggle_completion method in TaskManager service in src/services/task_manager.py
- [x] T039 [US5] Implement mark task complete/incomplete CLI command in src/cli/menu.py
- [x] T040 [US5] Integrate toggle completion functionality with main application in src/main.py
- [x] T041 [US5] Add input validation for toggle completion in src/cli/menu.py

---

## Phase 8: Console UI & Input Validation

**Goal**: Create a user-friendly console interface with proper input validation and error handling

- [x] T042 Implement main menu interface in src/cli/menu.py
- [x] T043 [P] Add error handling for invalid task IDs in src/services/task_manager.py
- [x] T044 [P] Add error handling for invalid input in src/cli/menu.py
- [x] T045 Implement graceful handling of invalid inputs in src/main.py
- [x] T046 Add user prompts and console formatting in src/cli/menu.py

---

## Phase 9: Final Testing

**Goal**: Comprehensive testing of all functionality to ensure quality

- [x] T047 Run all unit tests and ensure they pass
- [x] T048 Run all integration tests and ensure they pass
- [x] T049 Test complete workflow following quickstart.md examples
- [x] T050 Validate all edge cases from spec.md are handled properly
- [x] T051 Verify application handles invalid inputs gracefully without crashing

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T052 [P] Add docstrings to all classes and methods in src/
- [x] T053 Code cleanup and refactoring across all modules
- [x] T054 [P] Additional unit tests for edge cases in tests/unit/
- [x] T055 Run quickstart.md validation to ensure all examples work

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Console UI & Input Validation (Phase 8)**: Can run in parallel with user stories
- **Final Testing (Phase 9)**: Depends on all user stories being complete
- **Polish (Phase 10)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints/cli
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Unit test for Task model validation in tests/unit/test_task.py"
Task: "Unit test for TaskManager add_task functionality in tests/unit/test_task_manager.py"
Task: "Integration test for add task CLI flow in tests/integration/test_cli.py"

# Launch all models for User Story 1 together:
Task: "Implement Task model with validation in src/models/task.py"
Task: "Implement add_task method in TaskManager service in src/services/task_manager.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
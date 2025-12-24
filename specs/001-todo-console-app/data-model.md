# Data Model: Todo In-Memory Python Console Application

## Task Entity

**Definition**: The core entity representing a user's to-do item

**Attributes**:
- `id`: str - Unique identifier automatically generated for each task
- `title`: str - Required text content of the task
- `description`: str - Optional additional details about the task (default: "")
- `completed`: bool - Completion status (default: False)

**State Transitions**:
- Incomplete → Complete: When user marks task as complete
- Complete → Incomplete: When user marks task as incomplete

**Validation Rules**:
- ID must be unique within the application session
- Title must not be empty or contain only whitespace
- Description can be empty but not None
- Completed status must be a boolean value

## Task Manager Service

**Purpose**: Manages the collection of tasks in memory

**Attributes**:
- `tasks`: dict - Dictionary mapping task IDs to Task objects
- `next_id`: int - Counter for generating unique IDs

**Operations**:
- Add task: Validates and adds a new task to the collection
- Get all tasks: Returns all tasks in the collection
- Get task by ID: Returns a specific task or None if not found
- Update task: Modifies title and/or description of a task
- Delete task: Removes a task from the collection
- Toggle completion: Changes the completion status of a task

**Validation Rules**:
- Task IDs must exist before update/delete/toggle operations
- Title must be provided and not empty when adding a task
- Update operations must preserve task completion status unless specifically toggled
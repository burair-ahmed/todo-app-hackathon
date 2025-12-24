# Quickstart Guide: Todo In-Memory Python Console Application

## Getting Started

1. Ensure you have Python 3.13+ installed on your system
2. Navigate to the project directory
3. Run the application with: `python src/main.py`

## Basic Usage

When the application starts, you'll see a menu with the following options:

1. **Add Task**: Creates a new task with a unique ID
   - Prompts for: Task title, optional description
   - Task is created with "incomplete" status by default

2. **View Tasks**: Displays all tasks in a formatted list
   - Shows: ID, Title, Description, Status (Complete/Incomplete)

3. **Update Task**: Modifies an existing task
   - Prompts for: Task ID, new title (optional), new description (optional)
   - Completion status remains unchanged

4. **Delete Task**: Removes a task from memory
   - Prompts for: Task ID
   - Task is permanently removed

5. **Mark Task Complete/Incomplete**: Toggles the completion status
   - Prompts for: Task ID
   - Changes status from Complete ↔ Incomplete

6. **Exit**: Closes the application

## Example Workflow

1. Select "Add Task" → Enter "Buy groceries" as title → Task added with ID 1
2. Select "View Tasks" → See task "Buy groceries" with ID 1, status "Incomplete"
3. Select "Mark Task Complete" → Enter ID 1 → Status changes to "Complete"
4. Select "Update Task" → Enter ID 1 → Change title to "Bought groceries"
5. Select "View Tasks" → See updated task with new title, status "Complete"

## Error Handling

- Invalid task IDs will show an error message
- Empty titles will be rejected when adding tasks
- The application will not crash on invalid input; it will show helpful error messages

## Development

To run the tests:
```bash
python -m pytest tests/
```

The application is entirely in-memory, so all data is lost when the application exits.
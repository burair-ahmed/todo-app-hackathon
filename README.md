# Todo Console Application

A simple in-memory Python console application for managing todo tasks.

## Features

- Add new tasks with titles and optional descriptions
- View all tasks with their completion status
- Update task titles and descriptions
- Delete tasks by ID
- Mark tasks as complete/incomplete
- Console-based user interface

## Requirements

- Python 3.13 or higher

## Installation

1. Clone or download the repository
2. Navigate to the project directory
3. The application is ready to run (no external dependencies required)

## Usage

Run the application from the project root directory:

```bash
python src/main.py
```

The application will present a menu with the following options:
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Follow the on-screen prompts to manage your tasks.

## Project Structure

```
src/
├── main.py              # Main application entry point
├── models/
│   └── task.py          # Task data model
├── services/
│   └── task_manager.py  # Task operations logic
└── cli/
    └── menu.py          # Console interface and menu system
tests/
├── unit/
│   ├── test_task.py     # Task model tests
│   └── test_task_manager.py # Task service tests
└── integration/
    └── test_cli.py      # CLI integration tests
```

## Testing

To run all unit tests:
```bash
python -m unittest discover -s tests/unit -p "test_*.py"
```

To run all integration tests:
```bash
python -m unittest discover -s tests/integration -p "test_*.py"
```

To run all tests:
```bash
python -m unittest discover -s tests/ -p "test_*.py"
```

## Architecture

The application follows a modular architecture with clear separation of concerns:

- **Models**: Define the data structures (Task model)
- **Services**: Handle business logic (TaskManager service)
- **CLI**: Handle user interface and console interactions (Menu class)
- **Main**: Entry point that orchestrates the application

## Data Model

The `Task` model has the following attributes:
- `id`: Unique identifier for the task
- `title`: Required title of the task
- `description`: Optional description of the task
- `completed`: Boolean indicating completion status

## License

This project is open source and available under the MIT License.
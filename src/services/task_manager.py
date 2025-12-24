"""
Task Manager Service

This module provides the core business logic for managing tasks in the Todo Console Application.
"""

from typing import Dict, List, Optional
from ..models.task import Task


class TaskManager:
    """
    Manages the collection of tasks in memory.

    This service provides methods for adding, retrieving, updating, and deleting tasks.
    All tasks are stored in memory only, with no persistence.
    """

    def __init__(self):
        """Initialize the task manager with an empty task collection."""
        self.tasks: Dict[str, Task] = {}
        self.next_id = 1

    def generate_id(self) -> str:
        """
        Generate a unique ID for a new task.

        Returns:
            str: A unique task ID that is not currently in use
        """
        while str(self.next_id) in self.tasks:
            self.next_id += 1
        task_id = str(self.next_id)
        self.next_id += 1
        return task_id

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task to the collection.

        Args:
            title (str): The title of the task (required)
            description (str): The description of the task (optional)

        Returns:
            Task: The newly created task

        Raises:
            ValueError: If the title is empty or contains only whitespace
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty or contain only whitespace")

        task_id = self.generate_id()
        task = Task(id=task_id, title=title.strip(), description=description.strip())
        self.tasks[task_id] = task
        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks in the collection.

        Returns:
            List[Task]: A list of all tasks, sorted by ID
        """
        return sorted(self.tasks.values(), key=lambda x: int(x.id))

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        Get a specific task by its ID.

        Args:
            task_id (str): The ID of the task to retrieve

        Returns:
            Task or None: The task if found, None otherwise
        """
        return self.tasks.get(task_id)

    def validate_task_id(self, task_id: str) -> bool:
        """
        Validate if a task ID exists in the collection.

        Args:
            task_id (str): The ID to validate

        Returns:
            bool: True if the task ID exists, False otherwise
        """
        return task_id in self.tasks

    def update_task(self, task_id: str, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update an existing task's title and/or description.

        Args:
            task_id (str): The ID of the task to update
            title (str, optional): New title for the task
            description (str, optional): New description for the task

        Returns:
            bool: True if the task was updated, False if the task was not found

        Raises:
            ValueError: If the new title is empty or contains only whitespace
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        # Only update fields that are provided
        if title is not None:
            if not title or not title.strip():
                raise ValueError("Task title cannot be empty or contain only whitespace")
            task.title = title.strip()

        if description is not None:
            task.description = description.strip()

        return True

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task from the collection.

        Args:
            task_id (str): The ID of the task to delete

        Returns:
            bool: True if the task was deleted, False if the task was not found
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def toggle_completion(self, task_id: str) -> bool:
        """
        Toggle the completion status of a task.

        Args:
            task_id (str): The ID of the task to toggle

        Returns:
            bool: True if the task status was toggled, False if the task was not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.toggle_completion()
            return True
        return False

    def get_task_count(self) -> int:
        """
        Get the total number of tasks.

        Returns:
            int: The number of tasks in the collection
        """
        return len(self.tasks)
"""
Task Model

This module defines the Task data model for the Todo Console Application.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """
    Represents a single task in the todo list.

    Attributes:
        id (str): Unique identifier for the task
        title (str): Required title of the task
        description (str): Optional description of the task
        completed (bool): Completion status of the task (default: False)
    """

    id: str
    title: str
    description: str = ""
    completed: bool = False

    def __post_init__(self):
        """
        Validate the task after initialization.

        Raises:
            ValueError: If the title is empty or contains only whitespace
        """
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty or contain only whitespace")
        if self.description is None:
            self.description = ""

    def mark_complete(self):
        """Mark the task as complete."""
        self.completed = True

    def mark_incomplete(self):
        """Mark the task as incomplete."""
        self.completed = False

    def toggle_completion(self):
        """Toggle the completion status of the task."""
        self.completed = not self.completed

    def __str__(self):
        """
        String representation of the task.

        Returns:
            str: Formatted string representation of the task
        """
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.id}: {self.title} - {self.description}"
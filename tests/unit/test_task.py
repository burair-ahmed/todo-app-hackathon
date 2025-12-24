"""
Unit tests for the Task model.
"""
import unittest
import sys
import os
# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.task import Task


class TestTask(unittest.TestCase):
    """
    Unit tests for the Task model.
    """

    def test_task_creation_with_required_fields(self):
        """Test creating a task with required fields."""
        task = Task(id="1", title="Test Task")
        self.assertEqual(task.id, "1")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "")
        self.assertEqual(task.completed, False)

    def test_task_creation_with_all_fields(self):
        """Test creating a task with all fields."""
        task = Task(id="1", title="Test Task", description="Test Description", completed=True)
        self.assertEqual(task.id, "1")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.completed, True)

    def test_task_creation_with_empty_title_raises_error(self):
        """Test that creating a task with an empty title raises an error."""
        with self.assertRaises(ValueError):
            Task(id="1", title="")

    def test_task_creation_with_whitespace_only_title_raises_error(self):
        """Test that creating a task with whitespace-only title raises an error."""
        with self.assertRaises(ValueError):
            Task(id="1", title="   ")

    def test_task_mark_complete(self):
        """Test marking a task as complete."""
        task = Task(id="1", title="Test Task")
        task.mark_complete()
        self.assertTrue(task.completed)

    def test_task_mark_incomplete(self):
        """Test marking a task as incomplete."""
        task = Task(id="1", title="Test Task", completed=True)
        task.mark_incomplete()
        self.assertFalse(task.completed)

    def test_task_toggle_completion(self):
        """Test toggling task completion status."""
        task = Task(id="1", title="Test Task")
        self.assertFalse(task.completed)
        task.toggle_completion()
        self.assertTrue(task.completed)
        task.toggle_completion()
        self.assertFalse(task.completed)

    def test_task_string_representation(self):
        """Test string representation of a task."""
        task = Task(id="1", title="Test Task", description="Test Description")
        expected = "[○] 1: Test Task - Test Description"
        self.assertEqual(str(task), expected)

        task.mark_complete()
        expected = "[✓] 1: Test Task - Test Description"
        self.assertEqual(str(task), expected)


if __name__ == "__main__":
    unittest.main()
"""
Integration tests for the CLI add task flow.
"""
import unittest
import sys
import os
from io import StringIO
from unittest.mock import patch
# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.services.task_manager import TaskManager


class TestCLIAddTask(unittest.TestCase):
    """
    Integration tests for the CLI add task flow.
    """

    def setUp(self):
        """Set up a fresh TaskManager for each test."""
        self.task_manager = TaskManager()

    @patch('builtins.input')
    def test_add_task_through_cli_flow(self, mock_input):
        """Test the complete add task flow through CLI."""
        # Mock user input for title and description
        mock_input.side_effect = ["Test Task", "Test Description"]

        # Capture printed output
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            # Call the method that handles adding a task
            from src.cli.menu import Menu
            menu = Menu()

            # Temporarily replace the task manager to test our instance
            original_task_manager = menu.task_manager
            menu.task_manager = self.task_manager

            menu.handle_add_task()

            # Restore original task manager
            menu.task_manager = original_task_manager

            # Check that the task was added
            output = captured_output.getvalue()
            self.assertIn("Task added successfully!", output)

            # Verify the task exists in our task manager
            tasks = self.task_manager.get_all_tasks()
            self.assertEqual(len(tasks), 1)
            self.assertEqual(tasks[0].title, "Test Task")
            self.assertEqual(tasks[0].description, "Test Description")
            self.assertFalse(tasks[0].completed)

        finally:
            sys.stdout = sys.__stdout__  # Restore original stdout

    @patch('builtins.input')
    def test_add_task_with_empty_title_shows_error(self, mock_input):
        """Test that adding a task with empty title shows an error."""
        # Mock user input with empty title
        mock_input.side_effect = ["", "Test Description"]

        # Capture printed output
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            from src.cli.menu import Menu
            menu = Menu()
            menu.task_manager = self.task_manager  # Use our test instance

            menu.handle_add_task()

            output = captured_output.getvalue()
            self.assertIn("Error: Task title cannot be empty", output)

            # Verify no task was added
            self.assertEqual(self.task_manager.get_task_count(), 0)

        finally:
            sys.stdout = sys.__stdout__  # Restore original stdout


    def test_view_tasks_with_no_tasks_shows_message(self):
        """Test that viewing tasks shows appropriate message when no tasks exist."""
        # Capture printed output
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            from src.cli.menu import Menu
            menu = Menu()
            menu.task_manager = self.task_manager  # Use our test instance

            menu.handle_view_tasks()

            output = captured_output.getvalue()
            self.assertIn("No tasks found.", output)

        finally:
            sys.stdout = sys.__stdout__  # Restore original stdout

    @patch('builtins.input')
    def test_view_tasks_shows_all_tasks(self, mock_input):
        """Test that viewing tasks shows all tasks with complete information."""
        # Add some tasks to the manager
        task1 = self.task_manager.add_task("Task 1", "Description 1")
        task2 = self.task_manager.add_task("Task 2", "Description 2")
        self.task_manager.toggle_completion(task2.id)  # Mark task 2 as complete

        # Capture printed output
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            from src.cli.menu import Menu
            menu = Menu()
            # Use our test instance with the tasks we added
            menu.task_manager = self.task_manager

            menu.handle_view_tasks()

            output = captured_output.getvalue()
            self.assertIn("Total tasks: 2", output)
            self.assertIn("Task 1", output)
            self.assertIn("Description 1", output)
            self.assertIn("Task 2", output)
            self.assertIn("Description 2", output)
            self.assertIn("Complete", output)  # Task 2 is complete
            self.assertIn("Incomplete", output)  # Task 1 is incomplete

        finally:
            sys.stdout = sys.__stdout__  # Restore original stdout


    @patch('builtins.input')
    def test_update_task_successfully(self, mock_input):
        """Test updating a task successfully through CLI."""
        # Add a task to update
        task = self.task_manager.add_task("Original Title", "Original Description")

        # Mock user input for task ID, new title, and new description
        mock_input.side_effect = [task.id, "New Title", "New Description"]

        # Capture printed output
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            from src.cli.menu import Menu
            menu = Menu()
            menu.task_manager = self.task_manager  # Use our test instance

            menu.handle_update_task()

            output = captured_output.getvalue()
            self.assertIn("[COMPLETED] Task updated successfully!", output)

            # Verify the task was updated
            updated_task = self.task_manager.get_task_by_id(task.id)
            self.assertEqual(updated_task.title, "New Title")
            self.assertEqual(updated_task.description, "New Description")
            # Completion status should remain unchanged
            self.assertFalse(updated_task.completed)

        finally:
            sys.stdout = sys.__stdout__  # Restore original stdout

    @patch('builtins.input')
    def test_update_task_with_invalid_id_shows_error(self, mock_input):
        """Test that updating a task with invalid ID shows an error."""
        # Add a task so the check passes
        self.task_manager.add_task("Test task", "Test description")
        # Mock user input for invalid task ID
        mock_input.side_effect = ["999", "New Title", "New Description"]

        # Capture printed output
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            from src.cli.menu import Menu
            menu = Menu()
            menu.task_manager = self.task_manager  # Use our test instance

            menu.handle_update_task()

            output = captured_output.getvalue()
            self.assertIn("not found", output)

        finally:
            sys.stdout = sys.__stdout__  # Restore original stdout


    @patch('builtins.input')
    def test_delete_task_successfully(self, mock_input):
        """Test deleting a task successfully through CLI."""
        # Add a task to delete
        task = self.task_manager.add_task("Task to Delete", "Description to Delete")

        # Mock user input for task ID and confirmation
        mock_input.side_effect = [task.id, "y"]

        # Capture printed output
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            from src.cli.menu import Menu
            menu = Menu()
            menu.task_manager = self.task_manager  # Use our test instance

            menu.handle_delete_task()

            output = captured_output.getvalue()
            self.assertIn("[COMPLETED] Task deleted successfully!", output)

            # Verify the task was deleted
            deleted_task = self.task_manager.get_task_by_id(task.id)
            self.assertIsNone(deleted_task)

        finally:
            sys.stdout = sys.__stdout__  # Restore original stdout

    @patch('builtins.input')
    def test_delete_task_with_invalid_id_shows_error(self, mock_input):
        """Test that deleting a task with invalid ID shows an error."""
        # Add a task so the check passes
        self.task_manager.add_task("Test task", "Test description")
        # Mock user input for invalid task ID
        mock_input.side_effect = ["999", "y"]

        # Capture printed output
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            from src.cli.menu import Menu
            menu = Menu()
            menu.task_manager = self.task_manager  # Use our test instance

            menu.handle_delete_task()

            output = captured_output.getvalue()
            self.assertIn("not found", output)

        finally:
            sys.stdout = sys.__stdout__  # Restore original stdout

    @patch('builtins.input')
    def test_delete_task_cancelled_by_user(self, mock_input):
        """Test that deleting a task is cancelled when user declines confirmation."""
        # Add a task to delete
        task = self.task_manager.add_task("Task to Delete", "Description to Delete")

        # Mock user input for task ID and cancellation
        mock_input.side_effect = [task.id, "n"]

        # Capture printed output
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            from src.cli.menu import Menu
            menu = Menu()
            menu.task_manager = self.task_manager  # Use our test instance

            menu.handle_delete_task()

            output = captured_output.getvalue()
            self.assertIn("deletion cancelled", output)

            # Verify the task still exists
            existing_task = self.task_manager.get_task_by_id(task.id)
            self.assertIsNotNone(existing_task)

        finally:
            sys.stdout = sys.__stdout__  # Restore original stdout


    @patch('builtins.input')
    def test_toggle_completion_successfully(self, mock_input):
        """Test toggling task completion successfully through CLI."""
        # Add a task to toggle
        task = self.task_manager.add_task("Test Task", "Test Description")
        # Initially incomplete
        self.assertFalse(task.completed)

        # Mock user input for task ID
        mock_input.side_effect = [task.id]

        # Capture printed output
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            from src.cli.menu import Menu
            menu = Menu()
            menu.task_manager = self.task_manager  # Use our test instance

            menu.handle_toggle_completion()

            output = captured_output.getvalue()
            self.assertIn("changed from Incomplete to Complete", output)

            # Verify the task completion was toggled
            updated_task = self.task_manager.get_task_by_id(task.id)
            self.assertTrue(updated_task.completed)

        finally:
            sys.stdout = sys.__stdout__  # Restore original stdout

    @patch('builtins.input')
    def test_toggle_completion_twice_returns_to_original_state(self, mock_input):
        """Test toggling task completion twice returns to original state."""
        # Add a task to toggle
        task = self.task_manager.add_task("Test Task", "Test Description")
        original_status = task.completed  # Should be False

        # Mock user input for task ID - need to provide it twice since method is called twice
        mock_input.side_effect = [task.id, task.id]

        # Capture printed output
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            from src.cli.menu import Menu
            menu = Menu()
            menu.task_manager = self.task_manager  # Use our test instance

            # Toggle completion twice
            menu.handle_toggle_completion()
            menu.handle_toggle_completion()

            output = captured_output.getvalue()
            # Should see both transitions
            self.assertIn("changed from Incomplete to Complete", output)
            self.assertIn("changed from Complete to Incomplete", output)

            # Verify the task completion returned to original state
            updated_task = self.task_manager.get_task_by_id(task.id)
            self.assertEqual(updated_task.completed, original_status)

        finally:
            sys.stdout = sys.__stdout__  # Restore original stdout

    @patch('builtins.input')
    def test_toggle_completion_with_invalid_id_shows_error(self, mock_input):
        """Test that toggling completion with invalid ID shows an error."""
        # Add a task so the check passes
        self.task_manager.add_task("Test task", "Test description")
        # Mock user input for invalid task ID
        mock_input.side_effect = ["999"]

        # Capture printed output
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            from src.cli.menu import Menu
            menu = Menu()
            menu.task_manager = self.task_manager  # Use our test instance

            menu.handle_toggle_completion()

            output = captured_output.getvalue()
            self.assertIn("not found", output)

        finally:
            sys.stdout = sys.__stdout__  # Restore original stdout


if __name__ == "__main__":
    unittest.main()
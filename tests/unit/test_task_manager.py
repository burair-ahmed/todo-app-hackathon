"""
Unit tests for the TaskManager service add_task functionality.
"""
import unittest
import sys
import os
# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.services.task_manager import TaskManager


class TestTaskManagerAddTask(unittest.TestCase):
    """
    Unit tests for the TaskManager service add_task functionality.
    """

    def setUp(self):
        """Set up a fresh TaskManager for each test."""
        self.task_manager = TaskManager()

    def test_add_task_with_title_only(self):
        """Test adding a task with only a title."""
        task = self.task_manager.add_task("Test Task")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "")
        self.assertEqual(task.completed, False)
        self.assertIsNotNone(task.id)
        self.assertEqual(self.task_manager.get_task_count(), 1)

    def test_add_task_with_title_and_description(self):
        """Test adding a task with both title and description."""
        task = self.task_manager.add_task("Test Task", "Test Description")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.completed, False)
        self.assertIsNotNone(task.id)
        self.assertEqual(self.task_manager.get_task_count(), 1)

    def test_add_task_generates_unique_ids(self):
        """Test that adding multiple tasks generates unique IDs."""
        task1 = self.task_manager.add_task("Task 1")
        task2 = self.task_manager.add_task("Task 2")
        self.assertNotEqual(task1.id, task2.id)
        self.assertEqual(self.task_manager.get_task_count(), 2)

    def test_add_task_with_empty_title_raises_error(self):
        """Test that adding a task with an empty title raises an error."""
        with self.assertRaises(ValueError):
            self.task_manager.add_task("")

    def test_add_task_with_whitespace_only_title_raises_error(self):
        """Test that adding a task with whitespace-only title raises an error."""
        with self.assertRaises(ValueError):
            self.task_manager.add_task("   ")

    def test_added_task_is_in_storage(self):
        """Test that an added task can be retrieved by its ID."""
        task = self.task_manager.add_task("Test Task", "Test Description")
        retrieved_task = self.task_manager.get_task_by_id(task.id)
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.title, task.title)
        self.assertEqual(retrieved_task.description, task.description)
        self.assertEqual(retrieved_task.completed, task.completed)
        self.assertEqual(retrieved_task.id, task.id)


    def test_get_all_tasks_returns_empty_list_when_no_tasks(self):
        """Test that get_all_tasks returns an empty list when there are no tasks."""
        tasks = self.task_manager.get_all_tasks()
        self.assertEqual(len(tasks), 0)
        self.assertEqual(tasks, [])

    def test_get_all_tasks_returns_all_added_tasks(self):
        """Test that get_all_tasks returns all added tasks."""
        task1 = self.task_manager.add_task("Task 1")
        task2 = self.task_manager.add_task("Task 2", "Description for task 2")

        tasks = self.task_manager.get_all_tasks()
        self.assertEqual(len(tasks), 2)

        # Check that both tasks are present
        task_titles = [task.title for task in tasks]
        self.assertIn("Task 1", task_titles)
        self.assertIn("Task 2", task_titles)

        # Check that descriptions are preserved
        task2_found = next((task for task in tasks if task.title == "Task 2"), None)
        self.assertIsNotNone(task2_found)
        self.assertEqual(task2_found.description, "Description for task 2")

    def test_get_all_tasks_returns_tasks_sorted_by_id(self):
        """Test that get_all_tasks returns tasks sorted by ID."""
        # Add tasks in non-sequential order to test sorting
        task3 = self.task_manager.add_task("Task 3")
        task1 = self.task_manager.add_task("Task 1")
        task2 = self.task_manager.add_task("Task 2")

        tasks = self.task_manager.get_all_tasks()
        self.assertEqual(len(tasks), 3)

        # Check that tasks are sorted by ID (numerically)
        task_ids = [int(task.id) for task in tasks]
        self.assertEqual(task_ids, sorted(task_ids))


    def test_update_task_title_successfully(self):
        """Test updating a task's title successfully."""
        task = self.task_manager.add_task("Original Title", "Original Description")
        original_id = task.id
        original_completion = task.completed

        result = self.task_manager.update_task(original_id, title="New Title")

        self.assertTrue(result)
        updated_task = self.task_manager.get_task_by_id(original_id)
        self.assertEqual(updated_task.title, "New Title")
        self.assertEqual(updated_task.description, "Original Description")  # Should remain unchanged
        self.assertEqual(updated_task.completed, original_completion)  # Should remain unchanged

    def test_update_task_description_successfully(self):
        """Test updating a task's description successfully."""
        task = self.task_manager.add_task("Original Title", "Original Description")
        original_id = task.id
        original_completion = task.completed

        result = self.task_manager.update_task(original_id, description="New Description")

        self.assertTrue(result)
        updated_task = self.task_manager.get_task_by_id(original_id)
        self.assertEqual(updated_task.title, "Original Title")  # Should remain unchanged
        self.assertEqual(updated_task.description, "New Description")
        self.assertEqual(updated_task.completed, original_completion)  # Should remain unchanged

    def test_update_task_title_and_description_successfully(self):
        """Test updating both title and description of a task successfully."""
        task = self.task_manager.add_task("Original Title", "Original Description")
        original_id = task.id
        original_completion = task.completed

        result = self.task_manager.update_task(original_id, title="New Title", description="New Description")

        self.assertTrue(result)
        updated_task = self.task_manager.get_task_by_id(original_id)
        self.assertEqual(updated_task.title, "New Title")
        self.assertEqual(updated_task.description, "New Description")
        self.assertEqual(updated_task.completed, original_completion)  # Should remain unchanged

    def test_update_task_returns_false_for_nonexistent_task(self):
        """Test that updating a non-existent task returns False."""
        result = self.task_manager.update_task("999", title="New Title")
        self.assertFalse(result)

    def test_update_task_with_empty_title_raises_error(self):
        """Test that updating a task with an empty title raises an error."""
        task = self.task_manager.add_task("Original Title")

        with self.assertRaises(ValueError):
            self.task_manager.update_task(task.id, title="")

    def test_update_task_with_whitespace_only_title_raises_error(self):
        """Test that updating a task with whitespace-only title raises an error."""
        task = self.task_manager.add_task("Original Title")

        with self.assertRaises(ValueError):
            self.task_manager.update_task(task.id, title="   ")


    def test_delete_task_successfully(self):
        """Test deleting a task successfully."""
        task = self.task_manager.add_task("Task to Delete", "Description")
        original_count = self.task_manager.get_task_count()

        result = self.task_manager.delete_task(task.id)

        self.assertTrue(result)
        self.assertEqual(self.task_manager.get_task_count(), original_count - 1)
        # Verify the task no longer exists
        deleted_task = self.task_manager.get_task_by_id(task.id)
        self.assertIsNone(deleted_task)

    def test_delete_task_returns_false_for_nonexistent_task(self):
        """Test that deleting a non-existent task returns False."""
        result = self.task_manager.delete_task("999")
        self.assertFalse(result)
        # Task count should remain the same
        self.assertEqual(self.task_manager.get_task_count(), 0)

    def test_delete_task_does_not_affect_other_tasks(self):
        """Test that deleting one task does not affect other tasks."""
        task1 = self.task_manager.add_task("Task 1", "Description 1")
        task2 = self.task_manager.add_task("Task 2", "Description 2")
        task3 = self.task_manager.add_task("Task 3", "Description 3")
        original_count = self.task_manager.get_task_count()

        result = self.task_manager.delete_task(task2.id)

        self.assertTrue(result)
        self.assertEqual(self.task_manager.get_task_count(), original_count - 1)

        # Verify task1 and task3 still exist
        self.assertIsNotNone(self.task_manager.get_task_by_id(task1.id))
        self.assertIsNone(self.task_manager.get_task_by_id(task2.id))
        self.assertIsNotNone(self.task_manager.get_task_by_id(task3.id))


    def test_toggle_completion_successfully(self):
        """Test toggling a task's completion status successfully."""
        task = self.task_manager.add_task("Test Task", "Test Description")
        original_id = task.id
        original_status = task.completed  # Should be False by default

        # Toggle completion
        result = self.task_manager.toggle_completion(original_id)

        self.assertTrue(result)
        toggled_task = self.task_manager.get_task_by_id(original_id)
        self.assertEqual(toggled_task.completed, not original_status)  # Should be True now

        # Toggle again
        result = self.task_manager.toggle_completion(original_id)
        toggled_again_task = self.task_manager.get_task_by_id(original_id)
        self.assertEqual(toggled_again_task.completed, original_status)  # Should be False again

    def test_toggle_completion_returns_false_for_nonexistent_task(self):
        """Test that toggling completion of a non-existent task returns False."""
        result = self.task_manager.toggle_completion("999")
        self.assertFalse(result)

    def test_toggle_completion_preserves_other_attributes(self):
        """Test that toggling completion preserves other task attributes."""
        task = self.task_manager.add_task("Original Title", "Original Description")
        original_id = task.id
        original_title = task.title
        original_description = task.description
        original_completed = task.completed

        # Toggle completion
        result = self.task_manager.toggle_completion(original_id)

        self.assertTrue(result)
        toggled_task = self.task_manager.get_task_by_id(original_id)
        self.assertEqual(toggled_task.id, original_id)
        self.assertEqual(toggled_task.title, original_title)
        self.assertEqual(toggled_task.description, original_description)
        # Only completion status should change
        self.assertNotEqual(toggled_task.completed, original_completed)


if __name__ == "__main__":
    unittest.main()
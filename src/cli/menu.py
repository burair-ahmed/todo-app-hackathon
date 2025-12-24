"""
Menu Interface

This module provides the console interface for the Todo Console Application.
"""

from ..services.task_manager import TaskManager


class Menu:
    """
    Provides the console menu interface for the Todo Console Application.

    This class handles all user interactions through the console menu system,
    including adding, viewing, updating, deleting, and toggling completion
    status of tasks.
    """

    def __init__(self):
        """Initialize the menu with a task manager."""
        self.task_manager = TaskManager()

    def display_menu(self):
        """Display the main menu options."""
        print("\n" + "="*50)
        print("TODO CONSOLE APPLICATION")
        print("="*50)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete/Incomplete")
        print("6. Exit")
        print("="*50)

    def get_user_choice(self) -> str:
        """
        Get the user's menu choice.

        Returns:
            str: The user's menu choice (1-6)
        """
        try:
            choice = input("Enter your choice (1-6): ").strip()
            return choice
        except (EOFError, KeyboardInterrupt):
            print("\n\nExiting application...")
            return "6"

    def handle_add_task(self):
        """Handle the add task functionality."""
        print("\n--- Add New Task ---")
        try:
            title = input("Enter task title: ").strip()
            if not title:
                print("Error: Task title cannot be empty.")
                return

            description = input("Enter task description (optional): ").strip()

            task = self.task_manager.add_task(title, description)
            print(f"[COMPLETED] Task added successfully! ID: {task.id}")
        except ValueError as e:
            print(f"[ERROR] Error: {e}")
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred while adding the task: {e}")

    def handle_view_tasks(self):
        """Handle the view tasks functionality."""
        print("\n--- View All Tasks ---")
        try:
            tasks = self.task_manager.get_all_tasks()

            if not tasks:
                print("Info: No tasks found.")
                return

            print(f"\nTotal tasks: {len(tasks)}")
            for task in tasks:
                status_icon = "[COMPLETED]" if task.completed else "[INCOMPLETE]"
                status_text = "Complete" if task.completed else "Incomplete"
                print(f"ID: {task.id} | [{status_icon}] {status_text} | Title: {task.title}")
                if task.description:
                    print(f"     Description: {task.description}")
                print("-" * 40)
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred while viewing tasks: {e}")

    def handle_update_task(self):
        """Handle the update task functionality."""
        print("\n--- Update Task ---")
        try:
            if self.task_manager.get_task_count() == 0:
                print("Info: No tasks available to update.")
                return

            task_id = input("Enter task ID to update: ").strip()
            if not task_id:
                print("Info:  No task ID provided.")
                return

            task = self.task_manager.get_task_by_id(task_id)
            if not task:
                print(f"[ERROR] Error: Task with ID '{task_id}' not found.")
                return

            print(f"Current task: [{task.title}] - {task.description}")
            print(f"Status: {'Complete' if task.completed else 'Incomplete'}")

            new_title = input(f"Enter new title (or press Enter to keep '{task.title}'): ").strip()
            new_description = input(f"Enter new description (or press Enter to keep current): ").strip()

            # Use None to indicate no change, empty string to indicate clearing
            title_to_update = new_title if new_title != "" else None
            description_to_update = new_description if new_description != "" else None

            if title_to_update is None and description_to_update is None:
                print("Info:  No changes made.")
                return

            if self.task_manager.update_task(task_id, title_to_update, description_to_update):
                print("[COMPLETED] Task updated successfully!")
            else:
                print("[ERROR] Error updating task.")
        except ValueError as e:
            print(f"[ERROR] Error: {e}")
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred while updating the task: {e}")

    def handle_delete_task(self):
        """Handle the delete task functionality."""
        print("\n--- Delete Task ---")
        try:
            if self.task_manager.get_task_count() == 0:
                print("Info:  No tasks available to delete.")
                return

            task_id = input("Enter task ID to delete: ").strip()
            if not task_id:
                print("Info:  No task ID provided.")
                return

            task = self.task_manager.get_task_by_id(task_id)
            if not task:
                print(f"[ERROR] Error: Task with ID '{task_id}' not found.")
                return

            print(f"Task to delete: [{task.title}] - {task.description}")
            confirm = input("Are you sure you want to delete this task? (y/N): ").strip().lower()

            if confirm in ['y', 'yes']:
                if self.task_manager.delete_task(task_id):
                    print("[COMPLETED] Task deleted successfully!")
                else:
                    print("[ERROR] Error deleting task.")
            else:
                print("Info:  Task deletion cancelled.")
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred while deleting the task: {e}")

    def handle_toggle_completion(self):
        """Handle the toggle task completion functionality."""
        print("\n--- Toggle Task Completion ---")
        try:
            if self.task_manager.get_task_count() == 0:
                print("Info:  No tasks available to toggle.")
                return

            task_id = input("Enter task ID to toggle completion: ").strip()
            if not task_id:
                print("Info:  No task ID provided.")
                return

            task = self.task_manager.get_task_by_id(task_id)
            if not task:
                print(f"[ERROR] Error: Task with ID '{task_id}' not found.")
                return

            current_status = "Complete" if task.completed else "Incomplete"
            new_status = "Incomplete" if task.completed else "Complete"

            if self.task_manager.toggle_completion(task_id):
                print(f"[COMPLETED] Task status changed from {current_status} to {new_status}!")
            else:
                print("[ERROR] Error toggling task completion.")
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred while toggling task completion: {e}")

    def run(self):
        """Run the main application loop."""
        print("Welcome to the Todo Console Application!")
        print("Type '6' or use Ctrl+C to exit the application.")

        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == "1":
                self.handle_add_task()
            elif choice == "2":
                self.handle_view_tasks()
            elif choice == "3":
                self.handle_update_task()
            elif choice == "4":
                self.handle_delete_task()
            elif choice == "5":
                self.handle_toggle_completion()
            elif choice == "6":
                print("\nThank you for using the Todo Console Application!")
                print("Goodbye!")
                break
            else:
                print(f"\n[INVALID] Invalid choice: '{choice}'. Please enter a number between 1 and 6.")

            # Pause to let user see the result before showing the menu again
            input("\nPress Enter to continue...")
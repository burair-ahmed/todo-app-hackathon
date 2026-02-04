"""
Menu Interface

This module provides the console interface for the Todo Console Application.
"""

from ..services.task_manager import TaskManager


class Colors:
    """ANSI color codes for console styling."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


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

    def display_banner(self):
        """Display a stylized ASCII banner."""
        banner = rf"""{Colors.CYAN}{Colors.BOLD}
   __ __         _               
  / // /__  ____(_)__ ___  ___   
 / _  / _ \/ __/ /_ // _ \/ _ \  
/_//_/\___/_/ /_//__/\___/_//_/  
{Colors.BLUE}   AI-Native Task Orchestrator{Colors.RESET}
        """
        print(banner)

    def display_menu(self):
        """Display the main menu options."""
        print(f"{Colors.BLUE}{Colors.BOLD}{'='*50}{Colors.RESET}")
        print(f"{Colors.HEADER}{Colors.BOLD}  MAIN MENU{Colors.RESET}")
        print(f"{Colors.BLUE}{'='*50}{Colors.RESET}")
        print(f"{Colors.CYAN}1.{Colors.RESET} Add New Task")
        print(f"{Colors.CYAN}2.{Colors.RESET} View All Tasks")
        print(f"{Colors.CYAN}3.{Colors.RESET} Update Existing Task")
        print(f"{Colors.CYAN}4.{Colors.RESET} Delete Task")
        print(f"{Colors.CYAN}5.{Colors.RESET} Toggle Completion")
        print(f"{Colors.RED}6.{Colors.RESET} Exit System")
        print(f"{Colors.BLUE}{'='*50}{Colors.RESET}")

    def get_user_choice(self) -> str:
        """
        Get the user's menu choice.

        Returns:
            str: The user's menu choice (1-6)
        """
        try:
            prompt = f"{Colors.BOLD}Selection (1-6) > {Colors.RESET}"
            choice = input(prompt).strip()
            return choice
        except (EOFError, KeyboardInterrupt):
            print(f"\n\n{Colors.YELLOW}Exiting application...{Colors.RESET}")
            return "6"

    def handle_add_task(self):
        """Handle the add task functionality."""
        print(f"\n{Colors.BLUE}{Colors.BOLD}>>> {Colors.HEADER}Add New Task{Colors.RESET}")
        try:
            title = input(f"{Colors.BOLD}Title: {Colors.RESET}").strip()
            if not title:
                print(f"{Colors.RED}[ERROR] Task title cannot be empty.{Colors.RESET}")
                return

            description = input(f"{Colors.BOLD}Description (optional): {Colors.RESET}").strip()

            task = self.task_manager.add_task(title, description)
            print(f"{Colors.GREEN}[SUCCESS] Task added! ID: {Colors.CYAN}{task.id}{Colors.RESET}")
        except ValueError as e:
            print(f"{Colors.RED}[ERROR] {e}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[ERROR] Unexpected error: {e}{Colors.RESET}")

    def handle_view_tasks(self):
        """Handle the view tasks functionality."""
        print(f"\n{Colors.BLUE}{Colors.BOLD}>>> {Colors.HEADER}Your Task List{Colors.RESET}")
        try:
            tasks = self.task_manager.get_all_tasks()

            if not tasks:
                print(f"{Colors.YELLOW}Info: No tasks found.{Colors.RESET}")
                return

            print(f"Total: {Colors.CYAN}{len(tasks)}{Colors.RESET} tasks\n")
            for task in tasks:
                if task.completed:
                    status_badge = f"{Colors.GREEN}[✓ COMPLETE]{Colors.RESET}"
                    title_style = f"{Colors.BLUE}"
                else:
                    status_badge = f"{Colors.YELLOW}[- PENDING ]{Colors.RESET}"
                    title_style = f"{Colors.BOLD}"

                print(f"{Colors.CYAN}#{task.id[:8]}{Colors.RESET} {status_badge} {title_style}{task.title}{Colors.RESET}")
                if task.description:
                    print(f"       {Colors.BLUE}└─ {Colors.RESET}{task.description}")
            print(f"\n{Colors.BLUE}{'-' * 40}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[ERROR] Unexpected error: {e}{Colors.RESET}")

    def handle_update_task(self):
        """Handle the update task functionality."""
        print(f"\n{Colors.BLUE}{Colors.BOLD}>>> {Colors.HEADER}Update Task{Colors.RESET}")
        try:
            if self.task_manager.get_task_count() == 0:
                print(f"{Colors.YELLOW}Info: No tasks available to update.{Colors.RESET}")
                return

            task_id = input(f"{Colors.BOLD}Enter Task ID: {Colors.RESET}").strip()
            if not task_id:
                return
            
            # Handle '#' prefix if user copies it from the list view
            if task_id.startswith('#'):
                task_id = task_id[1:]

            task = self.task_manager.get_task_by_id(task_id)
            if not task:
                print(f"{Colors.RED}[ERROR] Task '{task_id}' not found.{Colors.RESET}")
                return

            print(f"{Colors.BLUE}Current: {Colors.RESET}{task.title}")
            
            new_title = input(f"{Colors.BOLD}New Title (ENTER to skip): {Colors.RESET}").strip()
            new_description = input(f"{Colors.BOLD}New Description (ENTER to skip): {Colors.RESET}").strip()

            title_to_update = new_title if new_title != "" else None
            description_to_update = new_description if new_description != "" else None

            if title_to_update is None and description_to_update is None:
                print(f"{Colors.YELLOW}No changes made.{Colors.RESET}")
                return

            if self.task_manager.update_task(task_id, title_to_update, description_to_update):
                print(f"{Colors.GREEN}[SUCCESS] Task updated.{Colors.RESET}")
            else:
                print(f"{Colors.RED}[ERROR] Update failed.{Colors.RESET}")
        except ValueError as e:
            print(f"{Colors.RED}[ERROR] {e}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[ERROR] Unexpected error: {e}{Colors.RESET}")

    def handle_delete_task(self):
        """Handle the delete task functionality."""
        print(f"\n{Colors.BLUE}{Colors.BOLD}>>> {Colors.HEADER}Delete Task{Colors.RESET}")
        try:
            if self.task_manager.get_task_count() == 0:
                print(f"{Colors.YELLOW}Info: No tasks to delete.{Colors.RESET}")
                return

            task_id = input(f"{Colors.BOLD}Enter Task ID: {Colors.RESET}").strip()
            if not task_id:
                return

            # Handle '#' prefix if user copies it from the list view
            if task_id.startswith('#'):
                task_id = task_id[1:]

            task = self.task_manager.get_task_by_id(task_id)
            if not task:
                print(f"{Colors.RED}[ERROR] Task '{task_id}' not found.{Colors.RESET}")
                return

            confirm = input(f"{Colors.RED}{Colors.BOLD}Delete '{task.title}'? (y/N): {Colors.RESET}").strip().lower()

            if confirm in ['y', 'yes']:
                if self.task_manager.delete_task(task_id):
                    print(f"{Colors.GREEN}[SUCCESS] Task deleted.{Colors.RESET}")
                else:
                    print(f"{Colors.RED}[ERROR] Deletion failed.{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}Cancelled.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[ERROR] Unexpected error: {e}{Colors.RESET}")

    def handle_toggle_completion(self):
        """Handle the toggle task completion functionality."""
        print(f"\n{Colors.BLUE}{Colors.BOLD}>>> {Colors.HEADER}Toggle Status{Colors.RESET}")
        try:
            if self.task_manager.get_task_count() == 0:
                return

            task_id = input(f"{Colors.BOLD}Enter Task ID: {Colors.RESET}").strip()
            if not task_id:
                return

            # Handle '#' prefix if user copies it from the list view
            if task_id.startswith('#'):
                task_id = task_id[1:]

            task = self.task_manager.get_task_by_id(task_id)
            if not task:
                print(f"{Colors.RED}[ERROR] Task '{task_id}' not found.{Colors.RESET}")
                return

            if self.task_manager.toggle_completion(task_id):
                # Status message reflects the NEW state
                status = f"{Colors.GREEN}COMPLETE{Colors.RESET}" if task.completed else f"{Colors.YELLOW}PENDING{Colors.RESET}"
                print(f"{Colors.GREEN}[SUCCESS] Status updated to {status}{Colors.RESET}")
            else:
                print(f"{Colors.RED}[ERROR] Toggle failed.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[ERROR] Unexpected error: {e}{Colors.RESET}")

    def run(self):
        """Run the main application loop."""
        self.display_banner()
        
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
                print(f"\n{Colors.HEADER}Thank you for using Horizon.{Colors.RESET}")
                print(f"{Colors.BLUE}Terminating session...{Colors.RESET}")
                break
            else:
                print(f"\n{Colors.RED}[INVALID]{Colors.RESET} Choice '{choice}' not recognized.")

            input(f"\n{Colors.BLUE}Press ENTER to return to menu...{Colors.RESET}")
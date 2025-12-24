#!/usr/bin/env python3
"""
Todo Console Application - Main Entry Point

This is the main entry point for the Todo In-Memory Python Console Application.
The application allows users to manage their tasks through a console interface.
"""

def main():
    """
    Main application entry point.

    This function initializes and runs the Todo Console Application.
    It creates the main menu and starts the application loop.
    """
    print("Welcome to the Todo Console Application!")
    print("Loading application...")

    # Import here to avoid circular dependencies during startup
    import sys
    import os

    # Determine if we're running as a script or as part of a package
    if __package__ is None:
        # We're running as a script, add src to path for relative imports to work
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        sys.path.insert(0, parent_dir)
        from src.cli.menu import Menu
    else:
        # We're running as part of a package
        from .cli.menu import Menu

    # Create and run the menu
    menu = Menu()
    menu.run()


if __name__ == "__main__":
    main()
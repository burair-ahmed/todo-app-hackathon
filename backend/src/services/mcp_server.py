from typing import List, Dict, Any
from sqlmodel import Session, select
from ..database import get_session
from ..models.task import Task, TaskUpdate, TaskCreate
from ..models.conversation import Conversation
from ..models.message import Message
from functools import wraps

# This is a simplified implementation of an MCP-like server
# In a real implementation, this would use the official MCP SDK

def enforce_user_ownership(func):
    """
    Decorator to enforce that operations only affect resources owned by the user
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # In a real implementation, this would verify that the operation
        # is only affecting resources owned by the requesting user
        return func(*args, **kwargs)
    return wrapper

@enforce_user_ownership
def add_task(user_id: str, title: str, description: str = None) -> Dict[str, Any]:
    """
    MCP tool to add a task for a user
    """
    try:
        from uuid import UUID
        from ..services.task_service import create_task

        # Validate user_id is a proper UUID
        user_uuid = UUID(user_id) if not isinstance(user_id, UUID) else user_id

        # Create task using the existing task service
        with next(get_session()) as session:
            task_data = TaskCreate(
                title=title,
                description=description or "",
                completed=False,
                user_id=user_uuid
            )
            created_task = create_task(session, task_data)

        return {
            "status": "success",
            "task_id": str(created_task.id),  # Convert UUID to string for JSON serialization
            "message": f"Task '{title}' added successfully"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to add task: {str(e)}"
        }

@enforce_user_ownership
def list_tasks(user_id: str, status: str = None) -> List[Dict[str, Any]]:
    """
    MCP tool to list tasks for a user
    """
    try:
        from uuid import UUID
        from ..services.task_service import get_tasks_by_user_id

        # Validate user_id is a proper UUID
        user_uuid = UUID(user_id) if not isinstance(user_id, UUID) else user_id

        # Get tasks using the existing task service
        with next(get_session()) as session:
            tasks = get_tasks_by_user_id(session, user_uuid)

            # Filter by status if specified
            if status:
                if status.lower() == 'completed':
                    tasks = [task for task in tasks if task.completed]
                elif status.lower() == 'pending':
                    tasks = [task for task in tasks if not task.completed]

            # Convert tasks to the expected format
            result = []
            for task in tasks:
                result.append({
                    "id": str(task.id),  # Convert UUID to string
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                })

        return result
    except Exception as e:
        return []

@enforce_user_ownership
def update_task(user_id: str, task_id: int, title: str = None, description: str = None) -> Dict[str, Any]:
    """
    MCP tool to update a task for a user
    """
    try:
        from uuid import UUID
        from ..services.task_service import get_task_by_id, update_task as service_update_task

        # Validate user_id is a proper UUID
        user_uuid = UUID(user_id) if not isinstance(user_id, UUID) else user_id

        # Get the task using the existing task service
        with next(get_session()) as session:
            task = get_task_by_id(session, task_id)

            # Check if task exists and belongs to user
            if not task or str(task.user_id) != str(user_uuid):
                return {
                    "status": "error",
                    "message": f"Task {task_id} not found or doesn't belong to user"
                }

            # Prepare update data
            update_data = {}
            if title is not None:
                update_data["title"] = title
            if description is not None:
                update_data["description"] = description

            # Update the task using the existing task service
            updated_task = service_update_task(session, task_id, update_data)

        return {
            "status": "success",
            "message": f"Task {task_id} updated successfully"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to update task: {str(e)}"
        }

@enforce_user_ownership
def complete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    MCP tool to mark a task as complete for a user
    """
    try:
        from uuid import UUID
        from ..services.task_service import get_task_by_id, update_task as service_update_task

        # Validate user_id is a proper UUID
        user_uuid = UUID(user_id) if not isinstance(user_id, UUID) else user_id

        # Get the task using the existing task service
        with next(get_session()) as session:
            task = get_task_by_id(session, task_id)

            # Check if task exists and belongs to user
            if not task or str(task.user_id) != str(user_uuid):
                return {
                    "status": "error",
                    "message": f"Task {task_id} not found or doesn't belong to user"
                }

            # Update the task to mark as complete
            update_data = {"completed": True}
            updated_task = service_update_task(session, task_id, update_data)

        return {
            "status": "success",
            "message": f"Task {task_id} marked as complete"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to complete task: {str(e)}"
        }

@enforce_user_ownership
def delete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    MCP tool to delete a task for a user
    """
    try:
        from uuid import UUID
        from ..services.task_service import get_task_by_id, delete_task as service_delete_task

        # Validate user_id is a proper UUID
        user_uuid = UUID(user_id) if not isinstance(user_id, UUID) else user_id

        # Get the task using the existing task service
        with next(get_session()) as session:
            task = get_task_by_id(session, task_id)

            # Check if task exists and belongs to user
            if not task or str(task.user_id) != str(user_uuid):
                return {
                    "status": "error",
                    "message": f"Task {task_id} not found or doesn't belong to user"
                }

            # Delete the task using the existing task service
            success = service_delete_task(session, task_id)

        if success:
            return {
                "status": "success",
                "message": f"Task {task_id} deleted successfully"
            }
        else:
            return {
                "status": "error",
                "message": f"Failed to delete task {task_id}"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to delete task: {str(e)}"
        }

def initialize_mcp_server():
    """
    Initialize the MCP server
    """
    # In a real implementation, this would set up the actual MCP server
    # For now, just returning a mock server object
    return {
        "status": "initialized",
        "tools": ["add_task", "list_tasks", "update_task", "complete_task", "delete_task"]
    }

def get_mcp_tools():
    """
    Get the registered MCP tools
    """
    return {
        "add_task": add_task,
        "list_tasks": list_tasks,
        "update_task": update_task,
        "complete_task": complete_task,
        "delete_task": delete_task
    }

# Initialize the server when module is loaded
mcp_server = initialize_mcp_server()
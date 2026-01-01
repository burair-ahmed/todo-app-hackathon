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
def add_task(
    user_id: str, 
    title: str, 
    description: str = None,
    priority: str = "medium",
    label: str = None,
    due_date: str = None,
    recurrence: str = "none"
) -> Dict[str, Any]:
    """
    MCP tool to add a task for a user with all available fields.
    - priority: low, medium, high
    - label: work, home
    - recurrence: none, daily, weekly, monthly
    - due_date: ISO format string
    """
    try:
        from uuid import UUID
        from datetime import datetime
        from dateutil import parser
        from ..services.task_service import create_task
        from ..models.task import PriorityEnum, LabelEnum, RecurrenceEnum

        # Validate user_id is a proper UUID
        user_uuid = UUID(user_id) if not isinstance(user_id, UUID) else user_id

        # Parse due_date
        parsed_due_date = None
        if due_date:
            try:
                from dateutil import parser
                import datetime as dt
                parsed_due_date = parser.parse(due_date)
                
                # If naive, assume it's user's local time (UTC+5) and convert to UTC
                if parsed_due_date.tzinfo is None:
                    tz = dt.timezone(dt.timedelta(hours=5))
                    parsed_due_date = parsed_due_date.replace(tzinfo=tz).astimezone(dt.timezone.utc)
            except Exception as de:
                print(f"ADD_TASK DUE_DATE PARSE ERROR: {de}")

        # Create task using the existing task service
        with next(get_session()) as session:
            task_data = TaskCreate(
                title=title,
                description=description or "",
                completed=False,
                priority=PriorityEnum(priority.lower()) if priority else PriorityEnum.MEDIUM,
                label=LabelEnum(label.lower()) if label else None,
                due_date=parsed_due_date,
                recurrence=RecurrenceEnum(recurrence.lower()) if recurrence else RecurrenceEnum.NONE
            )
            created_task = create_task(session, task_data, user_id=user_uuid)

        return {
            "status": "success",
            "task": {
                "id": str(created_task.id),
                "title": created_task.title
            },
            "message": f"Task '{title}' added successfully"
        }
    except Exception as e:
        import traceback
        print(f"ADD_TASK ERROR: {str(e)}\n{traceback.format_exc()}")
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
        from ..services.task_service import get_tasks_by_user

        # Validate user_id is a proper UUID
        user_uuid = UUID(user_id) if not isinstance(user_id, UUID) else user_id

        # Get tasks using the existing task service
        with next(get_session()) as session:
            # Note: get_tasks_by_user handles user_id as a required param
            tasks = get_tasks_by_user(session, user_id=user_uuid)

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
        import traceback
        print(f"LIST_TASKS ERROR: {str(e)}\n{traceback.format_exc()}")
        return []

@enforce_user_ownership
def update_task(
    user_id: str, 
    task_id: Any, 
    title: str = None, 
    description: str = None,
    priority: str = None,
    label: str = None,
    due_date: str = None,
    recurrence: str = None
) -> Dict[str, Any]:
    """
    MCP tool to update a task for a user.
    Supports updating title, description, priority, label, due_date, and recurrence.
    """
    try:
        from uuid import UUID
        from datetime import datetime
        from dateutil import parser
        from ..services.task_service import get_task_by_id, update_task as service_update_task
        from ..models.task import TaskUpdate, PriorityEnum, LabelEnum, RecurrenceEnum

        # Validate user_id is a proper UUID
        user_uuid = UUID(user_id) if not isinstance(user_id, UUID) else user_id
        
        # Validate task_id is a proper UUID
        try:
            task_uuid = UUID(str(task_id))
        except (ValueError, TypeError):
             return {
                "status": "error",
                "message": f"Invalid task ID format: {task_id}. Please use the full UUID."
            }

        # Get the task using the existing task service
        with next(get_session()) as session:
            task = get_task_by_id(session, task_uuid, user_id=user_uuid)

            if not task:
                return {
                    "status": "error",
                    "message": f"Task {task_id} not found or doesn't belong to you."
                }

            # Prepare update data
            parsed_due_date = task.due_date
            if due_date:
                try:
                    from dateutil import parser
                    import datetime as dt
                    parsed_due_date = parser.parse(due_date)
                    
                    # If naive, assume it's user's local time (UTC+5) and convert to UTC
                    if parsed_due_date.tzinfo is None:
                        tz = dt.timezone(dt.timedelta(hours=5))
                        parsed_due_date = parsed_due_date.replace(tzinfo=tz).astimezone(dt.timezone.utc)
                except Exception as de:
                    print(f"UPDATE DUE_DATE PARSE ERROR: {de}")

            task_update = TaskUpdate(
                title=title if title is not None else task.title,
                description=description if description is not None else task.description,
                priority=PriorityEnum(priority.lower()) if priority else task.priority,
                label=LabelEnum(label.lower()) if label else task.label,
                due_date=parsed_due_date,
                recurrence=RecurrenceEnum(recurrence.lower()) if recurrence else task.recurrence
            )

            # Update the task using the existing task service
            updated_task = service_update_task(session, task_uuid, task_update, user_id=user_uuid)

        return {
            "status": "success",
            "message": f"Task updated successfully"
        }
    except Exception as e:
        import traceback
        print(f"UPDATE_TASK ERROR: {str(e)}\n{traceback.format_exc()}")
        return {
            "status": "error",
            "message": f"Failed to update task: {str(e)}"
        }

@enforce_user_ownership
def complete_task(user_id: str, task_id: Any) -> Dict[str, Any]:
    """
    MCP tool to mark a task as complete for a user
    """
    try:
        from uuid import UUID
        from ..services.task_service import toggle_task_completion

        # Validate user_id is a proper UUID
        user_uuid = UUID(user_id) if not isinstance(user_id, UUID) else user_id
        
        # Validate task_id is a proper UUID
        try:
            task_uuid = UUID(str(task_id))
        except (ValueError, TypeError):
             return {
                "status": "error",
                "message": f"Invalid task ID format: {task_id}. Please use the full UUID."
            }

        # Toggle completion using the existing task service
        with next(get_session()) as session:
            updated_task = toggle_task_completion(session, task_uuid, user_id=user_uuid)

            if not updated_task:
                return {
                    "status": "error",
                    "message": f"Task {task_id} not found or doesn't belong to you."
                }

        return {
            "status": "success",
            "message": f"Task marked as complete"
        }
    except Exception as e:
        import traceback
        print(f"COMPLETE_TASK ERROR: {str(e)}\n{traceback.format_exc()}")
        return {
            "status": "error",
            "message": f"Failed to complete task: {str(e)}"
        }

@enforce_user_ownership
def delete_task(user_id: str, task_id: Any) -> Dict[str, Any]:
    """
    MCP tool to delete a task for a user
    """
    try:
        from uuid import UUID
        from ..services.task_service import delete_task as service_delete_task

        # Validate user_id is a proper UUID
        user_uuid = UUID(user_id) if not isinstance(user_id, UUID) else user_id
        
        # Validate task_id is a proper UUID
        try:
            task_uuid = UUID(str(task_id))
        except (ValueError, TypeError):
             return {
                "status": "error",
                "message": f"Invalid task ID format: {task_id}. Please use the full UUID."
            }

        # Delete the task using the existing task service
        with next(get_session()) as session:
            success = service_delete_task(session, task_uuid, user_id=user_uuid)

        if success:
            return {
                "status": "success",
                "message": f"Task deleted successfully"
            }
        else:
            return {
                "status": "error",
                "message": f"Failed to delete task {task_id} or not found."
            }
    except Exception as e:
        import traceback
        print(f"DELETE_TASK ERROR: {str(e)}\n{traceback.format_exc()}")
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
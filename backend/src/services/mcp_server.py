from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from ..database import get_session
from ..models.task import Task, TaskCreate, TaskUpdate, PriorityEnum, LabelEnum, RecurrenceEnum
from ..services.task_service import (
    create_task, 
    get_tasks_by_user, 
    get_task_by_id, 
    update_task as service_update_task, 
    toggle_task_completion, 
    delete_task as service_delete_task
)
from uuid import UUID
from datetime import datetime
import dateutil.parser
import datetime as dt

# Initialize FastMCP Server
mcp = FastMCP("TodoMCP")

@mcp.tool()
async def add_task(
    user_id: str, 
    title: str, 
    description: str = "",
    priority: str = "medium",
    label: str = None,
    due_date: str = None,
    recurrence: str = "none"
) -> Dict[str, Any]:
    """
    Add a task for a user.
    
    Args:
        user_id: The UUID of the user.
        title: Task title.
        description: Task description (optional).
        priority: 'low', 'medium', 'high' (default: 'medium').
        label: 'work', 'home' (optional).
        due_date: ISO 8601 string (e.g., '2023-12-31T23:59:00') (optional).
        recurrence: 'daily', 'weekly', 'monthly' (default: 'none').
    """
    try:
        user_uuid = UUID(user_id)
        
        parsed_due_date = None
        if due_date:
            try:
                parsed_due_date = dateutil.parser.parse(due_date)
                if parsed_due_date.tzinfo is None:
                    # Assume user's local time (approx UTC+5 per previous context) or UTC default
                    tz = dt.timezone(dt.timedelta(hours=5)) 
                    parsed_due_date = parsed_due_date.replace(tzinfo=tz).astimezone(dt.timezone.utc)
            except Exception:
                pass

        with next(get_session()) as session:
            task_data = TaskCreate(
                title=title,
                description=description,
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
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def list_tasks(user_id: str, status: str = None) -> List[Dict[str, Any]]:
    """
    List tasks for a user, optionally filtered by status ('completed' or 'pending').
    """
    try:
        user_uuid = UUID(user_id)
        with next(get_session()) as session:
            tasks = get_tasks_by_user(session, user_id=user_uuid)
            
            if status:
                if status.lower() == 'completed':
                    tasks = [t for t in tasks if t.completed]
                elif status.lower() == 'pending':
                    tasks = [t for t in tasks if not t.completed]
            
            return [{
                "id": str(t.id),
                "title": t.title,
                "description": t.description,
                "completed": t.completed,
                "priority": t.priority,
                "due_date": t.due_date.isoformat() if t.due_date else None
            } for t in tasks]
    except Exception as e:
        return []

@mcp.tool()
async def update_task(
    user_id: str, 
    task_id: str, 
    title: str = None, 
    description: str = None,
    priority: str = None,
    label: str = None,
    due_date: str = None,
    recurrence: str = None
) -> Dict[str, Any]:
    """
    Update an existing task.
    
    Args:
        user_id: The UUID of the user.
        task_id: The UUID of the task to update.
        title: New title (optional).
        description: New description (optional).
        priority: 'low', 'medium', 'high' (optional).
        label: 'work', 'home' (optional).
        due_date: ISO 8601 string (e.g., '2023-12-31T23:59:00'). Pass 'null' or 'clear' to remove the due date.
        recurrence: 'daily', 'weekly', 'monthly', 'none'. Pass 'none' or 'null' to remove recurrence.
    """
    try:
        user_uuid = UUID(user_id)
        task_uuid = UUID(task_id)
        
        with next(get_session()) as session:
            # Build update dict dynamically to avoid overwriting with None
            update_payload = {}
            
            if title is not None:
                update_payload["title"] = title
            if description is not None:
                update_payload["description"] = description
            if priority is not None:
                 update_payload["priority"] = PriorityEnum(priority.lower())
            if label is not None:
                 update_payload["label"] = LabelEnum(label.lower())
            
            # Handle Due Date
            if due_date is not None:
                if due_date.lower() in ["null", "none", "clear", "remove", ""]:
                    update_payload["due_date"] = None
                else:
                    try:
                        parsed = dateutil.parser.parse(due_date)
                        if parsed.tzinfo is None:
                            # Assume user local time (UTC+5 hack per context) or just UTC
                            tz = dt.timezone(dt.timedelta(hours=5))
                            parsed = parsed.replace(tzinfo=tz).astimezone(dt.timezone.utc)
                        update_payload["due_date"] = parsed
                    except Exception as e:
                        return {"status": "error", "message": f"Invalid date format: {due_date}"}

            # Handle Recurrence
            if recurrence is not None:
                if recurrence.lower() in ["null", "none", "clear", "remove", ""]:
                    update_payload["recurrence"] = RecurrenceEnum.NONE
                else:
                    try:
                        update_payload["recurrence"] = RecurrenceEnum(recurrence.lower())
                    except ValueError:
                         return {"status": "error", "message": f"Invalid recurrence: {recurrence}"}

            if not update_payload:
                return {"status": "success", "message": "No changes requested"}

            # Construct TaskUpdate with ONLY the set fields
            task_update = TaskUpdate(**update_payload)
            
            updated = service_update_task(session, task_uuid, task_update, user_id=user_uuid)
            
            if updated:
                return {"status": "success", "message": "Task updated"}
            else:
                return {"status": "error", "message": "Task not found or owned by user"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def complete_task(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Toggle completion status of a task.
    """
    try:
        user_uuid = UUID(user_id)
        task_uuid = UUID(task_id)
        
        with next(get_session()) as session:
            updated = toggle_task_completion(session, task_uuid, user_id=user_uuid)
            if updated:
                 return {"status": "success", "message": f"Task {'completed' if updated.completed else 'uncompleted'}"}
            return {"status": "error", "message": "Task not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def delete_task(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Delete a task.
    """
    try:
        user_uuid = UUID(user_id)
        task_uuid = UUID(task_id)
        
        with next(get_session()) as session:
            success = service_delete_task(session, task_uuid, user_id=user_uuid)
            if success:
                return {"status": "success", "message": "Task deleted"}
            return {"status": "error", "message": "Task not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_mcp_tools():
    """
    Expose tools for the Agent.
    """
    # FastMCP holds tools in internal registry. We can expose the underlying functions or use list_tools
    # For direct python usage in the same process, we can just return a dict of wrappers
    return {
        "add_task": add_task,
        "list_tasks": list_tasks,
        "update_task": update_task,
        "complete_task": complete_task,
        "delete_task": delete_task
    }

def initialize_mcp_server():
    """
    Dummy initialization for backward compatibility.
    """
    pass
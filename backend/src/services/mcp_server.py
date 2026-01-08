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
    """
    try:
        user_uuid = UUID(user_id)
        task_uuid = UUID(task_id)
        
        with next(get_session()) as session:
            parsed_due_date = None
            if due_date:
                try:
                    parsed_due_date = dateutil.parser.parse(due_date)
                    if parsed_due_date.tzinfo is None:
                         tz = dt.timezone(dt.timedelta(hours=5))
                         parsed_due_date = parsed_due_date.replace(tzinfo=tz).astimezone(dt.timezone.utc)
                except:
                    pass

            # If passing None to update_task service for fields, it usually ignores them or sets them to None
            # The service expects TaskUpdate model
            task_update = TaskUpdate(
                title=title,
                description=description,
                priority=PriorityEnum(priority.lower()) if priority else None,
                label=LabelEnum(label.lower()) if label else None,
                due_date=parsed_due_date,
                recurrence=RecurrenceEnum(recurrence.lower()) if recurrence else None
            )
            
            # Since update_task service checks for None fields in exclude_unset, we need to be careful
            # We constructed TaskUpdate with Nones for fields not passed.
            
            updated = service_update_task(session, task_uuid, task_update, user_id=user_uuid)
            
            if updated:
                return {"status": "success", "message": "Task updated"}
            else:
                return {"status": "error", "message": "Task not found or owned by user"}
    except Exception as e:
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
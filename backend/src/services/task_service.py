from sqlmodel import Session, select, or_, desc
from sqlalchemy.orm import selectinload
from typing import List, Optional, Dict
from uuid import UUID
from datetime import datetime, timedelta, timezone
from ..models.task import Task, TaskCreate, TaskUpdate, TaskPatch, Tag, TaskTagLink, RecurrenceEnum
from ..models.notification import Notification, NotificationType # Fixed import
from sqlalchemy import func

# In-memory cache to debounce recurrence checks (User ID -> Last Check Timestamp)
_last_recurrence_check = {}

def create_task(session: Session, task_create: TaskCreate, user_id: UUID) -> Task:
    """Create a new task for a user with priorities and tags."""
    task = Task(
        title=task_create.title,
        description=task_create.description,
        completed=task_create.completed,
        priority=task_create.priority,
        label=task_create.label,
        due_date=task_create.due_date,
        recurrence=task_create.recurrence,
        user_id=user_id
    )
    
    if task_create.tag_ids:
        statement = select(Tag).where(Tag.id.in_(task_create.tag_ids), Tag.user_id == user_id)
        tags = session.exec(statement).all()
        task.tags = tags

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def get_tasks_by_user(
    session: Session, 
    user_id: UUID,
    search: Optional[str] = None,
    priority: Optional[str] = None,
    completed: Optional[bool] = None,
    tag_id: Optional[UUID] = None,
    label: Optional[str] = None,
    sort_by: str = "created_at",
    order: str = "desc"
) -> List[Task]:
    """Get all tasks for a specific user with advanced filtering and sorting."""
    # Check for missing recurring tasks (auto-spawn)
    # Note: Recurring task spawning is now handled in background tasks by the API endpoint
    
    statement = select(Task).where(Task.user_id == user_id).options(selectinload(Task.tags))
    
    if search:
        statement = statement.where(
            or_(
                Task.title.ilike(f"%{search}%"),
                Task.description.ilike(f"%{search}%")
            )
        )
    
    if priority:
        statement = statement.where(Task.priority == priority)
        
    if completed is not None:
        statement = statement.where(Task.completed == completed)

    if tag_id:
        statement = statement.join(TaskTagLink).where(TaskTagLink.tag_id == tag_id)

    if label:
        statement = statement.where(Task.label == label)

    # Sorting logic
    sort_attr = getattr(Task, sort_by, Task.created_at)
    if order == "desc":
        statement = statement.order_by(desc(sort_attr))
    else:
        statement = statement.order_by(sort_attr)

    tasks = session.exec(statement).all()
    return tasks

def get_task_by_id(session: Session, task_id: UUID, user_id: UUID) -> Optional[Task]:
    """Get a specific task by ID for a specific user."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id).options(selectinload(Task.tags))
    task = session.exec(statement).first()
    return task

def update_task(session: Session, task_id: UUID, task_update: TaskUpdate, user_id: UUID) -> Optional[Task]:
    """Update a specific task for a user, including priority and tags."""
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return None

    update_data = task_update.dict(exclude_unset=True)
    
    # Handle tag_ids separately
    tag_ids = update_data.pop("tag_ids", None)
    if tag_ids is not None:
        statement = select(Tag).where(Tag.id.in_(tag_ids), Tag.user_id == user_id)
        tags = session.exec(statement).all()
        task.tags = tags

    for field, value in update_data.items():
        setattr(task, field, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def patch_task(session: Session, task_id: UUID, task_patch: TaskPatch, user_id: UUID) -> Optional[Task]:
    """Partially update a specific task for a user."""
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return None

    patch_data = task_patch.dict(exclude_unset=True)
    for field, value in patch_data.items():
        setattr(task, field, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def delete_task(session: Session, task_id: UUID, user_id: UUID) -> bool:
    """Delete a specific task for a user."""
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return False

    session.delete(task)
    session.commit()
    return True

def toggle_task_completion(session: Session, task_id: UUID, user_id: UUID) -> Optional[Task]:
    """Toggle the completion status of a specific task with recurrence logic."""
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return None

    from ..models.task import RecurrenceEnum
    
    # If task is currently being marked as completed (from False to True)
    if not task.completed:
        task.completed = True
        task.completed_at = datetime.now(timezone.utc)
        
        # Check for recurrence to spawn a NEW task
        if task.recurrence and task.recurrence != RecurrenceEnum.NONE:
            # Determine the new due date
            new_due_date = None
            if task.due_date:
                if task.recurrence == RecurrenceEnum.DAILY:
                    new_due_date = task.due_date + timedelta(days=1)
                elif task.recurrence == RecurrenceEnum.WEEKLY:
                    new_due_date = task.due_date + timedelta(weeks=1)
                elif task.recurrence == RecurrenceEnum.MONTHLY:
                    # Approximation: 30 days
                    new_due_date = task.due_date + timedelta(days=30)
            
            # Create the NEXT task instance
            # We copy everything except ID, created_at, updated_at, completed_at
            # We explicitly set completed=False
            
            # Ensure recurrence_group_id exists
            if not task.recurrence_group_id:
                task.recurrence_group_id =  task.id # Consider the first task as the group starter if none exists? 
                # Actually better to generate a new UUID if none exists, and assign it to BOTH
                # But we can't easily change the *current* task's ID structure if it was the group ID.
                # Let's just generate a new random UUID for the group if it's missing.
                if not task.recurrence_group_id:
                     import uuid
                     task.recurrence_group_id = uuid.uuid4()
            
            new_task = Task(
                title=task.title,
                description=task.description,
                completed=False,
                priority=task.priority,
                label=task.label,
                due_date=new_due_date,
                recurrence=task.recurrence,
                recurrence_group_id=task.recurrence_group_id,
                user_id=user_id,
                tags=task.tags # SQLAlchemy relationship copy
            )
            session.add(new_task)
            
            # FIRST: Commit the task changes (toggle + new task)
            session.add(task)
            session.commit()
            session.refresh(task)
            
            # SECOND: Attempt to create notification independently
            try:
                notification = Notification(
                    user_id=user_id,
                    type=NotificationType.RECURRING_SPAWNED,
                    message=f"New recurring task '{new_task.title}' has been scheduled for {new_task.due_date.strftime('%Y-%m-%d')}.",
                    task_id=new_task.id
                )
                session.add(notification)
                session.commit()
            except Exception as e:
                print(f"ERROR CREATING NOTIFICATION: {e}")
                session.rollback()
            
            # Note: We LEAVE the current task as completed. We do NOT reschedule it.
            return task
        
        # For non-recurring tasks, just save and return
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
            
    else:
        # Marking a completed task back to uncompleted
        task.completed = False
        task.completed_at = None
        # Implication: If the user unchecks a recurring task, do we delete the spawned one?
        # That's complex logic. For now, we just uncomplete this specific instance.
        # The spawned one remains (duplicate prevention is hard without strict checking).
        # We will assume the user handles duplicates or we implement advanced logic later.
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

def spawn_missing_recurring_tasks(session: Session, user_id: UUID) -> None:
    """
    Check for recurring tasks that should have been spawned but weren't.
    Ensures that if a user misses a day, the task for today/tomorrow still appears.
    Debounced to run at most once every 5 minutes per user.
    """
    global _last_recurrence_check
    
    now_utc = datetime.now(timezone.utc)
    last_check = _last_recurrence_check.get(user_id)
    
    # Debounce: If checked in last 1 minutes, skip (to allow UI to load fast)
    if last_check and (now_utc - last_check) < timedelta(minutes=1):
        return

    _last_recurrence_check[user_id] = now_utc

    # 1. Get the latest task for each recurring group
    # We need to find tasks that are recurring, and for each group, find the one with the max due_date.
    
    # Efficient strategy: Get ALL recurring tasks, handle logic in Python (acceptable for Todo app scale)
    statement = select(Task).where(
        Task.user_id == user_id, 
        Task.recurrence != None, 
        Task.recurrence != "none" # String check for enum in DB if needed, but safer to rely on Enum or NotNone
    )
    recurring_tasks = session.exec(statement).all()
    
    # 2. Group by recurrence_group_id
    from collections import defaultdict
    groups = defaultdict(list)
    
    for task in recurring_tasks:
        # If no group_id, use own id (singleton start)
        gid = task.recurrence_group_id if task.recurrence_group_id else task.id
        groups[gid].append(task)
        
    start_of_today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    
    # 3. Check each group's latest task
    for gid, group_tasks in groups.items():
        # Sort by due_date descending
        # Filter out tasks with no due_date (shouldn't happen for recurring usually, but safety first)
        valid_tasks = [t for t in group_tasks if t.due_date]
        if not valid_tasks:
            continue
            
        latest_task = sorted(valid_tasks, key=lambda t: t.due_date, reverse=True)[0]
        
        # If latest task's due date is in the past (before today logic depending on granularity), spawn next.
        # Logic: If latest_task.due_date < now, we need to spawn until we reach future.
        
        current_check_date = latest_task.due_date
        
        # Safety limit: don't spawn more than 10 instaces at once to prevent infinite loops/floods
        spawns = 0
        max_spawns = 30 # Cap at a month of dailies
        
        # While the latest scheduled date is before "now" (plus a buffer?), spawn the next one.
        # Actually, user said: "create a new task tomorrow at same time".
        # So we just ensure there is a task for the *current* or *next* slot.
        # Let's simple fill the gap up to "tomorrow".
        
        now = datetime.utcnow()
        
        from ..models.task import RecurrenceEnum
        
        while current_check_date < now and spawns < max_spawns:
            # Calculate next date
            next_date = None
            if latest_task.recurrence == RecurrenceEnum.DAILY:
                next_date = current_check_date + timedelta(days=1)
            elif latest_task.recurrence == RecurrenceEnum.WEEKLY:
                next_date = current_check_date + timedelta(weeks=1)
            elif latest_task.recurrence == RecurrenceEnum.MONTHLY:
                next_date = current_check_date + timedelta(days=30)
            
            if not next_date:
                break
                
            # Update check date for loop
            current_check_date = next_date
            
            # Spawn logic
            # Ensure group ID is set on the new task (and potentially the old one if it was missing?)
            group_id_to_use = latest_task.recurrence_group_id
            if not group_id_to_use:
                # If the parent didn't have one, we generate one now for the new task.
                # (For strictness we should update parent, but let's just use parent.id matching logic above)
                # Better: Generate a new UUID if missing, but we can't easily retroactively update the group 
                # without iterating. Let's make sure new tasks share a common ID.
                # If gid matches latest_task.id, it means latest_task was the "root" without a group_id.
                # Use latest_task.id as the group_id for children to keep them linked.
                group_id_to_use = latest_task.id 
                
            new_task = Task(
                title=latest_task.title,
                description=latest_task.description,
                completed=False,
                priority=latest_task.priority,
                label=latest_task.label,
                due_date=next_date,
                recurrence=latest_task.recurrence,
                recurrence_group_id=group_id_to_use, 
                user_id=user_id,
                tags=latest_task.tags 
            )
            session.add(new_task)
            
            # Commit the new task first
            session.commit()
            session.refresh(new_task)
            
            # Create notification
            try:
                notification = Notification(
                    user_id=user_id,
                    type=NotificationType.RECURRING_SPAWNED,
                    message=f"Missed recurring task '{new_task.title}' has been auto-scheduled for {new_task.due_date.strftime('%Y-%m-%d')}.",
                    task_id=new_task.id
                )
                session.add(notification)
                session.commit()
            except Exception as e:
                print(f"ERROR CREATING SPAWN NOTIFICATION: {e}")
                session.rollback()
            
            spawns += 1
            
            # Continue loop to see if we need another one (e.g. missed 3 days)
            
    if session.new:
        session.commit()

from ..database.database import engine
from sqlmodel import Session

def run_spawn_recurring_tasks_background(user_id: UUID):
    """
    Background worker to spawn recurring tasks.
    Creates its own session to ensure isolation from the request lifecycle.
    OPTIMIZED: Checks debounce cache BEFORE creating session to save resources.
    """
    try:
        # Check debounce BEFORE opening session
        now_utc = datetime.now(timezone.utc)
        last_check = _last_recurrence_check.get(user_id)
        if last_check and (now_utc - last_check) < timedelta(minutes=1):
            return

        with Session(engine) as session:
            spawn_missing_recurring_tasks(session, user_id)
    except Exception as e:
        print(f"BACKGROUND WORKER ERROR (spawn_recurring): {e}")

def check_upcoming_reminders():
    """
    Background task to check for tasks due within the next 10 minutes.
    If found, and no notification exists, create one.
    """
    try:
        with Session(engine) as session:
            now = datetime.now(timezone.utc)
            # Logic: Notify for any task due in the next 10 minutes (and hasn't been notified yet)
            # This covers tasks due in 1m, 5m, 10m.
            
            target_limit = now + timedelta(minutes=10)
            
            # We also verify due_date > now to avoid notifying for already overdue tasks (assuming overdue has its own logic)
            # Or maybe we include them? User said "before 10minutes of task time ending".
            
            statement = select(Task).where(
                Task.due_date > now,
                Task.due_date <= target_limit,
                Task.completed == False
            )
            tasks_due_soon = session.exec(statement).all()
            
            if tasks_due_soon:
                print(f"[Reminders] Found {len(tasks_due_soon)} tasks due soon.")

            for task in tasks_due_soon:
                # Check if we already notified for this specific "due soon" event
                from ..models.notification import Notification, NotificationType
                
                # We interpret "task_due_soon" as the unique key for this 10-min warning.
                existing_notif = session.exec(
                    select(Notification).where(
                        Notification.task_id == task.id,
                        Notification.type == NotificationType.TASK_DUE_SOON
                    )
                ).first()
                
                if not existing_notif:
                    # Create notification
                    time_diff = task.due_date - now
                    minutes_left = int(time_diff.total_seconds() / 60)
                    
                    notif = Notification(
                        user_id=task.user_id,
                        type=NotificationType.TASK_DUE_SOON,
                        message=f"Reminder: Task '{task.title}' is due in {minutes_left} minutes!",
                        task_id=task.id
                    )
                    session.add(notif)
                    session.commit()
                    print(f"[Reminders] Created notification for task {task.id}")

    except Exception as e:
        print(f"REMINDER WORKER ERROR: {e}")
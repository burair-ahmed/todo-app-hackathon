# Feature Specification: Recurring Tasks & Time Reminders

## 1. Recurring Tasks
### Requirements
- Users can set a recurrence pattern: `Daily`, `Weekly`, `Monthly`, `None`.
- When a recurring task is marked "done", a new instance is created for the next occurrence, or the current task's due date is updated.
- *Decision*: We will update the `due_date` of the existing task to the next occurrence to keep the task list clean, unless the user requests a "history" feature later.

### Data Model Changes
- `recurrence`: Enum (`none`, `daily`, `weekly`, `monthly`)
- `last_completed_at`: Timestamp (to track when it was last finished)

## 2. Due Dates & Time Reminders
### Requirements
- `due_date`: Optional Timestamp field.
- **UI**: A modern Date/Time picker in the `TaskForm`.
- **Reminders**: Browser Notification API integration.
- **Checking Logic**: Frontend will poll or use a timeout to trigger notifications for tasks due within the next minute.

### API Changes
- `GET /api/tasks`: Add `overdue` and `upcoming` filters.
- `POST /api/tasks`: Accept `due_date` and `recurrence`.

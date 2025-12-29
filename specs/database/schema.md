# Database Schema Reference

The database uses PostgreSQL with SQLModel/SQLAlchemy for schema definition.

## Tables

### Users
- `id`: UUID (Primary Key)
- `email`: String (Unique)
- `name`: String
- `hashed_password`: String
- `created_at`: Timestamp

### Tasks
- `id`: UUID (Primary Key)
- `title`: String
- `description`: String
- `priority`: PriorityEnum (low, medium, high)
- `label`: LabelEnum (home, work)
- `completed`: Boolean
- `user_id`: UUID (Foreign Key -> Users)
- `created_at`: Timestamp

### Tags
- `id`: UUID (Primary Key)
- `name`: String (Unique)
- `color`: String (Hex)

### TaskTagLink (Many-to-Many)
- `task_id`: UUID (Foreign Key -> Tasks)
- `tag_id`: UUID (Foreign Key -> Tags)

## Enums
- **PriorityEnum**: `low`, `medium`, `high`
- **LabelEnum**: `home`, `work`

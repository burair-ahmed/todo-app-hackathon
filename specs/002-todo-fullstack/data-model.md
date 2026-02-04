# Data Model: Todo Full-Stack Web Application

## Entity: User
**Fields**:
- id: UUID (Primary Key, auto-generated)
- email: String (Required, unique, validated)
- name: String (Optional)
- created_at: DateTime (Auto-generated)
- updated_at: DateTime (Auto-generated, updated on change)

**Validation rules**:
- Email must be a valid email format
- Email must be unique across all users
- Created_at and updated_at are automatically managed

**Relationships**:
- One-to-Many: User has many Tasks

## Entity: Task
**Fields**:
- id: UUID (Primary Key, auto-generated)
- title: String (Required, max 200 characters)
- description: String (Optional, max 1000 characters)
- completed: Boolean (Default: false)
- user_id: UUID (Foreign Key to User)
- created_at: DateTime (Auto-generated)
- updated_at: DateTime (Auto-generated, updated on change)

**Validation rules**:
- Title is required and cannot be empty
- Title must be between 1 and 200 characters
- Description, if provided, must be less than 1000 characters
- User_id must reference an existing user
- Only the task owner can modify the task

**Relationships**:
- Many-to-One: Task belongs to one User

## State Transitions

### Task Completion
- Initial state: completed = false
- Transition: User toggles completion status
- Final state: completed = true (or false if toggling back)
- Validation: Only task owner can perform this transition

### Task Data Modification
- Initial state: Task with specific title/description
- Transition: User updates title/description
- Final state: Updated task data
- Validation: Only task owner can perform this transition

## Database Schema

### Users Table
```
users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
)
```

### Tasks Table
```
tasks (
  id UUID PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  completed BOOLEAN DEFAULT FALSE,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
)
```

## Constraints
- Foreign key constraint: tasks.user_id references users.id
- Cascade delete: When a user is deleted, all their tasks are also deleted
- Index on user_id in tasks table for efficient filtering
- Unique constraint on email in users table
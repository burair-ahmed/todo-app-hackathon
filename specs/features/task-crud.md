# Feature Spec: Task CRUD

The Task CRUD (Create, Read, Update, Delete) system is the core of the application, featuring advanced categorization and ownership rules.

## Operations

### 1. Create
- **Input**: Title, Description (optional), Priority (LOW/MEDIUM/HIGH), Label (HOME/WORK), Tags.
- **Ownership**: The authenticated user's ID is automatically injected from the JWT `sub` claim.
- **Validation**: Title is required; Label and Priority defaults are handled by the backend.

### 2. Read (Querying)
- **Scoped**: Users can *only* see their own tasks.
- **Filtering**:
  - `search`: Case-insensitive partial matching on titles.
  - `priority`: Filtering by priority level.
  - `label`: Contextual filtering (Home/Work).
  - `tag_id`: Filtering by custom categories.
  - `completed`: Toggle between active and finished tasks.
- **Sorting**: Support for `created_at`, `title`, and `priority` in `asc` or `desc` order.

### 3. Update & Patch
- **Full Update (PUT)**: Replaces all task fields.
- **Partial Update (PATCH)**: Modifies only specific fields (e.g., toggling completion, updating title).

### 4. Delete
- **Security Check**: Verification that the task belongs to the user before permanent deletion.
- **Cascading**: Associated tag links are handled via the `tasktaglink` table.

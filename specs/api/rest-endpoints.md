# API Reference: REST Endpoints

All API endpoints are prefixed with `/api` and require a `Bearer <token>` in the Authorization header except for registration and login.

## Authentication
- `POST /api/auth/register`: Create a new user account.
- `POST /api/auth/login`: Authenticate and receive a JWT.
- `GET /api/auth/me`: Retrieve current user details from token.

## Tasks
- `GET /api/tasks`: List user tasks (with search, filter, sort).
- `POST /api/tasks`: Create a new task.
- `GET /api/tasks/{id}`: Get task details.
- `PUT /api/tasks/{id}`: Replace task.
- `PATCH /api/tasks/{id}`: Partial update.
- `PUT /api/tasks/{id}/toggle`: Toggle completion status.
- `DELETE /api/tasks/{id}`: Remove task.

## Tags
- `GET /api/tags`: List all available tags.
- `POST /api/tags`: Create a new tag.
- `DELETE /api/tags/{id}`: Remove a tag.
